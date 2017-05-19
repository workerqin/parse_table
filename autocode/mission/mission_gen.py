#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import xlrd
import sys
import os
import glob
import getopt
import re
import locale
import mission_type as MissionType
from datetime import date
from datetime import datetime
from gen_trigger import parse_line as parse_trigger_line 
from gen_trigger import get_error as get_trigger_error
from gen_trigger import parse_sheet as parse_trigger_sheet
from gen_trigger import clear_detail as clear_trigger_detail
from gen_trigger import get_detail as get_trigger_detail

sys.path.append("../")
sys.path.append("tools/autocode")

from Util import PythonData2Lpc 
from Util import PythonData2Lua 

svn_user_auth = " --username q1_autoparse_design --password Q1AutoParse"

global mission_error
global cur_bookname 

global global_mission
global global_mission_detail

cur_bookname = ""

TEMPLATE_SRC = '''
// 任务名
// %(MissionName)s 

#include <mission.h>
inherit %(MissionMode)s;
#include <var_prop.h>
#include <npc_key.h>
#include <user_key.h>
#include <event_type.h>

RESET_ONUPDATE_VAR(AutoCreate, 1)

//RESET_ONUPDATE_VAR(StoryID, "%(StoryID)s")

// =========基本属性==========
%(MissionProp)s

// =========任务奖励==========
%(RewardProp)s

// =========任务描述==========
%(DescribeProp)s

// =========任务数据==========
%(DataProp)s

// =========任务菜单==========
%(MenuProp)s

// =========触发器==========
%(TriggerProp)s
'''

# 注释掉的属性暂时没使用，如果有需求自行修改/添加	

# 基本属性区
dicMissionProp = {
		'任务名' : ('string', 'Name'),
		'任务ID' : ('string', 'Id'),
		'任务类型' : ('string', 'Type'),
		'前置任务' : ('string', 'NeedMission'),
		'玩家等级' : ('int', 'NeedGrade'),
		'可接任务' : ('string_array', 'AcceptMissionList'),
		'下一步任务' : ('string', 'NextMission'),
		}

# 奖励
rewardProp = {
		'物品奖励' : ('string', 'ItemReward'),
		'经验奖励' : ('int', 'ExpReward'),
		'灵兽经验奖励' : ('int', 'SummonExpReward'),
		'金钱奖励' : ('int', 'CashReward'),
		}

# 任务描述
describeProp = {
		'可接任务名' : ('string', 'AcceptName'),
		'可接任务目的' : ('string', 'AcceptPurpose'),
		'可接任务描述' : ('string', 'AcceptDescribe'),
		'当前任务名' : ('string', 'DoingName'),
		'当前任务目的' : ('string', 'DoingPurpose'),
		'当前任务描述' : ('string', 'DoingDescribe'),
		'任务追踪' : ('repKey', 'TackDescribe'),
		}

# 任务数据区
dataProp = {
		'目标NPC': ('int_array', 'TargetNpc'),
		'目标NPC样式': ('string_array', 'TargetNpcStyle'),
		'发放NPC': ('int', 'GrantNpc'),
		'剧情ID': ('string', 'StoryID')
		'对话内容': ('table', 'TalkPages')
		}

# 任务相关
menuProp = {
		'发放菜单头' : ('string', 'AcceptChatMsg'),
		'发放选项' : ('string', 'AcceptOption'),

		'目标菜单头' : ('string', 'TargetChatMsg'),
		'目标选项' : ('string', 'TargetOption'),
}

# 触发器相关
triggerProp = {
		'接受触发器' : ['AcceptTrigger'],
		'完成触发器' : ['CompleteTrigger'],
}

def encode(val):
	import locale
	encoding = locale.getdefaultlocale()[1]
	res = val.encode(encoding)
	return res

def cell_value(sh, row, col):
	val = sh.cell_value(rowx=row, colx=col)
	try :
		val = encode(val)
		return val
	except :
		return val

def usage():
    print "USAGE:gen_mission.py excel_file outputpath"
    print "--version : Prints the version number"
    print "--help    : Display this help"

