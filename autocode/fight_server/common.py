# -*- coding: utf-8 -*-
import re
import sys
import string

def get_str_from_sheet( sheet, row, col ):
	value = sheet.cell_value(rowx=row, colx=col)
	if isinstance(value, float):
		tmp = int(value)
		if (tmp - value < -0.999999):
			tmp = tmp + 1;
		return str(tmp)
	if isinstance(value, int):
		return str(value)

	return value.strip();

def get_str_array_from_sheet( sheet, row, col ):
	value = get_str_from_sheet( sheet, row, col )
	if ( len(value) == 0):
		return []

	return value.split(",")

def get_int_array_from_sheet( sheet, row, col ):
	value = get_str_from_sheet( sheet, row, col )
	if ( len(value) == 0):
		return []

	list = value.split(",")
	tmp = []
	for i in list:
		tmp.append( int(i) )
	return tmp

def get_int_from_sheet( sheet, row, col ):
	value = sheet.cell_value(rowx=row, colx=col)

	if  isinstance(value, float):
		tmp = int(value)
		if ( tmp - value < -0.999999 ):
			tmp = tmp + 1;
		return tmp

	if  isinstance(value, int):
		return value

	value = value.strip()
	if  value == '':
		return 0

	if  isinstance(value, basestring):
		return string.atoi(value)

	return value

headExp = re.compile(r"(?P<var_name>\w+)\((?P<var_type>\w+)\)")

# 从sh的curLine,startCol读出一个Table，同时
# 移动curLine,
# 头两行为Head
# 第一列为key
def parse_table( sh, curLine, startCol ):
	tb = {}
	row = curLine + 2
	head = get_str_from_sheet( sh, row, startCol )
	while len(head) > 0:
		keyNameType = get_str_from_sheet( sh, curLine+1, startCol)
		tmp = headExp.match( keyNameType )
		var_name = tmp.group("var_name")
		var_type = tmp.group("var_type")

		if var_type == "int":
			key = get_int_from_sheet( sh, row, startCol)
		else:
			key = get_str_from_sheet( sh, row, startCol)

		curData = {}
		
		for col in xrange( startCol + 1, sh.ncols):
			nameType = get_str_from_sheet( sh, curLine+1, col)
			print(nameType)
			if len(nameType) == 0:
				continue
			tmp = headExp.match( nameType )
			var_name = tmp.group("var_name")
			var_type = tmp.group("var_type")

			if var_type == "int":
				value = get_int_from_sheet( sh, row, col)
			elif var_type == "str_array":
				value = get_str_array_from_sheet( sh, row, col)
			elif var_type == "int_array":
				value = get_int_array_from_sheet( sh, row, col)
			elif var_type == "mapping":
				tmp = get_str_from_sheet( sh, row, col)
				value = eval("{%s}"%tmp)
			else:
				value = get_str_from_sheet( sh, row, col)

			if ( value != 0) and ( value != ""):
				curData[var_name] = value

		print( curData )
		tb[key] = curData


		row = row + 1
		if row >= sh.nrows:
			break
		head = get_str_from_sheet( sh, row, startCol )

	return tb, row

def write_file(filename, content ):

	msg = "writing file %s" %(filename)
	#print msg

	try :
		f = file(filename, "w+b")
	except :
		msg = "\rcan not write to " + filename
		print msg
		raise()
		#sys.exit(-1)
	#print "\r write file %s success"%(filename)
	f.write(content)
	f.close()
	
def write_src(src_file, begin, end, src, encode):
	p = re.compile(begin + r".*?" + end, re.S | re.M)
	try:
		oldSrc = open(src_file, "rb").read().decode("utf-8")
		
		if len(oldSrc) == 0:
			oldSrc = begin + u"\n\n" + end
	except IOError:
		oldSrc = begin + u"\n\n" + end

	src = p.sub(begin + u"\n" + src + u"\n" + end, oldSrc)

	#print src
	write_file(src_file, src.encode(encode))
