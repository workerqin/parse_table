#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import xlrd
import sys
import os
import glob
import getopt
import re
from datetime import date

sys.path.append("../")
sys.path.append("tools/autocode")

from Util import PythonData2Lpc 
from Util import PythonData2Lua 

import sys
import os
#sys.path.append("../../../module/trigger")
import trigger_command 
dicTriggerCmd = trigger_command.data
dicNameToCmd = trigger_command.nameToCmd

version = "1.0"
error = ""

#全局菜单表
global global_trigger_detail
global global_trigger_var

src_template = '''
// File     : %s.c
// Purpose  : 触发器实例
// Created  : %s
// By       : gen_triggers.py
inherit "trigger/base.c";

#include <trigger.h>

// ------------------------------------------
// 自动生成的数据部分

%s

void create()
{
	// 设置实例数
	SetInstanceLimit(%d);
	// 设置触发器内容
	SetTriggerType(TYPE_NORMORL);
}
// -------------------------------------------

'''

#维护菜单表，将菜单表保持服务器跟客户端都有一份，这样只需要编号就可以取到了
dicMissionAtomMenu = {
		'NPC_MENU': {'col': 1, },
		'TALK_PAGE_NPC': {'col': 1, },
		'TALK_PAGE_USR': {'col': 1, },
		'TALK_PAGE' : {'col': 1, },
		}

def filter_space(value):
	value1 = value.replace(" ", "")
	value1 = value1.replace("，", ",")
	value1 = value1.replace("：", ":")
	value1 = value1.replace("；", ";")
	value1 = value1.replace("“", "\"")
	value1 = value1.replace("”", "\"")
	return value1           

def usage():
	print "USAGE:gen_triggers.py excel_file"
	print "--version : Prints the version number"
	print "--help    : Display this help"

def write_file(filename, content ):
	if filename == "":
		return
	msg = "writting to file trigger",filename
	#print msg

	try :
		f = file(filename, "w+b")
	except :
		msg = "can not write to", filename
		#print msg
		sys.exit(-1)
	f.write(content)
	f.close()

def encode(val):
	import locale
	encoding = locale.getdefaultlocale()[1]
	res = val.encode(encoding)
	return res

def cell_value(sh, row, col):
	try:
		val = sh.cell_value(rowx=row, colx=col)
		if val == None:
			return ""
	except:
		return ""
	try : 
		return encode(val)
	except :
		return val

def get_error():
	global error
	return error

def parse_string(sh, row, col):
	val = cell_value(sh, row, col)
	try :
		if val == None:
			return ""
		ret = "%d"%(int(float(val)))
	except :
		ret = val.strip()
	return ret

def parse_mixed(sh, row, col):
	value = cell_value(sh, row, col)

	if  isinstance(value, int):
		return value
	if  isinstance(value, float):
		if value > 0:
			return int(value+0.5)
		return int(value)

	if value[0] == "[" or value[0] == "{":
		return eval(value)
	return value

def parse_int(sh, row, col):
	ret = 0
	try :
		tmp = cell_value(sh, row, col)
		ret = int(float(tmp))
	except :
		ret = 0
	return ret

def parse_map(sh, row, col):
	ret = parse_string(sh, row, col)
	ret = ret.replace("，", ",")
	ret = ret.replace("：", ":")
	if len(ret):
		return eval('{' + ret + '}')
	return {}

def parse_array(sh, row, col):
	ret = parse_string(sh, row, col)
	ret = ret.replace("，", ",")
	if len(ret):
		if ret[0] == '$':
			return ret
		try : 
			ret = eval('[' + ret + ']')
			return ret
		except ValueError:
			return ret
	return []

def parse_x_array(sh, row, col):
	ret_arr = []
	for varCol in range(col, sh.ncols):
		tmpStr = cell_value(sh, row, varCol)
		#type = sh.cell_type(rowx=row, colx=varCol)
		try:
			intval = int(tmpStr)
			ret_arr.append(intval)
		except ValueError:
			if len(tmpStr) and (tmpStr[0] == '[' or tmpStr[0] == '{'):
				val = eval(tmpStr)
			else:
				val = tmpStr
			ret_arr.append(val)
	return ret_arr


