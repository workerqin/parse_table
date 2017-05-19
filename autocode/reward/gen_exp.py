# -*- coding: utf-8 -*-

import sys

#默认的模板
SRC_TEMPLATE = """
#include <var_prop.h>

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

mapping GetExp(int grade, int tasknum)
{
	int exp = 0, monstexp = 0, tili = 0, jingli = 0, cash = 0, lineup = 0, deflineup = 0, renqi = 0, xinfa = 0, xinfa_shengwang = 0; 
	mapping mpExpInfo = ([]);

{%if formula_map.user%}\
	{{formula_map.user}};
{%endif%}\
{%if formula_map.summon%}\
	{{formula_map.summon}};
{%endif%}\
{%if formula_map.tili%}\
	{{formula_map.tili}};
{%endif%}\
{%if formula_map.jingli%}\
	{{formula_map.jingli}};
{%endif%}\
{%if formula_map.cash%}\
	{{formula_map.cash}};
{%endif%}\
{%if formula_map.lineup%}\
	{{formula_map.lineup}};
{%endif%}\
{%if formula_map.deflineup%}\
	{{formula_map.deflineup}};
{%endif%}\
{%if formula_map.renqi%}\
	{{formula_map.renqi}};
{%endif%}\
{%if formula_map.xinfa%}\
	{{formula_map.xinfa}};
{%endif%}\
{%if formula_map.xinfa_shengwang%}\
	{{formula_map.xinfa_shengwang}};
{%endif%}\

	mpExpInfo = ([ 
		"user": exp, 
		"summon": monstexp, 
		"tili": tili, 
		"jingli": jingli, 
		"cash": cash, 
		"lineup": lineup, 
		"deflineup" : deflineup,
		"renqi": renqi,
		"xinfa": xinfa,
		"xinfa_shengwang": xinfa_shengwang,
	]);

{%for value in grade_formula%}\
	if (grade >= {{value.low_grade}} && grade <= {{value.high_grade}}) {
{%if value.user_formula%}\
		mpExpInfo["user"] = {{value.user_formula}};
{%endif%}\
{%if value.summon_formula%}\
		mpExpInfo["summon"] = {{value.summon_formula}};
{%endif%}\
		return mpExpInfo;
	}
{%endfor%}
	return mpExpInfo;
}
"""

EXP_DIR = "data/exp/"

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

def DoParseFormula(SheetDict):
	var_map = {}
	for row in range(0, SheetDict["nrows"], 1):
		key = SheetDict[row][0]["value"]
		value = SheetDict[row][1]["value"]
		if key == u'人物经验公式':
			value = value.replace("POWER", "pow")
			var_map['user'] = value
			continue
		if key == u'召唤兽经验公式':
			value = value.replace("POWER", "pow")
			var_map['summon'] = value
			continue
		if key == u'人物精力公式':
			value = value.replace("POWER", "pow")
			var_map['jingli'] = value
			continue
		if key == u'人物体力公式':
			value = value.replace("POWER", "pow")
			var_map['tili'] = value
			continue
		if key == u'人物金钱公式':
			value = value.replace("POWER", "pow")
			var_map['cash'] = value
			continue
		if key == u'阵型经验公式':
			value = value.replace("POWER", "pow")
			var_map['lineup'] = value
			continue
		if key == u'默认阵型经验公式':
			value = value.replace("POWER", "pow")
			var_map['deflineup'] = value
			continue
		if key == u'人物人气公式':
			try:
				value = value.replace("POWER", "pow")
			except:
				pass
			var_map['renqi'] = value
			continue
		if key == u'人物心法熟练度公式':
			value = value.replace("POWER", "pow")
			var_map['xinfa'] = value
			continue
		if key == u'人物心法声望公式':
			value = value.replace("POWER", "pow")
			var_map['xinfa_shengwang'] = value
			continue
	return var_map

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
		user_formula = SheetDict[row][1]["value"]
		summ_formula = SheetDict[row][2]["value"]

		grades = str_grade.split(",")
		
		low_grade, high_grade = int(grades[0]), int(grades[1])

		var_map = {}
		var_map["low_grade"] = low_grade
		var_map["high_grade"] = high_grade
		var_map["user_formula"] = user_formula
		var_map["summon_formula"] = summ_formula

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
		table["ext_var_map"] = {u'TiliEffect': '0', u'ExtRewardType': u'([])', u'LeaderReward':'0',}
		tmpmap = DoParseBeginEnd(resDict[sheetindex], "extra_table_begin", "extra_table_end")
		table["ext_var_map"].update(tmpmap)

		table["formula_map"] = DoParseFormula(resDict[sheetindex])
		table["grade_formula"] = DoParseGradeFormula(resDict[sheetindex])

		Content = UTIL.RenderTemplateString(SRC_TEMPLATE, table)

		outputfile = EXP_DIR + name + ".c"
		PARSE.DoWrite(Content, WorkDir + outputfile)
		UTIL.WriteUpdateFile(WorkDir, outputfile + "\n")

