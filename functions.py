import buttons
import random
import time
import telebot
from data import users,  bot

def privetsvie(message): #приветсвие
    enter_text = "К нам прибыл " + message.chat.first_name
    for user in users:
        if user != "🤖ValeraBot🤖":
            bot.send_message(users[user][0], enter_text)
    users[message.chat.first_name] = [message.chat.id, 0, "None"]
    bot.send_message(message.chat.id, "🪐Ты оказался на планете КаменьНожницыБумага!🪐")
    time.sleep(0.5)
    bot.send_message(message.chat.id, "🦍🐙🐵🐲 Вокруг бродят игроки со всей вселенной," \
                                      "\nготовые сразиться с тобой  в 'Цу Ее Фа'👊✌✋.")
    time.sleep(0.5)
    bot.send_message(message.chat.id, "Жми '👁Осмотреться👁', чтобы выбрать соперника.🤼")
    time.sleep(0.5)
    bot.send_message(message.chat.id, "Также всегда есть робот Валера🤖", reply_markup=buttons.markup_1)


def game_func(User1_choise, User2_choise):
    if User1_choise == User2_choise:
        return "🤝Ничья!🤝"
    if (User1_choise == "👊Камень👊" and User2_choise == "✌Ножницы✌") or (
            User1_choise == "✋Бумага✋" and User2_choise == "👊Камень👊") or \
            (User1_choise == "✌Ножницы✌" and User2_choise == "✋Бумага✋"):
        return "🥳Ты выиграл!🥳"
    return "😭Ты проиграл😭"

def rsp_game(message):
    # задаем удобные имена игроков и результата
    User1_name = message.chat.first_name
    User1_choise = message.text
    User2_name = users[message.chat.first_name][2]
    User2_choise = users[User2_name][1]

    # меняем значение этому юзеру1 в глобальном словаре
    users[User1_name][1] = message.text
    time.sleep(0.5)

    # проверка на валеру, если опонент валера, то запускаем игру с рандомом
    if User2_name == "🤖ValeraBot🤖":
        User2_choise = random.choice(["👊Камень👊", "✌Ножницы✌", "✋Бумага✋"])
        text_valera = "У Валеры " + User2_choise
        bot.send_message(users[User1_name][0], text_valera)
        time.sleep(0.5)
        bot.send_message(users[User1_name][0], game_func(User1_choise, User2_choise))
        bot.send_message(users[User1_name][0], "Еще разок?", reply_markup=buttons.markup_3)

    # проверяем сходил ли опонент, если да, то запускаем игру и проверки результата
    elif User2_choise != 0:
        bot.send_message(users[User1_name][0], game_func(User1_choise, User2_choise))
        bot.send_message(users[User2_name][0], game_func(User2_choise, User1_choise))
        users[User1_name][1] = 0
        users[User2_name][1] = 0

        bot.send_message(users[User1_name][0], "Еще разок?", reply_markup=buttons.markup_3)
        bot.send_message(users[User2_name][0], "Еще разок?", reply_markup=buttons.markup_3)

