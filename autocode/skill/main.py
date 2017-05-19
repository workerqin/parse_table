
# -*- coding:utf-8 -*-

import os
import re
import xlrd
import string
from common import get_str_from_sheet
from common import get_str_array_from_sheet
from common import get_int_from_sheet
from common import write_src
from common import parse_function
from common import formla_int_to_float
from Python2Lpc import PythonData2Lpc

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


dicVar = {}

# 使用方法
def usage():
        print '''
        USAGE:python main.py root_path skill.xls sheet_name output_path
          --version : Prints the version number
          --help    : Display this help
'''

begin = u"//----------------------- Auto Genrate Begin --------------------\n"
end = u"//----------------------- Auto Genrate End   --------------------\n"

attrTemplete = u"""
// %s
RESET_ONUPDATE_VAR(%s, %s)
"""

srcStatusRateTemplete = u"""
// %s
int %s(mapping fight, mapping attShipInfo, mapping tagShipInfo, int lv)
{
    int result;
    %s
    return result;
}
"""

srcSelectCntTemplete = u"""
// %s
int %s(mapping fight, mapping attShipInfo, int lv)
{
    int result;
    %s
    return result;
}
"""



srcStatusCalcTemplete = u"""
// %s
mapping %s(mapping fight, mapping attShipInfo, mapping tagShipInfo, int lv, mapping mpResult)
{
    %s
    return mpResult;
}
"""



srcStatusDurationTemplete = u"""
// %s
int %s(mapping fight, mapping attShipInfo, mapping tagShipInfo, int lv)
{
    return %s
}
"""

srcStatusBreakTemplete = u"""
// %s
float %s(mapping fight, mapping attShipInfo, mapping tagShipInfo, int lv)
{
    return %s
}
"""




def GetSrcByType(headMemo, type, name, sh, row, col, templete):
    src = ""
    if ( type == "int"):
        value = get_int_from_sheet( sh, row, col )
        src = templete%(headMemo, name, PythonData2Lpc(value))
    elif ( type == "str"):
        value = get_str_from_sheet( sh, row, col )
        src = templete%(headMemo, name, PythonData2Lpc(value))
    elif type == "str_array":
        value = get_str_array_from_sheet( sh, row, col )
        src = templete%(headMemo, name, PythonData2Lpc(value))
    elif type == "status_array":
        tmp = get_str_array_from_sheet( sh, row, col)
        for idx in range(len(tmp)):
            if ( tmp[idx] in statusName2Id ):
                tmp[idx] = statusName2Id[tmp[idx]]
        value = tmp
        src = templete%(headMemo, name, PythonData2Lpc(value))
    elif type == "macro":
        value = get_str_from_sheet( sh, row, col )
        if ( len(value) == 0):
            return src
        src = templete%(headMemo, name, value)
        print("xxxxxxx: src = ", src)
    elif type == "function":
        value = get_str_from_sheet( sh, row, col )
        if ( len(value)):
            #print(value)
            #print( dicVar )
            src = parse_function( value, headMemo, name, dicVar, templete )
    else:
        value = get_str_from_sheet( sh, row, col )
        src = templete%(headMemo, name, PythonData2Lpc(value))
       
    #srcSkill += templete%headMemo, name, PythonData2Lpc(value))
    return src


# 技能变量策划使用表的解析
def parse_var_sheet(sh, dicVar):
    for row in range(1, sh.nrows):
        key = ""
        for col in range(0, sh.ncols):
            head = get_str_from_sheet(sh, 0, col)

            print( head );
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

statusName2Id = {}
statusRelation = {}
def parse_status_relation_sheet(sh, dicVar):
    headRow = 2
    headCol = 2
    for row in range(3, sh.nrows):
        for col in range(3, sh.ncols):
            relation = get_int_from_sheet( sh, row, col)
            if ( relation == 0):
                continue
            status = get_str_from_sheet( sh, row, headCol)
            targetStatus = get_str_from_sheet( sh, headRow, col)

            if status not in statusRelation:
                statusRelation[status] = {
                        "exclude":[],
                        "overwrite":[],
                        }
            if ( relation == 1):
                statusRelation[status]["exclude"].append(targetStatus)
            if ( relation == 2):
                statusRelation[status]["overwrite"].append(targetStatus)

