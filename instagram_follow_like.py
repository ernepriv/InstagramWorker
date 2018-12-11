import sys;
import pprint;
import os;
import time;
import re;
import ipdb;


from funzioni import genera_browser
from funzioni import genera_browser_fire
from funzioni import login_instagram
from funzioni import recupero_nome_da_argv
from funzioni import recupero_nomi_da_argv
from funzioni import retrive_fb_user_id
from funzioni import recupera_lista_amici_nickname
from funzioni import recupera_likes_in_comune
from funzioni import retrive_fb_user_id
from funzioni import retrieve_fb_users_ids
from funzioni import scrivi_csv
from funzioni import analisi_likes_comuni_amici

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


headless   = True
#headless  = False

br = genera_browser_fire(headless)
br = login_instagram(br)
link_base = 'https://www.instagram.com/explore/tags/'
nome_profilo = 'azzurroleggenda'
link_profilo = 'https://www.instagram.com/' + nome_profilo
intervallo_di_attesa = 10
hash_to_likes = ['carporn', '595', '695','husky','auto','alfa', '500', '595turismo','595competizione','akrapovic','auto']
#hash_to_likes = ['italia','turin','carporn', '595', '695']

#for i in range(1,10):
#	br.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#	time.sleep(1.5)


br.get(link_profilo)
follower_c = br.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[3]/a/span').text

while int(follower_c) < 1000:
	for hashtag in hash_to_likes:
		try:
			link = link_base + hashtag

			br.get(link)

			foto_array = br.find_elements_by_class_name('_9AhH0')
			print 'ANALISI di #' + hashtag
			print str(len(foto_array)) + ' foto da controllare'

			for e in foto_array:
				err_count = 0

				br.execute_script("arguments[0].click();", e)
				time.sleep(5)

				immagine_cuore = br.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/div[2]/section[1]/span[1]/button/span')
				bottone_cuore  = br.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/div[2]/section[1]/span[1]/button')
				bottone_x = br.find_element_by_xpath('/html/body/div[3]/div/button')
				bottone_follow = br.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/header/div[2]/div[1]/div[2]/button')
				out_1 = 1


				if immagine_cuore.get_attribute('class') == 'glyphsSpriteHeart__outline__24__grey_9 u-__7':
					# cuore e' grigio, clicco
					br.execute_script("arguments[0].click();", bottone_cuore)
					print 'like messo ;)'
				else:
					print 'like gia presente :O'


				if bottone_follow.get_attribute('class') == 'oW_lN _0mzm- sqdOP yWX7d        ':
					time.sleep(6) # per limitare quanti ne seguo in poco
					br.execute_script("arguments[0].click();", bottone_follow)
					print 'follow messo ;)'
				else:
					print 'follow gia presente :O'

				follow_try = 0
				out = 0

				while out == 0:

					time.sleep(1)
					if bottone_follow.get_attribute('class') == 'oW_lN _0mzm- sqdOP yWX7d    _8A5w5    ':
						out = 1
					else:
						follow_try += 1
						bottone_follow = br.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/header/div[2]/div[1]/div[2]/button')
						if bottone_follow.get_attribute('class') == 'oW_lN _0mzm- sqdOP yWX7d        ':
							br.execute_script("arguments[0].click();", bottone_follow)

				br.execute_script("arguments[0].click();", bottone_x)
		except:
			print 'recovery'

	br.get(link_profilo)
	follower_c = br.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[3]/a/span').text
