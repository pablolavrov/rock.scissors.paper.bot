import buttons
import random
import time
import telebot
from data import users,  bot


def play(User1_name, User1_choise, User2_name, User2_choise): #функция игры камень, ножницы бумага
    if User1_choise == User2_choise:
        return "zero"
    if (User1_choise == "Rock" and User2_choise == "Scissors") or (User1_choise == "Paper" and User2_choise == "Rock") or \
            (User1_choise == "Scissors" and User2_choise == "Paper"):
        return [User1_name, User2_name]
    return [User2_name, User1_name]


def choise(x): #генерит текст выбора
    if x == "Rock":
        return " выбрал 👊Камень👊"
    if x == "Scissors":
        return " выбрал ✌Ножницы✌"
    if x == "Paper":
        return " выбрал ✋Бумага✋"

def privetsvie(message): #приветсвие
    enter_text = "К нам прибыл " + message.chat.first_name
    for user in users:
        if user != "🤖ValeraBot🤖":
            bot.send_message(users[user][0], enter_text)
    users[message.chat.first_name] = [message.chat.id, 0]
    bot.send_message(message.chat.id, "🪐Ты оказался на планете КаменьНожницыБумага!🪐")
    time.sleep(0.5)
    bot.send_message(message.chat.id, "🦍🐙🐵🐲 Вокруг бродят игроки со всей вселенной," \
                                      "\nготовые сразиться с тобой  в 'Цу Ее Фа'👊✌✋.")
    time.sleep(0.5)
    bot.send_message(message.chat.id, "Жми '👁Осмотреться👁', чтобы выбрать соперника.🤼")
    time.sleep(0.5)
    bot.send_message(message.chat.id, "Также всегда есть робот Валера🤖", reply_markup=buttons.markup_1)


def result_func(User1_name, User2_name):
    vibor_text1 = User2_name + (choise(users[User2_name][1]))
    vibor_text2 = User1_name + (choise(users[User1_name][1]))
    if User1_name != "🤖ValeraBot🤖":
        bot.send_message(users[User1_name][0], vibor_text1)
    if User2_name != "🤖ValeraBot🤖":
        bot.send_message(users[User2_name][0], vibor_text2)
    users[User1_name][1] = 0
    users[User2_name][1] = 0
    markup_8 = buttons.gameBut(str(User2_name))
    markup_9 = buttons.gameBut(str(User1_name))
    time.sleep(0.5)
    if User1_name != "🤖ValeraBot🤖":
        bot.send_message(users[User1_name][0], "🥳Ты выиграл!🥳")
        time.sleep(0.5)
        bot.send_message(users[User1_name][0], "Еще разок?", reply_markup=markup_8)
    if User2_name != "🤖ValeraBot🤖":
        time.sleep(0.5)
        bot.send_message(users[User2_name][0], "😭Ты проиграл😭")
        time.sleep(0.5)
        bot.send_message(users[User2_name][0], "Еще разок?", reply_markup=markup_9)


def zero_result(User1_name, User2_name):
    # обнуляем глобальный словарь
    users[User1_name][1] = 0
    users[User2_name][1] = 0
    # запускаем новую игру
    markup_11 = buttons.gameBut(User2_name)
    bot.send_message(users[User1_name][0], "🤝Ничья!🤝")
    time.sleep(0.5)
    bot.send_message(users[User1_name][0], "Погнали заново!", reply_markup=markup_11)
    if User2_name != "🤖ValeraBot🤖":
        markup_10 = buttons.gameBut(User1_name)
        bot.send_message(users[User2_name][0], "🤝Ничья!🤝")
        time.sleep(0.5)
        bot.send_message(users[User2_name][0], "Погнали заново!", reply_markup=markup_10)


def rsp_game(call):
    # задаем удобные имена игроков и результата
    User1_name = call.message.json["chat"]["first_name"]
    User1_choise = call.data.split()[0]
    User2_name = call.data.split()[1]
    User2_choise = users[call.data.split()[1]][1]
    # меняем значение этому юзеру1 в глобальном словаре
    users[User1_name][1] = call.data.split()[0]
    # отправляем сообщение о выборе и удаляем кнопки
    bot.edit_message_reply_markup(chat_id=users[User1_name][0], message_id=call.message.message_id,
                                  reply_markup=None)
    bot.send_message(users[User1_name][0], ("Ты " + choise(call.data.split()[0])))
    time.sleep(0.5)
    bot.send_message(users[User1_name][0], "Ждем выбор противника!")

    time.sleep(0.5)

    # проверка на валеру, если опонент валера, то запускаем игру с рандомом
    if User2_name == "🤖ValeraBot🤖":
        User2_choise = random.choice(["Rock", "Scissors", "Paper"])
        users["🤖ValeraBot🤖"][1] = User2_choise

    # проверяем сходил ли опонент, если да, то запускаем игру и проверки результата
    if User2_choise != 0:
        result = play(User1_name, User1_choise, User2_name, User2_choise)
        if result == "zero":
            zero_result(User1_name, User2_name)
        elif result == [User1_name, User2_name]:
            result_func(User1_name, User2_name)
        elif result == [User2_name, User1_name]:
            result_func(User2_name, User1_name)
