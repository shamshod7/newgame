# -*- coding: utf-8 -*-
import redis
import os
import telebot
import math
import random
import threading
import info
import test
from telebot import types
from emoji import emojize
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)
base=[]
ban=['zombie']


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
            if t!=0:
              typemob2=classtoemoji(t['type'])
              emoj2= emojize(typemob2, use_aliases=True)
            typemob1=classtoemoji(info.lobby.game[creatorid][team][mob][number]['type'])
            emoj1= emojize(typemob1, use_aliases=True)
            emojattack=emojize(':crossed_swords:', use_aliases=True)
            emojdie=emojize(':x:', use_aliases=True)
            emojdmg=emojize(':broken_heart:', use_aliases=True)
            emojhp=emojize(':green_heart:', use_aliases=True)
            emojstun=emojize(':cyclone:', use_aliases=True)
            if team=='t1mobs':
                if info.lobby.game[creatorid][team][mob][number]['stun']<1:
                 if t['hp']<1:
                  for id in info.lobby.game[creatorid]['team2']:
                    info.lobby.game[creatorid]['players'][id]['mana']+=8
                    info.lobby.game[creatorid]['manaplust1']+=8
                    info.lobby.game[creatorid]['resultst1']+=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+' '+emojattack+' '+emoj2+t['name']+' '+emojdie+"\n"  
                 else:
                    info.lobby.game[creatorid]['resultst1']+=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+emojattack+emoj2+t['name']+emojdmg+str(dmg)+emojhp+str(t['hp'])+"\n"
                 if info.lobby.game[creatorid][team][mob][number]['skilltext']!='None':
                    info.lobby.game[creatorid]['skills1']+=info.lobby.game[creatorid][team][mob][number]['skilltext']+"\n"
                else:
                    info.lobby.game[creatorid]['resultst1']+=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+emojstun+"\n"
                 
            elif team=='t2mobs':
               if info.lobby.game[creatorid][team][mob][number]['stun']<1:
                 if t['hp']<1:
                   for id in info.lobby.game[creatorid]['team1']:
                    info.lobby.game[creatorid]['players'][id]['mana']+=8
                    info.lobby.game[creatorid]['manaplust2']+=8
                    info.lobby.game[creatorid]['resultst2']+=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+emojattack+emoj2+t['name']+emojdie+"\n"                 
                 else:
                    info.lobby.game[creatorid]['resultst2']+=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+emojattack+emoj2+t['name']+emojdmg+str(dmg)+emojhp+str(t['hp'])+"\n"
                 if info.lobby.game[creatorid][team][mob][number]['skilltext']!='None':
                    info.lobby.game[creatorid]['skills2']+=info.lobby.game[creatorid][team][mob][number]['skilltext']+"\n"
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
        text='O`liklar'
    elif name=='electro':
        text='Elektro'
    elif name=='fire':
        text='Olovlilar'
    elif name=='bio':
        text='Biologik'
    elif name=='ghost':
        text='Ruxlar'
    return text
          

def mobturn(creatorid, team, mob, number, t):
   if mob=='s_me4nik':
    if t['shield']==0:
     dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromdeaddmg']
    else:
     dmg=0
    dmg=round(dmg, 0)
    t['hp']-=dmg    
    end(creatorid, team, mob, number, t, dmg)
        
   elif mob=='phoenix':
     if t['shield']==0:
       dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromfiredmg']
     else:
       dmg=0
     dmg=round(dmg, 0)
     t['hp']-=dmg
     end(creatorid, team, mob, number, t, dmg)
   
   elif mob=='electromagnit':
     if t['shield']==0:
       dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromelectrodmg']
     else:
       dmg=0
     dmg=round(dmg, 0)
     t['hp']-=dmg
     end(creatorid, team, mob, number, t, dmg)
   
   elif mob=='manoed':
     if t['shield']==0:
       dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromghostdmg']
     else:
       dmg=0
     dmg=round (dmg, 0)
     t['hp']-=dmg    
     end(creatorid, team, mob, number, t, dmg)
   
   elif mob=='pyos' or mob=='tiranozavr': 
     if t['shield']==0:
       dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['frombiodmg']
     else:
       dmg=0
     dmg=round (dmg, 0)
     t['hp']-=dmg    
     end(creatorid, team, mob, number, t, dmg)
    
   elif mob=='s4upakabra':
     if t['shield']==0:
       dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromdeaddmg']
     else:
       dmg=0
     dmg=round (dmg, 0)
     t['hp']-=dmg  
     if info.lobby.game[creatorid][team][mob][number]['hp']>0:
       info.lobby.game[creatorid][team][mob][number]['hp']+=2
     end(creatorid, team, mob, number, t, dmg)
    
    
   elif mob=='golem':
     if t['shield']==0:
       dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromfiredmg']
     else:
       dmg=0
     dmg=round (dmg, 0)
     t['hp']-=dmg    
     end(creatorid, team, mob, number, t, dmg) 
        
   elif mob=='vsadnik':
    dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromghostdmg']
    dmg=round (dmg, 0)
    if team=='t1mobs':
        for mobs in info.lobby.game[creatorid]['t2mobs']:
          for numbers in info.lobby.game[creatorid]['t2mobs'][mobs]:
            if info.lobby.game[creatorid]['t2mobs'][mobs][numbers]['shield']!=1:
                info.lobby.game[creatorid]['t2mobs'][mobs][numbers]['hp']-=dmg                
    elif team=='t2mobs':
        for mobs in info.lobby.game[creatorid]['t1mobs']:
          for numbers in info.lobby.game[creatorid]['t1mobs'][mobs]:
            if info.lobby.game[creatorid]['t1mobs'][mobs][numbers]['shield']!=1:
                info.lobby.game[creatorid]['t1mobs'][mobs][numbers]['hp']-=dmg
    end(creatorid, team, mob, number, t, dmg) 
    
    
    
                
   elif mob=='soulcatcher':
     if t['shield']==0:
       dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromdeaddmg']
     else:
       dmg=0
     dmg=round (dmg, 0)
     t['hp']-=dmg  
     end(creatorid, team, mob, number, t, dmg)
    
    
   elif mob=='zombie':
     if t['shield']==0:
       dmg=info.lobby.game[creatorid][team][mob][number]['damage']*t['fromdeaddmg']
     else:
       dmg=0
     dmg=round (dmg, 0)
     t['hp']-=dmg  
     end(creatorid, team, mob, number, t, dmg)
    
    
    
   
        
    
     
def skills(mob, creatorid, team, team2, number):
    typemob1=classtoemoji(info.lobby.game[creatorid][team][mob][number]['type'])
    emoj1=emojize(typemob1, use_aliases=True)
    emojattack=emojize(':crossed_swords:', use_aliases=True)
    emojdie=emojize(':x:', use_aliases=True)
    emojdmg=emojize(':broken_heart:', use_aliases=True)
    emojhp=emojize(':green_heart:', use_aliases=True)
    emojstun=emojize(':cyclone:', use_aliases=True)
    emojskill=emojize(':eight_spoked_asterisk:', use_aliases=True)
    emojshield=emojize(':shield:', use_aliases=True)
    if mob=='s_me4nik':
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
          if info.lobby.game[creatorid][team][mob][number]['stun']<1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
              t=mobdmg(mob, creatorid, team, team2, number)
              if t!='None' and t!=None:
                typemob2=classtoemoji(t['type'])
                emoj2= emojize(typemob2, use_aliases=True)
                z=random.randint(1,100)
                if z<=25:
                  t['fromdeaddmg']+=1
                  info.lobby.game[creatorid][team][mob][number]['skilltext']=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+emojskill+emoj2+t['name']+' "O`liklar Lanati"'
                else:
                  info.lobby.game[creatorid][team][mob][number]['skilltext']='None'
                mobturn(creatorid, team, mob, number, t)
          else:
            end(creatorid, team, mob, number, 0, 0)
         info.lobby.game[creatorid][team][mob][number]['ready']=1

                



                    
    elif mob=='electromagnit':
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
          if info.lobby.game[creatorid][team][mob][number]['stun']<1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
              t=mobdmg(mob, creatorid, team, team2, number)
              if t!='None' and t!=None:
                typemob2=classtoemoji(t['type'])
                emoj2= emojize(typemob2, use_aliases=True)
                z=random.randint(1,100)
                if z<=35:
                    t['damage']-=2
                    info.lobby.game[creatorid][team][mob][number]['skilltext']=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+emojskill+emoj2+t['name']+' "Quvvat"'
                else:
                    skilltext=''
                mobturn(creatorid, team, mob, number, t)
          else:
            end(creatorid, team, mob, number, 0, 0)
         info.lobby.game[creatorid][team][mob][number]['ready']=1

          
                  

                
    elif mob=='phoenix':
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
          if info.lobby.game[creatorid][team][mob][number]['stun']<1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
              t=mobdmg(mob, creatorid, team, team2, number)
              if t!='None' and t!=None:
                mobturn(creatorid, team, mob, number, t)
          else:
            end(creatorid, team, mob, number, 0, 0)
         info.lobby.game[creatorid][team][mob][number]['ready']=1

                
    elif mob=='manoed':
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
          if info.lobby.game[creatorid][team][mob][number]['stun']<1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
              t=mobdmg(mob, creatorid, team, team2, number)
              if t!='None' and t!=None:
                typemob2=classtoemoji(t['type'])
                emoj2= emojize(typemob2, use_aliases=True)
                z=random.randint(1,100)
                if z<45:                   
                      info.lobby.game[creatorid][team][mob][number]['skilltext']=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+emojskill+emoj2+t['name']+' "Ichiga Kirish"'
                      t['hp']-=1
                mobturn(creatorid, team, mob, number, t)
          else:
            end(creatorid, team, mob, number, 0, 0)
         info.lobby.game[creatorid][team][mob][number]['ready']=1


                
    elif mob=='pyos':
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
          if info.lobby.game[creatorid][team][mob][number]['stun']<1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
               t=mobdmg(mob, creatorid, team, team2, number)
               if t!=None and t!='None':
                 x=random.randint(1,100)
                 if x<=25:
                     info.lobby.game[creatorid][team][mob][number]['shield']=1  
                     info.lobby.game[creatorid][team][mob][number]['skilltext']=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+emojskill+emojshield
                 mobturn(creatorid, team, mob, number, t)  
         info.lobby.game[creatorid][team][mob][number]['ready']=1
        
    elif mob=='tiranozavr':
        if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
          if info.lobby.game[creatorid][team][mob][number]['stun']<1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
               t=mobdmg(mob, creatorid, team, team2, number)
               x=random.randint(1,100)
               if x<=40:    
                  randomstun(creatorid, team2, info.lobby.game[creatorid][team][mob][number], 0)
               if t!=None and t!='None':
                   mobturn(creatorid, team, mob, number, t) 
          else:
            end(creatorid, team, mob, number, 0, 0)
        info.lobby.game[creatorid][team][mob][number]['ready']=1  
        
        
        
    elif mob=='s4upakabra':
        if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
          if info.lobby.game[creatorid][team][mob][number]['stun']<1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
               t=mobdmg(mob, creatorid, team, team2, number)                
               if t!=None and t!='None':
                   mobturn(creatorid, team, mob, number, t) 
          else:
            end(creatorid, team, mob, number, 0, 0)
        info.lobby.game[creatorid][team][mob][number]['ready']=1  
        
        
        
    elif mob=='golem':
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
          if info.lobby.game[creatorid][team][mob][number]['stun']<1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
              t=mobdmg(mob, creatorid, team, team2, number)
              if t!='None' and t!=None:
                mobturn(creatorid, team, mob, number, t)
          else:
            end(creatorid, team, mob, number, 0, 0)
         info.lobby.game[creatorid][team][mob][number]['ready']=1
     
    
    elif mob=='vsadnik':
         if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
          if info.lobby.game[creatorid][team][mob][number]['stun']<1:
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
              t=mobdmg(mob, creatorid, team, team2, number)
              if t!='None' and t!=None:
                info.lobby.game[creatorid][team][mob][number]['skilltext']=emoj1+info.lobby.game[creatorid][team][mob][number]['name']+emojdmg+''
                mobturn(creatorid, team, mob, number, t)
          else:
            end(creatorid, team, mob, number, 0, 0)
         info.lobby.game[creatorid][team][mob][number]['ready']=1
        
        
    elif mob=='soulcatcher':  
        if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
          if info.lobby.game[creatorid][team][mob][number]['stun']<1:
           x=random.randint(1,100)
           if x<=25:    
              randomeat(creatorid, team2, info.lobby.game[creatorid][team][mob][number], 0)
           if info.lobby.game[creatorid][team][mob][number]['target']==None:
               t=mobdmg(mob, creatorid, team, team2, number)
               if t!=None and t!='None':
                   mobturn(creatorid, team, mob, number, t) 
          else:
            end(creatorid, team, mob, number, 0, 0)
        info.lobby.game[creatorid][team][mob][number]['ready']=1 
        
    elif mob=='zombie':
        if info.lobby.game[creatorid][team][mob][number]['smert']!=1:
          if info.lobby.game[creatorid][team][mob][number]['stun']<1:
             x=random.randint(1,100)
             if x<=35:    
                randomlife(creatorid, team2, info.lobby.game[creatorid][team][mob][number], 0, info.lobby.game[creatorid][team])
             if info.lobby.game[creatorid][team][mob][number]['target']==None:
               t=mobdmg(mob, creatorid, team, team2, number)
               if t!=None and t!='None':
                   mobturn(creatorid, team, mob, number, t) 
          else:
            end(creatorid, team, mob, number, 0, 0)
        info.lobby.game[creatorid][team][mob][number]['ready']=1 
    
                    
                    
     

