from botCore import Telegram_API as API
from botCore import question_module as qs,profile_module as pr, about_module as ab, answer_module as an
from botCore import database_module as ORM


def executeCommands(db,text, user):
    if text == '/start':
        startMethod(db=db,user=user)
        return
    if text == 'Задать вопрос':
        qs.questionMethod(user=user)
        return
    if text[0] == '?' and text.find('id=') >= 0:
        text = text.split(',')
        question = text[0][1:]
        id = text[1][3:-1]
        qs.changeQuestion(db=db,id=id, text=question, user=user)
        return
    if text[0] == '?':
        qs.confirmQuestion(db=db,text=text, user=user)
        return
    if text[0] == '&':
        an.questionList(db=db,text=text,user=user)
    if text[0:2] == 'да':
        id = text[15:][:-1]
        qs.confirmUsingReputation(db=db,id=id, user=user)
        return
    if text == 'нет':
        qs.questionMessage(user=user)
        return
    if text.find('!r=') >= 0 and text.find(',id=') >= 0:
        text = text.split(',')
        reputation = int(text[0][3:])
        id = text[1][3:][:-1]
        qs.setReputationToQuestion(db=db,id=id, reputation=reputation, user=user)
        return
    if text == 'Ответить на вопрос':
        an.answerStartMethod(user=user)
        return
    if text == 'Показать вопросы':
        an.answerMethod(db=db, user=user)
        return
    if text == 'Найти вопрос':
        an.findQuestion(user)
        return
    if text == 'О программе':
        ab.aboutMethod(user=user)
        return
    if text == 'Поделиться Вконтакте':
        ab.shareVk(user)
        return
    if text == 'Профиль':
        pr.profileMethod(db=db,user=user)
        return
    if text == 'Список вопросов':
        pr.getQuestionList(db=db,user=user)
        return
    if text == 'На начало':
        startMethod(db=db,user=user)
        return
    if text.find('repchange') >= 0:
        id = text[13:]
        qs.confirmUsingReputation(db=db,id=id, user=user)
        return
    if text.find('qchange') >= 0:
        id = text[11:]
        pr.changeQuestionMessage(id=id, user=user)
        return
    if text == 'Список отвечающих':
        pr.getRespondentsList(db=db,user=user)
        return
    if text.find('mark='):

        return

def startMethod(db,user):
    id=user['id']
    if db.getUser(id)==None:
        print("OK")
        name=user['first_name']
        reputation=0
        db.setUser(id=id,name=name,reputation=reputation)

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

def runBot():
    offset = 0
    db=ORM.DataBase()
    db.connect()
    while True:
        (commands, users, offset) = API.getUpdates(offset=offset)
        for i in range(len(commands)):
            executeCommands(db=db,text=commands[i], user=users[i])
        offset=int(offset)
        offset += 1
runBot()



