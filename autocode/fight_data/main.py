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
from common import safe_cmd

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
        u"跟随":"follow",
        }

# 文件路径
dicFilePath = {
        u"普通战役":"data/battle/%s.c",
        u"精英战役":"data/battle/%s.c",
        u"PVE":"data/battle/%s.c",
        }

# 文件继承路径
dicBase = {
        u"普通战役":"FIGHT_DATA_BASE",
        u"精英战役":"FIGHT_DATA_BASE",
        u"PVE":"FIGHT_DATA_PVE",
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

def get_action_follow_function( actionFuncName, actId, actContent, tbActionFuncs, params ):
    lstTmp = actContent.split(",")

    iRange = int(lstTmp[0])

    time = 0
    if len(lstTmp) > 1:
        time = int(lstTmp[1]);

    params.append( iRange )
    params.append( time )



# action内容解析
dicActionContentParse = {
        u"延迟":get_action_delay_function,
        u"执行AI":get_action_run_ai_function,
        u"设置":get_action_set_function,
        u"打印":get_action_print_function,
        u"跟随":get_action_follow_function,
        }

# TODO:公用变量表

# 变量表

dicVar = {}

begin = u"//----------------------- Auto Genrate Begin --------------------"
end   = u"//----------------------- Auto Genrate End   --------------------\n"

srcSceneDataTemplete = u'''
static mapping localSceneData = %s;
RESET_ONUPDATE_VAR(SceneData, localSceneData)
'''

srcShipDataTemplete = u'''
static mapping localShipsData = %s;
RESET_ONUPDATE_VAR(Ships, localShipsData)
'''

srcFightDataTemplete = u'''
#include <fight.h>

inherit %s;

#include <var_prop.h>

// --------------------------
// 属性区域
%s
// --------------------------

// --------------------------
// 函数区域
%s
// --------------------------


// SceneData
%s

// Ships
%s
'''

srcAITemplete = u'''

// 自动生成AI,来源于[%s]

#include <ai.h>

inherit AI_BASE;

#include <var_prop.h>
#include <scene.h>
#include <user_key.h>
#include <fight.h>
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

srcFormulaFunction = u'''
// [备注]%s
int %s( mapping fight, mapping mpOwner, mapping srcData, int lv)
{
    %s	
    // %s
    float result = %s;	
    return to_int(result);
}
'''



# 使用方法
def usage():
    print '''
    USAGE:python main.py root_path ai.xls
          --version : Prints the version number
          --help    : Display this help
    ex: python main.py /cygdrive/d/dhh_client/client 战斗数值.xls '''


def add_to_file(filename, content):
    try :
        f = file(filename, "a+b")
    except :
        sys.exit(-1)
    f.write(content + "\n")
    f.close()

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

# 建立公用变量表
def parse_common_var(filename, dicVar):
    try :
        # 打开excel文件
        book = xlrd.open_workbook(filename)
    except :
        msg = "can't open file?", filename
        print( msg )
        raise

    # 先处理变量表
    for x in xrange(book.nsheets):
        sh = book.sheet_by_index(x)
        sheetname = sh.name
        if sheetname == u"服务器端变量表":
            parse_var_sheet(sh, dicVar)
            break


# 导整个表
def parse_xls(filename, parseAIFlg):

    ai_path = "data/ai/" 

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
        if sheetname == u"服务器端变量表":
            parse_var_sheet(sh, dicVar)
            break

    tbCondition = {}
    tbTarget = {}

    if parseAIFlg == u"1":
        #处理条件表
        for x in xrange(book.nsheets):
            sh = book.sheet_by_index(x)
            sheetname = sh.name
            if sheetname == u"条件":
                parse_condition_sheet(sh, tbCondition)
                break

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
                #暂时屏蔽AI
                parse_ai_sheet(sh, ai_path, tbCondition, tbTarget )
                break;

    formula = None
    hasPlot = False
    cehuaDecideWin = 0
    #for x in xrange(book.nsheets):
    #	sh = book.sheet_by_index(x)
    #	if sh.name == shname:
    #		tbAttr = {};
    #		#parse_fuben_sheet(sh, ai_path, tbAttr )
    # 遍历xls
    for x in xrange(book.nsheets):
        sh = book.sheet_by_index(x)
        sheetname = sh.name
        if sheetname == u"battle_scene":
            battle_id = common.get_str_from_sheet(sh, 0, 1);
            battle_type = common.get_str_from_sheet(sh, 0, 3);
            # 策划决定战斗胜利
            cehuaDecideWin = common.get_int_from_sheet(sh, 0, 5);
            # 玩家入场ai_list和x，y，dir
            player_ai_list = common.get_str_array_from_sheet(sh, 1, 1);
            player_x = common.get_int_from_sheet(sh, 1, 2)
            player_y = common.get_int_from_sheet(sh, 1, 3)
            player_dir = common.get_int_from_sheet(sh, 1, 4)
            target_dir = common.get_int_from_sheet(sh, 1, 5)
            scene_id = common.get_int_from_sheet(sh, 2, 1)
            # 场景AI
            scene_ai_list = common.get_str_array_from_sheet(sh, 2, 3);
            # 战斗时长
            fight_timeout = common.get_int_from_sheet(sh, 2, 5)
            reward = common.get_str_array_from_sheet(sh, 4, 1)
            level_type = common.get_int_from_sheet(sh, 4, 3);
            # 敌方入场数据
            scene_data, row_line = common.parse_table(sh, 5, 0)
            print "row_line:", row_line
            if (row_line == sh.nrows):
                continue;
            # 公式数据
            srcTmp = common.get_str_from_sheet(sh, row_line, 0); 

            # 寻找公式
            while srcTmp != u"公式" and row_line < sh.nrows:
                srcTmp = common.get_str_from_sheet(sh, row_line, 0); 
                row_line = row_line + 1

            if (row_line == sh.nrows):
                continue;
            # 公式数据
            formula, row_line = common.parse_table(sh, row_line, 0)

        if sheetname == u"ships":
            # 敌方入场数据
            ships, row_line = common.parse_table(sh, 0, 0)
        if sheetname == u"plot":
            hasPlot = True 

    if ( hasPlot ):
        plotId = int(battle_id)
    else:
        plotId = 0;

    if not scene_data:
        return

    srcAttribute = u''
    lstAttribute = []
    if player_ai_list and (len(player_ai_list) >= 1):
        lstAttribute.append( ("str_array", u"玩家AI", "AI", player_ai_list ) )
    if scene_ai_list and (len(scene_ai_list) >= 1):
        lstAttribute.append( ("str_array", u"场景AI", "SceneAI", scene_ai_list ) )
    # fight_timeout
    # FightTimeout
    if fight_timeout and ((fight_timeout) >= 60):
        lstAttribute.append( ("int", u"战斗时长", "FightTimeout", fight_timeout) )
    lstAttribute.append( ("int", u"玩家X", "UserX", player_x) )
    lstAttribute.append( ("int", u"玩家Y", "UserY", player_y) )
    lstAttribute.append( ("int", u"玩家Dir", "UserDir", player_dir) )
    lstAttribute.append( ("int", u"舰队Dir", "FleetDir", target_dir) )
    lstAttribute.append( ("int", u"地图ID", "SceneId", scene_id) )
    lstAttribute.append( ("int", u"策划决定战斗胜利", "CehuaDecideWin", cehuaDecideWin ) )
    if level_type:
        lstAttribute.append( ("int", u"等级类型", "LevelType", level_type) )
    if reward and (len(reward) >= 1):
        lstAttribute.append( ("str_array", u"奖励", "Reward", reward) )

    if hasPlot :
        lstAttribute.append( ("int", u"剧情ID", "PlotId", plotId) ) 
    for attr in lstAttribute:
        type = attr[0]
        memo = attr[1]
        param = attr[2]
        value = attr[3]
        srcTmp = u''
        if type == "int":
            srcTmp = srcIntData%(memo, param, value)
        elif type == "str_array":
            srcTmp = srcData%(memo, param, PythonData2Lpc(value) )

        srcAttribute += srcTmp

    baseName = dicBase[battle_type]
    srcFunctions = u""
    formulaResult = {}
    if formula:
        for k, v in formula.items():
            formula_name = "formula_%s"%k
            dicParam = {}
            exp = parse_expr_right(v["formula"], dicVar, 0, dicParam )
            #srcFunc = parse_function( v["formula"], formula_name, formula_name, dicVar, srcFormulaFunction )
            srcFunc = srcFormulaFunction%(v["memo"], formula_name, exp[0], v["formula"], exp[1])
            srcFunctions += srcFunc 
            formulaResult[k] = u"@@%s"%formula_name

    for k, v in ships.items():
        for fk, fn in formulaResult.items():
            if v.has_key(fk):
                v[fk] = fn
    srcSceneData = srcSceneDataTemplete%( PythonData2Lpc( scene_data, True, 1, 1 ) );
    srcShipData = srcShipDataTemplete%( PythonData2Lpc( ships, True, 1, 1 ) );
    srcFightData = srcFightDataTemplete%(baseName, srcAttribute, srcFunctions, srcSceneData, srcShipData )

    srcPath = (dicFilePath[battle_type])%(battle_id)

    print formula 
    #TODO:输出scene_data，ships
    write_src(srcPath, begin, end, srcFightData, "utf-8")
    add_to_file("tmp/update_file.txt", srcPath)

    #safe_cmd("echo '%s' >> etc/autoupdate"%srcPath);

if __name__ == "__main__":
    argv_len = len(sys.argv)
    if argv_len < 3:
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
            parseAIFlg = sys.argv[3]
            #shname = sys.argv[3].decode("utf-8")
            #out_path = sys.argv[3]

        commonVarXls = "tools/autocode/fight_data/AITemp.xls"
        parse_common_var( commonVarXls, dicVar );
        #print( shname );
        #预处理部分代码
        parse_xls(filename, parseAIFlg)

