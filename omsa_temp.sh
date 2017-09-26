#!/bin/bash

OMSA="/opt/dell/srvadmin/bin/omreport"

if [ "$1" = "autoconf" ]; then
        if [ -e "$OMSA" ]; then
                echo yes
                exit 0
        else
                echo no
                exit 1
        fi
fi

if [ "$1" = "config" ]; then
        echo 'graph_title OMSA - System Board Inlet Temp'
        echo 'graph_args --base 1000 -l 0'
        echo 'graph_vlabel Celcius'
        echo 'graph_category sensors'
        echo 'TEMP.label Temperature in C'
        echo 'TEMP.warning 25'
        echo 'TEMP.critical 30'
        exit 0
else
    VALUE=`$OMSA chassis temps | grep Reading | head -1 | awk '{print $3}'`
    echo "TEMP.value $VALUE" 
fi
