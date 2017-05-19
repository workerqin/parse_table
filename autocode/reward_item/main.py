# -*- coding: utf-8 -*-
""" 物品奖励表
"""

import xlrd
import sys
import getopt
import re
import string
from datetime import datetime

sys.path.append("../")
sys.path.append("tools/autocode")

from Util import PythonData2Lpc 
from Util import PythonData2Lua 

version = "1.00"


def usage():
	print "USAGE:main.py root_path excel_file 输出路径 "
	print '''
	--version : Prints the version number
	-h --help    : Display this help'''

dicKeys = {
	# 说明表格名字
	"comment_sheet"      : "说明",
	# 奖励物品名及其对应表
	"map_sheet"      : "奖励物品名及其对应表",
	# 奖励表类型
	"reward_type"        : "奖励表类型",
	# 发奖件数
	"reward_cnt"         : "发奖件数",
	# 发奖等级区间
	"reward_lv"          : "发奖等级区间",
	# 体力要求
	"tili_need"			 : "体力要求",
	# 奖励原因
	"reward_reason"      : "奖励原因",
	# 任务天数
	"reward_days"        : "任务天数",
	# 默认发奖项
	"reward_default"     : "默认发奖项",
	# 奖品名称
	"single_reward_name"       : "奖品名称",
	# 一次获得奖励投放数量
	"single_reward_cnt"        : "一次获得奖励投放数量",
	# 是否体力影响 
	"tili_effect"	           : "是否体力影响",
	# 属性
	"single_reward_att"        : "属性",
	# 物品栏
	"frame"					   : "物品栏",
	#公告内容
	"single_reward_gonggao"    : "公告内容",
	#离线信件
	"single_reward_mail"       : "公告内容",
	#元气任务影响
	"yuan_qi_task_effect"		: "元气任务影响",
	#自动任务影响
	"auto_mission_effect"		: "自动任务影响",
	"other_attr"		: "其他属性",
}

def write_file(filename, content ):
	msg = "writting to file",filename

	try :
		f = file(filename, "w+b")
	except :
		msg = "can not write to", filename
		sys.exit(-1)
	
	f.write(content)
	f.close()


def get_str_from_sheet( sheet, row, col ):
	value = sheet.cell_value(rowx=row, colx=col)
	
	if  isinstance(value, float):
		return str(int(value))
	
	if  isinstance(value, int):
		return str(value)

	value = value.encode("utf-8")
	return value	

def get_map_from_sheet( sheet, row, col ):
	value = get_str_from_sheet( sheet, row, col )

	value = value.strip()

	tmp = {}
	
	if  len(value) == 0:
		return tmp
	
	value = value.encode("utf-8")
	kvs = value.split(',')
	
	for kv in kvs:
		if not len(kv.strip()):
			continue
		kvpairs = kv.split(':')
		k = kvpairs[0]
		v = kvpairs[1]
		
		if v.startswith('"'):
			tmp[k] = v.replace('"', '')
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

src_templete = '''
// Purpose  : 自动生成的奖励表文件
// By       : Prophet@封神东游

#include <reward.h>

inherit REWARD_BASE;

#include <var_prop.h>

// -----------------------------------------------------------
// 基本数据区
// -----------------------------------------------------------

%s

mapping* rewards = %s;

mapping* __GetRewards()
{
        return rewards;
}

// -----------------------------------------------------------

'''

