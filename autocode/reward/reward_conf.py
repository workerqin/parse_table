# -*- coding: utf-8 -*-

SRC_TEMPLATE = """
mapping mpItem = ([ 
{%for item in table.Cols%} \
{%if item.NAME %} \
	{% if meta.xxxx%}
	{% if meta.udata....%}
	{{item.ROW}}:([ \
"Name":"{{item.NAME}}" \
{%if item.AMOUNT%}"amount":{{item.AMOUNT}},{%endif%} \
{%if item.ATTRIB%}"attrib":"{{item.ATTRIB}}",{%endif%} \
{%if item.RATE%}"rate":{{item.RATE}},{%endif%} \
{%if item.GROSS%}"gross":{{item.GROSS}},{%endif%} \
{%if item.VALUABLE%}"valueable":{{item.VALUABLE}},{%endif%} \
{%if item.VALUEABLE%}"perlimit":{{item.VALUEABLE}},{%endif%} \
{%if item.ANNOUNCE%}"announce":"{{item.ANNOUNCE}}",{%endif%} \
]),\
{%endif%}
{%endfor%}\
])

int life = {{life}};
string default = "{{default1}}";

"""

udata = {
	"life" : {"row":4, "col":1, }, 
	"default" : {"row":4, "col":3, },
	}

table_meta = {
	"TitleRow": 5,           #描述的列
	"NotParseSheet": [u"说明", ],
	#"Template": "./reward.template",
	"OutPutFile": "./test.c",
	"udata" = udata
	}