def get_error():
	global mission_error
	global cur_bookname
	error = get_trigger_error()
	print error, "in get mission error"
	return cur_bookname + " " + mission_error + " " + error
          
def write_file(filename, content ):

	msg = "writting to file",filename
	print msg
	try :
		f = file(filename, "w+b")
	except :
		msg = "can not write to", filename
		#print msg
		sys.exit(-1)

	f.write(content)
	f.close()

def add_to_file(filename, content):
	try :
		f = file(filename, "a+b")
	except :
		sys.exit(-1)
	f.write(content)
	f.close()

def filter_space( str ):
	tmp = str.replace(" ", "" )
	tmp = tmp.replace('，', ',')
	tmp = tmp.replace('：', ':')
	return tmp

#将一个字串 比如"2:20,3:12,4"转换成"2:20,3:12,4:1", 或者"3,"转换成"3:1,"
def str2pymap(Value):
	if Value == "":
		return ""
	ActionData = filter_space(Value).split(",");
	if len(ActionData) == 0:
		return ""
	cAction = ""
	for cData in ActionData:
		if cData == "":
			continue
		if len(cData.split(":")) == 2:
			cAction += "%s,"%(cData)
		elif len(cData.split(":")) == 1:
			cAction += "%s:1,"%(int(float(cData)))
	return cAction

#将一个python 字符串串array 按字串长度转换成 lpc src
def PyArraySort2LpcSrc(arrstr):
	mpSort = {}
	index = 0
	for cstr in arrstr:
		#print cstr, index, mpSort
		if len(mpSort) == 0:
			mpSort[index] = cstr
			continue
		itemp = index
		if len(mpSort[itemp]) < len(cstr):
			icurtemp = itemp
			while len(mpSort[itemp]) < len(cstr):
				mpSort[itemp + 1] = mpSort[itemp] 
				icurtemp = itemp
				if itemp == 0:
					break
				itemp = itemp - 1
			itemp = icurtemp
		else:
			itemp = index + 1
		index += 1
		mpSort[itemp] = cstr
	return mpSort

DECLARE_VAR = '''// %s
RESET_ONUPDATE_VAR(%s, %s)
'''
DECLARE_VAR_NO_DESC = '''RESET_ONUPDATE_VAR(%s, %s)
'''
DECLARE_DESC_VAR = '''RESET_ONUPDATE_VAR(%s, [%s, %s])
'''
def parse_triger( sh, i ):
	row = i
	ret = {}
	beginFlg = False
	content = ""
	while row < sh.nrows:
		tmp = cell_value(sh, row, 0)
		if tmp== "BEGIN":
			beginFlg = True
			row += 1
			continue
		if tmp == "END":
			row += 1
			break
		if beginFlg == True:
			content += (parse_trigger_line(sh, row) + '\n')
			row += 1
			continue
		row += 1
	return { "row":row, "content":content }

def parse_string(sh, row, col):
	tmp = cell_value(sh, row, col)
	try :
		ret = '%d'%(int(float(tmp)))
	except :
		ret = tmp
	return ret.strip()

def parse_int(sh, row, col):
	ret = 0
	try :
		tmp = cell_value(sh, row, col)
		ret = int(float(tmp))
	except :
		ret = 0
	return ret

def parse_sex(sh, row, col):
	try :
		ret = cell_value(sh, row, col)
		if ret == '男':
			return 1
		elif ret == '女':
			return 2
		return 0
	except :
		return 0

def parse_race(sh, row, col):
	try :
		ret = cell_value(sh, row, col)
		if ret == '人':
			return 1
		elif ret == '魔':
			return 2
		return 0
	except :
		return 0

def parse_string_array(sh, row, col):
	str = parse_string(sh, row, col).replace("，", ",")
	arrs = str.split(",")
	str_arr = []
	for tmp in arrs:
		if len(tmp) <= 0:
			continue
		str_arr.append(tmp)
	return str_arr

def parse_int_array(sh, row, col):
	str = parse_string(sh, row, col).replace("，", ",")
	arrs = str.split(",")
	int_arr = []
	for tmp in arrs:
		try : 
			tmp1 = int(tmp)
			int_arr.append(tmp1)
		except :
			continue
	return int_arr

