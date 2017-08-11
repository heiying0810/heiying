#!/bin/bash
IFS=`echo -en "\n\b"`
aa=1
while read line ;do
	lie=`echo $line|awk -F'\t+' '{print NF}'`
	phone=`echo $line|awk -F'\t+' '{print $1}'`
	city=`echo $line|awk -F'\t+' '{print $2}'`
	tel=`echo $line|awk -F'\t+' '{print $3}'`
	num1=`echo $line|awk -F'\t+' '{print $4}'`
	num2=`echo $line|awk -F'\t+' '{print $5}'`
	num3=`echo $line|awk -F'\t+' '{print $6}'`
	if [ $lie == 5 ] ;then
		expr $num1 + $num2 >/dev/null 2>&1
		if [[ -n $phone && -n $city && -n -$tel && -n -$num1 && -n $num2 && $? == 0 ]] ;then
			echo '{"number":"'$aa'","phone":"'$phone'","city":"'$city'","tel":"'$tel'","city_code":"'$num1'","yb_code":"'$num2'"}' >> yes.log
			((aa++))
		else
			echo "5=$line" >> no.log
		fi
	elif [ $lie == 6 ] ;then
		echo "6=$line" >> no.log
	else
		echo "!=$line" >> no.log
	fi
done  < all.txt
