-- ------------------------------
-- desc: generated by xls2data.py
-- source: ai.xls
-- sheet: ai
-- ------------------------------


local ai_134_info = {
	[1] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'add_skill',
		['ai_param'] = {{1026,1}},
		['des'] = '',
	},
	[2] = {
		['event'] = 'time',
		['event_param'] = {15},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 3,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {100},
		['des'] = '',
	},
	[3] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 2400,
		['target_y'] = 310,
		['target_range'] = 50,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[4] = {
		['event'] = 'time',
		['event_param'] = {15},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 5,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {100},
		['des'] = '',
	},
	[5] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 2400,
		['target_y'] = 1240,
		['target_range'] = 50,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[6] = {
		['event'] = 'time',
		['event_param'] = {15},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 7,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {100},
		['des'] = '',
	},
	[7] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 960,
		['target_y'] = 310,
		['target_range'] = 50,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[8] = {
		['event'] = 'time',
		['event_param'] = {15},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 9,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {100},
		['des'] = '',
	},
	[9] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 960,
		['target_y'] = 1240,
		['target_range'] = 50,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[10] = {
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
	[11] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {50},
		['des'] = '',
	},
	[12] = {
		['event'] = 'time',
		['event_param'] = {15},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "汪直", txt = "护卫船，加速前进！呈发散阵型，瓦解他们！"},
		['des'] = '',
	},
	[13] = {
		['event'] = 'time',
		['event_param'] = {30},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "汪直", txt = "集中火力消灭对方旗舰！别管其它该死的副舰！"},
		['des'] = '',
	},
	[14] = {
		['event'] = 'time',
		['event_param'] = {30},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 10,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {80},
		['des'] = '',
	},
	[15] = {
		['event'] = 'death_count',
		['event_param'] = {1, 1},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'sub_data',
		['ai_param'] = {"must_star",1},
		['des'] = '',
	},
	[16] = {
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
	[17] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "小心敌人的护卫船，他们虽然无远程攻击但近战伤害不容小觑。"},
		['des'] = '',
	},
	[18] = {
		['event'] = 'time',
		['event_param'] = {30},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "注意！敌人护卫船正在朝我方旗舰靠近。"},
		['des'] = '',
	},
	[19] = {
		['event'] = 'time',
		['event_param'] = {45},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 3,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {100},
		['des'] = '',
	},
	[20] = {
		['event'] = 'time',
		['event_param'] = {45},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 5,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {100},
		['des'] = '',
	},
	[21] = {
		['event'] = 'time',
		['event_param'] = {45},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 7,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {100},
		['des'] = '',
	},
	[22] = {
		['event'] = 'time',
		['event_param'] = {45},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 9,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {100},
		['des'] = '',
	},
	[23] = {
		['event'] = 'time',
		['event_param'] = {45},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 24,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "小心敌人的护卫船，他们虽然无远程攻击但近战伤害不容小觑。"},
		['des'] = '',
	},
	[24] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "汪直", txt = "再呈发散阵型，瓦解他们！"},
		['des'] = '',
	},
	[25] = {
		['event'] = 'time',
		['event_param'] = {60},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "汪直", txt = "集中火力消灭对方旗舰！！"},
		['des'] = '',
	},
	[26] = {
		['event'] = 'time',
		['event_param'] = {60},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 10,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {80},
		['des'] = '',
	},
	[27] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 17,
		['ai_event'] = 'playPlot',
		['ai_param'] = {1,2,3},
		['des'] = '',
	},
}

return ai_134_info