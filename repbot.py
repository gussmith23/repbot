from urllib.request import urlopen
from urllib.parse import urlencode
import json
import telegram

bot = telegram.Bot(token='90014310:AAH9v9gw8ly737sUyDnnNdK1hEQoduk7uPY')
print(bot.getMe())

last_update = 0 if len(bot.getUpdates()) < 1 else bot.getUpdates()[-1]['update_id'];

while True:
  for update in bot.getUpdates(offset=last_update):
    last_update = update['update_id'] + 1
    print("New last update id:")
    print(last_update)
    print(update)