def randomlife(creatorid, team2, mob, x, team):
             typemob1=classtoemoji(mob['type'])
             emoj1=emojize(typemob1, use_aliases=True)
             emojskill=emojize(':eight_spoked_asterisk:', use_aliases=True)
             emojlife=emojize(':black_heart:', use_aliases=True)
             if len(team)>0:
                    d=list(team.keys())
                    c=random.choice(d)
                    if len(team[c])>0:
                      g=list(team[c].keys())                    
                      b=random.choice(g)
                      target=team[c][b]
                      if target['smert']==1:
                        target['hp']=125
                        target['smert']=0
                        target['ready']=0
                        typemob2=classtoemoji(target['type'])
                        emoj2= emojize(typemob2, use_aliases=True)                
                        mob['skilltext']=emoj1+mob['name']+emojlife+emojskill+emoj2+target['name']+' "Qayta tirilish"'
                        info.lobby.game[creatorid]['lifecast']+=1
                      else:
                        if x<100:
                          x+=1
                          randomlife(creatorid, team2, mob, x, team)
                        else:
                          pass
                    else:
                      if x<100:
                        x+=1
                        randomlife(creatorid, team2, mob, x, team)
                      else:
                          pass
        
        
        
def randomstun(creatorid, team2, mob, x):
             typemob1=classtoemoji(mob['type'])
             emoj1=emojize(typemob1, use_aliases=True)
             emojskill=emojize(':eight_spoked_asterisk:', use_aliases=True)
             if len(info.lobby.game[creatorid][team2])>0:
                    print('>0')
                    d=list(info.lobby.game[creatorid][team2].keys())
                    c=random.choice(d)
                    if len(info.lobby.game[creatorid][team2][c])>0:
                      print('>0 duble2')
                      g=list(info.lobby.game[creatorid][team2][c].keys())                    
                      b=random.choice(g)
                      target=info.lobby.game[creatorid][team2][c][b]
                      if target['smert']!=1:
                        target['stun']=1
                        if target['ready']==1:
                            target['stun']=2
                        typemob2=classtoemoji(target['type'])
                        emoj2= emojize(typemob2, use_aliases=True)                
                        mob['skilltext']=emoj1+mob['name']+emojskill+emoj2+target['name']+' "Karaxtlovchi Nara"'
                        print('Karaxtlash')
                      else:
                        randomstun(creatorid, team2, mob, x)
                    else:
                        if x<100:
                          x+=1
                          randomstun(creatorid, team2, mob, x)
                        else:
                            pass
                        
                        
def randomeat(creatorid, team2, mob, x):
             typemob1=classtoemoji(mob['type'])
             emoj1=emojize(typemob1, use_aliases=True)
             emojskill=emojize(':eight_spoked_asterisk:', use_aliases=True)
             emojeat=emojize(':japanese_ogre:', use_aliases=True)
             if len(info.lobby.game[creatorid][team2])>0:
                    d=list(info.lobby.game[creatorid][team2].keys())
                    c=random.choice(d)
                    if len(info.lobby.game[creatorid][team2][c])>0:
                      g=list(info.lobby.game[creatorid][team2][c].keys())                    
                      b=random.choice(g)
                      target=info.lobby.game[creatorid][team2][c][b]
                      if target['smert']!=1:
                        if mob['hp']>0:
                          mob['hp']+=target['hp']*0.5
                        mob['hp']=round(mob['hp'], 2)
                        mob['damage']+=target['damage']
                        target['hp']=0
                        typemob2=classtoemoji(target['type'])
                        emoj2= emojize(typemob2, use_aliases=True)                
                        mob['skilltext']=emoj1+mob['name']+emojeat+emoj2+target['name']+' "Haydash"'
                      else:
                        randomeat(creatorid, team2, mob, x)
                    else:
                        if x<100:
                          x+=1
                          randomeat(creatorid, team2, mob, x)
                        else:
                            pass
   

                
            
                    
def testturn(creatorid, id):
  info.lobby.game[creatorid]['readys']+=1
  info.lobby.game[creatorid]['players'][id]['ready']=1
  if info.lobby.game[creatorid]['readys']!=len(info.lobby.game[creatorid]['players']):
    msg=medit('Boshqa oyinchilarni kutamiz...', id, info.lobby.game[creatorid]['players'][id]['lastmessage'])
    info.lobby.game[creatorid]['players'][id]['currentmessage']=msg.message_id
  else:
    msg=medit('Boshcha oyinchilarni kutamiz...', id, info.lobby.game[creatorid]['players'][id]['lastmessage'])
    info.lobby.game[creatorid]['players'][id]['currentmessage']=msg.message_id
    
    endturn(creatorid)
    
              
    
 
            
    


