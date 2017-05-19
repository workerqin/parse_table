#include <debug.h>

static mapping portsData = copy("data/port_data"->get_data());
static mapping goodsData = copy("data/goods_data"->get_data());

static int* goodsIds = keys(goodsData);
static int* portIds = keys(portsData);
static mapping goodsType = {};
static mapping goodsLevel = {};
static mapping portForbid = {};

static mapping portDefaultGoods = {};
static mapping goodsDefaultPort = {};
static mapping portAllGoods = {};
static string* allGoodsTypes = [];
static mapping fixedGoods = {};

static mapping goodsUseTimes = {};
static mapping portMaybeGoods = {};
static int* limitGoods = [];

#define REPEAT_MAX_TIMES 5
#define REPEAT_TYPE_MAX_TIMES 5

string GetPortName(int portId)
{
	return portsData[portId]["name"];
}

string GetGoodsName(int goodsId)
{
	string name = goodsData[goodsId]["name"];
	int level = goodsData[goodsId]["level"];
	//return sprintf("lv.%d:%s", level, name);
	return name;
}

string GetGoodsType(int goodsId)
{
	return goodsData[goodsId]["type"];
}

int GetGoodsLevel(int goodsId)
{
	return goodsData[goodsId]["level"];
}

string* GetPortNeedGoodsType(int portId)
{
	return "data/port_goods_data"->GetPortNeedType(portId);
}

void initPortFixedGoods()
{
	foreach (int portId in portIds) {
		if (!IsNull(fixedGoods[portId])) {
			mapping data = map_init(portMaybeGoods, portId);
			int max = "data/port_data"->GetMaxInvest(portId);
			foreach (int level, int goodsId in fixedGoods[portId]) {
				if (level > max) continue;

				data[level] = [goodsId];
				if (level != 1) limitGoods = array_add(limitGoods, goodsId);
			}
		}
	}
}

mapping initPortGoods(int portId)
{
	mapping data = map_init(portMaybeGoods, portId);

	string* needs = GetPortNeedGoodsType(portId);
	int max = "data/port_data"->GetMaxInvest(portId);
	string* selectTypes = [];
	mapping Forbid = portForbid[portId];

	if (!IsNull(portDefaultGoods[portId])) {
		foreach (int level, int* list in portDefaultGoods[portId]) {
			if (IsNull(list)) continue;
			if (level > max) continue;
			if (!IsNull(data[level])) continue;
			if (!IsNull(Forbid) && array_have(Forbid, level)) continue;

			int* new_list = copy(list);
			int get = 0;
			while (get < 1 && sizeof(new_list)) {
				int _get = rand_array(new_list);
				new_list -= [_get];

				if (array_have(limitGoods, _get)) continue;
				if (goodsUseTimes[_get] >= REPEAT_MAX_TIMES) continue;

				get = _get;
				break;
			}

			if (get < 1) continue;

			goodsUseTimes[get] += 1;
			data[level] = [get];
			selectTypes = array_add(selectTypes, GetGoodsType(get));
		}
	}

	int remain = 0;
	if (sizeof(selectTypes) < REPEAT_TYPE_MAX_TIMES) {
		remain = REPEAT_TYPE_MAX_TIMES - sizeof(selectTypes);
	}

	mapping portAllData = portAllGoods[portId];
	foreach (int level, int* ids in portAllData) {
		if (IsNull(ids)) continue;
		if (!IsNull(data[level])) continue;
		if (level > max) continue;

		if (!IsNull(Forbid) && array_have(Forbid, level)) continue;

		int get = 0;
		int* new_list = copy(ids);
		while (get < 1 && sizeof(new_list)) {
			int _goodsId = rand_array(new_list);
			new_list -= [_goodsId];
			if (array_have(limitGoods, _goodsId)) continue;
			if (goodsUseTimes[_goodsId] > REPEAT_MAX_TIMES) continue;

			string _type = GetGoodsType(_goodsId);
			if (!array_have(selectTypes, _type)) {
				if (remain < 1) continue;

				selectTypes = array_add(selectTypes, _type);
				remain -= 1;
			}

			get = _goodsId;
			break;
		}
		if (get < 1) continue;
		goodsUseTimes[get] += 1;
		data[level] = [get];
	}

	return data;
}

void initMaybeGoods()
{
	portMaybeGoods = {};
	goodsUseTimes = {};
	limitGoods = [];

	initPortFixedGoods();
	foreach (int _portId in rand_x_array(portIds, sizeof(portIds))) {
		portMaybeGoods[_portId] = initPortGoods(_portId);
	}
	reset_eval_cost();
}

