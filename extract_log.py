# -*- coding: utf-8 -*-

import os
import sys
import getopt
import xlrd
import json
import datetime
import re


version = u"1.00"

#logDir = "/Users/chenjun/mg01/q3_run355/logic/log"
logDir = "/home/qtz_qin/dhh/q3_run455/logic/log"
outputDir = "./"

def usage():
    print u'python extract_log.py root_path excel_file output_dir'

def get_str_from_sheet( sheet, row, col ):
	value = sheet.cell_value(rowx=row, colx=col)
	
	if  isinstance(value, float):
		return str(int(value))
	
	if  isinstance(value, int):
		return str(value)

	value = value.encode(u"utf-8")
	return value	


#抽取信息
extract_info = {}

def getHourByTimestamp( ts ):
	return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H')

def getTimeByTimestamp( ts ):
	return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def parse_total( sheet ):
	total_info = []
	for i in range(1, sheet.nrows):
		index = get_str_from_sheet( sheet, i, 0 )
		if len(index) == 0:
			continue;
		logFile = get_str_from_sheet( sheet, i, 1 )
		if len(logFile) == 0:
			continue;
		logType = get_str_from_sheet( sheet, i, 2 )
		if len(logType) == 0:
			continue;
		totalField = get_str_from_sheet( sheet, i, 3 )	
		if len(totalField) == 0:
			continue;
		outputFile = get_str_from_sheet( sheet, i, 4 )
		if len(outputFile) == 0:
			continue;
		condition = get_str_from_sheet( sheet, i, 5 )
		#print("condition = %s"%condition)

		total_info.append({
				u"index" : index,
				u"logFile" : logFile,
				u"logType" : logType,
				u"totalField" : totalField,
				u"outputFile" : outputFile,
				u"condition" : condition,
			})

	extract_info[u"total"] = total_info 

def parse_extract( sheet ):
	extract = []
	for i in range(1, sheet.nrows):
		index = get_str_from_sheet( sheet, i, 0 )
		if len(index) == 0:
			continue;
		logFile = get_str_from_sheet( sheet, i, 1 )
		if len(logFile) == 0:
			continue;
		logType = get_str_from_sheet( sheet, i, 2 )
		if len(logType) == 0:
			continue;
		extractField = get_str_from_sheet( sheet, i, 3 )	
		if len(extractField) == 0:
			continue;
		outputField = get_str_from_sheet( sheet, i, 4 )	
		outputFile = get_str_from_sheet( sheet, i, 5 )
		if len(outputFile) == 0:
			continue;
		condition = get_str_from_sheet( sheet, i, 6 )

		extract.append({
				u"index" : index,
				u"logFile" : logFile,
				u"logType" : logType,
				u"extractField" : extractField,
				u"outputField" : outputField,
				u"outputFile" : outputFile,
				u"condition" : condition,
			})

	extract_info[u"extract"] = extract 


def append_record( outputFile, outputData ):
	#print("append_record", outputData )
	outputStr = ",".join(map(str,outputData))
	outputStr = outputStr + "\n"

	outputFile.writelines( [outputStr,] )

	
reCon = re.compile(r'(?P<field_name>.*)(?P<relationship>(\=\=|\>\=|\<\=|\!\=|\>|\<))(?P<value>.*)');

def judge_condition( cond, jsonObj ):
	m = reCon.match( cond )

	rs = m.group("relationship").strip()
	fn = m.group("field_name").strip()
	va = m.group("value").strip()
	if va.find('"') >= 0:
		va = va.replace('"', '')
	else:
		va = int(va)

	if fn == "time":
		jsonData = jsonObj["time"]
	else:
		jsonData = jsonObj["data"][fn]

	if rs == "==":
		return jsonData == va

	if rs == ">=":
		return jsonData >= va

	if rs == "<=":
		return jsonData <= va

	if rs == "!=":
		return jsonData != va

	if rs == ">":
		return jsonData > va

	if rs == "<":
		return jsonData < va

	raise("ERROR: unkone relationship")