def endturn(creatorid):
 for ids in info.lobby.game[creatorid]['players']:
  if info.lobby.game[creatorid]['players'][ids]['ready']!=1:
    msg=medit('Vaqt tugadi!', ids, info.lobby.game[creatorid]['players'][ids]['lastmessage'])
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
            if e>3:
              info.lobby.game[creatorid]['t1hod']=1
   elif info.lobby.game[creatorid]['t1hod']==1:
            j+=1
            print('2')
            if j>3:
               info.lobby.game[creatorid]['t1hod']=0 
   for mob1 in info.lobby.game[creatorid]['t1mobs']:
        for number111 in info.lobby.game[creatorid]['t1mobs'][mob1]:
           if info.lobby.game[creatorid]['t1hod']==1:
            if info.lobby.game[creatorid]['t1mobs'][mob1][number111]['ready']!=1:
             skills(mob1, creatorid, 't1mobs', 't2mobs', number111)
             if info.lobby.game[creatorid]['lifecast']>0:
                allmobs+=info.lobby.game[creatorid]['lifecast']
                info.lobby.game['lifecast']=0
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
 emojshield=emojize(':shield:', use_aliases=True)
 emojshturm=emojize(':crossed_swords:', use_aliases=True)
 if info.lobby.game[creatorid]['manaplust2']>0:
   mana1='Olingan mana: '+droplet+str(info.lobby.game[creatorid]['manaplust2']/len(info.lobby.game[creatorid]['team2']))+"\n"+"\n"
 else:
   mana1=''
 if info.lobby.game[creatorid]['manaplust1']>0:
    mana2='Olingan mana: '+droplet+str(info.lobby.game[creatorid]['manaplust1']/len(info.lobby.game[creatorid]['team1']))+"\n"+"\n"
 else:
    mana2=''
 if info.lobby.game[creatorid]['skills1']!='':
   skills1="\n"+'Ishlatilgan kuchlar:'+"\n"+info.lobby.game[creatorid]['skills1']+"\n"+"\n"
 else:
   skills1=''
 if info.lobby.game[creatorid]['skills2']!='':
   skills2="\n"+'Ishlatilgan kuchlar:'+"\n"+info.lobby.game[creatorid]['skills2']+"\n"+"\n"
 else:
   skills2=''
 if len(info.lobby.game[creatorid]['team2'])>0 and len(info.lobby.game[creatorid]['team1'])>0:
   bot.send_message(info.lobby.game[creatorid]['chatid'],"*🗓Yurish *"+str(info.lobby.game[creatorid]['hod'])+':'+"\n\n"+te+'`"Xujum"'+emojshturm+' guruhi: '+info.lobby.game[creatorid]['teammates1']+"\n"+te+'"Himoya"'+emojshield+' guruhi: '+info.lobby.game[creatorid]['teammates2']+"`\n"+"\n_"+emojshturm*7+':'+info.lobby.game[creatorid]['resultst1']+skills1+mana1+emojshield*7+':'+info.lobby.game[creatorid]['resultst2']+skills2+mana2+'_*🌆Tirik qolgan mavjudotlar-* `'+info.lobby.game[creatorid]['teammates1']+"`*: "+str(livemobs1)+"ta!\n"+'🏙Tirik qolgan mavjudotlar:* `'+info.lobby.game[creatorid]['teammates2']+"`*: "+str(livemobs2)+"ta!*\n", parse_mode='markdown')
   print('🗓Yurish '+str(info.lobby.game[creatorid]['hod'])+':'+"\n"+te+'Guruh "Xujum": '+info.lobby.game[creatorid]['teammates1']+"\n"+te+'Guruh "Himoya": '+info.lobby.game[creatorid]['teammates2']+"\n"+"\n"+info.lobby.game[creatorid]['resultst1']+"\n"+'Ishlatilgan kuchlar:'+"\n"+info.lobby.game[creatorid]['skills1']+"\n"+'"Xujum" guruhining tirik qolgan mavjudotlari soni: '+str(livemobs1)+"\n"+'Guruhni har bir azosi '+droplet+str(info.lobby.game[creatorid]['manaplust2']/len(info.lobby.game[creatorid]['team2']))+' o`zlari o`ldirgan maxluqlar uchun mana oldi!'+"\n"+"\n"+info.lobby.game[creatorid]['resultst2']+"\n"+'🔮Ishlatilgan kuchlar'+"\n"+info.lobby.game[creatorid]['skills2']+"\n"+'"Himoya" guruhida tirik qolgan o`yinchilar: '+str(livemobs2)+"\n"+'Guruhning har bir azosi '+droplet+str(info.lobby.game[creatorid]['manaplust1']/len(info.lobby.game[creatorid]['team1']))+' o`zi o`ldirgan maxluqlar uchun mana oldi!')
 else:
   if len(info.lobby.game[creatorid]['team2'])<1:
      info.lobby.game[creatorid]['throne2hp']-=2000
   elif len(info.lobby.game[creatorid]['team1'])<1:
      info.lobby.game[creatorid]['throne1hp']-=2000
 info.lobby.game[creatorid]['resultst1']=''+"\n"
 info.lobby.game[creatorid]['resultst2']=''+"\n"
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
                  'pyos':{'count':0},
                  'tiranozavr':{'count':0},
                  's4upakabra':{'count':0},
                  'golem':{'count':0},
                  'vsadnik':{'count':0},
                  'soulcatcher':{'count':0},
                  'zombie':{'count':0}
                               }                 
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
      info.lobby.game[creatorid]['t1mobs'][mob10][number10]['shield']=0
        
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
      info.lobby.game[creatorid]['t2mobs'][mob11][number11]['shield']=0
 info.lobby.game[creatorid]['hod']+=1
 info.lobby.game[creatorid]['skills1']=''
 info.lobby.game[creatorid]['skills2']=''
 livemob1=0
 livemob2=0
 mobdmageall=0
 for mobtothrone1 in info.lobby.game[creatorid]['t1mobs']:
    for numberthrone1 in info.lobby.game[creatorid]['t1mobs'][mobtothrone1]:
      if info.lobby.game[creatorid]['t1mobs'][mobtothrone1][numberthrone1]['smert']!=1:
       if info.lobby.game[creatorid]['t1mobs'][mobtothrone1][numberthrone1]['stun']<1:
        livemob1+=1
 for mobtothrone2 in info.lobby.game[creatorid]['t2mobs']:
    for numberthrone2 in info.lobby.game[creatorid]['t2mobs'][mobtothrone2]:
      if info.lobby.game[creatorid]['t2mobs'][mobtothrone2][numberthrone2]['smert']!=1:
       if info.lobby.game[creatorid]['t2mobs'][mobtothrone2][numberthrone2]['stun']<1:
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
      emojheart=emojize(':heart:', use_aliases=True)
      if info.lobby.game[creatorid]['t2mobs'][mbs][nmbs]['smert']!=1:
       if info.lobby.game[creatorid]['t2mobs'][mbs][nmbs]['stun']<1:
         mobdmageall+=info.lobby.game[creatorid]['t2mobs'][mbs][nmbs]['damage']
         mobdmage=info.lobby.game[creatorid]['t2mobs'][mbs][nmbs]['damage']
         info.lobby.game[creatorid]['thronedamagemobs']+=emoj1+info.lobby.game[creatorid]['t2mobs'][mbs][nmbs]['name']+emojattack+' Saroyga🏯 xujum qildi❕'+"\n"
         info.lobby.game[creatorid]['t2mobs'][mbs][nmbs]['hp']-=7
         if info.lobby.game[creatorid]['t2mobs'][mbs][nmbs]['hp']<=0:
            info.lobby.game[creatorid]['t2mobs'][mbs][nmbs]['smert']=1
   info.lobby.game[creatorid]['throne1hp']-=1
   info.lobby.game[creatorid]['thronedamage']=info.lobby.game[creatorid]['thronedamagemobs']+"\n"+'🛡Himoya🏰 guruhi maxluqlari dushman saroyiga xujum qilishdi ! Endi unda '+emojheart+str(info.lobby.game[creatorid]['throne1hp'])+' jon qoldi! Hujum qilgan barcha maxluqlar 7 zarba⛓ oldi.'    
 elif livemob2==0 and livemob1>0:
    for mbs2 in info.lobby.game[creatorid]['t1mobs']:
     for nmbs2 in info.lobby.game[creatorid]['t1mobs'][mbs2]:
      typemob1=classtoemoji(info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['type'])
      throne=emojize(':european_castle:', use_aliases=True)
      emoj1=emojize(typemob1, use_aliases=True)
      emojattack=emojize(':arrow_right:', use_aliases=True)
      emojdmg=emojize(':broken_heart:', use_aliases=True)
      emojhp=emojize(':green_heart:', use_aliases=True)
      emojheart=emojize(':heart:', use_aliases=True)
      if info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['smert']!=1:
       if info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['stun']<1:
         mobdmageall+=info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['damage']
         mobdmage=info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['damage']
         info.lobby.game[creatorid]['thronedamagemobs']+=emoj1+info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['name']+emojattack+' Saroyga🏰 xujum qildi❕'+"\n"
         info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['hp']-=7
         if info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['hp']<=0:
            info.lobby.game[creatorid]['t1mobs'][mbs2][nmbs2]['smert']=1
    info.lobby.game[creatorid]['throne2hp']-=1
    info.lobby.game[creatorid]['thronedamage']=info.lobby.game[creatorid]['thronedamagemobs']+"\n"+'⚔️Xujum🏯 guruhi maxluqlari dushman saroyiga xujum qilishdi ! Endi unda '+emojheart+str(info.lobby.game[creatorid]['throne2hp'])+' jon qoldi! Hujum qilgan barcha maxluqlar 7 zarba⛓ oldi.'
 elif livemob2==0 and livemob1==0:
    info.lobby.game[creatorid]['thronedamage']='Saroylarga xujum bo`lmadi!'
 elif livemob2>0 and livemob1>0:
    info.lobby.game[creatorid]['thronedamage']='Saroylarga xujum bo`lmadi!'
 bot.send_message(info.lobby.game[creatorid]['chatid'], info.lobby.game[creatorid]['thronedamage'])
 info.lobby.game[creatorid]['thronedamage']=''
 info.lobby.game[creatorid]['thronedamagemobs']=''
 if info.lobby.game[creatorid]['throne2hp']<1 or info.lobby.game[creatorid]['throne1hp']<1:
   if info.lobby.game[creatorid]['throne2hp']<info.lobby.game[creatorid]['throne1hp']:
    bot.send_document(info.lobby.game[creatorid]['chatid'],test.masterid,caption='"Xujum" guruhi g`alaba qozondi!')    
    print('"Xujum" guruhi g`alabasi!')
    del info.lobby.game[creatorid]
   elif info.lobby.game[creatorid]['throne2hp']>info.lobby.game[creatorid]['throne1hp']:
    bot.send_document(info.lobby.game[creatorid]['chatid'],test.dogid,caption='"Himoya" guruhi g`alaba qozondi!')    
    print('"Himoya" guruhi g`alabasi!')
    timer=threading.Timer(4.0, delete, args=[creatorid])
    timer.start()
 else:
   battle(info.lobby.game[creatorid]['creatorid']['selfid'])
                                                                              
                                                                              
    
    
    
            
def delete(id):
    del info.lobby.game[id]
            
            


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
    elif name=='s4upakabra':
        x=info.s4upakabra
    elif name=='golem':
        x=info.golem
    elif name=='vsadnik':
        x=info.vsadnik
    elif name=='soulcatcher':
        x=info.soulcatcher
    elif name=='zombie':
        x=info.zombie
         
    return x



def mobs(callid, creatorid):    #выбирает 3х рандомных мобов для возможности спавна
            while len(info.lobby.game[creatorid]['players'][callid]['mobsinturn'])<3:
              x=random.randint(1,len(info.lobby.game[creatorid]['players'][callid]['allmobs']))
              if info.lobby.game[creatorid]['players'][callid]['allmobs'][x-1] not in info.lobby.game[creatorid]['players'][callid]['mobsinturn']:
               if info.lobby.game[creatorid]['players'][callid]['allmobs'][x-1] not in ban:
                info.lobby.game[creatorid]['players'][callid]['mobsinturn'].append(info.lobby.game[creatorid]['players'][callid]['allmobs'][x-1])
                if len(info.lobby.game[creatorid]['players'][callid]['mobsinturn'])==1:
                  y=nametoclass(info.lobby.game[creatorid]['players'][callid]['allmobs'][x-1])
                  info.lobby.game[creatorid]['players'][callid]['name1mob']=y.name
                elif len(info.lobby.game[creatorid]['players'][callid]['mobsinturn'])==2:
                  y=nametoclass(info.lobby.game[creatorid]['players'][callid]['allmobs'][x-1])
                  info.lobby.game[creatorid]['players'][callid]['name2mob']=y.name
                elif len(info.lobby.game[creatorid]['players'][callid]['mobsinturn'])==3:
                  y=nametoclass(info.lobby.game[creatorid]['players'][callid]['allmobs'][x-1])
                  info.lobby.game[creatorid]['players'][callid]['name3mob']=y.name
                        


def endt(callid):
   for id in info.lobby.game:
    if callid in info.lobby.game[id]['players']:
     if info.lobby.game[id]['players'][callid]['currentmessage']==info.lobby.game[id]['players'][callid]['lastmessage']:
      if info.lobby.game[id]['players'][callid]['ready']!=1:
        if callid in info.lobby.game[id]['players']:  
          testturn(info.lobby.game[id]['creatorid']['selfid'], callid)
                        
def buffcast(target, id, chatid, namemob, team):
    you=emojize(':smiling_imp:', use_aliases=True)
    cast=emojize(':eight_spoked_asterisk:', use_aliases=True)
    text=''
    shield=random.randint(1, 100)
    if shield<=30:
      target['shield']=1
      text+='Qalqon (Ehtimol 30% edi)'+"\n"
    
    hp=random.randint(1,100)
    if hp<=35:
      target['hp']+=4
      text+='+4 xp Jon (Ehtimol 35% edi)'+"\n"
    
    damage=random.randint(1,100)
    if damage<=60:
      target['damage']+=3
      text+='+3 zarb kuchi (Ehtimol 60% edi)'+"\n"
    
    die=random.randint(1,100)
    if die<=5:
        target['smert']=1
        target['hp']=0
        text='O`lim (Ehtimol 5% edi)'+"\n"
    if text=='':
        text='Omad kelmadi! Mavjudotga kuchayish bera olmadingiz'+"\n"
    if team==info.lobby.game[chatid]['t1mobs']:
      info.lobby.game[chatid]['skills1']+=you+' Sexr '+cast+'"Kuchayish" ('+namemob+'):'+"\n"+text
    elif team==info.lobby.game[chatid]['t2mobs']:
        info.lobby.game[chatid]['skills2']+=you+' Sexr '+cast+'"Kuchayish" ('+namemob+'):'+"\n"+text
    return text
        
    
    
    
      
            
            
