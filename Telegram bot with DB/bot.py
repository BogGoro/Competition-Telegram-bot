# -*- coding: utf-8 -*-
import telebot
import config as cg
#import logging
import DB
import middleware
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
bot = telebot.TeleBot(cg.TOKEN)

DB.DB_init()
Admins_ids=[x[0] for x in DB.get_admins()]
markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(KeyboardButton("🔐 Вход в ...(Deleted)...",request_contact=True))
keyboardremove = telebot.types.ReplyKeyboardRemove()

markupforstep4 = InlineKeyboardMarkup()
markupforstep4.add(InlineKeyboardButton(text='Узнать про ...(Deleted)...', callback_data='Information'))
markupforstep4.add(InlineKeyboardButton(text='Пройти AR-квест на мероприятии', callback_data='ARquest'))

markupforstart = InlineKeyboardMarkup()
markupforstart.add(InlineKeyboardButton(text='Пройти AR-квест на мероприятии', callback_data='ARquest'))

markupforquest = InlineKeyboardMarkup()
markupforquest.add(InlineKeyboardButton(text='ВВЕСТИ AR-ПОДСКАЗКУ', callback_data='ARhint'))

markupforquestkeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
markupforquestkeyboard.add(KeyboardButton("ВВЕСТИ AR-ПОДСКАЗКУ"))

@bot.message_handler(commands=['help'],func=lambda message: message.chat.id in Admins_ids)
def help_commands(message):
    bot.send_message(message.chat.id,'/start - бот приветствует пользователя и запоминает его в БД.\n/exportDB - создает выгрузку таблицы пользователей\n/send_all - для отправки сообщения всем пользователям стартанувшим бота\n/send_registrated - для отправки сообщения зарегистрированным пользователям\n/send_user - для отправки сообщения определённым пользователям по ID')

@bot.message_handler(commands=['start'])
def hello(message):
    DB.add_user(message)
    msg = bot.send_message(message.chat.id,'''Привет 👋 Это ...(Deleted)..., для получения подробностей о мероприятии, пожалуйста,  авторизуйтесь по номеру телефона 👇
''',reply_markup=markup,disable_web_page_preview=True, parse_mode = 'HTML')
    bot.register_next_step_handler(msg, addNumber)
def addNumber(message):
    try:
        number=message.contact.phone_number
        DB.add_registrated(message.from_user.id,message.from_user.username,number)
        msg = bot.send_message(message.from_user.id,'Введите свою фамилию',reply_markup=keyboardremove)
        bot.register_next_step_handler(msg, addSurname)
    except Exception:
        hello(message)
def addSurname(message):
    DB.add_surname(message.from_user.id,message)
    msg = bot.send_message(message.from_user.id,'Введите своё имя')
    bot.register_next_step_handler(msg, addName)
def addName(message):
    DB.add_name(message.from_user.id,message)
    bot.send_message(message.from_user.id,'Вы успешно авторизовались в ...(Deleted)...')
    bot.send_message(message.from_user.id,'''...(Deleted)...''',disable_web_page_preview=True, parse_mode = 'HTML',reply_markup=markupforstep4)
    bot.send_message(message.from_user.id,'Если у вас есть вопрос, просто отправьте сообщение:')

@bot.callback_query_handler(func=lambda call: call.data == 'Information')
def callback_query(call):
    bot.send_message(call.from_user.id,'''Вы приглашены на закрытое мероприятие ...(Deleted)...''',disable_web_page_preview=True , parse_mode = 'HTML')
    bot.send_message(call.from_user.id,'Если у вас есть вопрос, просто отправьте сообщение:')

