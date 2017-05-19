-- ------------------------------
-- desc: generated by xls2data.py
-- source: ai.xls
-- sheet: ai
-- ------------------------------


local ai_12_info = {
	[1] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'playPlot',
		['ai_param'] = {1,2,3,4,5,6,7,8,9,10},
		['des'] = '',
	},
	[2] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {20},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[3] = {
		['event'] = 'attack',
		['event_param'] = nil,
		['target_id'] = '友一',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[4] = {
		['event'] = 'attack',
		['event_param'] = nil,
		['target_id'] = '友二',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[5] = {
		['event'] = 'kill',
		['event_param'] = nil,
		['target_id'] = '敌一',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'del_ai',
		['ai_param'] = {3},
		['des'] = '',
	},
	[6] = {
		['event'] = 'kill',
		['event_param'] = nil,
		['target_id'] = '敌二',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'del_ai',
		['ai_param'] = {4},
		['des'] = '',
	},
	[7] = {
		['event'] = 'kill',
		['event_param'] = nil,
		['target_id'] = '敌三',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 8,
		['ai_event'] = 'playPlot',
		['ai_param'] = {11,12},
		['des'] = '',
	},
	[8] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'battle_end',
		['ai_param'] = {1},
		['des'] = '',
	},
	[9] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {90},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "摩尔海盗", txt = "哪里冒出来的小鬼！自寻死路！"},
		['des'] = '',
	},
	[10] = {
		['event'] = 'can_use_skill',
		['event_param'] = {1002},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 13,
		['ai_event'] = 'playPlot',
		['ai_param'] = {13,14},
		['des'] = '',
	},
	[11] = {
		['event'] = 'catch',
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
	[12] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'del_ai',
		['ai_param'] = {10},
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
		['ai_event'] = 'guide',
		['ai_param'] = {radius=40, pos={x=825,y=30}},
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
		['ai_event'] = 'del_ai',
		['ai_param'] = {14},
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
		['ai_param'] = {"must_star",2},
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
}

return ai_12_info