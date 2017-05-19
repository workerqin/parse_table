#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import xlrd
import shutil
import re

logfile = ""
work_dir = ""
config_file = "config/导表数据/config.xls"
#svn_root_path = "https://192.168.0.3/qtz/mg01/config/config_release_aboard_trunk/"
#svn_config_path = svn_root_path + config_file
svn_root_path = "https://192.168.0.3/qtz/mg01/config/config_release_RELEASE_DATE/"
svn_config_path = None #svn_root_path + config_file
svn_tmp_path = "tmp/"
#svn_user_auth = " --username dhh_parser --password DhhParser! --no-auth-cache"
svn_user_auth = " --username dhh_parser --password DhhParser!"


def encode(str):
	import locale		
	encoding = locale.getdefaultlocale()[1]
	res = str.encode(encoding)
	return res

def cmd(str):
	print(str);
	os.system(str)

#返回目标路径
def export_svn_file(svn_xls_file):

	#切换到tmp目录
	os.chdir(work_dir + svn_tmp_path)
	cmd("mkdir -p " + work_dir + svn_tmp_path)

	export_svn_dir = os.path.dirname(svn_root_path + svn_xls_file)
	export_dir = os.path.basename(os.path.dirname(svn_xls_file))
	export_file = work_dir + svn_tmp_path + export_dir + "/" + os.path.basename(svn_xls_file)

	#删除再co
	if os.path.isdir(export_dir) and os.path.isfile(export_file):
		#os.rmdir(work_dir + svn_tmp_path + export_dir)
		#os.system("rm -rf " + export_dir)
		tmp_cmd = "svn co " + export_svn_dir + svn_user_auth
		cmd(tmp_cmd);
		return export_file

	#否则删除
	cmdStr = "rm -rf " + export_dir
	cmd(cmdStr)

	cmdStr = "svn co " + export_svn_dir + " " + export_dir + svn_user_auth
	cmd(cmdStr)

	if not os.path.isfile(export_file):
		logfile.write("不存在文件[" + export_file + "]\n");
		return ""
	return export_file

def export_config_file(svn_config_file):
	p = work_dir + svn_tmp_path
	if not os.path.exists(p):
		os.makedirs(p)
	#切换到tmp目录
	os.chdir(p)

	export_svn_dir = os.path.dirname(svn_config_file)
	export_file = os.path.basename(svn_config_file)
	export_dir = os.path.basename(os.path.dirname(svn_config_file))

	if not os.path.isdir(export_dir):
		os.system( "svn co " + export_svn_dir + " " + export_dir + svn_user_auth)
	else:
		os.system( "svn up " + export_dir + svn_user_auth)

def parse_conf_sheet(sh, parsetable):
	#第一行不解析，作为标题
	for i in range(1, sh.nrows):
		parse_name = sh.cell_value(rowx=i, colx=0)
		parse_file = encode(sh.cell_value(rowx=i,colx=1))
		parse_sheet = encode(sh.cell_value(rowx=i,colx=2))
		parse_tool = encode(sh.cell_value(rowx=i, colx=3))
		parse_output = encode(sh.cell_value(rowx=i, colx=4))


		if parse_name == None or parse_name == "":
			continue
		parse_name = str(parse_name)
		if len(parse_file) == 0:
			continue
		if len(parse_tool) == 0:
			continue
		if len(parse_output) == 0:
			parse_output = ""
		if parse_sheet == None or len(parse_sheet) == 0:
			parse_sheet = ""
		if parse_name not in parsetable.keys():
			parsetable[parse_name] = []
		parse_item = { "parse_file":parse_file, "parse_sheet": parse_sheet, "parse_tool":parse_tool, "parse_output":parse_output }
		parsetable[parse_name].append(parse_item)
	return parsetable

# 将一个配置文件转成一个dict
def read_conf(parse_xls):
	if not os.path.isfile(parse_xls):
		logfile.write( "没有配置文件 " + parse_xls + "\n" )
		return {}
	book = xlrd.open_workbook(parse_xls)
	parse_conf_table = {}
	#读取xls获取索引表
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		print( book.nsheets, x, sh.name );
		if sh.name == u"说明":
			continue
		if sh.name == u"配置":
			continue
		parse_conf_sheet(sh, parse_conf_table)
	
	return parse_conf_table 

def write_file(filename, content ):
	msg = "writting to file " + filename
	logfile.write( msg + "\n" )
	try :
		f = file(filename, "w+b")
	except :
		msg = "can not write to " + filename + "\n"
		logfile.write( msg )
		sys.exit(-1)
	f.write(content)
	f.close()

def add_to_file(filename, content ):
	try :
		f = file(filename, "a+b")
	except :
		sys.exit(-1)
	f.write(content)
	f.close()
	
	