def check_condition( jsonObj, dealInfo ):
	#print( "xxxxxx:", dealInfo )
	if "condition" not in dealInfo:
		return True
	condition = dealInfo["condition"]
	if len(condition) == 0:
		return True

	#解析执行条件
	#条件基本格式
	# fieldStr=="1111";fieldInt>=100;fieldInt<=150
	lstCon = condition.split(u";")

	for singleCon in lstCon:
		# 有一个条件错误返回False
		if not judge_condition( singleCon, jsonObj ):
			#print("return false", singleCon, jsonObj)
			return False
		#print("check_condition", singleCon, jsonObj)

	return True

def genrate_total_output_data( jsonObj, dealInfo, totalTable, lastHour  ):
	dealIndex = dealInfo["index"]
	totalField = dealInfo["totalField"]

	# 计入总计	
	curValue = totalTable[dealIndex]["value"]

	outputData = (lastHour, curValue)

	return outputData

def genrate_extract_output_data( jsonObj, dealInfo, totalTable ):
	dealIndex = dealInfo["index"]
	extraceField = dealInfo["extractField"]

	timeStr = getTimeByTimestamp(jsonObj["time"])

	outputData = [timeStr,]

	lstField = extraceField.split(',')

	for field in lstField:
		if field not in jsonObj["data"]:
			outputData.append("")
			continue
		outputData.append( jsonObj["data"][field] )


	return outputData

def deal_total_value( totalField, dealIndex, jsonObj, totalTable ):
	if not totalField.startswith("__"):
		totalTable[dealIndex]["value"] = totalTable[dealIndex]["value"] + jsonObj["data"][totalField]
		return

	if totalField == "__count":
		totalTable[dealIndex]["value"] = totalTable[dealIndex]["value"] + 1
		return
	
	raise("ERROR:unkown totalField type");

def deal_log( jsonObj, dealInfo, totalTable, curHour):
	dealType = dealInfo["type"]
	dealIndex = dealInfo["index"]
	outputFile = outputDir + "/" + dealInfo["outputFile"]

	# 初始化文件
	if dealIndex not in totalTable:
		totalTable[dealIndex] = {}
	
	# 判断是否total，
	if dealType == u"total":
		totalField = dealInfo["totalField"]

		if "output_file" not in totalTable[dealIndex]:
			totalTable[dealIndex]["output_file"] = open( outputFile, "a" )

		# check condition
		# 条件不达成，直接return 
		if not check_condition( jsonObj, dealInfo ):
			return;

		# 做好total

		if "value" not in totalTable[dealIndex]:
			totalTable[dealIndex]["value"] = 0

		if "lastHour" not in totalTable[dealIndex]:
			totalTable[dealIndex]["lastHour"] = ""

		lastHour = totalTable[dealIndex]["lastHour"]

		# 根据时间改变做处理
		if (lastHour != curHour):
			# 将对应的统计数据计入输出文件，同时将对应的total清0

			# 生成结算放入文件数据
			outputData = genrate_total_output_data(jsonObj, dealInfo, totalTable, lastHour )

			# 放弃lastHour为空的记录
			if (lastHour != ""):
				# 追加一行记录到outputFile
				append_record( totalTable[dealIndex]["output_file"], outputData )

			#print("to reset value:", totalField, totalTable[dealIndex]["value"])
			# 将value设置为初始值
			totalTable[dealIndex]["value"] = 0
			#totalTable[dealIndex]["value"] = totalTable[dealIndex]["value"] + jsonObj["data"][totalField] 
			deal_total_value( totalField, dealIndex, jsonObj, totalTable )
			totalTable[dealIndex]["lastHour"] = curHour
		else:
			#print("to add value:", totalField, totalTable[dealIndex]["value"])
			#totalTable[dealIndex]["value"] = totalTable[dealIndex]["value"] + jsonObj["data"][totalField]
			deal_total_value( totalField, dealIndex, jsonObj, totalTable )

		return

	# 抽取操作
	extraceField = dealInfo["extractField"]
	outputField = dealInfo["outputField"]
	if len(outputField) == 0:
		outputField = extraceField

	# 判断目标文件是否存在，不存在，插入一行head
	#print("to output ", outputFile, os.path.exists(outputFile))
	if not os.path.exists(outputFile):	
		totalTable[dealIndex]["output_file"] = open( outputFile, "a" )
		append_record( totalTable[dealIndex]["output_file"], [u"time"] + outputField.split(","))
	else:
		totalTable[dealIndex]["output_file"] = open( outputFile, "a" )


	# 
	# check condition
	# 条件不达成，直接return 
	if not check_condition( jsonObj, dealInfo ):
		return;

	# 抽取操作
	#print("to extract", jsonObj)
	outputData = genrate_extract_output_data( jsonObj, dealInfo, totalTable )
	#print(dealIndex, totalTable[dealIndex])
	append_record( totalTable[dealIndex]["output_file"], outputData )


