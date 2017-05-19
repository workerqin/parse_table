# -*- coding: utf-8 -*-
# AI导表

import xlrd

import sys
import os
import glob
import getopt
import re
import string
import common
from common import get_str_from_sheet
from common import get_str_array_from_sheet
from common import get_int_from_sheet
from common import write_file
from common import parse_function
from common import parse_expr_right
from common import parse_word
from common import parse_value
from common import replace_str
from common import filter
from Python2Lpc import PythonData2Lpc
from common import write_src
from common import upFirstChar

# 时机
dicOpportunity = {
		u"AI执行":"AI_OPPORTUNITY_RUN",
		u"副本开始":"AI_OPPORTUNITY_SCENE_START",
		u"策略":"AI_OPPORTUNITY_TACTIC",
}

# action
dicAction = {
		u"延迟":"delay",
		u"设置":"op",
		u"打印":"op",
		u"执行AI":"run_ai",
		u"删除特定箱子":"op",
		u"删除特定对象":"op",
		u"添加箱子":"add_box",
		u"添加对象":"add_object",
		u"删除对象":"del_object",
		u"添加浮冰":"op",
		u"添加礁石":"op",
		u"添加海怪":"op",
		u"添加鲨鱼":"op",
		u"发奖":"op",
		u"同步玩家属性":"op",
		u"同步对象属性":"op",
		u"同步场景属性":"op",
		u"播放特效":"op",
		u"退出副本":"op",
		u"生成新一批事件通知":"op",
		u"解禁":"allow_move",
		u"禁止移动":"forbiden_move",
		u"检查玩家补给":"check_user_food",
		u"检查所有玩家补给":"check_users_food",
		u"发放事件奖励":"event_reward",
		u"统计星级":"op",
		u"随机位置添加无血量对象":"add_object_random_pos",
		u"随机位置添加有血量对象":"op",
		u"随机分配任务":"assign_mission",
		u"移动镜头":"move_camera",
		u"初始化副本任务":"op",
		u"初始化副本随机任务":"op",
		u"完成一次玩家任务":"op",
		u"玩家完成任务广播消息":"op",
		u"检查并设置对象打捞状态":"op",
		u"传送":"transport",
		u"弹框提示":"op",
		u"结束副本":"op",
		u"同步副本剩余时间":"remain_time",
		u"同步沉船添加信息":"sync_werck",
}

def get_action_set_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	dicParam = {}

	memo = "%s-[%s]"%(actId, actContent)

	srcFunc = parse_function( actContent, memo, actionFuncName, dicVar, srcActionSetFunction )

	tbActionFuncs[actionFuncName] = srcFunc

	params.append( "@@"+actionFuncName )

def get_action_delay_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	delayTime = int(actContent) 

	params.append( delayTime )

def get_action_null_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	pass


def get_action_run_ai_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	toRunAI = actContent 

	params.append( toRunAI )

def get_action_print_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	dicParam = {}
	exp = parse_word(actContent, dicVar, 0, dicParam)

	memo = "%s-[%s]"%(actId, actContent)

	srcTmp = u'''
%s
	debug_message(%s)
'''%(exp[0], exp[1])

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )


def get_action_delete_object_by_id_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	dicParam = {}
	exp = parse_value(actContent, dicVar, 0, dicParam )

	memo = "%s-[%s]"%(actId, actContent)

	srcTmp = u'''
%s
	ownerMod->DeleteObject(mpOwner, %s);
'''%(exp[0], exp[1])

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )


def get_action_add_box_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	#x,y,box1
	paramLst = actContent.split(",")
	x = int( paramLst[0] )
	y = int( paramLst[1] )
	cehua_symbol = paramLst[2]

	params.append(x)
	params.append(y)
	params.append(cehua_symbol)

def get_action_event_reward_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	dicParam = {}
	lstP = actContent.split(",")
	eventId = int(lstP[0])
	need_broadcast = int(lstP[1]) 

	params.append(eventId)
	params.append(need_broadcast)

def get_action_check_user_food_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	pass

def get_action_check_users_food_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	pass

def get_action_del_box_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	#box1
	paramLst = actContent.split(",")
	cehua_symbol = paramLst[0]

	params.append(cehua_symbol)

parse_args6 = re.compile(r"(?P<arg1>.+),(?P<arg2>.+),(?P<arg3>.+),(?P<arg4>.+),\$\((?P<arg5>.+)\),(?P<arg6>.+)")
parse_args4 = re.compile(r"(?P<arg1>.+),(?P<arg2>.+),\$\((?P<arg3>.+)\),(?P<arg4>.+)")

def get_action_add_ice_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	tmp = parse_args4.match(actContent)

	print( actContent, tmp )

	if ( tmp == None ):
		tmp = actContent.split(",")
		x = tmp[0]
		y = tmp[1]
		str_max_hp = tmp[2]
		cehua_symbol = tmp[3]
	else:
		x = tmp.group("arg1");
		y = tmp.group("arg2");
		str_max_hp = tmp.group("arg3");
		cehua_symbol = tmp.group("arg4");


	memo = "%s-[%s]"%(actId, actContent)
	
	dicParam = {}
	max_hp = parse_value( u"$(%s)"%str_max_hp, dicVar, 0, dicParam);


	srcTmp = u'''
%s
	mapping params = {};
	params[EVENT_DISPATCH_SYMBOL] = "%s";
	params[SCENE_OBJECT_FILE] = SCENE_OBJ_ICE;
	mapping data = {};
	params[SCENE_OBJECT_DATA] = data;
	data["max_hp"] = %s;
	data["hp"] = data["max_hp"];

	ownerMod->AddObject(mpOwner, params, %s, %s)
'''%(max_hp[0], cehua_symbol, max_hp[1], x, y)

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )


def get_action_transport_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	lst = actContent.split(",")
	for s in lst:
		params.append( int(s) )

