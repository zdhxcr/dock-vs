#!/bin/bash
> result.txt
 for i in out*; do
result=$( grep "REMARK VINA RESULT" $i | awk '{ print $4 }' )
echo " $i " >> result.txt
echo "$result" | tr ' ' '\n' >> result.txt
done

