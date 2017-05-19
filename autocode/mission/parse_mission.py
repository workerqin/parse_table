#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import xlrd
import shutil
import time

from mission_gen import parse_xls
from mission_gen import get_error

sys.path.append("../")
sys.path.append("tools/autocode")

from Util import PythonData2Lpc 
from Util import PythonData2Lua 

work_dir = ""
log_file = ""
config_svn_path = "https://192.168.0.3/qtz/q1/design/D导表文档/任务/"

#客户端文档输出路径
client_svn_path = "https://192.168.0.3/qtz/q1/design/data/mission/"
svn_user_auth = " --username q1_autoparse_design --password Q1AutoParse"

MISSIONS_OUTPUT = "data/missions"

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
def checkout_file(workdir, svnpath):
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
    print "USAGE:gen_all_mission.py 工作目录 任务标识"
    print "--version : Prints the version number"
    print "--help    : Display this help"

if __name__ == "__main__":
	sys.path.append("../")
	if len(sys.argv) < 2:
		usage()
		sys.exit(1)

	work_dir = (sys.argv[1]).strip()

	missionTags = ""
	if len(sys.argv) == 3:
		missionTags = sys.argv[2].strip() 

	if not work_dir.endswith("/"):
		work_dir = work_dir + "/"

	log_file = work_dir + "log/parse_log.log"

	log("\n开始更新..." )
	print work_dir
	print config_svn_path
	checkout_file(work_dir, config_svn_path)
	checkout_file(work_dir, client_svn_path)

	configDir = work_dir + "tmp/" + os.path.basename(os.path.dirname(config_svn_path)) + "/"
	configFile = configDir + "config.xls" 

	print configDir
	print configFile

	client_output = work_dir + "tmp/" + os.path.basename(os.path.dirname(client_svn_path)) + "/"

	try :
		book = xlrd.open_workbook(configFile)
	except :
		msg = "can't open file %s"%(configFile)
		print(msg)
		usage()
		sys.exit(-1)

	try:
		for x in xrange(book.nsheets):
			sh = book.sheet_by_index(x)
			if sh.name != u"导表索引":
				continue

			for i in range(1, sh.nrows):
				index = sh.cell_value(rowx=i, colx=0)
				if missionTags == "" or missionTags == index:
					# 任务xls的相对路径
					tmpdir = encode(sh.cell_value(rowx=i, colx=1))
					# 任务注释
					msg = encode(sh.cell_value(rowx=i, colx=2))

					if tmpdir != "":
						Missionxls = configDir + tmpdir 
					else:
						log("\n tags:"+ index + ' xls file is null')
						sys.exit(-1)

					try:
						parse_xls(Missionxls, work_dir, client_output)
						log("\n"+ Missionxls + "导表成功")
					except: 
						error = get_error()
						log("\n"+ Missionxls + "导表失败" + " error: " + error)
						log("\n发生错误: " + error)
						sys.exit(-1)

	except: 
		error = get_error()
		log("\n发生错误: " + error)
		sys.exit(-1)
