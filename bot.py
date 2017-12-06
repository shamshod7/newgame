# -*- coding: utf-8 -*-
import redis
import os
import telebot
import math
import random
import threading
import info
from telebot import types
from emoji import emojize
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)



def mobs(callid):
    for id in info.lobby.game:
      if callid in info.lobby.game[id]['players']:
          if callid in info.lobby.game[id]['team1']:
            while len(info.lobby.game[id]['team1'][callid]['mobsinturn'])<3:
              x=random.randint(1,len(info.lobby.game[id]['team1'][callid]['allmobs']))
              if info.lobby.game[id]['team1'][callid]['allmobs'][x-1] not in info.lobby.game[id]['team1'][callid]['mobsinturn']:
                info.lobby.game[id]['team1'][callid]['mobsinturn'].append(info.lobby.game[id]['team1'][callid]['allmobs'][x-1])
          elif callid in info.lobby.game[id]['team2']:
             while len(info.lobby.game[id]['team2'][callid]['mobsinturn'])<3:
               x=random.randint(1,len(info.lobby.game[id]['team2'][callid]['allmobs']))
               if info.lobby.game[id]['team2'][callid]['allmobs'][x-1] not in info.lobby.game[id]['team2'][callid]['mobsinturn']:
                 info.lobby.game[id]['team2'][callid]['mobsinturn'].append(info.lobby.game[id]['team2'][callid]['allmobs'][x-1])
                        



@bot.callback_query_handler(func=lambda call:True)
def inline(call):
  if call.data=='do':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:         
          Keyboard=types.InlineKeyboardMarkup()
          Keyboard.add(types.InlineKeyboardButton(text="Открыть портал", callback_data='altar'))
          Keyboard.add(types.InlineKeyboardButton(text="Главное меню", callback_data='menu'))
          msg=medit('Выберите действие', call.from_user.id, info.lobby.game[id]['players'][call.from_user.id]['lastmessage'], reply_markup=Keyboard)
          info.lobby.game[id]['players'][call.from_user.id]['lastmessage']=msg.message_id
          
          
  elif call.data=='menu':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
          mana=emojize(':droplet:', use_aliases=True)
          Keyboard=types.InlineKeyboardMarkup()
          Keyboard.add(types.InlineKeyboardButton(text="Действия", callback_data='do'))
          Keyboard.add(types.InlineKeyboardButton(text="Окончить ход", callback_data='end'))
          Keyboard.add(types.InlineKeyboardButton(text="Инфо обо мне", callback_data='info'))
          msg=medit('Главное меню:'+"\n"+mana+'Мана: '+str(info.lobby.game[id]['players'][call.from_user.id]['mana'])+'/'+str(info.lobby.game[id]['players'][call.from_user.id]['manamax']), call.from_user.id, info.lobby.game[id]['players'][call.from_user.id]['lastmessage'], reply_markup=Keyboard)
          info.lobby.game[id]['players'][call.from_user.id]['lastmessage']=msg.message_id 
          
          
  elif call.data=='altar':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
          if call.from_user.id in info.lobby.game[id]['team1']:
            Keyboard=types.InlineKeyboardMarkup()
            Keyboard.add(types.InlineKeyboardButton(text="mob1", callback_data=info.lobby.game[id]['team1'][call.from_user.id]['mobsinturn'][0]))
            Keyboard.add(types.InlineKeyboardButton(text="mob2", callback_data=info.lobby.game[id]['team1'][call.from_user.id]['mobsinturn'][1]))
            Keyboard.add(types.InlineKeyboardButton(text="mob3", callback_data=info.lobby.game[id]['team1'][call.from_user.id]['mobsinturn'][2]))
            Keyboard.add(types.InlineKeyboardButton(text="Главное меню", callback_data='menu'))
            msg=medit('В этом ходу вам доступны:', call.from_user.id, info.lobby.game[id]['players'][call.from_user.id]['lastmessage'], reply_markup=Keyboard)
            info.lobby.game[id]['players'][call.from_user.id]['lastmessage']=msg.message_id 
          elif call.from_user.id in info.lobby.game[id]['team2']:
            Keyboard=types.InlineKeyboardMarkup()
            Keyboard.add(types.InlineKeyboardButton(text="mob1", callback_data=info.lobby.game[id]['team2'][call.from_user.id]['mobsinturn'][0]))
            Keyboard.add(types.InlineKeyboardButton(text="mob2", callback_data=info.lobby.game[id]['team2'][call.from_user.id]['mobsinturn'][1]))
            Keyboard.add(types.InlineKeyboardButton(text="mob3", callback_data=info.lobby.game[id]['team2'][call.from_user.id]['mobsinturn'][2]))
            Keyboard.add(types.InlineKeyboardButton(text="Главное меню", callback_data='menu'))
            msg=medit('В этом ходу вам доступны:', call.from_user.id, info.lobby.game[id]['players'][call.from_user.id]['lastmessage'], reply_markup=Keyboard)
            info.lobby.game[id]['players'][call.from_user.id]['lastmessage']=msg.message_id 

     
  elif call.data=='s_me4nik':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if call.from_user.id in info.lobby.game[id]['team1']:
          if info.lobby.game[id]['team1'][call.from_user.id]['mana']>=info.s_me4nik.cost:
            info.lobby.game[id]['team1'][call.from_user.id]['tvari']['s_me4nik']+=1
            info.lobby.game[id]['team1'][call.from_user.id]['mana']-=info.s_me4nik.cost
          else:
            bot.send_message(call.from_user.id, 'Недостаточно маны!')
        elif call.from_user.id in info.lobby.game[id]['team2']:
          if info.lobby.game[id]['team2'][call.from_user.id]['mana']>=info.s_me4nik.cost:
            info.lobby.game[id]['team2'][call.from_user.id]['tvari']['s_me4nik']+=1
            info.lobby.game[id]['team2'][call.from_user.id]['mana']-=info.s_me4nik.cost
          else:
            bot.send_message(call.from_user.id, 'Недостаточно маны!')
            
       
  elif call.data=='tvar1':      
    bot.send_message(call.from_user.id, 'tvar1')
    
  elif call.data=='tvar2':      
    bot.send_message(call.from_user.id, 'tvar2')
            
    
  
