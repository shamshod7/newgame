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

def classtoemoji(classs):
    if classs=='dead':
        emoj=emojize(':skull:', use_aliases=True)
    elif classs=='electro':
        emoj=emojize(':zap:', use_aliases=True)
    elif classs=='bio':
        emoj=emojize(':evergreen_tree:', use_aliases=True)
    elif classs=='ghost':
        emoj=emojize(':ghost:', use_aliases=True)
    elif classs=='fire':
        emoj=emojize(':fire:', use_aliases=True)
    return emoj



def mobdmg(mob, creatorid, team, team2, number):
    t=None
    for mob2 in info.lobby.game[creatorid][team2]:
              for number2 in info.lobby.game[creatorid][team2][mob2]:
                if info.lobby.game[creatorid][team2][mob2][number2]['smert']!=1:
                 if info.lobby.game[creatorid][team2][mob2][number2]['hp']>0:
                  if info.lobby.game[creatorid][team][mob][number]['type']=='dead':
                    info.lobby.game[creatorid][team][mob][number]['koef']=info.lobby.game[creatorid][team2][mob2][number2]['fromdeaddmg']
                  elif info.lobby.game[creatorid][team][mob][number]['type']=='bio':
                    info.lobby.game[creatorid][team][mob][number]['koef']=info.lobby.game[creatorid][team2][mob2][number2]['frombiodmg']
                  elif info.lobby.game[creatorid][team][mob][number]['type']=='electro':
                    info.lobby.game[creatorid][team][mob][number]['koef']=info.lobby.game[creatorid][team2][mob2][number2]['fromelectrodmg']
                  elif info.lobby.game[creatorid][team][mob][number]['type']=='ghost':
                    info.lobby.game[creatorid][team][mob][number]['koef']=info.lobby.game[creatorid][team2][mob2][number2]['fromghostdmg']
                  elif info.lobby.game[creatorid][team][mob][number]['type']=='fire':
                    info.lobby.game[creatorid][team][mob][number]['koef']=info.lobby.game[creatorid][team2][mob2][number2]['fromfiredmg']
                  if info.lobby.game[creatorid][team][mob][number]['koef']>info.lobby.game[creatorid][team][mob][number]['maxkoef']:
                        info.lobby.game[creatorid][team][mob][number]['maxkoef']=info.lobby.game[creatorid][team][mob][number]['koef']
                        info.lobby.game[creatorid][team][mob][number]['target']=info.lobby.game[creatorid][team2][mob2][number2]
                        t=info.lobby.game[creatorid][team2][mob2][number2]
    if t==None:
        t='None'
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
        for number in info.lobby.game[creatorid][team][mob]:
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
              t=mobdmg(mob, creatorid, team, team2, number)
              if t!='None':
                z=random.randint(1,100)
                if z<=15:
                  t['fromdeaddmg']+=0.6
                  skilltext=', применив скилл "Проклятье мертвецов"'
                else:
                  skilltext=''
                dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromdeaddmg']
                t['hp']-=dmg
                if team=='t1mobs':
                 if t['hp']<1:
                  info.lobby.game[creatorid]['resultst1']+=info.lobby.game[creatorid][team][mob][number]['name']+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' нанёс '+str(dmg)+' урона по '+t['name']+'('+typetotext(t['type'])+')'+skilltext+'; Враг погибает!'+"\n"  
                 else:
                  info.lobby.game[creatorid]['resultst1']+=info.lobby.game[creatorid][team][mob][number]['name']+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' нанёс '+str(dmg)+' урона по '+t['name']+'('+typetotext(t['type'])+')'+skilltext+'; '+'У него остается '+str(t['hp'])+' хп!'+"\n"
                elif team=='t2mobs':
                 if t['hp']<1:
                  info.lobby.game[creatorid]['resultst2']+=info.lobby.game[creatorid][team][mob][number]['name']+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' нанёс '+str(dmg)+' урона по ('+t['name']+typetotext(t['type'])+')'+skilltext+'; Враг погибает!'+"\n"
                 else:
                  info.lobby.game[creatorid]['resultst2']+=info.lobby.game[creatorid][team][mob][number]['name']+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' нанёс '+str(dmg)+' урона по ('+t['name']+typetotext(t['type'])+')'+skilltext+'; '+'У него остается '+str(t['hp'])+' хп!'+"\n"

                    
    elif mob=='electromagnit':
        for number in info.lobby.game[creatorid][team][mob]:
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
              t=mobdmg(mob, creatorid, team, team2, number)
              if t!='None':
                z=random.randint(1,100)
                if z<=40:
                  if t['mana']>0:
                    h=100
                    t['mana']-=h
                    a=0-t['mana']
                    if a>0:
                        t['mana']+=a
                        h-=a    
                    info.lobby.game[creatorid][team][mob][number]['hp']+=h
                    skilltext=', и применил скилл "Проникновение", восстановив '+str(h)+' хп'
                else:
                  skilltext=''
                dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromelectrodmg']
                t['hp']-=dmg
                if team=='t1mobs':
                 if t['hp']<1:
                  info.lobby.game[creatorid]['resultst1']+=info.lobby.game[creatorid][team][mob][number]['name']+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' нанёс '+str(dmg)+' урона по '+t['name']+'('+typetotext(t['type'])+')'+skilltext+'; враг погибает!'+"\n"  
                 else:
                  info.lobby.game[creatorid]['resultst1']+=info.lobby.game[creatorid][team][mob][number]['name']+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' нанёс '+str(dmg)+' урона по '+t['name']+'('+typetotext(t['type'])+')'+skilltext+'; '+'у врага остается '+str(t['hp'])+' хп!'+"\n"
                elif team=='t2mobs':
                 if t['hp']<1:
                  info.lobby.game[creatorid]['resultst2']+=info.lobby.game[creatorid][team][mob][number]['name']+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' нанёс '+str(dmg)+' урона по ('+t['name']+typetotext(t['type'])+')'+skilltext+'; враг погибает!'+"\n"
                 else:
                  info.lobby.game[creatorid]['resultst2']+=info.lobby.game[creatorid][team][mob][number]['name']+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' нанёс '+str(dmg)+' урона по ('+t['name']+typetotext(t['type'])+')'+skilltext+'; '+'у врага остается '+str(t['hp'])+' хп!'+"\n"


                
    elif mob=='phoenix':
        for number in info.lobby.game[creatorid][team][mob]:
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
              t=mobdmg(mob, creatorid, team, team2, number)
              if t!='None':
                skilltext=''
                dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromfiredmg']
                t['hp']-=dmg
                info.lobby.game[creatorid][team][mob][number]['smert']=1
                if team=='t1mobs':
                 if t['hp']<1:
                  info.lobby.game[creatorid]['resultst1']+=info.lobby.game[creatorid][team][mob][number]['name']+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' самоубился об врага '+t['name']+'('+typetotext(t['type'])+')'+', нанеся '+str(dmg)+' урона ; враг погибает!'+"\n"  
                 else:
                  info.lobby.game[creatorid]['resultst1']+=info.lobby.game[creatorid][team][mob][number]['name']+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' самоубился об врага '+t['name']+'('+typetotext(t['type'])+')'+', нанеся '+str(dmg)+' урона ;'+'у него остается '+str(t['hp'])+' хп!'+"\n"
                elif team=='t2mobs':
                 if t['hp']<1:
                  info.lobby.game[creatorid]['resultst2']+=info.lobby.game[creatorid][team][mob][number]['name']+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' самоубился об врага '+t['name']+'('+typetotext(t['type'])+')'+', нанеся '+str(dmg)+' урона ; враг погибает!'+"\n" 
                 else:
                  info.lobby.game[creatorid]['resultst2']+=info.lobby.game[creatorid][team][mob][number]['name']+'('+typetotext(info.lobby.game[creatorid][team][mob][number]['type'])+')'+' самоубился об врага '+t['name']+'('+typetotext(t['type'])+')'+', нанеся '+str(dmg)+' урона ;'+'у него остается '+str(t['hp'])+' хп!'+"\n"                                                           
                                                                              

   

                
            
                    
