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

# 变量表
dicVar = {}

def parse_sheet(sh, dicVar):
	for row in range(11, sh.nrows):
		key = get_str_from_sheet(sh, row, 1)
		if len(key) == 0:
			continue
		dec = get_str_from_sheet(sh, row, 2)
		value = get_int_from_sheet(sh, row, 0)
		valueAndDec = {}
		valueAndDec["key"] = key 
		valueAndDec["dec"] = dec 
		dicVar[value] = valueAndDec
	#print dicVar

def parse_xls(filename, sn, output_path):
	try:
		book = xlrd.open_workbook(filename)
	except:
		msg = u"can't open file? %s"%filename
		print( msg )
		raise
		
	# 遍历xls
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		sheetname = sh.name
		if sheetname == u"提示":
			parse_sheet(sh, dicVar)

DEFINE_HEAD = u"#define"
	

begin = u"//----------------------- Auto Genrate Begin --------------------\n"
end = u"//----------------------- Auto Genrate End   --------------------\n"
ifndef = u"#ifndef __SERVER_MAS__\n"
define = u"#define __SERVER_MAS__\n"
endif = u"#endif\n"
def write_file(filename):
	try :
		f = file(filename, "w+b")
	except :
		msg = "\rcan not write to " + filename
		print msg
		raise()
		#sys.exit(-1)
	#print "\r write file %s success"%(filename)
	f.write(begin + "\n")
	f.write(ifndef + "\n")
	f.write(define + "\n")
	ids = dicVar.keys()
	ids.sort()
	for id in (ids):
		valueData = dicVar[id]
		key = valueData["key"]
		f.write("//" + valueData["dec"] + "\n" + DEFINE_HEAD + " " + key + " " + str(id) + "\n")
	f.write(endif + "\n")
	f.write(end + "\n")
	f.close()



if __name__ == "__main__":
	root_path = sys.argv[1]
	filename = sys.argv[2]
	sheetname = sys.argv[3]
	output_path = sys.argv[4]

	sys.path.append(root_path + "tools/autocode/")
	PARSE = __import__("TemplateParse")
	UTIL = __import__("Util")

	# 解析xls
	parse_xls( filename, sheetname, output_path )
	write_file(output_path)
