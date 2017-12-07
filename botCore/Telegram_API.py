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

def sendMessage(user,message,reply_markup=None):
    method_name='sendMessage'
    if reply_markup!=None:
        dic={
            'parse_mode':'Markdown',
            'chat_id':user['id'],
            'text':message,
            'reply_markup':json.dumps(reply_markup),
        }
    else:
        dic = {
            'chat_id': user['id'],
            'text': message,
        }
    requests.post(TELEGRAM_API_URL + method_name,data=dic)

def getUpdates():
    method_name='getUpdates'
    r = requests.get(TELEGRAM_API_URL + method_name)
    update=json.loads(r.text)['result']
    update=update[len(update)-1]

    if update.get('message')!=None:
        return update['message']['text'],update['message']['from']
    if update.get('callback_query')!=None:
        return update['callback_query']['data'], update['callback_query']['from']

    return 0,0


