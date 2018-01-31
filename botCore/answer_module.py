from TelegramBot.botCore import Telegram_API as API
from TelegramBot.botCore import database_module as ORM

def answerStartMethod(user):
    message="Выберите пункт."
    keyboard = {
        'keyboard': [
            [{'text': 'Показать вопросы'}],
            [{'text': 'Найти вопрос'}],
            [{'text': 'На начало'}]
        ],
        'one_time_keyboard': True
    }
    API.sendMessage(user=user, message=message, reply_markup=keyboard)

def answerMethod(db, user):
    user_id = user['id']
    for ques in db.getAllQuestions(id=user_id):
        message = 'Вопрос : ' + ques[1]
        message += '\nРепутация вопроса : ' + str(ques[2])
        keyboard = {
            'inline_keyboard': [
                [{'text': 'Ответить', 'url': 'https://telegram.me/share/url?url={url}&text={title}'}],
                ],
            'one_time_keyboard': True
        }
        API.sendMessage(user=user, message=message, reply_markup=keyboard)

def findQuestion(user):
    message = 'Введите ваш запрос таким образом.\n&Вопрос или его часть'
    API.sendMessage(user=user, message=message)

def questionList(db,text,user):
    question = text[1:len(text)]
    for quest in db.getQuestionsByWord(id=id, question=question):
        message = 'Вопрос : ' + quest[1]
        message += '\nРепутация вопроса : ' + str(quest[2])
        keyboard = {
            'inline_keyboard': [
                [{'text': 'Ответить', 'url': 'https://telegram.me/share/url?url={url}&text={title}'}],
            ],
            'one_time_keyboard': True
        }
        API.sendMessage(user=user, message=message, reply_markup=keyboard)