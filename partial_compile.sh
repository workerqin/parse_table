#!/usr/bin/env bash
if [ -d ".git" ];then
	change_files=`git status -s|grep "[MA]"|grep "\.c"|awk '{print $2}'`
else
	change_files=`svn status -q|grep "[MA]"|grep "\.c"|awk '{print $2}'`
fi	
for file in $change_files
do
	echo $file
	../engine/lpc -c $file
done