@bot.callback_query_handler(func=lambda call: call.data == 'ARquest')
def callback_query(call):
    DB.add_quest(call.from_user.id)
    bot.send_message(call.from_user.id,'''Приветствую вас на мероприятии ...(Deleted)...! 

Я помогу вам пройти 
<b>AR-квест от ...(Deleted)...</b> и получить подарок в финале мероприятия!  

Рядом со стендами с продуктами группы компаний расположены <b>7 QR-кодов</b>. 
Ищите и сканируйте их, осматривайте загруженные модели и находите <b>слова-подсказки</b>. Присылайте их мне, нажав на кнопку «<b>ВВЕСТИ AR-ПОДСКАЗКУ</b>».
''',disable_web_page_preview=True , parse_mode = 'HTML',reply_markup=markupforquestkeyboard)
    bot.send_message(call.from_user.id,'''Когда соберете все <b>7 слов-подсказок</b>, вы получите индивидуальный номер на розыгрыш подарков в конце второй официальной части мероприятия. 

<b>Уже нашли подсказку?</b> Нажимайте кнопку "ВВЕСТИ AR-ПОДСКАЗКУ", вводите найденное слово и отправляйте мне!
''',disable_web_page_preview=True , parse_mode = 'HTML',reply_markup=markupforquest)
    
@bot.callback_query_handler(func=lambda call: call.data == 'ARhint')
def callback_query(call):
    ARhint(call.from_user.id)

def ARhint(ID):
    msg = bot.send_message(ID,'''Введите подсказку''')
    bot.register_next_step_handler(msg, EnterHint)
