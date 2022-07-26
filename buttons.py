from telebot import types

#кнопки первого меню
LookBut = types.KeyboardButton("👁Осмотреться👁")
ExitBut = types.KeyboardButton("🚪Выход🚪")
markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markup_1.add(LookBut, ExitBut)

#Кнопка вызова на бой
markup_2 = types.InlineKeyboardMarkup()
markup_2.row_width = 1
callbacktext = "fightwith"
fightbut = types.InlineKeyboardButton(text="Вызвать на бой", callback_data=callbacktext, one_time_keyboard=True)
markup_2.add(fightbut)

#кнопки игры
RockBut = types.KeyboardButton("👊Камень👊")
ScisBut = types.KeyboardButton("✌Ножницы✌")
PapeBut = types.KeyboardButton("✋Бумага✋")
markup_3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_3.row_width = 3
markup_3.add(RockBut, ScisBut, PapeBut, LookBut, ExitBut)
markup_3

#кнопка "принимаешь бой"
markup_4 = types.InlineKeyboardMarkup()
markup_4.row_width = 1
fightYESbut = types.InlineKeyboardButton(text="Принимаю бой", callback_data="fightYES", one_time_keyboard=True)
fightNObut = types.InlineKeyboardButton(text="НЕТ", callback_data="fightNO", one_time_keyboard=True)
markup_4.add(fightYESbut, fightNObut )