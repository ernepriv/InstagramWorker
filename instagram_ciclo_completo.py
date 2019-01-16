import sys;
import pprint;
import os;
import time;
import re;
import ipdb;
import yaml;
import random;

from funzioni import genera_browser
from funzioni import genera_browser_fire
from funzioni import login_instagram
from funzioni import follow_and_like_some_hashtag
from funzioni import unfollow_all_follows

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

headless   = True
credentials 	= yaml.load(open('./credentials.yml'))
nome_profilo 	= credentials['instagram']['nome_profilo']
username		= credentials['instagram']['username']
password		= credentials['instagram']['password']
hashtags 		= credentials['instagram']['hashtags']
max_following 			= int(credentials['instagram']['max_following'])
preserved_follows   = credentials['instagram']['preserved_follows']

# for firefox browser
browser = genera_browser_fire(headless)

# for chrome browser
# browser = genera_browser(headless)

browser = login_instagram(browser, username, password)

while True:
	try:
		# follow & like
		returned 	= 0
		while returned == 0:
			# to randomize hashtag order
			random.shuffle(hashtags)
			returned = follow_and_like_some_hashtag(browser, username, password, nome_profilo, hashtags, max_following)

		# unfollow
		returned 	= 0
		while returned == 0:
			returned = unfollow_all_follows(browser, nome_profilo, preserved_follows)
	
	except WebDriverException:
		print "rescue WebDriverException"
