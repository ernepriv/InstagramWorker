#!/bin/bash

while true
do
        date
        echo 'follow & like'
        python instagram_follow_like.py

        date
        echo 'unfollow'
        python instagram_unfollow.py
done
