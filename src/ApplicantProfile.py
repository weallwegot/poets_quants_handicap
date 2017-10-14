import re

class ApplicantProfile():
	def __init__(self,list_of_stats_text,odds_string):
		self.uni = None
		self.gmat_score = None
		self.gpa = None
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
		self.odds = odds_string
		for t in [self.uni,self.gmat_score,self.gpa]:
			print(str(t)) 
		print(self.odds)

	"""
	represent one feature using this class
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
	def boss_setter(self,gpa_string,gmat_string,univeristy_string,odds_string,job_title=None,industry=None,company=None,international=False,race=None,age=None):
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

	# in progress lol, this is stupid.
	def parse_uni(self,uni_str):
		s = uni_str.upper()
		if 'IVY' in s and not 'NEAR' in s:
			return 'Tier 1'
		elif 'NEAR' in s and 'IVY' in s:
			return 'Tier 2'
		else:
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

			if(v != 0 and q != 0):
				rough_est = (v+q)*8.19
				rounded = rough_est - rough_est%10
				if rounded>800:
					return 800
				else:
					return rounded
			else:
				
				return None

		elif 'GMAT' in s:
			return int(re.findall('\d+',s)[0])
		print("Could not parse GMAT score")
		return None


