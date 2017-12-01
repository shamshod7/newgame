# -*- coding: utf-8 -*-
import redis
import os
import telebot
import opr_config
import opr_data
import math
import random
import threading
from telebot import types
token = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(token)

vip=[208094271, 314238081, 84959870]

def reboot(id):
    opr_data.oprmove[id]['tatk']=0
    opr_data.oprmove[id]['hatk']=0
    opr_data.oprmove[id]['latk']=0
    opr_data.oprmove[id]['tdef']=0
    opr_data.oprmove[id]['hdef']=0
    opr_data.oprmove[id]['ldef']=0
    opr_data.oprmove[id]['oprtdef']=2
    opr_data.oprmove[id]['oprhdef']=2
    opr_data.oprmove[id]['oprldef']=2
    opr_data.player.person[id]['pltdef']=2
    opr_data.player.person[id]['plhdef']=2
    opr_data.player.person[id]['plldef']=2
    opr_data.player.person[id]['tatk']=0
    opr_data.player.person[id]['hatk']=0
    opr_data.player.person[id]['latk']=0
    opr_data.player.person[id]['tdef']=0
    opr_data.player.person[id]['hdef']=0
    opr_data.player.person[id]['ldef']=0
    opr_data.player.person[id]['krit']=0
    opr_data.player.person[id]['miss']=0
    opr_data.oprmove[id]['krit']=0
    opr_data.oprmove[id]['miss']=0
    opr_data.oprmove[id]['chlen']=0
    
    


def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode='Markdown'):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)


@bot.callback_query_handler(func=lambda call:True)
def inline(call):
    if call.data=='telo':
      if call.from_user.id in opr_data.players:
        if opr_data.player.person[call.from_user.id]['x']==1:
            opr_data.player.person[call.from_user.id]['tatk']=1
            opr_data.player.person[call.from_user.id]['latk'] = 0
            opr_data.player.person[call.from_user.id]['hatk'] = 0
            medit('Атака: тело', call.from_user.id, call.message.message_id)
            Keyboard = types.InlineKeyboardMarkup()
            Keyboard.add(types.InlineKeyboardButton(text="Голова", callback_data='headd'))
            Keyboard.add(types.InlineKeyboardButton(text="Тело", callback_data='telod'))
            Keyboard.add(types.InlineKeyboardButton(text="Ноги", callback_data='legd'))
            msg = bot.send_message(call.from_user.id, '*Выберите место для защиты*', reply_markup=Keyboard)
            opr_data.player.person[call.from_user.id]['x'] = 0
            opr_data.player.person[call.from_user.id]['y'] = 1





    elif call.data=='leg':
      if call.from_user.id in opr_data.players:
        if opr_data.player.person[call.from_user.id]['x']==1:
            opr_data.player.person[call.from_user.id]['tatk']=0
            opr_data.player.person[call.from_user.id]['latk'] = 1
            opr_data.player.person[call.from_user.id]['hatk'] = 0
            medit('Атака: ноги', call.from_user.id, call.message.message_id)
            Keyboard = types.InlineKeyboardMarkup()
            Keyboard.add(types.InlineKeyboardButton(text="Голова", callback_data='headd'))
            Keyboard.add(types.InlineKeyboardButton(text="Тело", callback_data='telod'))
            Keyboard.add(types.InlineKeyboardButton(text="Ноги", callback_data='legd'))
            msg = bot.send_message(call.from_user.id, '*Выберите место для защиты*', reply_markup=Keyboard)
            opr_data.player.person[call.from_user.id]['x'] = 0
            opr_data.player.person[call.from_user.id]['y'] = 1




    elif call.data == 'head':
      if call.from_user.id in opr_data.players:
        if opr_data.player.person[call.from_user.id]['x']==1:
            opr_data.player.person[call.from_user.id]['tatk']=0
            opr_data.player.person[call.from_user.id]['latk'] = 0
            opr_data.player.person[call.from_user.id]['hatk'] = 1
            medit('Атака: голова', call.from_user.id, call.message.message_id)
            Keyboard = types.InlineKeyboardMarkup()
            Keyboard.add(types.InlineKeyboardButton(text="Голова", callback_data='headd'))
            Keyboard.add(types.InlineKeyboardButton(text="Тело", callback_data='telod'))
            Keyboard.add(types.InlineKeyboardButton(text="Ноги", callback_data='legd'))
            msg = bot.send_message(call.from_user.id, '*Выберите место для защиты*', reply_markup=Keyboard)
            opr_data.player.person[call.from_user.id]['x'] = 0
            opr_data.player.person[call.from_user.id]['y'] = 1


    elif call.data=='headd':
      if call.from_user.id in opr_data.players:
        if opr_data.player.person[call.from_user.id]['y']==1:
            medit('Защита: голова', call.from_user.id, call.message.message_id)
            opr_data.player.person[call.from_user.id]['tdef'] = 0
            opr_data.player.person[call.from_user.id]['ldef'] = 0
            opr_data.player.person[call.from_user.id]['hdef'] = 1
            opr_data.player.person[call.from_user.id]['y'] = 0
            z = random.randint(1, 5)
            starttimer = threading.Timer(z, endturn, [call.from_user.id])
            starttimer.start()

    elif call.data=='legd':
      if call.from_user.id in opr_data.players:
        if opr_data.player.person[call.from_user.id]['y']==1:
            medit('Защита: ноги', call.from_user.id, call.message.message_id)
            opr_data.player.person[call.from_user.id]['tdef'] = 0
            opr_data.player.person[call.from_user.id]['ldef'] = 1
            opr_data.player.person[call.from_user.id]['hdef'] = 0
            opr_data.player.person[call.from_user.id]['y'] = 0
            z = random.randint(1, 5)
            starttimer = threading.Timer(z, endturn, [call.from_user.id])
            starttimer.start()


    elif call.data == 'telod':
      if call.from_user.id in opr_data.players:
        if opr_data.player.person[call.from_user.id]['y']==1:
            medit('Защита: тело', call.from_user.id, call.message.message_id)
            opr_data.player.person[call.from_user.id]['tdef'] = 1
            opr_data.player.person[call.from_user.id]['ldef'] = 0
            opr_data.player.person[call.from_user.id]['hdef'] = 0
            opr_data.player.person[call.from_user.id]['y'] = 0
            z = random.randint(1, 5)
            starttimer = threading.Timer(z, endturn, [call.from_user.id])
            starttimer.start()




