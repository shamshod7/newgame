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

def mobdmg(mob, creatorid, team, team2, number):
    for mob2 in info.lobby.game[creatorid][team2]:
              print('1')
              for number2 in info.lobby.game[creatorid][team2][mob2]:
                  print('2')
                  info.lobby.game[creatorid][team][mob][number]['koef']=info.lobby.game[creatorid][team2][mob2][number2]['fromdeaddmg']
                  if info.lobby.game[creatorid][team][mob][number]['koef']>info.lobby.game[creatorid][team][mob][number]['maxkoef']:
                      print('3')
                      if info.lobby.game[creatorid][team2][mob2][number2]['hp']>0:
                        print('4')
                        info.lobby.game[creatorid][team][mob][number]['maxkoef']=info.lobby.game[creatorid][team][mob][number]['koef']
                        info.lobby.game[creatorid][team][mob][number]['target']=info.lobby.game[creatorid][team2][mob2][number2]
                        t=info.lobby.game[creatorid][team2][mob2][number2]
                        
    return t  


def typetotext(name):
    if name=='dead':
        text='Мертвец'
    elif name=='electro':
        text='Электро'
    elif name=='fire':
        text='Огненный'
    elif name=='bio':
        text='Биологический'
    elif name=='ghost':
        text='Призрачный'
    return text
        



def mobturn(mob, creatorid, team, team2):
    if mob=='s_me4nik':
        print('10')
        for number in info.lobby.game[creatorid][team][mob]:
         print('11')
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
           print('12')
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
             print('13')
             t=mobdmg(mob, creatorid, team, team2, number)
             t['underattack']=1
             if t['skill']!='returndmg':
              z=random.randint(1,100)
              if z<=15:
                  t['fromdeaddmg']+=0.6
                  skilltext=', применив скилл "Проклятье мертвецов"'
              else:
                  skilltext=''
              dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromdeaddmg']
              t['hp']-=dmg
              if team=='t1mobs':
                info.lobby.game[creatorid]['resultst1']+=info.lobby.game[creatorid][team][mob][number]['name']+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' нанёс '+str(dmg)+' урона по '+t['name']+'('+typetotext(t['type'])+')'+str(t['x'])+skilltext+';'+"\n"+str(t['hp'])+'smert:'+str(t['smert'])                
                print(info.lobby.game[creatorid]['resultst1'])
              elif team=='t2mobs':
                info.lobby.game[creatorid]['resultst2']+=info.lobby.game[creatorid][team][mob][number]['name']+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' нанёс '+str(dmg)+' урона по ('+t['name']+typetotext(t['type'])+')'+str(t['x'])+skilltext+';'+"\n"+str(t['hp'])+'smert:'+str(t['smert'])
                print(info.lobby.game[creatorid]['resultst2'])

                    
    elif mob=='electromagnit':
        for number in info.lobby.game[creatorid][team][mob]:
          if info.lobby.game[creatorid][team][mob][number]['target']=='None':
            t=mobdmg(mob, creatorid, team, team2)
            t['underattack']=1
            if t['skill']!='returndmg':
                skilltext=''                
                dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromdeaddmg']
                t['hp']-=dmg
                if team=='t1mobs':
                  info.lobby.game[creatorid]['resultst1']+=mob+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' нанёс '+str(dmg)+' урона по '+t['name']+typetotext(t['type'])+skilltext+';'+"\n"
                elif team=='t2mobs':
                  info.lobby.game[creatorid]['resultst2']+=mob+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' нанёс '+str(dmg)+' урона по '+t['name']+typetotext(t['type'])+skilltext+';'+"\n"

                
    elif mob=='phoenix':
        for number in info.lobby.game[creatorid][team][mob]:
          if info.lobby.game[creatorid][team][mob][number]['target']=='None':
            t=mobdmg(mob, creatorid, team, team2)
            t['underattack']=1
            if t['skill']!='returndmg': 
                skilltext=''                
                dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromdeaddmg']                                                              
                t['hp']-=dmg
                if team=='t1mobs':
                  info.lobby.game[creatorid]['resultst1']+=mob+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' нанёс '+str(dmg)+' урона по '+t['name']+typetotext(t['type'])+skilltext+';'+"\n"
                elif team=='t2mobs':
                  info.lobby.game[creatorid]['resultst2']+=mob+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' нанёс '+str(dmg)+' урона по '+t['name']+typetotext(t['type'])+skilltext+';'+"\n"                                                              
                                                                              

   

                
            
                    
                    
            
    


