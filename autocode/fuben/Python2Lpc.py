# -*- coding: utf-8 -*-

indent_space = '        '
max_indent_cnt = 0


# 计算缩进
def getIndent( indentFlg, indentCnt):
        result = ''
        
        if not indentFlg:
                return result
        
        for i in range( 0, indentCnt):
                result = result + indent_space
                
        return result

# 将python dict 转换为lpc dict
def PythonDict2Lpc( data, indentFlg=False, indentCnt=0):
        print(indentCnt, max_indent_cnt)
        if indentCnt > max_indent_cnt:
                indentFlg = False

                
        result = '{'
        if indentFlg :
                result = result + "\n"
        
        # 遍历 数据
        keys = data.keys()
        
        keys.sort()
        
        for key in keys:
                value = data[key]

                result = result + getIndent(indentFlg, indentCnt+1)

                strKey = (PythonData2Lpc(key,indentFlg, indentCnt+1))
                strValue = (PythonData2Lpc(value,indentFlg, indentCnt+1))
                
                result = result  + ("%s:%s, "%(strKey, strValue))
                if indentFlg:
                        result = result + "\n"
        
        result = result + getIndent(indentFlg, indentCnt) + '}'
        return result

# 将python list 转换为lpc list
def PythonList2Lpc( data, indentFlg=False, indentCnt=0):
	print(indentCnt, max_indent_cnt)
	if indentCnt > max_indent_cnt:
		indentFlg = False

	result = '['

	if indentFlg:
		result = result + "\n"
	# 遍历 数据
	for value in data:
		result = result + getIndent(indentFlg, indentCnt+1) + ("%s, "%(PythonData2Lpc(value,indentFlg, indentCnt+1)))
		if indentFlg:
			result = result + "\n"

	result = result + getIndent(indentFlg, indentCnt) + ']'
	return result


# 将python tuple 转换为lpc tuple
def PythonTuple2Lpc( data, indentFlg=False, indentCnt=0):
        return PythonList2Lpc(data, indentFlg, indentCnt)


def translate( data ):
	if data.startswith(u"R_A_"):
		return data
	if data.startswith(u"I_A_"):
		return data
	if data.startswith(u"I_FWK_"):
		return data
	if data.startswith(u"K_"):
		return data
	if data.startswith(u"CONSUME_METHOD_"):
		return data
	if data.startswith(u"Q_"):
		return data
	if data.startswith(u"@@"):
		return data[2:]
	return '"%s"'%data

# 将python数据转换为lpc数据
def PythonData2Lpc( data, indentFlg=False, indentCnt=0, maxIndentCnt=0):
	if maxIndentCnt > 0:
		global max_indent_cnt
		max_indent_cnt = maxIndentCnt

	if isinstance(data, str):
		return translate(data)
	elif isinstance(data, unicode):
		return translate(data)
	elif isinstance(data, int):
		return "%d"%data
	elif isinstance(data, float):
		return "%f"%data
	elif isinstance(data, list):
		return PythonList2Lpc( data, indentFlg, indentCnt)
	elif isinstance(data, tuple):
		return PythonList2Lpc( data, indentFlg, indentCnt)
	elif isinstance(data, dict):
		return PythonDict2Lpc( data, indentFlg, indentCnt)


if __name__ == "__main__":
        testData = { "a":1, "b":2, "c":3, "d":(1,2,3,4,5,6,), "d":{"a":3232, "b":42343}}
        print( PythonData2Lpc(testData, True, 1, 1))