def createuser():
    return {'x':0,
            'chlen':0,
            'yron':0,
            'y':0,
            'z':0,
            'krit':0,
            'miss':0,
           'pltdef':2,
           'plhdef':2,
           'plldef':2,
           'tatk':0,
           'hatk':0,
           'latk':0,
           'tdef':0,
           'hdef':0,
           'ldef':0,
           'hp':100,
           'dmg':25,
           'endgame':0,
           'name':''
            }



def createopr():
    return {'tatk':0,
            'chlen':0,
            'krit':0,
            'miss':0,
            'yron':0,
         'hatk':0,
         'latk':0,
         'tdef':0,
         'hdef':0,
         'ldef':0,
         'hp':100,
         'oprtdef':2,
         'oprhdef':2,
         'oprldef':2}



def selectopr(id):
    x=random.randint(1,3)
    if x==1:
        opr_data.oprmove[id]['tatk']=1
        opr_data.oprmove[id]['latk']=0
        opr_data.oprmove[id]['hatk']=0
    elif x==2:
        opr_data.oprmove[id]['tatk']=0
        opr_data.oprmove[id]['latk']=0
        opr_data.oprmove[id]['hatk']=1
    elif x==3:
        opr_data.oprmove[id]['tatk']=0
        opr_data.oprmove[id]['latk']=1
        opr_data.oprmove[id]['hatk']=0

    y=random.randint(1,3)
    if y==1:
        opr_data.oprmove[id]['tdef'] = 1
        opr_data.oprmove[id]['ldef'] = 0
        opr_data.oprmove[id]['hdef'] = 0
    elif y==2:
        opr_data.oprmove[id]['tdef'] = 0
        opr_data.oprmove[id]['ldef'] = 1
        opr_data.oprmove[id]['hdef'] = 0
    elif y==3:
        opr_data.oprmove[id]['tdef'] = 0
        opr_data.oprmove[id]['ldef'] = 0
        opr_data.oprmove[id]['hdef'] = 1




def oprdmg(id):
    if opr_data.oprmove[id]['tatk']==1:
        if opr_data.player.person[id]['tdef']==1:
            pltdef=1
            opr_data.player.person[id]['pltdef'] = pltdef
        elif opr_data.player.person[id]['tdef']==0:
            pltdef=0
            a=random.randint(15,30)
            opr_data.player.person[id]['hp']-=a
            opr_data.player.person[id]['pltdef']=pltdef
            opr_data.oprmove[id]['yron']=a

            
    elif opr_data.oprmove[id]['hatk']==1:
        if opr_data.player.person[id]['hdef']==1:
            plhdef=1
            opr_data.player.person[id]['plhdef'] = plhdef
        elif opr_data.player.person[id]['hdef']==0:
            plhdef=0
            kritdmg=random.randint(1,100)
            missed=random.randint(1,100)
            if missed<=15:
                opr_data.oprmove[id]['miss']=1
            else:
              if kritdmg<=25:
                a=45
                opr_data.oprmove[id]['krit']=1
              else:
                a=random.randint(9,18)
              opr_data.player.person[id]['hp']-=a
              opr_data.player.person[id]['plhdef']=plhdef
              opr_data.oprmove[id]['yron']=a


    elif opr_data.oprmove[id]['latk']==1:
        chl=random.randint(1,100)
        if chl==1:
            opr_data.player.person[id]['hp']=0
            opr_data.oprmove[id]['chlen']=1
        if opr_data.player.person[id]['ldef']==1:
            plldef=1
            opr_data.player.person[id]['plldef'] = plldef
        elif opr_data.player.person[id]['ldef']==0:
            plldef=0
            a=random.randint(15,20)
            opr_data.player.person[id]['hp']-=a
            opr_data.player.person[id]['plldef']=plldef
            opr_data.oprmove[id]['yron']=a



