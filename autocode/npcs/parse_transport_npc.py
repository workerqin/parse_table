# -*- coding: utf-8 -*-

import sys
import os

#默认的模板
SRC_TEMPLATE = """
// Transport NPC
#include <user_key.h>

{% autoescape off %} 
static mapping mpTranInfo =
{{table}}
;

void InitNpc(int npcid) 
{
	
}

int DoClick(object user, int npcid)
{
	return Import("UTIL")->DoClickTransNpc(user, npcid, mpTranInfo);
}
{% endautoescape %} 
"""


if __name__ == "__main__":
	WorkDir, ParseFile, ParseSheet, OutputDir = sys.argv[1:5]
	sys.path.append(WorkDir + "tools/autocode/")
	PARSE = __import__("TemplateParse")
	UTIL = __import__("Util")
	table = PARSE.DoParseBeginEnd(ParseFile, ParseSheet)
	OutputFile = ""
	if len(table):
		for primary in table.keys():
			data = table[primary]
			vars_map = {}
			vars_map["table"] = UTIL.PythonData2Lpc(data, True)
			OutputFile = OutputDir + primary + ".c"
			Content = UTIL.RenderTemplateString(SRC_TEMPLATE, vars_map)
			PARSE.DoWrite(Content, WorkDir + OutputFile)
			if os.path.isfile(WorkDir + OutputFile):
				UTIL.WriteUpdateFile(WorkDir, OutputFile + "\n")
