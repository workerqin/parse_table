-- ------------------------------
-- desc: generated by xls2data.py
-- source: ai.xls
-- sheet: ai
-- ------------------------------


local ai_31_jy_info = {
	[1] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 10,
		['ai_event'] = 'playPlot',
		['ai_param'] = {3,1,2},
		['des'] = '',
	},
	[2] = {
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
	[3] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 928,
		['target_y'] = 969,
		['target_range'] = 50,
		['next_ai'] = 11,
		['ai_event'] = 'say',
		['ai_param'] = {name = "奥斯曼海盗", txt = "嘿嘿，来到爱琴海得先搞清楚状态。"},
		['des'] = '',
	},
	[4] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 500,
		['target_y'] = 1089,
		['target_range'] = 50,
		['next_ai'] = 0,
		['ai_event'] = 'leave_scene',
		['ai_param'] = {5},
		['des'] = '',
	},
	[5] = {
		['event'] = 'time',
		['event_param'] = {10},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "奥斯曼海军", txt = "竟敢在东地中海对阿芒德的“商船”出手，你们是活得不耐烦了?!"},
		['des'] = '',
	},
	[6] = {
		['event'] = 'time',
		['event_param'] = {7},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 8,
		['ai_event'] = 'set_teamid',
		['ai_param'] = {2},
		['des'] = '',
	},
	[7] = {
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
	[8] = {
		['event'] = 'set_ai',
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
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "追上奥斯曼海军"},
		['des'] = '',
	},
	[11] = {
		['event'] = 'set_ai',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 4,
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "击杀所有奥斯曼海巡船。"},
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
		['ai_event'] = 'say',
		['ai_param'] = {name = "奥斯曼海军", txt = "前方船只立刻停止航行，你们因涉嫌袭击奥斯曼商船被批捕了！"},
		['des'] = '',
	},
	[13] = {
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
	[14] = {
		['event'] = 'death',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 15,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[15] = {
		['event'] = 'time_range',
		['event_param'] = {40, ">"},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'sub_data',
		['ai_param'] = {"must_star",2},
		['des'] = '',
	},
	[16] = {
		['event'] = 'death_count',
		['event_param'] = {1,1},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'sub_data',
		['ai_param'] = {"must_star",1},
		['des'] = '',
	},
	[17] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'add_skill',
		['ai_param'] = {{1038,1}},
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
		['ai_event'] = 'battle_end',
		['ai_param'] = {1},
		['des'] = '',
	},
}

return ai_31_jy_info