def get_action_add_rock_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	tmp = parse_args4.match(actContent)

	print( actContent, tmp )

	if ( tmp == None ):
		tmp = actContent.split(",")
		x = tmp[0]
		y = tmp[1]
		str_max_hp = tmp[2]
		cehua_symbol = tmp[3]
	else:
		x = tmp.group("arg1");
		y = tmp.group("arg2");
		str_max_hp = tmp.group("arg3");
		cehua_symbol = tmp.group("arg4");

	memo = "%s-[%s]"%(actId, actContent)
	
	dicParam = {}
	max_hp = parse_value( u"$(%s)"%str_max_hp, dicVar, 0, dicParam);


	srcTmp = u'''
%s
	mapping params = {};
	params[EVENT_DISPATCH_SYMBOL] = "%s";
	params[SCENE_OBJECT_FILE] = SCENE_OBJ_ROCK;
	mapping data = {};
	params[SCENE_OBJECT_DATA] = data;
	data["max_hp"] = %s;
	data["hp"] = data["max_hp"];
	ownerMod->AddObject(mpOwner, params, %s, %s)
'''%(max_hp[0], cehua_symbol, max_hp[1], x, y)

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )



def get_action_add_monster_function( actionFuncName, actId, actContent, tbActionFuncs, params ):

	tmp = parse_args6.match(actContent)

	print( actContent, tmp )

	if ( tmp == None ):
		tmp = actContent.split(",")
		x = tmp[0]
		y = tmp[1]
		x1 = tmp[2]
		y1 = tmp[3]
		str_max_hp = tmp[4]
		cehua_symbol = tmp[5]
	else:
		x = tmp.group("arg1");
		y = tmp.group("arg2");
		x1 = tmp.group("arg3");
		y1 = tmp.group("arg4");
		str_max_hp = tmp.group("arg5");
		cehua_symbol = tmp.group("arg6");

	memo = "%s-[%s]"%(actId, actContent)
	
	dicParam = {}
	max_hp = parse_value( u"$(%s)"%str_max_hp, dicVar, 0, dicParam);


	srcTmp = u'''
%s
	mapping params = {};
	params[EVENT_DISPATCH_SYMBOL] = "%s";
	mapping data = {};

	params[SCENE_OBJECT_DATA] = data;
	data["max_hp"] = %s;
	data["hp"] = data["max_hp"];

	params[SCENE_OBJECT_TARGET_X] = %s;
	params[SCENE_OBJECT_TARGET_Y] = %s;
	params[SCENE_OBJECT_FILE] = SCENE_OBJ_MONSTER;
	
	ownerMod->AddObject(mpOwner, params, %s, %s);
'''%(max_hp[0], cehua_symbol, max_hp[1], x1, y1, x, y)

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )

def get_action_add_biteboat_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	tmp = parse_args6.match(actContent)

	print( actContent, tmp )

	if ( tmp == None ):
		tmp = actContent.split(",")
		x = tmp[0]
		y = tmp[1]
		x1 = tmp[2]
		y1 = tmp[3]
		str_max_hp = tmp[4]
		cehua_symbol = tmp[5]
	else:
		x = tmp.group("arg1");
		y = tmp.group("arg2");
		x1 = tmp.group("arg3");
		y1 = tmp.group("arg4");
		str_max_hp = tmp.group("arg5");
		cehua_symbol = tmp.group("arg6");

	memo = "%s-[%s]"%(actId, actContent)
	
	dicParam = {}
	max_hp = parse_value( u"$(%s)"%str_max_hp, dicVar, 0, dicParam);


	srcTmp = u'''
%s
	mapping params = {};
	params[EVENT_DISPATCH_SYMBOL] = "%s";
	mapping data = {};
	params[SCENE_OBJECT_DATA] = data;
	data["max_hp"] = %s;
	data["hp"] = data["max_hp"];
	params[SCENE_OBJECT_TARGET_X] = %s;
	params[SCENE_OBJECT_TARGET_Y] = %s;
	params[SCENE_OBJECT_FILE] = SCENE_OBJ_SHARK;
	
	ownerMod->AddObject(mpOwner, params,  %s, %s)
'''%(max_hp[0], cehua_symbol, max_hp[1], x1, y1, x, y)

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )


def get_action_add_object_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	#x,y,box1
	paramLst = actContent.split(",")
	x = int( paramLst[0] )
	y = int( paramLst[1] )
	type = int( paramLst[2] )
	cehua_symbol = paramLst[3]

	params.append(x)
	params.append(y)
	params.append(type)
	params.append(cehua_symbol)

def get_action_add_object_random_pos_function(actionFuncName, actId, actContent, tbActionFuncs, params):
	paramLst     = actContent.split(",")
	mapid        = int( paramLst[0] )
	type         = int( paramLst[1] )
	cehua_symbol = paramLst[2]

	params.append(mapid)
	params.append(type)
	params.append(cehua_symbol)

def get_action_add_object_random_pos_hp_function(actionFuncName, actId, actContent, tbActionFuncs, params):
	tmp = parse_args4.match(actContent)

	#print( actContent, tmp )

	if ( tmp == None ):
		tmp          = actContent.split(",")
		type         = tmp[0]
		mapid        = tmp[1]
		str_max_hp   = tmp[2]
		cehua_symbol = tmp[3]
	else:
		type         = tmp.group("arg1");
		mapid        = tmp.group("arg2");
		str_max_hp   = tmp.group("arg3");
		cehua_symbol = tmp.group("arg4");

	memo = "%s-[%s]"%(actId, actContent)
	
	dicParam = {}
	max_hp = parse_value( u"$(%s)"%str_max_hp, dicVar, 0, dicParam);

	srcTmp = u'''
%s
	mapping params = {};
	params[EVENT_DISPATCH_SYMBOL] = "%s";

	mapping data = {};
	params[SCENE_OBJECT_DATA] = data;

	data["max_hp"] = %s;
	data["hp"] = data["max_hp"];

	mapping EventMaps = mpOwner[SCENE_EVENT_MAPS];
	mapping Map =  EventMaps[%s];
	if (IsNull(Map)) return 0;
	
	int* map_keys = keys(Map);	
	int ran = random(sizeof(map_keys));
	int key = map_keys[ran];
	
	int* pos = Map[key];
	if (IsNull(pos)) return 0;

	int  x = pos[0]; 
	int  y = pos[1]; 
	int targetX = 0;
	int targetY = 0;
	if (sizeof(pos) == 4) {	
		targetX = pos[2];
		targetY = pos[3];
	}

	params[SCENE_OBJECT_TARGET_X] = targetX;
	params[SCENE_OBJECT_TARGET_Y] = targetY;

	// TODO:object type
	params[SCENE_OBJECT_FILE] = "module/action/add_object"->GetObjFileByType(%s);

	map_delete(Map, key);	
	ownerMod->AddObject(mpOwner, params, x, y )
'''%(max_hp[0], cehua_symbol, max_hp[1], mapid, type)

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )

