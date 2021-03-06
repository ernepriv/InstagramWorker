# requires:
# sudo apt-get install python-yaml
#
# TODO
# - evitare login multipli
#
#
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
INSTAGRAM_LINK = 'https://www.instagram.com/'

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
	# verifica di corretto login
	print('verifica link')
	if len(re.findall(INSTAGRAM_LINK + '(\w+)',browser.current_url)) == 0:
		print('verifica ok!')
	else:
		print('PROBLEMA DI AUTENTICAZIONE! non so come procedere, mi trovo in url: ' + browser.current_url)
		raise 'PROBLEMA DI AUTENTICAZIONE! non so come procedere, mi trovo in url: ' + browser.current_url

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

def unfollow_all_follows(br, nome_profilo, preserved_follows):
	try:
		link_profilo = 'https://www.instagram.com/' + nome_profilo
		while True:

			br.get(link_profilo)

			if no_follows_to_unfollow(br, preserved_follows):
				return 1

			if zero_follows(br):
				return 1

			unfollow_visualized_follows(br, preserved_follows)

	except NoSuchElementException:
		# quando finisco i follower nella schermata
		return 0


def scroll_down_for_follows(br):

	# focusing on follows modal
	modal = br.find_element_by_xpath('/html/body/div[3]/div/div/div[2]')

	before_follows_array 	= []
	now_follows_array 		= br.find_elements_by_xpath('/html/body/div[3]/div/div/div[2]/ul/div/li')

	while now_follows_array != before_follows_array:
		# scroll down
		for x in range(0, 20):
			modal.send_keys(Keys.PAGE_DOWN)
			time.sleep(1)

		before_follows_array 	= now_follows_array
		now_follows_array 		= br.find_elements_by_xpath('/html/body/div[3]/div/div/div[2]/ul/div/li')

		print str(len(now_follows_array)) + ' analyzed...'

def open_following_list(br):
	button_show_followers = br.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')
	button_show_followers.click()

def list_of_following(br):
	return br.find_elements_by_xpath('/html/body/div[3]/div/div/div[2]/ul/div/li')

def close_following_modal(br):
	x_button = br.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/div[2]/button')
	x_button.click()

def real_following_count(br):
	# i must be in main page of profile
	open_following_list(br)
	# too fast is bad
	time.sleep(3)
	scroll_down_for_follows(br)
	following_count = list_of_following(br)
	close_following_modal(br)

	return len(following_count)

def unfollow_visualized_follows(br, preserved_follows):
	# i must be in main page of profile

	open_following_list(br)

	time.sleep(3)

	scroll_down_for_follows(br)

	follows_array = list_of_following(br)
	print "-------------------------------"
	print "---------- refresh! -----------"
	print "-------------------------------"

	current_action_c = 0

	for follow in follows_array:

		# necessary to limitate ban from instagram
		if (current_action_c%10 == 0) and (current_action_c != 0):
			time.sleep(500)

		follows_c = br.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[3]/a/span').text
		print 'Now ' + follows_c + ' followers'



		if not to_preserve(follow, preserved_follows):
			unfollow_follow(follow)
			current_action_c += 1
			time.sleep(7)
		else:
			#print name_from_follow(follow) + ' preserved!'
			print '---'
			if (current_action_c%10 == 0):
				# so i haven't to wait if stuck on current_action_c%10
				current_action_c += 1

	return True

def name_from_follow(follow):
	return follow.text.split("\n")[0]

def to_preserve(follow, preserved_follows):
	if any(follow_name(follow) in s for s in preserved_follows):
		return True
	else:
		return False


def follow_name(follow):
	return follow.text.split("\n")[0]

def no_follows_to_unfollow(br, preserved_follows):
	follows_c = real_following_count(br)
	if follows_c <= len(preserved_follows):
		return True
	else:
		return False

def zero_follows(br):
	follows_c = br.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[3]/a/span').text
	if follows_c == '0':
		return True
	else:
		return False


