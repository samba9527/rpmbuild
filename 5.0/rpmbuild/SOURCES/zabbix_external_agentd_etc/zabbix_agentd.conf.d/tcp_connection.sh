#!/bin/sh

ss -ant | awk 'NR>1 {++s[$1]} END {for(k in s) print k,s[k]}' |grep $1 | awk '{print $2}'