def EnterHint(message):
    hint = message.text.upper()
    user = DB.get_userFromQuestLogById(message.from_user.id)
    if hint=='TOKEN':
        if user[2]==0:
            DB.hintTOKEN(user[0])
            bot.send_message(message.from_user.id,f'''Поздравляю! Вы нашли {user[2]+user[3]+user[4]+user[5]+user[6]+user[7]+user[8]+1} подсказок из 7 и узнали больше о ...(Deleted)...''',disable_web_page_preview=True , parse_mode = 'HTML')
        else:
            bot.send_message(message.from_user.id,f'''Упс, вы уже вводили эту подсказку! Скорее ищите остальные у стендов продуктов и вводите сюда, всего их 7, а у вас пока только {user[2]+user[3]+user[4]+user[5]+user[6]+user[7]+user[8]}.
''',disable_web_page_preview=True , parse_mode = 'HTML')
    elif hint=='SPACE':
        if user[3]==0:
            DB.hintSPACE(user[0])
            bot.send_message(message.from_user.id,f'''Поздравляю! Вы нашли {user[2]+user[3]+user[4]+user[5]+user[6]+user[7]+user[8]+1} подсказок из 7 и узнали больше об ...(Deleted)...''',disable_web_page_preview=True , parse_mode = 'HTML')
        else:
            bot.send_message(message.from_user.id,f'''Упс, вы уже вводили эту подсказку! Скорее ищите остальные у стендов продуктов и вводите сюда, всего их 7, а у вас пока только {user[2]+user[3]+user[4]+user[5]+user[6]+user[7]+user[8]}.
''',disable_web_page_preview=True , parse_mode = 'HTML')
    elif hint=='LEARN':
        if user[4]==0:
            DB.hintLEARN(user[0])
            bot.send_message(message.from_user.id,f'''Поздравляю! Вы нашли {user[2]+user[3]+user[4]+user[5]+user[6]+user[7]+user[8]+1} подсказок из 7 и узнали больше о ...(Deleted)...''',disable_web_page_preview=True , parse_mode = 'HTML')
        else:
            bot.send_message(message.from_user.id,f'''Упс, вы уже вводили эту подсказку! Скорее ищите остальные у стендов продуктов и вводите сюда, всего их 7, а у вас пока только {user[2]+user[3]+user[4]+user[5]+user[6]+user[7]+user[8]}.
''',disable_web_page_preview=True , parse_mode = 'HTML')
    elif hint=='WALLET':
        if user[5]==0:
            DB.hintWALLET(user[0])
            bot.send_message(message.from_user.id,f'''Поздравляю! Вы нашли {user[2]+user[3]+user[4]+user[5]+user[6]+user[7]+user[8]+1} подсказок из 7 и узнали больше о ...(Deleted)...''',disable_web_page_preview=True , parse_mode = 'HTML')
        else:
            bot.send_message(message.from_user.id,f'''Упс, вы уже вводили эту подсказку! Скорее ищите остальные у стендов продуктов и вводите сюда, всего их 7, а у вас пока только {user[2]+user[3]+user[4]+user[5]+user[6]+user[7]+user[8]}.
''',disable_web_page_preview=True , parse_mode = 'HTML')
    elif hint=='TRADE':
        if user[6]==0:
            DB.hintTRADE(user[0])
            bot.send_message(message.from_user.id,f'''Поздравляю! Вы нашли {user[2]+user[3]+user[4]+user[5]+user[6]+user[7]+user[8]+1} подсказок из 7 и узнали больше о ...(Deleted)... ''',disable_web_page_preview=True , parse_mode = 'HTML')
        else:
            bot.send_message(message.from_user.id,f'''Упс, вы уже вводили эту подсказку! Скорее ищите остальные у стендов продуктов и вводите сюда, всего их 7, а у вас пока только {user[2]+user[3]+user[4]+user[5]+user[6]+user[7]+user[8]}.
''',disable_web_page_preview=True , parse_mode = 'HTML')
    elif hint=='HOLD':
        if user[7]==0:
            DB.hintHOLD(user[0])
            bot.send_message(message.from_user.id,f'''Поздравляю! Вы нашли {user[2]+user[3]+user[4]+user[5]+user[6]+user[7]+user[8]+1} подсказок из 7 и узнали больше о ...(Deleted)...''',disable_web_page_preview=True , parse_mode = 'HTML')
        else:
            bot.send_message(message.from_user.id,f'''Упс, вы уже вводили эту подсказку! Скорее ищите остальные у стендов продуктов и вводите сюда, всего их 7, а у вас пока только {user[2]+user[3]+user[4]+user[5]+user[6]+user[7]+user[8]}.
''',disable_web_page_preview=True , parse_mode = 'HTML')
    elif hint=='SWAP':
        if user[8]==0:
            DB.hintSWAP(user[0])
            bot.send_message(message.from_user.id,f'''Поздравляю! Вы нашли {user[2]+user[3]+user[4]+user[5]+user[6]+user[7]+user[8]+1} подсказок из 7 и узнали больше о ...(Deleted)...''',disable_web_page_preview=True , parse_mode = 'HTML')
        else:
            bot.send_message(message.from_user.id,f'''Упс, вы уже вводили эту подсказку! Скорее ищите остальные у стендов продуктов и вводите сюда, всего их 7, а у вас пока только {user[2]+user[3]+user[4]+user[5]+user[6]+user[7]+user[8]}.
''',disable_web_page_preview=True , parse_mode = 'HTML')
    else:
        bot.send_message(message.from_user.id,'''Увы, такой подсказки нет! Убедитесь, что вы верно написали слово – так, как оно представлено на модели.''')
    user = DB.get_userFromQuestLogById(message.from_user.id)
    if user[2]+user[3]+user[4]+user[5]+user[6]+user[7]+user[8]==7:
        DB.add_complete(user[0])
        user = DB.get_userFromQuestCompleteById(message.from_user.id)
        bot.send_message(message.from_user.id,f'''Поздравляю, вы собрали все подсказки и прошли AR-квест ...(Deleted)...!  Ваш индивидуальный номер: <b>{user[-1]}</b>

В конце второй официальной части будет проведен розыгрыш подарков от ...(Deleted)... с помощью генератора случайных чисел. Если ведущий назовет ваш номер, покажите ему это сообщение и получите подарок! 

Спасибо за активное участие в квесте, отличного вечера! 
''',disable_web_page_preview=True , parse_mode = 'HTML',reply_markup=keyboardremove)
    else:
        bot.send_message(message.from_user.id,f'''Продолжайте выполнять квест.
''',disable_web_page_preview=True , parse_mode = 'HTML',reply_markup=markupforquest)


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.from_user.id,'''...(Deleted)...
''',disable_web_page_preview=True , parse_mode = 'HTML')
    
@bot.message_handler(commands=['event'])
def event(message):
    bot.send_message(message.from_user.id,'''...(Deleted)...
''',disable_web_page_preview=True, parse_mode = 'HTML',reply_markup=markupforstep4)

@bot.message_handler(commands=['exportDB'],func=lambda message: message.chat.id in Admins_ids)
def exportDB(message):
    DB.export(bot,message.chat.id)