def parse_undef_val(sh, row, col):
	type = parse_string(sh, row, 1)
	if type == "?":
		return 0
	if type == "syscall":
		type = "string"
	return do_parse(type, sh, row, col)

def do_parse(type, sh, row, col):
	if type == "string":
		return parse_string(sh, row, col)
	if type == "mixed":
		return parse_mixed(sh, row, col)
	if type == "macros":
		tmp = parse_string(sh, row, col)
		if len(tmp):
			if tmp[0] == '$':
				return tmp
			return "@@"+parse_string(sh, row, col)
		return 0
	elif type == "int":
		tmp = parse_string(sh, row, col)
		if len(tmp) and tmp[0] == '$':
			return tmp
		return parse_int(sh, row, col)
	elif type == "map":
		return parse_map(sh, row, col)
	elif type == "array":
		return parse_array(sh, row, col)
	elif type == "*":
		return parse_x_array(sh, row, col)
	elif type == "?":
		return parse_undef_val(sh, row, col)
	return 0

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

def clear_detail():
	global global_trigger_detail
	global_trigger_detail = {}
	global_trigger_var = {}

def get_detail():
	global global_trigger_detail
	return global_trigger_detail

def get_trigger_detail(cmds):
	global global_trigger_detail
	global global_trigger_var

	if not len(cmds):
		return

	if cmds[0] in ["ACCEPT_MISSION", "ASSIGN_MISSION", "TRY_ACCEPT_MISSION"]:
		if "missions" not in global_trigger_detail.keys():
			global_trigger_detail["missions"] = {}
		global_trigger_detail["missions"][cmds[1]] = cmds[0]
		return
	if cmds[0] == "ACCEPT_CHILD_MISSION":
		if u"sub_missions" not in global_trigger_detail.keys():
			global_trigger_detail["sub_missions"] = []
		global_trigger_detail["sub_missions"].append(cmds[1])
		return
	if cmds[0] == "RUN_TRIGGER":
		if u"triggers" not in global_trigger_detail.keys():
			global_trigger_detail["triggers"] = []
		global_trigger_detail["triggers"].append(cmds[1])
		return
	if cmds[0] in ["START_STORY", "START_INTERACTIVE_STORY"]:
		if "storys" not in global_trigger_detail.keys():
			global_trigger_detail["storys"] = []
		global_trigger_detail["storys"].append(cmds[1])
		return

	if cmds[0] == "TRANS_PROP":
		if "vars" not in global_trigger_detail.keys():
			global_trigger_detail["vars"] = {}
		global_trigger_detail["vars"][cmds[1]] = [cmds[2], cmds[3]]

def parse_name_to_cmd(var):
	if var in dicNameToCmd.keys():
		return dicNameToCmd[var]
	else:
		return var

def parse_line_cmd(sh, row):
	# 触发器类型
	global error

	triggerType = cell_value(sh, row, 0)
	triggerLen = 0
	cmds = []
	error = ""
	try:
		triggerType = triggerType.strip()
		if triggerType[0] == '#':
			return cmds

		# 中文指令转英文
		triggerType = parse_name_to_cmd(triggerType)

		# 触发器长度
		if triggerType in dicTriggerCmd.keys():
			triggerLen = len(dicTriggerCmd[triggerType])
		for col in range(0, triggerLen):
			error = "row:%d col:%d command:%s"%(row, col, triggerType)
			cmd = do_parse(dicTriggerCmd[triggerType][col], sh, row, col)
			if col == 0:
				cmd = parse_name_to_cmd(cmd)
			cmds.append(cmd)
	except ValueError:
		error = "row:%d command:%s"%(row, triggerType)
		raise

	if triggerLen == 0:
		error = "row:%d command:%s"%(row, triggerType)
		raise

	return cmds

