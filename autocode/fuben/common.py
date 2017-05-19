# -*- coding: utf-8 -*-
import re
import sys
import string

def get_str_from_sheet( sheet, row, col ):
        value = sheet.cell_value(rowx=row, colx=col)

        if  isinstance(value, float):
                tmp = int(value)
                if ( tmp - value < -0.999999 ):
                        tmp = tmp + 1;
                return str(tmp)

        if  isinstance(value, int):
                return str(value)

        return value.strip();

def get_str_array_from_sheet( sheet, row, col ):
	value = get_str_from_sheet( sheet, row, col )
	if ( len(value) == 0):
		return []

	return value.split(",")


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
	
	
#公式分析表达式
pattern = re.compile(r'[%=\+\-\*\/\(\)\ ,\<\>!\?\:]')
#pattern = re.compile(r'[%=＋\+\-\*\/\(\) ,\<\>!]')

#int变float
to_float_pattern = re.compile("(\d{1,9}[.]\d{1,9}|\d{1,9}|[%\+\-\*\/\(\)]|\w|＋|,|\?|\:|\>)")

#过滤全角空格
def filte_space(value):
	return value.replace(u"　", u" ")

#过滤全角逗号
def filte_comma(value):
	return value.replace(u"，", u",")

#过滤全角括号
def filte_parenthesis(value):
	return value.replace(u"（", u"(").replace(u"）", u")")

#过滤全角分号
def filte_semicolon(value):
	return value.replace(u"；", u";")
	
#过滤等号
def filte_equal(value):
	return value.replace(u"＝", u"=")

#过滤加号
def filte_add(value):
	return value.replace(u"＋", u"+")

#过滤加号
def filte_sub(value):
	return value.replace(u"－", u"-")

#过滤乘号
def filte_multi(value):
	return value.replace(u"×", u"*")
	
#过滤百分号
def filte_percent(value):
	return value.replace(u"％", u"%")	

#把中文、全角符号替换成英文符号
def filter(value):
        value = filte_space(value)
        value = value.strip()
        value = filte_parenthesis(value)
        value = filte_comma(value)
        
        value = filte_equal( value )
        value = filte_add(value)
        value = filte_sub(value)
        value = filte_multi(value)
        value = filte_semicolon(value)
        
        value = filte_percent(value)
	return value		

def replace_str(str, pattern, rep_str):
	ret = str
	pos = 0
	index = 0
	pos = ret.find(pattern, index)
	while pos >= 0:
		index = pos + len(pattern)
		ret = ret[0:pos] + rep_str + ret[index:]
		pos = ret.find(pattern, index)
	return ret

def parse_expr_right(rvalue, dicVar, exprnum, paramReplaceDict):
	rvalue_c = rvalue
	temp = pattern.split(rvalue)
	#src = rvalue
	paramDeclare = ''

	index = 0
	
	#print("---------3----------")
	#print(chinese_encode(temp))
	#print("----------3---------")
	for param in temp:
		param = param.strip()
		
		if param in paramReplaceDict:
			continue

		if param == None or param == "pow" or param == "random" or param == "to_int" or param == "":
			continue
		try:
			if isinstance(float(param), float):
				continue
		except:
			pass

		if param in dicVar:
			tmpIndex = rvalue.find(param, index)
			if tmpIndex >= 0:
				if tmpIndex == 0:
					head = ''
				else:
					head = paramDeclare[0:tmpIndex]
				index = tmpIndex + len(param)
				var_name = dicVar[param]["var_name"]
			        get_func = dicVar[param]["get_func"]
				var_desc = dicVar[param]["var_desc"]
				
				if var_name:
                                        
        				paramDeclare += u"\t// %s\n" % var_desc
        				paramDeclare += u"\tmixed %s = %s;\n" % (var_name, get_func)
        				paramReplaceDict[param] = var_name
        			else:
        			        paramReplaceDict[param] = get_func
        			
		else:
			print(param)
			print(u"%s not in var dict!" % param)
			pass
	
	for k, v in sorted(paramReplaceDict.items(), key=lambda t: len(t[0]),reverse=True):
		#print("===== %s %s"%(chinese_encode(k), chinese_encode(v)))
		rvalue_c = replace_str(rvalue_c, k, v)
	
	#print("---------1----------")
	#print(chinese_encode(src))
	#print("----------1---------")
	return (paramDeclare, rvalue_c, paramReplaceDict)

