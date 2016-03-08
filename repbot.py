### IMPORTS
import telebot
import configparser
from dbinterface import DbInterface
import re
import time
###

### INIT

# get config
config = configparser.ConfigParser()
config.read("repbot.cfg")

bot = telebot.TeleBot(config['telegram_bot_api']['telegram_token'])

dbinterface = DbInterface(config['database']['db_path'])

# this is used to filter out messages from before the bot started
time_started = int(time.time())
### 

### EVENT HANDLERS 

@bot.message_handler(commands = ['register'], func = lambda m: m.date >= time_started)
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
@bot.message_handler(regexp = "[\+\-]rep ?[0-9]* ", func = lambda m: m.date >= time_started)
def handle_plus_minus_rep_message(message):

	relevant_section = re.search("[\+\-]rep ?[0-9]* ", message.text).group()

	## finding number
	number_match = re.search("[0-9]*", relevant_section)
	number_to_increment = 1
	if number_match != None:
		number_to_increment = int(number_match.group())
	if relevant_section[0] == "-":
		number_to_increment = -1 * number_to_increment
	print("Number found: {}".format(number_to_increment))
	##
	
	## finding usernames
	usernames = re.findall('@[a-zA-Z0-9]+', message.text)
	usernames = [name[1:] for name in usernames]
	
	print("Usernames found: {}".format(usernames))
	##


###

# wait for events (this should be the very last thing)
print("Bot started!")
bot.polling()