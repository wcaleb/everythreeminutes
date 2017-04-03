#!/usr/bin/python

import csv, os, random, twitter # https://github.com/bear/python-twitter
from PIL import Image
from OAuthSettings import settings

log_file = '/home/wcm1/.e3m'
api_key = settings['consumer_key']
api_secret = settings['consumer_secret']
access_token = settings['access_token_key']
access_token_secret = settings['access_token_secret']

api = twitter.Api(consumer_key = api_key, consumer_secret = api_secret, access_token_key = access_token, access_token_secret = access_token_secret)

count = api.GetUser(screen_name='every3minutes').statuses_count

def log_errors(message):
    l = open(log_file, 'a')
    l.write('Error\t' + str(message) + '\n')
    l.close()

def post_milestone():
    string = 'This account has tweeted ' + str(count) + ' times, each one representing a slave sold in the antebellum United States.'
    try:
       status = api.PostUpdate(string)
    except twitter.TwitterError, error:
       log_errors(error.message)
    exit()

def post_with_image():
    '''
    Periodically, the bot will use this function to post an image of a
    primary source related to a slave sale. We get a random file from the `images/`
    directory and crop it if it is larger than a certain width. We look up metadata
    about the file in a CSV spreadsheet so that a permalink to the full image and
    a name of a person sold (if available) can be included in the tweet.
    '''
    path = '/home/wcm1/everythreeminutes/images/'
    meta = open('/home/wcm1/everythreeminutes/images.csv', 'rU')
    reader = csv.DictReader(meta)
    newdict = {}
    for row in reader:
        newdict.update({row['FILE']:[row['PERMALINK'], row['NAMES']]})
    image = random.choice(os.listdir(path))
    string = 'A person was sold about every 3 minutes in the antebellum era. '
    if newdict[image][1]:
        string = string + 'One was called ' + random.choice(str.split(newdict[image][1], ', ')) + '. '
    string = string + '\n\n' + newdict[image][0]
    j = Image.open(path + image)
    if j.size[0] > 506:
       left = random.randint(0, j.size[0] - 506)
       upper = random.randint(0, j.size[1] - 253)
       j.crop((left, upper, left + 506, upper + 253)).save(path + 'pic_to_tweet.jpeg')
       image = 'pic_to_tweet.jpeg'
    try:
       status = api.PostMedia(string, path + image)
    except twitter.TwitterError, error:
       log_errors(error.message)
    exit()

# Create list of time phrases
times = ['in the antebellum American South', 'in the antebellum United States', 'in the antebellum U.S. South', 'in the antebellum U.S.']
times.append('#OnThisDay in ' + random.choice([str(random.randint(1820,1860)), 'history', '#history']))

# Create lists of people, roles, and verbs
people   = ['a slave', 'a person', 'an enslaved person', 'someone', 'a black person', 'a human being']
roles    = ['child', 'parent', 'grandparent', 'grandchild', 'friend']
verbs    = ['sold', 'bought', 'purchased', 'traded']
people   = people + [p + r for p in [p + '\'s ' for p in people] for r in roles]

# Create passive and active forms of subject-verb-object pairs
acts = ['someone', 'an American', 'a white American', 'a white slaver', 'a white person', 'a slaver']
acts = [a + ' just ' + random.choice(verbs) + ' ' + random.choice(people) for a in acts]
acts.append(random.choice(people) + ' was just ' + random.choice(verbs))

# Create list of delimiters to separate phrases
delimiters = [', ', ',  ', '---', '--', ' --- ', ' -- ', ' ', '  ']

# Create list of URLs for tweets
urls =  [
         'http://books.google.com/books?id=TUtFgWOISxMC&lpg=PA124&ots=JkLLPw4h9o&pg=PA124#v=onepage&q&f=false',
         'http://books.google.com/books?id=-dbFUlQvcRYC&lpg=PP5&ots=rrAzJ_8JYR&pg=PA172#v=onepage&q=minutes&f=false',
         'http://books.google.com/books?id=-dbFUlQvcRYC&lpg=PP11&ots=rrAzJ-6IUU&pg=PA292#v=onepage&q=minutes&f=false',
         'http://books.google.com/books?id=-dbFUlQvcRYC&lpg=PP11&ots=rrAzJ-6IUU&pg=PA347#v=onepage&q=minutes&f=false',
         'https://books.google.com/books?id=bZJJCAAAQBAJ&lpg=PA172&ots=856q5Cdmat&dq=steven%20deyle%20%22startling%20statistic%22&pg=PA172#v=onepage&q=steven%20deyle%20%22startling%20statistic%22&f=false',
         'https://books.google.com/books?id=-dbFUlQvcRYC&lpg=PA292&ots=rrGuP05JVQ&dq=steven%20deyle%20%22the%20magnitude%20of%20this%20number%22&pg=PA292#v=onepage&q=steven%20deyle%20%22the%20magnitude%20of%20this%20number%22&f=false',
         'http://www.owlnet.rice.edu/~wcm1/slave-sales-on-twitter.html',
         'http://docsouth.unc.edu/neh/bibb/ill18.html',
         'http://wcmcdaniel.web.rice.edu/slave-sales-on-twitter.html',
         'http://caleb.mcdaniel.web.rice.edu/slave-sales-on-twitter.html',
         'http://www.slaveryimages.org/details.php?categorynum=6&theRecord=42&recordCount=75',
         '', '', '', '', '', '', '', ''] 

# Get a random item from the times and acts lists; join with delimiters
snippets = [random.choice(x) for x in [times, acts]]
string = (random.choice(delimiters)).join(snippets).rstrip('- ,')

# Generate tweet by adding random URL to string
tweet =  string[0].upper() + string[1:] + '. ' + random.choice(urls)

# Print statements for local testing
# print tweet + random.choice(urls)
# print len(tweet)

# Try to post tweet to Twitter
# Comment out for local testing without posting

if (float(count) % 10000) == 0:
    post_milestone()

if random.randint(0, 200) < 10:
    post_with_image()

try:
    status = api.PostUpdate(tweet)
except twitter.TwitterError, error:
    log_errors(error.message)