void initDefaultGoods()
{
	mapping data = "data/use_gen_port_goods"->get_data();
	foreach (string name, mapping _data in data) {
		int portId = "data/port_data"->GetIdByName(name);
		xassert(portId > 0, name);
		mapping portData = map_init(portDefaultGoods, portId);
		string* goodsNames = explode(_data["name"], ",");
		foreach (string _name in goodsNames) {
			int _goodsId = "data/goods_data"->GetIdByName(_name);
			if (_goodsId < 1) {
				debug_message("%s:%s", name, _name);
				continue;
			}
			xassert(_goodsId > 0, _name);
			int level = GetGoodsLevel(_goodsId);
			portData[level] = array_add(portData[level], _goodsId);

			goodsDefaultPort[_goodsId] = array_add(goodsDefaultPort[_goodsId], portId);
		}

		mapping fixedgoods = _data["goods"];
		if (IsNull(fixedgoods)) continue;
		mapping FIXED = map_init(fixedGoods, portId);
		foreach (int level, string goodsName in fixedgoods) {
			int goodsId = "data/goods_data"->GetIdByName(goodsName);
			xassert(goodsId > 0, goodsName);
			FIXED[level] = goodsId;
		}
	}

	foreach (int portId in portIds) {
		mapping portData = map_init(portAllGoods, portId); 
		string* needs = GetPortNeedGoodsType(portId);
		int max = "data/port_data"->GetMaxInvest(portId);

		foreach (int _goodsId in goodsIds) {
			if (array_have(needs, GetGoodsType(_goodsId))) continue;
			if (sizeof(goodsDefaultPort[_goodsId])) {
				if (!array_have(goodsDefaultPort[_goodsId], portId)) continue;
			}

			int level = GetGoodsLevel(_goodsId);
			if (level > max) continue;
			portData[level] = array_add(portData[level], _goodsId);
		}
	}

	reset_eval_cost();
}

void init()
{
	initDefaultGoods();
	foreach (int _goodsId in goodsIds) {
		string type = GetGoodsType(_goodsId);
		goodsType[type] = array_add(goodsType[type], _goodsId);

		int level = GetGoodsLevel(_goodsId);
		goodsLevel[level] = array_add(goodsLevel[level], _goodsId);
	}

	foreach (int _portId, mapping _data in portsData) {
		int* all = [];
		if (sizeof(_data["invest_boat_remould"])) {
			all = array_merge(all, keys(_data["invest_boat_remould"]));
		}
		if (sizeof(_data["invest_keepsake"])) {
			all = array_merge(all, keys(_data["invest_keepsake"]));
		}
		if  (sizeof(_data["invest_exp_book"])) {
			all = array_merge(all, keys(_data["invest_exp_book"]));
		}
		portForbid[_portId] = all;
	}

	foreach (int id, mapping info in "data/goods_type_data"->get_data()) {
		allGoodsTypes = array_add(allGoodsTypes, info["type"]);
	}

	reset_eval_cost();
}

void writePort(int portId)
{
	mapping data = portMaybeGoods[portId];
	int max = "data/port_data"->GetMaxInvest(portId);
	int* Forbid = portForbid[portId];
	string* goodsmsg = [];
	for (int i = 1; i <= max; i++) {
		int* ids = data[i];
		if (!IsNull(ids)) {
			foreach (int id in ids) {
				goodsmsg = array_add(goodsmsg, GetGoodsName(id));
			}
		} else {
			if (!IsNull(Forbid) && array_have(Forbid, i)) goodsmsg = array_add(goodsmsg, "invest", 1);
			else goodsmsg = array_add(goodsmsg, "no", 1);
		}
	}

	string allgoodsmsg = string_join(goodsmsg, "	");
	allgoodsmsg = replace_string(allgoodsmsg, "\"", "");
	log_file("auto_goods", sprintf("%s	%s\n", GetPortName(portId), allgoodsmsg));
}

int check()
{
	foreach (int _portId, mapping data in portMaybeGoods) {
		int max = "data/port_data"->GetMaxInvest(_portId);
		if (max != (sizeof(data)+sizeof(portForbid[_portId]))) return 1;
	}

	return 0;
}

void run()
{
	os_command("/log/auto_goods.log", "" , "rm");
	init();

	initMaybeGoods();

	/*
	int i = 1000;
	while (i > 0) {
		if (check()) {
			initMaybeGoods();
			i -= 1;
		} else {
			break;
		}
	}
	*/

	if (check()) {
		log_file("auto_goods", "not all fit\n");
	} else log_file("auto_goods", "all fit\n");
	foreach (int _portId in sort_array(keys(portMaybeGoods), 1)) {
		writePort(_portId);
	}
}

void main()
{
	run();
}
