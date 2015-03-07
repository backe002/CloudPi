#!/bin/sh

all_instances=$(aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId]' --output text)

aws ec2 stop-instances --instance-ids $all_instances

echo stopping instances, please wait

aws ec2 wait instance-stopped --instance-ids $all_instances

echo all instances stopped