def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode='Markdown'):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)

@bot.message_handler(commands=['fight'])
def fightstart(message):
  if message.from_user.id in info.lobby.game:
    if message.chat.id==info.lobby.game[message.from_user.id]['chatid']:
      if info.lobby.game[message.from_user.id]['battle']==0:
        if info.lobby.game[message.from_user.id]['len']%2==0:
          if info.lobby.game[message.from_user.id]['battle']==0:
            bot.send_message(message.chat.id, 'Битва начинается! Приготовьте свою ману...')
            for id in info.lobby.game[message.from_user.id]['players']:
              if len(info.lobby.game[message.from_user.id]['team1'])==len(info.lobby.game[message.from_user.id]['team2']):
                a=random.randint(1,2)
                if a==1:
                  info.lobby.game[message.from_user.id]['team1'][id]=createuser(id, 1)
                else:
                  info.lobby.game[message.from_user.id]['team2'][id]=createuser(id, 1)
              elif len(info.lobby.game[message.from_user.id]['team1'])>len(info.lobby.game[message.from_user.id]['team2']):
                info.lobby.game[message.from_user.id]['team2'][id]=createuser(id, 1)
              else:
                info.lobby.game[message.from_user.id]['team1'][id]=createuser(id, 1)
            info.lobby.game[message.from_user.id]['battle']=1
            btl=threading.Thread(target=battle, args=[message.from_user.id])
            btl.start()
            print(info.lobby.game)
          else:
            bot.send_message(message.chat.id, 'Игра ('+info.lobby.game[message.from_user.id]['name']+') уже была запущена!')
        else:
          bot.send_message(message.chat.id, 'Можно играть только при четном количестве игроков!')

          
          
                     
  

@bot.message_handler(commands=['join'])
def joinm(message):
  for key in info.lobby.game:
    if info.lobby.game[key]['creatorid']['selfid']!=message.from_user.id:
      if info.lobby.game[key]['chatid']==message.chat.id:
       if info.lobby.game[key]['name']!='None':
         if message.from_user.id not in info.lobby.game[key]['players']:
           already=0
           for id in info.lobby.game:                    
             if message.from_user.id in info.lobby.game[id]['players']:
               already=1
               info.lobby.game[id]['players'][message.from_user.id]['cash']=info.lobby.game[id]['name']
           if already==0:
             info.lobby.game[key]['players'][message.from_user.id]=createuser(message.from_user.id, 1)
             info.lobby.game[key]['len']+=1
             bot.send_message(message.chat.id, 'Вы успешно присоединились в игру ('+str(info.lobby.game[id]['players'][message.from_user.id]['cash'])+')! Для начала игры её создатель должен нажать /fight')
           else:
             bot.send_message(message.chat.id, 'Вы уже в другом лобби! ('+info.lobby.game[key]['name']+')!')

           

@bot.message_handler(commands=['cancel'])
def cancelmessage(message):
  if message.from_user.id in info.lobby.game:
    if info.lobby.game[message.from_user.id]['playing']==0:
      cancel(message.from_user.id, message.chat.id)
    else:
      bot.send_message(message.chat.id, 'Игра уже была запущена!')

