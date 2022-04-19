from twilio.rest import Client
from decouple import config

account_sid = config('sid', default='')
auth_token = config('authToken', default='')
client = Client(account_sid, auth_token)

def sendText(message,phone):
  message = client.messages.create(
      messaging_service_sid='MG1f2aacd108e1a720ae9c3a4ee9400921',
      body=message,
      to=phone
  )
  print(message.sid)


sendText('Harvard scrape has finished!', '+16265608207')
