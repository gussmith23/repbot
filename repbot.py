import telebot
import configparser
from dbinterface import DbInterface

# get config
config = configparser.ConfigParser()
config.read("babble_bot.cfg")

# create bot with key
bot = telebot.TeleBot(config['telegram_bot_api']['telegram_token'])
