import opr_config
import telebot
import opr_data
import math
import random
import threading
from telebot import types
bot = telebot.TeleBot(opr_config.token)



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
            Keyboard.add(types.InlineKeyboardButton(text="Тело", callback_data='telod'))
            Keyboard.add(types.InlineKeyboardButton(text="Ноги", callback_data='legd'))
            Keyboard.add(types.InlineKeyboardButton(text="Голова", callback_data='headd'))
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
            Keyboard.add(types.InlineKeyboardButton(text="Тело", callback_data='telod'))
            Keyboard.add(types.InlineKeyboardButton(text="Ноги", callback_data='legd'))
            Keyboard.add(types.InlineKeyboardButton(text="Голова", callback_data='headd'))
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
            Keyboard.add(types.InlineKeyboardButton(text="Тело", callback_data='telod'))
            Keyboard.add(types.InlineKeyboardButton(text="Ноги", callback_data='legd'))
            Keyboard.add(types.InlineKeyboardButton(text="Голова", callback_data='headd'))
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
            'y':0,
            'z':0,
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
           'dmg':25
            }



def createopr():
    return {'tatk':0,
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
            opr_data.player.person[id]['hp']-=random.randint(15,25)
            opr_data.player.person[id]['pltdef']=pltdef

            
    elif opr_data.oprmove[id]['hatk']==1:
        if opr_data.player.person[id]['hdef']==1:
            plhdef=1
            opr_data.player.person[id]['plhdef'] = plhdef
        elif opr_data.player.person[id]['hdef']==0:
            plhdef=0
            opr_data.player.person[id]['hp']-=random.randint(15,25)
            opr_data.player.person[id]['plhdef']=plhdef


    elif opr_data.oprmove[id]['latk']==1:
        if opr_data.player.person[id]['ldef']==1:
            plldef=1
            opr_data.player.person[id]['plldef'] = plldef
        elif opr_data.player.person[id]['ldef']==0:
            plldef=0
            opr_data.player.person[id]['hp']-=random.randint(15,25)
            opr_data.player.person[id]['plldef']=plldef



def pldmg(id):
    if opr_data.player.person[id]['tatk']==1:
        if opr_data.oprmove[id]['tdef']==1:
            oprtdef=1
            opr_data.oprmove[id]['oprtdef'] = oprtdef
        elif opr_data.oprmove[id]['tdef']==0:
            oprtdef=0
            opr_data.oprmove[id]['hp']-=random.randint(15,25)
            opr_data.oprmove[id]['oprtdef']=oprtdef


    elif opr_data.player.person[id]['hatk']==1:
        if opr_data.oprmove[id]['hdef']==1:
            oprhdef=1
            opr_data.oprmove[id]['oprhdef'] = oprhdef
        elif opr_data.oprmove[id]['hdef']==0:
            oprhdef=0
            opr_data.oprmove[id]['hp']-=random.randint(15,25)
            opr_data.oprmove[id]['oprhdef']=oprhdef

    
    elif opr_data.player.person[id]['latk']==1:
        if opr_data.oprmove[id]['ldef']==1:
            oprldef=1
            opr_data.oprmove[id]['oprldef'] = oprldef
        elif opr_data.oprmove[id]['ldef']==0:
            oprldef=0
            opr_data.oprmove[id]['hp']-=random.randint(15,25)
            opr_data.oprmove[id]['oprldef']=oprldef



def abc(id):
    if opr_data.player.person[id]['plhdef']==1:
        opr_data.text4='Вы заблокировали удар в голову!'
    elif opr_data.player.person[id]['plhdef']==0:
        opr_data.text4 = 'Опричник нанес вам удар по голове!'
    elif opr_data.player.person[id]['plldef']==1:
        opr_data.text4='Вы спаслись от удара по ногам!'
    elif opr_data.player.person[id]['plldef']==0:
        opr_data.text4 = 'Опричник нанес вам удар по ногам!'
    elif opr_data.player.person[id]['pltdef']==1:
        opr_data.text4='Вы ушли от удара по телу!'
    elif opr_data.player.person[id]['pltdef']==0:
        opr_data.text4 = 'Опричник нанес вам удар по телу!'




def abcd(id):
    if opr_data.oprmove[id]['oprtdef']==1:
        opr_data.text3='Опричник успешно отразил удар по телу'
    elif opr_data.oprmove[id]['oprtdef']==0:
        opr_data.text3='Вы нанесли опричнику удар по телу!'
    elif opr_data.oprmove[id]['oprhdef']==1:
        opr_data.text3='Опричник уклонился от удара, который шел ровно ему в голову!'
    elif opr_data.oprmove[id]['oprhdef']==0:
        opr_data.text3 = 'Вы нанесли опричнику удар по голове!'
    elif opr_data.oprmove[id]['oprldef']==1:
        opr_data.text3='Опричник ушел от удара по ногам'
    elif opr_data.oprmove[id]['oprldef']==0:
        opr_data.text3 = 'Вы нанесли опричнику удар по ногам!'



def endturn(id):
    selectopr(id)
    pldmg(id)
    oprdmg(id)
    abc(id)
    abcd(id)
    reboot(id)
    bot.send_message(id,'Результаты хода:'+"\n"+
                     opr_data.text3+'; '+opr_data.text4)
    bot.send_message(id, 'Ваше ХП: '+str(opr_data.player.person[id]['hp'])+"\n"+'ХП Опричника: '+str(opr_data.oprmove[id]['hp']))
    play(id)






def removeban(id):
    opr_data.ban.remove(id)



def timers(id):
    if id not in opr_data.ban:
        opr_data.ban.append(id)
        print(opr_data.ban)
        removethread=threading.Timer(60.0, removeban,[id])
        removethread.start()
        opr_data.oprmove[id]=createopr()
        opr_data.player.person[id] = createuser()
        opr_data.players.append(id)
        return 'Вы не получали предупреждений, но теперь получили'
    else:
        thr=threading.Thread(target=play, args=[id])
        thr.start()
        #play(id)
        #opr_data.player.person[id]['z']=1
        return 'Ну что ж, посмотрим, кто кого...'

        

@bot.message_handler(content_types=['text'])
def send_message(message):
    bot.send_message(message.from_user.id, timers(message.from_user.id))




def play(id):
    if opr_data.player.person[id]['hp']>0 and opr_data.oprmove[id]['hp']>0:
        bot.send_message(id, 'Новый раунд!')
        opr_data.player.person[id]['x'] = 1
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text="Тело", callback_data='telo'))
        Keyboard.add(types.InlineKeyboardButton(text="Ноги", callback_data='leg'))
        Keyboard.add(types.InlineKeyboardButton(text="Голова", callback_data='head'))
        msg=bot.send_message(id, '*Выберите место для атаки*',reply_markup=Keyboard)
    else:
        if opr_data.player.person[id]['hp']<=0:
            bot.send_message(id, '*Опричник победил вас.*'+"\n"+
                             '-Даже с больным коленом брошу тебя в темницу...')
            print('Поражение '+str(id))
            opr_data.player.person[id]['z'] = 0
        else:
            bot.send_message(id, '*Вы победили Опричника и отстояли свою честь!*'+"\n"+
                             '-А ты силён... попадешь в темницу в другой раз')
            print('Победа ' + str(id))
            opr_data.player.person[id]['z']=0














if __name__ == '__main__':
  bot.polling(none_stop=True)
