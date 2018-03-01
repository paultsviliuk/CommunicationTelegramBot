from botCore import Telegram_API as API

def getQuestionList(db,user):
    id=user['id']
    for q in db.getUserQuestions(id=id):
        message = 'Вопрос : ' + q[1]
        message += '\nРепутация вопроса : ' + str(q[2])
        keyboard={
        'inline_keyboard': [
            [{'text':'Редактировать вопрос', 'callback_data': 'qchange, id='+str(q[0])},
             {'text': 'Изменить репутацию', 'callback_data': 'repchange, id=' + str(q[0])}
             ],
        ],
        'one_time_keyboard': True
        }

        API.sendMessage(user=user, message=message,reply_markup=keyboard)

def getRespondentsList(db,user):
    id=user['id']
    for r in db.getRespondetnsList(user_id=id):
        message = 'Вопрос : ' + r[0]
        message += '\nИмя ответчика : ' + r[1]
        message += '\nРепутация вопроса : ' + str(r[2])
        message += '\nОтветил ли он на ваш вопрос ?'
        keyboard1={
            'inline_keyboard':[
                [{'text': 'да', 'callback_data': 'mark=да,uid='+str(r[3])+',qid='+str(r[4])+',r='+str(r[2])}
                 ],
        ],
            'one_time_keyboard': True
        }

        API.sendMessage(user=user, message=message, reply_markup=keyboard1)

def positiveAnswer(db,user,reputation,qid,rid):
    db.deleteRespondentFromQuestion(question_id=int(qid), user_id=int(rid))
    db.deleteQuestion(question_id=qid)
    db.updateReputation(user_id=int(rid),reputation=int(reputation))
    message = 'Ответчик вознагражден,вопрос удален из списка.'
    API.sendMessage(user=user, message=message)



def changeQuestionMessage(id,user):
    message = 'Id вопроса : '+str(id)+'\n' \
              'Введите ваш вопрос таким образом.\n?[ваш вопрос],id=[id вопроса]' \
              '\n Например : ? как дела?,id=15'
    API.sendMessage(user=user, message=message)

def profileMethod(db,user):
    id=user['id']
    qcount=len(db.getUserQuestions(id=id))
    u=db.getUser(id=id)
    message = 'Количество репутации : ' + str(u[2]) + '\n' \
    'Количество вопросов : '+ str(qcount)
    keyboard = {
        'keyboard': [
            [{'text': 'Список вопросов'}],
            [{'text' : 'Список отвечающих'}],
            [{'text': 'На начало'}]
        ],
        'one_time_keyboard': True
    }
    API.sendMessage(user=user, message=message, reply_markup=keyboard)
