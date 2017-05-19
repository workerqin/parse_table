# -*- coding: utf-8 -*-

nameToCmd = {
		'调试信息':'DEBUG',
		'播放剧情':'PLAY_STORY',
		}

data = {
		#注释
		'#':('string', 'string'),
		#清空所有任务
		'CLEANALL':('string',),
		#延时
		'DELAY':('string', 'int'),
		#随机延时
		'RANDOM_DELAY':('string', 'array'),
		#延时到
		'DELAY_TO':('string', 'int'),
		#定时启动脚本，定时器
		'SCHEDULE':('string', 'string', 'string', 'int'),
		#子函数调用
		'CALL':('string', 'string', 'string', '*'),
		#子函数调用
		'LOOP':('string', 'int', 'string', '*'),
		#设值
		'SET':('string', 'string', 'string', '?'),
		#加法
		'ADD':('string', 'string', 'string', '?'),
		#条件判断
		'IF':('string', 'string', '?', 'string', '?', "string", "string"),
		#设置脚本运行时长
		'SET_TIMEOUT':('string', 'int'),
		#运行触发器
		'RUN_TRIGGER':('string', 'string', 'macros'),
		'DEBUG':('string', 'string'),

		'LEADER_RUN_TRIGGER':('string', 'string', 'macros'),
		'PLAY_STORY': ('string', 'string'),
}