def testturn(creatorid, id):
  info.lobby.game[creatorid]['readys']+=1
  info.lobby.game[creatorid]['players'][id]['ready']=1
  if info.lobby.game[creatorid]['readys']!=len(info.lobby.game[creatorid]['players']):
    msg=medit('Ожидание других игроков...', id, info.lobby.game[creatorid]['players'][id]['lastmessage'])
    info.lobby.game[creatorid]['players'][id]['currentmessage']=msg.message_id
  else:
    msg=medit('Ожидание других игроков...', id, info.lobby.game[creatorid]['players'][id]['lastmessage'])
    info.lobby.game[creatorid]['players'][id]['currentmessage']=msg.message_id
    
    endturn(creatorid)
    
              
    
 
            
    


def endturn(creatorid):
 for ids in info.lobby.game[creatorid]['players']:
  if info.lobby.game[creatorid]['players'][ids]['ready']!=1:
    msg=medit('Время вышло!', ids, info.lobby.game[creatorid]['players'][ids]['lastmessage'])
 for id in info.lobby.game[creatorid]['team1']:
     for name in info.lobby.game[creatorid]['players'][id]['allmobs']:
        if name in info.lobby.game[creatorid]['players'][id]['portals']:
          number=0
          while number<info.lobby.game[creatorid]['players'][id]['portals'][name]['count']:   
           if name in info.lobby.game[creatorid]['t1mobs']:
              s4islo=0
              for count in info.lobby.game[creatorid]['t1mobs'][name]:
                s4islo+=1
              print('name in t1mobs')
              info.lobby.game[creatorid]['t1mobs'][name][s4islo+1]=createmob(nametoclass(name), (s4islo+1), name)
              print(str(len(info.lobby.game[creatorid]['t1mobs'][name])))
              number+=1
           else:
            print('name not in t1')
            info.lobby.game[creatorid]['t1mobs']=createmob1(nametoclass(name), 1, name)
            number+=1
 for id in info.lobby.game[creatorid]['team2']:
    for name in info.lobby.game[creatorid]['players'][id]['allmobs']:
        if name in info.lobby.game[creatorid]['players'][id]['portals']:
          number=0
          while number<info.lobby.game[creatorid]['players'][id]['portals'][name]['count']:   
              if name in info.lobby.game[creatorid]['t2mobs']:               
                s4islo=0
                for count in info.lobby.game[creatorid]['t2mobs'][name]:
                  s4islo+=1
                print('name in t2mobs')
                info.lobby.game[creatorid]['t2mobs'][name][s4islo+1]=createmob(nametoclass(name), (s4islo+1), name)
                number+=1
              else:
                print('name not in t2mobs')
                info.lobby.game[creatorid]['t2mobs']=createmob1(nametoclass(name), 1, name)
                number+=1
            
 for mob in info.lobby.game[creatorid]['t1mobs']:
    mobturn(mob, creatorid, 't1mobs', 't2mobs')
 for mob in info.lobby.game[creatorid]['t2mobs']:
    mobturn(mob, creatorid, 't2mobs', 't1mobs')
    
 for mobs2 in info.lobby.game[creatorid]['t1mobs']:
    for xyz in info.lobby.game[creatorid]['t1mobs'][mob]:
      if info.lobby.game[creatorid]['t1mobs'][mobs2][xyz]['hp']<1:
        info.lobby.game[creatorid]['t1mobs'][mobs2][xyz]['smert']=1
        
 for mobs3 in info.lobby.game[creatorid]['t2mobs']:
    for xyz3 in info.lobby.game[creatorid]['t2mobs'][mobs3]:
      if info.lobby.game[creatorid]['t2mobs'][mobs3][xyz3]['hp']<1:
        info.lobby.game[creatorid]['t2mobs'][mobs3][xyz3]['smert']=1
 livemobs1=0
 livemobs2=0
 for mobs4 in info.lobby.game[creatorid]['t1mobs']:
    for number4 in info.lobby.game[creatorid]['t1mobs'][mobs4]:
        if info.lobby.game[creatorid]['t1mobs'][mobs4][number4]['hp']>0:
          livemobs1+=1
 for mobs5 in info.lobby.game[creatorid]['t2mobs']:
      for number5 in info.lobby.game[creatorid]['t2mobs'][mobs5]:
        if info.lobby.game[creatorid]['t2mobs'][mobs5][number5]['hp']>0:
          livemobs2+=1
 bot.send_message(info.lobby.game[creatorid]['chatid'],'Ход '+str(info.lobby.game[creatorid]['hod'])+':'+"\n"+'Команда 1: '+info.lobby.game[creatorid]['teammates1']+"\n"+'Команда 2: '+info.lobby.game[creatorid]['teammates2']+"\n"+info.lobby.game[creatorid]['resultst1']+"\n"+'Кол-во выживших существ команды 1: '+str(livemobs1)+"\n"+"\n"+info.lobby.game[creatorid]['resultst2']+"\n"+'Кол-во выживших существ команды 2: '+str(livemobs2)+"\n"+"\n") 
 info.lobby.game[creatorid]['resultst1']='Результаты монстров из команды 1:'+"\n"
 info.lobby.game[creatorid]['resultst2']='Результаты монстров из команды 2:'+"\n"
 for endid in info.lobby.game[creatorid]['players']:
    info.lobby.game[creatorid]['players'][endid]['ready']=0
    info.lobby.game[creatorid]['readys']=0
 for mob10 in info.lobby.game[creatorid]['t1mobs']:
    for number10 in info.lobby.game[creatorid]['t1mobs'][mob10]:
      info.lobby.game[creatorid]['t1mobs'][mob10][number10]['target']=None
      info.lobby.game[creatorid]['t1mobs'][mob10][number10]['maxkoef']=0
 for mob11 in info.lobby.game[creatorid]['t2mobs']:
    for number11 in info.lobby.game[creatorid]['t2mobs'][mob11]:
      info.lobby.game[creatorid]['t2mobs'][mob11][number11]['target']=None
      info.lobby.game[creatorid]['t2mobs'][mob11][number11]['maxkoef']=0
 info.lobby.game[creatorid]['hod']+=1
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
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
         if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
          portal=emojize(':crystal_ball:', use_aliases=True)
          back=emojize(':back:', use_aliases=True) 
          Keyboard=types.InlineKeyboardMarkup()
          Keyboard.add(types.InlineKeyboardButton(text=portal+"Открыть портал", callback_data='altar'))
          Keyboard.add(types.InlineKeyboardButton(text=back+"Главное меню", callback_data='menu'))
          msg=medit('Выберите действие', call.from_user.id, info.lobby.game[id]['players'][call.from_user.id]['lastmessage'], reply_markup=Keyboard)
          info.lobby.game[id]['players'][call.from_user.id]['currentmessage']=msg.message_id
          info.lobby.game[id]['players'][call.from_user.id]['lastmessage']=msg.message_id

          
          
          
  elif call.data=='menu':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
          if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
            mana=emojize(':droplet:', use_aliases=True)
            go=emojize(':video_game:', use_aliases=True)
            end=emojize(':white_check_mark:', use_aliases=True)
            infos=emojize(':question:', use_aliases=True)
            Keyboard=types.InlineKeyboardMarkup()
            Keyboard.add(types.InlineKeyboardButton(text=go+"Действия", callback_data='do'))
            Keyboard.add(types.InlineKeyboardButton(text=infos+"Инфо обо мне", callback_data='info'))  
            Keyboard.add(types.InlineKeyboardButton(text=end+"Окончить ход", callback_data='end'))
            msg=medit('Главное меню:'+"\n"+mana+'Мана: '+str(info.lobby.game[id]['players'][call.from_user.id]['mana'])+'/'+str(info.lobby.game[id]['players'][call.from_user.id]['manamax']), call.from_user.id, info.lobby.game[id]['players'][call.from_user.id]['lastmessage'], reply_markup=Keyboard)
            info.lobby.game[id]['players'][call.from_user.id]['lastmessage']=msg.message_id 
            info.lobby.game[id]['players'][call.from_user.id]['currentmessage']=msg.message_id
            
  elif call.data=='end':
   for id in info.lobby.game:
    if call.from_user.id in info.lobby.game[id]['players']:
     if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
      if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
       for creatorid in info.lobby.game:
        if call.from_user.id in info.lobby.game[creatorid]['players']:  
          testturn(info.lobby.game[creatorid]['creatorid']['selfid'], call.from_user.id)


           
          
          
  elif call.data=='altar':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']: 
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
          if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
            nc0=nametoclass(info.lobby.game[id]['players'][call.from_user.id]['mobsinturn'][0])
            nc1=nametoclass(info.lobby.game[id]['players'][call.from_user.id]['mobsinturn'][1])
            nc2=nametoclass(info.lobby.game[id]['players'][call.from_user.id]['mobsinturn'][2])
            manacost=emojize(':droplet:', use_aliases=True)
            emoj0=classtoemoji(nc0.type)
            emoj1=classtoemoji(nc1.type)
            emoj2=classtoemoji(nc2.type)
            back=emojize(':back:', use_aliases=True) 
            Keyboard=types.InlineKeyboardMarkup()
            Keyboard.add(types.InlineKeyboardButton(text=emoj0+info.lobby.game[id]['players'][call.from_user.id]['name1mob']+"\n"+manacost+str(nc0.cost), callback_data=info.lobby.game[id]['players'][call.from_user.id]['mobsinturn'][0]))
            Keyboard.add(types.InlineKeyboardButton(text=emoj1+info.lobby.game[id]['players'][call.from_user.id]['name2mob']+"\n"+manacost+str(nc1.cost), callback_data=info.lobby.game[id]['players'][call.from_user.id]['mobsinturn'][1]))
            Keyboard.add(types.InlineKeyboardButton(text=emoj2+info.lobby.game[id]['players'][call.from_user.id]['name3mob']+"\n"+manacost+str(nc2.cost), callback_data=info.lobby.game[id]['players'][call.from_user.id]['mobsinturn'][2]))
            Keyboard.add(types.InlineKeyboardButton(text=back+"Главное меню", callback_data='menu'))
            msg=medit('В этом ходу вам доступны:', call.from_user.id, info.lobby.game[id]['players'][call.from_user.id]['lastmessage'], reply_markup=Keyboard)
            info.lobby.game[id]['players'][call.from_user.id]['lastmessage']=msg.message_id 
            info.lobby.game[id]['players'][call.from_user.id]['currentmessage']=msg.message_id
         
     
  elif call.data=='s_me4nik':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
         if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
          if 's_me4nik' in info.lobby.game[id]['players'][call.from_user.id]['mobsinturn']:
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
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
         if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
          if 'phoenix' in info.lobby.game[id]['players'][call.from_user.id]['mobsinturn']:
           if info.lobby.game[id]['players'][call.from_user.id]['mana']>=info.phoenix.cost:
            info.lobby.game[id]['players'][call.from_user.id]['mana']-=info.phoenix.cost
            if 'phoenix' not in info.lobby.game[id]['players'][call.from_user.id]['portals']:
              info.lobby.game[id]['players'][call.from_user.id]['portals']=createportal('phoenix', 1)  
            else:
              info.lobby.game[id]['players'][call.from_user.id]['portals']=createportal('phoenix', info.lobby.game[id]['players'][call.from_user.id]['portals']['phoenix']['count']+1)  
            bot.send_message(call.from_user.id, 'Вы успешно призвали портал (Феникадзе)!'+"\n"+'Теперь у вас '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['phoenix']['count'])+' таких порталов!')
           else:
            bot.send_message(call.from_user.id, 'Недостаточно маны!')
            
  elif call.data=='electromagnit':
     for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
         if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
          if 'electromagnit' in info.lobby.game[id]['players'][call.from_user.id]['mobsinturn']:
           if info.lobby.game[id]['players'][call.from_user.id]['mana']>=info.electromagnit.cost:
            info.lobby.game[id]['players'][call.from_user.id]['mana']-=info.electromagnit.cost
            if 'electromagnit' not in info.lobby.game[id]['players'][call.from_user.id]['portals']:
              info.lobby.game[id]['players'][call.from_user.id]['portals']=createportal('electromagnit', 1)  
            else:
              info.lobby.game[id]['players'][call.from_user.id]['portals']=createportal('electromagnit', info.lobby.game[id]['players'][call.from_user.id]['portals']['electromagnit']['count']+1)  
            bot.send_message(call.from_user.id, 'Вы успешно призвали портал (Электромагнитень)!'+"\n"+'Теперь у вас '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['electromagnit']['count'])+' таких порталов!')
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
                  info.lobby.game[message.from_user.id]['team1'][id]=createuser(id, 1, info.lobby.game[message.from_user.id]['players'][id]['fname'])
                else:
                  info.lobby.game[message.from_user.id]['team2'][id]=createuser(id, 1, info.lobby.game[message.from_user.id]['players'][id]['fname'])
              elif len(info.lobby.game[message.from_user.id]['team1'])>len(info.lobby.game[message.from_user.id]['team2']):
                info.lobby.game[message.from_user.id]['team2'][id]=createuser(id, 1, info.lobby.game[message.from_user.id]['players'][id]['fname'])
              else:
                info.lobby.game[message.from_user.id]['team1'][id]=createuser(id, 1, info.lobby.game[message.from_user.id]['players'][id]['fname'])
            info.lobby.game[message.from_user.id]['battle']=1
            for id1 in info.lobby.game[message.from_user.id]['players']:
                if info.lobby.game[message.from_user.id]['players'][id1]['selfid'] in info.lobby.game[message.from_user.id]['team1']:
                    info.lobby.game[message.from_user.id]['teammates1']+=info.lobby.game[message.from_user.id]['players'][id1]['fname']+', '
                elif info.lobby.game[message.from_user.id]['players'][id1]['selfid'] in info.lobby.game[message.from_user.id]['team2']:
                    info.lobby.game[message.from_user.id]['teammates2']+=info.lobby.game[message.from_user.id]['players'][id1]['fname']+', '
            lenofteam1=len(info.lobby.game[message.from_user.id]['teammates1'])
            info.lobby.game[message.from_user.id]['teammates1']=info.lobby.game[message.from_user.id]['teammates1'][:(lenofteam1-2)]
            lenofteam2=len(info.lobby.game[message.from_user.id]['teammates2'])
            info.lobby.game[message.from_user.id]['teammates2']=info.lobby.game[message.from_user.id]['teammates2'][:(lenofteam2-2)]
            btl=threading.Thread(target=battle, args=[message.from_user.id])
            btl.start()
            print(info.lobby.game)
            info.lobby.game[message.from_user.id]['playing']=1
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
          if info.lobby.game[key]['playing']==0:
           already=0
           for id in info.lobby.game:                    
             if message.from_user.id in info.lobby.game[id]['players']:
               already=1
               info.lobby.game[id]['players'][message.from_user.id]['cash']=info.lobby.game[id]['name']
           if already==0:
             info.lobby.game[key]['players'][message.from_user.id]=createuser(message.from_user.id, 1, message.from_user.first_name)
             info.lobby.game[key]['len']+=1
             bot.send_message(message.chat.id, 'Вы успешно присоединились в игру ('+str(info.lobby.game[id]['players'][message.from_user.id]['cash'])+')! Для начала игры её создатель должен нажать /fight')
           else:
             bot.send_message(message.chat.id, 'Вы уже в другом лобби!')

           

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
    info.lobby.game[message.from_user.id]=createlobby(message.chat.id, message.from_user.id, message.from_user.first_name)
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
  
  

  
  
  
def createlobby(chatid, creatorid, fname):
  return {
    'name':'None',
    'chatid':chatid,
    'creatorid':createuser(creatorid, 1, fname),
    'naming':0,
    'playing':0,
    'players':{creatorid:createuser(creatorid, 1, fname)},
    'battle':0,
    'len':1,
    'team1':{},
    'team2':{},
    't1mobs':{},
    't2mobs':{},
    'resultst1':'Результаты монстров из команды 1'+"\n",
    'resultst2':'Результаты монстров из команды 2'+"\n",
    'readys':0,
    'launchtimer':0,
    'timer':None,
    'hod':1,
    'teammates1':'',
    'teammates2':''
      

  }
  
  
  
