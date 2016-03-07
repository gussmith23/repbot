import telebot
import configparser
from dbinterface import DbInterface

# get config
config = configparser.ConfigParser()
config.read("repbot.cfg")

# create bot with key
bot = telebot.TeleBot(config['telegram_bot_api']['telegram_token'])

dbinterface = DbInterface(config['database']['db_path'])

# wait for events (this should be the very last thing)
print("Bot started!")
bot.polling()