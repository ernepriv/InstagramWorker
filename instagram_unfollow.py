import sys;
import pprint;
import os;
import time;
import re;
import ipdb;
import logging;
import datetime;
import yaml

from funzioni import genera_browser
from funzioni import genera_browser_fire
from funzioni import login_instagram
from funzioni import unfollow_all_follows

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

headless   		= True
credentials 	= yaml.load(open('./credentials.yml'))
nome_profilo 	= credentials['instagram']['nome_profilo'] 
username		= credentials['instagram']['username']
password		= credentials['instagram']['password']

# for firefox browser
browser = genera_browser_fire(headless)

# for chrome browser
#browser = genera_browser(headless)

browser 	= login_instagram(browser, username, password)
returned 	= 0
count 		= 0
while returned == 0:
	returned = unfollow_all_follows(browser, nome_profilo)
	count += 1

	# if too many times it exit for errors (returned = 0)
	# i close and reopen browser to fix them
	if count > 2:
		browser.quit()		
		browser = genera_browser_fire(headless)
		browser = login_instagram()
		count = 0
