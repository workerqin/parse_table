-- ------------------------------
-- desc: generated by xls2data.py
-- source: ai.xls
-- sheet: ai
-- ------------------------------


local ai_92_jy_info = {
	[1] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 11,
		['ai_event'] = 'playPlot',
		['ai_param'] = {1,2,3,4,5,6,7,8,9},
		['des'] = '',
	},
	[2] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 1913,
		['target_y'] = 515,
		['target_range'] = 50,
		['next_ai'] = 0,
		['ai_event'] = 'battle_end',
		['ai_param'] = {1},
		['des'] = '',
	},
	[3] = {
		['event'] = 'attack',
		['event_param'] = nil,
		['target_id'] = '友1',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[4] = {
		['event'] = 'follow',
		['event_param'] = nil,
		['target_id'] = '友1',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[5] = {
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
	[6] = {
		['event'] = 'arrive',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 768,
		['target_y'] = 885,
		['target_range'] = 100,
		['next_ai'] = 10,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {6,7,8},
		['des'] = '',
	},
	[7] = {
		['event'] = 'arrive',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 1122,
		['target_y'] = 770,
		['target_range'] = 100,
		['next_ai'] = 0,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {9,10,11},
		['des'] = '',
	},
	[8] = {
		['event'] = 'arrive',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 1662,
		['target_y'] = 574,
		['target_range'] = 100,
		['next_ai'] = 0,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {12,13,14},
		['des'] = '',
	},
	[9] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'cloud',
		['ai_param'] = {60,{400,640},{800,1280}},
		['des'] = '',
	},
	[10] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'playPlot',
		['ai_param'] = {10},
		['des'] = '',
	},
	[11] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "护送莫卧儿商船进入卡利卡特，商船不能死亡。"},
		['des'] = '',
	},
	[12] = {
		['event'] = 'hp_ratio_less',
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
	[13] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {30},
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

return ai_92_jy_info