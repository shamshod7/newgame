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

ban=['pyos']


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


def end(creatorid, team, mob, number, t, dmg):
              typemob1=classtoemoji(info.lobby.game[creatorid][team][mob][number]['type'])
              typemob2=classtoemoji(t['type'])
              emoj1= emojize(typemob1, use_aliases=True)
              emoj2= emojize(typemob2, use_aliases=True)
              emojattack=emojize(':arrow_right:', use_aliases=True)
              emojdie=emojize(':x:', use_aliases=True)
              emojdmg=emojize(':broken_heart:', use_aliases=True)
              emojhp=emojize(':green_heart:', use_aliases=True)
              emojstun=emojize(':cyclone:', use_aliases=True)
              if team=='t1mobs':
                if info.lobby.game[creatorid][team][mob][number]['stun']<1:
                 if t['hp']<1:
                  for id in info.lobby.game[creatorid]['team2']:
                    info.lobby.game[creatorid]['players'][id]['mana']+=3
                    info.lobby.game[creatorid]['manaplust1']+=3
                  if info.lobby.game[creatorid][team][mob][number]['skilltext']!='None':
                    skillt=info.lobby.game[creatorid][team][mob][number]['skilltext']
                    info.lobby.game[creatorid]['resultst1']+=skillt
                  else:
                    info.lobby.game[creatorid]['resultst1']+=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+emojattack+emoj2+t['name']+emojdie+"\n"  
                 else:
                   if info.lobby.game[creatorid][team][mob][number]['skilltext']!='None':
                     skillt=info.lobby.game[creatorid][team][mob][number]['skilltext']
                     info.lobby.game[creatorid]['resultst1']+=skillt
                   else:  
                    info.lobby.game[creatorid]['resultst1']+=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+emojattack+emoj2+t['name']+emojdmg+str(dmg)+emojhp+str(t['hp'])+"\n"
                else:
                    info.lobby.game[creatorid]['resultst1']+=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+emojstun+"\n"
              elif team=='t2mobs':
               if info.lobby.game[creatorid][team][mob][number]['stun']<1:
                 if t['hp']<1:
                   for id in info.lobby.game[creatorid]['team1']:
                    info.lobby.game[creatorid]['players'][id]['mana']+=3
                    info.lobby.game[creatorid]['manaplust2']+=3
                   if info.lobby.game[creatorid][team][mob][number]['skilltext']!='None':
                     skillt=info.lobby.game[creatorid][team][mob][number]['skilltext']
                   else:
                     info.lobby.game[creatorid]['resultst2']+=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+emojattack+emoj2+t['name']+emojdie+"\n" 
                        
                 else:
                  if info.lobby.game[creatorid][team][mob][number]['skilltext']!='None':
                     skillt=info.lobby.game[creatorid][team][mob][number]['skilltext']
                  else:
                    info.lobby.game[creatorid]['resultst2']+=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+emojattack+emoj2+t['name']+emojdmg+str(dmg)+emojhp+str(t['hp'])+"\n"
               else:
                  info.lobby.game[creatorid]['resultst2']+=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+emojstun+"\n"
                



def mobdmg(mob, creatorid, team, team2, number):
    t=None
    for mob2 in info.lobby.game[creatorid][team2]:
            for number2 in info.lobby.game[creatorid][team2][mob2]:
              if info.lobby.game[creatorid][team2][mob2][number2]['smert']!=1:
                if info.lobby.game[creatorid][team2][mob2][number2]['stun']<1:
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
                    if info.lobby.game[creatorid][team2][mob2][number2]['hp']>0:
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
        

def mobturn(creatorid, team, mob, number, t):
   if mob=='s_me4nik':
     dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromdeaddmg']
     dmg=round(dmg, 2)
     t['hp']-=dmg    
     end(creatorid, team, mob, number, t, dmg)
        
   elif mob=='phoenix':
     dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromfiredmg']
     dmg=round(dmg, 2)
     t['hp']-=dmg
     end(creatorid, team, mob, number, t, dmg)
   
   elif mob=='electromagnit':
     dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromelectrodmg']
     dmg=round(dmg, 2)
     t['hp']-=dmg
     end(creatorid, team, mob, number, t, dmg)
   
   elif mob=='manoed':
     dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromghostdmg']
     dmg=round (dmg, 2)
     t['hp']-=dmg    
     end(creatorid, team, mob, number, t, dmg)
   
   elif mob=='pyos' or mob=='tiranozavr':
     dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['frombiodmg']
     dmg=round (dmg, 2)
     t['hp']-=dmg    
     end(creatorid, team, mob, number, t, dmg)
 
    
    
   
        
    
    