#随机分配任务
def get_action_assign_mission_function(actionFuncName, actId, actContent, tbActionFuncs, params):
	pass

def get_action_move_camera_function(actionFuncName, actId, actContent, tbActionFuncs, params):
	lstParam = actContent.split(",");

	for s in lstParam:
		params.append( int(s) )

#初始化副本随机任务
def get_action_init_scene_random_mission_function(actionFuncName, actId, actContent, tbActionFuncs, params):
	paramLst      = actContent.split(",")
	arrLen        = len(paramLst)
	if  arrLen%2 != 0 :
		print "任务参数个数不对"
		sys.exit()

	missions = {}
	for i in range(0, arrLen, 2):
		id    = int(paramLst[i])
		times = int(paramLst[i + 1])	 
		missions[id] = times

	memo = "%s-[%s]"%(actId, actContent)
		
	srcTmp = u'''
	mapping tmp  = %s;

	mapping scene = GetSceneInfo( mpAction );
	scene[SCENE_USERS_MISSIONS] = tmp;	
'''%(PythonData2Lpc(missions, True))
	
	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )
	tbActionFuncs[actionFuncName] = srcFunc
	params.append("@@"+actionFuncName)

#初始化副本任务
def get_action_init_scene_mission_function(actionFuncName, actId, actContent, tbActionFuncs, params):
	paramLst      = actContent.split(",")
	arrLen        = len(paramLst)
	if  arrLen%2 != 0 :
		print "任务参数个数不对"
		sys.exit()

	missions = {}
	for i in range(0, arrLen, 2):
		id    = int(paramLst[i])
		times = int(paramLst[i + 1])	 
		missions[id] = times

	memo = "%s-[%s]"%(actId, actContent)
		
	srcTmp = u'''
	mapping tmp  = %s;
	if (IsNull(tmp)) return 0;
	
	int* keys = keys(tmp);
	int ran = random(sizeof(keys));
	int mission_id = keys[ran];
	int mission_times = tmp[mission_id];

	mapping scene = GetSceneInfo( mpAction );
	scene[SCENE_USERS_MISSIONS] = {mission_id:mission_times};	
'''%(PythonData2Lpc(missions, True))
	
	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )
	tbActionFuncs[actionFuncName] = srcFunc
	params.append("@@"+actionFuncName)



#完成一次玩家任务
def get_action_do_user_mission_function(actionFuncName, actId, actContent, tbActionFuncs, params):
	paramList = string.split(actContent)
	if len(paramList) != 1:
		print "动作内容填写错误"

	mission_type = paramList[0]
	srcTmp = u'''
	mapping mission = mpTargetData["mission"];
	if (IsNull(mission)) return 0;
	
	if (mission["times"] <= 0) return 0;
	if (mission["complete"] == 1) return 0;
	if (mission["type"] != %s) return 0;

	mission["progress"]++;
	if (mission["times"] == mission["progress"]) {
		mission["complete"] = 1;
		if (IsNull(mpOwner["first_complete"])) {
			mpOwner["first_complete"] = target;
		}	 	
		mpOwner["complete_cnt"] += 1;
	}
	

	int* uids = ownerMod->GetAllUser( mpOwner );
		
	if (sizeof(uids))
	{
		scene_mission _mission = new scene_mission;

		_mission->uid      = target;
		_mission->name     = mpTarget[SCENE_OBJECT_NAME];
		_mission->type     = mission["type"];
		_mission->times    = mission["times"];
		_mission->complete = mission["complete"];
		_mission->progress = mission["progress"];

		buffer buf = patch_pto_args(RPC_CLIENT_COPY_SCENE_MISSIONS, _mission );
		fs_transmit_netd_pto(uids, buf);
	}


'''%(mission_type)

	memo = "%s-[%s]"%(actId, actContent)
	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )
	tbActionFuncs[actionFuncName] = srcFunc
	params.append("@@"+actionFuncName)

def get_action_set_dalao_status_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	paramList = string.split(actContent)
	if len(paramList) != 0:
		print "动作内容填写错误"

	srcTmp = u'''
	mapping users = map_init(mpOwner, SCENE_USERS);
	int last_uid = mpTargetData["is_operation"];
	
	//如果上一次被人打捞过但是因为退出副本还没打捞成功
	if(last_uid > 0) {
		if (!map_have(users, last_uid)) {
			mpTargetData["is_operation"] = mpParams[AI_PARAMS_CLICK_OBJECT_UID];
		}
	}
	else {
		mpTargetData["is_operation"] = mpParams[AI_PARAMS_CLICK_OBJECT_UID];
	}
'''
	memo = "%s-[%s]"%(actId, actContent)
	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )
	tbActionFuncs[actionFuncName] = srcFunc
	params.append("@@"+actionFuncName)


#玩家完成任务广播消息
def get_action_complete_mission_message_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	srcTmp = u'''
	int* uids = ownerMod->GetAllUser( mpOwner );
	if (sizeof(uids))
	{
		buffer buf = patch_pto_args(RPC_CLIENT_COPY_SCENE_COMPLETE_MISSION_MESSAGE, target);
		fs_transmit_netd_pto(uids, buf);
	}
'''

	memo = "%s-[%s]"%(actId, actContent)
	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )
	tbActionFuncs[actionFuncName] = srcFunc
	params.append("@@"+actionFuncName)