def parse_string_key(strkey):
	size = len(strkey)
	if strkey[0] == '"' and strkey[size] == '"':
		return strkey[0:len-1]
	try: 
		ret = int(float(strkey))
		return ret
	except:
		return strkey

def parse_map(sh, row, col):
	tmpStr = cell_value(sh, row, col)
	tmpMap = {}
	if is_null(tmpStr):
		return tmpMap
	try:
		tmpStr = tmpStr.replace("，", ",")
		tmpStr = tmpStr.replace("：", ":")
		tmpMap = eval("{" + tmpStr + "}")
	except ValueError:
		tmpMap = {}
	return tmpMap

def parse_array(sh, row, col):
	tmpStr = cell_value(sh, row, col)
	tmpArr = []
	if is_null(tmpStr):
		return tmpArr
	try:
		if isinstance(tmpStr, str):
			tmpStr = tmpStr.replace("，", ",")
			#print tmpStr
			tmpArr = eval("[" + tmpStr + "]")
		else:
			value = int(tmpStr)
			tmpArr.append(value)
	except ValueError:
		tmpArr = []
	return tmpArr

def parse_x_array(xtype, sh, row, col):
	tmp = []
	for tmpcol in range(col, sh.ncols):
		value = do_parse(xtype, sh, row, tmpcol)
		if is_null(value):
			continue
		tmp.append(value)
	return tmp

# 解析一个表格出来
#------------------------
#例:
# isHero(int)  resid(int)   dress_no(int)   action(string)  name(string)  title(string)       msg(string)
# 0      10007   1           stand  小猪 无敌飞天女王 说点啥 
# 0      10007   1           stand  小猪 无敌飞天女王 说点啥 
# 0      10007   1           stand  小猪 无敌飞天女王 说点啥 
# 0      10007   1           stand  小猪 无敌飞天女王 说点啥 
# 0      10007   1           stand  小猪 无敌飞天女王 说点啥 
#返回一个数组:
#
def parse_table(sh, row, col):
	tmp = []
	currow = currow + 1
	# 读取第一行确定表头
	head = [] 
	
		
	# 读取后面几行
	#while 

	return tmp

def parse_bool(sh, row, col):
	try :
		ret = cell_value(sh, row, col)
		if ret == '是':
			return 1
		elif ret == '否':
			return 0
	except :
		return ''
	return ''

def parse_date(sh, row, col):
	parse_str = parse_string(sh, row, col)
	date_type = 0
	try :
		if parse_str == "":
			return 0
		if parse_str.find("每天") >= 0:
			date_type = "T_DATE_DAY"
			return '''{ "type":%s, }'''%(date_type)
		elif parse_str.find("每月") >= 0:
			Re = re.compile("每月([\d]*)")
			m = Re.search(parse_str)
			index = int(m.group(1))
			if index <= 0 or index > 31:
				return 0
			date_type = "T_DATE_MONTH"
			return '''{ "type":%s, "date":%d, }'''%(date_type, index)
		elif parse_str.find("每周") >= 0:
			Re = re.compile("每周([\d]*)")
			m = Re.search(parse_str)
			index = int(m.group(1))
			if index <= 0 or index > 7:
				return 0
			date_type = "T_DATE_WEEK"
			return '''{ "type":%s, "date":%d, }'''%(date_type, index)
		else:
			date_type = "T_DATE_TIME"
			#TODO: 检查是否合法
			return '''{ "type":%s, "date":"%s", }'''%(date_type, parse_str)
	except :
		return 0
	return 0

def parse_date_time(sh, row, col):
	parse_str = parse_string(sh, row, col)
	time_type = ""
	if 1:
		if parse_str.find("接受") >= 0:
			time_type = "K_PERIOD_ACCEPT_CNT"
			Re = re.compile("接受([\d]*)次")
			m = Re.search(parse_str)
			index = int(m.group(1))
			return '''[ %s, %d ]'''%(time_type, index)
		elif parse_str.find("完成") >= 0:
			time_type = "K_PERIOD_FINISH_CNT"
			Re = re.compile("完成([\d]*)次")
			m = Re.search(parse_str)
			index = int(m.group(1))
			return '''[ %s, %d ]'''%(time_type, index)
		else:
			return 0
	else:
		return 0
	return 0

