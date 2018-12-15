# InstagramWorker
Project realized in python, which allows to interact automatically and structured with the social network Instagram, allowing massive operations Scheduled in defined intervals and at certain times of the day.

## Requirements
To work properly, the scripts need to have all required dependencies installed (explained in requirements.txt), including the firefox or chrome webdriver
```txt
selenium==3.14.0
ipdb==0.11
PyYAML==3.13
```

## Setup credentials.yml
```yaml
instagram:
  nome_profilo: profilename
  username: mail@mail.com
  password: secret
  max_following: 1000 # I suggest max 1000, instagram could ban you if g too fast
  preserved_follows: # follows that you want to preserve when launch unfollow script
    - pippo
    - pluto
  hashtags: # hashtags that you want to use in follow script
    - abarth
    - thescorpionship
```

## FollowLike script
This script allows you to follow the latest accounts that have posted a content using the hashtags provided in the credentials.yml file
```bash
python instagram_follow_like.py
```

## Unfollow script
This script allows you to remove the follow-up to all your following, except for those expressed in the credentials.yml file
```bash
python instagram_unfollow.py
```


## About me
I like to create scripts of this type aimed at automating operations that I often know repetitive and cumbersome, for any information on this proposal or collaboration, please do not hesitate to contact me
