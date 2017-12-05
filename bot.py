# -*- coding: utf-8 -*-
import redis
import os
import telebot
import math
import random
import threading
from telebot import types
token = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(token)



@bot.message_handler(commands=['start'])
def startmessage(message):
  m=message.from_user.id
  bot.send_message(m, 'Приветствую тебя в игре "MagicWars! Здесь тебе предстоит научиться создавать свои мистические войска и сражаться с друзьями'+
                  ', а так же изучать особенности каждого своего воина! Жми /help, чтобы узнать всё в подробностях') 
                  
                   












if __name__ == '__main__':
  bot.polling(none_stop=True)



