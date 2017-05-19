# -*- coding:utf-8 -*-

import sys
import os
import glob
import getopt
import re
import xlrd
import string
from common import get_str_from_sheet
from common import get_int_from_sheet
from common import write_file
from common import parse_function
from common import replace_str
from common import filter
from common import PythonData2Lua
from common import write_src

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

# 变量表
dicVar = {}

# 使用方法
def usage():
        print '''
        USAGE:python main.py root_path 技能.xls sheet_name output_file
          --version : Prints the version number
          --help    : Display this help
'''

# 函数格式
srcSkillFormla = u'''
// %s
mapping %s (int lv, int quality)
{
	mapping tbResult = {};
%s
	return tbResult;
}
'''

begin = u"//----------------------- Auto Genrate Begin --------------------\n"
end = u"//----------------------- Auto Genrate End   --------------------\n"


# 技能变量策划使用表的解析
def parse_var_sheet(sh, dicVar):
        for row in range(1, sh.nrows):
                key = ""
                for col in range(0, sh.ncols):
                        head = get_str_from_sheet(sh, 0, col)

                        if head == u"策划用名":
                                key = get_str_from_sheet(sh, row, col)
                                dicVar[key] = {}

                        else:
                                if head == u"程序变量获取":
                                        get_var = get_str_from_sheet(sh, row, col)
                                        dicVar[key]["get_func"] = get_var
                                elif head == u"程序变量设置":
                                        set_var = get_str_from_sheet(sh, row, col)
                                        dicVar[key]["set_func"] = set_var
                                elif head == u"变量名":
                                        name = get_str_from_sheet(sh, row, col)
                                        dicVar[key]["var_name"] = name
                                elif head == u"备注":
                                        desc = get_str_from_sheet(sh, row, col)
                                        dicVar[key]["var_desc"] = desc
                                else:
                                        continue



def parse_formula_sheet(sh, output_file):

		all_fun = begin
		for row in range(2, sh.nrows):
				skill_id_str = get_str_from_sheet(sh, row, 0)
				skill_name_str = get_str_from_sheet(sh, row, 1)
				skill_formula_str = get_str_from_sheet(sh, row, 2)
				fun_str = parse_function(skill_formula_str, u"技能名："+skill_name_str, u"ser_%s" % skill_id_str, dicVar, srcSkillFormla)
				all_fun += fun_str
			#	src_file = path + "/" + skill_id_str + ".c"
			#	write_src(output_file, begin, end, fun_str, "utf-8")
		all_fun += end
		write_file(output_file, all_fun)



# 导整个表
def parse_xls(filename, sn, output_file):

	try :
	# 打开excel文件
			book = xlrd.open_workbook(filename)
	except :
			msg = "can't open file?", filename
			#my_echo( msg, dictDebugLevel.get("ERROR") )
			print msg
			usage()
			raise

	# 先处理变量表
	for x in xrange(book.nsheets):
			sh = book.sheet_by_index(x)
			sheetname = sh.name
			if sheetname == u"服务端变量表":
					parse_var_sheet(sh, dicVar)
					break
	# 再处理公式表
	for x in xrange(book.nsheets):
			sh = book.sheet_by_index(x)
			sheetname = sh.name
			if sheetname == u"公式表":
					parse_formula_sheet(sh, output_file)
					break


if __name__ == "__main__":
	argv_len = len(sys.argv)

	if argv_len < 5:
		usage()
	else:
		root_path = sys.argv[1]
		filename = sys.argv[2]
		sheetname = sys.argv[3]
		output_file = sys.argv[4]

		#预处理部分代码
		parse_xls(filename, sheetname, output_file)

