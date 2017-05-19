# -*- coding: utf-8 -*-

import sys

#默认的模板
SRC_TEMPLATE = """
mapping data = {
{% autoescape off %} 
{%for row, data in table.items%}\
	{{data.PrimaryKey}}:{ {%for key, value in data.Cols.items%}\
{% if "@@" in key %}{{key|slice:"2:"}}:{{value}}, \
{% else %}"{{key}}":{{value}},{% endif %}{%endfor%} },
{%endfor%}\
{% endautoescape %} 
};

mapping get_data()
{
	return data;
}
"""

"""
data[row] = {
		"PrimaryKey": value,
		"Cols": {
			"key": value0,
			"key1": value1,
			}
		}
"""
# 本模块为通用的导表程序，如果需要自己定制，则配置一个table_meta
# 并调用PARSE.DoParse()

# 默认的配置
DefaultTableMeta = {
	"KeyRow": 1,
	"ParseRow": 2,
	"PrimaryKeyCol": 0,
	"TemplateSrc": SRC_TEMPLATE,
	#"udata": udata,
	#"Template": xxx.template        #模板
	}

def ReadTblMeta(SheetDict):
	table_meta = {}
	start_row = 0
	for row in range(0, SheetDict["nrows"], 1):
		key = SheetDict[row][0]["value"]
		value = SheetDict[row][1]["value"]
		if key == 'key_row':
			if SheetDict[row].has_key(2):
				str_value = SheetDict[row][2]["value"]
				tmp_value = 0
				if  isinstance(str_value, int):
					tmp_value = str_value
				elif  isinstance(str_value, float):
					tmp_value = int(str_value)
				elif isinstance(str_value, str) or isinstance(str_value, unicode):
					str_value = str_value.strip()
					if len(str_value):
						tmp_value = int(str_value)
				if tmp_value:
					value = tmp_value
			table_meta["KeyRow"] = int(float(value)) - 1
			continue
		if key == 'start_row':
			table_meta["ParseRow"] = int(float(value)) - 1
			start_row = int(float(value))
			continue
		if start_row and row > start_row:
			break
	if len(table_meta):
		table_meta["PrimaryKeyCol"] = 0
		table_meta["TemplateSrc"] = SRC_TEMPLATE
		return table_meta
	else:
		return DefaultTableMeta

if __name__ == "__main__":
	WorkDir, ParseFile, ParseSheet, OutputFile = sys.argv[1:5]
	sys.path.append(WorkDir + "tools/autocode/")
	PARSE = __import__("TemplateParse")
	resDict = PARSE.XlsSheet2Dict(ParseFile, ParseSheet)
	table_meta = ReadTblMeta(resDict)
	PARSE.DoParseNormalWrite(table_meta, ParseFile, ParseSheet, WorkDir + OutputFile, resDict)