@bot.message_handler(commands=['add_admin'],func=lambda message: message.chat.id in Admins_ids)
def hearAdmin(message):
    msg = bot.send_message(message.chat.id, 'Введите информацию об админе: ID и username через пробел. username без знака @.')
    bot.register_next_step_handler(msg, addAdminToBase)
def addAdminToBase(message):
    try:
        ID, username = message.text.split()
    except Exception:
        bot.send_message(message.from_user.id,'Проверьте правильность вводимой информации')
    DB.add_admin(ID,username)
    if int(ID) not in Admins_ids:
        Admins_ids.append(int(ID))
    bot.send_message(message.from_user.id,'Админ успешно добавлен')
    try:
        bot.send_message(ID,'Вы добавлены администратором.')
    except Exception:
        bot.send_message(message.from_user.id,'Не удалось оповестить админа.')

@bot.message_handler(commands=['delete_admin'],func=lambda message: message.chat.id in Admins_ids)
def hearDelAdmin(message):
    msg = bot.send_message(message.chat.id, 'Введите информацию об админе: ID.')
    bot.register_next_step_handler(msg, delAdmin)
def delAdmin(message):
    try:
        DB.delete_admin(message.text)
        Admins_ids.remove(int(message.text))
        bot.send_message(message.from_user.id,'Админ успешно удален')
    except Exception:
        bot.send_message(message.from_user.id,'Не удалось удалить админа')

@bot.message_handler(commands=['send_all'],func=lambda message: message.chat.id in Admins_ids)
def checkMessageAll(message):
    msg = bot.send_message(message.chat.id, 'Напишите сообщение, которое нужно отправить всем пользователям. Напишите "отмена", если вы передумали отправлять сообщение.')
    bot.register_next_step_handler(msg, hearMessageAll)
def hearMessageAll(message):
    if message.text != 'отмена':
        try:
            users = DB.get_users()
            for line in users:
                try:
                    bot.copy_message(line[0],message.chat.id,message.message_id)
                except Exception:
                    continue
        except Exception:
            bot.send_message(message.from_user.id,'Не удалось выполнить отправку')
        else:
            bot.send_message(message.from_user.id,'Отправка завершена')
    else:
        bot.send_message(message.from_user.id,text='Рассылка отменена.')

@bot.message_handler(commands=['change_ind_num'],func=lambda message: message.chat.id in Admins_ids)
def checkMessageIND(message):
    msg = bot.send_message(message.chat.id, 'Напишите id пользователя, которому нужно поменять индивидуальный номер и через пробел номер')
    bot.register_next_step_handler(msg, hearMessageIND)
def hearMessageIND(message):
    if message.text != 'отмена':
        try:
            DB.changeUsersIndNum(message)
        except Exception:
            bot.send_message(message.from_user.id,'Не удалось изменить номер')
    else:
        bot.send_message(message.from_user.id,text='Отменено.')

@bot.message_handler(commands=['send_registrated'],func=lambda message: message.chat.id in Admins_ids)
def checkMessageRegistrated(message):
    msg = bot.send_message(message.chat.id, 'Напишите сообщение, которое нужно отправить зарегистрированным пользователям. Напишите "отмена", если вы передумали отправлять сообщение.')
    bot.register_next_step_handler(msg, hearMessageRegistrated)
def hearMessageRegistrated(message):
    if message.text != 'отмена':
        try:
            users = DB.get_registrated()
            for line in users:
                try:
                    bot.copy_message(line[0],message.chat.id,message.message_id)
                except Exception:
                    continue
        except Exception:
            bot.send_message(message.from_user.id,'Не удалось выполнить отправку')
        else:
            bot.send_message(message.from_user.id,'Отправка завершена')
    else:
        bot.send_message(message.from_user.id,text='Рассылка отменена.')

