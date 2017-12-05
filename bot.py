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











if __name__ == '__main__':
  bot.polling(none_stop=True)



