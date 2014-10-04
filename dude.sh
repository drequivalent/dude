#!/bin/bash

IFS=$'\n'
lines1=($(diff --changed-group-format='%<' --unchanged-group-format='' $1 $2))

lines2=$(diff --changed-group-format='%>' --unchanged-group-format='' $1 $2)

function difference {
        unset IFS
        for ((i=0; i < ${#lines1[*]}; i++)) do
                LINE1_DIR=$(echo ${lines1[i]} | cut -d " " -f 2)
                LINE1_SIZE=$(echo ${lines1[i]} | cut -d " " -f 1)
                LINE2=`echo "$lines2" | grep -w $LINE1_DIR$`
                LINE2_DIR=`echo $LINE2 | cut -d " " -f 2`
                LINE2_SIZE=`echo $LINE2 | cut -d " " -f 1`
                DIFFERENCE=`expr $LINE2_SIZE - $LINE1_SIZE 2>/dev/null || echo C`
                        echo "$DIFFERENCE             $LINE1_SIZE           $LINE2_SIZE                         $LINE1_DIR"
        done
}

difference $1 $2