def unfollow_follow(follow):
	# try to unfollow a follow
	# unfollow this!
	follow.find_elements_by_css_selector("button")[0].click()
	print(str(datetime.datetime.now()) + ' unfollow!')

	try:
		time.sleep(3)
		# i'm sure and confirm it!
		follow.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[1]').click()
		return True
	except NoSuchElementException:
		return True


def check_if_was_unfollowed(follow):
	unfollow_done 		= '_0mzm- sqdOP  L3NKy       '
	unfollow_not_done 	= '_0mzm- sqdOP  L3NKy   _8A5w5    '

	if follow.find_elements_by_css_selector("button")[0].get_attribute('class') == unfollow_done:
		return True
	else:
		return False

def profile_link(profile_name):
	return INSTAGRAM_LINK + profile_name

def how_many_following(browser, profile_name):
	# i must be logged before do this!
	browser.get(profile_link(profile_name))
	count = browser.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[3]/a/span').text
	# remove ',' from string
	count = re.sub(",","",count)
	return int(count)

def hashtag_link(hashtag):
	link_base   = 'https://www.instagram.com/explore/tags/'
	return link_base + hashtag

def foto_from_hashtag_page(browser):
	return browser.find_elements_by_class_name('_9AhH0')

def button_heart_like(browser):
	# i must have a foto open in browser before do this!
	return browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/div[2]/section[1]/span[1]/button/span')

def button_x_close(browser):
	# i must have a foto open in browser before do this!
	return browser.find_element_by_xpath('/html/body/div[3]/div/button')

def button_follow(browser):
	# i must have a foto open in browser before do this!
	return browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/header/div[2]/div[1]/div[2]/button')

def image_heart_like(browser):
	# i must have a foto open in browser before do this!
	 return browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/div[2]/section[1]/span[1]/button/span')

def empty_heart(heart_image):
	# i must have a foto open in browser before do this!
	return heart_image.get_attribute('class') == 'glyphsSpriteHeart__outline__24__grey_9 u-__7'

def not_followed_yet(follow_button):
	# i must have a foto open in browser before do this!
	return follow_button.get_attribute('class') == 'oW_lN _0mzm- sqdOP yWX7d        '

def follow_and_like_some_hashtag(browser, username, password, profile_name, hash_to_likes, max_following):
	# i must be logged before do this!
	after_follow_wait_time 	= 5
	after_click_wait_time 	= 5
	big_pause = 800

	while True:
		for hashtag in hash_to_likes:
			try:
				# return to profile page to check how many following i have
				browser.get(profile_link(profile_name))
				following_count = how_many_following(browser, profile_name)
				if following_count > max_following:
					return 1

				browser.get(hashtag_link(hashtag))
				foto_from_hashtag_page(browser)
				foto_array = foto_from_hashtag_page(browser)

				print ''
				print ''
				print '--> Now ' + str(following_count) + ' following!' '<-----------------------'
				print ''
				print ''
				print '-----------------------------------------------------------------------------'
				print '-------------- Ready to likes and follow some #' + hashtag + ' --------------'
				print '-----------------------------------------------------------------------------'
				time.sleep(big_pause)
				print 'Analyzing ' + str(len(foto_array)) + ' pictures!'

				for e in foto_array:

					browser.execute_script("arguments[0].click();", e)
					time.sleep(after_click_wait_time)

					if empty_heart(image_heart_like(browser)):
						browser.execute_script("arguments[0].click();", button_heart_like(browser))
						print 'PIC -> liked!'
					else:
						print '-'

					if not_followed_yet(button_follow(browser)):
						browser.execute_script("arguments[0].click();", button_follow(browser))
						print 'ACCOUNT -> followed!'
						time.sleep(after_follow_wait_time)
					else:
						print '-'

					browser.execute_script("arguments[0].click();", button_x_close(browser))
			except:
				print 'Recovery some crash :S'
				browser.get(profile_link(profile_name))
				following_count = how_many_following(browser, profile_name)
				if following_count > max_following:
					return 1


	return 1