def buffchoice(aidi, team, chatid, mana):
     d=list(team.keys())
     c=random.choice(d)
     alive=0
     for lists in team:
        for mobs in team[lists]:
         if team[lists][mobs]['smert']==0:
             alive+=1
     if alive>0:
       g=list(team[c].keys())    
       if len(g)>0:
         b=random.choice(g)
         target=team[c][b]
         if target['smert']!=1:
           if mana['mana']>=50:
             mana['mana']-=50
             text=buffcast(target, aidi, chatid, target['name'], team)
             bot.send_message(aidi, 'Siz mavjudotga kuchayishni omadli berdingiz ('+target['name']+')! U oldi:'+"\n"+text)
           else:
            bot.send_message(aidi, 'Mana yetarli emas!')
         else:
          buffchoice(aidi, team, chatid, mana)
       else:
          buffchoice(aidi, team, chatid, mana)
     else:
         bot.send_message(aidi, 'Sizda bitta ham tirik mavjudot yo`q!')

def mobtoinfo(mob):
    if mob=='s_me4nik':
        inform='me4nikinfo'
    elif mob=='pyos':
        inform='pyosinfo'
    elif mob=='phoenix':
        inform='phoenixinfo'
    elif mob=='electromagnit':
        inform='magnitinfo'
    elif mob=='manoed':
        inform='manoedinfo'
    elif mob=='tiranozavr':
        inform='tiranozavrinfo'
    elif mob=='s4upakabra':
        inform='s4upakabrainfo'
    elif mob=='golem':
        inform='goleminfo'
    elif mob=='vsadnik':
        inform='vsadnikinfo'
    elif mob=='soulcatcher':
        inform='soulinfo'
    elif mob=='zombie':
        inform='zombieinfo'
    return inform
        
                      
            
