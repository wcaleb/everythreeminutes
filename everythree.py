#!/usr/bin/python

import random, twitter # https://github.com/bear/python-twitter
from OAuthSettings import settings

log_file = '/home/wcm1/.e3m'
api_key = settings['consumer_key']
api_secret = settings['consumer_secret']
access_token = settings['access_token_key']
access_token_secret = settings['access_token_secret']

times = ['in the antebellum American South']
times.append('#OnThisDay in ' + random.choice([str(random.randint(1820,1860)), 'history', '#history']))

people   = ['a slave', 'a person', 'an enslaved person', 'someone', 'a black person', 'an African American']
roles    = ['child', 'parent', 'grandparent', 'grandchild', 'friend']
verbs    = ['sold', 'bought', 'purchased', 'traded']
people   = people + [p + r for p in [p + '\'s ' for p in people] for r in roles]

acts = ['someone just']
acts[0] = acts[0] + ' ' + random.choice(verbs) + ' ' + random.choice(people)
acts.append(random.choice(people) + ' was just ' + random.choice(verbs))

delimiters = [', ', '---', '--', ' --- ', ' -- ', ' ']

urls =  ['http://books.google.com/books?id=TUtFgWOISxMC&lpg=PA124&ots=JkLLPw4h9o&pg=PA124#v=onepage&q&f=false', 'http://books.google.com/books?id=-dbFUlQvcRYC&lpg=PP5&ots=rrAzJ_8JYR&pg=PA172#v=onepage&q=minutes&f=false', 'http://books.google.com/books?id=-dbFUlQvcRYC&lpg=PP11&ots=rrAzJ-6IUU&pg=PA292#v=onepage&q=minutes&f=false', 'http://books.google.com/books?id=-dbFUlQvcRYC&lpg=PP11&ots=rrAzJ-6IUU&pg=PA347#v=onepage&q=minutes&f=false', '', '', ''] 

snippets = [random.choice(x) for x in [times, acts]]

string = (random.choice(delimiters)).join(snippets).rstrip('- ,')

tweet =  string[0].upper() + string[1:] + '. ' + random.choice(urls)

# print tweet + random.choice(urls)
# print len(tweet)

# Try to post tweet to Twitter
# Comment out for local testing without posting

l = open(log_file, 'a')
try:
    api = twitter.Api(consumer_key = api_key, consumer_secret = api_secret, access_token_key = access_token, access_token_secret = access_token_secret)
    status = api.PostUpdate(tweet)
except twitter.TwitterError, error:
    l.write('Error\t' + str(error.message) + '\n')
l.close()

