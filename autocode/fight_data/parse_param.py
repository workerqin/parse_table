# -*- coding: utf-8 -*-

import xlrd
import sys
import getopt
import re
import string
import codecs
from datetime import datetime
from Python2Py import PythonData2Py

dicKeys = {
	# 说明表格名字
	"comment_sheet"      : u"说明",
	# 变量表所在sheet
	"param_sheet"       : u"变量表",
	# 战斗数值
	"param_type_fight"  : u"战斗数值",
	# 战士数值
	"param_type_warrior"  : u"战士数值",
	# 战士变量
	"param_type_warrior_data"  : u"战士变量",
	# 战士只读变量
	"param_type_warrior_RO"  : u"战士只读变量",
	# 战士扩展变量
	"param_type_warrior_ext"  : u"战士扩展变量",
	# 战场扩展变量
	"param_type_fight_ext"  : u"战斗扩展变量",
	# AI变量
	"param_type_ai"  : u"AI变量",
	# 程序变量
	"param_program"  : u"程序",
}

TARGET_STRING = "$target"
KEY_STRING = "$key"
VALUE_STRING = "$value"
VS_STRING = "$vstatus"

begin = "# -------------------  Auto Generate Begin --------------------"
end   = "# -------------------  Auto Generate End   --------------------\n"
replace_pattern  = re.compile(begin + r".*?" + end, re.S | re.M)

dicPrograms = {
	u"战斗数值" : [ "GET_FV( fightId, " + KEY_STRING + " )", "", ],
	u"战士数值" : [ "GET_WV( fightId, " + TARGET_STRING + ", " + KEY_STRING + " )", 
					"SET_WV( fightId, " + TARGET_STRING + ", " + KEY_STRING + ", " + VALUE_STRING + " )",  
					"SET_TMP_WV( fightId, " + TARGET_STRING + ", " + VS_STRING + ", " + KEY_STRING + ", " + VALUE_STRING + " )",  
				  ],
	u"战士只读数值" : [ "GET_WV( fightId, " + TARGET_STRING + ", " + KEY_STRING + " )", "" ],
	u"战士变量" : [ "GET_WD( fightId, " + TARGET_STRING + ", " + KEY_STRING + " )", "" ],
	u"战士只读变量" : [ "GET_WD( fightId, " + TARGET_STRING + ", " + KEY_STRING + " )", "" ],
	u"战士扩展变量" : [ "GET_WEV( fightId, " + TARGET_STRING + ", " + KEY_STRING + " )", "SET_WEV( fightId, " + TARGET_STRING + ", " + KEY_STRING + ", " + VALUE_STRING + " )" ],
	u"战斗扩展变量" : [ "GET_FEV( fightId, " + KEY_STRING + " )", "SET_FEV( fightId, " + KEY_STRING + ", " + VALUE_STRING + " )" ],
}

def write_file(filename, content ):
	msg = "writting to file",filename

	try :
		f = file(filename, "w+b")
	except :
		msg = "can not write to", filename
		sys.exit(-1)
	
	f.write(content.encode("utf-8"))
	f.close()

def usage():
	print "USAGE:parse_param.py root_path excel_file 输出文件名 "
	print '''
	--version : Prints the version number
	-h --help    : Display this help'''

def get_str_from_sheet( sheet, row, col ):
	value = sheet.cell_value(rowx=row, colx=col)
	
	if  isinstance(value, float):
		return str(int(value))
	
	if  isinstance(value, int):
		return str(value)

	return value
	
