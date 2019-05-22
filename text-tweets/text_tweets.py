import os
import base64
import hashlib
import hmac
import json
import tweepy
import urllib
from twilio.request_validator import RequestValidator


def lambda_handler(event, context):
    print("received: " + str(event))
    # if twilioSignature exists, create a validator & a dictionary of received data
    if u'twilioSignature' in event and u'Body' in event:
        form_parameters = {
            key: urllib.parse.unquote_plus(value) for key, value in event.items()
            if key != u'twilioSignature'
        }

        validator = RequestValidator(os.environ['AUTH_TOKEN'])

        # validate api call is from twilio
        request_valid = validator.validate(
            os.environ['REQUEST_URL'],
            form_parameters,
            event[u'twilioSignature']
        )

        # if request valid, authenticate tweepy and send tweet
        if request_valid:
            auth = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['API_SECRET'])
            auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_SECRET'])
            api = tweepy.API(auth)
            api.update_status(event['Body'])

            return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>' \
                   '<Response><Message>Request Received, OK!</Message></Response>'

        # if request is not from twilio, give appropriate response
        else:
            return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>' \
                   '<Response><Message>Nice Try...</Message></Response>'
