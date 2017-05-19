
# -*- coding: utf-8 -*-

import string
import sys
import re

def write_file(filename, content ):

    msg = "writing file %s" %(filename)
    #print msg

    try :
        f = file(filename, "w+b")
    except :
        msg = "\rcan not write to " + filename
        print msg
        raise()
    #sys.exit(-1)
    #print "\r write file %s success"%(filename)
    f.write(content)
    f.close()

def read_file(filename, codeing ):
    tFile = open(filename)
    content = tFile.read( ).decode(codeing)

    return content

CSV_TABLE_TEMPLETE = u"""
.. csv-table:: %s
    :header: %s
    :widths: %s

%s
"""

u'''
title 表格标题
actionsList 表格数据
fieldIdx 表格字段顺序
allFieldsInfo 字段信息
'''
def GetCSVTable( title, tableData, fieldsIdx, allFieldsInfo ):

    head = u""
    widths = u""

    idx = 0
    for field in fieldsIdx:
        fieldInfo = allFieldsInfo[field]
        #print(fieldInfo)
        head = head + (u"\"%s\""%fieldInfo[u"field_name"]);
        widths =  widths + (u"%d"%fieldInfo[u"len"])
        idx = idx + 1
        if ( idx < len(fieldsIdx)):
            head = head + (u",")
            widths = widths + (u",")

    #print( head )
    allLines = u""
    for (actionId, fields) in tableData:

        line = u"    "
        idx = 0
        for field in fieldsIdx:
            fieldInfo = allFieldsInfo[field]
            fieldType = fieldInfo["data_type"]

            if fieldType == u"str":
                line = line + u"\"%s\""%fields[fieldInfo[u"data_idx"]]
            elif fieldType == u"int":
                line = line + u"%s"%fields[fieldInfo[u"data_idx"]]
            elif fieldType == u"float":
                line = line + u"%s"%fields[fieldInfo[u"data_idx"]]
            else:
                print("ERROR:unknow type:", fieldType)
            idx = idx + 1

            if ( idx < len(fieldsIdx)):
                line = line + u","

        allLines = allLines + line + "\n"


    strTable = CSV_TABLE_TEMPLETE%(title, head, widths, allLines)

    return strTable

FIGURE_TEMPLETE = u'''
.. plot::

    from report_common import draw_action_figure

    draw_action_figure(u"%s", u"%s", u"%s", u"%s")
'''


def GetFigure( dataFileName, xLabel, yLabel, title):
    return FIGURE_TEMPLETE%(dataFileName, xLabel, yLabel, title )


