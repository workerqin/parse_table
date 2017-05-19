-- ------------------------------
-- desc: generated by xls2data.py
-- source: ai.xls
-- sheet: ai
-- ------------------------------


local ai_103_info = {
	[1] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 31,
		['ai_event'] = 'playPlot',
		['ai_param'] = {5,6,7,8,9,10},
		['des'] = '',
	},
	[2] = {
		['event'] = 'catch',
		['event_param'] = nil,
		['target_id'] = '玩家',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 3,
		['ai_event'] = 'ship_add_effect',
		['ai_param'] = {10,{{id =1,name="tx_qihuo",x=0,y=0,add_ship=false,ctime=150}}},
		['des'] = '',
	},
	[3] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 4,
		['ai_event'] = 'playPlot',
		['ai_param'] = {1,2},
		['des'] = '',
	},
	[4] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'add_data',
		['ai_param'] = {"num_2",1},
		['des'] = '',
	},
	[5] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_2",cond = "==",value = 1},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 26,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {8},
		['des'] = '',
	},
	[6] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 290,
		['target_y'] = 1002,
		['target_range'] = 50,
		['next_ai'] = 7,
		['ai_event'] = 'say',
		['ai_param'] = {name = "吉布斯", txt = "嘘……"},
		['des'] = '',
	},
	[7] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 8,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {0},
		['des'] = '',
	},
	[8] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 9,
		['ai_event'] = 'delay',
		['ai_param'] = {6},
		['des'] = '',
	},
	[9] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'add_data',
		['ai_param'] = {"num_2",1},
		['des'] = '',
	},
	[10] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_2",cond = "==",value = 2},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 12,
		['ai_event'] = 'say',
		['ai_param'] = {name = "吉布斯", txt = "搞定一个。（小声说道）"},
		['des'] = '',
	},
	[11] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_2",cond = "==",value = 2},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'set_teamid',
		['ai_param'] = {3},
		['des'] = '',
	},
	[12] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 13,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {100},
		['des'] = '',
	},
	[13] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 151,
		['target_y'] = 1002,
		['target_range'] = 50,
		['next_ai'] = 14,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {0},
		['des'] = '',
	},
	[14] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 15,
		['ai_event'] = 'delay',
		['ai_param'] = {6},
		['des'] = '',
	},
	[15] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'add_data',
		['ai_param'] = {"num_2",1},
		['des'] = '',
	},
	[16] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_2",cond = "==",value = 3},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 18,
		['ai_event'] = 'say',
		['ai_param'] = {name = "吉布斯", txt = "我只能帮到这，在他们发现我之前我得撤退了。"},
		['des'] = '',
	},
	[17] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_2",cond = "==",value = 3},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'set_teamid',
		['ai_param'] = {3},
		['des'] = '',
	},
	[18] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 19,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {100},
		['des'] = '',
	},
	[19] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 157,
		['target_y'] = 1065,
		['target_range'] = 50,
		['next_ai'] = 33,
		['ai_event'] = 'leave_scene',
		['ai_param'] = {8},
		['des'] = '',
	},
	[20] = {
		['event'] = 'follow',
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
	[21] = {
		['event'] = 'death',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'add_data',
		['ai_param'] = {"num_1",1},
		['des'] = '',
	},
	[22] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {0},
		['des'] = '',
	},
	[23] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_2",cond = "==",value = 3},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 29,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {100},
		['des'] = '',
	},
	[24] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 25,
		['ai_event'] = 'say',
		['ai_param'] = {name = "守卫旗舰", txt = "炮……炮塔！后面发生什么事了！"},
		['des'] = '',
	},
	[25] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "守卫旗舰", txt = "可恶的家伙！一定是你们搞的鬼。"},
		['des'] = '',
	},
	[26] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_1",cond = "<",value = 3},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 27,
		['ai_event'] = 'playPlot',
		['ai_param'] = {3,4},
		['des'] = '',
	},
	[27] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'battle_end',
		['ai_param'] = {0},
		['des'] = '',
	},
	[28] = {
		['event'] = 'death',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'battle_end',
		['ai_param'] = {0},
		['des'] = '',
	},
	[29] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 300,
		['target_y'] = 840,
		['target_range'] = 50,
		['next_ai'] = 24,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[30] = {
		['event'] = 'time',
		['event_param'] = {10},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "守卫旗舰", txt = "给我消灭他们，他们是无法靠近马六甲的城墙的。"},
		['des'] = '',
	},
	[31] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "消灭三艘守卫舰后靠近酒桶，给吉布斯发信号,杰克不能死亡"},
		['des'] = '',
	},
	[32] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_2",cond = "==",value = 1},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "吉布斯已收到信号，等待吉布斯搞定炮塔。"},
		['des'] = '',
	},
	[33] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "消灭护卫舰。"},
		['des'] = '',
	},
	[34] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {50},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'sub_data',
		['ai_param'] = {"must_star",1},
		['des'] = '',
	},
	[35] = {
		['event'] = 'time',
		['event_param'] = {60},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'sub_data',
		['ai_param'] = {"must_star",2},
		['des'] = '',
	},
}

return ai_103_info