def skills(mob, creatorid, team, team2, number):
    if mob=='s_me4nik':
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
              t=mobdmg(mob, creatorid, team, team2, number)
              if t!='None' and t!=None:
                z=random.randint(1,100)
                if z<=25:
                  t['fromdeaddmg']+=0.6
                  skilltext='"Проклятье мертвецов"'
                else:
                  skilltext=''
                mobturn(creatorid, team, mob, number, t)
         info.lobby.game[creatorid][team][mob][number]['ready']=1

                



                    
    elif mob=='electromagnit':
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
              t=mobdmg(mob, creatorid, team, team2, number)
              if t!='None' and t!=None:
                z=random.randint(1,100)
                if z<=30:
                    t['damage']-=45  
                    skilltext='"Разряд"'
                else:
                    skilltext=''
                mobturn(creatorid, team, mob, number, t)
         info.lobby.game[creatorid][team][mob][number]['ready']=1

          
                  

                
    elif mob=='phoenix':
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
              t=mobdmg(mob, creatorid, team, team2, number)
              if t!='None' and t!=None:
                skilltext=''
                mobturn(creatorid, team, mob, number, t)
         info.lobby.game[creatorid][team][mob][number]['ready']=1

                
    elif mob=='manoed':
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
              t=mobdmg(mob, creatorid, team, team2, number)
              if t!='None' and t!=None:
                z=random.randint(1,100)
                if z<45:
                    skilltext='Проникновение'
                    if t['mana']>0:
                      a=70
                      t['mana']-=a                
                      b=0+t['mana']
                      if b<0:
                        t['mana']-=b
                        a+=b
                        t['hp']-=a
                      else:
                        t['hp']-=a
                mobturn(creatorid, team, mob, number, t)
         info.lobby.game[creatorid][team][mob][number]['ready']=1


                
    elif mob=='pyos':
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
               t=mobdmg(mob, creatorid, team, team2, number)
               if t!=None and t!='None':
                 x=random.randint(1,100)
                 if x<=50:
                  typemob1=classtoemoji(info.lobby.game[creatorid][team][mob][number]['type'])
                  emoj1= emojize(typemob1, use_aliases=True)
                  emojattack=emojize(':arrow_right:', use_aliases=True)
                  emojdie=emojize(':x:', use_aliases=True)
                  emojdmg=emojize(':broken_heart:', use_aliases=True)
                  emojhp=emojize(':green_heart:', use_aliases=True)
                  if team=='t1mobs':
                    info.lobby.game[creatorid]['throne2hp']-=100
                    info.lobby.game[creatorid][team][mob][number]['skilltext']=emoj1+'Pyos'+emojattack+'Крепость'+emojdmg+'100.0'+emojhp+str(info.lobby.game[creatorid]['throne2hp'])+"\n"
                  elif team=='t2mobs':
                    info.lobby.game[creatorid]['throne1hp']-=100
                    info.lobby.game[creatorid][team][mob][number]['skilltext']=emoj1+'Pyos'+emojattack+'Крепость'+emojdmg+'100.0'+emojhp+str(info.lobby.game[creatorid]['throne1hp'])+"\n"
               mobturn(creatorid, team, mob, number, t)  
         info.lobby.game[creatorid][team][mob][number]['ready']=1
        
    elif mob=='tiranozavr':
        if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
               t=mobdmg(mob, creatorid, team, team2, number)
               if t!=None and t!='None':
                 x=random.randint(1,100)
                 if x<=40:
                  if len(info.lobby.game[creatorid][team2])>0:
                    d=list(info.lobby.game[creatorid][team2].keys())
                    c=random.choice(d)
                    g=list(info.lobby.game[creatorid][team2][c].keys())
                    b=random.choice(g)
                    if d!=
                    info.lobby.game[creatorid][team2][c][b]['stun']=1
                    if info.lobby.game[creatorid][team2][c][b]['ready']==1:
                      info.lobby.game[creatorid][team2][c][b]['stun']=2
               mobturn(creatorid, team, mob, number, t)   
        info.lobby.game[creatorid][team][mob][number]['ready']=1    
                    
                    
     

       
        

   

                
            
                    
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
           if len(info.lobby.game[creatorid]['t1mobs'][name])==0:
              info.lobby.game[creatorid]['t1mobs'][name]=createmob1(nametoclass(name), 1, name)
              number+=1
           else:
              diction=createmob1(nametoclass(name),(len(info.lobby.game[creatorid]['t1mobs'][name])+1), name)
              info.lobby.game[creatorid]['t1mobs'][name].update(diction)
              number+=1
 for id in info.lobby.game[creatorid]['team2']:
    for name in info.lobby.game[creatorid]['players'][id]['allmobs']:
        if name in info.lobby.game[creatorid]['players'][id]['portals']:
          number=0
          while number<info.lobby.game[creatorid]['players'][id]['portals'][name]['count']:   
              if len(info.lobby.game[creatorid]['t2mobs'][name])==0:               
                info.lobby.game[creatorid]['t2mobs'][name]=createmob1(nametoclass(name), 1, name)
                number+=1
              else:
                diction2=createmob1(nametoclass(name),(len(info.lobby.game[creatorid]['t2mobs'][name])+1), name)
                info.lobby.game[creatorid]['t2mobs'][name].update(diction2)
                number+=1
 allmobs=0
 for mobs2x in info.lobby.game[creatorid]['t1mobs']:
    for xyz2x in info.lobby.game[creatorid]['t1mobs'][mobs2x]:
      allmobs+=1
 for mobs2xx in info.lobby.game[creatorid]['t2mobs']:
    for xyz2xx in info.lobby.game[creatorid]['t2mobs'][mobs2xx]:
      allmobs+=1 
 readymobs=0
 e=0
 j=0
 info.lobby.game[creatorid]['t1hod']=random.randint(0,1)
 while readymobs<allmobs: 
   readymobs=0
   if info.lobby.game[creatorid]['t1hod']==0:
            e+=1
            print('1')
            if e>2:
              info.lobby.game[creatorid]['t1hod']=1
   elif info.lobby.game[creatorid]['t1hod']==1:
            j+=1
            print('2')
            if j>1:
               info.lobby.game[creatorid]['t1hod']=0 
   for mob1 in info.lobby.game[creatorid]['t1mobs']:
        for number111 in info.lobby.game[creatorid]['t1mobs'][mob1]:
           if info.lobby.game[creatorid]['t1hod']==1:
            if info.lobby.game[creatorid]['t1mobs'][mob1][number111]['ready']!=1:
             skills(mob1, creatorid, 't1mobs', 't2mobs', number111)
             info.lobby.game[creatorid]['t1hod']=0
             e=0       
   for mob2 in info.lobby.game[creatorid]['t2mobs']:
       for number222 in info.lobby.game[creatorid]['t2mobs'][mob2]:
         if info.lobby.game[creatorid]['t1hod']==0:
          if info.lobby.game[creatorid]['t2mobs'][mob2][number222]['ready']!=1:
           skills(mob2, creatorid, 't2mobs', 't1mobs', number222)
           info.lobby.game[creatorid]['t1hod']=1
           j=0
   for readymob1 in info.lobby.game[creatorid]['t1mobs']:
     for readynumber1 in info.lobby.game[creatorid]['t1mobs'][readymob1]:
       if info.lobby.game[creatorid]['t1mobs'][readymob1][readynumber1]['ready']==1:
         readymobs+=1
   for readymob2 in info.lobby.game[creatorid]['t2mobs']:
     for readynumber2 in info.lobby.game[creatorid]['t2mobs'][readymob2]:
       if info.lobby.game[creatorid]['t2mobs'][readymob2][readynumber2]['ready']==1:
         readymobs+=1


 for mobs2 in info.lobby.game[creatorid]['t1mobs']:
    for xyz2 in info.lobby.game[creatorid]['t1mobs'][mobs2]:
      if info.lobby.game[creatorid]['t1mobs'][mobs2][xyz2]['hp']<1:
        info.lobby.game[creatorid]['t1mobs'][mobs2][xyz2]['smert']=1
        
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
 droplet=emojize(':droplet:', use_aliases=True)
 te=emojize(':busts_in_silhouette:', use_aliases=True)
 bot.send_message(info.lobby.game[creatorid]['chatid'],'Ход '+str(info.lobby.game[creatorid]['hod'])+':'+"\n"+te+'Команда "Штурм": '+info.lobby.game[creatorid]['teammates1']+"\n"+te+'Команда "Оборона": '+info.lobby.game[creatorid]['teammates2']+"\n"+"\n"+info.lobby.game[creatorid]['resultst1']+"\n"+'Кол-во выживших существ команды "Штурм": '+str(livemobs1)+"\n"+'Каждый игрок команды получил '+droplet+str(info.lobby.game[creatorid]['manaplust2']/len(info.lobby.game[creatorid]['team2']))+' маны за своих убитых существ!'+"\n"+"\n"+info.lobby.game[creatorid]['resultst2']+"\n"+'Кол-во выживших существ команды "Оборона": '+str(livemobs2)+"\n"+'Каждый игрок команды получил '+droplet+str(info.lobby.game[creatorid]['manaplust1']/len(info.lobby.game[creatorid]['team1']))+' маны за своих убитых существ!') 
 info.lobby.game[creatorid]['resultst1']='Результаты монстров из команды "Штурм":'+"\n"
 info.lobby.game[creatorid]['resultst2']='Результаты монстров из команды "Оборона":'+"\n"
 info.lobby.game[creatorid]['manaplust1']=0
 info.lobby.game[creatorid]['manaplust2']=0
 for endid in info.lobby.game[creatorid]['players']:
    info.lobby.game[creatorid]['players'][endid]['ready']=0
    info.lobby.game[creatorid]['readys']=0
    info.lobby.game[creatorid]['players'][endid]['mobsinturn']=[]
    info.lobby.game[creatorid]['players'][endid]['portals']={'s_me4nik':{'count':0},
                  'phoenix':{'count':0},
                  'electromagnit':{'count':0},
                  'manoed':{'count':0},
                  'pyos':{'count':0}}                 
    info.lobby.game[creatorid]['players'][endid]
 for mob10 in info.lobby.game[creatorid]['t1mobs']:
    for number10 in info.lobby.game[creatorid]['t1mobs'][mob10]:
      info.lobby.game[creatorid]['t1mobs'][mob10][number10]['target']=None
      info.lobby.game[creatorid]['t1mobs'][mob10][number10]['maxkoef']=0
      info.lobby.game[creatorid]['t1mobs'][mob10][number10]['mob']=None
      info.lobby.game[creatorid]['t1mobs'][mob10][number10]['team']=None
      info.lobby.game[creatorid]['t1mobs'][mob10][number10]['number']=None
      info.lobby.game[creatorid]['t1mobs'][mob10][number10]['t']=None
      info.lobby.game[creatorid]['t1mobs'][mob10][number10]['skilltext']='None'
      info.lobby.game[creatorid]['t1mobs'][mob10][number10]['ready']=0
      info.lobby.game[creatorid]['t1mobs'][mob10][number10]['stun']-=1
        
 for mob11 in info.lobby.game[creatorid]['t2mobs']:
    for number11 in info.lobby.game[creatorid]['t2mobs'][mob11]:
      info.lobby.game[creatorid]['t2mobs'][mob11][number11]['target']=None
      info.lobby.game[creatorid]['t2mobs'][mob11][number11]['maxkoef']=0
      info.lobby.game[creatorid]['t2mobs'][mob11][number11]['mob']=None
      info.lobby.game[creatorid]['t2mobs'][mob11][number11]['team']=None
      info.lobby.game[creatorid]['t2mobs'][mob11][number11]['number']=None
      info.lobby.game[creatorid]['t2mobs'][mob11][number11]['t']=None
      info.lobby.game[creatorid]['t2mobs'][mob11][number11]['skilltext']='None'
      info.lobby.game[creatorid]['t2mobs'][mob11][number11]['ready']=0
      info.lobby.game[creatorid]['t2mobs'][mob11][number11]['stun']-=1
 info.lobby.game[creatorid]['hod']+=1
 livemob1=0
 livemob2=0
 mobdmageall=0
 for mobtothrone1 in info.lobby.game[creatorid]['t1mobs']:
    for numberthrone1 in info.lobby.game[creatorid]['t1mobs'][mobtothrone1]:
      if info.lobby.game[creatorid]['t1mobs'][mobtothrone1][numberthrone1]['smert']!=1:
        livemob1+=1
 for mobtothrone2 in info.lobby.game[creatorid]['t2mobs']:
    for numberthrone2 in info.lobby.game[creatorid]['t2mobs'][mobtothrone2]:
      if info.lobby.game[creatorid]['t2mobs'][mobtothrone2][numberthrone2]['smert']!=1:
        livemob2+=1
        
 if livemob1==0 and livemob2>0:
   for mbs in info.lobby.game[creatorid]['t2mobs']:
     for nmbs in info.lobby.game[creatorid]['t2mobs'][mbs]:
      typemob1=classtoemoji(info.lobby.game[creatorid]['t2mobs'][mbs][nmbs]['type'])
      throne=emojize(':european_castle:', use_aliases=True)
      emoj1=emojize(typemob1, use_aliases=True)
      emojattack=emojize(':arrow_right:', use_aliases=True)
      emojdmg=emojize(':broken_heart:', use_aliases=True)
      emojhp=emojize(':green_heart:', use_aliases=True)
      if info.lobby.game[creatorid]['t2mobs'][mbs][nmbs]['smert']!=1:
       mobdmageall+=info.lobby.game[creatorid]['t2mobs'][mbs][nmbs]['damage']
       mobdmage=info.lobby.game[creatorid]['t2mobs'][mbs][nmbs]['damage']
       info.lobby.game[creatorid]['thronedamagemobs']+=emoj1+info.lobby.game[creatorid]['t2mobs'][mbs][nmbs]['name']+emojattack+throne+'Крепость'+emojdmg+str(mobdmage)+emojhp+str(info.lobby.game[creatorid]['throne1hp']-mobdmage)+"\n"
       info.lobby.game[creatorid]['throne1hp']-=mobdmage
       info.lobby.game[creatorid]['t2mobs'][mbs][nmbs]['smert']=1
       info.lobby.game[creatorid]['t2mobs'][mbs][nmbs]['hp']=0
   info.lobby.game[creatorid]['thronedamage']=info.lobby.game[creatorid]['thronedamagemobs']+"\n"+'Мобы из команды "Оборона" нанесли '+str(mobdmageall)+' урона по крепости команды "Штурм"! Теперь у неё '+str(info.lobby.game[creatorid]['throne1hp'])+' хп! А все атакующие её мобы погибли.'    
 elif livemob2==0 and livemob1>0:
    for mbs2 in info.lobby.game[creatorid]['t1mobs']:
     for nmbs2 in info.lobby.game[creatorid]['t1mobs'][mbs2]:
      typemob1=classtoemoji(info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['type'])
      throne=emojize(':european_castle:', use_aliases=True)
      emoj1=emojize(typemob1, use_aliases=True)
      emojattack=emojize(':arrow_right:', use_aliases=True)
      emojdmg=emojize(':broken_heart:', use_aliases=True)
      emojhp=emojize(':green_heart:', use_aliases=True)
      if info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['smert']!=1:
       mobdmageall+=info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['damage']
       mobdmage=info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['damage']
       info.lobby.game[creatorid]['thronedamagemobs']+=emoj1+info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['name']+emojattack+throne+'Крепость'+emojdmg+str(mobdmage)+emojhp+str(info.lobby.game[creatorid]['throne2hp']-mobdmage)+"\n"
       info.lobby.game[creatorid]['throne2hp']-=mobdmage 
       info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['smert']=1
       info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['hp']=0
    info.lobby.game[creatorid]['thronedamage']=info.lobby.game[creatorid]['thronedamagemobs']+"\n"+'Мобы из команды "Штурм" нанесли '+str(mobdmageall)+' урона по крепости команды "Оборона"! Теперь у неё '+str(info.lobby.game[creatorid]['throne2hp'])+' хп! А все атакующие её мобы погибли.'
 elif livemob2==0 and livemob1==0:
    info.lobby.game[creatorid]['thronedamage']='Урона по крепостям нанесено не было!'
 elif livemob2>0 and livemob1>0:
    info.lobby.game[creatorid]['thronedamage']='Урона по крепостям нанесено не было!'
 bot.send_message(info.lobby.game[creatorid]['chatid'], info.lobby.game[creatorid]['thronedamage'])
 info.lobby.game[creatorid]['thronedamage']=''
 info.lobby.game[creatorid]['thronedamagemobs']=''
 if info.lobby.game[creatorid]['throne2hp']<1 or info.lobby.game[creatorid]['throne1hp']<1:
   if info.lobby.game[creatorid]['throne2hp']<info.lobby.game[creatorid]['throne1hp']:
    bot.send_message(info.lobby.game[creatorid]['chatid'], 'Победа команды "Штурм"!')
    del info.lobby.game[creatorid]
   elif info.lobby.game[creatorid]['throne2hp']>info.lobby.game[creatorid]['throne1hp']:
    bot.send_message(info.lobby.game[creatorid]['chatid'], 'Победа команды "Оборона"!')
    del info.lobby.game[creatorid]
 else:
   battle(info.lobby.game[creatorid]['creatorid']['selfid'])
                                                                              
                                                                              
    
    
    
            
            
            
            