def createuser(id, x, fname):
  
  return{'selfid':id,
         'lastmessage':0,
         'tvari':{'s_me4nik':{},
                  'phoenix':{},
                  'electromagnit':{}
         },
         'portals':{},
         'mana':0,
         'mobnumber':0,
         'manamax':250,
         'inlobby':x,
         'cash':'',
         'allmobs':['s_me4nik', 'electromagnit', 'phoenix'],
         'mobsinturn':[],
         'name1mob':'',
         'name2mob':'',
         'name3mob':'',
         'ready':0,
         'fname':fname,
         'currentmessage':''
            }  
  
def createportal(name, x):  
    return {name:{'name':name,
          'count':x
           }}

    
def createmob(nameclass, x, namemob):
      return{
        'hp':nameclass.hp,
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
    
def createmob1(nameclass, x, namemob):
      return{namemob:{x:{
        'hp':nameclass.hp,
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
    if info.lobby.game[creatorid]['launchtimer']==0:
      t=threading.Timer(120.0, endturn, args=[creatorid])
      t.start()
      info.lobby.game[creatorid]['launchtimer']=1
      info.lobby.game[creatorid]['timer']=t
    else:
      info.lobby.game[creatorid]['timer'].cancel()
      t=threading.Timer(120.0, endturn, args=[creatorid])
      t.start()
      info.lobby.game[creatorid]['launchtimer']=1
      info.lobby.game[creatorid]['timer']=t
    for key in info.lobby.game[creatorid]['players']:
      mobs(key)
      info.lobby.game[creatorid]['players'][key]['mana']=info.lobby.game[creatorid]['players'][key]['manamax']      
      mana=emojize(':droplet:', use_aliases=True)
      go=emojize(':video_game:', use_aliases=True)
      end=emojize(':white_check_mark:', use_aliases=True)
      infos=emojize(':question:', use_aliases=True)
      Keyboard=types.InlineKeyboardMarkup()       
      Keyboard.add(types.InlineKeyboardButton(text=go+"Действия", callback_data='do'))
      Keyboard.add(types.InlineKeyboardButton(text=infos+"Инфо обо мне", callback_data='info'))
      Keyboard.add(types.InlineKeyboardButton(text=end+"Окончить ход", callback_data='end'))     
      msg=bot.send_message(key, 'Главное меню:'+"\n"+mana+'Мана: '+str(info.lobby.game[creatorid]['players'][key]['mana'])+'/'+str(info.lobby.game[creatorid]['players'][key]['manamax']),reply_markup=Keyboard)
      info.lobby.game[creatorid]['players'][key]['lastmessage']=msg.message_id
      info.lobby.game[creatorid]['players'][key]['currentmessage']=msg.message_id
       


if __name__ == '__main__':
  bot.polling(none_stop=True)