param_templete = '''
// %s
RESET_ONUPDATE_VAR(%s, %s)
'''

	
#用Book生成代码	
def parse_data_sheet(sh, outputPath, rootPath):
	outputfile = rootPath + outputPath + sh.name + '.c'
	#相对路径
	reloutputfile = outputPath + sh.name + '.c' 
	
	rewardType = ""
	rewardCntDown = 0
	rewardCntUp = 0
	rewardReason = ""
	rewardBegin = 0
	rewardDays = 0
	rewardLvDown = 0
	rewardLvUp = 0
	rewardTiliNeed = ""
	rewardYQTEffect = ""
	rewardAutomissionEffect = 0
	
	rewards = []
	
	for i in range(0, sh.nrows):
		data = get_str_from_sheet(sh, i, 0)
		
		if data == dicKeys.get('reward_type'):
			rewardType = get_str_from_sheet(sh, i, 1)
			continue
		if data == dicKeys.get('reward_cnt'):
			rewardCntDown = get_int_from_sheet(sh, i, 1)
			rewardCntUp = get_int_from_sheet(sh, i, 2)
			continue
		if data == dicKeys.get('reward_reason'):
			rewardReason = get_str_from_sheet(sh, i, 1)
			continue
		if data == dicKeys.get('reward_days'):
			rewardDays = get_str_from_sheet(sh, i, 1)
			continue
		if data == dicKeys.get('single_reward_name'):
			rewardBegin = i
			break
		if data == dicKeys.get('reward_lv'):
			rewardLvDown = get_int_from_sheet(sh, i, 1)
			rewardLvUp = get_int_from_sheet(sh, i, 2)
			continue
		if data == dicKeys.get('tili_need'):
			rewardTiliNeed = get_str_from_sheet(sh, i, 1)
			continue
		if data == dicKeys.get('yuan_qi_task_effect'):
			rewardYQTEffect = get_str_from_sheet(sh, i, 1)
			continue
		if data == dicKeys.get('auto_mission_effect'):
			rewardAutomissionEffect = get_int_from_sheet(sh, i, 1)
			continue
	
	for i in range(rewardBegin+3, sh.nrows):
		
		name = get_str_from_sheet(sh, i, 0)
		
		if len(name) == 0:
			continue;
		
		reward = {}
		rewards.append(reward)
		
		for j in range(0, sh.ncols):
			title = get_str_from_sheet(sh, rewardBegin+1, j)
			
			#print title
			if len(title) == 0:
				continue
			
			titleType = get_str_from_sheet(sh, rewardBegin+2, j)
			
			if titleType == 'int':
				reward[title] = get_int_from_sheet(sh, i, j)
				continue
			if titleType == 'string':
				reward[title] = get_str_from_sheet(sh, i, j)
				continue	
			if titleType == 'macros':
				reward[title] = get_str_from_sheet(sh, i, j)
				continue
			if titleType == 'mapping':
				reward[title] = get_map_from_sheet(sh, i, j)
				continue
			
	params = ''
	
	
	params += param_templete%("奖励表类型", "RewardType", '"%s"'%rewardType)
	
	if rewardCntDown != 0:
		params += param_templete%("奖励数量下限", "RewardCntDown", rewardCntDown)
	
	if rewardCntUp != 0:
		params += param_templete%("奖励数量上限", "RewardCntUp", rewardCntUp)

	if rewardLvDown != 0:
		params += param_templete%("奖励等级下限", "RewardLvDown", rewardLvDown)
	if rewardLvUp != 0:
		params += param_templete%("奖励等级上限", "RewardLvUp", rewardLvUp)

	if rewardTiliNeed != "":
		params += param_templete%("体力要求", "TiliNeed", "\"%s\""%rewardTiliNeed)	
	if rewardYQTEffect!= "":
		params += param_templete%("元气任务影响", "YuanQiTaskEffect", "\"%s\""%rewardYQTEffect)	
	if rewardAutomissionEffect!= 0:
		params += param_templete%("自动任务影响", "AutoMissionEffect", rewardAutomissionEffect)
	
	params += param_templete%("奖励原因", "RewardReason", '"%s"'%rewardReason)
	
	# 尝试读取outputfile
	try:
		file = open(outputfile, "rb")
		lpc_src = file.read()
		if ( len( lpc_src ) == 0):
			lpc_src = begin + "\n\n" + end
		file.close()
	except IOError:
		lpc_src = begin + "\n\n" + end
	
	new_src = src_templete%(params, PythonData2Lpc(rewards, True, 1))
	tmp = replace_pattern.sub(begin + "\n" + new_src + "\n" + end, lpc_src)
	
	write_file( outputfile, tmp )

	sys.path.append(rootPath + "tools/autocode/")
	UTIL = __import__("Util")
	UTIL.WriteUpdateFile(rootPath, reloutputfile + "\n")
			
def parse_xls(filename, outputPath, rootPath):
	try :
		book = xlrd.open_workbook(filename)
	except :
		msg = "can't open file?", filename
		usage()
		sys.exit(-1)
	
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		sheetname = sh.name.encode("utf-8")
		# 不处理说明表格
		if sheetname == dicKeys.get("comment_sheet"):
			continue
		# 不处理对应表
		if sheetname == dicKeys.get("map_sheet"):
			continue
		parse_data_sheet(sh, outputPath, rootPath)
		
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
		outputPath = args[2]	
	

	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		raise
		#sys.exit(2)

	print execelFile,outputPath

	parse_xls( execelFile, outputPath, rootPath)

if __name__ == "__main__":
	main()