def nametoclass(name):  #делает перевод названия сущ-ва в ссылку на класс
    if name=='s_me4nik':
        x=info.s_me4nik
    elif name=='phoenix':
        x=info.phoenix
    elif name=='electromagnit':
        x=info.electromagnit
    elif name=='manoed':
        x=info.manoed
    elif name=='pyos':
        x=info.pyos
    elif name=='tiranozavr':
        x=info.tiranozavr
         
    return x



def mobs(callid):    #выбирает 3х рандомных мобов для возможности спавна
    for id in info.lobby.game:
      if callid in info.lobby.game[id]['players']:
            while len(info.lobby.game[id]['players'][callid]['mobsinturn'])<3:
              x=random.randint(1,len(info.lobby.game[id]['players'][callid]['allmobs']))
              if info.lobby.game[id]['players'][callid]['allmobs'][x-1] not in info.lobby.game[id]['players'][callid]['mobsinturn']:
               if info.lobby.game[id]['players'][callid]['allmobs'][x-1] not in ban:
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
        if call.from_user.id in info.lobby.game[id]['players']:  
          testturn(info.lobby.game[id]['creatorid']['selfid'], call.from_user.id)


           
          
          
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
            if info.lobby.game[id]['players'][call.from_user.id]['portals']['s_me4nik']['count']==0:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['s_me4nik']=createportal('s_me4nik', 1)  
            else:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['s_me4nik']=createportal('s_me4nik', info.lobby.game[id]['players'][call.from_user.id]['portals']['s_me4nik']['count']+1)  
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
            if info.lobby.game[id]['players'][call.from_user.id]['portals']['phoenix']['count']==0:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['phoenix']=createportal('phoenix', 1)  
            else:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['phoenix']=createportal('phoenix', info.lobby.game[id]['players'][call.from_user.id]['portals']['phoenix']['count']+1)  
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
            if info.lobby.game[id]['players'][call.from_user.id]['portals']['electromagnit']['count']==0:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['electromagnit']=createportal('electromagnit', 1)  
            else:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['electromagnit']=createportal('electromagnit', info.lobby.game[id]['players'][call.from_user.id]['portals']['electromagnit']['count']+1)  
            bot.send_message(call.from_user.id, 'Вы успешно призвали портал (Электромагнитень)!'+"\n"+'Теперь у вас '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['electromagnit']['count'])+' таких порталов!')
           else:
            bot.send_message(call.from_user.id, 'Недостаточно маны!')
            
  elif call.data=='manoed': 
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
         if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
          if 'manoed' in info.lobby.game[id]['players'][call.from_user.id]['mobsinturn']:
           if info.lobby.game[id]['players'][call.from_user.id]['mana']>=info.manoed.cost:
            info.lobby.game[id]['players'][call.from_user.id]['mana']-=info.manoed.cost
            if info.lobby.game[id]['players'][call.from_user.id]['portals']['manoed']['count']==0:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['manoed']=createportal('manoed', 1)  
            else:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['manoed']=createportal('manoed', info.lobby.game[id]['players'][call.from_user.id]['portals']['manoed']['count']+1)  
            bot.send_message(call.from_user.id, 'Вы успешно призвали портал (Маноед)!'+"\n"+'Теперь у вас '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['manoed']['count'])+' таких порталов!')
           else:
            bot.send_message(call.from_user.id, 'Недостаточно маны!')
            
            
  elif call.data=='pyos':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
         if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
          if 'pyos' in info.lobby.game[id]['players'][call.from_user.id]['mobsinturn']:
           if info.lobby.game[id]['players'][call.from_user.id]['mana']>=info.pyos.cost:
            info.lobby.game[id]['players'][call.from_user.id]['mana']-=info.pyos.cost
            if info.lobby.game[id]['players'][call.from_user.id]['portals']['pyos']['count']==0:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['pyos']=createportal('pyos', 1)  
            else:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['pyos']=createportal('pyos', info.lobby.game[id]['players'][call.from_user.id]['portals']['pyos']['count']+1)  
            bot.send_message(call.from_user.id, 'Вы успешно призвали портал (Pyos)!'+"\n"+'Теперь у вас '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['pyos']['count'])+' таких порталов!')
           else:
            bot.send_message(call.from_user.id, 'Недостаточно маны!')
            
  elif call.data=='tiranozavr':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
         if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
          if 'tiranozavr' in info.lobby.game[id]['players'][call.from_user.id]['mobsinturn']:
           if info.lobby.game[id]['players'][call.from_user.id]['mana']>=info.tiranozavr.cost:
            info.lobby.game[id]['players'][call.from_user.id]['mana']-=info.tiranozavr.cost
            if info.lobby.game[id]['players'][call.from_user.id]['portals']['tiranozavr']['count']==0:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['tiranozavr']=createportal('pyos', 1)  
            else:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['tiranozavr']=createportal('tiranozavr', info.lobby.game[id]['players'][call.from_user.id]['portals']['tiranozavr']['count']+1)  
            bot.send_message(call.from_user.id, 'Вы успешно призвали портал (Тиранозавр)!'+"\n"+'Теперь у вас '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['tiranozavr']['count'])+' таких порталов!')
           else:
            bot.send_message(call.from_user.id, 'Недостаточно маны!')
   
                
   
       
                 
            
    
  
