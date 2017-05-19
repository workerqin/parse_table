#!/bin/bash

mkdir -p rpc_files

rpc_dir=../rc/rpc_decl
output=rpc_files
output_src=$output/src
output_decl=$output/decl

mkdir -p $output_src
mkdir -p $output_decl

for file in `ls $rpc_dir | grep ".decl$"`; do   #获取所有decl文件名
	path="$rpc_dir/$file"
	for str in $(grep ^imp $path | cut -d " " -f 2 | tr "." "/"); do   #wanfa/ability/main{
		rpc_file=../${str/\{/}.c         #rpc_file = ../wanfa/ability/main.c
		if ! [ -f $rpc_file ]; then
			echo -e "[warning] \033[32m$rpc_file \033[0m in $path is not exist!"
			continue
		fi
		rpc_file_dir=$(dirname $rpc_file|cut -d "/" -f 2-) #../wanfa/ability ==> wanfa/ability
		rpc_file_output=$output_src/$rpc_file_dir          #rpc_files/src/wanfa/ability
		mkdir -p $rpc_file_output
		cp $rpc_file $rpc_file_output
	done

	cp $rpc_dir/$file $output_decl
done

tar czvf rpcPacket.tar.gz  $output
rm -rf $output
echo -e "\033[33m ok! \033[0m"
