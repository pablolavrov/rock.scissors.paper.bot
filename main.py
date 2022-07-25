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
    if message.text == "👁Осмотреться👁":
        if message.chat.first_name in users: #проверка что игрок, есть в нашем словаре игроков
            for user in users:
                if message.chat.first_name != user:
                    bot.send_message(message.chat.id, user, reply_markup=buttons.markup_2)
        else:
            bot.send_message(message.chat.id, "Сначала надо приземлиться, жми /start бродяга!")
    elif message.text == "🚪Выход🚪":
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
    else:
        bot.send_message(message.chat.id, "Моя твоя не понимать.")


@bot.callback_query_handler(func=lambda call: True)
#тут ответные сообщения, которые обрабатываются прогой в результате нажатия кнопок
def callback_inline(call):
    if call.data == 'fightwith': #если нажал кнопку "вызвать на бой"
        if call.message.json["chat"]['first_name'] in users:
            fight_await = "Ты вызвал на бой " + call.message.json["text"]
            bot.send_message(call.from_user.id, fight_await)
            time.sleep(0.5)

            if call.message.json["text"] == "🤖ValeraBot🤖":
                markup_3 = buttons.gameBut(str("🤖ValeraBot🤖"))
                bot.send_message(call.from_user.id, "Он принимает бой, погнали!", reply_markup=markup_3)
            else:
                bot.send_message(call.from_user.id, "Ждем его ответа!")
                User2 = call.message.json["text"]
                fight_request = call.message.json["chat"]['first_name'] + " вызывает тебя на бой!"
                bot.send_message(users[User2][0], fight_request, reply_markup=buttons.markup_4)
        else:
            bot.send_message(call.from_user.id, "Сначала надо приземлиться, жми /start бродяга!")

    elif call.data == "fightYES" or call.data == "fightNO": #принял или не принял бой
        if call.message.json["chat"]['first_name'] in users:
            User1 = call.message.json["text"].split()[0]
            if call.data == "fightYES":
                markup_5 = buttons.gameBut(str(User1))
                bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                              reply_markup=None)
                bot.send_message(call.from_user.id, "Ну погнали!", reply_markup=markup_5)
                time.sleep(0.5)

                markup_6 = buttons.gameBut(str(call.message.json["chat"]["first_name"]))
                bot.send_message(users[User1][0], "Он принимает бой, погнали!" , reply_markup=markup_6)
                time.sleep(0.5)

            if call.data == "fightNO":
                time.sleep(0.5)
                bot.send_message(call.from_user.id, "😼Ну и не надо😼")
                bot.send_message(users[User1][0], "🐣Он струсил, вызови другого🐣")
        else:
            bot.send_message(call.from_user.id, "Сначала надо приземлиться, жми /start бродяга!")
    elif call.data.__contains__("Rock") or call.data.__contains__("Scissors") or call.data.__contains__("Paper"):
        #тут идет обработка выбора камень, ножницы, бумага
        if call.message.json["chat"]['first_name'] in users:
            functions.rsp_game(call)
        else:
            bot.send_message(call.from_user.id, "Сначала надо приземлиться, жми /start бродяга!")

bot.polling(none_stop=True)