def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode='Markdown'):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)

@bot.message_handler(commands=['electro'])
def electro(message):
    emojelectro=emojize(':zap:', use_aliases=True)
    emojbio=emojize(':evergreen_tree:', use_aliases=True)
    emojfire=emojize(':fire:', use_aliases=True)
    emojghost=emojize(':ghost:', use_aliases=True)
    emojundead=emojize(':skull:', use_aliases=True)
    bot.send_message(message.from_user.id, emojelectro+'Электро:'+"\n"+'Оболочка этих монстров состоит из плоти, а внутренности отсутствуют. Вместо них внутри монстра присутствует электричество, заполняющее всё тело и контролирующее его. У существ этого типа есть свой запас маны, за счёт которого они и удерживают электричество в теле.'+"\n"+
                    'Наносимый урон:'+"\n"+'По '+emojbio+'био: 130%'+"\n"+'По '+emojfire+'огненным: 50%'+"\n"+'По '+emojghost+'призрачным: 150%'+"\n"+'По '+emojundead+'мертвецам: 100%'+"\n"+"\n"+
                     'Получаемый урон:'+"\n"+'От '+emojbio+'био: 100%'+"\n"+'От '+emojfire+'огненных: 50%'+"\n"+'От '+emojghost+'призрачных: 80%'+"\n"+'От '+emojundead+'мертвецов: 150%'+"\n"+"\n"+
                     'Скиллы:'+"\n"+'"Разряд" (присутствует у: Электромагнитень) - бьёт разрядом по врагу, и с 30% шансом отнимает у существа, которое атакует, 45 урона (урон может уйти в минус!)'
                    )
    
    
