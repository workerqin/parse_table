#-*- coding:utf-8 -*-

import sys
import os
import codecs


DEFINE_HEAD = u"#define"

info = {}

begin = u"//----------------------- Auto Genrate Begin --------------------\n"
end = u"//----------------------- Auto Genrate End   --------------------\n"
ifndef = u"#ifndef __IDIP_TOOL_H__\n"
define = u"#define __IDIP_TOOL_H__\n"
endif = u"#endif\n"

def write_file(filename):
	try :
		f = file(filename, "w+b")
	except :
		msg = "\rcan not write to " + filename
		print msg 
		raise()
	 #sys.exit(-1)
	 #print "\r write file %s success"%(filename)
	f.write(ifndef + "\n")
	f.write(define + "\n")
	#f.write(begin + "\n")

	#导请求串和返回串对应的cmdid
	for data in info.items():
		key = data[0][2:-3]
		value = data[1]
		idip = value["idip"]
		cmd = value["cmd"]
		f.write("//" + key + "\n")
		i = 0
		for id in cmd:
			f.write(DEFINE_HEAD + " " + id + " " + "(" + idip[i] + ")" + "\n")
			i += 1
	f.write("\n")
	
	f.write("mapping ReqCmd2ResCmd = { \n")
	#导请求串的cmdid对应返回串的cmdid
	for data in info.items():
		key = data[0][2:-3]
		value = data[1]
		idip = value["idip"]
		cmd = value["cmd"]
		f.write("//" + key + "\n")
		f.write(cmd[0] + ":" + cmd[1] + "," + "\n")
	f.write("}\n")

	f.write("\n")
	f.write(endif + "\n")
	#f.write(end + "\n")

	f.close()
			

def handle_txt(filename, outfilename):
	f = open(filename, "r")
	allKey = {}
	block = []
	i = 1
	allBlock = {}

	#对文件分块
	for line in f.readlines():
		if line != "======================================================================\n":
			block.append(line)
		elif block:
			allBlock[i] = block
			i += 1
			block = []
	allBlock[i] = block
	
	#去除第一个没用的块
	for i in allBlock.items():
		if i[1][1].find("cmd") != 1:
			allBlock.pop(i[0])
	
	for i in allBlock.values():
		allIdipInfo = []
		allCmdInfo = []
		#取出说明文字
		note = i[0]
		for str in i:
			str = str.strip()
			cmdidx = str.find("Cmdid")
			#找出cmdid
			if cmdidx >= 0:
				idx1 = str.find(":")
				idx2 = str.find(",")
				allIdipInfo.append(str[idx1+1:idx2].strip())
				#allIdipInfo.append(str[10:14])

			idipidx = str.find("IDIP")
			#找出请求宏
			if idipidx >= 0 :
				#print str[idx:]
				allCmdInfo.append(str[idipidx:])

		oneinfo = {}
		oneinfo["idip"] = allIdipInfo
		oneinfo["cmd"] = allCmdInfo
		info[note] = oneinfo

	write_file(outfilename)
		

def iconv_txt(filename):
	cmd = "iconv -f GBK -t UTF-8 %s > %s" % (filename, filename+"_bak") 
	os.system(cmd)

def remove_bak_txt(filename):
	cmd = "rm %s"%filename
	os.system(cmd)

USAGE = "usage: python idip.py path input_file output_file"

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print USAGE 
		sys.exit(1)

	filename = sys.argv[2]
	outfilename = sys.argv[3]
	print filename, outfilename

	iconv_txt(filename)
	handle_txt(filename+"_bak", outfilename)
	remove_bak_txt(filename+"_bak")