def replace_task_desc(val):
	Re = re.compile("\$([\w][:\w]*)")
	arrtmp = Re.findall(val)

	Re2 = re.compile("\&([\w][:\w]*)\(([^\)]*)\)")
	arrtmp2 = Re2.findall(val)

	valstr = val
	mpSort = PyArraySort2LpcSrc(arrtmp)
	arrstr = []
	ikey = 0
	i = 0
	while i < len(mpSort):
		repstr = "$%s"%(mpSort[i])
		valstr = valstr.replace(repstr, "$%d"%(ikey))
		arrstr.append(mpSort[i])
		i += 1
		ikey += 1

	i = 0
	while i < len(arrtmp2):
		funcarr = arrtmp2[i]
		funcstr = "&%s(%s)"%(funcarr[0], funcarr[1])
		valstr = valstr.replace(funcstr, "$%d"%(ikey))

		newfuncarr = []
		newfuncarr.append(funcarr[0])
		for _item in funcarr[1].split(","):
			newfuncarr.append(_item)

		arrstr.append(newfuncarr)
		ikey += 1
		i += 1

	if len(valstr):
		return [valstr, arrstr]
	else:
		return []
	

def do_parse(type, sh, row, col):
	if is_null(type):
		return 0
	if type == "string":
		return parse_string(sh, row, col)
	elif type == "macros":
		return "@@%s"%parse_string(sh, row, col)
	elif type == "int":
		return parse_int(sh, row, col)
	elif type == "map":
		return parse_map(sh, row, col)
	elif type == "array":
		return parse_array(sh, row, col)
	elif type == "bool":
		return parse_bool(sh, row, col)
	elif type == "sex":
		return parse_sex(sh, row, col)
	elif type == "date":
		return parse_date(sh, row, col)
	elif type == "date_time":
		return parse_date_time(sh, row, col)
	elif type == "int_array":
		return parse_int_array(sh, row, col)
	elif type == "string_array":
		return parse_string_array(sh, row, col)
	elif type == "repKey":
		value = parse_string(sh, row, col)
		return replace_task_desc(value)
	elif type == "table":
		return  parse_table( sh, row, col )	
	elif type[len(type)-1] == '*':
		return parse_x_array(type[0:(len(type)-1)], sh, row, col)
	return 0

def is_null(val):
	if val == None or val == 0 or val == '' or val == [] or val == {}:
		return 1
	return 0

def getMissionType(type_name):
	if type_name in MissionType.data.keys():
		return MissionType.data[type_name]
	else:
		print 'error unknow mission type:' + type_name
		return 'MISSION_BASE'