def get_action_del_object_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	#box1
	paramLst = actContent.split(",")
	cehua_symbol = paramLst[0]

	params.append(cehua_symbol)


def get_action_get_reward_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	dicParam = {}
	lstP = actContent.split(",");
	id = lstP[0]
	rewardTb = lstP[1]
	need_broadcast = lstP[2]
	eventId = lstP[3]

	expId = parse_value(id, dicVar, 0, dicParam )
	expRewardTb = parse_word(rewardTb, dicVar, 0, dicParam )

	memo = "%s-[%s]"%(actId, actContent)

	srcTmp = u'''
%s
	"wanfa/scene/scene_util"->ActionGetRewardMapReduce(mpOwner, %s, %s, %s, %s);	
'''%(expId[0] + expRewardTb[0], expId[1], expRewardTb[1], need_broadcast, eventId)

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )

def get_action_fuben_werck_owner_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	#x,y,box1
	paramLst = actContent.split(",")
	x = int( paramLst[0] )
	y = int( paramLst[1] )
	cehua_symbol = paramLst[2]

	params.append(x)
	params.append(y)
	params.append(cehua_symbol)

def get_action_sync_object_attr_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	dicParam = {}
	lstP = actContent.split(",");
	strObjectId = lstP[0]
	lstAttr = lstP[1:]
	objectId = parse_value(strObjectId, dicVar, 0, dicParam )

	memo = u"%s-[%s]"%(actId, actContent)

	srcDeclareAttr = u""
	srcAttrResult  = u"[" 

	for attr in lstAttr:
		attrKey = parse_word(attr, dicVar, 0, dicParam )
		srcDeclareAttr = srcDeclareAttr + "\n"  + attrKey[0]
		srcAttrResult = srcAttrResult + "%s,"%attrKey[1]

	srcAttrResult  = srcAttrResult + u"]" 
	srcTmp = u'''
%s
	mapping scene = GetSceneInfo( mpAction );
	string sceneFile = scene[SCENE_PATH];
	mapping mpObjInfo = sceneFile->GetObjInfo( scene, %s );
	int* allUids = sceneFile->GetAllUser(scene);
	mpTarget[SCENE_OBJECT_FILE]->RsyncAttr( scene, allUids, mpObjInfo, %s);
'''%(objectId[0] + srcDeclareAttr, objectId[1], srcAttrResult  )

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )

def get_action_sync_scene_attr_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	dicParam = {}
	lstP = actContent.split(",");

	memo = u"%s-[%s]"%(actId, actContent)

	srcDeclareAttr = u""
	srcAttrResult  = u"[" 

	for attr in lstP:
		attrKey = parse_word(attr, dicVar, 0, dicParam )
		srcDeclareAttr = srcDeclareAttr + "\n"  + attrKey[0]
		srcAttrResult = srcAttrResult + "%s,"%attrKey[1]

	srcAttrResult  = srcAttrResult + u"]" 
	srcTmp = u'''
%s
	mapping scene = GetSceneInfo( mpAction );
	string sceneFile = scene[SCENE_PATH];
	sceneFile->SyncSceneAttr( scene, %s );
'''%(srcDeclareAttr,srcAttrResult)

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )

def get_action_calc_star( actionFuncName, actId, actContent, tbActionFuncs, params ):
	memo = u"%s-[%s]"%(actId, actContent)
	
	srcTmp = u'''
	mapping scene = GetSceneInfo( mpAction );
	"data/fuben/explore"->SetSceneStar(scene);
	'''

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )

def get_action_sync_user_attr_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	dicParam = {}
	lstP = actContent.split(",");
	strUID = lstP[0]
	lstAttr = lstP[1:]
	userId = parse_value(strUID, dicVar, 0, dicParam )

	memo = u"%s-[%s]"%(actId, actContent)

	srcDeclareAttr = u""
	srcAttrResult  = u"[" 

	for attr in lstAttr:
		attrKey = parse_word(attr, dicVar, 0, dicParam )
		srcDeclareAttr = srcDeclareAttr + "\n"  + attrKey[0]
		srcAttrResult = srcAttrResult + "%s,"%attrKey[1]

	srcAttrResult  = srcAttrResult + u"]" 

	srcTmp = u'''
%s
	mapping mpUser = GetTargetObj(mpAI, %s, SCENE_OBJ_TYPE_USER);
	if (IsNull(mpUser)) return 0;
	mpTarget[SCENE_OBJECT_FILE]->RsyncAttr( mpOwner, target, mpUser, %s);
'''%(userId[0] + srcDeclareAttr, userId[1], srcAttrResult)

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )

def get_action_create_batch_event_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	dicParam = {}
	lstP = actContent.split(",");
	id = int(lstP[0])

	memo = "%s-[%s]"%(actId, actContent)

	srcTmp = u'''
	"wanfa/scene/scene_util"->create_batch_event_notify(mpOwner, %s);
'''%(id)

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )

def get_action_play_action_function( actionFuncName, actId, actContent, tbActionFuncs, params ):

	dicParam = {}
	lstP = actContent.split(",");
	type = lstP[0]
	expType = parse_word(type, dicVar, 0, dicParam )
	amount = int(lstP[1])

	memo = "%s-[%s]"%(actId, actContent)

	srcTmp = u'''
%s
	"wanfa/scene/scene_util"->play_action(target, %s, %s);
'''%(expType[0], expType[1], amount)

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )

def get_action_end_fuben_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	dicParam = {}

	memo = "%s-[%s]"%(actId, actContent)

	srcTmp = u'''
	mpOwner[SCENE_PATH]->ToFinishFuben(mpOwner, FUBEN_CLOSE_REASON_COMPELTE);
'''

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )

def get_action_fuben_remain_time_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	pass	

