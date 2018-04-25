import re
import logging

class ApplicantProfile():
	def __init__(self,list_of_stats_text,odds_string):
		self.uni = None
		self.gmat_score = None
		self.gpa = None
		self.odds = None
		self.age = None
		self.race = None
		self.gender = None
		self.major = None
		self.job_title  = None
		self.international = None
		self.odds = None
		for stat in list_of_stats_text:
			su = stat.upper()
			# the length check is to make sure we dont get extraneeous comments tht have "GMAT" in them
			if 'GMAT' in su and bool(re.search('\d',su)) and (self.gmat_score is None):
				self.gmat_score = self.parse_gmat(su)
			elif ('GPA' in su or 'GRADE POINT AVERAGE' in su) and (bool(re.search('\d',su)) and self.gpa is None):
				self.gpa = self.parse_gpa(su)
			elif ('UNIVERSITY' in su or 'COLLEGE' in su or 'DEGREE' in su or 'INSTITUTE' in su) and (self.uni is None):
				self.uni = self.parse_uni(su)
				self.major = self.parse_major(su)
			elif ('YEAR' in su) and (bool(re.search('\d',su)) and self.age is None):
				self.age = self.parse_age(su)
				self.race = self.parse_race(su)
				self.gender = self.parse_gender(su)
		self.odds = odds_string
		for t in [self.uni,self.gmat_score,self.gpa]:
			logging.info(str(t)) 
		logging.info(self.odds)

	"""
	represent one feature using this class. Why does this exist?
	gpa_string: string of gpa
	university_string: string of school they went to 
	gmat_string: a string because sometimes its represented as a __Q/__V other times as raw score
				we will do some parsing depending on the format
	job_title: defaults to None (financial analyst, engineer, software, teacher, consultant)
	industry: which industry is the person in (finance, energy, marketing, automotive)
	company: type of company, defaults to None (large well known, medium sized, start up, unicorn)
	international: boolean. defaults to False -> U.S applicants 
	race: string representing race, may need parsing when we check out the raw text data
	age: how old is the person featured
	"""
	def boss_setter(self,gpa_string,gmat_string,univeristy_string,odds_string,job_title=None,industry=None,company=None,international=False,race=None,age=None,gender=None,major=None):
		# mandatory
		self.gpa = self.parse_gpa(gpa_string)
		self.gmat_score = self.parse_gmat(gmat_string)
		self.uni = self.parse_uni(univeristy_string)
		self.odds = odds_string
		# optionals
		self.job_title = job_title
		self.industry = industry
		self.company = company
		self.international = international
		self.race = race
		self.age = age
		self.gender = gender
		self.major = major

	def parse_major(self, major_str):
		su = major_str.upper()
		if 'ENGINEER' in su or 'COMPUTER' in su:
			return 'Engineering'
		elif 'FINANCE'in major_str or 'ECON' in major_str:
			return 'Economics'
		elif 'BUSINESS' in major_str:
			return 'Business'
		elif 'INTERNATIONAL' in major_str:
			return 'International Studies'
		elif 'EDUCATION' in major_str:
			return 'Education'
		elif 'FROM' in major_str:
			split_major = major_str.split('FROM')
			if len(split_major)>1:
				self.uni = self.parse_uni(split_major[1])
		else:
			try:
				logging.warning("Didn't parse any major from: {}\n".format(major_str))
			except UnicodeEncodeError:
				pass

	# not politically correct , will fix later and see how data comes out
	def parse_gender(self, gender_str):
		su = gender_str.upper()
		if 'FE' in su or 'WOMAN' in su:
			return 'Female'
		# this order matters, since male is in female and man is in woman
		elif 'MALE' in su or 'MAN' in su:
			return 'MALE'
		else:
			try:
				logging.warning("Could not parse sex from {}\n".format(gender_str))
			except UnicodeEncodeError:
				pass
			return None
	
	# basic & non researched, potentially problematic.. working on it.
	def parse_race(self,race_str):
		s = race_str.upper()
		if('AFRICA' in s or 'BLACK' in s):
			return 'Black'
		elif 'ASIA' in s or 'INDIA':
			return 'Asian'
		elif ('HISPANIC' in s) or ('LATIN' in s):
			return 'Latinx'
		elif ('WHITE' in s):
			return 'White'
		else:
			try:
				logging.warning("Didnt parse any race from: {}\n".format(race_str))
			except UnicodeEncodeError:
				pass
			return None



	def parse_age(self,age_str):
		g = re.findall('[-+]?\d*\.\d+|\d+',age_str)
		if len(g) > 0:
			age = g[0]
			if age > 80 or age < 18:
				try:
					logging.warning("Messed up age parsing: {}\n".format(age_str))
				except UnicodeEncodeError:
					pass
			else:
				return age
		elif '-' in age_str and 'YEAR' in age_str:
			split_age = age_str.split('-')
			age = split_age[0]
			return age

		try:
			logging.warning("Could not age parse: {}\n".format(age_str))
		except UnicodeEncodeError:
			pass
		return



	# in progress lol, this is stupid.
	def parse_uni(self,uni_str):
		s = uni_str.upper()
		# need to rework to have this be a list that allows you to update and add more entries
		# this methodology is pretty bad. right now but ok for first pass.
		if ('IVY' in s and not 'NEAR' in s) or ('M.I.T' in s) or ('COLUMBIA' in s) or ('YALE' in s):
			return 'Tier 1'
		elif 'NEAR' in s and 'IVY' in s:
			return 'Tier 2'
		else:
			try:
				logging.warning("Not enough info to parse university: {}".format(uni_str))
			except UnicodeEncodeError:
				pass
			return 'Tier 3'

	def parse_gpa(self,gpa_str):
		#https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string
		return re.findall('[-+]?\d*\.\d+|\d+',gpa_str)[0]

	def parse_gmat(self,gmat_str):
		s = gmat_str.upper()
		if '/' in s:
			v=0
			q=0
			if 'V' in s:
				v=int(re.findall('\d+',s)[0])


			if 'Q' in s:
				q=int(re.findall('\d+',s)[0])
			# try to convert a gre score to gmat (rough)
			if(v != 0 and q != 0):
				rough_est = (v+q)*8.19
				rounded = rough_est - rough_est%10
				if rounded>800:
					return 800
				else:
					return rounded
			else:
				try:
					logging.warning("Could not parse gmat: {}\n".format(gmat_str))
				except UnicodeEncodeError:
					pass
				return None

		elif 'GMAT' in s:
			return int(re.findall('\d+',s)[0])
		try:
			logging.warning("Could not parse GMAT score from: {}\n".format(gmat_str))
		except UnicodeEncodeError:
			pass
		return None


