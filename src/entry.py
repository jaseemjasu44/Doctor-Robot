from os import stat
import telegram
import subprocess
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
import json
import logging
from expiringdict import ExpiringDict

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

questions = [
    {'Q': "Question 1 is here",
     'A': [
         ("Answer 1", 0),
         ("Answer 2", 1),
         ("Answer 3", 3)]},
    {'Q': "Another question is here",
     'A': [("Just one answer", 2),
           ("wrong answer", 0)]}]

user_status = {}

initial_data = {'stage': 0, 'score': 0}


def entry(bot, update):
    print(user_status)
    print(initial_data)
    try:
        # res = bot.send_message(chat_id="-1001164870268", text=json.dumps(update.to_dict(), indent=2))
        # print(json.dumps(update.to_dict(), indent=2))
        logging.info(update)
        pass
    except Exception as e:
        logging.error(e)
        # bot.send_message(chat_id="-1001164870268", text=str(e))
        pass
    if update.message and update.message.text:
        chat_id = update.message.chat_id
        if chat_id not in user_status:
            user_status[chat_id] = initial_data.copy()
        if update.message.text == "/start":
            user_status[chat_id] = initial_data.copy()
        if update.message.text == "/cancel":
            del user_status[chat_id]
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Operation cancelled. Send /start to continue", reply_markup=ReplyKeyboardRemove())
            return
        if user_status[chat_id]['stage'] > 0:
            answers = questions[(user_status[chat_id]['stage'])-1]['A']
            for a in answers:
                if update.message.text in a:
                    user_status[chat_id]['score'] = user_status[chat_id]['score'] + a[1]
                    break
        if user_status[chat_id]['stage'] < len(questions):
            answers = questions[(user_status[chat_id]['stage'])]['A']
            ans_list = [[i[0]] for i in answers]
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=questions[user_status[chat_id]['stage']]['Q'],
                            reply_markup=ReplyKeyboardMarkup(ans_list))
            user_status[chat_id]['stage'] = user_status[chat_id]['stage']+1
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Score = "+str(user_status[chat_id]['score'])+"\nEnd of questions, Send /start to start over", reply_markup=ReplyKeyboardRemove())