def get_action_tips_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	dicParam = {}
	lstP = actContent.split(",");
	tips_id = int(lstP[0])
	interval = int(lstP[1])

	memo = "%s-[%s]"%(actId, actContent)

	srcTmp = u'''
	mapping scene = GetSceneInfo( mpAction );
	string sceneFile = scene[SCENE_PATH];

	int* AllUser = sceneFile->GetAllUser( scene );

	string _name = "module/message/main"->SerializeName(mpTarget[SCENE_OBJECT_NAME]);
	string message = "module/message/main"->SerializeMessage(%s, [_name]);

	send_user_rpc(AllUser, RPC_CLIENT_FUBEN_TIPS, message, %s);

'''%(tips_id, interval)

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )


def get_action_exit_scene_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
	dicParam = {}
	lstP = actContent.split(",");
	uid = parse_value(lstP[0], dicVar, 0, dicParam )

	memo = "%s-[%s]"%(actId, actContent)

	srcTmp = u'''
%s
	int sceneId = mpParams[AI_PARAMS_SCENE_ID];
	ModRemoteCallMain->RemoteCallNoReturn(SERVICE_USER, %s, "module/scene/protocol","UserLeaveFuben", %s, sceneId );
'''%(uid[0], uid[1], uid[1])

	srcFunc = srcActionSetFunction%(memo, actionFuncName, srcTmp )

	tbActionFuncs[actionFuncName] = srcFunc
	params.append( "@@"+actionFuncName )



# action内容解析
dicActionContentParse = {
		u"延迟":get_action_delay_function,
		u"执行AI":get_action_run_ai_function,
		u"设置":get_action_set_function,
		u"打印":get_action_print_function,
		u"添加箱子":get_action_add_box_function,
		u"删除特定箱子":get_action_delete_object_by_id_function,
		u"删除特定对象":get_action_delete_object_by_id_function,
		u"发奖":get_action_get_reward_function,
		u"添加对象":get_action_add_object_function,
		u"删除对象":get_action_del_object_function,
		u"同步玩家属性":get_action_sync_user_attr_function,
		u"同步对象属性":get_action_sync_object_attr_function,
		u"同步场景属性":get_action_sync_scene_attr_function,
		u"添加浮冰":get_action_add_ice_function,
		u"添加礁石":get_action_add_rock_function,
		u"添加海怪":get_action_add_monster_function,
		u"添加鲨鱼":get_action_add_biteboat_function,
		u"播放特效":get_action_play_action_function,
		u"退出副本":get_action_exit_scene_function,
		u"解禁":get_action_null_function,
		u"禁止移动":get_action_null_function,
		u"检查玩家补给":get_action_check_user_food_function,
		u"检查所有玩家补给":get_action_check_users_food_function,
		u"发放事件奖励":get_action_event_reward_function,
		u"生成新一批事件通知":get_action_create_batch_event_function,
		u"统计星级":get_action_calc_star,
		u"随机位置添加无血量对象":get_action_add_object_random_pos_function,
		u"随机位置添加有血量对象":get_action_add_object_random_pos_hp_function,
		u"随机分配任务":get_action_assign_mission_function,
		u"移动镜头":get_action_move_camera_function,
		u"初始化副本任务":get_action_init_scene_mission_function,
		u"初始化副本随机任务":get_action_init_scene_random_mission_function,
		u"完成一次玩家任务":get_action_do_user_mission_function,
		u"玩家完成任务广播消息":get_action_complete_mission_message_function,
		u"检查并设置对象打捞状态":get_action_set_dalao_status_function,
		u"传送":get_action_transport_function,
		u"弹框提示":get_action_tips_function,
		u"结束副本":get_action_end_fuben_function,
		u"同步副本剩余时间":get_action_fuben_remain_time_function,
		u"同步沉船添加信息":get_action_fuben_werck_owner_function,
}

# TODO:公用变量表

# 变量表

dicVar = {}

begin = u"//----------------------- Auto Genrate Begin --------------------"
end   = u"//----------------------- Auto Genrate End   --------------------\n"

srcAITemplete = u'''

// 自动生成AI,来源于[%s]

#include <ai.h>

inherit AI_BASE;

#include <scene.h>
#include <var_prop.h>
#include <macros.h>
#include <module.h>
#include "/rc/rpc/copy_scene.h"
//#include "/rc/rpc/rpc_id.h"
//#include "/rc/rpc/rewards.h"

//--------------------------- 基本属性函数开始 ------------------------------
%s
//--------------------------- 基本属性函数结束 ------------------------------


//--------------------------- 条件函数区开始 ------------------------------
%s
//--------------------------- 条件函数区结束 ------------------------------

//--------------------------- 目标函数区开始 ------------------------------
%s
//--------------------------- 目标函数区结束 ------------------------------

//--------------------------- 动作函数区开始 ------------------------------
%s
//--------------------------- 动作函数区结束 ------------------------------


mixed* actions = %s;

mixed* GetActions()
{
	return actions;
}

mapping mpAlLTargetMethos = %s;

mapping GetAllTargetMethod()
{
	return mpAlLTargetMethos; 
}
'''

# 全变量转换
srcData = '''
// %s
RESET_ONUPDATE_VAR(%s, %s)
'''

# 字符串变量
# 依次变量为: 变量中文名,变量名,变量内容
srcStrData = '''
// %s
RESET_ONUPDATE_VAR(%s, "%s")
'''

# 整形变量
# 依次变量为: 变量中文名,变量名,变量内容
srcIntData = u'''
// %s
RESET_ONUPDATE_VAR(%s, %d)
'''

# 数组变量
# 依次变量为: 变量中文名,类名,变量名,变量内容 to lua
srcArrayData = u'''
// %s
RESET_ONUPDATE_VAR(%s, %s)
'''

srcConditionFunction = u'''
// [备注]%s
int %s( mapping mpAI, int target )
{
	int ownerId = mpAI[AI_KEY_OWNER];
	mapping mpOwner = GetOwner(mpAI);
	string ownerMod = GetOwnerMod(mpAI);
	mapping mpParams = mpAI[AI_KEY_PARAMS];

	//if ( target ) then
	//end

%s

	return 1
}

'''

srcCheckConditionFunction = u'''
// 本AI的判定条件
int CheckCondition(mapping mpAI)
{
%s
}
'''

