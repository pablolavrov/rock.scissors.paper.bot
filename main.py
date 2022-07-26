import time
import telebot
import buttons
import functions
from data import users, bot

remove = telebot.types.ReplyKeyboardRemove()

@bot.message_handler(commands=["start"])
#при нажатии на старт
def start(message):
    functions.privetsvie(message)

@bot.message_handler()
#здесь ловим команды и сообщения от пользователся
def centr_mes(message):
    remove = telebot.types.ReplyKeyboardRemove()
    if message.text == "👁Осмотреться👁":

        if message.chat.first_name in users: #проверка что игрок, есть в нашем словаре игроков
            bot.send_message(message.chat.id, "Ты смотришь по сторонам и видишь следующих игроков",
                             reply_markup=buttons.markup_1)
            if users[message.chat.first_name][2] != "None":
                opponent_name = users[message.chat.first_name][2]
                text = message.chat.first_name + " покинул бой"
                users[opponent_name][2] = "None"
                users[message.chat.first_name][2] = "None"
                bot.send_message(users[opponent_name][0], text, reply_markup=buttons.markup_1)
            for user in users:
                if message.chat.first_name != user:
                    bot.send_message(message.chat.id, user, reply_markup=buttons.markup_2)
        else:
            bot.send_message(message.chat.id, "Сначала надо приземлиться, жми /start бродяга!")
    elif message.text == "🚪Выход🚪":
        if users[message.chat.first_name][2] != "None":
            opponent_name = users[message.chat.first_name][2]
            text = message.chat.first_name + " покинул бой"
            users[opponent_name][2] = "None"
            users[message.chat.first_name][2] = "None"
            bot.send_message(users[opponent_name][0], text, reply_markup=buttons.markup_1)
        bot.send_message(message.chat.id, "🚀Ты улетел восвояси, теперь никто не доберется до тебя.🚀")
        remove = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Чтобы телепортироваться обратно, нажми нажми /start", reply_markup=remove)
        try:
            users.pop(message.chat.first_name)
            leaving_text = message.chat.first_name + " покинул нас!"
            for user in users:
                if user != "🤖ValeraBot🤖":
                    bot.send_message(users[user][0], leaving_text)
        except:
            pass
    elif message.text == "👊Камень👊" or message.text == "✌Ножницы✌" or message.text == "✋Бумага✋":

        if message.chat.first_name in users:
            bot.send_message(message.chat.id, "Ждем выбор противника!", reply_markup=remove)
            functions.rsp_game(message)
        else:
            bot.send_message(message.chat.id, "Сначала надо приземлиться, жми /start бродяга!", reply_markup=remove)

    else:
        bot.send_message(message.chat.id, "Моя твоя не понимать.", reply_markup=remove)


@bot.callback_query_handler(func=lambda call: True)
#тут ответные сообщения, которые обрабатываются прогой в результате нажатия кнопок

def callback_inline(call):
    # если нажал кнопку "вызвать на бой"
    if call.data == 'fightwith':
        if call.message.json["chat"]['first_name'] in users:
            if call.message.json["text"] == "🤖ValeraBot🤖":
                bot.send_message(call.from_user.id, "Он принимает бой, погнали!", reply_markup=buttons.markup_3)
                users[call.message.json["chat"]['first_name']][2] = "🤖ValeraBot🤖"

            elif users[call.message.json["text"]][2] == "None":
                fight_await = "Ты вызвал на бой " + call.message.json["text"]
                bot.send_message(call.from_user.id, fight_await)
                time.sleep(0.5)
                bot.send_message(call.from_user.id, "Ждем его ответа!")
                User2 = call.message.json["text"]
                fight_request = call.message.json["chat"]['first_name'] + " вызывает тебя на бой!"
                bot.send_message(users[User2][0], fight_request, reply_markup=buttons.markup_4)

            elif users[call.message.json["text"]][2] != "None":
                bot.send_message(call.from_user.id, "Он уже бьется, вызови другого!")

        else:
            bot.send_message(call.from_user.id, "Сначала надо приземлиться, жми /start бродяга!")

    elif call.data == "fightYES" or call.data == "fightNO":
        #принял или не принял бой
        if call.message.json["chat"]['first_name'] in users:
            #вытаскиваем имя оппонента и имя принимающего бой
            opponent_name = call.message.json["text"].split()[0]
            user_name = call.message.json["chat"]['first_name']

            if call.data == "fightYES":
                bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                              reply_markup=None)

                # в словаре users выставляем опонентов
                users[user_name][2] = opponent_name
                users[opponent_name][2] = user_name
                # и зануляем им выбор КНБ на всякий случай
                users[user_name][1] = 0
                users[opponent_name][1] = 0

                bot.send_message(call.from_user.id, "Ну погнали!", reply_markup=buttons.markup_3)
                bot.send_message(users[opponent_name][0], "Он принимает бой, погнали!", reply_markup=buttons.markup_3)
                time.sleep(0.5)

            if call.data == "fightNO":
                time.sleep(0.5)
                bot.send_message(call.from_user.id, "😼Ну и не надо😼")
                bot.send_message(users[User1][0], "🐣Он струсил, вызови другого🐣")
        else:
            bot.send_message(call.from_user.id, "Сначала надо приземлиться, жми /start бродяга!")


bot.polling(none_stop=True)