@bot.callback_query_handler(func=lambda call:True)
def inline(call):
  emojarrow=emojize(':arrow_right:', use_aliases=True)
  emojskill=emojize(':eight_spoked_asterisk:', use_aliases=True)
  emojelectro=emojize(':zap:', use_aliases=True)
  emojbio=emojize(':evergreen_tree:', use_aliases=True)
  emojfire=emojize(':fire:', use_aliases=True)
  emojghost=emojize(':ghost:', use_aliases=True)
  emojundead=emojize(':skull:', use_aliases=True)
  emojattack=emojize(':crossed_swords:', use_aliases=True)
  emojhp=emojize(':heart:', use_aliases=True)
  emojmana=emojize(':droplet:', use_aliases=True) 
  emojmanamob=emojize(':diamond_shape_with_a_dot_inside:', use_aliases=True)
  if call.data=='do':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
         if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
          portal=emojize(':crystal_ball:', use_aliases=True)
          back=emojize(':back:', use_aliases=True) 
          cast=emojize(':man_with_turban:', use_aliases=True)
          Keyboard=types.InlineKeyboardMarkup()
          Keyboard.add(types.InlineKeyboardButton(text=portal+"Portalni ochish", callback_data='altar'))
          Keyboard.add(types.InlineKeyboardButton(text=cast+"Sexrlash", callback_data='skills'))
          Keyboard.add(types.InlineKeyboardButton(text=back+"Bosh menyu", callback_data='menu'))
          msg=medit('Harakatni tanlang', call.from_user.id, info.lobby.game[id]['players'][call.from_user.id]['lastmessage'], reply_markup=Keyboard)
          info.lobby.game[id]['players'][call.from_user.id]['currentmessage']=msg.message_id
          info.lobby.game[id]['players'][call.from_user.id]['lastmessage']=msg.message_id
            
            
            
  elif call.data=='skills':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
          if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
            infos=emojize(':question:', use_aliases=True)
            back=emojize(':back:', use_aliases=True) 
            droplet=emojize(':droplet:', use_aliases=True)
            Keyboard=types.InlineKeyboardMarkup()
            Keyboard.add(types.InlineKeyboardButton(text="Kuchayish "+droplet+'50', callback_data='buff'), types.InlineKeyboardButton(text=infos+"Info", callback_data='infobuff')) 
            Keyboard.add(types.InlineKeyboardButton(text=back+"Bosh menyu", callback_data='menu'))
            msg=medit('Kuchni tanlang:', call.from_user.id, info.lobby.game[id]['players'][call.from_user.id]['lastmessage'], reply_markup=Keyboard)
            
    
  elif call.data=='infobuff':
    bot.send_message(call.from_user.id, 'Bu qobiliyatni sizning taqribiy mavjudotlaringizdan biri oladi va quyidagi xususiyatlarga ega:'+"\n"+
                     '1. Mavjudot yurish yakunigacha o`lmaslik xususiyatini oladi ("Qora Ajal" ning "Haydash" kuchi ta`sir etganda ishlamaydi) (ehtimol 30%);'+"\n"+
                     '2. Mavjudot kuchi 65 ga ortadi; (ehtimol 60%);'+"\n"+
                     '3. Mavjudot +70 xp Jon oladi (ehtimol 35%);'+"\n"+
                     '4. Mavjudot o`ladi (ehtimol 5%);'+"\n"+
                     'Bu kuchlar bir biriga bog`liq bo`lmagan holda tushadi, lekin bular hech biri ishlamasligi ham mumkin. Omadingizga qarab tavakkal qilishingiz mumkin!'
                    )
    
  
  elif call.data=='buff':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
          if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
                if call.from_user.id in info.lobby.game[id]['team1']:
                    buffchoice(call.from_user.id, info.lobby.game[id]['t1mobs'], id, info.lobby.game[id]['players'][call.from_user.id])
                elif call.from_user.id in info.lobby.game[id]['team2']:
                    buffchoice(call.from_user.id, info.lobby.game[id]['t2mobs'], id, info.lobby.game[id]['players'][call.from_user.id])
          
          
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
            Keyboard.add(types.InlineKeyboardButton(text=go+"Harakatlar", callback_data='do'))
            Keyboard.add(types.InlineKeyboardButton(text=infos+"Men haqimda ma`lumot", callback_data='info'))  
            Keyboard.add(types.InlineKeyboardButton(text=end+"Yurishni yakunlash", callback_data='end'))
            msg=medit('Bosh Menyu:'+"\n"+mana+'Mana: '+str(info.lobby.game[id]['players'][call.from_user.id]['mana'])+'/'+str(info.lobby.game[id]['players'][call.from_user.id]['manamax']), call.from_user.id, info.lobby.game[id]['players'][call.from_user.id]['lastmessage'], reply_markup=Keyboard)
            info.lobby.game[id]['players'][call.from_user.id]['lastmessage']=msg.message_id 
            info.lobby.game[id]['players'][call.from_user.id]['currentmessage']=msg.message_id
            
  elif call.data=='end':
   t=threading.Timer(0.1, endt, args=[call.from_user.id])
   t.start()

        
        
  elif call.data=='info':
    hp=emojize(':heart:', use_aliases=True)
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if call.from_user.id in info.lobby.game[id]['team1']:
          bot.send_message(call.from_user.id, 'Sizning guruhingiz: '+info.lobby.game[id]['teammates1']+"\n"+'Sizning Saroyingiz Joni: '+hp+str(info.lobby.game[id]['throne1hp'])+"\n"+'Dushman Saroyi Joni: '+hp+str(info.lobby.game[id]['throne2hp']))
        elif call.from_user.id in info.lobby.game[id]['team2']:  
          bot.send_message(call.from_user.id, 'Sizning guruhingiz: '+info.lobby.game[id]['teammates2']+"\n"+'Sizning Saroyingiz Joni: '+hp+str(info.lobby.game[id]['throne2hp'])+"\n"+'Dushman Saroyi Joni: '+hp+str(info.lobby.game[id]['throne1hp']))


           
          
          
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
            emojdmg=emojize(':crossed_swords:', use_aliases=True)
            emojhp=emojize(':green_heart:', use_aliases=True)
            back=emojize(':back:', use_aliases=True) 
            Keyboard=types.InlineKeyboardMarkup()
            Keyboard.add(types.InlineKeyboardButton(text=emoj0+info.lobby.game[id]['players'][call.from_user.id]['name1mob'], callback_data=info.lobby.game[id]['players'][call.from_user.id]['mobsinturn'][0]),types.InlineKeyboardButton(text='Narx: '+manacost+str(nc0.cost), callback_data='no'),types.InlineKeyboardButton(text='Info', callback_data=mobtoinfo(info.lobby.game[id]['players'][call.from_user.id]['mobsinturn'][0])))
            Keyboard.add(types.InlineKeyboardButton(text=emoj1+info.lobby.game[id]['players'][call.from_user.id]['name2mob'], callback_data=info.lobby.game[id]['players'][call.from_user.id]['mobsinturn'][1]),types.InlineKeyboardButton(text='Narx: '+manacost+str(nc1.cost), callback_data='no'),types.InlineKeyboardButton(text='Info', callback_data=mobtoinfo(info.lobby.game[id]['players'][call.from_user.id]['mobsinturn'][1])))
            Keyboard.add(types.InlineKeyboardButton(text=emoj2+info.lobby.game[id]['players'][call.from_user.id]['name3mob'], callback_data=info.lobby.game[id]['players'][call.from_user.id]['mobsinturn'][2]),types.InlineKeyboardButton(text='Narx: '+manacost+str(nc2.cost), callback_data='no'),types.InlineKeyboardButton(text='Info', callback_data=mobtoinfo(info.lobby.game[id]['players'][call.from_user.id]['mobsinturn'][2])))
            Keyboard.add(types.InlineKeyboardButton(text=back+"Bosh Menyu", callback_data='menu'))
            msg=medit('Chaqirish imkoniyati bor mavjudotlar:', call.from_user.id, info.lobby.game[id]['players'][call.from_user.id]['lastmessage'], reply_markup=Keyboard)
            info.lobby.game[id]['players'][call.from_user.id]['lastmessage']=msg.message_id 
            info.lobby.game[id]['players'][call.from_user.id]['currentmessage']=msg.message_id
            
            
  elif call.data=='me4nikinfo':
    bot.send_message(call.from_user.id, 
        'Nomi: *Skilet-qilichboz*'+"\n"+
        'Tip: '+emojundead+'O`liklar'+"\n"+
        emojattack+'Zarb: 55'+"\n"+
        emojhp+'Jon: 65'+"\n"+
        emojmana+'Narx: 30'+"\n"+
        emojmanamob+'Mana (shaxsiy): 30'+"\n"+
        emojskill+'Kuch: "O`liklar lanati" (ehtimol: 40%): nishonga hujum qilayotgan barcha maxluqlar 60% ga kuchi ortadi (hujumdan oldin ishlatiladi)'+"\n"+
                    'Maxluqlar bir biridan ustunligi:'+"\n"+
                    emojelectro+emojarrow+emojghost+emojarrow+emojfire+emojarrow+emojbio+emojarrow+emojundead+emojarrow+emojelectro, parse_mode='markdown'
                    )
    
    
  elif call.data=='pyosinfo':
    bot.send_message(call.from_user.id,
        'Nomi: *Pyos*'+"\n"+
        'Tip: '+emojbio+'Bio'+"\n"+
        emojattack+'Zarb: 50'+"\n"+
        emojhp+'Jon: 300'+"\n"+
        emojmana+'Narx: 75'+"\n"+
        emojmanamob+'Mana (shaxsiy): 30'+"\n"+
        emojskill+'Kuch: "Bot programmasini buzish" (ehtimol 35%): hujum qilayotgan mavjudot o`zidan o`zi zarb oladi (qabul qilayotgan barcha zarb bloklanadi)'+"\n"+
                     'Maxluqlar bir biridan ustunligi:'+"\n"+
                    emojelectro+emojarrow+emojghost+emojarrow+emojfire+emojarrow+emojbio+emojarrow+emojundead+emojarrow+emojelectro, parse_mode='markdown') 
    
  elif call.data=='phoenixinfo':
    bot.send_message(call.from_user.id, 
        'Nomi: *Feniks*'+"\n"+
        'Тип: '+emojfire+'Olovli'+"\n"+
        emojattack+'Zarb: 200'+"\n"+
        emojhp+'Jon: 25'+"\n"+
        emojmana+'Narx: 60'+"\n"+
        emojmanamob+'Mana (shaxsiy): 30'+"\n"+
        emojskill+'Kuch: Yoq'+"\n"+
                     'Maxluqlar bir biridan ustunligi:'+"\n"+
                    emojelectro+emojarrow+emojghost+emojarrow+emojfire+emojarrow+emojbio+emojarrow+emojundead+emojarrow+emojelectro, parse_mode='markdown') 
    
  elif call.data=='magnitinfo':
    bot.send_message(call.from_user.id,
        'Nomi: *Elektromagniten*'+"\n"+
        'Tip: '+emojelectro+'Elektro'+"\n"+
        emojattack+'Zarb: 70'+"\n"+
        emojhp+'Jon: 180'+"\n"+
        emojmana+'Narx: 60'+"\n"+
        emojmanamob+'Mana (shaxsiy): 80'+"\n"+
        emojskill+'Kuch: "Quvvat" (ehtimol 30%): dushmanni tok uradi va uning 45 zarb kuchini tortib oladi (zarb minusga ham ketishi mumkin!)'+"\n"+
                     'Maxluqlar bir biridan ustunligi:'+"\n"+
                    emojelectro+emojarrow+emojghost+emojarrow+emojfire+emojarrow+emojbio+emojarrow+emojundead+emojarrow+emojelectro, parse_mode='markdown') 
         
        
        
  elif call.data=='manoedinfo':
    bot.send_message(call.from_user.id,
        'Nomi: *Monoed*'+"\n"+
        'Tip: '+emojghost+'Ruxlar'+"\n"+
        emojattack+'Zarb: 45'+"\n"+
        emojhp+'Jon: 135'+"\n"+
        emojmana+'Narx: 45'+"\n"+
        emojmanamob+'Mana (shaxsiy): 30'+"\n"+
        emojskill+'Kuch: "Ichiga kirish" (ehtimol 60%): nishondan 70 qism mana olib qo`yadi (0 dan kam bo`lmagan mana qoladi), tortib olgan manasi miqdorida zarb yetkazadi.'+"\n"+
                     'Maxluqlar bir biridan ustunligi:'+"\n"+
                    emojelectro+emojarrow+emojghost+emojarrow+emojfire+emojarrow+emojbio+emojarrow+emojundead+emojarrow+emojelectro, parse_mode='markdown') 
    
    
    
  elif call.data=='tiranozavrinfo':
    bot.send_message(call.from_user.id,
        'Nomi: *Tiranozarv*'+"\n"+
        'Tip: '+emojbio+'Bio'+"\n"+
        emojattack+'Zarb: 120'+"\n"+
        emojhp+'Jon: 260'+"\n"+
        emojmana+'Narx: 90'+"\n"+
        emojmanamob+'Mana (shaxsiy): 30'+"\n"+
        emojskill+'Kuch: "Karaxtlovchi Nara" (ehtimol 40%): baqiradi va taqribiy dushmanlardan birini karaxtlaydi (agarda avval karaxt bo`lgan sexr keyingi yurishga o`tadi)'+"\n"+
                     'Maxluqlar bir biridan ustunligi:'+"\n"+
                    emojelectro+emojarrow+emojghost+emojarrow+emojfire+emojarrow+emojbio+emojarrow+emojundead+emojarrow+emojelectro, parse_mode='markdown') 
    
    
    
  elif call.data=='s4upakabrainfo':
    bot.send_message(call.from_user.id,
        'Nomi: *Chupakabra*'+"\n"+
        'Tip: '+emojundead+'O`liklar'+"\n"+
        emojattack+'Zarb: 90'+"\n"+
        emojhp+'Jon: 75'+"\n"+
        emojmana+'Narx: 50'+"\n"+
        emojmanamob+'Mana (shaxsiy): 55'+"\n"+
        emojskill+'Kuch: "Qonxo`rlik" (ehtimol: 100%): hujum vaqtida yetkazgan zarbini 50% ga o`z jonini to`ldirib oladi (kuchni ishlatish vaqtida joni 0xp dan ko`p bo`lishi lozim)'+"\n"+
                     'Maxluqlar bir biridan ustunligi:'+"\n"+
                    emojelectro+emojarrow+emojghost+emojarrow+emojfire+emojarrow+emojbio+emojarrow+emojundead+emojarrow+emojelectro, parse_mode='markdown')   
  
    
    
  elif call.data=='goleminfo':
    bot.send_message(call.from_user.id, 
        'Nomi: *Olovli golem*'+"\n"+
        'Tip: '+emojfire+'Olovlilar'+"\n"+
        emojattack+'Zarb: 100'+"\n"+
        emojhp+'Jon: 600'+"\n"+
        emojmana+'Narx: 165'+"\n"+
        emojmanamob+'Mana (xususiy): 100'+"\n"+
        emojskill+'Kuch: Yoq'+"\n"+
                     'Maxluqlar bir biridan ustunligi:'+"\n"+
                    emojelectro+emojarrow+emojghost+emojarrow+emojfire+emojarrow+emojbio+emojarrow+emojundead+emojarrow+emojelectro, parse_mode='markdown') 
      
    
    
  elif call.data=='vsadnikinfo':
      bot.send_message(call.from_user.id, 
        'Nomi: *Boshsiz Chavandoz*'+"\n"+
        'Tip: '+emojghost+'Ruxlar'+"\n"+
        emojattack+'Zarb: 70'+"\n"+
        emojhp+'Joni: 200'+"\n"+
        emojmana+'Narx: 70'+"\n"+
        emojmanamob+'Mana (shaxsiy): 50'+"\n"+
        emojskill+'Kuchi: "Ruxsimon qilich" (ehtimol: 100%): bitta nishonga xujum qilib HAMMA dushmanlarga zarb yetkazadi'+"\n"+
                       'Maxluqlar bir biridan ustunligi:'+"\n"+
                    emojelectro+emojarrow+emojghost+emojarrow+emojfire+emojarrow+emojbio+emojarrow+emojundead+emojarrow+emojelectro, parse_mode='markdown') 
    
    
    
  elif call.data=='soulinfo':
      bot.send_message(call.from_user.id, 
        'Nomi: *Qora Ajal*'+"\n"+
        'Tip: '+emojundead+'O`liklar'+"\n"+
        emojattack+'Zarbi: 75'+"\n"+
        emojhp+'Joni: 110'+"\n"+
        emojmana+'Narxi: 70'+"\n"+
        emojmanamob+'Mana (shaxsiy): 50'+"\n"+
        emojskill+'Kuch: "Haydash" (ehtimol: 15%) - Taqribiy dushman maxluqini narigi dunyoga haydab yuboradi (o`ldiradi), uning yuragiga ega bo`lib - o`z jonini 40% ni dushman joni hisobiga to`ldiradi, shuningdek 100% uning zarb kuchini oladi.'+"\n"+
                       'Maxluqlar bir biridan ustunligi:'+"\n"+
                    emojelectro+emojarrow+emojghost+emojarrow+emojfire+emojarrow+emojbio+emojarrow+emojundead+emojarrow+emojelectro, parse_mode='markdown') 
        
        
  elif call.data=='zombieinfo':
     bot.send_message(call.from_user.id, 
        'Nomi: *Zombi*'+"\n"+
        'Tip: '+emojundead+'O`liklar'+"\n"+
        emojattack+'Zarbi: 25'+"\n"+
        emojhp+'Joni: 230'+"\n"+
        emojmana+'Narxi: 65'+"\n"+
        emojmanamob+'Mana (shaxsiy): 50'+"\n"+
        emojskill+'Kuch: "Qayta Tirilish" (ehtimol: 40%) - Jangda o`lgan taqribiy do`st maxluqni o`ldiradi. Tirilganning joni 100 xp ga teng bo`ladi.'+"\n"+
                       'Maxluqlar bir biridan ustunligi:'+"\n"+
                    emojelectro+emojarrow+emojghost+emojarrow+emojfire+emojarrow+emojbio+emojarrow+emojundead+emojarrow+emojelectro, parse_mode='markdown')
    
    
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
            bot.send_message(call.from_user.id, 'Siz portalni omadli ochdingiz (Skilet-qilichboz)!'+"\n"+'Endi sizda '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['s_me4nik']['count'])+' ta shunday portal bor!')
           else:
            bot.send_message(call.from_user.id, 'Mana yetarli emas!')
            
            
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
            bot.send_message(call.from_user.id, 'Siz portalni omadli ochdingiz (Feniks)!'+"\n"+'Endi sizda '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['phoenix']['count'])+' ta shunday portal bor!')
           else:
            bot.send_message(call.from_user.id, 'Mana yetarli emas!')
            
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
            bot.send_message(call.from_user.id, 'Siz portalni omadli ochdingiz (Elektromagniten)!'+"\n"+'Endi sizda '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['electromagnit']['count'])+' ta shunday portal bor!')
           else:
            bot.send_message(call.from_user.id, 'Mana yetarli emas!')
            
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
            bot.send_message(call.from_user.id, 'Siz portalni omadli ochdingiz (Monoed)!'+"\n"+'Endi sizda '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['manoed']['count'])+' ta shunday portal bor!')
           else:
            bot.send_message(call.from_user.id, 'Mana yetarli emas!')
            
            
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
            bot.send_message(call.from_user.id, 'Siz portalni omadli ochdingiz (Pyos)!'+"\n"+'Endi sizda '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['pyos']['count'])+' ta shunday portal bor!')
           else:
            bot.send_message(call.from_user.id, 'Mana yetarli emas!')
            
  elif call.data=='tiranozavr':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
         if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
          if 'tiranozavr' in info.lobby.game[id]['players'][call.from_user.id]['mobsinturn']:
           if info.lobby.game[id]['players'][call.from_user.id]['mana']>=info.tiranozavr.cost:
            info.lobby.game[id]['players'][call.from_user.id]['mana']-=info.tiranozavr.cost
            if info.lobby.game[id]['players'][call.from_user.id]['portals']['tiranozavr']['count']==0:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['tiranozavr']=createportal('tiranozavr', 1)  
            else:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['tiranozavr']=createportal('tiranozavr', info.lobby.game[id]['players'][call.from_user.id]['portals']['tiranozavr']['count']+1)  
            bot.send_message(call.from_user.id, 'Siz portalni omadli ochdingiz (Tiranozavr)!'+"\n"+'Endi sizda '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['tiranozavr']['count'])+' ta shunday portal bor!')
           else:
            bot.send_message(call.from_user.id, 'Mana yetarli emas!')
            
            
            
  elif call.data=='s4upakabra':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
         if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
          if 's4upakabra' in info.lobby.game[id]['players'][call.from_user.id]['mobsinturn']:
           if info.lobby.game[id]['players'][call.from_user.id]['mana']>=info.s4upakabra.cost:
            info.lobby.game[id]['players'][call.from_user.id]['mana']-=info.s4upakabra.cost
            if info.lobby.game[id]['players'][call.from_user.id]['portals']['s4upakabra']['count']==0:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['s4upakabra']=createportal('s4upakabra', 1)  
            else:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['s4upakabra']=createportal('s4upakabra', info.lobby.game[id]['players'][call.from_user.id]['portals']['s4upakabra']['count']+1)  
            bot.send_message(call.from_user.id, 'Siz portalni omadli ochdingiz (Chupakabra)!'+"\n"+'Endi sizda '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['s4upakabra']['count'])+' ta shunday portal bor!')
           else:
            bot.send_message(call.from_user.id, 'Mana yetarli emas!')
          
        
        
  elif call.data=='golem':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
         if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
          if 'golem' in info.lobby.game[id]['players'][call.from_user.id]['mobsinturn']:
           if info.lobby.game[id]['players'][call.from_user.id]['mana']>=info.golem.cost:
            info.lobby.game[id]['players'][call.from_user.id]['mana']-=info.golem.cost
            if info.lobby.game[id]['players'][call.from_user.id]['portals']['golem']['count']==0:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['golem']=createportal('golem', 1)  
            else:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['golem']=createportal('golem', info.lobby.game[id]['players'][call.from_user.id]['portals']['golem']['count']+1)  
            bot.send_message(call.from_user.id, 'Siz portalni omadli ochdingiz (Olovli Golem)!'+"\n"+'Endi sizda '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['golem']['count'])+' ta shunday portal bor!')
           else:
            bot.send_message(call.from_user.id, 'Mana yetarli emas!')
            
            
  elif call.data=='vsadnik':
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
         if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
          if 'vsadnik' in info.lobby.game[id]['players'][call.from_user.id]['mobsinturn']:
           if info.lobby.game[id]['players'][call.from_user.id]['mana']>=info.vsadnik.cost:
            info.lobby.game[id]['players'][call.from_user.id]['mana']-=info.vsadnik.cost
            if info.lobby.game[id]['players'][call.from_user.id]['portals']['vsadnik']['count']==0:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['vsadnik']=createportal('vsadnik', 1)  
            else:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['vsadnik']=createportal('vsadnik', info.lobby.game[id]['players'][call.from_user.id]['portals']['vsadnik']['count']+1)  
            bot.send_message(call.from_user.id, 'Siz portalni omadli ochdingiz (Boshsiz chavondoz)!'+"\n"+'Endi sizda '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['vsadnik']['count'])+' ta shunday portal bor!')
           else:
            bot.send_message(call.from_user.id, 'Mana yetarli emas!')
            
              
  elif call.data=='soulcatcher':     
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
         if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
          if 'soulcatcher' in info.lobby.game[id]['players'][call.from_user.id]['mobsinturn']:
           if info.lobby.game[id]['players'][call.from_user.id]['mana']>=info.soulcatcher.cost:
            info.lobby.game[id]['players'][call.from_user.id]['mana']-=info.soulcatcher.cost
            if info.lobby.game[id]['players'][call.from_user.id]['portals']['soulcatcher']['count']==0:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['soulcatcher']=createportal('soulcatcher', 1)  
            else:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['soulcatcher']=createportal('soulcatcher', info.lobby.game[id]['players'][call.from_user.id]['portals']['soulcatcher']['count']+1)  
            bot.send_message(call.from_user.id, 'Siz portalni omadli ochdingiz (Qora ajal)!'+"\n"+'Endi sizda '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['soulcatcher']['count'])+' ta shunday portal bor!')
           else:
            bot.send_message(call.from_user.id, 'Mana yetarli emas!')
            
            
  elif call.data=='zombie':          
    for id in info.lobby.game:
      if call.from_user.id in info.lobby.game[id]['players']:
        if info.lobby.game[id]['players'][call.from_user.id]['currentmessage']==info.lobby.game[id]['players'][call.from_user.id]['lastmessage']:
         if info.lobby.game[id]['players'][call.from_user.id]['ready']!=1:
          if 'zombie' in info.lobby.game[id]['players'][call.from_user.id]['mobsinturn']:
           if info.lobby.game[id]['players'][call.from_user.id]['mana']>=info.zombie.cost:
            info.lobby.game[id]['players'][call.from_user.id]['mana']-=info.zombie.cost
            if info.lobby.game[id]['players'][call.from_user.id]['portals']['zombie']['count']==0:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['zombie']=createportal('zombie', 1)  
            else:
              info.lobby.game[id]['players'][call.from_user.id]['portals']['zombie']=createportal('zombie', info.lobby.game[id]['players'][call.from_user.id]['portals']['zombie']['count']+1)  
            bot.send_message(call.from_user.id, 'Siz portalni omadli ochdingiz(Zombi)!'+"\n"+'Endi sizda '+str(info.lobby.game[id]['players'][call.from_user.id]['portals']['zombie']['count'])+'ta shunday portal bor!')
           else:
            bot.send_message(call.from_user.id, 'Mana yetarli emas!')
   
                 
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
    bot.send_message(message.from_user.id, emojelectro+'Elektro maxluqlar:'+"\n"+'Tanasini teri o`rab turadi lekin ichki azolari yo`q. Uni o`rnini elektr toki to`ldirib turadi. Bu mavjudotlar o`zining shaxsiy manasi orqali ichidagi elektr toki doimiyligini ta`minlaydi.'+"\n"+
                    'Zarb yetkazishi:'+"\n"+'= '+emojbio+'bio: 100%'+"\n"+'= '+emojfire+'olovlilar: 100%'+"\n"+'= '+emojghost+'ruxlar: 200%'+"\n"+'= '+emojundead+'o`liklar: 100%'+"\n"+"\n"+
                     'Qabul qiluvchi zarbi:'+"\n"+'= '+emojbio+'bio: 100%'+"\n"+'= '+emojfire+'olovlilar: 100%'+"\n"+'= '+emojghost+'ruxlar: 100%'+"\n"+'= '+emojundead+'o`liklar: 200%'+"\n"+"\n"+
                     'Kuchlar:'+"\n"+'"Quvvat" (Elektromagnitenda bor) - dushmanga tok bilan hujum qiladi va 30% ehtimollikda hujum qilayotgan mavjudotning o`zi o`ziga 45 zarb yetkazadi (Zarb minusga ham ketishi mumkin)'
                    )
    
    