def parse_mission_sheet( sh, bookname ):

	global mission_error
	global global_menu_index
	global global_menu_key
	global global_mission

	mission_error = ""
	
	missionId = bookname + encode(sh.name)
	mission_name = ''
	mission_mode = ''

	mission_prop = ''
	mission_reward = ''
	mission_describe = ''
	mission_menu = ''
	mission_data = ''
	mission_trigger = ''

	i = 0
	currow = i
	cur_str = ""

	print missionId
	print PythonData2Lpc(missionId)
	mission_prop += DECLARE_VAR%("任务ID", dicMissionProp["任务ID"][1], PythonData2Lpc(missionId))

	mission_info = {}
	mission_info["基本属性"] = {}
	mission_info["奖励"] = {}
	mission_info["描述"] = {}

	#print global_menu_key
	try:
		while 1:
			i = currow
			if i >= sh.nrows:
				break
			cur_str = parse_string(sh, i, 0)
			tmp = cur_str
			#默认为增加一行
			currow = currow + 1
	
			if tmp == '任务模式':
				mission_mode = getMissionType(parse_string(sh, i, 1))
				continue
	
			# 基本属性
			if tmp in dicMissionProp.keys():
				val = do_parse(dicMissionProp[tmp][0], sh, i, 1)
				if tmp == "任务名":
					mission_name = val
				# 不是bool,则空返回
				if not (dicMissionProp[tmp][0] == "bool" and isinstance(val, int)):
					if is_null(val):
						continue
				if tmp in ["任务名","任务ID","任务类型", "前置任务","玩家等级"]:
					mission_info["基本属性"][tmp] = val
				'''
				if tmp == "任务周期":
					mission_prop += DECLARE_VAR%(tmp, dicMissionProp[tmp][1], val)
					continue
				'''
				mission_prop += DECLARE_VAR%(tmp, dicMissionProp[tmp][1], PythonData2Lpc(val))
				continue
	
			# 奖励
			if tmp in rewardProp.keys():
				val = do_parse(rewardProp[tmp][0], sh, i, 1)
				mission_reward += DECLARE_VAR%(tmp, rewardProp[tmp][1], PythonData2Lpc(val))

				if tmp in ["物品奖励","经验奖励","灵兽经验奖励", "金钱奖励"]:
					mission_info["奖励"][tmp] = val

				continue

			# 任务描述
			if tmp in describeProp.keys():
				val = do_parse(describeProp[tmp][0], sh, i, 1)
				mission_describe += DECLARE_VAR%(tmp, describeProp[tmp][1], PythonData2Lpc(val))

				if tmp in ["可接任务名", '可接任务目的','可接任务描述','当前任务名','当前任务目的','当前任务描述']:
					mission_info["描述"][tmp] = val

				continue

			# 菜单
			if tmp in menuProp.keys():
				val = do_parse(menuProp[tmp][0], sh, i, 1)
				mission_menu += DECLARE_VAR%(tmp, menuProp[tmp][1], PythonData2Lpc(val))
				continue

			# 数据
			if tmp in dataProp.keys():
				val = do_parse(dataProp[tmp][0], sh, i, 1)
				mission_data += DECLARE_VAR%(tmp, dataProp[tmp][1], PythonData2Lpc(val))
				continue

			# 触发器
			if tmp in triggerProp.keys():
				ret = parse_triger(sh, i)
				if ret["content"] != "":
					mission_trigger += DECLARE_VAR%(tmp, triggerProp[tmp][0], '''[\n%s]\n'''%(ret["content"]))
				currow = ret["row"]
				continue

	except:
		mission_error = "error row:%d, %s"%(currow, cur_str)
		raise

	global_mission[missionId] = mission_info

	params = {
			"StoryID": bookname,
			"MissionName": mission_name,
			"MissionMode": mission_mode,
			"MissionProp": mission_prop,
			"RewardProp": mission_reward,
			"DescribeProp": mission_describe,
			"MenuProp": mission_menu,
			"TriggerProp":mission_trigger,
			"DataProp": mission_data,
			}

	src = TEMPLATE_SRC % params
	return src

src_template_triger = '''
#include <trigger.h>

inherit TRIGGER_BASE;

#include <var_prop.h>
#include <npc_key.h>
#include <user_key.h>
#include <macros.h>

RESET_ONUPDATE_VAR(StoryID, "%(StoryID)s")

MEMORY_VAR(HookMethod, {}) 

%(TriggerID)s

%(src_main)s

void create()
{
	SetInstanceLimit(100);
	SetTriggerType(TYPE_MISSION);
}
'''

def parse_triger_xls( sh, bookname ):
	global global_mission_detail

	#清除触发器的详细信息
	clear_trigger_detail()

	#从0行开始解析
	ret = parse_trigger_sheet( sh )
	params = {
		"TriggerID": DECLARE_VAR%("触发器ID", "TriggerID", '"' + bookname + encode(sh.name) + '"'),
		"src_main": ret["content"],
		"StoryID": bookname,
		}

	missionId = bookname + encode(sh.name)
	global_mission_detail[missionId] = get_trigger_detail()

	return src_template_triger % params