# status_name   status_type status_desc status_effect   status_effect_type  affect_effect_statusT   affect_effect_statusA   calculate_idx   status_icon status_prompt
parseStatusTable = {
        u"status_name":{"type":"str", "value_name":"StatusName", "templete":attrTemplete,},
        u"status_type":{"type":"str", "value_name":"StatusType", "templete":attrTemplete,},
        u"status_desc":{"type":"str", "value_name":"StatusDesc", "templete":attrTemplete,},
        u"status_effect":{"type":"str", "value_name":"StatusEffect", "templete":attrTemplete,},
        u"status_effect_type":{"type":"str", "value_name":"StatusEffectType", "templete":attrTemplete,},
        u"status_icon":{"type":"str", "value_name":"StatusIcon", "templete":attrTemplete,},
        u"status_prompt":{"type":"str", "value_name":"StatusPrompt", "templete":attrTemplete,},
        u"affect_effect_statusA":{"type":"str_array", "value_name":"AffectStatusA", "templete":attrTemplete,},
        u"affect_effect_statusT":{"type":"str_array", "value_name":"AffectStatusT", "templete":attrTemplete,},
        u"calculate_idx":{"type":"int", "value_name":"CalculateIdx", "templete":attrTemplete,},
    }

def parse_status_sheet(sh, dicVar):
    idCol = 0
    headRow = 1
    for row in range(2, sh.nrows):
        status = get_str_from_sheet( sh, row, idCol)
        print status
        srcStatus = u"""
#include <fight.h>

inherit STAUTS_BASE;

#include <var_prop.h>
#include <user_key.h>

// 状态ID
RESET_ONUPDATE_VAR(StatusId, "%s")

"""%(status)
        for col in range(1, sh.ncols):
            headMemo = get_str_from_sheet( sh, 0, col)
            head = get_str_from_sheet( sh, 1, col)
            type = parseStatusTable[head]["type"]
            name = parseStatusTable[head]["value_name"]
            templete = parseStatusTable[head]["templete"]

            srcStatus += GetSrcByType( headMemo, type, name, sh, row, col, templete )

            if ( head == "status_name" ):
                value = get_str_from_sheet( sh, row, col)
                statusName2Id[value] = status;

        if (status in statusRelation):
            #状态关系表
            #ExcludeStatus
            #OverwriteStatus
            srcStatus += u"""
// 排斥状态
RESET_ONUPDATE_VAR(ExcludeStatus, %s)
"""%(PythonData2Lpc(statusRelation[status]["exclude"]))
            srcStatus += u"""
// 覆盖状态
RESET_ONUPDATE_VAR(OverwriteStatus, %s)
"""%(PythonData2Lpc(statusRelation[status]["overwrite"]))
        statusFile = "module/fight/status/%s.c"%status;

        write_src( statusFile, begin, end, srcStatus, u"utf-8")
        
skillSimpleFuncTemplete = u"""
// %s
int %s(mapping fight, mapping attShipInfo, int lv)
{
    int result;
    %s
    return result;
}
"""

parseSkillTable = {
        # 技能ID
        u"skill_id":{"type":"str", "value_name":"SkillId", "templete":attrTemplete, },
        # 技能类型
        u"skill_type":{"type":"str", "value_name":"SkillType", "templete":attrTemplete,},
        # 技能系别
        u"skill_series":{"type":"str", "value_name":"SkillSeries", "templete":attrTemplete,},
        # 技能名
        u"skill_name":{"type":"str", "value_name":"SkillName", "templete":attrTemplete,},
        # common_cd
        u"common_cd":{"type":"int", "value_name":"CommonCD", "templete":attrTemplete,},
        # 技能CD
        u"skill_cd":{"type":"function", "value_name":"SkillCD", "templete":skillSimpleFuncTemplete,},
        # 技能自动施放几率
        u"skill_rate":{"type":"function", "value_name":"SkillRate", "templete":skillSimpleFuncTemplete,},
        # status_limit
        u"status_limit":{"type":"status_array", "value_name":"StatusLimit", "templete":attrTemplete,},
        # 目标选择
        u"select_scope":{"type":"macro", "value_name":"SelectScope", "templete":attrTemplete,},
        # 
        u"min_limit_distance":{"type":"function", "value_name":"MinLimitDistance", "templete":skillSimpleFuncTemplete,},
        u"max_limit_distance":{"type":"function", "value_name":"MaxLimitDistance", "templete":skillSimpleFuncTemplete,},
        # 施法清除状态
        u"skill_clear_status":{"type":"status_array", "value_name":"SkillClearStatus", "templete":attrTemplete,},
        # 施法触发状态
        u"skill_active_status":{"type":"status_array", "value_name":"SkillActiveStatus", "templete":attrTemplete,},
    }



