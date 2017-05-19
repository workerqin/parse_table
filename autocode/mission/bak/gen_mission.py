#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import xlrd
import sys
import os
import glob
import getopt
import re
import locale
from datetime import date
from datetime import datetime

from gen_trigger import parse_line as parse_trigger_line 
from gen_trigger import parse_line_cmd as parse_trigger_line_cmd
from gen_trigger import parse_sheet as parse_trigger_sheet
from gen_trigger import get_error as get_trigger_error
from gen_trigger import clear_detail as clear_trigger_detail
from gen_trigger import get_detail as get_trigger_detail

sys.path.append("../")
sys.path.append("tools/autocode")

from Util import PythonData2Lpc 
from Util import PythonData2Lua 

svn_user_auth = " --username fs_autoparse_design --password \!QA2ws3ed"
#svn_user_path = ""

global mission_error
global cur_bookname 

global global_mission
global global_mission_detail


cur_bookname = ""

TEMPLATE_SRC = '''
// 任务名
// %(MissionName)s 

#include "/module/mission/mission_macros.h"
inherit %(MissionType)s;
#include <equip.h>
#include <var_prop.h>
#include <npc_key.h>
#include <user_key.h>
#include <macros.h>
#include <trigger.h>
#include <event_type.h>
#include <task.h>
#include <weather.h>

RESET_ONUPDATE_VAR(AutoCreate, 1)

RESET_ONUPDATE_VAR(StoryID, "%(StoryID)s")

// =========任务属性==========
%(MissionProp)s

// =========任务流程==========
%(MissionFlow)s

// =======任务跟踪描述========
%(DynamicDesc)s

// =========任务条件==========
%(MissionCondition)s

// =========任务限制==========
%(MissionLimit)s

// =========任务物品==========
%(MissionItem)s

// =========任务参数==========
%(MissionArgs)s

// ========任务触发器=========
%(MissionTrigger)s

// ========扩展触发器=========
%(MissionExtTrigger)s

// ========任务变量===========
%(MissionVariable)s

// =====任务目标NPC闲话=======
%(MissionActionChat)s

// ======任务功能代码=========
%(MissionFuncSrc)s
'''

dicMissionProp = {
		'任务名' : ('string', 'MissionName'),
		'任务ID' : ('string', 'MissionID'),
		'任务类别' : ('string', 'MissionType'),
		'任务时间(分钟)' : ('int', 'TimeLimit'),
		'任务难度等级' : ('int', 'MissionGrade'),
		'任务物品奖励' : ('repKey', 'ItemReward'),
		'任务经验奖励' : ('int', 'ExpReward'),
		'任务灵兽经验奖励' : ('int', 'SummonExpReward'),
		'任务金钱奖励' : ('int', 'CashReward'),
		'任务奖励描述' : ('string', 'RewardDesc'),
		'任务周期' : ('date', 'MissionPeriod'),
		'任务轮次' : ('int', 'MissionRound'),
		'任务是否共享' : ('bool', 'ShareMission'),
		'是否可以取消' : ('bool', 'CanCancel'),
		'任务背景' : ('string', 'BackGround'),
		'周期数据任务ID' : ('string', 'PeriodDataID'),
		'二次确认提醒' : ('string', 'ConfirmMessage'),
		'是否允许传送到任务NPC' : ('int', 'CanTransToNpc'),
		'是否自动追踪任务NPC' : ('bool', 'AutoTraceNpc'),
		'客户端任务指引' : ('string', 'ClientDescGuide'),
		'任务可接受描述' : ('repKey', 'AcceptableDesc'),
		}

dicMissionFlow = {
		'是否发放给队员' : ('bool', 'TeamerCanAccept'),
		'任务发放NPC' : ('array', 'AcceptNpcList'),
		'任务目标NPC' : ('array', 'ActionNpcList'),
		'任务完成NPC' : ('array', 'CompleteNpcList'),
		}

