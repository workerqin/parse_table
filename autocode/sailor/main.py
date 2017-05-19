# -*- coding:utf-8 -*-

import sys
import os
import glob
import getopt
import re
import xlrd
import string
from common import get_str_from_sheet
from common import get_int_from_sheet
from common import write_file
from common import parse_function
from common import replace_str
from common import filter
from common import parse_map
from Python2Lpc import PythonData2Lpc
from common import write_src
from Python2Lpc import PythonDict2Lpc

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

# 变量表
dicVar = {}

srcSailorTemplete = u'''

#include <user_key.h>
#include <sailor.h>
inherit SAILOR_BASE;
#include <var_prop.h>
#include <boat.h>
//注：基础xx资质、洗练xx资质、升星xx、升级xx资质都是一个变量的不同表达方式
//	  基础xx资质上限、洗练xx资质上限、升星xx资质上限都是一个变量的不同表达方式
//	  基础xx、洗练xx、升星xx、升级xx都是一个变量的不同表达方式

// -----------------------------------------
// 属性区
// -----------------------------------------
%s
// -----------------------------------------

// -----------------------------------------
// 函数区域
// -----------------------------------------

%s
//水手投资获得经验
int GetSailorInvestExp(int oUser,int sailorId)
{
	int investExp = 0;
	int lv = oUser->GetSailorLv(sailorId);
	int quality = oUser->GetSailorQuality(sailorId);
	int star = oUser->GetSailorStar(sailorId);

	%s

	return investExp;
}

//获得雷达上限
mapping* GetRadarValue(object oUser, int sailorId, int lv, int quality, int star)
{
	mapping* radarValue = [];
	//资质雷达上限值
	mapping aptitudeRadarVertex = {};
	//属性雷达上限值
	mapping attrRadarVertex = {};

	%s
	radarValue += [aptitudeRadarVertex];
	radarValue += [attrRadarVertex];
	return radarValue;
}

//水手资质范围值
float GetBaseAttrAptitude()
{
	mixed* region = GetRegion();
	int totalRan = 0;
	foreach(mixed arr in region){
		totalRan += arr[0];
	}   
	int randomNum = random(totalRan+1);
	int max = 0;
	int min = 0;
	for(int i=0; i<sizeof(region); i++){
		if(randomNum <= region[i][0]){
			min = region[i][1];   
			max = region[i][2];   
			break;
		}   
		randomNum -= region[i][0];
	}
	return random_between(min, max)/100.0;
}

//水手出生属性
mapping* GetSailorBaseAttrs(object oUser, mapping aptRangeValue, int lv, int quality, int star )
{
	mapping* baseAttrRange = [];
	//属性值
	mapping baseAttrs = {};
	//资质值
	mapping baseRange = {};
	//资质上限值
	mapping maxRange = {};
	//资质范围值
	mapping aptitudeRange = {};

	//初始化资质范围值(0.3)
	aptitudeRange[MELEE_RANGE] = aptRangeValue[MELEE_RANGE];
	aptitudeRange[REMOTE_RANGE] = aptRangeValue[REMOTE_RANGE];
	aptitudeRange[DURABLE_RANGE] = aptRangeValue[DURABLE_RANGE];
	aptitudeRange[DEFENSE_RANGE] = aptRangeValue[DEFENSE_RANGE];

	%s

	baseAttrRange += [baseAttrs];
	baseAttrRange += [baseRange];
	baseAttrRange += [maxRange];
	baseAttrRange += [aptitudeRange];
	return baseAttrRange;
}

//水手洗练属性
mapping* GetSailorTrainAttrs(object oUser, int lv, int quality, int star )
{
	mapping* trainAttrRange = [];
	mapping trainAttrs = {};
	mapping trainRange = {};
	mapping maxRange = {};
	mapping aptitudeRange = {};

	%s
	trainAttrRange += [trainAttrs];
	trainAttrRange += [trainRange];
	trainAttrRange += [maxRange];
	trainAttrRange += [aptitudeRange];
	return trainAttrRange;
}

//水手升星属性变化
mapping* CalcSailorBaseAttrs(int lv, int quality, int star, mapping aptitudeRange)
{
	mapping* upstarAttrRange = [];
	mapping upstarLevelAttrs = {};
	mapping upstarLevelRange = {};
	mapping maxRange = {};

	%s
	upstarAttrRange += [upstarLevelAttrs];
	upstarAttrRange += [upstarLevelRange];
	upstarAttrRange += [maxRange];
	return upstarAttrRange;
}

//水手升级属性变化
mapping CalcSailorUpgradeAttrs(int lv, int quality, int star, mapping upgradeRange)
{
	mapping upgradeAttrs = {};

	%s
	return upgradeAttrs;
}


//水手临时数据
mapping __CustomCalcSailorTmp( object oUser, int sailorId, mapping mpSailorTmp )
{
	int lv = oUser->GetSailorLv(sailorId);
	int quality = GetSailorQuality(); 
	int star = oUser->GetSailorStar( sailorId );

%s
	return mpSailorTmp;
}

// 水手基础属性影响
mapping __CustomBaseEffect( object oUser, int sailorId, string boatKey, mapping mpBase )
{
	int lv = oUser->GetSailorLv(sailorId);
	int star = oUser->GetSailorStar( sailorId );
	int quality = GetSailorQuality(); 

%s

	return mpBase;
}

// 水手战斗数值影响
mapping __CustomFightValueEffect( object oUser, int sailorId, string boatKey, mapping mpFightValue )
{
	int lv = oUser->GetSailorLv(sailorId);
	int star = oUser->GetSailorStar( sailorId );

%s

	return mpFightValue;
}

// -----------------------------------------

'''

