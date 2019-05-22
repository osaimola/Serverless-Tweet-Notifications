from requests_oauthlib import OAuth1Session
import urllib

# dummy keys, replace with your Twitter keys
CONSUMER_KEY = 'REMINDGKHKDFDSDSSDSDF'
CONSUMER_SECRET = 'juzdandsdFsdFVfvdfVDVDvdgdgdggd'
ACCESS_TOKEN = '9124105652-vNFVfcdc353ndsvf8vdnvfduv8fG'
ACCESS_SECRET = 'EvndhsdFERRdjnvfvGUCCIfdjdfgdgh'

twitter = OAuth1Session(CONSUMER_KEY,
                        client_secret=CONSUMER_SECRET,
                        resource_owner_key=ACCESS_TOKEN,
                        resource_owner_secret=ACCESS_SECRET)

# replace webhook_endpoint with your endpoint enabled to handle crc get requests
webhook_endpoint = urllib.parse.quote_plus('https://yourdomain.com/yourendpoint')
# replace your env with your dev environment
url = 'https://api.twitter.com/1.1/account_activity/all/YOUR_ENV/webhooks.json?url={}'.format(webhook_endpoint)
r = twitter.post(url)
print(r.status_code)
# note your webhook ID which will be present in the response
print (r.content)

url = 'https://api.twitter.com/1.1/account_activity/all/YOUR_ENV/subscriptions.json'
r = twitter.post(url)
print(r.status_code)
print (r.content)