def pldmg(id):
    if opr_data.player.person[id]['tatk']==1:
        if opr_data.oprmove[id]['tdef']==1:
            oprtdef=1
            opr_data.oprmove[id]['oprtdef'] = oprtdef
        elif opr_data.oprmove[id]['tdef']==0:
            oprtdef=0
            a=random.randint(15,25)
            opr_data.oprmove[id]['hp']-=a
            opr_data.oprmove[id]['oprtdef']=oprtdef
            opr_data.player.person[id]['yron']=a


    elif opr_data.player.person[id]['hatk']==1:
        if opr_data.oprmove[id]['hdef']==1:
            oprhdef=1
            opr_data.oprmove[id]['oprhdef'] = oprhdef
        elif opr_data.oprmove[id]['hdef']==0:
            oprhdef=0
            krit=random.randint(1,100)
            promax=random.randint(1,100)
            if promax<=30:
                opr_data.player.person[id]['miss']=1
            else:
              if krit<=50:
                  opr_data.oprmove[id]['hp']-=32
                  opr_data.player.person[id]['krit']=1
              else:
                  a=random.randint(15,25)
                  opr_data.oprmove[id]['hp']-=a
                  opr_data.oprmove[id]['oprhdef']=oprhdef
                  opr_data.player.person[id]['yron']=a

    
    elif opr_data.player.person[id]['latk']==1:
        chlen=random.randint(1, 100)
        if chlen==1:
            opr_data.oprmove[id]['hp']=0
            opr_data.player.person[id]['chlen']=1
        if opr_data.oprmove[id]['ldef']==1:
            oprldef=1
            opr_data.oprmove[id]['oprldef'] = oprldef
        elif opr_data.oprmove[id]['ldef']==0:
            oprldef=0
            a=random.randint(10,15)
            opr_data.oprmove[id]['hp']-=a
            opr_data.oprmove[id]['oprldef']=oprldef
            opr_data.player.person[id]['yron']=a



def abc(id):
    if opr_data.player.person[id]['plhdef']==1:
        opr_data.text4='Вы заблокировали удар в голову!'
    elif opr_data.player.person[id]['plhdef']==0:
        opr_data.text4 = 'Опричник поразил вас ударом в голову, нанеся '+str(opr_data.oprmove[id]['yron'])+' урона!'
    elif opr_data.player.person[id]['plldef']==1:
        opr_data.text4='Вы спаслись от удара по ногам!'
    elif opr_data.player.person[id]['plldef']==0:
        opr_data.text4 = 'Опричник ударил вас по ногам, нанеся '+str(opr_data.oprmove[id]['yron'])+' урона!'
    elif opr_data.player.person[id]['pltdef']==1:
        opr_data.text4='Вы ушли от удара по телу!'
    elif opr_data.player.person[id]['pltdef']==0:
        opr_data.text4 = 'Опричник нанес вам удар по телу, уменьшив ваше хп на '+str(opr_data.oprmove[id]['yron'])+'!'
    if opr_data.oprmove[id]['krit']==1:
        opr_data.text4='Опричник разозлился и испытал на вас свой коронный удар в голову, нанеся 45 урона!'
    if opr_data.oprmove[id]['miss']==1:
        opr_data.text4='Опричник промахнулся!'
    if opr_data.oprmove[id]['chlen']==1:
        opr_data.text4='Опричник поразил вас ударом между ног! Вы в нокауте!'
        