@bot.message_handler(commands=['bio'])
def bio(message):
    emojelectro=emojize(':zap:', use_aliases=True)
    emojbio=emojize(':evergreen_tree:', use_aliases=True)
    emojfire=emojize(':fire:', use_aliases=True)
    emojghost=emojize(':ghost:', use_aliases=True)
    emojundead=emojize(':skull:', use_aliases=True)
    bot.send_message(message.from_user.id, emojbio+'Биологические:'+"\n"+'Существа, состоящие из плоти и крови. Имеют стандартный набор свойств, олицетворяющих живое существо в людском мире.'+"\n"+
                     'Наносимый урон:'+"\n"+'По '+emojfire+'огненным: 70%'+"\n"+'По '+emojghost+'призрачным: 75%'+"\n"+'По '+emojundead+'мертвецам: 150%'+"\n"+'По '+emojelectro+'электро: 100%'+"\n"+"\n"+
                     'Получаемый урон:'+"\n"+'От '+emojfire+'огненных: 150%'+"\n"+'От '+emojghost+'призрачных: 80%'+"\n"+'От '+emojundead+'мертвецов: 110%'+"\n"+'От '+emojelectro+'электро: 130%'+"\n"+"\n"+
                     'Скиллы:'+"\n"+'"Запрограммировать бота" (присутствует у: Pyos (Уникальный моб Пйоса)) - с 25% шансом программирует бота, который игнорируя поле боя, дамажит крепость соперника на 100 единиц урона'
                    )
    
    