begin = u"//----------------------- Auto Genrate Begin --------------------\n"
end = u"//----------------------- Auto Genrate End   --------------------\n"
p = re.compile(begin + r".*?" + end, re.S | re.M)

attrSrc = u'''RESET_ONUPDATE_VAR(%s, %s)'''
#attrReviseSrc = u'''static float %s = %s;'''
attrReviseSrc = u'''static int %s = %s;'''

headExp = re.compile(r"(?P<var_name>\w+)\((?P<var_type>\w+)\)")

# 解析水手表
def parse_sailor_sheet(sh, dicVar, output_path):
	startRow = get_int_from_sheet( sh, 3, 1 ) - 1
	headRow = startRow - 1
	print( "startRow = %d"%startRow )
	print( "headRow = %d"%headRow )

	#表添加了新的列，这个变量要改
	#endCol = 27 
	endCol = sh.ncols

	for row in range(startRow, sh.nrows):
		baseSrcLst = [];
		fightValueSrcLst = [];
		sailorTmpSrcLst = [];
		sailorBaseSrcLst = [];
		sailorTrainSrcLst = [];
		upstarUpgradeSailorLst = [];
		upgradeSailorLst = [];
		sailorInvestLst = [];
		attrLst = [];
		reviseAttrLst = [];
		commonLst = [];
		sailorId = get_str_from_sheet(sh, row, 0)
		for col in range(0, endCol):
			head = get_str_from_sheet(sh, headRow, col )
			if (len(head) == 0):
				continue
			data = get_str_from_sheet(sh, row, col )
			if (len(data) == 0):
				continue

			#print( "[%s]=%s"%(head, data) )
			if ( head == u"formula" ):
				note = get_str_from_sheet(sh, headRow-2, col )
				# TODO:打断公式取左值，看看是那种类型的变量
				eqCharIdx = data.find(u"=")
				lrSplit = re.compile(u'[=＝]{1}')

				if eqCharIdx != -1:
					lvalue = data[0 : eqCharIdx]
					lvalue = lvalue.strip()

				src = parse_function(data, note, "", dicVar, "\t// %s%s%s" );
				print(src)
				if dicVar[lvalue]["var_type"] == u"战斗数值":
					fightValueSrcLst.append( src );
				elif dicVar[lvalue]["var_type"] == u"水手临时数值":
					sailorTmpSrcLst.append( src );
				elif dicVar[lvalue]["var_type"] == u"船只基础数值":
					baseSrcLst.append( src );
				elif dicVar[lvalue]["var_type"] == u"水手基础属性值":
					sailorBaseSrcLst.append( src );
				elif dicVar[lvalue]["var_type"] == u"水手洗练属性值":
					sailorTrainSrcLst.append( src );
				elif dicVar[lvalue]["var_type"] == u"水手升星属性值":
					upstarUpgradeSailorLst.append( src );
				elif dicVar[lvalue]["var_type"] == u"水手升级属性值":
					upgradeSailorLst.append( src );
				elif dicVar[lvalue]["var_type"] == u"水手投资获得经验值":
					sailorInvestLst.append( src );
				elif dicVar[lvalue]["var_type"] == u"公用":
					commonLst.append( src );
				continue
			
			tmp = headExp.match( head )
			if tmp == None:
				continue

			var_name = tmp.group("var_name")
			var_type = tmp.group("var_type")

			if var_type == "int":
				var = int(data)
				srcAttr = attrSrc%(var_name, PythonData2Lpc(var) )
				attrLst.append(srcAttr)
			if var_type == "float":
				var = float(data)
				srcAttr = attrSrc%(var_name, PythonData2Lpc(var) )
				attrLst.append(srcAttr)
			if var_type == "string":
				var = data
				srcAttr = attrSrc%(var_name, PythonData2Lpc(var) )
				attrLst.append(srcAttr)
			if var_type == "array":
				var = [] 
				tmpLst = data.split(",")
				for tmp in tmpLst:
					var.append( int(tmp) )
				srcAttr = attrSrc%(var_name, PythonData2Lpc(var) )
				attrLst.append(srcAttr)
			if var_type == "special":
				var = []
				tmpLst = data.split(";")
				for st in tmpLst:
					tm = st.split(",")
					tmp1 = [];
					for tmp in tm:
						tmp1.append( int(tmp) )
					var.append(tmp1)
				srcAttr = attrSrc%(var_name, PythonData2Lpc(var) )
				attrLst.append(srcAttr)

			if var_type == "intermediate":
				#reviseVar = int(data)/100.0
				reviseVar = int(data)
				reviseAttr = attrReviseSrc%(var_name, PythonData2Lpc(reviseVar) )
				reviseAttrLst.append(reviseAttr)

			if var_type == "dir":
				var = []
				tmpLst = data.split(";")
				for st in tmpLst:
					tm = st.split(",")
					tmp1 = []
					for tmp in tm:
						tmp1.append(tmp)
					var.append(tmp1)
				srcAttr = attrSrc%(var_name, PythonData2Lpc(var) )
				attrLst.append(srcAttr)

			if var_type == "dir_map":
				var = []
				tmpLst = data.split(";")
				for st in tmpLst:
					tm = st.split(",")
					tmp1 = [];
					for tmp in tm:
						tmp1.append( int(tmp) )
					var.append(tmp1)
				srcAttr = attrSrc%(var_name, PythonData2Lpc(var) )
				attrLst.append(srcAttr)
			if var_type == "map":
				var = parse_map(data)
				srcAttr = attrSrc%(var_name, PythonData2Lpc(var))
				attrLst.append(srcAttr)

		
		if sailorId != "":
			filename = "%s/%s.c"%(output_path, sailorId)
			filecontent = srcSailorTemplete%(
				u"\n".join(attrLst)	,
				u"\n".join(reviseAttrLst)	,
				u"\n".join(sailorInvestLst)	,
				u"\n".join(commonLst)	,
				u"\n".join(sailorBaseSrcLst)	,
				u"\n".join(sailorTrainSrcLst)	,
				u"\n".join(upstarUpgradeSailorLst)	,
				u"\n".join(upgradeSailorLst)	,
				u"\n".join(sailorTmpSrcLst)	,
				u"\n".join(baseSrcLst)	,
				u"\n".join(fightValueSrcLst)	
			)

			print( filecontent )
			try:
				src_data = open(filename, "rb").read()
				if len(src_data) == 0:
					src_data = begin + "\n\n" + end
			except IOError:
				src_data = begin + "\n\n" + end

			tmp = p.sub(begin + "\n" + filecontent + "\n" + end, src_data)

			write_file(filename, tmp)











