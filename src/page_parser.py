import urllib2
import lxml.html
import re 
import requests
from ApplicantProfile import ApplicantProfile

## Data Structure to Hold Applicant Profiles ##
all_profiles = []

## Get The Data on P&Q Website ##

all_articles_page = requests.get("http://poetsandquants.com/2017/05/30/handicapping-your-elite-mba-odds-18/5/")
print("*********** STATUS CODE: " + str(all_articles_page.status_code) + "********************")

articles_page_tree = lxml.html.fromstring(all_articles_page.content)
all_listed_a_tags = articles_page_tree.xpath('//html//a')

all_listed_article_links = [el.attrib['href'] for el in all_listed_a_tags if "Part" in el.text_content()]

#print(str(all_listed_article_links))

for art in all_listed_article_links:
	print art
	art_content_tree = lxml.html.fromstring(requests.get(art).content)
	# make sure to get all the pages in the article
	pages_nav_xpath = '//span[@class="pages"]'
	nav_element = art_content_tree.xpath(pages_nav_xpath)
	# we could make this an internal attribute of a data class or just do everything in less OO terms
	# for now make it more scripty and just have a "global" var to hold the applicant profiles
	profiles = create_applicant_profiles(art_content_tree)
	all_profiles = all_profiles + profiles
	num_pages = 1
	if len(nav_element) == 1:
		num_pages = nav_element[0].text_content()[-1]
		print(str(num_pages))
	for page in range(2,num_pages+1):
		art_content_tree_next_page = lxml.html.fromstring(requests.get(art+'/'+str(page)+'/').content)
		nxt_page_profiles = create_applicant_profiles(art_content_tree_next_page)
		all_profiles = all_profiles + nxt_page_profiles


def create_applicant_profiles(page_tree):
	# look for <strong></strong> w
	# look for <ul></ul>
	# each <li></li> in there will then have one or more attributes
	# about the persons appllication profile and then from there you can 
	# probably do the regular parsing 