dicMissionMenu = {
		'任务发放菜单项' : ('string', 'AcceptMenu'),
		'任务发放菜单头' : ('string', 'AcceptMenuTitle'),
		'目标NPC菜单项' : ('string', 'ActionMenu'),
		'目标NPC菜单头' : ('string', 'ActionMenuTitle'),
		'任务完成菜单项' : ('string', 'CompleteMenu'),
		'任务完成菜单头' : ('string', 'CompleteMenuTitle'),
}

#状态定义
#S_ASSIGN = 1
#S_ACTION = 2
#S_COMPLETE = 3

#静态描述
dicMissionDesc = {
		'任务分派描述' : "@@S_NO_MISSION",
		'任务过程描述' : "@@S_ACTION",
		'任务完成描述' : "@@S_FINISH",
		}

dicLyricDesc = {
		'任务分派歌词' : ('string', 'int', 1),
		'任务过程歌词' : ('string', 'int', 2),
		'任务完成歌词' : ('string', 'int', 3),
		}

dicMissionCond = {
		'任务要求等级下限' : ('int', 'Cond_GradeLow'),
		'任务要求等级上限' : ('int', 'Cond_GradeHigh'),
		'任务称谓要求' : ('string', 'Cond_Title'),
		'任务性别要求' : ('sex', 'Cond_Sex'),
		'任务门派要求' : ('array', 'Cond_Race'),
		'任务境界要求' : ('array', 'Cond_Realm'),
		'互斥任务' : ('array', 'Cond_Mutex'),
		'任务周期完成次数' : ('int', 'PeriodFinishLimit'),
		'任务周期接受次数' : ('int', 'PeriodAcceptLimit'),
		'任务取消时间限制' : ('int', 'CancelTimeLimit'),
		}
dicMissionTeamCond = {
		'队伍人数上限' : ('int', 'Cond_TmHSize'),
		'队伍人数下限' : ('int', 'Cond_TmLSize'),
		}

dicMissionLimit = {
		'飞行旗限制' : ('bool', 'FlyLimit'),
		'暗雷触发限制' : ('bool', 'AnleiLimit'),
		'PK限制' : ('bool', 'PKLimit'),
		'组队限制' : ('bool', 'TeamLimit'),
		'称谓更换限制' : ('bool', 'ChgTitleLimit'),
		'临时离开限制' : ('bool', 'TempLeaveLimit'),
		'飞行限制' : ('bool', 'FlyActionLimit'),
		}

dicMissionTrigger = {
		'初始化触发器' : ['InitTrigger', ],
		'接受触发器' : ['AcceptTrigger', ],
		'目标NPC触发器' : ['ActionTrigger', ], 
		'完成触发器' : ['FinishTrigger', ],
		'失败触发器' : ['FailTrigger', ],
		'物品使用触发器' : ['UseItemTrigger', ],
		'战斗胜利触发器' : ['FightSuccessTrigger', ],
		'战斗成功触发器' : ['FightSuccessTrigger', ],
		'战斗失败触发器' : ['FightFailTrigger', ],
		'目的地触发器' : ['DestinationTrigger',],
		'捕抓成功触发器' : ['CatchTrigger',],
		'条件达成触发器' : ['ReachCondTrigger',],
		'帮杀触发器' : ['HelpFightTrigger',],
		}


src_template_triger = '''
inherit "/module/mission/story_trigger.c";

#include <trigger.h>
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

src_template_config = '''
#include <var_prop.h>
#include <macros.h>
#include <npc_key.h>

RESET_ONUPDATE_VAR(StoryID, "%(id)s")
static mapping mpConfig = %(src_main)s;

void create()
{
	
}

mapping GetData()
{
	return mpConfig;
}