@bot.message_handler(commands=['start'])
def startmessage(message):
  m=message.from_user.id
  bot.send_message(m, 'Приветствую тебя в игре "MagicWars! Здесь тебе предстоит научиться создавать свои мистические войска и сражаться с друзьями'+
                  ', а так же изучать особенности каждого своего воина! Жми /help, чтобы узнать всё в подробностях') 
                  
                   

@bot.message_handler(commands=['help'])
def helpmessage(message):
  bot.send_message(message.from_user.id, 'Чтобы сыграть в игру, добавьте меня в чат и напишите /begin для начала набора игроков. В одном чате можно запустить несколько игр, но один игрок может присутствовать только в одной из них'+"\n"+      
                   'В этой игре вы играете за одного из магов, который обороняет свою крепость, или нападает на чужую! '+
                   'Чтобы атаковать врага, вы чертите на земле специальные символы, открывая портал, из которого каждый новый ход появляется одно из ваших выбранных '+
                   'существ (для открытия портала требуется мана), которое вступает в бой с существами врагов, и разделавшись с ними, идет в атаку на крепость.'+
                   ' Все существа полностью самостоятельны, вам лишь нужно грамотно выбрать алтари для их появления.'+'Можно играть команда на команду!'+"\n"+'Цель игры: уничтожить крепость соперника')



@bot.message_handler(commands=['begin'])
def beginmessage(message):
  if message.from_user.id not in info.lobby.game:
    info.lobby.game[message.from_user.id]=createlobby(message.chat.id, message.from_user.id)
    print(info.lobby.game)
    bot.send_message(message.chat.id, 'Лобби создано! Назовите его, отправив название следующим сообщением.'+"\n"+'Если вы хотите отменить игру - нажмите /cancel.'+"\n"+'Игра автоматически удалится через 5 минут!')
    info.lobby.game[message.from_user.id]['naming']=1
    lobbycancel=threading.Timer(300.0, cancel, args=[message.from_user.id, message.chat.id])
    
  
  
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
          info.lobby.game[message.from_user.id]['name']=message.text
          bot.send_message(message.chat.id, 'Вы назвали лобби! ('+message.text+').'+"\n"+'Ожидайте второго игрока (/join для присоединения).')
          info.lobby.game[message.from_user.id]['naming']=0  
         else:
          bot.send_message(message.chat.id, 'Недопустимое имя!')
        else:
          bot.send_message(message.chat.id, 'Длина названия не должна превышать 30 символов!')
          
  
def cancel(id, chatid):
  if info.lobby.game[id]['playing']==0:
    info.lobby.game[id].clear()
    del info.lobby.game[id]
    bot.send_message(chatid, 'Лобби удалено!')
  
  

  
  
  
def createlobby(chatid, creatorid):
  return {
    'name':'None',
    'chatid':chatid,
    'creatorid':createuser(creatorid, 1),
    'naming':0,
    'playing':0,
    'players':{creatorid:createuser(creatorid, 1)},
    'battle':0,
    'len':1,
    'team1':{},
    'team2':{},
    

  }
  
  
  
def createuser(id, x):
  return{'selfid':id,
         'lastmessage':0,
         'tvari':{'s_me4nik':0                 
         },
         'mana':0,
         'manamax':100,
         'inlobby':x,
         'cash':'',
         'allmobs':['s_me4nik', 'tvar1', 'tvar2'],
         'mobsinturn':[]
            }  
  

  
def battle(creatorid):
    for id in info.lobby.game[creatorid]['players']:
      if id in info.lobby.game[creatorid]['team1']:
        mobs(id)
        info.lobby.game[creatorid]['team1'][id]['mana']=info.lobby.game[creatorid]['team1'][id]['manamax']
        print(str(info.lobby.game[creatorid]['team1'][id]['mana']))
      elif id in info.lobby.game[creatorid]['team2']:
        mobs(id)
        info.lobby.game[creatorid]['team2'][id]['mana']=info.lobby.game[creatorid]['team2'][id]['manamax']
        print(str(info.lobby.game[creatorid]['team2'][id]['mana']))
      mana=emojize(':droplet:', use_aliases=True)
      Keyboard=types.InlineKeyboardMarkup()
      Keyboard.add(types.InlineKeyboardButton(text="Действия", callback_data='do'))
      Keyboard.add(types.InlineKeyboardButton(text="Окончить ход", callback_data='end'))
      Keyboard.add(types.InlineKeyboardButton(text="Инфо обо мне", callback_data='info'))
      msg=bot.send_message(id, 'Главное меню:'+"\n"+mana+'Мана: '+str(info.lobby.game[creatorid]['players'][id]['mana'])+'/'+str(info.lobby.game[creatorid]['players'][id]['manamax']),reply_markup=Keyboard)
      info.lobby.game[creatorid]['players'][id]['lastmessage']=msg.message_id
      


if __name__ == '__main__':
  bot.polling(none_stop=True)



