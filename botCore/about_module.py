from botCore import Telegram_API as API

def shareVk(user):
    id = user['id']
    message = 'Сделать репост'
    keyboard = {
        'inline_keyboard': [
            [{'text': 'Ответить', 'url': 'http://vk.com/share.php?url={@test_pilot_bot}'}]
        ],
        'one_time_keyboard': True
        }
    API.sendMessage(user=user, message=message, reply_markup=keyboard)


def aboutMethod(user):
    id=user['id']
    message = 'Принципы и польза работы с программой'
    keyboard = {
        'keyboard': [
            [{'text': 'Поделиться Вконтакте'}],
            [{'text': 'На начало'}]
        ],
        'one_time_keyboard': True
    }
    API.sendMessage(user=user, message=message, reply_markup=keyboard)