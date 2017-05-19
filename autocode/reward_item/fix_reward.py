# -*- coding: utf-8 -*-
""" 物品奖励表
"""

import xlrd
import sys
import getopt
import re
import string
import locale
from datetime import datetime
from Python2Lpc import PythonData2Lpc

version = "1.00"
rootPath = ""

def usage():
	print "USAGE:main.py root_path excel_file 输出路径 "
	print '''
	--version : Prints the version number
	-h --help    : Display this help'''

dicKeys = {
	# 说明表格名字
	"comment_sheet"      : u"说明",
	# 奖励物品名及其对应表
	"map_sheet"      : u"奖励物品名及其对应表",
	# 固定奖励表
	"fix_reward"        : u"固定奖励表",
	# 奖励编号
	"reward_no"         : u"奖励编号",
	# 奖励原因
	"reward_reason"      : u"奖励原因",
	# 奖品名称
	"single_reward_name"        : u"奖品名称",
	# 一次获得奖励投放数量
	"single_reward_cnt"        : u"一次获得奖励投放数量",
	# 属性
	"single_reward_att"        : u"属性",
}

def write_file(filename, content ):
	msg = "writting to file",filename

	try :
		f = file(filename, "w+b")
	except :
		msg = "can not write to", filename
		sys.exit(-1)
	
	f.write(content.encode('gbk'))	
	f.close()


def get_str_from_sheet( sheet, row, col ):
	value = sheet.cell_value(rowx=row, colx=col)
	
	if  isinstance(value, float):
		return str(int(value))
	
	if  isinstance(value, int):
		return str(value)

	return value	

def get_map_from_sheet( sheet, row, col ):
	value = get_str_from_sheet( sheet, row, col )
	
	tmp = {}
	
	if  len(value) == 0:
		return tmp
	
	kvs = value.split(u',')
	
	for kv in kvs:
		kvpairs = kv.split(u':')
		k = kvpairs[0]
		v = kvpairs[1]
		
		if v.startswith(u'"'):
			tmp[k] = v.replace(u'"', u'')
		else:
			tmp[k] = int(v)

	return tmp

def get_int_from_sheet( sheet, row, col ):
	value = sheet.cell_value(rowx=row, colx=col)

	if  isinstance(value, float):
		return int(value)
	
	if  isinstance(value, int):
		return value

	if  value == '':
		return 0
	
	if  isinstance(value, basestring):
		return string.atoi(value)

	return value

def get_float_from_sheet( sheet, row, col ):
	value = sheet.cell_value(rowx=row, colx=col)

	if  isinstance(value, float):
		return (value)
	
	if  isinstance(value, int):
		return value
	
	if  isinstance(value, basestring):
		return string.atof(value)
		
	return value
	
begin = "// -------------------  Auto Generate Begin --------------------"
end   = "// -------------------  Auto Generate End   --------------------\n"
replace_pattern  = re.compile(begin + r".*?" + end, re.S | re.M)


	
#用Book生成代码	
def parse_data_sheet(sh, outputfile):
	
	rewardBegin = 0
	
	allReward = {}
	dictClientDesc = {}
	
	
	for i in range(0, sh.nrows):
		data = get_str_from_sheet(sh, i, 0)
		
		if data == dicKeys.get('reward_no'):
			rewardBegin = i
			continue
	
	for i in range(rewardBegin+3, sh.nrows):
		
		id = get_str_from_sheet(sh, i, 0)
		
		if len(id) == 0:
			continue;

		rewardReason = get_str_from_sheet(sh, i, 1)
		reward_name = get_str_from_sheet(sh, i, 2)
		item_type = get_str_from_sheet(sh, i, 3)
		reward_type = get_str_from_sheet(sh, i, 4)

		prop_key = get_str_from_sheet(sh, i, 5)
		
		allReward[id] = {}
		allReward[id]["reason"] = rewardReason
		allReward[id]["reward_name"] = reward_name 
		allReward[id]["prop_key"] = prop_key
		allReward[id]["reward_type"] = reward_type 
		rewards = {}
		allReward[id]["rewards"] = rewards

		dictClientDesc[id] = {}
		dictClientDesc[id]["item_type"] = item_type 
		dictClientDesc[id]["prop_key"] = prop_key
		dictClientDesc[id]["items"] = {}
		
		
		index = 1
		for j in range( 6, sh.ncols, 4):
			key = get_str_from_sheet(sh, i, j)
			cType = get_str_from_sheet(sh, i, j+1)
			if len(cType) == 0:
				continue
			
			tmp = {}
			if not len(key):
				key = index

			rewards[key] = tmp
				
			tmp["cType"] = cType
			tmp["cnt"] = get_int_from_sheet(sh, i, j+2)
			tmp["attribute"] = get_map_from_sheet( sh, i, j+3 )
			
			index = index + 1
			dictClientDesc[id]["items"][key] = tmp
	
	
	# 尝试读取outputfile
	try:
		file = open(outputfile, "rb")
		lpc_src = file.read()
		if ( len( lpc_src ) == 0):
			lpc_src = begin + "\n\n" + end
		file.close()
	except IOError:
		lpc_src = begin + "\n\n" + end
	
	new_src = u'''
#include <user_key.h>
#include <school.h>
static mapping mpReward = %s;
'''%(PythonData2Lpc(allReward, True, 1))

	res = lpc_src.decode("GBK")

	tmp = replace_pattern.sub(begin + "\n" + new_src + "\n" + end, res)
	
	write_file( outputfile, tmp )

	sys.path.append(rootPath + "tools/autocode")
	CLIENT_SAVE = __import__("Util")
	CLIENT_SAVE.WriteClientFile(rootPath, "reward_desc", "const_reward_desc", dictClientDesc)
			
def parse_xls(filename, outputfile):
	try :
		book = xlrd.open_workbook(filename)
	except :
		msg = "can't open file?", filename
		usage()
		sys.exit(-1)

	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		print sh.name.encode('gbk')
		# 不处理说明表格
		if sh.name == dicKeys.get("comment_sheet"):
			continue
		# 不处理对应表
                if sh.name == dicKeys.get("map_sheet"):
			continue
                if sh.name == dicKeys.get("fix_reward"):
                	parse_data_sheet(sh, outputfile)
		
def main():
	global rootPath
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
		for o, a in opts:
	       		if o == "-v":
				#print version	
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
		outputfile = rootPath + args[2]	
	

	except getopt.GetoptError, err:
		# print help information and exit:
		# print str(err) # will print something like "option -a not recognized"
		usage()
		raise
		#sys.exit(2)

	#print execelFile,outputfile

	parse_xls( execelFile, outputfile)

if __name__ == "__main__":
	main()
