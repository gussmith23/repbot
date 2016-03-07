### IMPORTS
import telebot
import configparser
from dbinterface import DbInterface
###

### INIT

# get config
config = configparser.ConfigParser()
config.read("repbot.cfg")

bot = telebot.TeleBot(config['telegram_bot_api']['telegram_token'])

dbinterface = DbInterface(config['database']['db_path'])
### 

### EVENT HANDLERS 

# we're searching for '+rep or -rep' with an optional number after it.
@bot.message_handler(regexp = "[\+\-]rep ?[0-9]*")
def handle_plus_minus_rep_message(message):
	print("not implemented")

###

# wait for events (this should be the very last thing)
print("Bot started!")
bot.polling()