#!/bin/sh

target=(team1 team2 move1 move2 move3 move4 mission1 mission2 fight50 fight60)

for val in ${target[@]}
do
	make $val
	sleep 40
done

