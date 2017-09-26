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
        echo 'graph_title OMSA - current power usage in Watt'
        echo 'graph_args --base 1000 -l 0'
        echo 'graph_vlabel Watt'
        echo 'graph_category sensors'
        echo 'PWR.label Power usage in W'
        exit 0
else
    VALUE=`$OMSA chassis pwrmonitoring | grep Reading | grep -v 'KWh' | grep -v 'Peak' | awk '{print $3}'`
    echo "PWR.value $VALUE" 
fi