def endturn(creatorid):
  for id in info.lobby.game[creatorid]['team1']:
    for name in info.lobby.game[creatorid]['players'][id]['allmobs']:
        if name in info.lobby.game[creatorid]['players'][id]['portals']:
          number=0
          while number<info.lobby.game[creatorid]['players'][id]['portals'][name]['count']:   
           if name in info.lobby.game[creatorid]['t1mobs']:
            print('name in t1mobs')
            info.lobby.game[creatorid]['t1mobs']=createmob(nametoclass(name), (len(info.lobby.game[creatorid]['t1mobs'][name])+1), name)
            print('lent1 '+str(len(info.lobby.game[creatorid]['t1mobs'][name])))
            number+=1
           else:
            print('name not in t1')
            info.lobby.game[creatorid]['t1mobs']=createmob(nametoclass(name), 1, name)
            number+=1
            print('lent1 '+str(len(info.lobby.game[creatorid]['t1mobs'][name])))
  for id in info.lobby.game[creatorid]['team2']:
    for name in info.lobby.game[creatorid]['players'][id]['allmobs']:
        if name in info.lobby.game[creatorid]['players'][id]['portals']:
          number=0
          while number<info.lobby.game[creatorid]['players'][id]['portals'][name]['count']:   
              if name in info.lobby.game[creatorid]['t2mobs']:
                print('name in t2mobs')
                info.lobby.game[creatorid]['t2mobs']=createmob(nametoclass(name), (len(info.lobby.game[creatorid]['t2mobs'][name])+1), name)
                number+=1
                print('lent2 '+str(len(info.lobby.game[creatorid]['t2mobs'][name])))
              else:
                print('name not in t2mobs')
                info.lobby.game[creatorid]['t2mobs']=createmob(nametoclass(name), 1, name)
                number+=1
                print('lent2 '+str(len(info.lobby.game[creatorid]['t2mobs'][name])))
            
  for mob in info.lobby.game[creatorid]['t1mobs']:
    mobturn(mob, creatorid, 't1mobs', 't2mobs')
  for mob in info.lobby.game[creatorid]['t2mobs']:
    mobturn(mob, creatorid, 't2mobs', 't1mobs')
    
  for mob in info.lobby.game[creatorid]['t1mobs']:
    for number in info.lobby.game[creatorid]['t1mobs'][mob]:
      if info.lobby.game[creatorid]['t1mobs'][mob][number]['hp']<1:
        info.lobby.game[creatorid]['t1mobs'][mob][number]['smert']=1
        
  for mob in info.lobby.game[creatorid]['t2mobs']:
    for number in info.lobby.game[creatorid]['t2mobs'][mob]:
      if info.lobby.game[creatorid]['t2mobs'][mob][number]['hp']<1:
        info.lobby.game[creatorid]['t2mobs'][mob][number]['smert']=1
        
  bot.send_message(info.lobby.game[creatorid]['chatid'],info.lobby.game[creatorid]['resultst1']+"\n"+info.lobby.game[creatorid]['resultst2']) 
  battle(info.lobby.game[creatorid]['creatorid']['selfid'])
                                                                              
                                                                              
    
    
    
            
            
            
            


def nametoclass(name):  #делает перевод названия сущ-ва в ссылку на класс
    if name=='s_me4nik':
        x=info.s_me4nik
    elif name=='phoenix':
        x=info.phoenix
    elif name=='electromagnit':
        x=info.electromagnit
         
    return x