def parse_expr_left(lvalue, rvalue, dicVar, exprnum, expr):
	src = ''
	lvalue = lvalue.strip()
	if len(dicVar[lvalue]["set_func"]) == 0:
		print("ERROR! lvalue[%s] is can not set , please check var dict!"%lvalue.encode('utf-8'))
		assert 1==0
		
	if lvalue in dicVar:
		var_name = dicVar[lvalue]["var_name"]
		set_func = dicVar[lvalue]["set_func"]
		var_desc = dicVar[lvalue]["var_desc"]
		src += u"\t// 公式原文:%s\n" % expr 
		
		src += u"\t%s;\n" % set_func
		src = replace_str(src, "$(value)", rvalue)
	else:
		print("ERROR! lvalue[%s] is not in var dict!"%lvalue.encode('utf-8'))
	return src

def parse_word( word, dicVar, indent, dicParam ):
	rule = re.compile(r'\$\(.*?\)', re.S)

	data = '"%s"'%word
	params = rule.findall(data)

	strDeclare = ""

	for i in params:
		exp = parse_expr_right(i[2:-1], dicVar, indent, dicParam )
		exp = exp or ("", "", dicParam) 

		strDeclare += exp[0]

		data = data.replace( i, '" + (%s) + "'%(exp[1]), 1)


	return [strDeclare, data]

def parse_value( word, dicVar, indent, dicParam ):
	rule = re.compile(r'\$\(.*?\)$', re.S)

	data = '%s'%word
	params = rule.findall(data)

	strDeclare = ""

	if( len(params)):
		print("ERROR:parse_value cnt > 1")

	for i in params:
		exp = parse_expr_right(i[2:-1], dicVar, indent, dicParam )
		exp = exp or ("", "", dicParam) 

		strDeclare += exp[0]

		data = exp[1]

	return [strDeclare, data]
	

exprSplit = re.compile(u'[;；]')
lrSplit = re.compile(u'[=＝]{1}')


def parse_function( data, note, fname, dicVar, funcTemplete ):
	data = filter(data)
	# 分割表达式
	exprs = exprSplit.split(data)
	
	srcFormla = ''
	srcDeclare = ''
	i = 1
	paramReplaceDict = {}
	
	for expr in exprs:
		#print(i)
		if len(expr) == 0:
			continue
		# 分割该表达式的左右值
		eqCharIdx = expr.find(u"=")
		#print( "eqCharIdx:",eqCharIdx )
		lr = lrSplit.split(expr)
		#print(expr, eqCharIdx)
		if eqCharIdx != -1:
			lvalue = expr[0 : eqCharIdx]
			rvalue = expr[eqCharIdx + 1 : ] 
			
			r_result = parse_expr_right(rvalue, dicVar, i, paramReplaceDict)
			l_result = parse_expr_left(lvalue, r_result[1], dicVar, i, expr)
			srcFormla += l_result
                        
                        srcDeclare += r_result[0]
                        
			#print(chinese_encode(l_result))
		else:
			r_result = parse_expr_right(expr, dicVar, i, paramReplaceDict)
			#print("ERROR! var function type request '='! \n %s"%chinese_encode(data))
			#print(lr)
			srcFormla += r_result[1]
		i += 1

        src = srcDeclare + u'\n' + srcFormla
	# TODO:重构函数名 
	src = funcTemplete % (note, fname, src)

	#print(chinese_encode(src))
	return src

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

def upFirstChar( s ):
	return s[0].upper() + s[1:]

if __name__ == "__main__":
	pass
