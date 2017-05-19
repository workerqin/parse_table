#!/bin/python
#-*- coding: utf-8 -*

#使用条件
# 1、安装 psutil
# 2、mongo c driver 1.6.0 以上

import psutil
import time
import sys
import os
import re


def write_file(logfile, value):
#	cur_file = os.getcwd()
#	file = os.path.join(cur_file, logfile)

	f = open(logfile, "a+")
	f.write(value)
	f.close()

def process_check(pid, argfile):
	if(not psutil.pid_exists(pid)):
		return None;

#	cur_file = os.getcwd()
#	file = os.path.join(cur_file, argfile)
	f = open(argfile, "w")
	f.close()
	return True;

def process_cpu(argv):
	pid = int(argv[0])
	argfile = argv[1]
	interval = int(argv[2])

	if(not process_check(pid, argfile)):
		return

	while True:
		if(not psutil.pid_exists(pid)):
			print("pid is not exist", pid); 
			return;

		tmp=psutil.Process(pid)
		cpu = tmp.cpu_percent(interval)
		#print(cpu)

		value = "%12d %12f\n"%(int(time.time()), cpu)
		write_file(argfile, value)


def process_mem(argv):
	pid = int(argv[0])
	argfile = argv[1]
	interval = int(argv[2])
	if(not process_check(pid, argfile)):
		print("check process failed")
		return
	
	while True:
		if(not psutil.pid_exists(pid)):
			print("pid is not exist", pid); 
			return;

		tmp=psutil.Process(pid)
		mem=tmp.memory_info()
		value="%12d %12d\n"%(int(time.time()), mem.vms)
		write_file(argfile, value)
		time.sleep(interval)
		
def process_dbd(argv):
	pid = int(argv[0])
	argfile = argv[1]
	interval = int(argv[2])
	if(not process_check(pid, argfile)):
		return

	sent=0
	received=0

#	cur_file = os.getcwd()
#	file = os.path.join(cur_file, logfile)

	f = open(argfile, "w")
	value = "mongoc sent received\n"
	f.write(value)
	f.close

	while True:
		if(not psutil.pid_exists(pid)):
			print("pid is not exist", pid); 
			return;

		command="mongoc-stat %d"%pid; 
		retval=os.popen(command).read()

		#print(retval)
		reg=r".*Streams : Egress Bytes             : The number of bytes sent. .*: ([0-9]+).*\n.*Streams : Ingress Bytes            : The number of bytes received.*: ([0-9]+).*"; 
		#reg=r'.*The number of bytes sent.*: ([0-9]+) .*'; 
		matchObj = re.search(reg, retval)
		if matchObj:
			tmpSent=int(matchObj.group(1))
			tmpReceived=int(matchObj.group(2))
			value = "%12d %12d %12d\n"%(int(time.time()),tmpSent-sent, tmpReceived-received)

			write_file(argfile, value)
			sent=tmpSent
			received=tmpReceived

		else:
			print("not match")

		time.sleep(interval)


cmd_table = {
	"mem":{"args":["pid", "logfile", "interval"], "func":process_mem},
	"cpu":{"args":["pid", "logfile", "interval"], "func":process_cpu},
	"dbdio":{"args":["pid", "logfile", "interval"], "func":process_dbd},
}


def usage():
	str = """\
usage:
	python status.py mem pid logfile interval
	python status.py cpu pid logfile interval
	python status.py dbdio pid logfile interval
"""
	print(str)


if __name__ == '__main__':

	if(len(sys.argv) < 3):
		usage()
		sys.exit(1)

	cmd = sys.argv[1]
	if not cmd_table.has_key(cmd):
		print("cmd error")
		usage()
		sys.exit(2)

	if len(sys.argv) != len(cmd_table[cmd]["args"])+2:
		print("cmd args error")
		usage()
		sys.exit(3)
            
	print(sys.argv[2:])
	cmd_table[cmd]["func"](sys.argv[2:])

