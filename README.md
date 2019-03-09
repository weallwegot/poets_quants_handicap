# Handicapping EVERYONES MBA Odds

[Blog post on motivation](https://andcomputers.io/bschool-webscrapes-and-machine-learning/)

This project is essentially a webscrape of an MBA website where a former admissions officer gives people the odds that they'll get into certain programs across the country. 

There is an api deployed at `https://jcp.pythonanywhere.com/api/v1` and it processes POST requests with the following format.

The following JSON payload would be sent to the api to receive  the chances of admission to University of Chicago Booth MBA for an underrepresented minority male with a `3.1` gpa, a `650` gmat, a STEM major, and a degree from a well recognized school (whatever that means).

```python

{"gpa":"3.1",
 "gmat":"650",
 "major":"1",
 "race":"1",
 "gender":"0",
 "school":"1",
 "university":"booth"}
```

`gpa`: your gpa on a 4 point scale

`major`: 1 for STEM, 0 for non stem

`urm`: 1 for underrepresented minority, 0 for not

`gender`: 1 for female, else 0

`university`: 1 if you went to a school everyone knows, 0 if its less known

`school`: the school you want to predict your MBA admission chances for. choices are ["stanford","harvard","wharton","booth","columbia","sloan","kellogg"]

_noting that these features are not high enough resolution to truly represent an applicant, but read the blog post for more on that_

-------------------------------------------------------------

- The `page_parser` is used to build a dataset of applicant profiles from [Poets and Quants](http://poetsandquants.com/2017/05/30/handicapping-your-elite-mba-odds-18/5/)

- Applicant information will be the features that go into a ML model. probably just linear regression. Not sure yet. 
  Progress on those results can be found [here](/machine_learning/README.md)

- Uses the basic features from the webscrape:
  - GMAT or GMAT equivalent (using this [conversion tool](https://github.com/weAllWeGot/gre_to_gmat))
  - GPA
  - school
  - major
  - gender
  - race
  
#### End goal

predict someones<sup>1</sup> chances of getting into different<sup>2</sup> business schools based on their profile<sup>3</sup>.

_____
 
 <sup>1</sup> someone willing to provide the features listed above
 
 <sup>2</sup> so poets & quants or their readers really only seem to be interested in the same 6 or 7 schooles. harvard, stanford, yale, ross, kellogg, booth, anderson, and occassionally a few others. so its not *any* school.
 
 <sup>3</sup>Yes, a lot more goes into an admission decision, but this is still fun to do. Since I'm assuming people don't want to read all 250+ profiles looking for one with a similar background/stats to them. I think there's real demand for this because the comments in those articles are overflowing with people posting their profiles and waiting for the website to do a feature on them.
 
_________
 
 ** [Peep the latest data scrape progress](data_out/pq_data_4_24_18.csv) from a more updated version **

old visuals of the webscraper doin its thingy thing.


![demo_gif](http://g.recordit.co/WuFYYsQ4uw.gif)




## Contributing

Its still pretty early but if you have suggestions, thoughts, feedback, criticism, etc feel free to open a PR or submit an Issue. 

Thanks in advance :blush:

--------------------------------------------------------------------------

#### Donating

If ya feeling generous, hollr @ the kid :heart:

https://www.paypal.me/hijodelsol

**BTC: 3EbMygEoo8gqgPHxmqa631ZVSwgWaoCj3m**

**ETH: 0x2F2604AA943dB4E7257636793F38dD3B1808A9e7**

**LTC: MQVgzNDgw43YzyUg3XmH3jQ7L8ndVswmN3**