@bot.message_handler(commands=['bio'])
def bio(message):
    emojelectro=emojize(':zap:', use_aliases=True)
    emojbio=emojize(':evergreen_tree:', use_aliases=True)
    emojfire=emojize(':fire:', use_aliases=True)
    emojghost=emojize(':ghost:', use_aliases=True)
    emojundead=emojize(':skull:', use_aliases=True)
    bot.send_message(message.from_user.id, emojbio+'Biologik maxluqlar:'+"\n"+'Haqiqiy jon va qondan iborat mavjudotlar bo`lib, odamlar dunyosidagi standart mavjudotlar sifatlariga ega.'+"\n"+
                     'Zarb yetkazishi:'+"\n"+'= '+emojfire+'olovlilar: 100%'+"\n"+'= '+emojghost+'ruxlar: 100%'+"\n"+'= '+emojundead+'o`liklar: 200%'+"\n"+'= '+emojelectro+'elektro: 100%'+"\n"+"\n"+
                     'Qabul qiluvchi zarbi:'+"\n"+'= '+emojfire+'olovlilar: 200%'+"\n"+'= '+emojghost+'ruxlar: 100%'+"\n"+'= '+emojundead+'o`liklar: 100%'+"\n"+'= '+emojelectro+'elektro: 100%'+"\n"+"\n"+
                     'Kuchlari:'+"\n"+'"Bot programmasini buzish" (Pyosda bor) - 35% ehtimollikda dushman o`zidan o`zi zarba yeydi (barcha qabul qilingan zarblar bloklanadi)'+"\n"+
                     '"Karaxtlovchi nara" (Tironozavrda) - 40% ehtimol bilan baqirig`i taqribiy bir o`yinchini karaxt qilib qo`yadi (agar u allaqachon karxt bo`lgan bo`lsa sexr keyingi yurishda ta`sir etadi)'
                    )
    
    
@bot.message_handler(commands=['fire'])
def fire(message):
    emojelectro=emojize(':zap:', use_aliases=True)
    emojbio=emojize(':evergreen_tree:', use_aliases=True)
    emojfire=emojize(':fire:', use_aliases=True)
    emojghost=emojize(':ghost:', use_aliases=True)
    emojundead=emojize(':skull:', use_aliases=True)
    bot.send_message(message.from_user.id, emojfire+'Olovlilar'+"\n"+'Xarorat juda yuqori bo`lgan yer osti dunyosida vujudga kelishgan. Ular sovib qolishmasliklari uchun ular to`g`ridan to`g`ri portal orqali chiqishadi.'+"\n"+
                     'Zarb yetkazishi:'+"\n"+'= '+emojghost+'ruxlar: 100%'+"\n"+'= '+emojundead+'o`liklar: 100%'+"\n"+'= '+emojelectro+'elektro: 100%'+"\n"+'= '+emojbio+'bio: 200%'+"\n"+"\n"+
                     'Qabul qiluvchi zarbi:'+"\n"+'= '+emojghost+'ruxlar: 200%'+"\n"+'= '+emojundead+'o`liklar: 100%'+"\n"+'= '+emojelectro+'elektro: 100%'+"\n"+'= '+emojbio+'bio: 100%'+"\n"+"\n"+
                     'Kuchlari:'+"\n"+'Hozircha hech bir mo`jizaviy kuchga ega emas.'
                    )
    
