-- ------------------------------
-- desc: generated by xls2data.py
-- source: 港口config.xls
-- sheet: 港口类型
-- ------------------------------


local port_type_info = {
	['market'] = {
		['name'] = '商业城市',
		['reward'] = '商业投资：可解锁高利润特产',
		['res'] = '#port_merge.png',
	},
	['ship'] = {
		['name'] = '工业城市',
		['reward'] = '工业投资：可解锁新的船只',
		['res'] = '#port_ship.png',
	},
	['pub'] = {
		['name'] = '文化城市',
		['reward'] = '文化投资：可获得航海士信物',
		['res'] = '#port_pub.png',
	},
}

return port_type_info