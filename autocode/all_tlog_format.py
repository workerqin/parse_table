#-*- coding: utf-8 -*-

import xml.parsers.expat 
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')

partner = re.compile(r"\[.*\]")
tlog_types = []
safe_tlog_types = []


global keep_name 
#file_name = "手游经分Tlog标准_V1.2.7.xml"
line_start = "//=================auto generate start tlog==================="
line_end = "//=================auto generate end tlog====================="
save_list = {}
name_list = {}

type2format = {
    u'string':"%s",
    u'int':"%d",
    u'datetime':"%s",
    u'float':"%f",
    u'uint':"%d",
    u'uint64':"%d",
}

safe_func_template = """
void TLog%s(object oUser, mixed* args)
{
	if (sizeof(GetAppID(oUser->GetChannel())) <= 0) return;

    mixed* allLog = MustSafeLogInfo(oUser) + args;
    "module/tlog/main"->TLogInfo("all_tlog", 0, 0, %s, allLog...);
}
"""

func_template = """
void TLog%s(object oUser, mixed* args)
{
	if (sizeof(GetAppID(oUser->GetChannel())) <= 0) return;

    mixed* allLog = MustLogInfo(oUser) + args;
    "module/tlog/main"->TLogInfo("all_tlog", 0, 0, %s, allLog...);
}
"""

game_state = """
void TLog%s(mixed* args)
{
    "module/tlog/main"->TLogInfo("all_tlog", 0, 0, %s, args...);
}
"""


def start_element(name, attrs):
    #print 'Start element:', name, attrs

    if name == "struct":
        global keep_name
        keep_name = attrs[u"name"].encode("utf-8")
        save_list[keep_name] = [];
        name_list[keep_name] = [];

    if name == "entry":
        save_list[keep_name].append(attrs[u"type"])
        name_list[keep_name].append(attrs[u"name"])

def end_element(name):
    #print 'End element:', name
    if name == "struct":
        global keep_name
        keep_name = ""

def char_data(data):
    pass
    #print 'Character data:', repr(data)

def handler_tlog(result, tmp):
	if tmp[0] in ["GameSvrState", "GuildFlow", "SnsFlow", "IDIPFLOW", "ADDMAILFLOW", "DELMAILFLOW"]:
		result.append(game_state % (tmp[0], tmp[0].upper()))
	else:
		result.append(func_template % (tmp[0], tmp[0].upper()))

def handler_safe_tlog(result, tmp):
	if tmp[0] in ["SecRoundStartFlow", "SecRoundEndFlow",]:
		pass
	else: 
		result.append(safe_func_template % (tmp[0], tmp[0].upper()))

def gen_new_content(filename):
    p = xml.parsers.expat.ParserCreate()
    p.StartElementHandler = start_element
    p.EndElementHandler = end_element
    p.CharacterDataHandler = char_data

    fp = file(filename);
    p.ParseFile(fp);

    result = []
    
    for key, value in save_list.items():
        tmp = [key,]
        for type in value:
            tmp.append(type2format[type])
        head = "//%s \n#define %s " % ("|".join(name_list[key]), tmp[0].upper())
        result.append(head + "\"" + "|".join(tmp) + "\"")
        if tmp[0] in tlog_types:
            handler_tlog(result, tmp)
        if tmp[0] in safe_tlog_types:
            handler_safe_tlog(result, tmp)
    return "\n".join(result)


def write_file(filename, path_content):
    tmp, flag = [], 1

    fp = file(filename, "r")
    line_list = fp.readlines()
    for line in line_list:
        if flag == 1:
            tmp.append(line)
        if flag and line_start in line:
            tmp.append(gen_new_content(path_content))
            tmp.append("\n")
            flag = 0
        if not flag and line_end in line:
            tmp.append(line)
            flag = 1
    fp.close()
    fp = file(filename, "w")
    fp.write("".join(tmp))
    fp.close()
            

#取出所有的tlog类型和safe_tlog类型
def get_tlog_types(xml_file):
	fd = open(xml_file, "r")
	for line in fd.readlines():
		line = line.strip()
		if line.startswith("tlog_type"):
			par_line = partner.findall(line)[0]
			par_line = par_line[1:-1].strip()
			tlog_list= par_line.split(",")
			for key in tlog_list:
				tlog_types.append(key.strip())

		if line.startswith("safe_tlog_type"):
			safe_par_line = partner.findall(line)[0]
			safe_par_line = safe_par_line[1:-1]
			safe_tlog_list= safe_par_line.split(",")
			for key in safe_tlog_list:
				safe_tlog_types.append(key.strip())
	fd.close()

if __name__ == "__main__":
    path_dir, path_content, path_write = sys.argv[1:]

    get_tlog_types(path_content)

    write_file(path_dir+path_write, path_content)

