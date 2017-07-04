# coding: utf-8
from time import sleep
import telebot, cv2, threading
import sys
from telebot import types

TOKEN = sys.argv[1]

bot = telebot.TeleBot(TOKEN)

Users_seeing = set([])

#For private content
if len(sys.argv) > 2:
    mychat = int(sys.argv[2])
else:
    mychat = ""

global interval
interval = 10

get_interval = False

vc = cv2.VideoCapture(0)

mainKeyboard = types.ReplyKeyboardMarkup(row_width=1)
mainButton1 = types.KeyboardButton("See")
mainButton2 = types.KeyboardButton("Stop")
mainKeyboard.add(mainButton1, mainButton2)


def get_img():
    vc = cv2.VideoCapture(0)
    if vc.isOpened():
        rval, frame = vc.read()
    vc.release()
    return frame
                        
def save_img(frame):
    cv2.imwrite('prueba.jpg',frame)

def load_img():
    return open('prueba.jpg','rb')

def send_img(userid, frame):
    try:
        bot.send_photo(userid, frame)
    except:
        pass

@bot.message_handler(commands=['start'])
def hello(message):
    print(message.chat.username + " initialized the bot")
    bot.send_message(message.chat.id,
                     "This is a spy bot test.\nThis bot is a initial version with many errors")
    bot.send_message(message.chat.id, "Select a option:", reply_markup=mainKeyboard)

@bot.message_handler(func=lambda msg: msg.text == "See")
def add(message):
    if mychat != "":
        if mychat == message.chat.id:
            Users_seeing.add(message.chat.id)
            bot.send_message(message.chat.id, "From now you will receive photos", reply_markup=mainKeyboard)
            return
    else:
        Users_seeing.add(message.chat.id)
        bot.send_message(message.chat.id, "From now you will receive photos", reply_markup=mainKeyboard)
        return
    bot.send_message(message.chat.id, "You haven't got access to see the content")
    
@bot.message_handler(func=lambda msg: msg.text == "Stop")
def delete(message):
    if mychat != "":
        if mychat == message.chat.id:
            Users_seeing.discard(message.chat.id)
            bot.send_message(message.chat.id, "You won't receive more photos", reply_markup=mainKeyboard)
            return
    else:
        Users_seeing.discard(message.chat.id)
        bot.send_message(message.chat.id, "You won't receive more photos", reply_markup=mainKeyboard)
        return
    bot.send_message(message.chat.id, "You haven't got access to see the content")

#Write a number to change de interval of update, it changes it for all
@bot.message_handler(func=lambda msg: msg.text.isnumeric())
def catch(message):
    global interval
    interval = int(message.text)
    bot.send_message(message.chat.id, str(interval))

        
def updater():
    save_img(get_img())
    print(Users_seeing)
    for uid in Users_seeing:
        frame = load_img()
        send_img(uid, frame)
    print(interval)
    threading.Timer(interval, updater).start()


if __name__ == "__main__":
    updater()
    bot.polling(none_stop=False)


