#!/bin/sh


ids=$(aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId]' --output text)

for i in $ids; do
    echo $i;
 done