'''

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

def get_mission_detail():
	global global_mission_detail
	return global_mission_detail
          
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

def parse_mission_args(sh, i):
	row = i
	ret = {}
	beginFlg = False
	content = ""
	while row < sh.nrows:
		tmp = parse_string(sh, row, 0)
		if tmp.find("参数") == 0:
			type = parse_string(sh, row, 2)
			key = parse_string(sh, row, 1)
			val = do_parse(type, sh, row, 3)
			parse_str = PythonData2Lpc(val, False)

			#太长且字典则采用格式化, 因为list在util做了除了
			#如果map做处理，不好看
			if len(parse_str) > 200 and isinstance(val, dict):
				parse_str = PythonData2Lpc(val, True)
			content += '''\t"%s": %s, \n'''%(key, parse_str)
		row += 1

	if content != "":
		content = '''{ \n%s }''' % content
	return { "row":i+1, "content":content }

def parse_mission_item(sh, i):
	row = i + 1
	missionitem = {}
	while row < sh.nrows:
		tmp = cell_value(sh, row, 0)
		#print tmp
		if tmp.find("物品") == 0:
			type = parse_string(sh, row, 1)
			if not len(type):
				break
			missionitem[type] = {}
			missionitem[type]["Name"] = parse_string(sh, row, 2)
			missionitem[type]["MaxAmount"] = parse_int(sh, row, 3)
			missionitem[type]["UseType"] = parse_int(sh, row, 4)
			missionitem[type]["Desc"] = parse_string(sh, row, 5)
		row += 1
	return missionitem

#任务闲话
def parse_mission_idle_chat(sh, i):
	row = i
	idle_word = []
	while row < sh.nrows:
		tmp = cell_value(sh, row, 0)
		if tmp.find("目标NPC闲话") == 0:
			word = parse_string(sh, row, 1)
			if len(word):
				idle_word.append(word)
		row += 1
	return idle_word 

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
	elif type == "repKey":
		value = parse_string(sh, row, col)
		return replace_task_desc(value)
	elif type[len(type)-1] == '*':
		return parse_x_array(type[0:(len(type)-1)], sh, row, col)
	return 0

def is_null(val):
	if val == None or val == 0 or val == '' or val == [] or val == {}:
		return 1
	return 0

def parse_mission_sheet( sh, bookname ):

	global mission_error
	global global_menu_index
	global global_menu_key
	global global_mission
	global global_mission_detail

	mission_error = ""
	
	missionId = bookname + encode(sh.name)
	mission_name = ''
	mission_prop = ''
	mission_limit = ''
	mission_trigger = ''
	mission_ext_trigger = ''
	mission_cond = ''
	mission_item = ''
	mission_args = ''
	mission_flow = ''
	mission_idle_chat = ''
	mission_time = ''
	mission_type = 'TPL_MISSION_BASE'
	mission_variable = ''
	mission_area = ''
	mission_func_code = ''

	py_mission_cond = {}
	py_mission_team_cond = {}
	py_mission_item = {}
	py_mission_dynamic_desc = {}
	py_mission_long_dynamic_desc = {}
	py_npc_idle_chat = []

	i = 0
	currow = i
	cur_str = ""

	print missionId
	print PythonData2Lpc(missionId)
	mission_prop += DECLARE_VAR%("任务ID", dicMissionProp["任务ID"][1], PythonData2Lpc(missionId))

	mission_info = {}

	#清除触发器的详细信息
	clear_trigger_detail()


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
	
			if tmp == '任务类型':
				mission_type = parse_string(sh, i, 1)
				if not len(mission_type):
					mission_type = 'MISSION_BASE'
				continue
	
			#属性
			if tmp in dicMissionProp.keys():
				val = do_parse(dicMissionProp[tmp][0], sh, i, 1)
				if tmp == "任务名":
					mission_name = val
				# 不是bool,则空返回
				if not (dicMissionProp[tmp][0] == "bool" and isinstance(val, int)):
					if is_null(val):
						continue
				if tmp == "任务周期":
					mission_prop += DECLARE_VAR%(tmp, dicMissionProp[tmp][1], val)
					continue
				mission_prop += DECLARE_VAR%(tmp, dicMissionProp[tmp][1], PythonData2Lpc(val))
				continue
	
			if tmp in dicMissionDesc.keys():
				#任务追踪描述
				val = do_parse("string", sh, i, 1)
				if not is_null(val):
					py_mission_dynamic_desc[dicMissionDesc[tmp]] = replace_task_desc(val)
				val = do_parse("string", sh, i, 2)
				if not is_null(val):
					py_mission_long_dynamic_desc[dicMissionDesc[tmp]] = replace_task_desc(val)
				continue

			if tmp in dicLyricDesc.keys():
				lyric = do_parse(dicLyricDesc[tmp][0], sh, i, 1)
				if not len(lyric):
					lyric = ""
				duration = do_parse(dicLyricDesc[tmp][1], sh, i, 2)
				if not duration and len(lyric):
					duration = 5
				continue

			#任务流程
			if tmp in dicMissionFlow.keys():
				val = do_parse(dicMissionFlow[tmp][0], sh, i, 1)
				if is_null(val):
					continue
				mission_flow += DECLARE_VAR%(tmp, dicMissionFlow[tmp][1], PythonData2Lpc(val))
				continue
	
			if tmp in dicMissionMenu.keys():
				val = do_parse(dicMissionMenu[tmp][0], sh, i, 1)
				if is_null(val):
					continue
				val = replace_task_desc(val)
				mission_flow += DECLARE_VAR%(tmp, dicMissionMenu[tmp][1], PythonData2Lpc(val))
				continue
	
			#任务条件
			if tmp in dicMissionCond.keys():
				cond_val = do_parse(dicMissionCond[tmp][0], sh, i, 1)
				if is_null(cond_val):
					continue
				cond_hint = parse_string(sh, i, 2)
				py_mission_cond[tmp] = [cond_val, cond_hint]
				continue
			#任务队伍条件
			if tmp in dicMissionTeamCond.keys():
				cond_val = do_parse(dicMissionTeamCond[tmp][0], sh, i, 1)
				if is_null(cond_val):
					continue
				cond_hint = parse_string(sh, i, 2)
				py_mission_team_cond[tmp] = [cond_val, cond_hint]
				continue
			#任务限制
			if tmp in dicMissionLimit.keys():
				val = do_parse(dicMissionLimit[tmp][0], sh, i, 1)
				if is_null(val):
					continue
				mission_limit += DECLARE_VAR%(tmp, dicMissionLimit[tmp][1], PythonData2Lpc(val, True))
				continue
			#触发器
			if tmp in dicMissionTrigger.keys():
				ret = parse_triger(sh, i)
				if ret["content"] != "":
					mission_trigger += DECLARE_VAR%(tmp, dicMissionTrigger[tmp][0], '''[\n%s]\n'''%(ret["content"]))
				currow = ret["row"]
				continue
			if tmp.find("扩展触发器") >= 0:
				Re = re.compile("扩展触发器([\d]*)")
				m = Re.search(tmp)
				index = int(m.group(1))

				ret = parse_triger(sh, i)
				if ret["content"] != "":
					mission_ext_trigger += "\t%d : [\n%s\t  ],\n"%(index, ret["content"]);
				continue
			#物品
			if tmp == "任务物品":
				py_mission_item = parse_mission_item(sh, i)
				continue
			if tmp.find("目标NPC闲话") >= 0 and not len(py_npc_idle_chat):
				py_npc_idle_chat = parse_mission_idle_chat(sh, i)
				continue
			if tmp == "任务参数":
				ret = parse_mission_args(sh, i)
				if len(ret["content"]) :
					mission_args = DECLARE_VAR_NO_DESC%("MissionArgs", ret["content"])
				currow = ret["row"]
				continue
			if tmp == "任务功能代码":
				inc_str = parse_string(sh, i, 1)
				if len(inc_str):
					mission_func_code += '''\n#include "/mission/ext_method/%s.h"'''%(inc_str)
				continue
	except:
		mission_error = "error row:%d, %s"%(currow, cur_str)
		raise

	
	if len(py_mission_cond) > 0:
		mission_cond += DECLARE_VAR_NO_DESC%("MissionCond", PythonData2Lpc(py_mission_cond, True))
	if len(py_mission_team_cond) > 0:
		mission_cond += DECLARE_VAR_NO_DESC%("MissionTeamCond", PythonData2Lpc(py_mission_team_cond, True))
	if len(py_mission_item) > 0:
		mission_item = DECLARE_VAR_NO_DESC%("MissionItem", PythonData2Lpc(py_mission_item, True))
	if len(mission_ext_trigger) > 0:
		mission_ext_trigger = DECLARE_VAR_NO_DESC%("ExtendTrigger", '''{\n%s}\n'''%(mission_ext_trigger))
	mission_dynamic_desc = ""
	if len(py_mission_dynamic_desc):
		mission_dynamic_desc = DECLARE_VAR_NO_DESC%("MissionTrackDesc", PythonData2Lpc(py_mission_dynamic_desc, True))
	if len(py_mission_long_dynamic_desc):
		mission_dynamic_desc += DECLARE_VAR_NO_DESC%("MissionLongTrackDesc", PythonData2Lpc(py_mission_long_dynamic_desc, True))
	if len(py_npc_idle_chat):
		mission_idle_chat = DECLARE_VAR_NO_DESC%("MissionActionChat", PythonData2Lpc(py_npc_idle_chat, True))


	global_mission[missionId] = mission_info
	global_mission_detail[missionId] = get_trigger_detail()

	params = {
			"MissionName": mission_name,
			"MissionType": mission_type,
			"MissionProp": mission_prop,
			"MissionCondition": mission_cond,
			"MissionLimit": mission_limit,
			"MissionItem": mission_item,
			"MissionArgs": mission_args,
			"MissionTrigger": mission_trigger,
			"MissionExtTrigger": mission_ext_trigger,
			"MissionFlow": mission_flow,
			"DynamicDesc": mission_dynamic_desc,
			"MissionVariable": mission_variable,
			"MissionActionChat": mission_idle_chat,
			"MissionFuncSrc": mission_func_code,
			"StoryID": bookname,
			}
	src = TEMPLATE_SRC % params
	return src

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


