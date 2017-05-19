-- ------------------------------
-- desc: generated by xls2data.py
-- source: ai.xls
-- sheet: ai
-- ------------------------------


local ai_22_info = {
	[1] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 10,
		['ai_event'] = 'playPlot',
		['ai_param'] = {1,2,3},
		['des'] = '',
	},
	[2] = {
		['event'] = 'time',
		['event_param'] = {6},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "海盗斥候", txt = "警报！！发现入侵者，赶快回去报告?!"},
		['des'] = '',
	},
	[3] = {
		['event'] = 'time',
		['event_param'] = {7},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 4,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[4] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 1800,
		['target_y'] = 800,
		['target_range'] = 30,
		['next_ai'] = 0,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "追上并消灭【海盗斥候】，不能让他报信。"},
		['des'] = '',
	},
	[5] = {
		['event'] = 'arrive',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 1800,
		['target_y'] = 800,
		['target_range'] = 30,
		['next_ai'] = 6,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[6] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 2100,
		['target_y'] = 500,
		['target_range'] = 20,
		['next_ai'] = 7,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {6,7,8,9,10},
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
		['ai_event'] = 'playPlot',
		['ai_param'] = {6,7,8},
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
		['ai_param'] = {0},
		['des'] = '',
	},
	[9] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {95},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "追上并消灭【海盗斥候】，不能让他报信。"},
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
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "靠近前方海盗。"},
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
		['ai_event'] = 'add_data',
		['ai_param'] = {"must_star",2},
		['des'] = '',
	},
	[12] = {
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
	[13] = {
		['event'] = 'time',
		['event_param'] = {45},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'sub_data',
		['ai_param'] = {"must_star",2},
		['des'] = '',
	},
	[14] = {
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
}

return ai_22_info