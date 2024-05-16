import os
# import types
from telebot import types
import telebot
import ast
from telebot.util import quick_markup
import json

BOT_TOKEN = "6891204613:AAFQFq9qtS7S4V0MCdHjlZCZLWmYtswYbWo"

stringList = {"LED": "ON", "suhu":"82","servo":"ON", "buzzer":"ON"}


authorize ={"a1560123529":"kipas", "a1467110098":"kipas","a1799522585":"kipas"}


# crossIcon = u"\u274C"

def makeKeyboard():
    markup = types.InlineKeyboardMarkup()

    for key, value in stringList.items():
        if value == "ON":
            value = u"\u2705"
        else:
            try:
                float(value)
                value = value + "°C"
            except:
                value = u"\u274C"
                
        markup.add(types.InlineKeyboardButton(text=key+" "+value,
                                              callback_data="['key', '" + key + "', '" + value + "']"))
    return markup


def makeKeyboardUbah():
    markup = types.InlineKeyboardMarkup()

    for key, value in stringList.items():
        if key == "suhu":
            continue
        if value == "ON":
            value = u"\u2705"
        else:
            try:
                int(value)
                value = value + "°C"
            except:
                value = u"\u274C"
        
        key = "ubah " + key

        markup.add(types.InlineKeyboardButton(text=key+" "+value,
                                              callback_data="['key', '" + key + "', '" + value + "']"))
    return markup

bot = telebot.TeleBot(BOT_TOKEN)
@bot.message_handler(commands=['start', 'hello', 'status', 'id', 'suhu', 'ubah'])
def send_welcome(message): 
    print(message.text[1:])
    if message.text[1:] == 'status':
        f= open("C:/Users/Alienware M17/Desktop/PA/posttest4-praktikum-iot-unmul-2024-main/posttest4-praktikum-iot-unmul-2024-main/posttest4/data.txt", 'r')
        suhu = f.readline()
        suhu = json.loads(suhu.replace("'", '"'))
        suhu = suhu["Temperature"][0:5]
        # print(suhu)
        stringList["suhu"] = suhu
        print(stringList["suhu"])
        print(stringList)
        # text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
        # sent_msg = bot.send_message(message.chat.id, text)
        
        bot.reply_to(message, "Berikut Status LED, suhu, servo dan buzzer", reply_markup=makeKeyboard(),parse_mode="HTML")
        # bot.register_next_step_handler(sent_msg, echo_all)
        # bot.reply_to(message, "berikut adalah status dari iot"+ str(message.id)+ str(message),)
        # return
    elif message.text[1:] == 'id' :
        bot.reply_to(message, "Berikut adalah id tele anda : "+str(message.from_user.id))
        # bot.reply_to(message, f"suhu pada dht anda : {27}°C")
        # bot.reply_to(message, f"")
    elif message.text[1:] == 'suhu' :
        bot.reply_to(message, f"Berikut adalah suhu pada dht anda : {stringList['suhu']}°C")
    elif message.text[1:] == 'ubah' :
        bot.reply_to(message, f"apa yang ingin ada ubah.", reply_markup=makeKeyboardUbah(),parse_mode="HTML")
    # bot.reply_to(message, message.text[1:]+" Howdy, how are you doing?")



@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):

    if (call.data.startswith("['key'")):
        print(f"call.data : {call.data} , type : {type(call.data)}")
        print(f"ast.literal_eval(call.data) : {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        print("berikut adalah id call : "+str(call.from_user.id))
        # for i in range(len(authorize)):
        # print(keyFromCallBack)
        print(valueFromCallBack[:4])
        if valueFromCallBack[:4] == "ubah":
            for key, value in stringList.items():
                if valueFromCallBack[5:] == key :
                    if value == "ON":
                        value = "OFF"
                        valuex = u"\u274C"
                    else:
                        value = "ON"
                        valuex = u"\u2705"
                    bot.answer_callback_query(callback_query_id=call.id,
                                    show_alert=True,
                                    text="kamu menekan " + valueFromCallBack + f" dan {valueFromCallBack[5:]} dalam keadaan " + keyFromCallBack+ " akan menjadi "+valuex)
                    stringList[key] = value
                    print(call.message.chat.id)
                    if key == "LED":
                        f = open("C:/Users/Alienware M17/Desktop/PA/posttest4-praktikum-iot-unmul-2024-main/posttest4-praktikum-iot-unmul-2024-main/posttest4/led1.txt", "w")
                        if value == "ON":
                            f.write("1")
                        else:
                            f.write("0")
                    if key == "servo":
                        f = open("C:/Users/Alienware M17/Desktop/PA/posttest4-praktikum-iot-unmul-2024-main/posttest4-praktikum-iot-unmul-2024-main/posttest4/led3.txt", "w")
                        if value == "ON":
                            f.write("1")
                        else:
                            f.write("0")
                    if key == "buzzer":
                        f = open("C:/Users/Alienware M17/Desktop/PA/posttest4-praktikum-iot-unmul-2024-main/posttest4-praktikum-iot-unmul-2024-main/posttest4/led2.txt", "w")
                        if value == "ON":
                            f.write("1")
                        else:
                            f.write("0")
                    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text= f"apa yang ingin ada ubah.", reply_markup=makeKeyboardUbah(),parse_mode="HTML")
                    
                

        else:
            for key, value in stringList.items():
                if valueFromCallBack == 'suhu':
                    bot.answer_callback_query(callback_query_id=call.id,
                                    show_alert=True,
                                    text="kamu menekan " + valueFromCallBack + f" dan {valueFromCallBack}nya adalah " + keyFromCallBack)
                elif valueFromCallBack == key :
                    bot.answer_callback_query(callback_query_id=call.id,
                                    show_alert=True,
                                    text="kamu menekan " + valueFromCallBack + f" dan {valueFromCallBack} dalam keadaan " + keyFromCallBack)
        
        # if 








        # elif valueFromCallBack == "kipas" :
        #     bot.answer_callback_query(callback_query_id=call.id,
        #                     show_alert=True,
        #                     text="kamu menekan " + valueFromCallBack + " dan kipas dalam keadaan " + keyFromCallBack)
            
        # elif valueFromCallBack == authorize["a"+str(call.from_user.id)] :
        #     bot.answer_callback_query(callback_query_id=call.id,
        #                     show_alert=True,
        #                     text="kamu menekan " + valueFromCallBack + " dan LED dalam keadaan " + keyFromCallBack)
        
        # else:
            # bot.answer_callback_query(callback_query_id=call.id,
            #                 show_alert=True,
            #                 text="anda tidak punya authorize")



        # bot.answer_callback_query(callback_query_id=call.id,
        #                       show_alert=True,
        #                       text="You Clicked " + valueFromCallBack + " and LED is " + keyFromCallBack)

    # if (call.data.startswith("['value'")):
    #     keyFromCallBack = ast.literal_eval(call.data)[1]
    #     del stringList[keyFromCallBack]
    #     bot.edit_message_text(chat_id=call.message.chat.id,
    #                           text="Here are the values of stringList",
    #                           message_id=call.message.message_id,
    #                           reply_markup=makeKeyboard(),
    #                           parse_mode='HTML')
        

# @bot.message_handler(func=lambda msg: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)

bot.infinity_polling()