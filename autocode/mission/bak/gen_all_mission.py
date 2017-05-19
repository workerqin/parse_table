#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import xlrd
import shutil
import time

from gen_mission import parse_xls
from gen_mission import get_xls_missions
from gen_mission import get_error
from gen_mission import get_mission_detail

sys.path.append("../")
sys.path.append("tools/autocode")

from Util import PythonData2Lpc 
from Util import PythonData2Lua 

config_file_name = "config.xls"
work_dir = ""
log_file = ""
config_svn_path = "https://192.168.0.3/qtz/fsegg/design/trunk/D导表文档/server/R任务库/"

#客户端文档输出路径
client_svn_path = "https://192.168.0.3/qtz/fs/design/data/info/mission/"

svn_user_auth = " --username fs_autoparse_design --password \!QA2ws3ed"

MISSIONS_OUTPUT = "data/missions"
#svn_user_auth = ""

src_preload = '''
static mapping mpPreloadMissions = %s;


static mixed *lsPreloadStory = %s;

mapping GetPreloadMissions()
{
	return mpPreloadMissions;
}

mixed *GetAllStory()
{
	return lsPreloadStory;
}
'''

src_tree = '''

static mapping mpMissionTree = %s;

'''

def usage():
        print "USAGE:gen_all.py 任务总列表.xls path "
        print '''\
          --version : Prints the version number
          --help    : Display this help'''

def encode(val):
	import locale
	encoding = locale.getdefaultlocale()[1]
	res = val.encode(encoding)
	return res

def write_file(filename, content ):
	msg = "writting to file",filename
	print msg
	try :
		f = file(filename, "a+")
	except :
		msg = "can not write to", filename
		print msg
		sys.exit(-1)
	f.write(content)
	f.close()

def log(log_str):
	global log_file
	write_file(log_file, log_str)

#将svnpath co or up 到workdir里面
def prepare_file(workdir, svnpath):
	tmp_dir = workdir + "tmp/"
	os.chdir(tmp_dir)

	filename = os.path.basename(svnpath)
	svn_co_dir = os.path.dirname(svnpath)

	log("\n开始更新 %s"%(svn_co_dir))
	if not os.path.isdir(svn_co_dir):
		os.system("svn co " + svn_co_dir + svn_user_auth)
	else:
		os.system("svn up " + svn_co_dir + svn_user_auth)
	#os.chdir( workdir )

def usage():
    print "USAGE:gen_all_mission.py 工作目录 导表标识"
    print "--version : Prints the version number"
    print "--help    : Display this help"

if __name__ == "__main__":
	sys.path.append("../")
	if len(sys.argv) < 2:
		sys.exit(1)

	work_dir = (sys.argv[1]).strip()

	tblindex = ""
	if len(sys.argv) == 3:
		tblindex = sys.argv[2].strip() 

	if not work_dir.endswith("/"):
		work_dir = work_dir + "/"
	log_file = work_dir + "log" + "/parse_log.log"
	preload_file = work_dir + "module/mission/preload.c"
	tree_file = work_dir + "module/mission/tree.c"

	log("\n开始更新..." )
	prepare_file(work_dir, config_svn_path)
	#prepare_file(work_dir, client_svn_path)

	#pre_dir = os.path.basename(os.path.dirname(xls_dir))

	lib_basedir = work_dir + "tmp/" + os.path.basename(os.path.dirname(config_svn_path)) + "/"
	xlsfile = lib_basedir + "任务列表.xls" 

	print lib_basedir
	print xlsfile
	client_output = work_dir + "tmp/" + os.path.basename(os.path.dirname(client_svn_path)) + "/"
	print client_output

	Missionxls = ""
	MissionOutputDir = work_dir + MISSIONS_OUTPUT

	try :
		book = xlrd.open_workbook(xlsfile)
	except :
		msg = "can't open file %s"%(xlsfile)
		print( msg )
		usage()
		sys.exit(-1)

	output_map = {}
	tree_map = {}
	output_all_missions = []
	try:
		for x in xrange(book.nsheets):
			sh = book.sheet_by_index(x)
			if sh.name == u"说明":
				continue

			for i in range(1, sh.nrows):
				index = sh.cell_value(rowx=i, colx=0)
				tmpdir = encode(sh.cell_value(rowx=i, colx=1))
				sheetname = encode(sh.cell_value(rowx=i, colx=2))
				isrelease = encode(sh.cell_value(rowx=i, colx=3))
				type = sh.cell_value(rowx=i, colx=4)

				if tmpdir != "":
					Missionxls = lib_basedir + tmpdir + "/" + sheetname + ".xls"
				else:
					Missionxls = lib_basedir + sheetname + ".xls"

				#print index, tmpdir, sheetname, isrelease, type
				if index != "" and (tblindex == "" or index == tblindex):
					#保证本次之更新最新的
					#if time.time() - os.stat(Missionxls).st_mtime < 20:
					log("\n" + Missionxls)
					try:
						parse_xls(Missionxls, work_dir, client_output)
						log("\n"+ Missionxls + "导表成功")
					except: 
						error = get_error()
						log("\n"+ Missionxls + "导表失败" + " error: " + error)
						log("\n发生错误: " + error)
						sys.exit(-1)
				
				if tblindex == "" and index != "":
					tmpdetail = get_mission_detail()
					tree_map.update(tmpdetail)

				if index != "" and isrelease == "是":
					update_files = get_xls_missions(Missionxls)
					if type not in output_map.keys():
						output_map[type] = {}
						output_map[type]["missions"] = []
						output_map[type]["release"] = 1
					output_map[type]["missions"] = output_map[type]["missions"] + update_files
				if sheetname not in output_all_missions:
					output_all_missions.append(sheetname)
	except: 
		error = get_error()
		log("\n发生错误: " + error)
		sys.exit(-1)
	preload_content = src_preload % (PythonData2Lpc(output_map, True), PythonData2Lpc(output_all_missions, True))

	sys.path.append(work_dir+ "tools/autocode/")
	PARSE = __import__("TemplateParse")
	PARSE.DoWrite(preload_content, preload_file)

	if len(tree_map):
		tree_content = src_tree % (PythonData2Lpc(tree_map, True))
		PARSE.DoWrite(tree_content, tree_file)
	log("\n")
