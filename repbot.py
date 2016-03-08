### IMPORTS
import telebot
import configparser
from dbinterface import DbInterface
import re
###

### INIT

# get config
config = configparser.ConfigParser()
config.read("repbot.cfg")

bot = telebot.TeleBot(config['telegram_bot_api']['telegram_token'])

dbinterface = DbInterface(config['database']['db_path'])
### 

### EVENT HANDLERS 

@bot.message_handler(commands = ['register'])
def user_register(message):
	
	print("Attempting to add user {}.".format(message.from_user.username))
	
	added = dbinterface.adduser(userid = message.from_user.id,
															startingrep = 100,
															username = message.from_user.username)
	
	if added:
		bot.reply_to(message, "You are now registered to send and recieve reputation!")
		print("User added.")
	else:
		bot.reply_to(message, "You were already registered!")
		print("User was already registered.")

# we're searching for '+rep or -rep' with an optional number after it.
@bot.message_handler(regexp = "[\+\-]rep ?[0-9]* ")
def handle_plus_minus_rep_message(message):
	print("not implemented")
	print(message)
	usernames = re.findall('@[a-zA-Z0-9]+', message.text)
	


###

# wait for events (this should be the very last thing)
print("Bot started!")
bot.polling()