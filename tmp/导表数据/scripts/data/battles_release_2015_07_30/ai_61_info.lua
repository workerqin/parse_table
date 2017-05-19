-- ------------------------------
-- desc: generated by xls2data.py
-- source: ai.xls
-- sheet: ai
-- ------------------------------


local ai_61_info = {
	[1] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'add_skill',
		['ai_param'] = {{1006,1},{1010,1}},
		['des'] = '',
	},
	[2] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {80},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'use_skill',
		['ai_param'] = {1006},
		['des'] = '',
	},
	[3] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {40},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'use_skill',
		['ai_param'] = {1006},
		['des'] = '',
	},
	[4] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 28,
		['ai_event'] = 'playPlot',
		['ai_param'] = {1,2,3,4,5,6,7},
		['des'] = '',
	},
	[5] = {
		['event'] = 'catch',
		['event_param'] = nil,
		['target_id'] = '玩家',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 4,
		['ai_event'] = 'use_skill',
		['ai_param'] = {1010},
		['des'] = '',
	},
	[6] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'ship_add_effect',
		['ai_param'] = {7,{{id =1,name="jiantou",x=0,y=0,add_ship=true,ctime=50}}},
		['des'] = '',
	},
	[7] = {
		['event'] = 'arrive',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 1461,
		['target_y'] = 1081,
		['target_range'] = 100,
		['next_ai'] = 14,
		['ai_event'] = 'add_data',
		['ai_param'] = {"num_1",1},
		['des'] = '',
	},
	[8] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 22,
		['ai_event'] = 'say',
		['ai_param'] = {name = "", txt = "敌人越来越多，改变方向，向东南方向前进。"},
		['des'] = '',
	},
	[9] = {
		['event'] = 'arrive',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 2319,
		['target_y'] = 734,
		['target_range'] = 100,
		['next_ai'] = 10,
		['ai_event'] = 'add_data',
		['ai_param'] = {"num_1",1},
		['des'] = '',
	},
	[10] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_1",cond = "==",value = 2},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'battle_end',
		['ai_param'] = {1},
		['des'] = '',
	},
	[11] = {
		['event'] = 'time',
		['event_param'] = {10},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 12,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {5,6,19,20},
		['des'] = '',
	},
	[12] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 29,
		['ai_event'] = 'say',
		['ai_param'] = {name = "", txt = "可恶，敌方的主舰实在太坚固了，更多的海盗冲过来了，得想办法远离他们"},
		['des'] = '',
	},
	[13] = {
		['event'] = 'attack',
		['event_param'] = nil,
		['target_id'] = '玩家',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[14] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 8,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {9,10,21,22},
		['des'] = '',
	},
	[15] = {
		['event'] = 'time',
		['event_param'] = {25},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {11,12},
		['des'] = '',
	},
	[16] = {
		['event'] = 'time',
		['event_param'] = {35},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {13,14},
		['des'] = '',
	},
	[17] = {
		['event'] = 'time',
		['event_param'] = {45},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {15,16},
		['des'] = '',
	},
	[18] = {
		['event'] = 'death',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {17},
		['des'] = '',
	},
	[19] = {
		['event'] = 'beHit',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "海盗首领", txt = "尽情攻击我吧，不痛不痒，哈哈哈"},
		['des'] = '',
	},
	[20] = {
		['event'] = 'follow',
		['event_param'] = nil,
		['target_id'] = '敌3',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[21] = {
		['event'] = 'time',
		['event_param'] = {30},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "海盗首领", txt = "快跟上，别让他们跑了！"},
		['des'] = '',
	},
	[22] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 23,
		['ai_event'] = 'ship_del_effect',
		['ai_param'] = {1},
		['des'] = '',
	},
	[23] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 31,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {8},
		['des'] = '',
	},
	[24] = {
		['event'] = 'arrive',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 2093,
		['target_y'] = 754,
		['target_range'] = 100,
		['next_ai'] = 0,
		['ai_event'] = 'playPlot',
		['ai_param'] = {16,17,18},
		['des'] = '',
	},
	[25] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'add_data',
		['ai_param'] = {"must_star",1},
		['des'] = '',
	},
	[26] = {
		['event'] = 'time',
		['event_param'] = {60},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'sub_data',
		['ai_param'] = {"must_star",1},
		['des'] = '',
	},
	[27] = {
		['event'] = 'death_count',
		['event_param'] = {2,10},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'sub_data',
		['ai_param'] = {"must_star",2},
		['des'] = '',
	},
	[28] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "消灭所有敌人"},
		['des'] = '',
	},
	[29] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 30,
		['ai_event'] = 'say',
		['ai_param'] = {name = "", txt = "绕开他们，向东北方向前行！"},
		['des'] = '',
	},
	[30] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 33,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "敌方主舰坚不可摧，向东北方向指引箭头航行"},
		['des'] = '',
	},
	[31] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 34,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "向东南方向指引箭头航行,逃离战场。"},
		['des'] = '',
	},
	[32] = {
		['event'] = 'death',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {18},
		['des'] = '',
	},
	[33] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 35,
		['ai_event'] = 'add_path_effect',
		['ai_param'] = {x=1461,y=1081},
		['des'] = '',
	},
	[34] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 36,
		['ai_event'] = 'add_path_effect',
		['ai_param'] = {x=2292,y=734},
		['des'] = '',
	},
	[35] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {7},
		['des'] = '',
	},
	[36] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'leave_scene',
		['ai_param'] = {7},
		['des'] = '',
	},
}

return ai_61_info