import urllib2
import lxml.html
import re 
import requests
import csv
import logging
from ApplicantProfile import ApplicantProfile

import logging
logging.basicConfig(format='%(asctime)s %(message)s',
 datefmt='%m/%d/%Y %I:%M:%S %p',
 filename='poetsquants_webscrape.log',
 level=logging.DEBUG)

"""
PARAMS
-------
alist: a list. of stuff
indices: a list of indices to slice the a list on

RETURNS
--------
returns a list of lists, split on indices contained in indices
"""
# https://stackoverflow.com/questions/1198512/split-a-list-into-parts-based-on-a-set-of-indexes-in-python
def partition(alist,indices):
	g = [alist[i:j] for i, j in zip([0]+indices, indices+[None])]
	# gets rid of empty lists if you are splitting on 0.
	return [a for a in g if len(a) != 0]


"""
PARAMS
---------
stats_list: list, each entry is a stat for an applicant. Thus, more than one entry for each applicant 
ex: ['GMAT','GPA','Undergrad from Near Ivy University', 'Work experience Raytheon as financial doubts','Extracurricular includes alumni involvement']

odds_list: list, each entry is a string saying their chances of admissions to diff schools. 1 entry to 1 applicant
ex: ['Harvard University: 40% Stanford: 40% Wharton: 35%']

analysis_list: list, each entry might be a paragraph of the analysis. not clear yet. wont be used for now.
ex: ['Another danger, though rare, is just going a bit weird on the application through a combination of odd and unsupported goals']

RETURNS
---------
list of ApplicantProfile objects. see ApplicantProfile.py
"""
def parse_lists_into_app_objects(stats_list,odds_list,analysis_list,my_writer):
	#find number of applicants defined by list.
	#there should only be GMAT so use that to split list
	start_indices = []
	for i in range(len(stats_list)):
		e = stats_list[i]
		if 'GMAT' in e.upper() and len(e)<10:
			start_indices.append(i)
	list_of_lists_of_applicant_stats = partition(stats_list,start_indices)
	n_apps = len(list_of_lists_of_applicant_stats)
	aps = []
	for j in range(n_apps):
		if len(odds_list)>=n_apps:
			ap = ApplicantProfile(list_of_lists_of_applicant_stats[j],odds_list[j])
			with open('poetsquantsdata.csv', 'ar') as csvfile:
				# fieldnames = ["GMAT",
				# "GPA",
				# "UNIVERSITY","MAJOR","JOBTITLE",
				# "GENDER","RACE","AGE",
				# "INTERNATIONAL",
				# "ODDS"]
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				d = {}
				d["GMAT"] = ap.gmat_score
				d["GPA"] = ap.gpa
				d["UNIVERSITY"] = ap.uni
				d["MAJOR"] = ap.major
				d["JOBTITLE"] = ap.job_title
				d["GENDER"] = ap.gender
				d["RACE"] = ap.race
				d["AGE"] = ap.age
				d["INTERNATIONAL"] = ap.international
				d["ODDS"] = ap.odds.encode('utf-8').strip()
				writer.writerow(d)
			aps.append(ap)
	return aps




def create_applicant_profiles(page_tree,my_writer):
	# look for <strong></strong> w
	# look for <ul></ul>
	# each <li></li> in there will then have one or more attributes
	# about the persons appllication profile and then from there you can 
	# probably do the regular parsing 
	x_path_to_entry_stats_text = '//ul/li/text()'
	x_path_to_headers = '//p/strong' 
	# TODO: list comprehensions stop being cute at a certain point vvvvv
	odds_of_success_text = [hdr.getparent().getnext().text_content() for hdr in page_tree.xpath(x_path_to_headers) if 'SUCCESS' in hdr.text_content().upper() and 'ODDS' in hdr.text_content().upper()]
	# odds_of_success_text = []
	# for hdr in page_tree.xpath(x_path_to_headers):
	# 	if 'SUCCESS' in hdr.text_content().upper() and 'ODDS' in hdr.text_content().upper():
	# 		odds = hdr.getparent().getnext().text_content()
	# 		odds_of_success_text.append(odds)

	# TODO: list comprehensions stop being cute at a certain point vvvvv
	partial_analysis_text = [hdr.getparent().getnext().text_content() for hdr in page_tree.xpath(x_path_to_headers) if 'ANALYSIS' in hdr.text_content().upper()]
	# gets rid of garbage '<li>' elements that are blank or have the comment count in them.
	applicant_stats_text = [li_text for li_text in page_tree.xpath(x_path_to_entry_stats_text) if li_text != ' ' and 'COMMENTS' not in li_text.upper()]
	applicant_list = parse_lists_into_app_objects(applicant_stats_text,odds_of_success_text,partial_analysis_text,my_writer)
	#logging.info(str(applicant_stats_text))


	return applicant_list

fieldnames = ["GMAT",
"GPA","UNIVERSITY","MAJOR","JOBTITLE",
"GENDER","RACE","AGE",
"INTERNATIONAL",
"ODDS"]
## create csv
mw = None
with open('poetsquantsdata.csv', 'wr') as csvfile:

    mw = csv.DictWriter(csvfile, fieldnames=fieldnames)
    mw.writeheader()


## Data Structure to Hold Applicant Profiles ##
all_profiles = []

## Get The Data on P&Q Website ##

all_articles_page = requests.get("http://poetsandquants.com/2017/05/30/handicapping-your-elite-mba-odds-18/5/")
logging.info("*********** STATUS CODE: " + str(all_articles_page.status_code) + "********************")


articles_page_tree = lxml.html.fromstring(all_articles_page.content)
all_listed_a_tags = articles_page_tree.xpath('//html//a')

# this grabs all the links from the initial page that say "Part xxx"
all_listed_article_links = [el.attrib['href'] for el in all_listed_a_tags if "Part" in el.text_content()]

# loop through all of the links on the root page
for art in all_listed_article_links:
	logging.info("current article link: {}\n".format(art))
	# retrieve content of current link.
	art_content_tree = lxml.html.fromstring(requests.get(art).content)
	# make sure to get all the pages in the article
	# here we or getting the part that says "Page 1 of 4"
	pages_nav_xpath = '//span[@class="pages"]'
	nav_element = art_content_tree.xpath(pages_nav_xpath)
	# we could make this an internal attribute of a data class or just do everything in less OO terms
	# for now make it more scripty and just have a "global" var to hold the applicant profiles
	profiles = create_applicant_profiles(art_content_tree,mw)
	# this is like append, but a bit diff; ex: [] += [1,2] -> [1,2]
	all_profiles += profiles
	num_pages = 1
	if len(nav_element) == 1:
		# get last character of string that says "Page 1 of 4"
		num_pages = nav_element[0].text_content()[-1]
		logging.info("Number of pages: {}\n".format(num_pages))
	# loop through all of the pages that make up the given article.
	for page in range(2,int(num_pages)+1):
		logging.info("On page #{}\n".format(page))
		art_content_tree_next_page = lxml.html.fromstring(requests.get(art+'/'+str(page)+'/').content)
		nxt_page_profiles = create_applicant_profiles(art_content_tree_next_page,mw)
		all_profiles += nxt_page_profiles







