import urllib2
import lxml.html
import re 
import requests
from ApplicationProfile import ApplicationProfile


## Get The Data on P&Q Website ##

all_articles_page = requests.get("http://poetsandquants.com/2017/05/30/handicapping-your-elite-mba-odds-18/5/")
print("*********** STATUS CODE: " + str(all_articles_page.status_code) + "********************")

articles_page_tree = lxml.html.fromstring(all_articles_page.content)
all_listed_a_tags = articles_page_tree.xpath('//html//a')

all_listed_article_links = [el.attrib['href'] for el in all_listed_a_tags if "Part" in el.text_content()]

#print(str(all_listed_article_links))

for art in all_listed_article_links:
	art_content_tree = lxml.html.fromstring(requests.get(art).content)
