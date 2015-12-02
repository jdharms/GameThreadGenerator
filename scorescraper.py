def getgametimes(urlname):
	from lxml import html
	import requests 
	import scorescraper
	from datetime import datetime, timedelta
	page = requests.get(urlname)
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
	TimeDeltas2 = list(scorescraper.rename_duplicates(TimeDeltas))
	return (TimeDeltas2,URLs)	
	
def getcbbthread(urlname,secret,token):
	from datetime import datetime
	from lxml import html
	import pandas as pd
	import requests 
	import requests.auth
	import csv
	import scorescraper
	import OAuth2Util
	page = requests.get('http://sports.yahoo.com'+urlname)
	page.content2 =  page.content.replace("\\", "")
	tree=html.fromstring(page.content2) 
	df1=pd.read_csv('https://raw.githubusercontent.com/airjesse123/GameThreadGenerator/master/TeamLookup.csv', sep=',',header=None)
	df = df1.fillna('')

	VisitingTeamName = tree.xpath('//div[@class="team away"]/div[@class="team-info"]/div[@class="name"]/a/text()')[0]
	VisitingYahooName = tree.xpath('//div[@class="team away"]/div[@class="team-info"]/div[@class="name"]//@href')[0][13:-1]
	try:
		VisitingRedditName = df[df[1]==VisitingYahooName].iloc[0][2]
	except:
		VisitingRedditName = ''
	try:
		VisitingRadioURL = df[df[1]==VisitingYahooName].iloc[0][4]
	except:
		VisitingRadioURL = ''
	try:
		VisitingSubReddit = df[df[1]==VisitingYahooName].iloc[0][5]
	except:
		VisitingSubReddit = ''
	VisitingTeamRecord = tree.xpath('//div[@class="team away"]/div[@class="team-info"]/div[@class="rank"]/text()')[0]
	VisitingTeamLogo = tree.xpath('//div[@class="team away"]/div[@class="team-info"]/div[@class="rank"]/text()')[0]
	HomeTeamName = tree.xpath('//div[@class="team home"]/div[@class="team-info"]/div[@class="name"]/a/text()')[0]
	HomeYahooName = tree.xpath('//div[@class="team home"]/div[@class="team-info"]/div[@class="name"]//@href')[0][13:-1]
	try:
		HomeRedditName = df[df[1]==HomeYahooName].iloc[0][2]
	except:
		HomeRedditName = ''
	try:
		HomeRadioURL = df[df[1]==HomeYahooName].iloc[0][4]
	except:
		HomeRadioURL = ''
	try:
		HomeSubReddit = df[df[1]==HomeYahooName].iloc[0][5]
	except:
		HomeSubReddit = ''
	HomeTeamRecord = tree.xpath('//div[@class="team home"]/div[@class="team-info"]/div[@class="rank"]/text()')[0]
	HomeTeamLogo = tree.xpath('//div[@class="team away"]/div[@class="team-info"]/div[@class="rank"]/text()')[0]
	if HomeSubReddit=='' and VisitingSubReddit=='':
		Subreddits = ''
	elif HomeSubReddit=='' or VisitingSubReddit=='':
		Subreddits = '\n' + '\n' + '\n' + '\n' + '**Subscribe to these communities**'  + '\n' + '\n' + HomeSubReddit + VisitingSubReddit
	else:
		Subreddits =  '\n' + '\n' + '\n' + '\n' + '**Subscribe to these communities**' + '\n' + '\n' + VisitingSubReddit + ' | ' + HomeSubReddit
	if HomeRadioURL == '':
		HomeRadioName = ''
	else:
		HomeRadioName = HomeRedditName
	if VisitingRadioURL == '':
		VisitingRadioName = ''
	else:
		VisitingRadioName = VisitingRedditName
	PreTime = tree.xpath('//li[@class="status"]/text()')[0]
	DateTime = datetime.strptime(PreTime[5:-7], "%b %d %H:%M").strftime("%-H:%M") + PreTime[-7:-4] + ' EST'
	Stadium = tree.xpath('//li[@class="stadium"]/span/text()')[0]
	try:
		TV = tree.xpath('//li[@class="left"]/ul/li/text()')[0]
	except:
		TV = '    No TV'	
	try:
		OddsFavorite = tree.xpath('//li[@class="odds-ps-name\"]/text()')[0]
	except:
		OddsFavorite = 'Odds not set'
	try:
		OddsSpread = tree.xpath('//li[@class="odds-ps"]/text()')[0]
	except:
		OddsSpread = 'NA'
	try:
		OddsOU = tree.xpath('//li[@class="odds-overunder"]/text()')[0]
	except:
		OddsOU = 'NA'

	subreddit = 'collegebasketball'

	title = '[Game Thread] ' + VisitingTeamName + ' at ' + HomeTeamName + ' (' + DateTime + ')'

	body = '###NCAA Basketball' + '\n' + ' ' + '\n' + '---' \
	+ '\n' + '[](/' + VisitingRedditName + ') **'+VisitingTeamName+'** '+VisitingTeamRecord+' at ' + '[](/' + HomeRedditName + ') **' + HomeTeamName+'** '+HomeTeamRecord   \
	+ '\n' + ' ' + '\n' + '**Tipoff:** '+ DateTime + '\n' +  ' ' \
	+ '\n' +  '**Venue:** '+Stadium + '\n' +  ' ' \
	+ '\n' +  '-----------------------------------------------------------------' + '\n' +  ' ' \
	+ '\n' +  '**[Join the live IRC chat on freenode, #redditcbb](http://webchat.freenode.net/?channels=#redditcbb)**' \
	+ '\n' +  ' '	 \
	+ '\n' +  '-----------------------------------------------------------------' + '\n' +  ' ' \
	+ '\n' +  '**Television:** ' + '\n' +  TV[4:] + '\n' +  ' ' + '\n' +  '**Streams:** ' \
	+ '\n' +  '[IsTheGameOn?](http://isthegameon.com/)' + '\n' +  ' ' \
	+ '\n' +  '**Radio:** ' + '\n' +  '[' + VisitingRadioName + '](http://tunein.com' + VisitingRadioURL + ')' + '\n'  +  ' ' \
	+ '  [' + HomeRadioName + '](http://tunein.com' + HomeRadioURL + ')' + '\n'  +  ' ' \
	+ '\n' +  '**Preview/Follow:**' + '\n' +  '[Yahoo!](http://sports.yahoo.com'+urlname+')' \
	+ '\n' +  ' '  + '\n' +  '**Odds**'  + '\n' +  ' '	 \
	+ '\n' +  '**Favorite:** ' + OddsFavorite + '\n' +  ' '	+ '\n' +  '**Game Line:** '+OddsSpread \
	+ '\n' +  ' ' + '\n' +  '**O/U:** ' + OddsOU \
	+ '\n' +  ' ' + '\n' +  '----------------------------------------------------------------- ' \
	+ '\n' + '\n' + '\n' + '\n' + '**Thread Notes:**   ' \
	+ '\n' + '\n' + '- Discuss whatever you wish. You can trash talk, but keep it civil.' \
	+ '\n' + '\n' + '- Turning comment sort to new will help you see the newest posts. ' \
	+ '\n' + '\n' + '- Try [Chrome Refresh](https://chrome.google.com/extensions/detail/aifhnlnghddfdaccgbbpbhjfkmncekmn) or Firefoxs [ReloadEvery](https://addons.mozilla.org/en-US/firefox/addon/115/) to auto-refresh this tab.' \
	+ '\n' + '\n' + '- You may also like [reddit stream](http://www.reddit.com/r/CFB/comments/wn9uj/lets_discuss_game_threads_come_fall/c5esw1u) to keep up with comments. ' \
	+ '\n' + '\n' + '- [Follow @redditCBB](https://twitter.com/redditCBB) on twitter for news, updates, and bad attempts at humor.' \
	+ Subreddits

	scorescraper.posttoreddit(subreddit,title,body,secret,token)

def postupcoming(url,secret,token):
	import scorescraper
	import pandas as pd
	(timedeltas,urls) = scorescraper.getgametimes(url)
	df = pd.DataFrame({'timedeltas': timedeltas, 'urls': urls})
	df2 = df[df['timedeltas'].between(50,59)]
	for index, row in df2.iterrows():
		scorescraper.getcbbthread(row['urls'],secret,token)
		
def rename_duplicates( old ):
	seen = {}
	for x in old:
		if x in seen:
			seen[x] += 1
			yield x + 11
		else:
			seen[x] = 0
			yield x

def posttoreddit(subreddit,title,body,secret,token):
	import praw
	r = praw.Reddit('GameThreadGenerator')
	r.set_oauth_app_info(client_id='toi-mfvVqbptkA',client_secret=secret,redirect_uri='http://127.0.0.1:65010/authorize_callback')
	r.refresh_access_information(token)
	r.submit(subreddit,title,body,send_replies='false')

