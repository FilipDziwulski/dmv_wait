import requests
import time
from twilio.rest import Client

WAIT_TIME_TRIGGER = 10
 
# URLs 
url = "https://local.dmv.org/california/branch/san-mateo-dmv-office-2"
ajax_url = "https://local.dmv.org/ajax/WaitTimes/currentTimes?id=593&stateCode=CA"

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "********************************"
auth_token = "*******************************"
twilio_msg_uri = "https://api.twilio.com/2010-04-01/Accounts/" + account_sid + "/Messages"
client = Client(account_sid, auth_token)
 

s = requests.Session()
s.get(url = url)
s.headers.update({'origin': url})

while True:

	r = s.get(url = ajax_url)
 
	# extracting data in json format
	data = r.json()

	wait_time = data['593'][1]

	print(wait_time)

	time.sleep(30)

	if wait_time <= WAIT_TIME_TRIGGER:

		message = client.messages.create(
        "**********",
        body="The San Mateo DMV Wait time is now " + str(wait_time) + " minutes!",
        from_="**********")

		print(message.sid)

		requests.post(twilio_msg_uri, message);

		break