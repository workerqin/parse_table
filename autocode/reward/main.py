# -*- coding: utf-8 -*-
# 

import xlrd
import sys
import getopt
import re
import string
import codecs
from datetime import datetime
from Python2Lpc import PythonData2Lpc

from common import get_str_from_sheet
from common import get_str_array_from_sheet
from common import get_int_from_sheet
from common import get_map_from_sheet
from common import write_file
from common import parse_function
from common import parse_expr_right
from common import replace_str
from common import filter
from common import write_src

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

version = "1.00"

def usage():
	print "USAGE:main.py root_path excel_file 输出目录"
	print '''
	--version : Prints the version number
	-h --help    : Display this help'''

dicVar = {}

begin = u"//----------------------- Auto Genrate Begin --------------------"
end   = u"//----------------------- Auto Genrate End   --------------------\n"

strRewardTemplete = u'''
#include <reward.h>

inherit REWARD_BASE;

#include <var_prop.h>

// 属性区
// -----------------------------------------
%s
// -----------------------------------------

// 自动生成函数区域
// -----------------------------------------
%s
// -----------------------------------------

// 奖励表
static mapping lootTable = %s;
RESET_ONUPDATE_VAR(LootTable, lootTable)
'''

srcFuncTemplete = u'''
// %s
int %s(int lv, mapping mpParam)
{
	mixed result = %s;
	return to_int(result);
}
'''

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

	# 打印解析结果
	#print(PythonData2Lpc(dicVar, True))

def parse_sheet(sh, outputpath):
	# 读取奖励表
	print sh.name

	startRow = get_int_from_sheet(sh, 3, 1) - 1
	rRewardId = get_str_from_sheet(sh, 0, 5)
	rType = get_str_from_sheet(sh, 4, 4)

	endRow = sh.nrows

	srcAttr = u""

	srcAttr += u'''
RESET_ONUPDATE_VAR(Id, %s)
'''%PythonData2Lpc(rRewardId)
	srcAttr += u'''
RESET_ONUPDATE_VAR(Type, TB_TYPE_%s)
'''%rType

	srcFunction = u""

	rewardData = {}
	for row in range(startRow, endRow):
		#序号	类型	名字	类型ID	数量	概率	商会公告   公告	   说明
		#reward_no(str)	type(str)		id(int)	cnt(int)	rate(int)		memo(str)
		#reward_no(str)	type(str)		id(int)	cnt(int)	rate(int)	group_gonggao(str)   gonggao(str)	memo(str)    condition(str)
		no = get_str_from_sheet(sh, row, 0 )
		rTypeName = get_str_from_sheet(sh, row, 1 )
		rType = get_str_from_sheet(sh, row, 2 )
		rName = get_str_from_sheet(sh, row, 3 )
		rId = get_str_from_sheet(sh, row, 4 )
		if (rId != "" and not rId.isdigit()):
			funcName = u"CalcId%s"%no
			expTmp = parse_expr_right(rId, dicVar, 0, {})
			srcTmp = srcFuncTemplete%("奖励ID计算函数,只为公会红包准备", funcName, expTmp[1])

			srcFunction += srcTmp

			rId = "@@%s"%funcName
		else:
			if ( rId == ""):
				rId = 0
			else:
				rId = int(rId)

		rAmount = get_str_from_sheet(sh, row, 5 )
		rRate = get_int_from_sheet(sh, row, 6)

		# 商会公告(目前应该没用)
		rGroupGonggao = get_str_array_from_sheet(sh, row, 7)
		if( len(rGroupGonggao) > 0 ):
			rGroupGonggao[0] = int(rGroupGonggao[0])

		# 公告 = 世界公告;商会公告;系统提示
		rGonggao = get_str_from_sheet(sh, row, 8)
		gonggaos = []
		if (len(rGonggao) > 0):
			gonggaos = rGonggao.split(";")
			if (len(gonggaos) != 3):
				raise Exception("奖励公告格式错误")
			i = 0
			for gonggao in gonggaos:
				gonggaos[i] = gonggao.split(",")
				if len(gonggao) > 0:
					gonggaos[i] = gonggao.split(",")
					gonggaos[i][0] = int(gonggaos[i][0])
				else:
					gonggaos[i] = []
				i += 1

		rMemo = get_str_from_sheet(sh, row, 10)
		rArgs = get_map_from_sheet(sh, row, 9)
		rCnd = ""

		if (rAmount != "" and not rAmount.isdigit()):
			funcName = u"CalcAmount%s"%no
			expTmp = parse_expr_right(rAmount, dicVar, 0, {})
			srcTmp = srcFuncTemplete%("奖励数量计算函数", funcName, expTmp[1])

			srcFunction += srcTmp

			rAmount = "@@%s"%funcName
		else:
			if (rAmount == ""):
				rAmount = 0
			else:
				rAmount = int(rAmount)


		if ( sh.ncols > 11 ):
			rCnd = get_str_from_sheet(sh, row, 11)
			if ( len(rCnd) ):
				funcName = u"Condition%s"%no

				expTmp = parse_expr_right(rCnd, dicVar, 0, {})
				srcTmp = srcFuncTemplete%(u"条件函数", funcName, expTmp[1])
	
				srcFunction += srcTmp

				rCnd = "@@%s"%funcName

		rewardData[no] = (rType, rName, rId, rAmount, rRate, gonggaos, rMemo, rCnd, rGroupGonggao, rArgs); 

	
	srcAll = strRewardTemplete%(srcAttr, srcFunction, PythonData2Lpc(rewardData, True, 2, 2));

	print(srcAll);
	output_file = outputpath + "%s.c"%rRewardId
	print(output_file)
	write_src(output_file, begin, end, srcAll, "utf-8")

def parse_xls(filename, outputpath):
	try :
		book = xlrd.open_workbook(filename)
	except :
		msg = "can't open file?", filename
		usage()
		sys.exit(-1)

	# 保证先处理扩展数值表
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		if sh.name == u"变量表":
			parse_var_sheet(sh, dicVar)
			continue
	print dicVar

	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		#print(sh.name, sheetname.decode("utf-8"))
		if sh.ncols < 3:
			continue;
		# 判断是否奖励表
		if get_str_from_sheet(sh, 0, 4) != u"奖励表" :
			continue;
		parse_sheet(sh, outputpath)
		continue


if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
		for o, a in opts:
			if o == "-v":
				print version	
				sys.exit()
			elif o in ("-h", "--help"):
				usage()
				sys.exit()
			elif o in ("-o", "--output"):
				output = a
			else:
				assert False, "unhandled option"
		if (len(args) < 3):
			usage()
			sys.exit(-1)
		rootPath = args[0]
		execelFile = args[1]	
		outputPath = rootPath + args[2]	

	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		raise
		#sys.exit(2)

	print execelFile,outputPath

	try :
		parse_xls( execelFile, outputPath)
	except:
		raise