@bot.message_handler(commands=['ghost'])
def ghost(message):   
    emojelectro=emojize(':zap:', use_aliases=True)
    emojbio=emojize(':evergreen_tree:', use_aliases=True)
    emojfire=emojize(':fire:', use_aliases=True)
    emojghost=emojize(':ghost:', use_aliases=True)
    emojundead=emojize(':skull:', use_aliases=True)
    bot.send_message(message.from_user.id, emojghost+'Ruxlar:'+"\n"+'Narigi dunyodan chaqirilgan yarimjon maxluqotlar bo`lib, jismoniy zarbdan kam zarar oladi. Lekin elektromaxluqlar ularga kuchli zarar yetkaza oladi.'+"\n"+
                     'Zarb yetkazishi:'+"\n"+'= '+emojundead+'o`liklar: 100%'+"\n"+'= '+emojelectro+'elektro: 100%'+"\n"+'= '+emojbio+'bio: 100%'+"\n"+'= '+emojfire+'olovlilar: 200%'+"\n"+"\n"+    
                     'Qabul qiluvchi zarari:'+"\n"+'= '+emojundead+'o`liklar: 100%'+"\n"+'= '+emojelectro+'elektro: 200%'+"\n"+'= '+emojbio+'bio: 100%'+"\n"+'= '+emojfire+'olovlilar: 100%'+"\n"+"\n"+ 
                     'Kuchlari:'+"\n"+'"Tanaga kirish" (Monoedda bor) - 45% ehtimollikda dushmanni qo`shimcha 1xp jonini olib qo`yadi.'+"\n"+
                     '"Ruxsimon qilich" (Boshsiz chavandozda bor) - bitta nishonga hujum qilish orqali HAMMA maxluqlarga zarb yetkazishi mumkin.'
                    )
    
    
@bot.message_handler(commands=['undead'])
def undead(message):
    emojelectro=emojize(':zap:', use_aliases=True)
    emojbio=emojize(':evergreen_tree:', use_aliases=True)
    emojfire=emojize(':fire:', use_aliases=True)
    emojghost=emojize(':ghost:', use_aliases=True)
    emojundead=emojize(':skull:', use_aliases=True)
    bot.send_message(message.from_user.id, emojundead+'O`liklar:'+"\n"+'Ushba mavjudotlar allaqachon o`lib bo`lishgan ularni rostakamiga o`ldirishning yagona yo`li ularning jismoniy tanalarini yo`q qilishdir.'+"\n"+
                     'Zarb yetkazishi:'+"\n"+'= '+emojelectro+'elektro: 200%'+"\n"+'= '+emojbio+'bio: 100%'+"\n"+'= '+emojfire+'olovlilar: 100%'+"\n"+'= '+emojghost+'ruxlar: 100%'+"\n"+"\n"+  
                     'Qabul qiluvchi zarari:'+"\n"+'= '+emojelectro+'elektro: 100%'+"\n"+'= '+emojbio+'bio: 200%'+"\n"+'= '+emojfire+'olovlilar: 100%'+"\n"+'= '+emojghost+'ruxlar: 100%'+"\n"+"\n"+ 
                     'Kuchlari:'+"\n"+'"O`liklar lanati" (Skilet-qilichbozda bor) - 25% ehtimollikda o`liklar zarbini 60% ga kuchaytirish imkoniyatiga ega.'+"\n"+
                     '"Qonxo`rlik" (Chupakabrada bor) - hujum qilayotganda yetkazgan zarbini 50% ga o`zini davolab olishi mumkin (kuch ishlatilganda jon 0dan ko`p bo`lishi lozim).'+"\n"+
                     '"Haydash" (Qora Ajalda bor) - 15% ehtimollikda taqribiy dushman maxluqini bu dunyodan haydab yuboradi. Uning hayotiga ega bo`lib jonining 40% ini o`ziniki qilib oladi. Shuningdek uning zarb kuchini 100% o`ziniki qilib oladi!'
                    )
    
 
    
@bot.message_handler(commands=['fight'])
def fightstart(message):
  if message.from_user.id in info.lobby.game:
    if message.chat.id==info.lobby.game[message.from_user.id]['chatid']:
      if info.lobby.game[message.from_user.id]['battle']==0:
        if len(info.lobby.game[message.from_user.id]['players'])%2==0:
         if len(info.lobby.game[message.from_user.id]['players'])!=0:
          if info.lobby.game[message.from_user.id]['battle']==0:
            bot.send_document(message.chat.id,test.newid,caption="*📯O'yin boshlanayabdi! 💧O'z Manangizni tayyorlang......*", parse_mode='markdown')
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
                bot.send_message(ids2, 'Siz saroy himoyachisisiz! Sizning komandangiz: '+info.lobby.game[message.from_user.id]['teammates2'])
            for ids1 in info.lobby.game[message.from_user.id]['team1']:
                bot.send_message(ids1, 'Siz saroyga xujumchisisiz! Sizning komandangiz: '+info.lobby.game[message.from_user.id]['teammates1'])
            btl=threading.Thread(target=battle, args=[message.from_user.id])
            btl.start()
            bot.send_message(441399484, 'Qaysidir chatda o`yin boshlandi!')
            info.lobby.game[message.from_user.id]['thread']=btl
            print(info.lobby.game)
            info.lobby.game[message.from_user.id]['playing']=1
          else:
            bot.send_message(message.chat.id, 'O`yin - ('+info.lobby.game[message.from_user.id]['name']+') allaqachon boshlangandi!')
         else:
            bot.send_message(message.chat.id, 'O`yinda 0 ta o`yinchi!')  
        else:
          bot.send_message(message.chat.id, 'Faqatgina juft o`yinchilar soni bilan o`yinni boshlash mumkin!')

       
@bot.message_handler(commands=['join'])
def joinm(message):
  for key in info.lobby.game:
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
               bot.send_message(message.from_user.id, 'Siz o`yinga omadli qo`shildingiz!')
               info.lobby.game[key]['players'][message.from_user.id]=createuser(message.from_user.id, 1, message.from_user.first_name)
               info.lobby.game[key]['players'][message.from_user.id]['cash']=info.lobby.game[id]['name']
               info.lobby.game[key]['len']+=1
               bot.send_message(message.chat.id, 'Siz o`yinga omadli qo`shildingiz ('+str(info.lobby.game[key]['players'][message.from_user.id]['cash'])+')! O`yin boshlanishi uchun uni boshlagan odam /fight tugmasini bosishi lozim!')
    if info.lobby.game[message.from_user.id]['playing']==0: 
    else:
      bot.send_message(message.chat.id, 'O`yin allaqachon boshlangan!')         
              except:
                bot.send_message(message.chat.id, 'O`yinga qo`shilish uchun @WarsUzBot bilan bog`lan!')
           else:  
                pass

           
@bot.message_handler(commands=['cancel'])
def cancelmessage(message):
  if message.from_user.id in info.lobby.game:
    if info.lobby.game[message.from_user.id]['playing']==0:
      cancel(message.from_user.id, message.chat.id)
    else:
      bot.send_message(message.chat.id, 'O`yin allaqachon boshlangan!')


@bot.message_handler(commands=["rathunt"])
def start_game(message):
  m=message.from_user.id
  bot.send_document(m,test.dogid,caption="Qo`shilish uchun /join knopkasini bosing. O`yin bekor qilinishiga 5 daqiqa qoldi.")
    
@bot.message_handler(commands=['start'])
def startmessage(message):
  m=message.from_user.id
  bot.send_message(m, '"Sexrli Janglar" o`yiniga hush kelibsiz! Bu yerda siz o`z mo`jizaviy qo`shiningizni yaratib do`stlaringiz bilan kurashishingiz mumkin.'+
                  ' Buning uchun esa har bir mavjudotlarni hususiyatlarini o`rganib chiqing! To`liq ma`lumot uchun /help tugmasini bosing!') 
                  
                   

@bot.message_handler(commands=['help'])
def helpmessage(message):
 try:
  bot.send_message(message.from_user.id, 'Bu o`yinni o`nash uchun botni guruhga qo`shing va /begin tugmasini bosing. Bir o`yinchi faqat bitta o`yinda mavjud bo`lishi mumkin. O`yinni boshlagan odam avtomatik uni azosiga aylanadi.'+"\n"+      
                   'Bu o`yinda siz saroyni himoya qiluvchi yoki dushmanga hujum qiluvchi afsungarlardan biri bo`lasiz (kuchlar teng bo`ladi). '+
                   'Dushmanga hujum qilish uchun sexrli belgilar chizib portal ochasiz. Portaldan siz tanlagan mo`jizaviy mavjudotlardan biri chiqadi'+
                   '(Portalni ochish uchun Mana-Sexr kerak bo`ladi. Mana har yurishda 55taga ko`payadi (Agarda o`yinda 2tadan ko`p odam bo`lsa 30tadan ko`payadi). Chiqargan mo`jizaviy mavjudotlaringiz dushman saroyiga hujum qilishadi. Agarda 1ta bo`lsa ham mavjudot dushman darvozasiga yetib borsa saroy 1ta jonini yo`qotadi (Umumiy 5ta).'+
                   'Barcha mavjudotlar o`z xususiyatiga ega. Sizning vazifangiz ularni aql bilan tanlash.'+'Har bir yurishda sizga taqribiy 3ta portal beriladi va ularni tanlab o`ziz hohlagan mavjudotni chiqarasiz.'+'Guruhga qarshi guruh o`ynashi mumkin!'+"\n"+'O`yindan maqsad: Dushman saroyini yo`q qilish.'+"\n"+'O`yinda 5ta klass mavjudotlar bor:'+"\n"+'Elektromaxluqlar, Biologik mutantlar, Olovli maxluqlar, Ruhsimon maxluqlar va O`liksimon maxluqlar.'+"\n"+
                    'Ularni har biri bilan tanishish uchun bos: /electro, /bio, /fire, /ghost, /undead. (Bir xil mavjudotlar doimo bir biriga 100% zarar yetkazadi)')
  if message.chat.id<0:
        bot.send_message(message.chat.id, 'Sizga shaxsiy xat jo`natildi')
 except:
        bot.send_message(message.chat.id, 'O`yinga qo`shilish uchun @WarsUzBot bilan bog`lan!')


@bot.message_handler(commands=['begin'])
def beginmessage(message):
 a=0
 if message.from_user.id not in info.lobby.game:
  for id in info.lobby.game:
    if message.chat.id==info.lobby.game[id]['chatid']:
        a+=1
  if a>0:
    bot.send_message(message.chat.id, 'O`yin guruhda allaqachon ketayabdi!')
  else:
   if message.chat.id<0:
    userapply=0
    try:
      bot.send_message(message.from_user.id, 'Siz o`yinga omadli qo`shildingiz!')
      userapply=1
    except:
      bot.send_message(message.chat.id, 'O`yinga qo`shilish uchun @WarsUzBot bilan bog`laning!')
    if userapply==1:
      createdlobby=createlobby(message.chat.id, message.from_user.id, message.from_user.first_name)
      info.lobby.game.update(createdlobby)
      print(info.lobby.game)
      bot.send_document(message.chat.id,test.dragoid,caption="*🧙‍♂O`yin yaratildi! Keyingi jo`natadigan xatingiz bilan uni nomlang!*"+"\n"+"*🔮Agarda siz o`yinni to`xtatmoqchi bo`lsaz* /cancel *tugmasini bosing.*"+"\n"+"*⏳O`yin 20 daqiqadan so`ng avtomatik o`chiriladi!*", parse_mode='markdown')   
      info.lobby.game[message.from_user.id]['naming']=1
      lobbycancel=threading.Timer(1200.0, cancel, args=[message.from_user.id, message.chat.id])
      lobbycancel.start()
        
   else:
    bot.send_message(message.from_user.id, 'Faqat guruhlardagina o`ynash mumkin!')
    
    
