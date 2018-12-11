import sys;
import pprint;
import os;
import time;
import re;
import ipdb;
import datetime;
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions 	import NoSuchElementException

link_login_instagram 	= 'https://www.instagram.com/accounts/login/?source=auth_switcher'

def login_instagram(browser, username_instagram, password_instagram):
	browser.get(link_login_instagram)
	input_fields = browser.find_elements_by_xpath('//input')
	while not input_fields:
		input_fields = browser.find_elements_by_xpath('//input')

	input_fields[0].send_keys(username_instagram)
	input_fields[1].send_keys(password_instagram)
	# un po debole
	button_login = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/button')
	button_login.click()

	time.sleep(2)
	return browser

def genera_browser(visible='true'):
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	import os
	chrome_options = Options()
	if visible == 'false':
		chrome_options.add_argument("--headless")
	chrome_options.add_argument("--window-size=1920x1080")
	chrome_options.add_argument("--start-maximized")
	prefs = {"profile.default_content_setting_values.notifications" : 2}

	#chrome_options.binary_location = "/usr/bin/chromedriver"

	chrome_options.add_experimental_option("prefs",prefs)
	browser = webdriver.Chrome(chrome_options=chrome_options)
	return browser

def genera_browser_fire(show_browser):
	from selenium import webdriver
	from selenium.webdriver.firefox.options import Options
	import os
	firefox_options = Options()
	firefox_options.headless = show_browser
	browser = webdriver.Firefox(firefox_options=firefox_options)
	return browser

def unfollow_all_follows(br, nome_profilo):
	try:
		link_profilo = 'https://www.instagram.com/' + nome_profilo
		while True:

			br.get(link_profilo)

			if zero_follows(br):
				return 1

			unfollow_first_follows(br)

		return 0
	except NoSuchElementException:
	# quando finisco i follower nella schermata
		return 0

def unfollow_first_follows(br):
	# i must be in main page of profile

	button_show_followers = br.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')
	button_show_followers.click()

	# too fast is bad
	time.sleep(3)

	follows_array = br.find_elements_by_xpath('/html/body/div[3]/div/div/div[2]/ul/div/li')
	print str(len(follows_array)) + " to unfollow"

	for follow in follows_array:
		time.sleep(7)

		unfollow_follow(follow)

		out = 0
		while out == 0:
			
			if check_if_was_unfollowed(follow):
				out = 1
			else:
				if not check_if_was_unfollowed(follow):
					unfollow_follow(follow)

def zero_follows(br):
	follows_c = br.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[3]/a/span').text
	print 'Now ' + follows_c + ' followers'
	if follows_c == '0':
		return True
	else:
		return False

def unfollow_follow(follow):
	# try to unfollow a follow
	
	# unfollow this!
	follow.find_elements_by_css_selector("button")[0].click()
	print(str(datetime.datetime.now()) + ' unfollow!')

	# ne sono sicuro
	follow.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[1]').click()


def check_if_was_unfollowed(follow):
	unfollow_done 		= '_0mzm- sqdOP  L3NKy       '
	unfollow_not_done 	= '_0mzm- sqdOP  L3NKy   _8A5w5    '

	if follow.find_elements_by_css_selector("button")[0].get_attribute('class') == unfollow_done:
		return True
	else:
		return False

