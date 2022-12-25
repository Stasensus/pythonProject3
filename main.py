import telebot
from telebot import types
bot = telebot.TeleBot('5976159929:stasensusAAFe6Uff5nr5-wUrgCRERp_iLNqwK2lV5LU')
users = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton('Сейчас посчитаем')
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
        users[message.chat.id] = {'friends_amount': int(message.text)}
        print(users)
        count_friends(message)
    else:
        bot.send_message(message.chat.id, 'Ваш ответ не распознан. Напишите цифру от 1 до 100')
        bot.register_next_step_handler(message, set_amount)

def count_friends(message):
    pass












# list = [100, 50, 200, 500, 300, 400, 0, 650, 300, 500]
# list2 = ['Маша', 'Глаша', 'Петя', 'Серёжа', 'Ваня', 'Стасик', 'Мишка', 'Гришка', 'Автандил Петрович', 'Пётр Абдурахманович']
# slovnik = {'Маша': 100, 'Глаша': 50, 'Петя': 200, 'Серёжа': 500, 'Ваня': 300, 'Стасик': 400, 'Мишка': 0, 'Гришка': 650, 'Автандил Петрович': 300, 'Пётр Абдурахманович': 500}
# list3 = []
# result = {}
# mean = sum(list)/len(list)
# #print(list)
# #print(list2)
# print(slovnik)
# print(f'В среднем было потрачено {mean} рублей')
# for i in range(len(list)):
#     x = mean-list[i]
#     list3.append(x)
# #print(list3)
#
# def find_max():
#     max = list3[0]
#     max_number = 0
#     for j in range(len(list3)):
#         if list3[j] > max:
#             max = list3[j]
#             max_number = j
#     return max, max_number
#
#
# def find_min():
#     min = list3[0]
#     min_number = 0
#     for k in range(len(list3)):
#         if list3[k] < min:
#             min = list3[k]
#             min_number = k
#     return min, min_number
#
# def iterate():
#     max, max_number = find_max()
#     min, min_number = find_min()
#     # print (max, max_number)
#     # print(min, min_number)
#     if max != 0 and min != 0:
#         if max**2 <= min**2:
#             print(f'{list2[max_number]} ===>>> {list2[min_number]} - {round(max, 1)} рублей')
#             min = min + max
#             max = 0
#             list3[max_number] = max
#             list3[min_number] = min
#             #print(list3)
#         else:
#             max = max + min
#             min = 0
#             list3[max_number] = max
#             list3[min_number] = min
#             #print(list3)
#         iterate()

if __name__ == '__main__':
    print("Бот запущен!")
    bot.infinity_polling()