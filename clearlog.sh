#!/bin/sh 

function clearLog()
{
	cd  ~
	ALL_LOG=`find . -name "*.log"`
	
	for log in $ALL_LOG
	do
		echo "clear"$log
		truncate $log --size=0
	done
}

function clearEngine()
{
	cd ~

	ALL_ENGINE=`find . -name "nohup*"`

	for eng in $ALL_ENGINE
	do
		echo "clear"$eng
		truncate $eng --size=0
	done
}

clearEngine
clearLog

