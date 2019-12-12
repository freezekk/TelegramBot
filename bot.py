import telebot, random
from flask import Flask,request
import os

TOKEN = "966837741:AAERo0ws1miT9ISarbNtsJygHAPF3Z3PDhY"
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)

class Lobby:
    def __init__(self, max_size=10):
        self.players = {}
        self.max_size = max_size

    def add_player(self, player, chat):
        if len(self.players) < self.max_size and player.id not in self.players:
            self.players[player.id] = str(player.username or player.first_name)
            return True
        return False

    def remove_player(self, player):
        if len(self.players) > 0 and player.id in self.players:
            del self.players[player.id]
            return True
        return False

    def get_all_players(self):
        return list(self.players.values())


    def get_random_players(self):
        result = list(self.players.values())
        random.shuffle(result)
        return result

    def get_lobby_size(self):
        return len(self.players)


help_msg = ("You can use /create to create a lobby \n"
            "/join to enter the lobby \n"
            "/leave to leave the lobby \n"
            "/team to create equilibrated teams \n"
            "/teamrandom to create a random teams")

# TODO remove
players_nostri = ["JOHNFET", "21|SAVEGE","FREEZE","DORDE","LUIKZ",
                  "DOOMDAS","OLIVA","RIDA","PERUZ","GIORDY"]

lobby = None

def print_team(players):
    # TODO check vari
    mid = len(players) // 2
    s = ("TEAM 1: " + " ".join(players[:mid])
        + "\nTEAM 2: " + " ".join(players[mid:]))
    return s

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
    elif lobby.get_lobby_size() < 2:
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
    elif lobby.get_lobby_size() < 2:
        bot.reply_to(message, "Not enough members yet, use the command /join to enter the lobby")
    else:
        bot.send_message(chat_id, print_team(lobby.get_random_players()))

@bot.message_handler(commands=["join"]) # Add a player to the lobby
def create_random_team(message):
    global lobby
    chat_id = message.chat.id
    player = message.from_user
    if lobby is None:
        bot.reply_to(message, "You have to create a lobby using the command /create")
    elif lobby.add_player(player, chat_id):
        bot.send_message(chat_id, "Joined correctly as " + lobby.players[player.id])
        #TODO max_size
        bot.send_message(chat_id, "Lobby: " + str(lobby.get_lobby_size()) + "/10")
    else:
        bot.reply_to(message, "You can not join this lobby")

@bot.message_handler(commands=["leave"]) # Add a player to the lobby
def create_random_team(message):
    global lobby
    chat_id = message.chat.id
    player = message.from_user
    if lobby is None:
        bot.reply_to(message, "You have to create a lobby using the command /create")
    elif lobby.remove_player(player):
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
