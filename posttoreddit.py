import time
import praw
r = praw.Reddit('PRAW related-question monitor by u/_Daimon_ v 1.0.'
                'Url: https://praw.readthedocs.org/en/latest/'
                'pages/writing_a_bot.html')
r.login('airjesse', 'Calee55')
r.submit('test', 'This is just a test for me', text='Hello World!')

'''
	print '[Game Thread] ' , VisitingTeamName,' ',VisitingTeamRecord,' at '+HomeTeamName,' ',HomeTeamRecord,'(',DateTime,')'
	print ' '
	print '---'
	print '###',HomeTeamName,HomeTeamRecord,' at ',VisitingTeamName,VisitingTeamRecord
	print ' '
	print '**Tipoff** ',DateTime
	print ' '
	print '**Venue** ',Stadium
	print ' '
	print '-----------------------------------------------------------------'
	print ' '
	print '**[Join the live IRC chat on freenode, #redditcbb](http://webchat.freenode.net/?channels=#redditcbb)**'
	print ' '
	print '-----------------------------------------------------------------'
	print ' '	
	print '**Television:** '
	print TV[4:]
	print ' '
	print '**Streams** '
	print '[IsTheGameOn?](http://isthegameon.com/)'
	print ' '
	print '**Preview/Follow**'
	print '[Yahoo!](http://sports.yahoo.com',urlname,')'
	print ' '
	print '**Odds '
	print 'Favorite: ',OddsFavorite
	print '**Game Line:** ',OddsSpread
'''	