@bot.message_handler(commands=['fire'])
def fire(message):
    emojelectro=emojize(':zap:', use_aliases=True)
    emojbio=emojize(':evergreen_tree:', use_aliases=True)
    emojfire=emojize(':fire:', use_aliases=True)
    emojghost=emojize(':ghost:', use_aliases=True)
    emojundead=emojize(':skull:', use_aliases=True)
    bot.send_message(message.from_user.id, emojfire+'Огненные:'+"\n"+'Существа, сформированные из огня в подземном мире, где температура достигает очень высоких величин. Портал призывает их прямо оттуда, чтобы они не успели угаснуть.'+"\n"+
                     'Наносимый урон:'+"\n"+'По '+emojghost+'призрачным: 90%'+"\n"+'По '+emojundead+'мертвецам: 110%'+"\n"+'По '+emojelectro+'электро: 50%'+"\n"+'По '+emojbio+'био: 150%'+"\n"+"\n"+
                     'Получаемый урон:'+"\n"+'От '+emojghost+'призрачных: 150%'+"\n"+'От '+emojundead+'мертвецов: 120%'+"\n"+'От '+emojelectro+'электро: 50%'+"\n"+'От '+emojbio+'био: 70%'+"\n"+"\n"+
                     'Скиллы:'+"\n"+'Пока что ни у одного существа типа "огненные" скиллов нет.'
                    )
    