def abcd(id):
    if opr_data.oprmove[id]['oprtdef']==1:
        opr_data.text3='Опричник успешно отразил удар по телу;'
    elif opr_data.oprmove[id]['oprtdef']==0:
        opr_data.text3='Вы нанесли опричнику удар по телу, и убавили его ХП на '+str(opr_data.player.person[id]['yron'])+';'
    elif opr_data.oprmove[id]['oprhdef']==1:
        opr_data.text3='Опричник уклонился от удара, который шел ровно ему в голову;'
    elif opr_data.oprmove[id]['oprhdef']==0:
        opr_data.text3 = 'Вы поразили опричника в голову, нанеся '+str(opr_data.player.person[id]['yron'])+' урона;'
    elif opr_data.oprmove[id]['oprldef']==1:
        opr_data.text3='Опричник ушел от удара по ногам;'
    elif opr_data.oprmove[id]['oprldef']==0:
        opr_data.text3 = 'Вы ударили опричника по ногам, нанеся '+str(opr_data.player.person[id]['yron'])+' урона;'
    if opr_data.player.person[id]['chlen']==1:
        opr_data.text3 = 'Вы нанесли опричнику КРИТИЧЕСКИЙ удар между ног! опричник повержен;'
    if opr_data.player.person[id]['miss']==1:
        opr_data.text3='Вы промахнулись!'
    if opr_data.player.person[id]['krit']==1:
        opr_data.text3='Вы нанесли опричнику критический удар!(32 урона);'



def endturn(id):
    selectopr(id)
    pldmg(id)
    oprdmg(id)
    abc(id)
    abcd(id)
    reboot(id)
    bot.send_message(id,'Результаты хода:'+"\n"+
                     opr_data.text3+"\n"+opr_data.text4)
    bot.send_message(id, 'Ваше ХП: '+str(opr_data.player.person[id]['hp'])+"\n"+'ХП Опричника: '+str(opr_data.oprmove[id]['hp']))
    play(id)






def removeban(id):
    if id in opr_data.ban:
      opr_data.ban.remove(id)
  



def timers(id, fname):
    if id not in opr_data.ban:
        opr_data.ban.append(id) 
        print(opr_data.ban)
        removethread=threading.Timer(80.0, removeban,[id])
        removethread.start()
        opr_data.oprmove[id]=createopr()
        opr_data.player.person[id] = createuser()
        opr_data.player.person[id]['name']=fname
        opr_data.players.append(id)
        return 'Подсказки по бою: атакуя в ноги, вы наносите меньше урона, но имеете шанс нанести опричнику фатальный урон. Атакуя в голову, у вас есть шанс нанести критический урон, но есть и шанс промаха. Напишите что-нибудь еще раз, чтобы вступить в драку'
    else:
        if id in opr_data.players:
          if opr_data.player.person[id]['endgame']==1:
            return 'опричник отдыхает, приходите через 2 минут после начала предыдущего боя'
          thr=threading.Thread(target=play, args=[id])
          thr.start()
        #play(id)
        #opr_data.player.person[id]['z']=1
          return 'Ну что ж, посмотрим, кто кого...'

        

@bot.message_handler(content_types=['text'])
def send_message(message):
    bot.send_message(message.from_user.id, timers(message.from_user.id, message.from_user.first_name))
   




def play(id):
    if opr_data.player.person[id]['hp']>0 and opr_data.oprmove[id]['hp']>0:
        bot.send_message(id, 'Новый раунд!')
        opr_data.player.person[id]['x'] = 1
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text="Голова", callback_data='head'))
        Keyboard.add(types.InlineKeyboardButton(text="Тело", callback_data='telo'))
        Keyboard.add(types.InlineKeyboardButton(text="Ноги", callback_data='leg'))
        msg=bot.send_message(id, '*Выберите место для атаки*',reply_markup=Keyboard)
    else:
        if opr_data.player.person[id]['hp']<=0:
            bot.send_message(id, '*Опричник победил вас.*'+"\n"+
                             '-Даже с больным коленом брошу тебя в темницу, '+opr_data.player.person[id]['name']+'!'+"\n"+'*Следующий бой через 2 минут после начала предыдущего*')
                             
            print('Поражение '+str(id))
            opr_data.oprmove[id]['chlen']=0
            opr_data.player.person[id]['z'] = 0
            opr_data.player.person[id]['endgame']=1
            if id in vip:
                opr_data.player.person[id]['endgame']=0
                opr_data.player.person[id]['hp']=100
                opr_data.oprmove[id]['hp']=100
        else:
            bot.send_message(id, '*Вы победили Опричника и отстояли свою честь!*'+"\n"+
                             '-А ты силён, '+opr_data.player.person[id]['name']+'! Попадешь в темницу в другой раз'+"\n"+'*Следующий бой через 2 минут после начала предыдущего*')
            print('Победа ' + str(id))
            opr_data.oprmove[id]['chlen']=0
            opr_data.player.person[id]['z']=0
            opr_data.player.person[id]['endgame']=1
            if id in vip:
                opr_data.player.person[id]['endgame']=0
                opr_data.player.person[id]['hp']=100
                opr_data.oprmove[id]['hp']=100
                



                











if __name__ == '__main__':
  bot.polling(none_stop=True)
