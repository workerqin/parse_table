-- ------------------------------
-- desc: generated by xls2data.py
-- source: ai.xls
-- sheet: ai
-- ------------------------------


local ai_5_info = {
	[1] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'playPlot',
		['ai_param'] = {1,2,3,4,5},
		['des'] = '',
	},
	[2] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {10},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 8,
		['ai_event'] = 'playPlot',
		['ai_param'] = {6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36},
		['des'] = '',
	},
	[3] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 4000,
		['target_y'] = 2000,
		['target_range'] = 30,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[4] = {
		['event'] = 'kill',
		['event_param'] = nil,
		['target_id'] = '敌一',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {4,5},
		['des'] = '',
	},
	[5] = {
		['event'] = 'kill',
		['event_param'] = nil,
		['target_id'] = '敌二',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {6,7},
		['des'] = '',
	},
	[6] = {
		['event'] = 'kill',
		['event_param'] = nil,
		['target_id'] = '敌三',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {8},
		['des'] = '',
	},
	[7] = {
		['event'] = 'follow',
		['event_param'] = nil,
		['target_id'] = '敌七',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 300,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
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
}

return ai_5_info