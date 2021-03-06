#!/bin/sh

all_instances=$(aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId]' --output text)

aws ec2 start-instances --instance-ids $all_instances

echo starting instances, please wait

aws ec2 wait instance-running --instance-ids $all_instances

echo all instances running

aws ec2 run_instances --image-id 'ami-dee6bdb6'

echo starting app-tier instance..