def parse_sheet(sh, bookname, workdir, filename):
	global mission_error
	global cur_bookname
	sheetname = encode(sh.name)
	if sheetname[0] != 'M' and sheetname[0] != 'T' and sheetname != 'config':
		return ""
	print bookname, sheetname, sheetname[0]

	cur_bookname = encode(bookname + sheetname)

	mission_error = ""
	if sheetname[0] == 'M':
		return parse_mission_sheet(sh, bookname)
	if sheetname[0] == 'T':
		return parse_triger_xls(sh, bookname)
	return ""

def get_xls_missions(filename):
	xls_missions = []
	try :
		book = xlrd.open_workbook(filename) 
	except :
		msg = "can't open file?", filename
		return xls_missions

	bookname = os.path.basename(filename).split(".")[0]

	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		if sh.name == u"说明" or sh.name == u"模板说明" or sh.name == u"触发器指令说明":
			continue
		sheetname = encode(sh.name)
		if sheetname[0] != 'M':
			continue
		mission_name = bookname + sh.name
		xls_missions.append(mission_name)
	return xls_missions

src_client_menu = '''

module("m_task", package.seeall)

if not const_task_table then const_task_table = {} end

table.merge(const_task_table,
%(src_mission)s
)

'''

def parse_xls(filename, outputpath, client_output):
	global global_menu_index
	global global_mission
	global global_mission_detail

	begin = r"// -------------------  Auto Generate Begin --------------------"
	end   = r"// -------------------  Auto Generate End   --------------------" + "\n"
	p = re.compile(begin + r".*?" + end, re.S | re.M)
	try :
		book = xlrd.open_workbook(filename) 
	except :
		msg = "can't open file?", filename
		#print( msg )
		usage()
		sys.exit(-1)

	#print outputpath
	update_file = outputpath + "tmp/update_file.txt"
	outputpathdir = outputpath + "data/missions/"
	log_file = outputpath + "log/parse_log.dat"
	str_update_files = ""
        
	bookname = os.path.basename(filename).split(".")[0]

	global_mission = {}
	global_mission_detail = {}


	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		if sh.name == u"说明" or sh.name == u"模板说明" or sh.name == u"触发器指令说明":
			continue

		strLpc = parse_sheet(sh, bookname, outputpath, filename)
		if strLpc == "":
			continue
		src_file = outputpathdir + bookname + encode(sh.name) + ".c"
		try:
			src_data = open(src_file, "rb").read()
		except IOError:
			src_data = begin + "\n\n" + end + "\n"
		strLpc = p.sub(begin + "\n" + strLpc + "\n" + end, src_data)
		write_file( src_file, strLpc )
		str_update_files += bookname + encode(sh.name) + ".c" + "\n"
	
	add_to_file(update_file, str_update_files)

	svn_add_files = [] 

	#客户端表
	if len(client_output) and os.path.isdir(client_output):
		client_file = client_output+ bookname + ".lua"
		params = {
			"src_mission": PythonData2Lua(global_mission, True), 
			}
		menu_content = src_client_menu % (params)

		#if not os.path.isfile(client_file):   
		svn_add_files.append(client_file)
		write_file(client_file, menu_content)
		
		os.chdir(client_output)
		if len(svn_add_files):
			for file in svn_add_files:
				try : 
					#continue
					os.system("svn add " + file)
				except :
					continue
		filelist = os.listdir(client_output) 
		init_content = ""
		for file in filelist:
			if file[-4:] != ".lua":
				continue
			if file[:-4] == "init":
				continue
			init_content += '''fs_require("script/data", "info/mission/%s")\n'''%(file)
		client_init_file = client_output + "init.lua"
		write_file(client_init_file, init_content)
		os.system("svn ci " + svn_user_auth + " -m " + "\"" "更新成功 from "+ client_output + "\"")

if __name__ == "__main__":
	sys.path.append("../")
	if len(sys.argv) < 3:
		usage()
	elif sys.argv[1].startswith('--'):
		sys.exit()
	else:
		filename = sys.argv[1]
		outputpath = sys.argv[2]
		clientoutput = ""
		if len(sys.argv) >= 4:
			clientoutput = sys.argv[3]
		#预处理部分代码
		parse_xls(filename, outputpath, clientoutput) 
