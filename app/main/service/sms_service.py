import requests
from app.main import Config


def send_one_sms(phone, text):
  account_key = Config.SMS4FREE_KEY
  account_user = Config.SMS4FREE_USER
  account_pass = Config.SMS4FREE_PASSWORD

  url = "https://www.sms4free.co.il/ApiSMS/SendSMS"

  payload={'key' : account_key, 'user' : account_user, 'pass' : account_pass, 'sender' : "HANDSON", 'recipient': phone, 'msg': text}
  headers = {
    'content-type': 'application/json',
    'accept-language': 'en-US,en;q=0.9,he;q=0.8'
  }

  requests.request("POST", url, headers=headers, data=payload)