import telebot
from telebot import types
bot = telebot.TeleBot('5976159929:AAFe6Uff5nr5-wUrgCRERp_iLNqwK2lV5LU')
users = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton('Давайте посчитаем')
    markup.row(button_start)
    bot.send_message(message.chat.id, 'Добро пожаловать в бота для расчёта общих расходов. Если несколько человек '
                                      'потратили разные суммы, бот поможет "выйти в ноль", подсказав, кто кому и '
                                      'сколько должен', reply_markup=markup)
    bot.register_next_step_handler(message, ask_amount)

def ask_amount(message):
    bot.send_message(message.chat.id, 'Сколько человек потратили деньги? Напишите цифру от 1 до 100')
    bot.register_next_step_handler(message, set_amount)

def set_amount(message):
    if message.text.isdigit():
        users[message.chat.id] = {'friends_amount': int(message.text), 'list_of_friends': {}}
        print(users)
        ask_names(message)
        #bot.send_message(message.chat.id, 'Введите имя человека №1:')
        #bot.register_next_step_handler(message, count_friends)
    else:
        bot.send_message(message.chat.id, 'Ваш ответ не распознан. Напишите цифру от 1 до 100')
        bot.register_next_step_handler(message, set_amount)

# def count_friends(message):
#     if users.get(message.chat.id):
#         if len(users.get(message.chat.id)['list_of_friends']) != users.get(message.chat.id)['friends_amount']:
#             users[message.chat.id]['list_of_friends'][message.text] = 0
#             if len(users.get(message.chat.id)['list_of_friends']) + 1 <= users.get(message.chat.id)['friends_amount']:
#                 bot.send_message(message.chat.id,
#                                  f"Введите имя человека №{len(users.get(message.chat.id)['list_of_friends']) + 1}: ")
#                 bot.register_next_step_handler(message, count_friends)
#             else:
#                 count_costs(message)

def ask_names(message):
    if users.get(message.chat.id):
        if len(users.get(message.chat.id)['list_of_friends']) != users.get(message.chat.id)['friends_amount']:
            bot.send_message(message.chat.id,
                             f"Введите имя человека №{len(users.get(message.chat.id)['list_of_friends']) + 1}: ")
            bot.register_next_step_handler(message, ask_costs)

            #users[message.chat.id]['list_of_friends'][message.text] = 0
            #if len(users.get(message.chat.id)['list_of_friends']) + 1 <= users.get(message.chat.id)['friends_amount']:
  #              bot.send_message(message.chat.id,
   #                               f"Введите имя человека №{len(users.get(message.chat.id)['list_of_friends']) + 1}: ")
   #             bot.register_next_step_handler(message, count_costs)
        else:
            algebra(message)

def ask_costs(message):
    if message.text not in users[message.chat.id].get('list_of_friends'):
        users[message.chat.id]['list_of_friends'][message.text] = 0
        users[message.chat.id]['temp'] = message.text
        bot.send_message(message.chat.id, f'Сколько потратил {message.text}?')
        bot.register_next_step_handler(message, set_pair)
    else:
        bot.send_message(message.chat.id,
                         f"Вы уже ввели аналогичное имя. Во избежание путаницы, назовите этого человека как-нибудь иначе.")
        ask_names(message)
def set_pair(message):
    if message.text.isdigit():
        users[message.chat.id]['list_of_friends'][users.get(message.chat.id)['temp']] = int(message.text)
        print(users)
        ask_names(message)
    else:
        bot.send_message(message.chat.id, 'Ваш ответ не распознан. Напишите сумму цифрами')
        bot.register_next_step_handler(message, set_pair)


def algebra(message):
    users[message.chat.id]['list_costs'] = []
    users[message.chat.id]['list_costs'] = list(users[message.chat.id]['list_of_friends'].values())
    users[message.chat.id]['list_names'] = []
    users[message.chat.id]['list_names'] = list(users[message.chat.id]['list_of_friends'].keys())
    print(users[message.chat.id]['list_costs'])
    print(users[message.chat.id]['list_names'])
    users[message.chat.id]['list_temp'] = []
    result = {}
    mean = sum(users[message.chat.id].get('list_costs'))/len(users[message.chat.id].get('list_costs'))
    for i in range(len(users[message.chat.id].get('list_costs'))):
        x = mean-users[message.chat.id].get('list_costs')[i]
        users[message.chat.id].get('list_temp').append(x)
    print(users[message.chat.id]['list_temp'])
    print(f'В среднем было потрачено {mean} рублей')
    print(users)
    bot.send_message(message.chat.id, f'В среднем было потрачено {round(mean, 1)} рублей')
    iterate(message)

def find_max(message):
    max = users[message.chat.id].get('list_temp')[0]
    max_number = 0
    for j in range(len(users[message.chat.id].get('list_temp'))):
        if users[message.chat.id].get('list_temp')[j] > max:
            max = users[message.chat.id].get('list_temp')[j]
            max_number = j
    return max, max_number


def find_min(message):
    min = users[message.chat.id].get('list_temp')[0]
    min_number = 0
    for k in range(len(users[message.chat.id].get('list_temp'))):
        if users[message.chat.id].get('list_temp')[k] < min:
            min = users[message.chat.id].get('list_temp')[k]
            min_number = k
    return min, min_number

def iterate(message):
    max, max_number = find_max(message)
    min, min_number = find_min(message)
    if max != 0 and min != 0:
        if max**2 <= min**2:
            a = users[message.chat.id]['list_names'][max_number]
            b = users[message.chat.id]['list_names'][min_number]
            print(f'{a} должен {b} - {round(max, 1)} рублей')
            bot.send_message(message.chat.id,
                             f'{a} ==>> {round(max, 1)} рублей ==>> {b}')
            min = min + max
            max = 0
            users[message.chat.id]['list_temp'][max_number] = max
            users[message.chat.id]['list_temp'][min_number] = min
            print(users[message.chat.id]['list_temp'])
        else:
            a = users[message.chat.id]['list_names'][max_number]
            b = users[message.chat.id]['list_names'][min_number]
            print(f'{a} должен {b} - {round(max, 1)} рублей')
            bot.send_message(message.chat.id,
                             f'{a} ==>> {round(max, 1)} рублей ==>> {b}')
            max = max + min
            min = 0
            users[message.chat.id]['list_temp'][max_number] = max
            users[message.chat.id]['list_temp'][min_number] = min
            print(users[message.chat.id]['list_temp'])
        iterate(message)
    else:
        finish(message)

def finish(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton('Посчитаем ещё раз')
    markup.row(button_start)
    bot.send_message(message.chat.id,
                     f'Больше никто никому ничего не должен', reply_markup=markup)
    bot.register_next_step_handler(message, ask_amount)

def padezh(b):
    all_names = ['саша', 'паша', 'маша']
    all_names2 = ['Саше', 'Паше', 'Маше']
    for i in range(len(all_names)):
        if b.lower() == all_names[i]:
            b = all_names2[i]
    return b

if __name__ == '__main__':
    print("Бот запущен!")
    bot.infinity_polling()

