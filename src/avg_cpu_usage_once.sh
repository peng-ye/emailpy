#!/usr/bin/bash
interval=30
times=10

if [ ! -z "$1" ] && [ ! -z "$2" ]; then
	interval="$1"
	times="$2"
fi

minutes=$(($interval*$times/60))

stat=`mpstat $interval $times | tail -1 | perl -lane '$_=$1 if /all\s+(\S+)/; print'`
echo -e "Average CPU usage (%) in the past $minutes minutes (interval = ${interval}s): $stat"