def mobs(callid):    #выбирает 3х рандомных мобов для возможности спавна
    for id in info.lobby.game:
      if callid in info.lobby.game[id]['players']:
            while len(info.lobby.game[id]['players'][callid]['mobsinturn'])<3:
              x=random.randint(1,len(info.lobby.game[id]['players'][callid]['allmobs']))
              if info.lobby.game[id]['players'][callid]['allmobs'][x-1] not in info.lobby.game[id]['players'][callid]['mobsinturn']:
                info.lobby.game[id]['players'][callid]['mobsinturn'].append(info.lobby.game[id]['players'][callid]['allmobs'][x-1])
                if len(info.lobby.game[id]['players'][callid]['mobsinturn'])==1:
                  y=nametoclass(info.lobby.game[id]['players'][callid]['allmobs'][x-1])
                  info.lobby.game[id]['players'][callid]['name1mob']=y.name
                elif len(info.lobby.game[id]['players'][callid]['mobsinturn'])==2:
                  y=nametoclass(info.lobby.game[id]['players'][callid]['allmobs'][x-1])
                  info.lobby.game[id]['players'][callid]['name2mob']=y.name
                elif len(info.lobby.game[id]['players'][callid]['mobsinturn'])==3:
                  y=nametoclass(info.lobby.game[id]['players'][callid]['allmobs'][x-1])
                  info.lobby.game[id]['players'][callid]['name3mob']=y.name
                        



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
            
  elif call.data=='end':
    for id in info.lobby.game:
        if call.from_user.id in info.lobby.game[id]['players']:
          endturn(info.lobby.game[id]['creatorid']['selfid'])
           
          
          
  elif call.data=='altar':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:          
            Keyboard=types.InlineKeyboardMarkup()
            Keyboard.add(types.InlineKeyboardButton(text=info.lobby.game[id]['players'][call.from_user.id]['name1mob'], callback_data=info.lobby.game[id]['players'][call.from_user.id]['mobsinturn'][0]))
            Keyboard.add(types.InlineKeyboardButton(text=info.lobby.game[id]['players'][call.from_user.id]['name2mob'], callback_data=info.lobby.game[id]['players'][call.from_user.id]['mobsinturn'][1]))
            Keyboard.add(types.InlineKeyboardButton(text=info.lobby.game[id]['players'][call.from_user.id]['name3mob'], callback_data=info.lobby.game[id]['players'][call.from_user.id]['mobsinturn'][2]))
            Keyboard.add(types.InlineKeyboardButton(text="Главное меню", callback_data='menu'))
            msg=medit('В этом ходу вам доступны:', call.from_user.id, info.lobby.game[id]['players'][call.from_user.id]['lastmessage'], reply_markup=Keyboard)
            info.lobby.game[id]['players'][call.from_user.id]['lastmessage']=msg.message_id 
         
     
  elif call.data=='s_me4nik':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
          if info.lobby.game[id]['players'][call.from_user.id]['mana']>=info.s_me4nik.cost:
            info.lobby.game[id]['players'][call.from_user.id]['mana']-=info.s_me4nik.cost
            if 's_me4nik' not in info.lobby.game[id]['players'][call.from_user.id]['portals']:
              info.lobby.game[id]['players'][call.from_user.id]['portals']=createportal('s_me4nik', 1)  
            else:
              info.lobby.game[id]['players'][call.from_user.id]['portals']=createportal('s_me4nik', info.lobby.game[id]['players'][call.from_user.id]['portals']['s_me4nik']['count']+1)  
            bot.send_message(call.from_user.id, 'Вы успешно призвали портал (Скелет-мечник)!'+"\n"+'Теперь у вас '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['s_me4nik']['count'])+' таких порталов!')
          else:
            bot.send_message(call.from_user.id, 'Недостаточно маны!')
            
            
  elif call.data=='phoenix':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
          if info.lobby.game[id]['players'][call.from_user.id]['mana']>=info.phoenix.cost:
            info.lobby.game[id]['players'][call.from_user.id]['mana']-=info.phoenix.cost
            info.lobby.game[id]['players'][call.from_user.id]['portals']['phoenix']=createportal()    
            bot.send_message(call.from_user.id, 'Вы успешно призвали портал (Феникадзе)!')
          else:
            bot.send_message(call.from_user.id, 'Недостаточно маны!')
            
  elif call.data=='electromagnit':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
          if info.lobby.game[id]['players'][call.from_user.id]['mana']>=info.electromagnit.cost:
            info.lobby.game[id]['players'][call.from_user.id]['mana']-=info.electromagnit.cost
            info.lobby.game[id]['players'][call.from_user.id]['portals']['electromagnit']=createportal()              
            bot.send_message(call.from_user.id, 'Вы успешно призвали портал (Электромагнитень)!')
          else:
            bot.send_message(call.from_user.id, 'Недостаточно маны!')
       
                 
            
    
  
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
    if info.lobby.game[message.from_user.id]['creatorid']['selfid']==message.from_user.id:
      if info.lobby.game[message.from_user.id]['naming']==1:
        if len(message.text)<31:
         if message.text!='None':
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
    't1mobs':{},
    't2mobs':{},
    'resultst1':'Результаты монстров из команды 1:'+"\n",
    'resultst2':'Результаты монстров из команды 2:'+"\n"
      

  }
  
  
  
