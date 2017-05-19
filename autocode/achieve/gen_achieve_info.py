# -*- coding: utf-8 -*-

import sys
import re

#默认的模板
SRC_TEMPLATE = u"""
mapping data = ([ 
{% autoescape off %} 
{%for row, data in table.items%}\
	{%for key, value in data.Cols.items%}"{{key}}":{{value}},{%endfor%}]),
{%endfor%}\
{% endautoescape %} 
]);

mapping get_data()
{
	return data;
}
"""

#name(c2t)	type(int)	desc(string)
ACHIEVE_SRC = u"""
#include "/module/achieve/achieve_arg_def.h"
#include "/module/achieve/achieve_def.h"
mapping data = 
%s;

mapping get_data()
{
	return data;
}
"""

ACHIEVE_DEFINE_SRC = u"""
#ifndef __ACHIEVE_DEF_H_
#define __ACHIEVE_DEF_H_

{% autoescape off %} 
{%for key, value in table_stats.items%}\
#define {{value.0|ljust:"40"}}{{key|ljust:30}}/*{{value.1}}*/
{%endfor%}\

{%for key, value in table_achieve.items%}\
#define {{value.0|ljust:"60"}}{{key|ljust:40}}/*{{value.1}}*/
{%endfor%}\
{% endautoescape %} 

#endif /*__ACHIEVE_DEF_H_*/
"""

ACHIEVE_COND_SRC1 = u'''fun(int value, int stats, mapping arg) {if (%s) return value;}'''
ACHIEVE_COND_SRC2 = u'''fun(int value, int stats, mapping arg) {if (%s) return (%s);}'''

# 默认的配置
DefaultTableMeta = {
	"KeyRow": 9,
	"ParseRow": 11,
	}


def DoParseStats(data_map):
	parse_row = 0
	vars_map = {}
	define_map = {}
	PARSE = __import__("TemplateParse")
	for row in data_map.keys():
		data = data_map[row]
		name = data["Cols"]["name"]
		if len(name) <= 0:
			continue

		temp_data = {}
		for key in data["Cols"].keys():
			value = data["Cols"][key]
			if key == u"cond":
				if not len(value):
					continue
				value = value.replace(u"？", "?");
				exp_strs = []
				exp_str = ""
				if value.find("?") >= 0:
					value = value.replace(" ", "")
					exp_strs = value.split("?")
					exp_str = "@@"+ ACHIEVE_COND_SRC2 % (exp_strs[0], exp_strs[1])
				else:
					exp_str = "@@"+ ACHIEVE_COND_SRC1 % (value)

				temp_data[key] = exp_str
				#任务
				#arg[AK_MISSION_ID] == "jq_nbM029"
				value = value.strip().replace(" ", "")
				Re = re.compile("arg\[AK_MISSION_ID\]==\"([\w]*)\"")
				m = Re.findall(value)
				if not len(m):
					continue
				temp_data["missions"] = m
				continue
			if key == u"name":
				temp_data[key] = value[0]
				continue
			temp_data[key] = value

		primary_key = "ACHIEVE_" + name[1]

		primary_key_macros = "@@" + primary_key
		if primary_key_macros in vars_map.keys():
			print PARSE.encode(name[0]), "repeat define[", PARSE.encode(vars_map[primary_key_macros]["name"]), "]"
			raise
		print data["Cols"]["name"] 
		if not data["Cols"].has_key("id"):
			continue;
		ach_id = data["Cols"]["id"]
		if ach_id in define_map.keys():
			print PARSE.encode(name[0]), "id repeat", ach_id
			raise

		#print data["Cols"].keys()
		if data["Cols"].has_key("id"):
			vars_map[primary_key_macros] = temp_data
			define_map[data["Cols"]["id"]] = [primary_key, name[0]]

	return vars_map, define_map


def ParseAchieveDef(data_map):
	define_map = {}
	for row in data_map.keys():
		data = data_map[row]
		print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ", row,  data["Cols"])
		if len(data["Cols"]) == 0:
			continue;
		name = data["Cols"]["name"]
		if not len(name):
			continue

		ach_id = data["Cols"]["id"]
		str_ach_id = "ACH_ID_" + PARSE.parse_c2t(name)
		if str_ach_id in define_map.keys():
			print PARSE.encode(name), "id repeat", ach_id
			raise
		define_map[ach_id] = [str_ach_id, name]

	return define_map

if __name__ == "__main__":
	global PARSE, UTIL
	WorkDir, ParseFile, OutPutFile = sys.argv[1:4]
	sys.path.append(WorkDir + "tools/autocode/")
	PARSE = __import__("TemplateParse")
	UTIL = __import__("Util")
	resDict = UTIL.Xls2Dict(ParseFile)
	define_file = WorkDir + "module/achieve/achieve_def.h"

	table = {}
	for sheetindex in resDict.keys():
		name = resDict[sheetindex]["name"]
		if name in [u'说明页', ]:
			continue
		if name == u'统计':
			data_map = PARSE.DoParseSheet(DefaultTableMeta, resDict[sheetindex], 0)
			vars_map,define_map = DoParseStats(data_map["table"])

			table_src = UTIL.PythonData2Lpc(vars_map, True)
			content = ACHIEVE_SRC % (table_src)
			PARSE.DoWrite(content, WorkDir + OutPutFile)
			table["table_stats"] = define_map 
			continue
		if name == u"成就":
			data_map = PARSE.DoParseSheet(DefaultTableMeta, resDict[sheetindex], 0)
			define_map = ParseAchieveDef(data_map["table"])
			table["table_achieve"] = define_map 
			continue
	if len(table):
		define_content = UTIL.RenderTemplateString(ACHIEVE_DEFINE_SRC, table)
		PARSE.DoWrite(define_content, define_file)
