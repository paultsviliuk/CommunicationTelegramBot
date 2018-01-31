from TelegramBot.botCore import Telegram_API as API


def changeQuestion(db,id,text,user):
    user_id=user['id']
    question_id=int(id)
    if db.updateUserQuestion(question_id=question_id,user_id=user_id,text=text):
        message='Вопрос отредактирован'
    else:
        message='Вопроса с таким id у вас нет'
    API.sendMessage(user=user, message=message)


def questionMethod(user):
    message = 'Введите ваш вопрос таким образом.\n?[ваш вопрос]?'
    API.sendMessage(user=user, message=message)

def confirmQuestion(db,text,user):
    question=text[1:len(text)-1]
    user_id=user['id']
    id=db.setQuestion(user_id=user_id,question=question)

    message = 'Использовать репутацию для большего интереса среди ответчиков ?'
    keyboard = {
        'keyboard': [
            [{'text': 'да (id вопроса:'+str(id)+')'}],
            [{'text': 'нет'}],
            [{'text': 'На начало'}]
        ],
        'one_time_keyboard': True
    }
    API.sendMessage(user=user, message=message, reply_markup=keyboard)


def questionMessage(user):
    message='После получения ответа на ваш вопрос обязательно отметьте его. '
    API.sendMessage(user=user, message=message)

def setReputationToQuestion(db,id,reputation,user):
    u=db.getUser(user['id'])
    if reputation>=0:
        if reputation <= u[2]:
            if db.updateQuestionReputation(reputation=reputation,user_id=user['id'],question_id=int(id)):
                message = 'репутация для вопроса установлена'
            else:
                message = 'У вас нет вопроса с таким id'
        else:
            message = 'у вас не хватает репутации'
    else:
        message = 'значение репутации должно быть положительным'

    API.sendMessage(user=user, message=message)
    questionMessage(user=user)

def confirmUsingReputation(db,id,user):
    reputation=db.getUser(user['id'])[2]
    message = 'количество доступной репутации : '+str(reputation)+'\n'+\
        'Id вопроса : '+str(id)+'\n'+\
        'Введите количество репутации для вопроса и id вопроса в таком формате. \n' \
        ' !r=[количество репутации],id=[id вопроса]!'
    API.sendMessage(user=user, message=message)
