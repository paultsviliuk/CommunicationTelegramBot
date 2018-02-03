from botCore import Telegram_API as API

def getQuestionList(db,user):
    id=user['id']
    for q in db.getUserQuestions(id=id):
        message = 'Вопрос : ' + q[1]
        message += '\nРепутация вопроса : ' + str(q[2])
        keyboard={
        'inline_keyboard': [
            [{'text':'Редактировать вопрос', 'callback_data': 'qchange, id='+str(q[0])}],
            [{'text': 'Изменить репутацию', 'callback_data': 'repchange, id='+str(q[0])}]
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
        message += '\nПоставить балы отвечающему'
        keyboard1={
            'inline_keyboard':[
                [{'text': '1', 'callback_data': 'mark=1'},
                 {'text': '2', 'callback_data': 'mark=2'},
                 {'text': '3', 'callback_data': 'mark=3'},
                 {'text': '4', 'callback_data': 'mark=4'},
                 {'text': '5', 'callback_data': 'mark=5'}
                 ],
        ],
            'one_time_keyboard': True
        }

        API.sendMessage(user=user, message=message, reply_markup=keyboard1)

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