def createuser(id, x):
  
  return{'selfid':id,
         'lastmessage':0,
         'tvari':{'s_me4nik':{},
                  'phoenix':{},
                  'electromagnit':{}
         },
         'portals':{},
         'mana':0,
         'mobnumber':0,
         'manamax':100,
         'inlobby':x,
         'cash':'',
         'allmobs':['s_me4nik', 'electromagnit', 'phoenix'],
         'mobsinturn':[],
         'name1mob':'',
         'name2mob':'',
         'name3mob':''
            }  
  
def createportal(name, x):  
    return {name:{'name':name,
          'count':x
           }}

    
def createmob(nameclass, x, namemob):
      return{namemob:{x:{'hp':nameclass.hp,
        'name':nameclass.name,
        'mana':nameclass.mana,
        'damage':nameclass.damage,
        'cost':nameclass.cost,
        'type':nameclass.type,
        'fromelectrodmg':nameclass.fromelectrodmg,
        'frombiodmg':nameclass.frombiodmg,          
        'fromghostdmg':nameclass.fromghostdmg,
        'fromdeaddmg':nameclass.fromdeaddmg,
        'fromfiredmg':nameclass.fromfiredmg,     
        'x':x,
        'target':None,
        'koef':0,
        'maxkoef':0,
        'underattack':0,
        'skill':nameclass.skill,
        'smert':0
                
        }
       }
    }
       
    
    
    
def battle(creatorid):
    for key in info.lobby.game[creatorid]['players']:
      mobs(key)
      info.lobby.game[creatorid]['players'][key]['mana']=info.lobby.game[creatorid]['players'][key]['manamax']      
      mana=emojize(':droplet:', use_aliases=True)
      Keyboard=types.InlineKeyboardMarkup()
      Keyboard.add(types.InlineKeyboardButton(text="Действия", callback_data='do'))
      Keyboard.add(types.InlineKeyboardButton(text="Окончить ход", callback_data='end'))
      Keyboard.add(types.InlineKeyboardButton(text="Инфо обо мне", callback_data='info'))      
      msg=bot.send_message(key, 'Главное меню:'+"\n"+mana+'Мана: '+str(info.lobby.game[creatorid]['players'][key]['mana'])+'/'+str(info.lobby.game[creatorid]['players'][key]['manamax']),reply_markup=Keyboard)
      info.lobby.game[creatorid]['players'][key]['lastmessage']=msg.message_id
       


if __name__ == '__main__':
  bot.polling(none_stop=True)



