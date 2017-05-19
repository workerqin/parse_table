
# -*- coding: utf-8 -*-

import os
import sys

from common import read_file
from common import GetCSVTable
from common import GetFigure

CODING = "utf-8"

u"""
报告生成程序

./data/stable_00001/
    all_action.ms  # 事务总括

    1                                         事务名    最大耗时(毫秒)  最小耗时(毫秒)  平均耗时(毫秒)   调用次数    成功   成功率      平均tps
    2                                      UserMove     3395431              1            137           7066748   3531414  49.972267%        16
    3                                     EnterArea        1246              8            166              1694       837  49.409679%         0
    4                                 UserHeartBeat         323              1             15             23570     23558  99.949089%         0
    5                                        NewUid           0              0              0              1513         0  0.000000%         0
    6                                      UserAuth         844              1             61              2025      2019  99.703705%         0
    7                                     UserLogin      410730             50          48965               446       393  88.116592%         0
    8                                       Version         842             22            113              2025      2025  100.000000%         0

    NewUid总括 ->> NewUid.action.sort action_NewUid.sort
    NewUid time -> 响应 action_NewUid


    CPU [netd gs userd]

    cpu_netd_[hostid]
    cpu_gs_[hostid]
    cpu_user_[hostid]

    MEMORY

    memory_netd_[hostid]
    memory_gs_[hostid]

    MONOGO

    monogodb_[hostid]

"""


#稳定测试报告模版
STABLE_TEMPLETE = "stable_templete.rst"

TEST_NO_KEY = u"%TEST_NO%"
TEST_DESC_KEY = u"%TEST_DESC%"
ALL_ACTION_TB_KEY = u"%ALL_ACTION_TABLE%"

STABLE_TEST_DESC = u"""
    这是一次稳定性测试,需要修改描述，到tools/server_profile/gen_report.py:51
"""



# 所有事务的输出结果
ALL_ACTION_FILE_NAME = "all_actions.ms"

ACTION_ID_IDX = 0
ACTION_MAX_MS = 1
ACTION_MIN_MS = 2
ACTION_AVG_MS = 3
ACTION_COUNT  = 4
ACTION_SUCC_CNT  = 5
ACTION_SUCC_RATE = 6
ACTION_AVG_TPS   = 7

allActionsFileds = (u"action_id", u"max_ms", u"min_ms", u"avg_ms", u"call_count", u"succ_count", u"succ_rate", u"avg_tps" )
allActionsTbDesc = {
    u"action_id":{
        u"len":20,
        u"field_name":u"事务名",
        u"data_idx": ACTION_ID_IDX,
        u"data_type": u"str",
    },
    u"max_ms":{
        u"len":12,
        u"field_name":u"最大耗时(ms)",
        u"data_idx": ACTION_MAX_MS,
        u"data_type": u"int",
    },
    u"min_ms":{
        u"len":12,
        u"field_name":u"最小耗时(ms)",
        u"data_idx": ACTION_MIN_MS,
        u"data_type": u"int",
    },
    u"avg_ms":{
        u"len":12,
        u"field_name":u"平均耗时(ms)",
        u"data_idx": ACTION_AVG_MS,
        u"data_type": u"int",
    },
    u"call_count":{
        u"len":12,
        u"field_name":u"调用次数",
        u"data_idx": ACTION_COUNT,
        u"data_type": u"int",
    },
    u"succ_count":{
        u"len":12,
        u"field_name":u"成功次数",
        u"data_idx": ACTION_SUCC_CNT,
        u"data_type": u"int",
    },
    u"succ_rate":{
        u"len":12,
        u"field_name":u"成功率",
        u"data_idx": ACTION_SUCC_RATE,
        u"data_type": u"float",
    },
    u"avg_tps":{
        u"len":12,
        u"field_name":u"平均TPS",
        u"data_idx": ACTION_AVG_TPS,
        u"data_type": u"float",
    },
}

ACTION_ANSWER_TIME_TEMPLETE = u"""

~~~~~~~~~~~~~~~~~~~~~~
%s 响应
~~~~~~~~~~~~~~~~~~~~~~

%s
"""


def GetAllActions( dataDir, keyIdx ):
    # TODO:读入所有的*.ms构建all_actions.ms

    allActions = {}

    allActionFileName = os.path.join(dataDir, ALL_ACTION_FILE_NAME)

    allActionsData = read_file(allActionFileName, CODING);

    allActionsDataList = allActionsData.split(u'\n')

    for anActionData in allActionsDataList:
        #print anActionData
        fields = anActionData.split(u',');

        id = fields[ACTION_ID_IDX].strip();
        #kprint id
        if ( id == u"事务名" ):
            continue
        if ( id == u"" ):
            continue

        allActions[id] = fields

    # 排序
    actionsList = sorted( allActions.items(), key=lambda item:item[1][keyIdx], reverse = True);

    allActionsStr = GetCSVTable( u"事务响应概述", actionsList, allActionsFileds, allActionsTbDesc);

    return actionsList, allActionsStr


def GenStableReport(workDir, dataRootDir, reportRootDir, number):

    # 切换工作路径
    os.chdir(workDir)

    # 测试编号
    testNO = "stable_%d"%number

    # 数据目录
    dataDir = os.path.join(dataRootDir, testNO)
    # 报告路径
    reportDir = os.path.join(reportRootDir, testNO)

    # 读入模版
    templete = read_file( STABLE_TEMPLETE, CODING)

    src = templete.replace(TEST_NO_KEY, testNO)
    src = src.replace(TEST_DESC_KEY, STABLE_TEST_DESC)

    # 读入全事务
    actionsList, allActionsStr  = GetAllActions( dataDir, ACTION_AVG_TPS )
    #print( actionsList )
    #print( allActionsStr )

    # TODO:每个事务的详情
    # 事务响应时长分布

    actionsAnswerTimeRst = u""

    for (actionId, fields)in actionsList:
        # ACTION_ANSWER_TIME_TEMPLETE
        dataFileName = os.path.join(dataDir, u"%s.action"%actionId );

        xLabel = u"cost time(ms)"
        yLabel = u"%s count"%actionId
        title = u"%s"%actionId

        srcFigure = GetFigure( dataFileName, xLabel, yLabel, title )

        actionsAnswerTimeRst = actionsAnswerTimeRst + srcFigure
        
        #print actionId

    src = src.replace(ALL_ACTION_TB_KEY, allActionsStr + actionsAnswerTimeRst )


    

    # 构建事务列表
    print(src)

    # TODO：输出报告，将必要文件移动到目标目录
    # *.actions

if __name__ == "__main__":
    GenStableReport( "./tools/server_profile/", "/home/prophet/q3/logic/tools/server_profile/data/", "/home/prophet/q3/logic/tools/server_profile/report/", 1 );
