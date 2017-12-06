from TelegramBot import settings
import requests,json

TELEGRAM_BOT_TOKEN='491379466:AAGuk7_XH2sMZRpaiAYxw1jyE-xO81VBXsY'
TELEGRAM_API_URL='https://api.telegram.org/bot'+TELEGRAM_BOT_TOKEN+'/'

def setWebhook():
    method_name = 'setWebhook'
    dic = {
        'url': 'http://' + settings.ALLOWED_HOSTS[1]
    }
    requests.post(TELEGRAM_API_URL + method_name, data=dic)

def sendMessage(chat,message,reply_markup=None):
    method_name='sendMessage'
    if reply_markup!=None:
        dic={
            'chat_id':chat['id'],
            'text':message,
            'reply_markup':json.dumps(reply_markup),
        }
    else:
        dic = {
            'chat_id': chat['id'],
            'text': message,
        }
    requests.post(TELEGRAM_API_URL + method_name,data=dic)

def getUpdates():
    method_name='getUpdates'
    r = requests.get(TELEGRAM_API_URL + method_name)
    update=json.loads(r.text)['result']
    return update[len(update)-1]