def parse_xls(filename ):
	global error_tbl
	try :
		# 读取excel
		book = xlrd.open_workbook(filename)
	except :
		msg = u"can't open file?", filename
		usage()
		sys.exit(-1)

	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		if sh.name == u"汇总":
			parse_total(sh)
			continue;
		if sh.name == u"抽取":
			parse_extract(sh)
			continue;
	
	# 整理extract_info
	# 按logFile来分，防止重复读取logFile
	logExtraceData = {}

	totalInfo = extract_info[u"total"];

	for total in totalInfo:
		logFile = total["logFile"];
		if (logFile not in logExtraceData):
			logExtraceData[logFile] = {}

		logType = total["logType"];
		if (logType not in logExtraceData[logFile]):
			logExtraceData[logFile][logType] = []

		info = logExtraceData[logFile][logType]

		info.append( {
				"type":"total",
				"index":total["index"],
				"totalField":total["totalField"],
				"outputFile":total["outputFile"],
				"condition":total["condition"],
			} )
	
	extrace = extract_info[u"extract"]
	for data in extrace:
		logFile = data["logFile"];
		if (logFile not in logExtraceData):
			logExtraceData[logFile] = {}

		logType = data["logType"];
		if (logType not in logExtraceData[logFile]):
			logExtraceData[logFile][logType] = []

		info = logExtraceData[logFile][logType]

		info.append( {
				"type":"extract",
				"index":data["index"],
				"extractField":data["extractField"],
				"outputField":data["outputField"],
				"outputFile":data["outputFile"],
				"condition":data["condition"],
			} )

	#print logExtraceData
	for logFile in logExtraceData:
		logDeal = logExtraceData[logFile]
		# 按行读取logFile
		try:
			f = open(logDir + "/" + logFile, "r") 
		except IOError:
			continue;

		totalTable = {}

		line = f.readline()


		#print logDeal
		while line:
			#print( line )
			#try:
			if True:
				jsonData = json.loads( line ) 
				
				logType = jsonData[u'type']

				#print logType
				# 判断log是否需要处理
				if logType not in logDeal:
					line = f.readline()
					continue

				info = logDeal[logType]

				# 根据time判断是否更换小时
				logTime = jsonData[u'time']

				curHour = getHourByTimestamp( logTime ) 

				for toDealInfo in info:
					#print(curHour, line)
					# 抽取json数据
					deal_log( jsonData, toDealInfo, totalTable, curHour )
					

				# read next line
				line = f.readline()
					
			#except :
			#	print(u"ERROR:[%s] cann't parse to json"%(line))
			#	sys.exit(-99)

		
		# :补齐最后一小时log的total处理
		#deal_log( jsonData, toDealInfo, totalTable, "" )
		for index in totalTable:
			tmpData = totalTable[index]

			if "value" in tmpData:
				append_record( tmpData["output_file"], (tmpData["lastHour"], tmpData["value"]) )

			if "output_file" in tmpData:
				tmpData["output_file"].close()

		# 根据tatalTable处理下
		# totalTable[index]

		f.close();

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", ])
		for o, a in opts:
			if o == "-v":
				print version
				sys.exit()
			elif o in ("-h", "--help"):
				usage()
				sys.exit()
			else:
				assert False, "unhandled option"

		if (len(args) < 3):
			usage()
			sys.exit(-1)
		
		rootPath = args[0]
		execelFile = args[1]
		global outputDir
		outputDir = rootPath + "/" + args[2]
		os.system("rm -r " + outputDir)
		os.system("mkdir -p " + outputDir)
		print rootPath, execelFile 

		#解析xls文件，获得需要汇总和抽取的结构
		parse_xls(execelFile)

	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		raise
		#sys.exit(2)

if __name__ == "__main__":
	main()
