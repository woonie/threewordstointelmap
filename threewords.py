#takes three words in the format <word1>.<word2>.<word3> 
#to retrieve latlng coordinates via what3words.com 
#and returns an Ingress Intel Map link with the latlng coordinates

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

import requests
import json

import re

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Send a message in the format "<word1>.<word2>.<word3>" and receive an Ingress Intel Map link with the respective latlng')

def threewords(bot, update):
    addr=update.message.text
    if re.match(".*\..*\..*", addr):
        key="" #obtain from what3words Developer API
        url="https://api.what3words.com/v2/forward?addr="+addr+"&key="+key
        response=requests.get(url)
        content = response.content.decode('utf8')
        data = json.loads(content)

        intel_url = "https://www.ingress.com/intel?ll="
        latlong = str(data['geometry']['lat']) + ',' + str(data['geometry']['lng'])
        update.message.reply_text(intel_url + latlong + "&z=21")
        #currently doesn't support sending error messages if the three words do not give a valid latlng
    else:
        update.message.reply_text("format should be <word1>.<word2>.<word3>")
    logger.info("threewords: " + update.message.text + " " + intel_url + latlong)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    tg_bot_token = "" #obtain from telegram botfather
    updater = Updater(tg_bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    # dp.add_handler(CommandHandler("threewords", threewords))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, threewords))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()