def parse_menu_var(var):
	global error
	Re = re.compile("([\$|\&][\w][:\w]*)")
	arrtmp = Re.findall(var)
	mpSort = PyArraySort2LpcSrc(arrtmp)
	menukeys = []

	valstr = var
	ikey = 0
	#参数限制， 不然$10,$11可能跟$1冲突, 所以默认只解释1位
	if len(mpSort) >= 10:
		raise
	while ikey < len(mpSort):
		valstr = valstr.replace(mpSort[ikey], "$%d"%(ikey))
		menukeys.append(mpSort[ikey])
		ikey += 1
	
	return valstr, menukeys

def parse_line(sh, row):
	global error

	error = ""
	if (sh.cell_value(rowx=row, colx=0).strip() == ''):
		return '';
		#注释
		if (sh.cell_value(rowx=row, colx=0).strip() == '#'):
			strLine = "        // " + sh.cell_value(rowx=row, colx=1)
			strLine += (strLine + "\n")
			return strLine;

	cmds = parse_line_cmd(sh, row)
	get_trigger_detail(cmds)

	if not len(cmds):
		return ""
		# 头
	strLine = '        [ ';

	if cmds[0] in dicMissionAtomMenu.keys():
		val = cmds[dicMissionAtomMenu[cmds[0]]['col']]
		menuval, menukeys = parse_menu_var(val)
		cmds[dicMissionAtomMenu[cmds[0]]['col']] = [menuval, menukeys]

	for index in range(0, len(cmds)):
		strLine += '''%s, '''%(PythonData2Lpc(cmds[index]))

	strLine += '], ';
	return strLine

def parse_sheet(sh):
	lpcSrc = ""
	allModules = ''

	content = ""
	beginFlg = 0;
	#各模块名
	modules = []
	# 各模块的起止
	modulesBegin = []
	modulesEnd = []
	instanceLimit = 0
	allowRepeatCall = 0
	for i in range(0, sh.nrows):
		# 实例数限制
		if cell_value(sh, i, 0) == "实例数限制:":
			instanceLimit = int(cell_value(sh, i, 1))
			continue
		if cell_value(sh, i, 0) == "ALLOW_REPEAT_CALL":
			allowRepeatCall = 1
			continue
			# 找到模块起始点
		if beginFlg == 0:
			if cell_value(sh, i, 0) == "BEGIN":
				modules.append(cell_value(sh, i-1, 0))
				beginFlg = 1
				modulesBegin.append(i)
			continue
				# 找到模块终止点
		elif beginFlg == 1:
			if cell_value(sh, i, 0) == "END":
				beginFlg = 0
				modulesEnd.append(i)
			continue

	for i in range(0, len(modules)):
		#print modules[i]
		moduleContent = ''
		strModule = '''
static mixed *  %s = [
%s
];'''
		for row in range(modulesBegin[i]+1, modulesEnd[i]):
			moduleContent += (parse_line(sh, row) + "\n")
		strModule = strModule%(modules[i], moduleContent)
		allModules += (strModule + '\n')
		allModules += '''mixed * get_%s() { return %s; }\n'''%(modules[i], modules[i])
	
	if allowRepeatCall:
		allModules += '''\nint allow_repeat_call() {return 1;}\n'''

	return { "content": allModules, "instancelimit":instanceLimit, }

def parse_xls(filename, outputfile):
	try:
		book = xlrd.open_workbook(filename)
	except:
		msg = "can't open file? " + filename
		#print( msg )
		usage()
		sys.exit(-1)
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		# 说明无需生成，触发器总表 解析方法不同
		if encode(sh.name) != "说明" and encode(sh.name) != "触发器总表":
			transformSh = book.sheet_by_index(x)
			ret = parse_sheet(sh)
			strLpc = src_template%(filename, date.today(), ret["content"], ret["instancelimit"])
			write_file(outputfile, strLpc)


if __name__ == "__main__":
	sys.path.append("../")
	if len(sys.argv) < 3:
		usage();
	elif sys.argv[1].startswith('--'):
		option = sys.argv[1][2:]
		if option == 'version':
			print 'Version',version
		elif option == 'help':
			usage()
		sys.exit()
	else:
		filename = sys.argv[1]
		outputfile = sys.argv[2] 
		parse_xls(filename, outputfile) 