@bot.message_handler(commands=['ghost'])
def ghost(message):   
    emojelectro=emojize(':zap:', use_aliases=True)
    emojbio=emojize(':evergreen_tree:', use_aliases=True)
    emojfire=emojize(':fire:', use_aliases=True)
    emojghost=emojize(':ghost:', use_aliases=True)
    emojundead=emojize(':skull:', use_aliases=True)
    bot.send_message(message.from_user.id, emojghost+'Призрачные:'+"\n"+'Монстры, имеющие полу-материальное тело, что позволяет им получать меньше повреждений от физического мира, но от электро-монстров урона они получают очень много'+"\n"+
                     'Наносимый урон:'+"\n"+'По '+emojundead+'мертвецам: 110%'+"\n"+'По '+emojelectro+'электро: 80%'+"\n"+'По '+emojbio+'био: 80%'+"\n"+'По '+emojfire+'огненным: 150%'+"\n"+"\n"+    
                     'Получаемый урон:'+"\n"+'От '+emojundead+'мертвецов: 75%'+"\n"+'От '+emojelectro+'электро: 150%'+"\n"+'От '+emojbio+'био: 75%'+"\n"+'От '+emojfire+'огненных: 90%'+"\n"+"\n"+ 
                     'Скиллы:'+"\n"+'"Проникновение" (присутствует у: Маноед) - с шансом 45% отнимает у цели до 70 маны (у цели остается не меньше, чем 0), и наносит урон, соответствующий выжженной мане'
                    )
    
    
@bot.message_handler(commands=['undead'])
def undead(message):
    emojelectro=emojize(':zap:', use_aliases=True)
    emojbio=emojize(':evergreen_tree:', use_aliases=True)
    emojfire=emojize(':fire:', use_aliases=True)
    emojghost=emojize(':ghost:', use_aliases=True)
    emojundead=emojize(':skull:', use_aliases=True)
    bot.send_message(message.from_user.id, emojundead+'Мертвецы:'+"\n"+'Существа, которые уже мертвы, и поэтому самый действенный способ убить их - физическое уничтожение частей тела.'+"\n"+
                     'Наносимый урон:'+"\n"+'По '+emojelectro+'электро: 150%'+"\n"+'По '+emojbio+'био: 110%'+"\n"+'По '+emojfire+'огненным: 120%'+"\n"+'По '+emojghost+'призракам: 75%'+"\n"+"\n"+  
                     'Получаемый урон:'+"\n"+'От '+emojelectro+'электро: 70%'+"\n"+'От '+emojbio+'био: 150%'+"\n"+'От '+emojfire+'огненных: 100%'+"\n"+'От '+emojghost+'призраков: 90%'+"\n"+"\n"+ 
                     'Скиллы:'+"\n"+'"Проклятье мертвецов" (присутствует у: Скелет-мечник) - имеет 15% шанс при атаке цели повысить получаемый ей урон от мертвецов на 60% (складывается от нескольких применений скилла по одной цели).'
                    )
    
 
    
    
                     


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
            for ids2 in info.lobby.game[message.from_user.id]['team2']:
                bot.send_message(ids2, 'Вы в обороне! Ваша команда: '+info.lobby.game[message.from_user.id]['teammates2'])
            for ids1 in info.lobby.game[message.from_user.id]['team1']:
                bot.send_message(ids1, 'Вы штурмуете крепость! Ваша команда: '+info.lobby.game[message.from_user.id]['teammates1'])
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
           x=0
           for id in info.lobby.game:                    
             if message.from_user.id in info.lobby.game[id]['players']:
               x+=1
             if x<1:        
              try:
               bot.send_message(message.from_user.id, 'Вы успешно присоединились!')
               info.lobby.game[key]['players'][message.from_user.id]=createuser(message.from_user.id, 1, message.from_user.first_name)
               info.lobby.game[key]['players'][message.from_user.id]['cash']=info.lobby.game[id]['name']
               info.lobby.game[key]['len']+=1
               bot.send_message(message.chat.id, 'Вы успешно присоединились в игру ('+str(info.lobby.game[key]['players'][message.from_user.id]['cash'])+')! Для начала игры её создатель должен нажать /fight')
              except:
                bot.send_message(message.chat.id, 'Для начала надо начать разговор с @MagicWarsBot !')
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
 try:
  bot.send_message(message.from_user.id, 'Чтобы сыграть в игру, добавьте меня в чат и напишите /begin для начала набора игроков. В одном чате можно запустить несколько игр, но один игрок может присутствовать только в одной из них'+"\n"+      
                   'В этой игре вы играете за одного из магов, который обороняет свою крепость, или нападает на чужую! '+
                   'Чтобы атаковать врага, вы чертите на земле специальные символы, открывая портал, из которого появляется одно из ваших выбранных '+
                   'существ (для открытия портала требуется мана), которое вступает в бой с существами врагов, и разделавшись с ними, идет в атаку на крепость.'+
                   ' Все существа полностью самостоятельны, вам лишь нужно грамотно выбрать порталы для их появления.'+'В каждом раунде вам даются 3 случайно выбранных портала, которые вы можете открывать.'+'Можно играть команда на команду!'+"\n"+'Цель игры: уничтожить крепость соперника.'+"\n"+'Всего в игре есть 5 классов существ:'+"\n"+'электро, биологические, огненные, призрачные и мертвецы.'+"\n"+
                    'Чтобы узнать про каждый: /electro, /bio, /fire, /ghost, /undead. (От своего класса мобы всегда получают 100% урон)')
 except:
        bot.send_message(message.chat.id, 'Для начала надо начать разговор с @MagicWarsBot !')