@bot.message_handler(commands=['surrender'])
def surrender(message):
    for id in info.lobby.game:
        if message.chat.id==info.lobby.game[id]['chatid']:
          if message.from_user.id in info.lobby.game[id]['players']:
            bot.send_message(message.chat.id, info.lobby.game[id]['players'][message.from_user.id]['fname']+' taslim bo`ldi!')
            del info.lobby.game[id]['players'][message.from_user.id]
            if message.from_user.id in info.lobby.game[id]['team1']:
                del info.lobby.game[id]['team1'][message.from_user.id]
                info.lobby.game[id]['len']-=1
            elif message.from_user.id in info.lobby.game[id]['team2']:
                del info.lobby.game[id]['team2'][message.from_user.id]
                info.lobby.game[id]['len']-=1

    
  
  
@bot.message_handler(content_types=['text'])
def namemessage(message):
  if message.from_user.id in info.lobby.game:
    if info.lobby.game[message.from_user.id]['creatorid']['selfid']==message.from_user.id:
      if info.lobby.game[message.from_user.id]['naming']==1:
        if len(message.text)<31:
         if message.text!='None':
          if message.chat.id==info.lobby.game[message.from_user.id]['chatid']:
            info.lobby.game[message.from_user.id]['name']=message.text
            bot.send_message(message.chat.id, "🎴Siz o'yinga yangi nom berdingiz: *"+message.text+"*❕"+"\n"+"O'yinchilarni kutyabmiz...\nO'yinga qo'shilish uchun /join tugmasini bosing.", parse_mode='markdown')
            info.lobby.game[message.from_user.id]['naming']=0  
         else:
          bot.send_message(message.chat.id, 'Ruxsat etilmaydigan nom!')
        else:
          bot.send_message(message.chat.id, 'Nomning uzunligi 30ta belgidan oshmasligi lozim!')
                
  
def cancel(id, chatid):
 if id in info.lobby.game:
  if info.lobby.game[id]['playing']==0:
    info.lobby.game[id].clear()
    del info.lobby.game[id]
    bot.send_message(chatid, 'O`yin to`xtatildi!')
  
  

  
  
  
def createlobby(chatid, creatorid, fname):
  emojshield=emojize(':shield:', use_aliases=True)
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
                  'tiranozavr':{},
                  's4upakabra':{},
                  'golem':{},
                  'vsadnik':{},
                  'soulcatcher':{},
                  'zombie':{}
             },
    't2mobs':{'s_me4nik':{},
                  'phoenix':{},
                  'electromagnit':{},
                  'manoed':{},
                  'pyos':{},
                  'tiranozavr':{},
                  's4upakabra':{},
                  'golem':{},
                  'vsadnik':{},
                  'soulcatcher':{},
                  'zombie':{}
             },
    'resultst1':''+"\n",
    'resultst2':''+"\n",
    'readys':0,
    'launchtimer':0,
    'timer':None,
    'hod':1,
    'teammates1':'',
    'teammates2':'',
    'throne1hp':3,
    'throne2hp':3,
    'thronedamage':'',
    'manaplust1':0,
    'manaplust2':0,
    't1hod':0,
    'thronedamagemobs':'',
    'skills1':'',
    'skills2':'',
    'thread':None,
    'lifecast':0
      

           }
        }
  
  
def createuser(id, x, fname):
    if id==197216910:   #pyos
        return{'selfid':id,
         'lastmessage':0,
         'tvari':{'s_me4nik':{},
                  'phoenix':{},
                  'electromagnit':{},
                  'manoed':{},
                  'pyos':{},
                  'tiranozavr':{},
                  's4upakabra':{},
                  'golem':{},
                  'vsadnik':{}
         },
         'portals':{'s_me4nik':{'count':0},
                  'phoenix':{'count':0},
                  'electromagnit':{'count':0},
                  'manoed':{'count':0},
                  'pyos':{'count':0},
                  'tiranozavr':{'count':0},
                  's4upakabra':{'count':0},
                  'golem':{'count':0},
                  'vsadnik':{'count':0}

                   },
         'mana':60,
         'mobnumber':0,
         'manamax':500,
         'inlobby':x,
         'cash':'',
         'allmobs':['s_me4nik', 'electromagnit', 'phoenix', 'manoed', 'pyos', 'tiranozavr', 's4upakabra', 'golem', 'vsadnik'],
         'mobsinturn':[],
         'name1mob':'',
         'name2mob':'',
         'name3mob':'',
         'ready':0,
         'fname':fname,
         'currentmessage':'',
         'manaregen':55,
         'bufftext':''
            } 
    
    elif id==218485655:   #vasiliy
        return{'selfid':id,
         'lastmessage':0,
         'tvari':{'s_me4nik':{},
                  'phoenix':{},
                  'electromagnit':{},
                  'manoed':{},
                  'tiranozavr':{},
                  's4upakabra':{},
                  'golem':{},
                  'vsadnik':{},
                  'soulcatcher':{}
         },
         'portals':{'s_me4nik':{'count':0},
                  'phoenix':{'count':0},
                  'electromagnit':{'count':0},
                  'manoed':{'count':0},
                  'tiranozavr':{'count':0},
                  's4upakabra':{'count':0},
                  'golem':{'count':0},
                  'vsadnik':{'count':0},
                  'soulcatcher':{'count':0}

                   },
         'mana':60,
         'mobnumber':0,
         'manamax':500,
         'inlobby':x,
         'cash':'',
         'allmobs':['s_me4nik', 'electromagnit', 'phoenix', 'manoed', 'tiranozavr', 's4upakabra', 'golem', 'vsadnik', 'soulcatcher'],
         'mobsinturn':[],
         'name1mob':'',
         'name2mob':'',
         'name3mob':'',
         'ready':0,
         'fname':fname,
         'currentmessage':'',
         'manaregen':55
            } 
    
    
    elif id==441399484:  #ya
        return{'selfid':id,
         'lastmessage':0,
         'tvari':{'s_me4nik':{},
                  'phoenix':{},
                  'electromagnit':{},
                  'manoed':{},
                  'tiranozavr':{},
                  's4upakabra':{},
                  'golem':{},
                  'vsadnik':{},
                  'soulcatcher':{},
                  'pyos':{},
                  'zombie':{}
         },
         'portals':{'s_me4nik':{'count':0},
                  'phoenix':{'count':0},
                  'electromagnit':{'count':0},
                  'manoed':{'count':0},
                  'tiranozavr':{'count':0},
                  's4upakabra':{'count':0},
                  'golem':{'count':0},
                  'vsadnik':{'count':0},
                  'soulcatcher':{'count':0},
                  'pyos':{'count':0},
                  'zombie':{'count':0}
                    
                   },
         'mana':60,
         'mobnumber':0,
         'manamax':500,
         'inlobby':x,
         'cash':'',
         'allmobs':['s_me4nik', 'electromagnit', 'phoenix', 'manoed', 'tiranozavr', 's4upakabra', 'golem', 'vsadnik', 'soulcatcher', 'pyos', 'zombie'],
         'mobsinturn':[],
         'name1mob':'',
         'name2mob':'',
         'name3mob':'',
         'ready':0,
         'fname':fname,
         'currentmessage':'',
         'manaregen':55
            } 
    
    
    
    elif id==385049690:  #griffit
        return{'selfid':id,
         'lastmessage':0,
         'tvari':{'s_me4nik':{},
                  'phoenix':{},
                  'electromagnit':{},
                  'manoed':{},
                  'tiranozavr':{},
                  's4upakabra':{},
                  'golem':{},
                  'vsadnik':{},
                  'zombie':{}
         },
         'portals':{'s_me4nik':{'count':0},
                  'phoenix':{'count':0},
                  'electromagnit':{'count':0},
                  'manoed':{'count':0},
                  'tiranozavr':{'count':0},
                  's4upakabra':{'count':0},
                  'golem':{'count':0},
                  'vsadnik':{'count':0},
                  'zombie':{'count':0}
                   },
         'mana':60,
         'mobnumber':0,
         'manamax':500,
         'inlobby':x,
         'cash':'',
         'allmobs':['s_me4nik', 'electromagnit', 'phoenix', 'manoed', 'tiranozavr', 's4upakabra', 'golem', 'vsadnik', 'zombie'],
         'mobsinturn':[],
         'name1mob':'',
         'name2mob':'',
         'name3mob':'',
         'ready':0,
         'fname':fname,
         'currentmessage':'',
         'manaregen':55
            }  
    
    
    else:  
      return{'selfid':id,
         'lastmessage':0,
         'tvari':{'s_me4nik':{},
                  'phoenix':{},
                  'electromagnit':{},
                  'manoed':{},
                  'tiranozavr':{},
                  's4upakabra':{},
                  'golem':{},
                  'vsadnik':{}
         },
         'portals':{'s_me4nik':{'count':0},
                  'phoenix':{'count':0},
                  'electromagnit':{'count':0},
                  'manoed':{'count':0},
                  'tiranozavr':{'count':0},
                  's4upakabra':{'count':0},
                  'golem':{'count':0},
                  'vsadnik':{'count':0}
                   },
         'mana':60,
         'mobnumber':0,
         'manamax':500,
         'inlobby':x,
         'cash':'',
         'allmobs':['s_me4nik', 'electromagnit', 'phoenix', 'manoed', 'tiranozavr', 's4upakabra', 'golem', 'vsadnik'],
         'mobsinturn':[],
         'name1mob':'',
         'name2mob':'',
         'name3mob':'',
         'ready':0,
         'fname':fname,
         'currentmessage':'',
         'manaregen':55
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
        'stun':0,
        'shield':0
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
        'stun':0,
        'shield':0
                
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
      print(info.lobby.game[creatorid]['players'])
    for key in info.lobby.game[creatorid]['players']:
      mobs(key, creatorid)
      if len(info.lobby.game[creatorid]['players'])>2:
             for id in info.lobby.game[creatorid]['players']:
               info.lobby.game[creatorid]['players'][id]['manaregen']=30
      info.lobby.game[creatorid]['players'][key]['mana']+=info.lobby.game[creatorid]['players'][key]['manaregen']      
      mana=emojize(':droplet:', use_aliases=True)
      go=emojize(':video_game:', use_aliases=True)
      end=emojize(':white_check_mark:', use_aliases=True)
      infos=emojize(':question:', use_aliases=True)
      Keyboard=types.InlineKeyboardMarkup()       
      Keyboard.add(types.InlineKeyboardButton(text=go+"Harakatlar", callback_data='do'))
      Keyboard.add(types.InlineKeyboardButton(text=infos+"Men haqimdagi ma`lumot", callback_data='info'))
      Keyboard.add(types.InlineKeyboardButton(text=end+"Yurishni yakunlash", callback_data='end'))     
      msg=bot.send_message(key, 'Bosh Menyu:'+"\n"+mana+'Mana: '+str(info.lobby.game[creatorid]['players'][key]['mana'])+'/'+str(info.lobby.game[creatorid]['players'][key]['manamax']),reply_markup=Keyboard)
      info.lobby.game[creatorid]['players'][key]['lastmessage']=msg.message_id
      info.lobby.game[creatorid]['players'][key]['currentmessage']=msg.message_id
       


if __name__ == '__main__':
  bot.polling(none_stop=True)
