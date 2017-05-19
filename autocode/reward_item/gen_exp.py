# -*- coding: utf-8 -*-

import sys

#默认的模板
SRC_TEMPLATE = """
#include <var_prop.h>
#include <value_reward.h>

{% autoescape off %} 
{%for key, value in var_map.items%}\
static float {{key}} = {{value}};
{%endfor%}\
{% endautoescape %} 

{% autoescape off %} 
{%for key, value in ext_var_map.items%}\
RESET_ONUPDATE_VAR({{key}}, {{value}})
{%endfor%}\
{% endautoescape %} 

mapping GetData(object user, int tasknum)
{
	int grade =  user->GetGrade();
	mapping data = {};

{%for formula in formula_list%}\
	data[{{formula.key}}] = {{formula.value}};
{%endfor%}\

	return data;
}
"""

EXP_DIR = "data/value_reward/"

def DoParseBeginEnd(SheetDict, begin_ident, end_ident):
	parse_row = 0
	var_map = {}
	PARSE = __import__("TemplateParse")
	UTIL = __import__("Util")

	for row in range(0, SheetDict["nrows"], 1):
		key = SheetDict[row][0]["value"]
		if key == end_ident:
			return var_map
		if key == begin_ident:
			parse_row = row + 1
			var_map = {}
			continue
		if row < parse_row:
			continue

		key = SheetDict[row][0]["value"].strip()
		value = SheetDict[row][1]["value"]
		value = PARSE.parse_mixed(value)
		var_map[key] = UTIL.PythonData2Lpc(value, False)
	return {}

formula_meta = {
	u'人物经验公式' : [ "K_REWARD_USER_EXP" ], 
	u'召唤兽经验公式': [ "K_REWARD_SUMM_EXP" ],
	u'人物金钱公式': [ "K_REWARD_CASH" ],
	u'元神公式': [ "K_REWARD_YUANSHEN" ],
	u'魅力公式': [ "K_REWARD_MEILI" ],
}


def DoParseFormula(SheetDict):
	var_list = [] 
	for row in range(0, SheetDict["nrows"], 1):
		key = SheetDict[row][0]["value"]
		value = SheetDict[row][1]["value"]
		if key not in formula_meta.keys():
			continue
		if isinstance(value, unicode) or isinstance(value, str):
			value = value.replace("POWER", "pow")
		print "______",value
		var_list.append({"key":formula_meta[key][0], "value":value})
	return var_list 

def DoParseGradeFormula(SheetDict):
	global PARSE, UTIL
	parse_row = 0
	var_list = []
	for row in range(0, SheetDict["nrows"], 1):
		key = SheetDict[row][0]["value"]
		if key == "grade_end":
			return var_list
		if key == "grade_begin":
			parse_row = row + 1
			var_list = []
			continue
		if not parse_row or row < parse_row:
			continue

		str_grade = SheetDict[row][0]["value"].strip()
		str_grade_data = SheetDict[row][1]["value"]

		grades = str_grade.split(",")
		
		low_grade, high_grade = int(grades[0]), int(grades[1])

		var_map = {}
		var_map["low_grade"] = low_grade
		var_map["high_grade"] = high_grade
		var_map["grade_data"] = str_grade_data

		var_list.append(var_map)
	return []

if __name__ == "__main__":
	global PARSE, UTIL
	WorkDir, ParseFile = sys.argv[1:3]
	sys.path.append(WorkDir + "tools/autocode/")
	PARSE = __import__("TemplateParse")
	UTIL = __import__("Util")
	resDict = UTIL.Xls2Dict(ParseFile)

	for sheetindex in resDict.keys():
		name = resDict[sheetindex]["name"]
		if name in [u'说明页', u'说明']:
			continue
		table = {}
		table["var_map"] = DoParseBeginEnd(resDict[sheetindex], "table_begin", "table_end")
		table["ext_var_map"] = {'TiliEffect': '0', 'ExtRewardType': '([])', 'LeaderReward':'0',}
		tmpmap = DoParseBeginEnd(resDict[sheetindex], "extra_table_begin", "extra_table_end")
		table["ext_var_map"].update(tmpmap)

		table["formula_list"] = DoParseFormula(resDict[sheetindex])
		table["grade_formula"] = DoParseGradeFormula(resDict[sheetindex])
		print table

		Content = UTIL.RenderTemplateString(SRC_TEMPLATE, table)

		outputfile = EXP_DIR + name + ".c"
		PARSE.DoWrite(Content, WorkDir + outputfile)
		UTIL.WriteUpdateFile(WorkDir, outputfile + "\n")

