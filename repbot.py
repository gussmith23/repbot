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

rep_command_regex = "[\+\-][0-9]* ?rep ?[0-9]*"
### 

### EVENT HANDLERS 
@bot.message_handler(commands = ['getrep'], func = lambda m: m.date >= time_started)
def user_register(message):
	rep = dbinterface.getrep(message.from_user.username)
	
	if rep == False:
		bot.reply_to(message, "You are not registered! Have you used the 'register' command?")
	else:
		bot.reply_to(message, "Your reputation is {}.".format(rep))

@bot.message_handler(commands = ['register'], func = lambda m: m.date >= time_started)
def user_register(message):
	
	print("Attempting to add user {}.".format(message.from_user.username))
		
	if message.from_user.username == None or message.from_user.username == "":
		bot.reply_to(message, "Please add a username before registering.")
		print("User needed username.")
		return
	
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
@bot.message_handler(regexp = rep_command_regex, func = lambda m: m.date >= time_started)
def handle_plus_minus_rep_message(message):

	relevant_section = re.search(rep_command_regex, message.text).group()
	
	# check if sending user is registered.
	if dbinterface.getrep(message.from_user.username) == False:
		bot.reply_to(message, "Please register using the 'register' command first.")
		print("Unregistered user {} tried to use +rep".format(message.from_user.username))
		return
		
	## finding number
	# this will find the FIRST number in the message
	number_match = re.search("[0-9]{1-3}", relevant_section)
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

	for username in usernames:	
		if number_to_increment >= 0:
			# add rep to reciever, take rep from giver (but only if add rep succeeds!)
			if dbinterface.incrementrep(username, number_to_increment):
				dbinterface.incrementrep(message.from_user.username, -1*number_to_increment)
				print("{} gave {} rep to {}.".format(message.from_user.username, number_to_increment, username))
			else:
				print("Username {} not found; no rep changed.".format(username))
				
		else:
			dbinterface.incrementrep(username, number_to_increment)

###

# wait for events (this should be the very last thing)
print("Bot started!")
bot.polling()