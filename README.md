# Handicapping EVERYONES MBA Odds

This project is still a work in progress but its essentially a webscrape of an MBA website where a former admissions officer gives people the odds that they'll get into certain programs across the country. 

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
