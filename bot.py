import telebot, random
from flask import Flask,request
import os

TOKEN = "966837741:AAERo0ws1miT9ISarbNtsJygHAPF3Z3PDhY"
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)

help_msg= "You can use /create for know who play /team for create equilibrated squads /teamrandom for create a random squads"

players=["JOHNFET", "21|SAVEGE","FREEZE","DORDE","LUIKZ","DOOMDAS","OLIVA","RIDA","PERUZ","GIORDY"]

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    bot.reply_to(message, "matteo fagiano dell'anno")

@bot.message_handler(commands=['create']) # welcome message handler
def send_welcome(message):
    bot.reply_to(message, 'questa funzione non e stata ancora implementata')

@bot.message_handler(commands=['team']) # welcome message handler
def send_welcome(message):
    bot.reply_to(message, 'non puoi generare un team senza prima aver creato una partita')

@bot.message_handler(commands=['randomteam']) # welcome message handler
def send_welcome(message):
    chat_id= message.chat.id
    bot.send_message(chat_id,'siamo stronzi: '+players.size()+'e partecipano: '.join(players))
    if(players.size()==0):
        bot.reply_to(message, 'non puoi generare un team senza prima aver creato una partita')
    else:
        random.shuffle(players)
        bot.send_message(chat_id,'siamo in: '+players.size()+'e partecipano: '.join(players))


@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    bot.reply_to(message, help_msg)

@bot.message_handler(func=lambda msg: msg.text is not None and '@' in msg.text)
# lambda function finds messages with the '@' sign in them
# in case msg.text doesn't exist, the handler doesn't process it
def at_converter(message):
    texts = message.text.split()
    at_text = findat(texts)
    if at_text == '@': # in case it's just the '@', skip
        pass
    else:
        insta_link = "https://instagram.com/{}".format(at_text[1:])
        bot.reply_to(message, insta_link)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://telegrambot1233.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
