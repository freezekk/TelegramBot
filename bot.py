import telebot, random
from flask import Flask,request
import os

TOKEN = "966837741:AAERo0ws1miT9ISarbNtsJygHAPF3Z3PDhY"
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)

class Lobby:
    def __init__(self, max_size=10):
        self.players = []
        self.max_size = max_size

    def add_player(self, player):
        if len(self.players) < self.max_size and player not in self.players: 
            self.players.add(player)
            return True
        return False

    def remove_player(self, player):
        if len(self.players) > 0 and player in self.players:
            self.players.remove(player)
            return True
        return False

    def get_random_players(self):
        random.shuffle(self.players)
        return self.players

    def get_lobby_size(self):
        return len(self.players)

help_msg = ("You can use /create to create a lobby"
            "/join to enter the lobby"
            "/leave to leave the lobby"
            "/team to create equilibrated squads"
            "/teamrandom to create a random squads")

# TODO remove
players_nostri = ["JOHNFET", "21|SAVEGE","FREEZE","DORDE","LUIKZ",
                  "DOOMDAS","OLIVA","RIDA","PERUZ","GIORDY"]

lobby = None

@bot.message_handler(commands=["start"]) # welcome message handler
def start_bot(message):
    bot.reply_to(message, help_msg)

@bot.message_handler(commands=["create"]) 
def create_lobby(message):
    # TODO possibility to have different max sizes
    global lobby
    lobby = Lobby()
    bot.reply_to(message, "New lobby created")

@bot.message_handler(commands=["team"]) # Generate a team based on elo
def create_team(message):
    global lobby
    chat_id = message.chat.id
    if lobby is None:
        bot.reply_to(message, "You have to create a lobby using the command /create")
    elif lobby.get_lobby_size < 2:
        bot.reply_to(message, "Not enough members yet, use the command /join to enter the lobby")
    else:
        # TODO implementation
        bot.send_message(chat_id, "Not implemented yet")

@bot.message_handler(commands=["randomteam"]) # Generate a random team
def create_random_team(message):
    global lobby
    chat_id = message.chat.id
    if lobby is None:
        bot.reply_to(message, "You have to create a lobby using the command /create")
    elif lobby.get_lobby_size < 2:
        bot.reply_to(message, "Not enough members yet, use the command /join to enter the lobby")
    else:
        bot.send_message(chat_id, " ".join(lobby.get_random_players()))

@bot.message_handler(commands=["join"]) # Add a player to the lobby
def create_random_team(message):
    global lobby
    chat_id = message.chat.id
    player = message.from_user.id
    if lobby is None:
        bot.reply_to(message, "You have to create a lobby using the command /create")
    elif lobby.add_player(player):
        bot.send_message(chat_id, "Joined correctly")
    else:
        bot.reply_to(message, "You can not join this lobby")
        
@bot.message_handler(commands=["leave"]) # Add a player to the lobby
def create_random_team(message):
    global lobby
    chat_id = message.chat.id
    player = message.from_user.id
    if lobby is None:
        bot.reply_to(message, "You have to create a lobby using the command /create")
    elif lobby.remove_player(player) < 2:
        bot.send_message(chat_id, "Removed from the lobby correctly")
    else:
        bot.reply_to(message, "You can not leave this lobby")


@bot.message_handler(commands=["help"]) # help message handler
def send_help(message):
    bot.reply_to(message, help_msg)


# WebHooks methods, do not modify
@server.route("/" + TOKEN, methods=["POST"])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://telegrambot1233.herokuapp.com/" + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
