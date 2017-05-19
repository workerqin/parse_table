-- ------------------------------
-- desc: generated by xls2data.py
-- source: ai.xls
-- sheet: ai
-- ------------------------------


local ai_83_jy_info = {
	[1] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 28,
		['ai_event'] = 'playPlot',
		['ai_param'] = {1,2,3,4},
		['des'] = '',
	},
	[2] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 1200,
		['target_y'] = 1100,
		['target_range'] = 100,
		['next_ai'] = 3,
		['ai_event'] = 'add_data',
		['ai_param'] = {"num_1",1},
		['des'] = '',
	},
	[3] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'leave_scene',
		['ai_param'] = {2},
		['des'] = '',
	},
	[4] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 1200,
		['target_y'] = 200,
		['target_range'] = 100,
		['next_ai'] = 5,
		['ai_event'] = 'add_data',
		['ai_param'] = {"num_1",1},
		['des'] = '',
	},
	[5] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'leave_scene',
		['ai_param'] = {3},
		['des'] = '',
	},
	[6] = {
		['event'] = 'death',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {4},
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
		['ai_event'] = 'enter_scene',
		['ai_param'] = {5},
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
		['ai_event'] = 'enter_scene',
		['ai_param'] = {6},
		['des'] = '',
	},
	[9] = {
		['event'] = 'death',
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
	[10] = {
		['event'] = 'death',
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
	[11] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_1",cond = ">=",value = 3},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'playPlot',
		['ai_param'] = {7},
		['des'] = '',
	},
	[12] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_2",cond = ">=",value = 4},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'playPlot',
		['ai_param'] = {5,6},
		['des'] = '',
	},
	[13] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_1",cond = ">=",value = 6},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'battle_end',
		['ai_param'] = {1},
		['des'] = '',
	},
	[14] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_2",cond = ">=",value = 7},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'battle_end',
		['ai_param'] = {0},
		['des'] = '',
	},
	[15] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 1000,
		['target_y'] = 1100,
		['target_range'] = 20,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[16] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 1000,
		['target_y'] = 200,
		['target_range'] = 20,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[17] = {
		['event'] = 'time',
		['event_param'] = {3},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 18,
		['ai_event'] = '',
		['ai_param'] = nil,
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
		['ai_event'] = 'delay',
		['ai_param'] = {10},
		['des'] = '',
	},
	[19] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 20,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {10,11},
		['des'] = '',
	},
	[20] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 21,
		['ai_event'] = 'delay',
		['ai_param'] = {10},
		['des'] = '',
	},
	[21] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 22,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {12,13},
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
		['ai_event'] = 'delay',
		['ai_param'] = {10},
		['des'] = '',
	},
	[23] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 24,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {14,15},
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
		['ai_event'] = 'delay',
		['ai_param'] = {10},
		['des'] = '',
	},
	[25] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 26,
		['ai_event'] = 'enter_scene',
		['ai_param'] = {16,17},
		['des'] = '',
	},
	[26] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 27,
		['ai_event'] = 'delay',
		['ai_param'] = {10},
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
		['ai_event'] = 'enter_scene',
		['ai_param'] = {18,19},
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
		['ai_param'] = {txt = "护送6艘平民船安全逃离，平民船死亡数量不能超过6。"},
		['des'] = '',
	},
	[29] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_1",cond = ">=",value = 1},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'sub_data',
		['ai_param'] = {"must_star",1},
		['des'] = '',
	},
	[30] = {
		['event'] = 'data_check',
		['event_param'] = {key = "num_1",cond = ">=",value = 3},
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

return ai_83_jy_info