SRC_TEMPLATE = """
{ 
{% autoescape off %} 
{%for row, data in table.items%}\
	{{data.PrimaryKey}}:{{%for key, value in data.Cols.items%}"{{key}}":{{value}},{%endfor%}},
{%endfor%}\
{% endautoescape %} 
};
"""

def parse_config(workdir, filename, bookname, sh):
	meta = {
		"KeyRow": 1,
		"ParseRow": 2,
		"PrimaryKeyCol": 0,
	}
	sheetname = encode(sh.name)
	sys.path.append(workdir + "tools/autocode/")
	PARSE = __import__("TemplateParse")
	UTIL = __import__("Util")
	table = {}
	inittable = PARSE.DoParseNormal2(meta, filename, sheetname)
	#content = UTIL.RenderTemplateString(SRC_TEMPLATE, inittable)
	content = UTIL.PythonData2Lpc(inittable, True)
	params = {
			"id": bookname,
			"src_main" : content,
			}
	return src_template_config % params

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
	if sheetname == "config":
		return parse_config(workdir, filename, bookname, sh)
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

#客户端导表
#	if len(client_output) and os.path.isdir(client_output):
#		client_file = client_output+ bookname + ".lua"
#		params = {
#			"src_main": PythonData2Lua(tmp_global_menu, True), 
#			"src_mission": PythonData2Lua(global_mission, True), 
#			}
#		menu_content = src_client_menu % (params)
#
#		#if not os.path.isfile(client_file):   
#		svn_add_files.append(client_file)
#		write_file(client_file, menu_content)
#		
#		os.chdir(client_output)
#		if len(svn_add_files):
#			for file in svn_add_files:
#				try : 
#					#continue
#					os.system("svn add " + file)
#				except :
#					continue
#		filelist = os.listdir(client_output) 
#		init_content = ""
#		for file in filelist:
#			if file[-4:] != ".lua":
#				continue
#			if file[:-4] == "init":
#				continue
#			init_content += '''fs_require("script/data", "info/mission/%s")\n'''%(file)
#		client_init_file = client_output + "init.lua"
#		write_file(client_init_file, init_content)
#		os.system("svn ci " + svn_user_auth + " -m " + "\"" + "导表更新 from " + client_output + "\"")

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
