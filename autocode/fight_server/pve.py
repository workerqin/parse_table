# -*- coding:utf-8 -*-

import sys
import os
import xlrd
import common
from Python2Lpc import PythonData2Lpc

reload(sys)
sys.setdefaultencoding('utf-8')

# 使用方法
def usage():
	print """
	USAGE:python main.py root_path 战役.xls sheet_name output_path
		--version : Prints the version number
		--help    : Display this help
	"""

srcData = '''

#include <fight.h>

inherit FIGHT_DATA_PVE;

#include <var_prop.h>
#include <scene.h>
#include <user_key.h>

RESET_ONUPDATE_VAR(AI, %s)
RESET_ONUPDATE_VAR(UserDir, %s)
RESET_ONUPDATE_VAR(FleetDir, %s)
RESET_ONUPDATE_VAR(UserX, %s)
RESET_ONUPDATE_VAR(UserY, %s)
RESET_ONUPDATE_VAR(SceneId, %s)
RESET_ONUPDATE_VAR(PlotId, %s)

RESET_ONUPDATE_VAR(SceneData, %s)

mapping mpTmpShip = %s;
RESET_ONUPDATE_VAR(Ships, mpTmpShip)

RESET_ONUPDATE_VAR(Reward, %s)

'''

begin = u"//----------------------- Auto Genrate Begin --------------------"
end   = u"//----------------------- Auto Genrate End   --------------------\n"

# 导整个表
def parse_xls(filename, sn, output_path):
	try:
		book = xlrd.open_workbook(filename)
	except:
		msg = u"can't open file? %s"%filename
		print( msg )
		usage()
		raise

	hasPlot = False
	# 遍历xls
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		sheetname = sh.name
		if sheetname == u"battle_scene":
			battle_id = common.get_str_from_sheet(sh, 0, 1);
			# 玩家入场ai_list和x，y，dir
			player_ai_list = common.get_str_array_from_sheet(sh, 1, 1);
			player_x = common.get_int_from_sheet(sh, 1, 2)
			player_y = common.get_int_from_sheet(sh, 1, 3)
			player_dir = common.get_int_from_sheet(sh, 1, 4)
			target_dir = common.get_int_from_sheet(sh, 1, 5)
			scene_id = common.get_int_from_sheet(sh, 2, 1)
			reward = common.get_str_array_from_sheet(sh, 4, 1)
			# 敌方入场数据
			scene_data, row_line = common.parse_table(sh, 5, 0)

		if sheetname == u"ships":
			# 敌方入场数据
			ships, row_line = common.parse_table(sh, 0, 0)
		if sheetname == u"plot":
			hasPlot = True

	# 写文件
	if hasPlot:
		src = srcData % (PythonData2Lpc(player_ai_list, True, 2, 0), player_dir, target_dir, player_x, player_y, scene_id, battle_id, PythonData2Lpc(scene_data, True, 1, 1), PythonData2Lpc(ships, True, 1, 1), PythonData2Lpc(reward, True, 2, 0))
	else:
		src = srcData % (PythonData2Lpc(player_ai_list, True, 2, 0), player_dir, target_dir, player_x, player_y, scene_id, 0, PythonData2Lpc(scene_data, True, 1, 1), PythonData2Lpc(ships, True, 1, 1), PythonData2Lpc(reward, True, 2, 0))
	common.write_src(output_path, begin, end, src, 'utf-8')

if __name__ == "__main__":
	argv_len = len(sys.argv)
	if argv_len < 5:
		usage()
	else:
		root_path = sys.argv[1]
		filename = sys.argv[2]
		sheetname = sys.argv[3]
		output_path = sys.argv[4]

		# 解析xls
		parse_xls( filename, sheetname, output_path )