@bot.message_handler(commands=['start_quest'],func=lambda message: message.chat.id in Admins_ids)
def start_quest(message):
    try:
        users = DB.get_registrated()
        for line in users:
            try:
                bot.send_message(line[0],'''Уважаемый пользователь! С этого момента вы можете принять участие в AR-квесте от ...(Deleted)...! Скорее жмите на кнопку ниже:
''',disable_web_page_preview=True, parse_mode = 'HTML',reply_markup=markupforstart)
            except Exception:
                continue
    except Exception:
        bot.send_message(message.from_user.id,'Не удалось выполнить отправку')

@bot.message_handler(commands=['send_user'],func=lambda message: message.chat.id in Admins_ids)
def checkMessageUser(message):
    msg = bot.send_message(message.chat.id, 'Напишите через пробел id пользователей, которым нужно отправить сообщение.')
    bot.register_next_step_handler(msg, hearMessageIds)
def hearMessageIds(message):
    global userIds
    userIds = message.text.split()
    msg = bot.send_message(message.chat.id, 'Напишите сообщение, которое нужно отправить всем указанным пользователям. Напишите "отмена", если вы передумали отправлять сообщение.')
    bot.register_next_step_handler(msg, hearMessageUser)
def hearMessageUser(message):
    global userIds
    if message.text != 'отмена':
        try:
            for id in userIds:
                user = DB.get_userById(id)
                try:
                    bot.copy_message(user[0],message.chat.id,message.message_id)
                    bot.send_message(message.from_user.id,f'Сообщение отправлено пользователю с id={user[0]}')
                except Exception:
                    bot.send_message(message.from_user.id,f'Не удалось выполнить отправку пользователю с id={user[0]}')
        except Exception:
            bot.send_message(message.from_user.id,'Не выполнить отправку, проверьте вводимые id.')
    else:
        bot.send_message(message.from_user.id,text='Рассылка отменена.')

@bot.message_handler(commands=['delete_from_registrated'],func=lambda message: message.chat.id in Admins_ids)
def hearDelRegistrated(message):
    msg = bot.send_message(message.chat.id, 'Введите информацию об пользователе: ID.')
    bot.register_next_step_handler(msg, delRegistrated)
def delRegistrated(message):
    try:
        DB.delete_user_from_registrated(message.text)
        bot.send_message(message.from_user.id,'Пользователь успешно исключен из зарегистрированных')
    except Exception:
        bot.send_message(message.from_user.id,'Не удалось удалить пользователя из зарегистрированных')

@bot.message_handler(commands=['clearDB'],func=lambda message: message.chat.id in Admins_ids)
def clearDB(message):
    msg = bot.send_message(message.chat.id, 'Вы уверены в том, что хотите очистить базу данных под 0? Данное действие необратимо. Советую сделать выгрузку пользователей перед очисткой.\nЕсли вы уверены, то введите пароль админа.')
    bot.register_next_step_handler(msg, checkPassDB)
def checkPassDB(message):
    if message.text == cg.password:
        DB.removeDB()
        bot.send_message(message.chat.id,'База данных очищена')
    else: 
        bot.send_message(message.chat.id,'Неверный пароль')

@bot.message_handler(commands=['remakeRegistrated'],func=lambda message: message.chat.id in Admins_ids)
def remakeReg(message):
    msg = bot.send_message(message.chat.id, 'Вы уверены в том, что хотите пересоздать таблицу? Данное действие необратимо. Советую сделать выгрузку пользователей перед очисткой.\nЕсли вы уверены, то введите пароль админа.')
    bot.register_next_step_handler(msg, remakeRegcheck)
def remakeRegcheck(message):
    if message.text == cg.password:
        DB.remakeRegistrated()
        bot.send_message(message.chat.id,'Таблица пересоздана')
    else: 
        bot.send_message(message.chat.id,'Неверный пароль')

@bot.message_handler(content_types=['text'])
def hearAdmin(message):
    if message.text == 'ВВЕСТИ AR-ПОДСКАЗКУ':
        ARhint(message.from_user.id)
    else:
        for adminID in Admins_ids:
            try:
                bot.forward_message(adminID,message.from_user.id,message.message_id)
                bot.send_message(adminID,f'ID пользователя - {message.from_user.id}')
            except Exception:
                bot.send_message(cg.adminId,'ошибка')

bot.polling(none_stop=True)
