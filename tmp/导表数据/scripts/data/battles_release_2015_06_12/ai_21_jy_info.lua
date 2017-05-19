-- ------------------------------
-- desc: generated by xls2data.py
-- source: ai.xls
-- sheet: ai
-- ------------------------------


local ai_21_jy_info = {
	[1] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 9,
		['ai_event'] = 'playPlot',
		['ai_param'] = {1,2,3},
		['des'] = '',
	},
	[2] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {99},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "海盗水手", txt = "我好像听到打雷了，嗝！"},
		['des'] = '',
	},
	[3] = {
		['event'] = 'time',
		['event_param'] = {12},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "摩尔船长", txt = "有敌人偷袭！水手们，拿起武器应战"},
		['des'] = '',
	},
	[4] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {80},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "摩尔船长", txt = "醒醒，醉鬼们！拿武器，不是拿酒瓶"},
		['des'] = '',
	},
	[5] = {
		['event'] = 'goto',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 2200,
		['target_y'] = 800,
		['target_range'] = 100,
		['next_ai'] = 0,
		['ai_event'] = '',
		['ai_param'] = nil,
		['des'] = '',
	},
	[6] = {
		['event'] = 'time',
		['event_param'] = {12},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'del_ai',
		['ai_param'] = {5},
		['des'] = '',
	},
	[7] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {99},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "海盗水手", txt = "ZZZzzz，好多金子！"},
		['des'] = '',
	},
	[8] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {99},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'say',
		['ai_param'] = {name = "海盗水手", txt = "船舱进水了，快逃命吧！"},
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
		['ai_event'] = 'new_goal',
		['ai_param'] = {txt = "击沉所有敌人。"},
		['des'] = '',
	},
	[10] = {
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
	[11] = {
		['event'] = 'battle_start',
		['event_param'] = nil,
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'add_skill',
		['ai_param'] = {{1030,1,"passive"}},
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
		['ai_event'] = 'use_skill',
		['ai_param'] = {1030},
		['des'] = '',
	},
	[13] = {
		['event'] = 'time',
		['event_param'] = {90},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'sub_data',
		['ai_param'] = {"must_star",1},
		['des'] = '',
	},
	[14] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {10},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'sub_data',
		['ai_param'] = {"must_star",2},
		['des'] = '',
	},
	[15] = {
		['event'] = 'hp_ratio_less',
		['event_param'] = {50},
		['target_id'] = '',
		['target_x'] = 0,
		['target_y'] = 0,
		['target_range'] = 0,
		['next_ai'] = 0,
		['ai_event'] = 'use_skill',
		['ai_param'] = {1030},
		['des'] = '',
	},
}

return ai_21_jy_info