def parse_var_sheet(sh, dicVar):
	for row in range(1, sh.nrows):
		key = ""
		for col in range(0, sh.ncols):
			head = get_str_from_sheet(sh, 0, col)

			if head == u"策划用名":
				key = get_str_from_sheet(sh, row, col)
				dicVar[key] = {}
			else:
				if head == u"程序变量获取":
					get_var = get_str_from_sheet(sh, row, col)
					dicVar[key]["get_func"] = get_var
				elif head == u"程序变量设置":
					set_var = get_str_from_sheet(sh, row, col)
					dicVar[key]["set_func"] = set_var
				elif head == u"变量名":
					name = get_str_from_sheet(sh, row, col)
					dicVar[key]["var_name"] = name
				elif head == u"备注":
					desc = get_str_from_sheet(sh, row, col)
					dicVar[key]["var_desc"] = desc
				elif head == u"更改变量类型":
					var_type = get_str_from_sheet(sh, row, col)
					dicVar[key]["var_type"] = var_type 
				else:
					continue



	


# 使用方法
def usage():
	print """
	USAGE:python main.py root_path 水手.xls sheet_name output_path
		--version : Prints the version number
		--help    : Display this help
	"""

# 导整个表
def parse_xls(filename, sn, output_path):
	try:
		book = xlrd.open_workbook(filename)
	except:
		msg = u"can't open file? %s"%filename
		print( msg )
		usage()
		raise

	# 遍历xls
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		sheetname = sh.name
		print( sheetname )
		# 优先导变量表
		if sheetname == u"变量表":
			parse_var_sheet(sh, dicVar)

	# 导水手表
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		sheetname = sh.name

		if sheetname != sn:
			continue
		
		print("to parse sheet", sn)
		
		parse_sailor_sheet(sh, dicVar, output_path )




	
if __name__ == "__main__":
	argv_len = len(sys.argv)
	if argv_len < 5:
		usage()
	else:
		root_path = sys.argv[1]
		filename = sys.argv[2]
		sheetname = sys.argv[3]

		output_path = sys.argv[4]

		print(root_path)
		print(filename)
		print(sheetname)
		print(output_path)

		# 解析xls
		parse_xls( filename, sheetname, output_path )