def parse_skill_sheet(sh, output_path):
    #print( "xxxxxxxxxxxxxxxxxxxx\n", statusName2Id )
    statusStartCol = 26
    statusColCnt = 13
    # 导技能表
    # parseSkillTable
    for row in range(3, sh.nrows):
        skillId = get_str_from_sheet( sh, row, 0)
        srcSkill = u"""
#include <fight.h>

inherit SKILL_BASE;

#include <var_prop.h>
#include <user_key.h>
#include <skill.h>

"""
        skillFile = "module/skill/"+ skillId+".c"
        for col in range( 0, statusStartCol - 1):
            headMemo = get_str_from_sheet( sh, 1, col)
            head = get_str_from_sheet( sh, 2, col)
            if ( head not in parseSkillTable ):
                continue;
            type = parseSkillTable[head]["type"]
            name = parseSkillTable[head]["value_name"]

            templete = parseSkillTable[head]["templete"]
            print( headMemo, type, name, sh, row, col, templete)
            srcSkill += GetSrcByType( headMemo, type, name, sh, row, col, templete )
        
        statusIdx = 0
        allStatus = [];
        # TODO:操作区解析
        for col in range( statusStartCol, sh.ncols, statusColCnt):
            head = get_str_from_sheet( sh, 2, col)

            # TODO:根据列名逐个获取内容


            curCol = col;
            # 无法完整的读出一个状态
            if curCol + statusColCnt > sh.ncols:
                break;
            # pre_actions
            curCol = curCol + 1;
            # scope
            value = get_str_from_sheet( sh, row, curCol)
            print(head, value)

            if len( value ) == 0:
                continue
            status = {}

            print(curCol, value );
            status["@@SCOPE"] = "@@" + value
            # sort_method
            curCol = curCol + 1;
            value = get_str_from_sheet( sh, row, curCol)
            if ( len(value) > 0):
                status["@@SORT_METHOD"] = "@@" + value
            # select_cnt
            curCol = curCol + 1;
            value = get_str_from_sheet( sh, row, curCol)
            if "=" not in value:
                print row, col, value
                value = get_int_from_sheet( sh, row, curCol)
                status["@@SELECT_CNT"] = value
            else:
                funcName = "StatusSelectCnt%d"%(statusIdx);
                statusSelectCnt = parse_function( value, u"状态选择数量", funcName, dicVar, srcSelectCntTemplete)
                srcSkill += statusSelectCnt;
                status["@@SELECT_CNT"] = "@@" + funcName

            # TargetUnselectMain
            curCol = curCol + 1;
            tmp = get_str_array_from_sheet( sh, row, curCol)
            for idx in range(len(tmp)):
                if ( tmp[idx] in statusName2Id ):
                    tmp[idx] = statusName2Id[tmp[idx]]
            value = tmp
            status["@@UNSELECT_MAIN"] = value
            # effect_name
            curCol = curCol + 1;
            # effect_type
            curCol = curCol + 1;
            # effect_time
            curCol = curCol + 1;
            # StatusAdd
            curCol = curCol + 1;
            value = get_str_from_sheet( sh, row, curCol)
            if ( value in statusName2Id ):
                value = statusName2Id[value];
            status["@@STATUS_ADD"] = value
            # status_duration
            curCol = curCol + 1;
            value = get_str_from_sheet( sh, row, curCol)
            if (len(value) > 0):
                if "=" in value:
                    funcName = "StatusDuration%d"%(statusIdx);
                    statusDuration = parse_function( value, u"状态持续时间", funcName, dicVar, srcStatusRateTemplete)
                    srcSkill += statusDuration;
                    status["@@STATUS_DURATION"] = "@@" + funcName
                elif "+" in value:
                    funcName = "StatusDuration%d"%(statusIdx);
                    statusDuration = parse_function( value, u"状态持续时间", funcName, dicVar, srcStatusDurationTemplete)
                    srcSkill += statusDuration;
                    status["@@STATUS_DURATION"] = "@@" + funcName
                elif "/" in value:
                    funcName = "StatusDuration%d"%(statusIdx);
                    statusDuration = parse_function( value, u"状态持续时间", funcName, dicVar, srcStatusDurationTemplete)
                    srcSkill += statusDuration;
                    status["@@STATUS_DURATION"] = "@@" + funcName
                else:
                    print value
                    status["@@STATUS_DURATION"] = get_int_from_sheet( sh, row, curCol)
            # status_break
            curCol = curCol + 1;
            value = get_str_from_sheet( sh, row, curCol)
            if ( len(value) > 0 ):
                funcName = "StatusBreak%d"%(statusIdx);
                value = formla_int_to_float(value);
                statusBreak = parse_function( value, u"状态心跳时间", funcName, dicVar, srcStatusBreakTemplete)
                srcSkill += statusBreak;
                status["@@STATUS_BREAK"] = "@@" + funcName
            # 命中率公式
            curCol = curCol + 1;
            # skillSimpleFuncTemplete
            value = get_str_from_sheet( sh, row, curCol)
            funcName = "StatusRate%d"%(statusIdx);
            status["@@STATUS_RATE"] = "@@" + funcName
            # 生成函数，加入技能表中去
            statusRate = parse_function( value, u"状态命中", funcName, dicVar, srcStatusRateTemplete)
            srcSkill += statusRate;
            # 处理过程
            curCol = curCol + 1;
            value = get_str_from_sheet( sh, row, curCol)
            funcName = "StatusCalc%d"%(statusIdx);
            status["@@STATUS_CALCULATE"] = "@@" + funcName
            statusCalc = parse_function( value, u"状态结算", funcName, dicVar, srcStatusCalcTemplete)
            srcSkill += statusCalc;

            print(status)
            allStatus.append( status )
            # 状态操作区+1
            statusIdx = statusIdx + 1

        # status
        srcSkill += u"""
mapping* allStatus = %s;
mapping* GetAllStatus()
{
    return allStatus;
}
"""%( PythonData2Lpc(allStatus, True, 0) )


        # 非操作区的处理
        write_src( skillFile, begin, end, srcSkill, u"utf-8")

    pass



