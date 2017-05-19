-- ------------------------------
-- desc: generated by xls2data.py
-- source: ai.xls
-- sheet: ai
-- ------------------------------


local ai_132_info = {
	[1] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 6,
		['ai_event'] = 'playPlot',
		['ai_param'] = {1,2,3},
		['des'] = '',
	},
	[2] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'add_skill',
		['ai_param'] = {{1018,1}},
		['des'] = '',
	},
	[3] = {
		['event'] = 'beHit',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {100},
		['des'] = '',
	},
	[4] = {
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
	[5] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'add_skill',
		['ai_param'] = {{1010,1}},
		['des'] = '',
	},
	[6] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 17,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "敌人的冲锋船近战伤害较高，安宅船远程伤害较高。"},
		['des'] = '',
	},
	[7] = {
		['event'] = 'death',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'add_data',
		['ai_param'] = {"num_a",1},
		['des'] = '',
	},
	[8] = {
		['event'] = 'death',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'add_data',
		['ai_param'] = {"num_b",1},
		['des'] = '',
	},
	[9] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_a",cond = "==",value = 3},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 11,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "敌人的冲锋船被全歼时，持续一段时间会再加入战斗。"},
		['des'] = '',
	},
	[10] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_b",cond = "==",value = 3},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 12,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "敌人的安宅船被全歼时，持续一段时间会再加入战斗。"},
		['des'] = '',
	},
	[11] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 13,
		['ai_event'] = 'delay',
		['ai_param'] = {20},
		['des'] = '',
	},
	[12] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 14,
		['ai_event'] = 'delay',
		['ai_param'] = {20},
		['des'] = '',
	},
	[13] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 15,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {8,9},
		['des'] = '',
	},
	[14] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 16,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {10,11},
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
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "小心！额外的冲锋船加入了战斗！"},
		['des'] = '',
	},
	[16] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "小心！额外的安宅船加入了战斗！"},
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
		['ai_event'] = 'add_data',
		['ai_param'] = {"must_star",2},
		['des'] = '',
	},
	[18] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {30},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'sub_data',
		['ai_param'] = {"must_star",1},
		['des'] = '',
	},
	[19] = {
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

return ai_132_info