def parse_param_sheet( sh, tbParam, inParseParam=1 ):
	
	for i in range(1, sh.nrows):
		cehuaParam = get_str_from_sheet( sh, i, 0 )
		comment = get_str_from_sheet( sh, i, 1 )
		paramType = get_str_from_sheet( sh, i, 2 )
		key = get_str_from_sheet( sh, i, 3 )
		readMethod = get_str_from_sheet( sh, i, 4 )
		writeMethod = get_str_from_sheet( sh, i, 5 )
		
		tmpTb = {}
		tbParam[cehuaParam] = tmpTb
		
		
		if paramType == dicKeys["param_type_fight"]:
			
			#dicPrograms
			tmpTb["type"] = paramType
			
			tmpTb["read"] = dicPrograms[paramType][0].replace(KEY_STRING, key)
			tmpTb["write"] = ""
			continue	
		if paramType == dicKeys["param_type_warrior"]:
			
			#dicPrograms
			tmpTb["type"] = paramType
			
			tmpTb["read"] = dicPrograms[paramType][0].replace(KEY_STRING, key)
			tmpTb["write"] = dicPrograms[paramType][1].replace(KEY_STRING, key)
			tmpTb["temp_write"] = dicPrograms[paramType][2].replace(KEY_STRING, key)
			
			continue
		if paramType == dicKeys["param_type_warrior_data"]:
			
			#dicPrograms
			tmpTb["type"] = paramType
			
			tmpTb["read"] = dicPrograms[paramType][0].replace(KEY_STRING, key)
			tmpTb["write"] = ""
			
			continue
		if paramType == dicKeys["param_type_warrior_RO"]:
			
			#dicPrograms
			tmpTb["type"] = paramType
			
			tmpTb["read"] = dicPrograms[paramType][0].replace(KEY_STRING, key)
			tmpTb["write"] = ""
			
			continue
		if paramType == dicKeys["param_type_warrior_ext"]:
			
			#dicPrograms
			tmpTb["type"] = paramType
			
			if (inParseParam == 1):
				tmpTb["read"] = dicPrograms[paramType][0].replace(KEY_STRING, '\\"%s\\"'%key)
				tmpTb["write"] = dicPrograms[paramType][1].replace(KEY_STRING, '\\"%s\\"'%key)
			else:
				tmpTb["read"] = dicPrograms[paramType][0].replace(KEY_STRING, '"%s"'%key)
				tmpTb["write"] = dicPrograms[paramType][1].replace(KEY_STRING, '"%s"'%key)

			continue

		if paramType == dicKeys["param_type_fight_ext"]:
			#dicPrograms
			tmpTb["type"] = paramType
			
			if (inParseParam == 1):
				tmpTb["read"] = dicPrograms[paramType][0].replace(KEY_STRING, '\\"%s\\"'%key)
				tmpTb["write"] = dicPrograms[paramType][1].replace(KEY_STRING, '\\"%s\\"'%key)
			else:
				tmpTb["read"] = dicPrograms[paramType][0].replace(KEY_STRING, '"%s"'%key)
				tmpTb["write"] = dicPrograms[paramType][1].replace(KEY_STRING, '"%s"'%key)

			continue
		
		if paramType == dicKeys["param_program"]:
			
			#dicPrograms
			tmpTb["type"] = paramType
			
			tmpTb["read"] = readMethod
			tmpTb["write"] = writeMethod
			continue
def parse_xls(filename, outputfile):
	try :
		book = xlrd.open_workbook(filename)
	except :
		msg = "can't open file?", filename
		usage()
		sys.exit(-1)
	
	tbParam = {}
	
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		print sh.name.encode('utf-8')
		# 不处理说明表格
		if sh.name == dicKeys.get("comment_sheet"):
			continue
                # 变量表
                elif sh.name == dicKeys.get("param_sheet"):
                	parse_param_sheet( sh, tbParam )
			continue
	
	# 尝试读取outputfile
	try:
		file = codecs.open(outputfile, "rb", "utf-8")
		main_py = file.read()
		if ( len( main_py ) == 0):
			main_py = begin + "\n\n" + end
		file.close()
	except IOError:
		main_py = begin + u"\n\n" + end
	
	new_src = "dicParams = %s"%(PythonData2Py(tbParam, True, 0))
	
	tmp = replace_pattern.sub(begin + "\n" + new_src + "\n" + end, main_py)
	
	write_file( outputfile, tmp )
		
def main():
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
		outputFile = rootPath + "/" + args[2]	
	

	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		raise
		#sys.exit(2)

	print execelFile,outputFile

	parse_xls( execelFile, outputFile)

if __name__ == "__main__":
	main()
