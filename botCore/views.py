from django.http import HttpResponse
from botCore import Telegram_API as API
from .models import User,Questions

users=User.objects
questions=Questions.objects

# Create your views here.

def executeCommands(text,user,chat):
        if text=='/start':
            startMethod(chat=chat,user=user)
        if text=='Задать вопрос':
            questionMethod(chat=chat)
        if text[0]=='?' and text[len(text)-1]=='?':
            confirmQuation(text=text,user=user,chat=chat)
        if text[:-2]=='да':
            confirmUsingReputation(id)



#/start
def startMethod(chat,user):
    id=user['id']
    if users.filter(id=id).count()==0:
        name=user['first_name']
        reputation=0
        User(name,reputation,id).save()

    message='Выберите нужный пункт'
    keyboard={
    'keyboard':[
        [{'text':'Задать вопрос'}],
        [{'text':'Ответить на вопрос'}],
        [{'text':'О программе'}],
        [{'text':'Профиль'}]
    ],
    'one_time_keyboard':True
    }
    API.sendMessage(chat=chat,message=message,reply_markup=keyboard)


def questionMethod(chat):
    message = 'Введите ваш вопрос таким образом.\n?[ваш вопрос]?'
    API.sendMessage(chat=chat, message=message)

def confirmQuation(text,user,chat):
    question=text[1:len(text)-1]
    question=Questions(questions.all()[questions.all().count()-1].id+1,question,user['id'],0)
    question.save()
    message = 'Использовать репутацию для большего интереса среди ответчиков ?'
    keyboard = {
        'keyboard': [
            [{'text': 'да (id вопроса:'+str(question.id)+')'}],
            [{'text': 'нет'}]
        ],
        'one_time_keyboard': True
    }
    API.sendMessage(chat=chat, message=message, reply_markup=keyboard)

def confirmUsingReputation(id,user,chat):
    pass

def executeBot(request):
    update = API.getUpdates()
    message = update['message']
    chat = message['chat']
    user = message['from']
    executeCommands(text=message['text'], chat=chat, user=user)
    return HttpResponse("Ok")

