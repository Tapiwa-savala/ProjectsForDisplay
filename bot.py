import requests
import json
from telegram.ext import Updater , CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
#------------JSON FORMAT---------------------------
#   {"ok":true,
#   "result":[{"update_id":931053850,
#   "message":{"message_id":4,"from":{"id":1309397409,"is_bot":false,"first_name":"Tapiwa","last_name":"Savala"},
#   "chat":{"id":-656541255,"title":"Family Motivation","type":"group","all_members_are_administrators":true}, 
#   "date":1639486699,
#   "text":"/my_id @TapsMotivationBot",
#   "entities":[{"offset":0,"length":6,"type":"bot_command"},{"offset":7,"length":18,"type":"mention"}]}}]}
#---------------------------------------------------

#https://api.telegram.org/bot5019890198:AAF5MJMmo8HWl9YhwiHLF5vyaQHKU0tPJNM/getUpdates

telegram_bot_token = "5019890198:AAF5MJMmo8HWl9YhwiHLF5vyaQHKU0tPJNM"
updater = Updater(token = telegram_bot_token, use_context= True)
dispatcher = updater.dispatcher

def greet(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="WAAAAAAAAAASSSSSSUUUUUUUP")

def convert(update,context):
    if len(context.args) < 2 :
        context.bot.send_message(chat_id=update.effective_chat.id, text = "the format is /greet <from currency> <to currency> <amount>")
    else:    
        curr_1 = context.args[0]
        curr_2 = context.args[1]
        amount = context.args[2]
        url = "https://currency-converter5.p.rapidapi.com/currency/convert"
        querystring = {"format":"json","from":curr_1,"to":curr_2,"amount":amount}
        headers = {
            'x-rapidapi-host': "currency-converter5.p.rapidapi.com",
            'x-rapidapi-key': "4e4c2b438emsh7844dac41dabf89p1e79ebjsn2816c81a97cf"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response)
        response_data = response.json()
        if response_data["status"] == "success":
            result = curr_1 + " "+ amount +" ---> " + curr_2 + " " + response_data["rates"][curr_2.upper()]["rate_for_amount"]
            context.bot.send_message(chat_id = update.effective_chat.id, text = result)
        else:
            context.bot.send_message(chat_id = update.effective_chat.id, text = "incorrect currency code")


def start(update,context):
    introduction = "Welcome Family & Friends \U0001F970, You can enter the following commands:\n"
    introduction = introduction + "/greet - to have me greet you"
    context.bot.send_message(chat_id=update.effective_chat.id, text=introduction)

def inline_help(update,context):
    query = update.inline_query.query
    if not query:
        return
    introduction = "Welcome Family & Friends \U0001F970, You can enter the following commands:\n"
    introduction = introduction + "/greet - to have me greet you"    
    results = []
    results.append(
        InlineQueryResultArticle(
            id = query.upper(),
            title = "Help",
            input_message_content = InputTextMessageContent(introduction)
        )
    )
    context.bot.answer_inline_query(update.inline_query.id,results)

convert_handler = CommandHandler('convert',convert)
dispatcher.add_handler(convert_handler)

start_handler = CommandHandler('start',start)
dispatcher.add_handler(start_handler)  

greeting_handler = CommandHandler('greet',greet)
dispatcher.add_handler(greeting_handler)

inline_help_handler = InlineQueryHandler(inline_help)
dispatcher.add_handler(inline_help_handler)

updater.start_polling()