srcTargetFunction = u'''
// [备注]%s
mixed* %s( mapping mpAI )
{
	int ownerId = mpAI[AI_KEY_OWNER];
	mapping mpOwner = GetOwner(mpAI);
	string ownerMod = GetOwnerMod(mpAI);
	mapping mpParams = mpAI[AI_KEY_PARAMS];


	// 目标选择范围
	string fanwei = "%s";
	// 目标排序方法
	string sort_key = "%s";
	int sort_asc = %d;
	// 目标选择数量
	int select_cnt = %d;

	mixed* mpFanwei = SelectFanwei(mpAI, fanwei);
	int targetType = mpFanwei[0];
	int* tmp_targets = mpFanwei[1];

	// sort_method
	tmp_targets = SortTargets( mpAI, tmp_targets, sort_key, sort_asc )

	int tmp_cnt = 0
	int* targets_result = allocate(select_cnt);
	foreach(int target in tmp_targets) 
	{
		// 获取对象
		mapping mpTarget = GetTargetObj(mpAI, target, targetType);
		mapping mpTargetData = mpTarget[SCENE_OBJECT_DATA];

%s
		targets_result[tmp_cnt] =  target;
		tmp_cnt++
		if ( tmp_cnt >= select_cnt ) break;
	}

	if ( tmp_cnt == 0) return [targetType, []];

	return [targetType, targets_result[0 .. (tmp_cnt - 1)],];

}
'''

srcActionSetFunction = u'''
// [备注]%s
void %s( mapping mpAI, mapping mpAction, int target, int targetType, int deltaTime )
{
	int ownerId = mpAI[AI_KEY_OWNER];
	mapping mpOwner = GetOwner(mpAI);
	string ownerMod = GetOwnerMod(mpAI);
	mapping mpParams = mpAI[AI_KEY_PARAMS];

	// 获取对象
	mapping mpTarget = GetTargetObj(mpAI, target, targetType);
	mapping mpTargetData = mpTarget[SCENE_OBJECT_DATA];

%s
}
'''


# 使用方法
def usage():
	print '''
	USAGE:python ai.py root_path ai.xls sheet_name out_path
		  --version : Prints the version number
		  --help    : Display this help
	ex: python main.py /cygdrive/d/dhh_client/client 战斗数值.xls .//resource/scripts/gameobj/battle/ai'''

# 技能变量策划使用表的解析
def parse_var_sheet(sh, dicVar):
	for row in range(1, sh.nrows):
		key = ""
		for col in range(0, sh.ncols):
			head = get_str_from_sheet(sh, 0, col)

			if head == u"策划用名":
				key = get_str_from_sheet(sh, row, col)
				dicVar[key] = {}

			else:
				if head == u"程序变量获取":
					get_var = get_str_from_sheet(sh, row, col)
					dicVar[key]["get_func"] = get_var
				elif head == u"程序变量设置":
					set_var = get_str_from_sheet(sh, row, col)
					dicVar[key]["set_func"] = set_var
				elif head == u"变量名":
					name = get_str_from_sheet(sh, row, col)
					dicVar[key]["var_name"] = name
				elif head == u"备注":
					desc = get_str_from_sheet(sh, row, col)
					dicVar[key]["var_desc"] = desc
				else:
					continue

	# 打印解析结果
	#print(PythonData2Lpc(dicVar, True))

def parse_condition_sheet(sh, tbCondition):
	# cnd_hpmax_50
	for row in range(1, sh.nrows):
		# 条件id
		conditionId = get_str_from_sheet(sh, row, 0)

		if conditionId == "":
			continue;

		cndFuncName = "cnd" + upFirstChar(conditionId)

		# 条件备注
		conditionMemo = get_str_from_sheet(sh, row, 1)

		paramDefine  = ""
		cnds = ""

		dicParam = {}

		for col in range( 2, sh.ncols):
			cnd = ( get_str_from_sheet(sh, row, col) )
			if (len(cnd) == 0):
				continue
			exp = parse_expr_right(cnd, dicVar, 0, dicParam )
			#print("exp[0]", exp[0])
			#print("exp[1]", exp[1])
			paramDefine += exp[0]
			cnds += '''
	// %s
	if ( !(%s) ) return 0;
'''%(cnd, exp[1])

		conditionSrc = srcConditionFunction%(conditionMemo, cndFuncName, paramDefine + cnds )

		#print( conditionId, conditionMemo )
		#print( conditionSrc )

		tbCondition[conditionId] = conditionSrc

	#print( PythonData2Lpc(tbCondition, True) )

def parse_target_sheet(sh, tbTarget, tbCondition):
	for row in range(1, sh.nrows):

		targetId = get_str_from_sheet(sh, row, 0)
		targetFuncName = "target" + upFirstChar(targetId)

		memo = get_str_from_sheet(sh, row, 1)
		fanwei = get_str_from_sheet(sh, row, 2)
		sortMethod = get_str_from_sheet(sh, row, 3)
		selectCnt = get_int_from_sheet(sh, row, 4)
		if ( selectCnt == 0):
			selectCnt = 9999

		#in buff
		inBuff = get_str_array_from_sheet( sh, row, 5)
		#not in buff
		notInBuff = get_str_array_from_sheet( sh, row, 6)

		#print(targetId, memo, fanwei, sortMethod, selectCnt, inBuff, notInBuff)

		# 解析
		sortKey = ""
		intAsc = 1

		if ( len( sortMethod )):
			lstSortMethod = sortMethod.split(",")
			sortKey = lstSortMethod[0]

			if ( len(lstSortMethod) > 1):
				intAsc = int( lstSortMethod[1] )

		paramDefine = ""
		srcCnd = ""
		dicParam = {}

		for col in range(7, sh.ncols):
			cnd = get_str_from_sheet(sh, row, col)

			if len(cnd) == 0:
				continue

			if ( cnd in tbCondition):
				srcCnd += u'''
		if ( !(%s( ai_obj, nil)) ) continue;
'''%("cnd" + upFirstChar(cnd))
			else:
				exp = parse_expr_right(cnd, dicVar, 1, dicParam )
				paramDefine += exp[0]
				srcCnd += u'''
		if ( !(%s) ) continue;
'''%exp[1]

		src = srcTargetFunction%(memo, targetFuncName, fanwei, sortKey, intAsc, selectCnt, paramDefine + srcCnd )
		#print( src )
		tbTarget[targetId] = src

