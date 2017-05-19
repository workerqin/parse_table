# -*- coding:utf-8 -*-

import sys
import re
import xlrd

from common import get_str_from_sheet
from common import get_int_from_sheet
from common import write_file
from common import parse_function

from Python2Lpc import PythonData2Lpc

reload(sys)
sys.setdefaultencoding( "utf-8" )


# 变量表
dicVar = {}

srcSailorTemplete = u'''

#include <role.h>

inherit ROLE_BASE;

#include <var_prop.h>
#include <common_key.h>

// 基本信息
%s

// 中间变量
%s


// 人物基本属性
void GetRoleBaseAttr(object oUser, mapping mpBase)
{
	int lv = oUser->GetGrade();

%s
}

// 计算精英属性
// 返回千分率，比如0.123返回123，因为要显示百分率并保留小数点后1位
void CalcEliteAttr(object oUser, int lv, mapping mpBase)
{
	//int lv = oUser->GetGrade();

%s
}

'''

begin = u"//----------------------- Auto Genrate Begin --------------------\n"
end = u"//----------------------- Auto Genrate End   --------------------\n"
p = re.compile(begin + r".*?" + end, re.S | re.M)

attrSrc = u'''RESET_ONUPDATE_VAR(%s, %s)'''
intermediateSrc = u'''static float %s = %s;'''

headExp = re.compile(r"(?P<var_name>\w+)\((?P<var_type>\w+)\)")

# 使用方法
def usage():
	print """
	USAGE:python main.py root_path 角色.xls sheet_name output_path
		--version : Prints the version number
		--help    : Display this help
	"""


def parse_sailor_sheet(sh, output_path):
	startRow = get_int_from_sheet( sh, 3, 1 ) - 1
	headRow = startRow - 1
	print( "startRow = %d"%startRow )
	print( "headRow = %d"%headRow )

	for row in range(startRow, sh.nrows):
		roleId = get_str_from_sheet(sh, row, 0)
		baseVarList = []
		baseSrcLst = []
		intermediateList = []
		eliteSrcLst = []
		for col in range(0, sh.ncols):
			head = get_str_from_sheet(sh, headRow, col )
			if (len(head) == 0):
				continue
			data = get_str_from_sheet(sh, row, col )
			if (len(data) == 0):
				continue

			if (head == u"formula"):
				note = get_str_from_sheet(sh, headRow-2, col )
				# TODO:打断公式取左值，看看是那种类型的变量
				eqCharIdx = data.find(u"=")
				#lrSplit = re.compile(u'[=＝]{1}')

				if eqCharIdx != -1:
					lvalue = data[0 : eqCharIdx]
					lvalue = lvalue.strip()

				src = parse_function(data, note, "", dicVar, "\t// %s%s%s" );
				if dicVar[lvalue]["var_type"] == u"人物基本属性":
					baseSrcLst.append(src);
				if dicVar[lvalue]["var_type"] == u"人物精英属性":
					eliteSrcLst.append(src);

				continue

			tmp = headExp.match(head)
			if tmp == None:
				continue

			var_name = tmp.group("var_name")
			var_type = tmp.group("var_type")

			baseFlag = 0
			intermediateFlag = 0
			intermediateVar = ""
			baseVar = ""
			if var_type == "intermediate":
				intermediateFlag = 1
				intermediateVar = int(data) / 100.0
			if var_type == "int":
				baseFlag = 1
				baseVar = int(data)
			if var_type == "string":
				baseFlag = 1
				baseVar = data
			if var_type == "array":
				baseFlag = 1
				baseVar = [] 
				tmpLst = data.split(",")
				for tmp in tmpLst:
					baseVar.append(int(tmp))

			srcAttr = attrSrc % (var_name, PythonData2Lpc(baseVar))
			srcIntermediate = intermediateSrc % (var_name, PythonData2Lpc(intermediateVar))

			if baseFlag:
				baseVarList.append(srcAttr)
			if intermediateFlag:
				intermediateList.append(srcIntermediate)

		if roleId != "":
			filename = "%s/%s.c"%(output_path, roleId)
			filecontent = srcSailorTemplete%(
				u"\n".join(baseVarList)	,
				u"\n".join(intermediateList)	,
				u"\n".join(baseSrcLst)	,
				u"\n".join(eliteSrcLst)	,
			)
			try:
				src_data = open(filename, "rb").read()
				if len(src_data) == 0:
					src_data = begin + "\n\n" + end
			except IOError:
				src_data = begin + "\n\n" + end

			tmp = p.sub(begin + "\n" + filecontent + "\n" + end, src_data)

			write_file(filename, tmp)


def parse_var_sheet(sh):
	for row in range(1, sh.nrows):
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
				elif head == u"变量类型":
					var_type = get_str_from_sheet(sh, row, col)
					dicVar[key]["var_type"] = var_type 
				else:
					continue

# 导整个表
def parse_xls(filename, sn, output_path):
	try:
		book = xlrd.open_workbook(filename)
	except:
		msg = u"can't open file? %s"%filename
		print(msg)
		usage()
		raise

	# 遍历xls
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		sheetname = sh.name
		# 优先导变量表
		if sheetname == u"变量表":
			parse_var_sheet(sh)

	# 导水手表
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		sheetname = sh.name

		if sheetname != sn:
			continue

		print("to parse sheet", sn)

		parse_sailor_sheet(sh, output_path)


if __name__ == "__main__":
	argv_len = len(sys.argv)
	if argv_len < 5:
		usage()
	else:
		root_path = sys.argv[1]
		filename = sys.argv[2]
		sheetname = sys.argv[3]
		output_path = sys.argv[4]

		# 解析xls
		parse_xls( filename, sheetname, output_path )
