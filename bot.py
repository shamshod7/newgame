# -*- coding: utf-8 -*-
import redis
import os
import telebot
import math
import random
import threading
import info
from telebot import types
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)






  

@bot.message_handler(commands=['join'])
def joinm(message):
  for key in info.lobby.game:
    if info.lobby.game[key]['creatorid']['selfid']!=message.from_user.id:
      if info.lobby.game[key]['chatid']==message.chat.id:
       if info.lobby.game[key]['name']!='None':
        info.lobby.game[key]['player2id']=message.from_user.id
        bot.send_message(message.chat.id, 'Вы успешно присоединились в игру ('+info.lobby.game[key]['name']+')! Для начала игры её создатель должен нажать /fight')
           

@bot.message_handler(commands=['cancel'])
def cancelmessage(message):
  if message.chat.id in info.lobby.game:
    if info.lobby.game[message.chat.id]['playing']==0:
      cancel(message.chat.id)
    else:
      bot.send_message(message.chat.id, 'Игра уже была запущена!')

@bot.message_handler(commands=['start'])
def startmessage(message):
  m=message.from_user.id
  bot.send_message(m, 'Приветствую тебя в игре "MagicWars! Здесь тебе предстоит научиться создавать свои мистические войска и сражаться с друзьями'+
                  ', а так же изучать особенности каждого своего воина! Жми /help, чтобы узнать всё в подробностях') 
                  
                   

@bot.message_handler(commands=['help'])
def helpmessage(message):
  bot.send_message(message.from_user.id, 'Чтобы сыграть в игру, добавьте меня в чат и напишите /begin для начала набора игроков.'+"\n"+
                   'Пока что доступен только режим игры 1 на 1, но в будущих обновлениях будут добавлены командные бои!'+"\n"+"\n"+
                   'В этой игре вы играете за одного из магов, который обороняет свою крепость, или нападает на чужую! '+
                   'Чтобы атаковать врага, вы призываете специальный алтарь, на котором каждый новый ход появляется одно из ваших выбранных '+
                   'существ (для каждого существа свой алтарь), которое вступает в бой с существами врагов, и разделавшись с ними, идет в атаку на крепость.'+
                   ' Все существа полностью самостоятельны, вам лишь нужно грамотно выбрать алтари для их появления.'+"\n"+'Цель игры: уничтожить крепость соперника')



@bot.message_handler(commands=['begin'])
def beginmessage(message):
  if message.from_user.id not in info.lobby.game:
    info.lobby.game[message.from_user.id]=createlobby(message.chat.id, message.from_user.id)
    print(info.lobby.game)
    bot.send_message(message.chat.id, 'Лобби создано! Назовите его, отправив название следующим сообщением.'+"\n"+'Если вы хотите отменить игру - нажмите /cancel.'+"\n"+'Игра автоматически удалится через 5 минут!')
    info.lobby.game[message.from_user.id]['naming']=1
    lobbycancel=threading.Timer(300.0, cancel, args=[message.from_user.id])
    
  
  
@bot.message_handler(content_types=['text'])
def namemessage(message):
  if message.from_user.id in info.lobby.game:
    print('1')
    if info.lobby.game[message.from_user.id]['creatorid']['selfid']==message.from_user.id:
      print('2')
      if info.lobby.game[message.from_user.id]['naming']==1:
        print('3')
        if len(message.text)<31:
         print('4')
         if message.text!='None':
          print('5')
          info.lobby.game[message.from_user.id]['name']=message.from_user.id
          bot.send_message(message.chat.id, 'Вы назвали лобби! ('+message.text+').'+"\n"+'Ожидайте второго игрока (/join для присоединения).')
          info.lobby.game[message.from_user.id]['naming']=0  
         else:
          bot.send_message(message.chat.id, 'Недопустимое имя!')
        else:
          bot.send_message(message.chat.id, 'Длина названия не должна превышать 30 символов!')
          
  
def cancel(id):
  if info.lobby.game[id]['playing']==0:
    info.lobby.game[id].clear()
    del info.lobby.game[id]
    bot.send_message(id, 'Лобби удалено!')
  
  

  
  
  
def createlobby(chatid, creatorid):
  return {
    'name':'None',
    'chatid':chatid,
    'creatorid':createuser(creatorid),
    'naming':0,
    'playing':0,
    'player2id':0,
  }
  
  
  
  
def createuser(id):
  return{
    'selfid':0
  }



if __name__ == '__main__':
  bot.polling(none_stop=True)