def parse_action_function( aiId, index, actId, actContent, tbActionFuncs ):
	actionFuncName = "%s_act_%d"%(aiId,  index)
	#print(actionFuncName)
	
	if actId not in dicActionContentParse:
		print("ERROR:unknow action id:", actId)

	func = dicActionContentParse[actId]

	params = []
	func( actionFuncName, actId, actContent, tbActionFuncs, params )

	return params

# 技能导表parse_xls
def parse_ai_sheet(sh, path, tbCondition, tbTarget):
	srcCnd = ""

	for cndId in tbCondition:
		srcTmp = tbCondition[cndId]
		srcCnd += srcTmp

	srcTarget = ""
	for targetId in tbTarget:
		srcTmp = tbTarget[targetId]
		srcTarget += srcTmp

	

	for row in range(1, sh.nrows):
		#srcAITemplete
		aiId = get_str_from_sheet(sh, row, 0)
		if aiId == "":
			continue
		# 1 ai memo
		memo = get_str_from_sheet(sh, row, 1)
		# 2 ai class name
		aiClsName = "ClsAI" + upFirstChar(aiId)
		# 3 base attr funcs
		#   id
		funcId = srcStrData%(u"AI ID", "AIId", aiId)
		srcBaseAttrFuncs = funcId
		#   时机
		opportunity = get_str_from_sheet(sh, row, 2)
		if opportunity not in dicOpportunity:
			print(u"ERROR:unknow opportunity:" + opportunity)
			strOpportunity = "ERROR:" + opportunity
		else:
			strOpportunity = "@@" + dicOpportunity[opportunity]

		funcOpportunity = srcData%(u"AI时机", "Opportunity", PythonData2Lpc(strOpportunity))

		srcBaseAttrFuncs += funcOpportunity
		#   优先级别
		priority = get_int_from_sheet(sh, row, 3)
		funcPriority = srcIntData%(u"AI优先级别", "Priority", priority)
		srcBaseAttrFuncs += funcPriority

		# 停止标记
		stop_other_flg = get_int_from_sheet(sh, row, 4)
		funcStopOtherFlg = srcIntData%(u"AI停止标记",  "StopOtherFlg", stop_other_flg)
		srcBaseAttrFuncs += funcStopOtherFlg

		# 删除标记
		delete_other_flg = get_int_from_sheet(sh, row, 5)
		funcDeleteOtherFlg = srcIntData%(u"AI删除标记", "DeleteOtherFlg", delete_other_flg)
		srcBaseAttrFuncs += funcDeleteOtherFlg

		lstTarget = []
		lstCnd = []

		# 4 cnd funcs
		cnd = get_str_from_sheet(sh, row, 6)
		conditionSrc = ""
		if ( len (cnd) ):

			# 处理条件
			if ( cnd in tbCondition):
				cndFunName = "cnd" + upFirstChar(cnd)
				srcTmp = u'''\treturn %s(mpAI, 0)'''%cndFunName
				lstCnd.append(cnd)
			else:
				dicParam = {}
				exp = parse_expr_right(cnd, dicVar, 0, dicParam )
				#print("xxxxxxxxxxxxxx", cnd, exp)
				srcTmp = u'''\t%s\n\treturn (%s)'''%(exp[0], exp[1])

			conditionSrc = srcCheckConditionFunction%( srcTmp )


			#srcCnd += conditionSrc

		lstAct = []
		tbActionFuncs = {}
		index = 0
		for col in range( 7, sh.ncols, 3 ):
			# 5 target funcs
			target = get_str_from_sheet(sh, row, col)
			# 6 act funcs
			action = get_str_from_sheet(sh, row, col + 1)
			if ( len(action) == 0):
				continue
			# 7 actions
			action_content = get_str_from_sheet(sh, row, col + 2)

			# {"delay", "SELF", { 6000, }},
			tmpAction = [dicAction[action], "", [],]
			if (target in tbTarget ):
				tmpAction[1] = "@@target" + upFirstChar(target);
			else:
				tmpAction[1] = target;

			#TODO:parse action functions
			params = parse_action_function( aiId, index, action, action_content, tbActionFuncs )
			tmpAction[2] = params

			lstAct.append( tmpAction )
			index += 1

		srcActFuncs = ""
		for actFunctionName in tbActionFuncs: 
			srcActFuncs += tbActionFuncs[actFunctionName]

		dictTargetMethod = {}
		for targetMethod in tbTarget.keys():
			dictTargetMethod[targetMethod] = "@@target" + upFirstChar(targetMethod)

		aiSrc = srcAITemplete %(memo, srcBaseAttrFuncs, srcCnd + conditionSrc, srcTarget, srcActFuncs, PythonData2Lpc(lstAct, True, 1, 1), PythonData2Lpc(dictTargetMethod, True, 1, 1) )

		ai_str = ("/" +aiId+".c").encode(sys.getfilesystemencoding())
		#print(aiSrc)
		#print(path + ai_str) 
		#print(begin)
		#print(end)
		write_src(path + ai_str, begin, end, aiSrc, "utf-8")
		print(">>> [I] ai success write to "+ path + ai_str)

		#if ( aiId == "test"):
			#print(aiSrc)

def parse_enter_pos( sh, curLine, col ):
	enterPos = get_str_from_sheet( sh, curLine, col + 1 )
	return eval("[" + enterPos + "]") , curLine

def parse_int( sh, curLine, col ):
	intValue = get_int_from_sheet( sh, curLine, col + 1 ) 
	return int(intValue), curLine

def parse_string( sh, curLine, col ):
	strValue = get_str_from_sheet( sh, curLine, col + 1 ) 
	return strValue, curLine

def parse_string_array( sh, curLine, col ):
	strValue = get_str_from_sheet( sh, curLine, col + 1 ) 
	strArray = strValue.split(",")
	return strArray, curLine