@bot.message_handler(commands=['begin'])
def beginmessage(message):
  if message.from_user.id not in info.lobby.game:
   if message.chat.id<0:
    userapply=0
    try:
      bot.send_message(message.from_user.id, 'Вы создали лобби!')
      userapply=1
    except:
      bot.send_message(message.chat.id, 'Для начала надо начать разговор с @MagicWarsBot !')
    if userapply==1:
      createdlobby=createlobby(message.chat.id, message.from_user.id, message.from_user.first_name)
      info.lobby.game.update(createdlobby)
      print(info.lobby.game)
      bot.send_message(message.chat.id, 'Лобби создано! Назовите его, отправив название следующим сообщением.'+"\n"+'Если вы хотите отменить игру - нажмите /cancel.'+"\n"+'Игра автоматически удалится через 5 минут!')
      info.lobby.game[message.from_user.id]['naming']=1
      lobbycancel=threading.Timer(300.0, cancel, args=[message.from_user.id, message.chat.id])
      lobbycancel.start()
        
   else:
    bot.send_message(message.from_user.id, 'Играть можно только в группах!')
    
  
  
@bot.message_handler(content_types=['text'])
def namemessage(message):
  if message.from_user.id in info.lobby.game:
    if info.lobby.game[message.from_user.id]['creatorid']['selfid']==message.from_user.id:
      if info.lobby.game[message.from_user.id]['naming']==1:
        if len(message.text)<31:
         if message.text!='None':
          if message.chat.id==info.lobby.game[message.from_user.id]['chatid']:
            info.lobby.game[message.from_user.id]['name']=message.text
            bot.send_message(message.chat.id, 'Вы назвали лобби! ('+message.text+').'+"\n"+'Ожидайте игроков (/join для присоединения).')
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
  return{creatorid: {
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
    't1mobs':{'s_me4nik':{},
                  'phoenix':{},
                  'electromagnit':{},
                  'manoed':{},
                  'pyos':{},
                  'tiranozavr':{}
             },
    't2mobs':{'s_me4nik':{},
                  'phoenix':{},
                  'electromagnit':{},
                  'manoed':{},
                  'pyos':{},
                  'tiranozavr':{}
             },
    'resultst1':'Результаты монстров из команды "Штурм"'+"\n",
    'resultst2':'Результаты монстров из команды "Оборона"'+"\n",
    'readys':0,
    'launchtimer':0,
    'timer':None,
    'hod':1,
    'teammates1':'',
    'teammates2':'',
    'throne1hp':1000,
    'throne2hp':1000,
    'thronedamage':'',
    'manaplust1':0,
    'manaplust2':0,
    't1hod':0,
    'thronedamagemobs':''
      

           }
        }
  
  
def createuser(id, x, fname):
    if id==197216910 or id==441399484:
        return{'selfid':id,
         'lastmessage':0,
         'tvari':{'s_me4nik':{},
                  'phoenix':{},
                  'electromagnit':{},
                  'manoed':{},
                  'pyos':{},
                  'tiranozavr':{}
         },
         'portals':{'s_me4nik':{'count':0},
                  'phoenix':{'count':0},
                  'electromagnit':{'count':0},
                  'manoed':{'count':0},
                  'pyos':{'count':0},
                  'tiranozavr':{'count':0}

                   },
         'mana':150,
         'mobnumber':0,
         'manamax':500,
         'inlobby':x,
         'cash':'',
         'allmobs':['s_me4nik', 'electromagnit', 'phoenix', 'manoed', 'pyos', 'tiranozavr'],
         'mobsinturn':[],
         'name1mob':'',
         'name2mob':'',
         'name3mob':'',
         'ready':0,
         'fname':fname,
         'currentmessage':'',
         'manaregen':40
            }  
    else:  
      return{'selfid':id,
         'lastmessage':0,
         'tvari':{'s_me4nik':{},
                  'phoenix':{},
                  'electromagnit':{},
                  'manoed':{}
         },
         'portals':{'s_me4nik':{'count':0},
                  'phoenix':{'count':0},
                  'electromagnit':{'count':0},
                  'manoed':{'count':0},
                  'tiranozavr':{'count':0}
                   },
         'mana':150,
         'mobnumber':0,
         'manamax':500,
         'inlobby':x,
         'cash':'',
         'allmobs':['s_me4nik', 'electromagnit', 'phoenix', 'manoed', 'tiranozavr'],
         'mobsinturn':[],
         'name1mob':'',
         'name2mob':'',
         'name3mob':'',
         'ready':0,
         'fname':fname,
         'currentmessage':'',
         'manaregen':40
            }  
  
def createportal(name, x):  
    return {'name':name,
          'count':x
           }

    
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
        'smert':0,
        'cachedmg':0,
        'skilltext':'None',
        'stun':0
        }
    
def createmob1(nameclass, x, namemob):
      return{x:{
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
        'smert':0,
        'cachedmg':0,
        'skilltext':'None',
        'ready':0,
        'stun':0
                
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
      info.lobby.game[creatorid]['players'][key]['mana']+=info.lobby.game[creatorid]['players'][key]['manaregen']      
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



