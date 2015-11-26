
from lxml import html
import requests
from datetime import datetime, timedelta
page = requests.get('http://sports.yahoo.com/college-basketball/scoreboard/?date=2015-11-26')
page.content2 =  page.content.replace("\\", "")
tree=html.fromstring(page.content2)
Time = tree.xpath('//tr[@class="game pre link"]//span[@class="time"]/text()')
if not Time:
	Time = tree.xpath('//span[@class="time"]/text()')
Time2 = [x[0:-4] for x in Time]
URLs = tree.xpath('//tr[@class="game pre link"]//td[@class="score"]//@href')
if not URLs:
	URLs = tree.xpath('//td[@class="score"]//@href')
TimeDeltas = [(datetime.strptime(x, '%I:%M %p')-datetime.utcnow()+timedelta(hours=5)).seconds/60 for x in Time2]

TimeDeltas