headExp = re.compile(r"(?P<var_name>\w+)\((?P<var_type>\w+)\)")

# 从sh的curLine,startCol读出一个Table，同时
# 移动curLine,
# 头两行为Head
# 第一列为key
def parse_table( sh, curLine, startCol ):
	tb = {}
	row = curLine + 2
	if row >= sh.nrows:
		return tb, row;
	head = get_str_from_sheet( sh, row, startCol )
	while len(head) > 0:
		keyNameType = get_str_from_sheet( sh, curLine+1, startCol)
		tmp = headExp.match( keyNameType )
		var_name = tmp.group("var_name")
		var_type = tmp.group("var_type")

		if var_type == "int":
			key = get_int_from_sheet( sh, row, startCol)
		else:
			key = get_str_from_sheet( sh, row, startCol)

		curData = {}
		
		for col in xrange( startCol + 1, sh.ncols):
			nameType = get_str_from_sheet( sh, curLine+1, col)
			print(nameType)
			tmp = headExp.match( nameType )
			var_name = tmp.group("var_name")
			var_type = tmp.group("var_type")

			if var_type == "int":
				value = get_int_from_sheet( sh, row, col)
			else:
				value = get_str_from_sheet( sh, row, col)

			curData[var_name] = value

		print( curData )
		tb[key] = curData


		row = row + 1
		if row >= sh.nrows:
			break
		head = get_str_from_sheet( sh, row, startCol )

	return tb, row
	


dicParseTable = {
	u"副本属性":u"pass",
	u"副本名":(parse_string, u"FubenName"),
	u"副本ID":(parse_string, u"FubenId"),
	u"副本地图":(parse_int, u"BaseSceneId"),
	u"副本类型":(parse_int, u"FubenType"),
	u"进入方式":(parse_int, u"EnterMethod"),
	u"副本时长":(parse_int, u"FubenTime"),
	u"入口位置":(parse_enter_pos, u"EnterPos"),
	u"副本描述":(parse_string, u"FubenDesc"),
	u"副本AI":(parse_string_array, u"FubenAILst"),
	u"事件分发表":u"pass",
	u"事件序号":(parse_table, u"FubenDispatch" ),
	}


srcFubenTemplete = u"""
// 
#include <scene.h>

inherit MODULE_SCENE_FUBEN;

#include <var_prop.h>
#include <ai.h>

// ------------------------------------
// 属性区 
// ------------------------------------
%s
// ------------------------------------


"""

def parse_fuben_sheet(sh, path, tbAttr ):
	for row in range(0, sh.nrows):
		head = get_str_from_sheet(sh, row, 0)
		#print(head)
		if (len(head) == 0):
			continue;

		if head not in dicParseTable:
			continue;

		parseInfo = dicParseTable[head]
		if parseInfo == u"pass":
			continue

		#print( parseInfo )
		result = parseInfo[0](sh, row, 0)
		#print(result)
		tbAttr[parseInfo[1]] = { "data":result[0], "memo":head }
		row = result[1]
		#tbAttr.append( (passInfo[1], )

	srcAttr = u''
	for attrName in tbAttr:
		attrData = tbAttr[attrName]
		if ( attrName != u"FubenDispatch" ):
			srcAttr += (u'''
// %s
RESET_ONUPDATE_VAR( %s, %s )'''%(attrData["memo"], attrName, PythonData2Lpc(attrData["data"], True)))
		else:
			srcAttr += (u'''
// %s
mapping mpFubenDispatch = %s;
mapping GetFubenDispatch()
{
	return mpFubenDispatch;
}
'''%(attrData["memo"], PythonData2Lpc(attrData["data"], True)))
			

	src = srcFubenTemplete % srcAttr

	#print( src )
	#print( path + "../scene" )
	#print(tbAttr)
	fubenId = tbAttr[u"FubenId"]["data"];
	srcFile = path + "/../fuben/" + fubenId + ".c"
	#print( srcFile )
	write_src(srcFile, begin, end, src, "utf-8")

	


# 导整个表
def parse_xls(filename, shname, path):

	ai_path = path 
	
	try :
		# 打开excel文件
		book = xlrd.open_workbook(filename)
	except :
		msg = "can't open file?", filename
		print( msg, )
		usage()

		raise

	# 先处理变量表
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		sheetname = sh.name
		if sheetname == u"变量表":
			parse_var_sheet(sh, dicVar)
			break

	tbCondition = {}
	#处理条件表
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		sheetname = sh.name
		if sheetname == u"条件":
			parse_condition_sheet(sh, tbCondition)
			break

	tbTarget = {}
	#解析目标
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		sheetname = sh.name
		if sheetname == u"目标":
			parse_target_sheet(sh, tbTarget, tbCondition)
			break;

	#解析AI
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		sheetname = sh.name
		if sheetname == u"AI":
			parse_ai_sheet(sh, ai_path, tbCondition, tbTarget )
			break;
	
	for x in xrange(book.nsheets):
		sh = book.sheet_by_index(x)
		if sh.name == shname:
			tbAttr = {};
			parse_fuben_sheet(sh, ai_path, tbAttr )


	

if __name__ == "__main__":
	argv_len = len(sys.argv)
	if argv_len < 4:
		if argv_len > 1 and sys.argv[1].startswith('--'):
			option = sys.argv[1][2:]

			# fetch sys.argv[1] but without the first two characters
			if option == 'version':
				print 'Version 1.00'
			elif option == 'help':
				usage()
			else:
				usage()
			sys.exit()

		usage();
	else:
		if sys.argv[1].startswith('--'):
			option = sys.argv[1][2:]

			# fetch sys.argv[1] but without the first two characters
			if option == 'version':
				print 'Version 1.00'
			elif option == 'help':
				usage()
			else:
				usage()
			sys.exit()
		else:
			root_path = sys.argv[1]
			filename = sys.argv[2]
			shname = sys.argv[3].decode("utf-8")
			out_path = sys.argv[4]

			path = out_path

		#print( shname );
		#预处理部分代码
		parse_xls(filename, shname, path)

