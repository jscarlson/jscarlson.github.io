import tweepy
from bs4 import BeautifulSoup
from requests import get
from datetime import datetime, timedelta

# twitter variables
consumer_key = 'dsz0AfRwT018gD7gtIplf4aTP'
consumer_secret = 'ez35PdYl9f8PbHJuwcjtd3ZW2SpIhr0XjLZR2tX572OprYvU4I'
access_token = '1083242106871836672-xAlbY3iNkBb0IjXgg8wEv6ZUox9oSZ'
access_token_secret = 'bGLpxZHOn8HDkXah2sR2rZ8bKhDfZW3Nip4X60hDXW4BY'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
user = api.me()

# web-scraping variables
day_window = 7
today = datetime.today().strftime('%Y%m%d')
before_today = (datetime.today() - timedelta(days=day_window)).strftime('%Y%m%d')
start_date = before_today
end_date = today
case_list = []

# web-scraping and html parsing
results_supreme_court = ('https://caselaw.findlaw.com/search.html?search_type=text&court=us-supreme-court'
                         '&text=privacy&date_start=%s&date_end=%s' % (start_date, end_date))
response_supreme_court = get(results_supreme_court)
soup_supreme = BeautifulSoup(response_supreme_court.text, 'html.parser')

# add found cases to array
for case in soup_supreme.select('#srpcaselaw a'):
    print(case['title'], case['href'])
    temp_tuple = ("SUPREME COURT", case['title'], case['href'])
    case_list.append(temp_tuple)

# tweet new cases
if len(case_list) == 0:
    print("nothing this week")
else:
    for case in case_list:
        try:
            api.update_status(case[0] + ": " + case[1] + " See: " + case[2])
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

