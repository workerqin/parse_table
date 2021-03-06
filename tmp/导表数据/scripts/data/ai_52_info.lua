-- ------------------------------
-- desc: generated by xls2data.py
-- source: ai.xls
-- sheet: ai
-- ------------------------------


local ai_52_info = {
	[1] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 13,
		['ai_event'] = 'playPlot',
		['ai_param'] = {1,2,3,4},
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
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {0},
		['des'] = '',
	},
	[3] = {
		['event'] = 'time',
		['event_param'] = {10},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {6,7,8,9},
		['des'] = '',
	},
	[4] = {
		['event'] = 'time',
		['event_param'] = {11},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 14,
		['ai_event'] = 'say',
		['ai_param'] = {name = "守备军官", txt = "你们这些海盗居然敢在汉萨同盟的海域撒野！"},
		['des'] = '',
	},
	[5] = {
		['event'] = 'time',
		['event_param'] = {11},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 6,
		['ai_event'] = 'set_speed_ratio',
		['ai_param'] = {100},
		['des'] = '',
	},
	[6] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 2400,
		['target_y'] = 1100,
		['target_range'] = 50,
		['next_ai'] = 7,
		['ai_event'] = 'say',
		['ai_param'] = {name = "北欧海盗", txt = "让他们互相残杀，我们乘机溜吧！"},
		['des'] = '',
	},
	[7] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'leave_scene',
		['ai_param'] = {2,3,4,5},
		['des'] = '',
	},
	[8] = {
		['event'] = 'time',
		['event_param'] = {18},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'set_teamid',
		['ai_param'] = {2},
		['des'] = '',
	},
	[9] = {
		['event'] = 'time',
		['event_param'] = {18},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "守备队长", txt = "咦？你们不是汉萨同盟的商船，本海域严禁汉萨同盟以外的船只经过，速速离开。"},
		['des'] = '',
	},
	[10] = {
		['event'] = 'time',
		['event_param'] = {11},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "北欧海盗", txt = "那是阿姆斯特丹的守备军，快撤！"},
		['des'] = '',
	},
	[11] = {
		['event'] = 'time',
		['event_param'] = {18},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "", txt = "汉萨同盟居然要独霸整个海域，实在丧心病狂，我们决不退缩。"},
		['des'] = '',
	},
	[12] = {
		['event'] = 'time',
		['event_param'] = {19},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "守备队长", txt = "你会为自己的决定后悔的，进攻！"},
		['des'] = '',
	},
	[13] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "击杀所有北欧海盗。"},
		['des'] = '',
	},
	[14] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "击杀所有阿姆斯特丹守备军。"},
		['des'] = '',
	},
	[15] = {
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
	[16] = {
		['event'] = 'death',
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
	[17] = {
		['event'] = 'time',
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
	[18] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'add_skill',
		['ai_param'] = {{1002,1}},
		['des'] = '',
	},
	[19] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {25},
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

return ai_52_info