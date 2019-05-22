def crc(event, context):
    """ Returns a CRC (Challenge Response Check) to keep this webhook
    secure. https://goo.gl/kFdJgV for more details.
    Also takes account activity events from twitter and sends an sms notification if SEND_NOTIFICATIONS is True"""
    # Short circuit ping from CloudWatch Events
    if event.get('source', None) == 'aws.events':
        print('ping')
        return

    # If request is a GET method, handle CRC request as documented by Twitter
    if event['httpMethod'] == 'GET':
        import base64
        import hmac
        import hashlib
        import os
        import json

        print(str(event))
        print('Calculating CRC')
        crc = event['queryStringParameters']['crc_token']
        sha256_hash_digest = hmac.new(
            os.environ['API_SECRET'].encode('utf-8'), msg=crc.encode('utf-8'),
            digestmod=hashlib.sha256).digest()

        body = json.dumps({'response_token': 'sha256=' +
                                             base64.b64encode(sha256_hash_digest).decode('utf-8')})
        print('Body response: {}'.format(body))
        response = {
            'statusCode': 200,
            'body': body
        }
        return response

    # If request is POST, handle account activity event from twitter
    if event['httpMethod'] == 'POST':
        import os
        import json

        print("EVENT!!!!" + str(event))
        body = json.loads(event['body'])

        # If we want to forward notifications and this is a direct message event
        if os.environ['SEND_NOTIFICATIONS'] == 'True' and 'direct_message_events' in body:

            # If the sender of the direct message is not me, forward notification
            sender_id = body['direct_message_events'][0]['message_create']['sender_id']
            if sender_id != os.environ['MY_TWITTER_ID']:

                # importing requests takes a while (>3 seconds may cause timeout fail or increased AWS costs)
                # requests a better alternative to twilio.rest.Client. smaller package size for Lambda
                import requests
                dm = "@" + body['users'][sender_id]['screen_name'] + ": "
                dm += body['direct_message_events'][0]['message_create']['message_data']['text']
                # Use twilio to send an sms notification
                print ("HANDLING FOR TWILIO: " + dm)
                response = requests.post(
                    "https://api.twilio.com/2010-04-01/Accounts/"+os.environ['TWILIO_ACCOUNT_SID']+"/Messages.json",
                    headers={"Content-Type": "application/x-www-form-urlencoded"
                             },
                    data={
                        "From": os.environ['TWILIO_NUMBER'],
                        "To": os.environ['MY_NUMBER'],
                        "Body": dm
                    },
                    auth=(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
                    )

                print("SEND UPDATE STATUS: " + response.status)

            content = "direct message event received"

        else:
            print("EVENT RECEIVED AND IGNORED")
            content = "no"

        return {
            'statusCode': 200,
            'body': content
        }
