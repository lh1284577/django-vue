#!/bin/bash

a=$1
echo $a
count=1
while true
do
        echo $count条测试数据
        sleep 1
        count=`expr $count + 1`
        if [ $count == 10 ]
        then
                exit 0
        fi
done