# 导表
def parse_xls(filename, sn, path):
    try :
        # 打开excel文件
        book = xlrd.open_workbook(filename)
    except :
        msg = "can't open file?", filename
        #my_echo( msg, dictDebugLevel.get("ERROR") )
        print msg
        usage()
        raise

    # 先处理变量表
    for x in xrange(book.nsheets):
        sh = book.sheet_by_index(x)
        sheetname = sh.name
        print( "sheetname", sheetname );
        if sheetname == u"服务器端变量表":
            parse_var_sheet(sh, dicVar)
            break
    # 再处理状态关系表
    for x in xrange(book.nsheets):
        sh = book.sheet_by_index(x)
        sheetname = sh.name
        print( "sheetname", sheetname );
        if sheetname == u"状态关系表":
            parse_status_relation_sheet(sh, dicVar)
            break

    # 再处理状态表
    for x in xrange(book.nsheets):
        sh = book.sheet_by_index(x)
        sheetname = sh.name
        print( "sheetname", sheetname );
        if sheetname == u"状态表":
            parse_status_sheet(sh, dicVar)
            break

    print("sn", sn);
    # 然后处理技能表
    for x in xrange(book.nsheets):
        sh = book.sheet_by_index(x)
        sheetname = sh.name
        if sheetname == sn:
            parse_skill_sheet(sh, path)
            break



if __name__ == "__main__":
    argv_len = len(sys.argv)
    if argv_len < 3:
        usage();
    else:
        # 根路径
        root_path = sys.argv[1]
        # 文件名
        filename = sys.argv[2]
        # sheet名
        sheetname = sys.argv[3]
        # 技能输出路径
        out_path = sys.argv[4]
        parse_xls(filename, sheetname, out_path)

