from django.http import HttpResponse
from botCore import Telegram_API as API
from .models import User,Questions

users=User.objects
questions=Questions.objects

# Create your views here.

def executeCommands(text,user):
        if text=='/start':
            startMethod(user=user)
        if text=='Задать вопрос':
            questionMethod(user=user)
        if text[0]=='?' and text[-1]=='?':
            confirmQuation(text=text,user=user)
        if text[0:2]=='да':
            id=text[15:][:-1]
            confirmUsingReputation(id=id,user=user)
        if text=='нет':
            questionMessage(user=user)
        if text.find('!r=')>=0 and text.find(',id=')>=0 and text[-1]=='!':
            text=text.split(',')
            reputation=int(text[0][3:])
            id=text[1][3:][:-1]
            setReputationToQuestion(id=id,reputation=reputation,user=user)
        if text=='Профиль':
            profileMethod(user=user)
        if text=='Список вопросов':
            getQuestionList(user=user)
        if text=='на начало':
            startMethod(user=user)

def startMethod(user):
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
    API.sendMessage(user=user,message=message,reply_markup=keyboard)


def profileMethod(user):
    u = users.get(id=user['id'])
    qcount=questions.filter(user=u).count()
    message = 'Количество репутации : ' + str(u.reputation) + '\n' \
    'Количество вопросов : ' + str(qcount)
    keyboard = {
        'keyboard': [
            [{'text': 'Список вопросов'}],
            [{'text': 'На начало'}]
        ],
        'one_time_keyboard': True
    }
    API.sendMessage(user=user, message=message, reply_markup=keyboard)

def changeQuestion(id,text,user):



def questionMethod(user):
    message = 'Введите ваш вопрос таким образом.\n?[ваш вопрос]?'
    API.sendMessage(user=user, message=message)

def confirmQuation(text,user):
    question=text[1:len(text)-1]
    question=Questions(questions.all()[questions.all().count()-1].id+1,question,user['id'],0)
    question.save()
    message = 'Использовать репутацию для большего интереса среди ответчиков ?'
    keyboard = {
        'keyboard': [
            [{'text': 'да (id вопроса:'+str(question.id)+')'}],
            [{'text': 'нет'}],
            [{'text': 'На начало'}]
        ],
        'one_time_keyboard': True
    }
    API.sendMessage(user=user, message=message, reply_markup=keyboard)

def questionMessage(user):
    message='После получения ответа на ваш вопрос обязательно отметьте его. '
    API.sendMessage(user=user, message=message)

def confirmUsingReputation(id,user):
    reputation=users.get(id=user['id']).reputation
    message = 'количество доступной репутации : '+str(reputation)+'\n'+\
        'Id вопроса : '+str(id)+'\n'+\
        'Введите количество репутации для вопроса и id вопроса в таком формате. \n' \
        ' !r=[количество репутации],id=[id вопроса]!'
    API.sendMessage(user=user, message=message)

def setReputationToQuestion(id,reputation,user):
    u=users.get(id=user['id'])
    question=questions.filter(id=id,user=u)
    if question!=0:
        question=question[0]
        if reputation<=u.reputation:
            u.reputation-=reputation
            u.save()
            question.reputation=reputation
            question.save()
            message='репутация для вопроса установлена'
        else:
            message = 'у вас не хватает репутации'
    else:
        message = 'У вас нет вопроса с таким id'
    API.sendMessage(user=user, message=message)
    questionMessage(user=user)

def getQuestionList(user):
    u=users.get(id=user['id'])
    message='\n\n'
    for q in questions.filter(user=u) :
        q='Вопрос : '+ q.question+'\n' \
        'Репутация : ' + str(q.reputation) + '\n' \
        'id Вопроса : ' + str(q.id) + '\n\n\n'
        message+=q
    API.sendMessage(user=user, message=message)

def executeBot(request):
    update = API.getUpdates()
    message = update['message']
    user = message['from']
    executeCommands(text=message['text'], user=user)
    return HttpResponse("Ok")