#执行导标命令
def do_parse_xls(parse_table):

	print( "begin do_parse_xls" );
	parse_file = export_svn_file(parse_table["parse_file"])
	print( parse_file );
	if not parse_file:
		logfile.write("不能获取对应的文件: " + parse_table["parse_file"] + "\n")
		raise
		#sys.exit(-1)

	parse_tool_path = work_dir + parse_table["parse_tool"]
	parse_tool_path = parse_tool_path.strip()
	parse_output_path = parse_table["parse_output"]
	parse_sheet = parse_table["parse_sheet"]

	tool_dir = work_dir + "tools/autocode/"
	if not os.path.isdir(tool_dir):
		print "not dir" + tool_dir
		raise
		#sys.exit(-1)
	sys.path.append(tool_dir)
	sys.path.append(work_dir)
	os.chdir(work_dir)

	if parse_tool_path.endswith( ".py" ):
		parse_cmd = "python " + parse_tool_path + " " + work_dir + " " + parse_file + " " + parse_sheet + " " + parse_output_path + " >> " + logfilename
	else:
		parse_cmd = parse_tool_path + " " + work_dir + parse_file + " " + parse_sheet + " " + parse_output_path + " >> " + logfilename

	logfile.write("执行命令 : " +  parse_cmd + "\n")

	if os.system(parse_cmd):
		raise
	#os.popen(parse_cmd)

def do_parse_tbl_item(table_item):
	if not len(table_item["parse_output"]):
		table_item["parse_output"] = ""
		#获得需要解析的对应项的信息
	try : 
		do_parse_xls(table_item)
		if os.path.isfile(work_dir + table_item["parse_output"]):
			add_to_file(updatefile, table_item["parse_output"] + "\n")
		elif os.path.isdir(work_dir + table_item["parse_output"]):
			svn_st_file = work_dir + "tmp/svnst.txt"
			os.chdir(work_dir)

			if os.path.exists(".git"):
			    parse_cmd = "git status %s |grep modified > %s" % (table_item["parse_output"], svn_st_file)
			else:
			    parse_cmd = "svn status " + table_item["parse_output"] + svn_user_auth + " > " + svn_st_file

			os.system(parse_cmd)
			tmpfile = open(svn_st_file, "rb")
			file_content = tmpfile.readlines()
			if len(file_content):
				for filestr in file_content:
					if filestr.find('char') > 0:
						index = filestr.find('char')
						ret = filestr[index:len(filestr)]
						add_to_file(updatefile, ret)
	except :
		logfile.write(table_item["parse_output"] + "导表失败\n" );
		return 0
	return 1

br_pt = re.compile(r'.* tencent/([\d\.]+)\n')
def check_parse_branch_env():
	logic_dir = os.path.realpath(os.path.dirname((sys.argv[0]))) + '/..'
	cmd = 'cd %s && git status' % logic_dir
	out = os.popen(cmd).readline()
	arr = br_pt.findall(out)
	if len(arr) != 1:
		print 'no logic_dir or logic_dir it not under git control'
		sys.exit(-1)
	print 'logic branch: %s' % out
	rd = arr[0].replace('.', '_')
	global svn_root_path, svn_config_path
	svn_root_path = svn_root_path.replace('RELEASE_DATE', rd)
	svn_config_path = svn_root_path + config_file

	parse_config_dir = '%s/%s/%s' % (logic_dir, svn_tmp_path, '导表数据')
	cmd = 'svn info %s' % parse_config_dir
	out = os.popen(cmd)
	out.readline()  # skip the first line
	line2 = out.readline()  # URL: https://192.168.0.3/qtz/mg01/config/config_release_2017_05_08/xxxxxx
	print 'parse table: %s' % line2
	if line2.find(rd) < 0: # 跟当前代码分支不一致
		print '@@==导表分支跟当前代码分支不一致, 将删除tmp目录==@@\n'
		os.system('rm -rf  %s/%s' % (logic_dir, svn_tmp_path))

if __name__ == "__main__":
	check_parse_branch_env()
	
	if len(sys.argv) < 3:
		print 'usage: python logic_root_dir index'
		sys.exit(1)

	work_dir = os.path.abspath((sys.argv[1]).strip())

	parse_str = (sys.argv[2]).strip() #现在改为index

	logfilename = work_dir + "/log/parse_log.log"
	updatefile = work_dir + "/tmp/update_file.txt"
	logfile = open( logfilename, "a" )
	logfile.write( "开始导表过程\n" );

	if not os.path.isdir( work_dir ):
		logfile.write("工作目录不存在: " + work_dir + "\n");
		sys.exit(-1)

	if not work_dir.endswith("/"):
		work_dir = work_dir + "/"

	export_config_file(svn_config_path)

	parse_xls = work_dir + svn_tmp_path + "导表数据/config.xls"

	conftable = read_conf(parse_xls)
	if not len(conftable):
		logfile.write("获取配置文件表失败: " + parse_xls + "\n")
		sys.exit(-1)

	if len(parse_str):
		if not conftable.has_key(parse_str):
			logfile.write("没有对应的表项 : " + parse_str + "\n")
			sys.exit(-1)
		for table_item  in conftable[parse_str]:
			ret = do_parse_tbl_item(table_item)
			if not ret:
				break
	else:
		ret = 1
		for parse_str in conftable.keys():
			for table_item  in conftable[parse_str]:
				ret = do_parse_tbl_item(table_item)
				#if not ret:
				#	break
			#if not ret:
			#	break
	logfile.write( "导表过程结束\n" );
	logfile.close()

