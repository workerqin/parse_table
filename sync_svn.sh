#!/bin/sh
echo  "start up_svn "
LOGIC_ROOT="$1"
HOSTID="$2"
echo $LOGIC_ROOT
if [ "$LOGIC_ROOT" = "" ]; then
    echo "未输入工程路径"
    exit 0
fi

echo $HOSTID
if [ "$HOSTID" = "" ]; then
    echo "未输入服务器编号"
    exit 0
fi
echo  "LOGIC_ROOT "$LOGIC_ROOT
TARGET_DIR=$LOGIC_ROOT"/.svn_data"
PROJID="q3"
SVN_URL="http://192.168.16.145/repos/server_log/"$PROJID"/"$HOSTID
AUTH=" --username q3_log --password 175@game --no-auth-cache --non-interactive --trust-server-cert"

if [ ! -d $TARGET_DIR ] ; then # 不存在目标路径，需要从服务器上重新拉
    mkdir -p $TARGET_DIR
fi

echo $TARGET_DIR"/.svn" 
if [ ! -d $TARGET_DIR"/.svn" ] ; then
    svn checkout --force $AUTH $SVN_URL $TARGET_DIR >/dev/null 2>&1
    if [ $? == 1 ] ; then
        svn mkdir $AUTH $SVN_URL -m "Create new data folder for $HOSTID" >/dev/null 2>&1
        svn checkout $AUTH $SVN_URL $TARGET_DIR >/dev/null 2>&1
    fi
fi

# 暂不处理删除的表
#CLEAN_FILES=`find $TARGET_DIR -name '*.[ch]'` 
#if [ ! -z "$CLEAN_FILES" ] ; then 
#    echo $CLEAN_FILES | xargs rm 
#fi

cur_path=`pwd`
cd $LOGIC_ROOT
find -L . -path "./.svn_data" -type f -a -prune -o -name '*.[ch]'|grep -v "\.svn_data" | xargs grep -l 'Auto Generate Begin' | cpio -pdm --quiet $TARGET_DIR >/dev/null 2>&1

ADD_FILES=`svn status $TARGET_DIR | awk '{if($1=="?"){print $2}}'`
if [ ! -z "$ADD_FILES" ] ; then
    echo $ADD_FILES | xargs svn add
fi

echo $cur_path
cd $cur_path
RET=$(svn commit -m "提交导表更新" $AUTH $TARGET_DIR | wc -l)

echo $RET
exit $RET
