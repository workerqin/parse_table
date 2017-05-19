# -*- coding: utf-8 -*-

import xlrd
import sys
import os
import re
import getopt
from common import get_str_from_sheet
from common import get_int_from_sheet
from common import get_str_array_from_sheet
from common import parse_map 
from common import parse_function
from Python2Lpc import PythonData2Lpc
from common import write_src

reload(sys)
sys.setdefaultencoding('utf8')

DEFAULT_ITEM_DIR = "data/item/"

dicVar = {}
ITEM_BASE = "ITEM_BASE"
ITEM_BASE_GIFT = "ITEM_BASE_GIFT"
ITEM_BASE_EXP_BOOK = "ITEM_BASE_EXP_BOOK"
ITEM_BASE_SKILL_BOOK = "ITEM_BASE_SKILL_BOOK"
ITEM_BASE_BAWOU_BOX = "ITEM_BASE_BAWOU_BOX"

sConsume = """
mapping GetConsume(object oUser)
{
    mapping consume = {};
    %s
    return consume;
}
"""

ParseVarTable = {
	"name":["attr", "ItemName",],
	"type":["attr", "ItemType",],
	"exp":["attr", "Exp",],
	"rewards":["attr", "Rewards",],
	"canSell":["func", "CanSell", "int"],
	"sell_get":["attr", "Things"],
	"cansynthetic":["func", "CanSynthesis", "int"],
	"synthetic_num":["attr", "SynthesisNeed"],
	"synthetic_item":["attr", "SynthesisItem"],
	"max limit":["attr", "ItemMaxLimit"],
	"boatId":["attr", "BoatId"],
	"skillIds":["attr", "SkillIds"],
	"consume":["attr", "ConsumeGuide"],
	"LevelLimit":["attr", "LevelLimit"],
	"noblelimit":["attr", "noblelimit"],
    "UseGradeLimit":["attr", "UseGradeLimit"],
}

begin = u"//----------------------- Auto Genrate Begin --------------------"
end   = u"//----------------------- Auto Genrate End   --------------------\n"

SRC_ITEM_TEMPLATE = """

#include <item.h>

inherit %s;

#include <var_prop.h>

%s

"""
def usage():
	print u"USAGE:gen_all_item.py root_path excel_file 输出目录"
	print u'''
	--version : Prints the version number
	-h --help    : Display this help'''



parse_head = re.compile(r"(?P<var>.+)\((?P<type>.+)\)")


def parse_formula(data, sNote):
    eq_index = data.find("=")
    if eq_index == -1:
        return ""
    src = parse_function(data, sNote, "", dicVar, "// %s%s%s");
    return src


def parse_sheet(sh, outputpath):
	headRow = 10
	startRow = 11

	for row in xrange(startRow, sh.nrows):
		itemid = get_int_from_sheet( sh, row, 0 );
		if ( itemid == 0):
			continue;

		itemData = {};
		for col in xrange(1, sh.ncols):
			head = get_str_from_sheet( sh, headRow, col );	
			if ( len(head) == 0):
				continue;

			tmp = parse_head.match(head)

			if ( tmp == None ):
				#print("ERROR:HEAD %s", head)
				#print(tmp)
				continue;

			var = tmp.group("var");
			varType = tmp.group("type");

			if ( varType == 'int'):
				data = get_int_from_sheet(sh, row, col);
				if data == 0 and var != "type":
					continue;
			elif ( varType == 'str'):
				data = get_str_from_sheet(sh, row, col);
				if data == "":
					continue;
			elif ( varType == 'macro'):
				data = "@@%s"%get_str_from_sheet(sh, row, col);
			elif ( varType == 'str_array'):	
				data = get_str_array_from_sheet(sh, row, col);
				if len(data) == 0:
					continue;
			elif ( varType == 'map' ):
				data = parse_map(get_str_from_sheet(sh, row, col))
			elif varType == 'formula':
				sNote = get_str_from_sheet(sh, headRow - 2, col)
				data = parse_formula(get_str_from_sheet(sh, row, col), sNote)
			itemData[var] = data
			
		#print( itemid, itemData )
		itemType = ("%s"%itemData["server_item_base"])

		itemBase = PythonData2Lpc(itemType);
		#print( itemType, itemBase )

		# 处理各种类型的特殊参数
		if ( itemBase == ITEM_BASE_EXP_BOOK ):
			exp = int(itemData["args"]);
			itemData["exp"] = exp
		elif ( itemBase == ITEM_BASE_GIFT ):
			rewards = itemData["args"].split(",")
			itemData["rewards"] = rewards 
		elif ( itemBase == ITEM_BASE_SKILL_BOOK ):
			skillIdStrs = itemData["args"].split(",")
			skillIds = []
			for var in skillIdStrs:
				skillIds += [int(var)]
			itemData["skillIds"] = skillIds
		elif ( itemBase == ITEM_BASE_BAWOU_BOX ):
			rewards = itemData["args"].split(",")
			itemData["rewards"] = rewards 

		srcAttr = u""
		for var in itemData.keys():
			
			if var not in ParseVarTable:
				continue
			info = ParseVarTable[var]

			data = itemData[var]

			if info[0] == u"attr":
				srcTmp = u'''
RESET_ONUPDATE_VAR(%s, %s)
'''%(info[1], PythonData2Lpc(data))

				srcAttr += srcTmp
			elif info[0] == u"func":
				srcTmp = u'''
%s %s()
{
	return %s;
}

'''%(info[2], info[1], PythonData2Lpc(data))

				srcAttr += srcTmp
			elif info[0] == u"formula":
				if data:
				    srcTmp = info[1] % (data)
				    srcAttr += srcTmp


		src = SRC_ITEM_TEMPLATE%(itemBase, srcAttr)

		#print(src)
		filename = "%s/%d.c"%(outputpath, itemid)
		#print( filename )
		write_src( filename, begin, end, src, "utf-8");

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
				elif head == u"更改变量类型":
					var_type = get_str_from_sheet(sh, row, col)
					dicVar[key]["var_type"] = var_type 
				else:
					continue


def parse_xls(filename, sheetname, outputpath):
    try:
        book = xlrd.open_workbook(filename)
    except:
        msg = "can't open file?", filename
        usage()
        sys.exit(-1)

    for x in xrange(book.nsheets):
        sh = book.sheet_by_index(x)
        if sh.name == u"变量表":
            parse_var_sheet(sh, dicVar)

    for x in xrange(book.nsheets):
        sh = book.sheet_by_index(x)
        if sh.name == sheetname.decode("utf-8"):
            parse_sheet(sh, outputpath)


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
		sheetName = args[2]
		outputPath = rootPath + args[3]	

	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		raise
		#sys.exit(2)

	try :
		parse_xls( execelFile, sheetName, outputPath)
	except:
		raise


