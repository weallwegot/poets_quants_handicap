class ApplicantProfile():
	"""
	represent one feature using this class
	age: how old is the person featured
	university: the tier of school they went to (elite,middle,small)
	gmat_string: a string because sometimes its represented as a __Q/__V other times as raw score
				we will do some parsing depending on the format
	job_title: defaults to None (financial analyst, engineer, software, teacher, consultant)
	industry: which industry is the person in (finance, energy, marketing, automotive)
	company: type of company, defaults to None (large well known, medium sized, start up, unicorn)
	international: boolean. defaults to False -> U.S applicants 
	race: string representing race, may need parsing when we check out the raw text data
	"""
	def __init__(self,age,university,gmat_string,job_title=None,industry=None,company=None,international=False,race=None):
		self.age = age
		self.uni = university
		self.gmat_score = int(self.parse_gmat(gmat_string))
		self.job_title = job_title
		self.industry = industry
		self.company = company
		self.international = international
		self.race = race

	def parse_gmat(self,gmat_str):
		s = gmat_str.upper()
		if '/' in s:
			pass
			
			if 'V' in s:
				pass


			if 'Q' in s:
				pass

		elif 'GMAT' in s:
			pass


		return 800


