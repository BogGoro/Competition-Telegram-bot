import sqlite3
import config as cg
import middleware
def DB_init():
    global conn
    global crsr
    conn = sqlite3.connect('Event_users.db',check_same_thread=False)
    crsr = conn.cursor()
    crsr.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INT PRIMARY KEY,
        username TEXT
    )""")
    conn.commit()
    crsr.execute("""CREATE TABLE IF NOT EXISTS registratedUsers(
        user_id INT PRIMARY KEY,
        username TEXT,
        number TEXT,
        surname TEXT,
        name TEXT
    )""")
    conn.commit()
    crsr.execute("""CREATE TABLE IF NOT EXISTS questlog(
        user_id INT PRIMARY KEY,
        individual_number INT,
        TOKEN INT,
        SPACE INT,
        LEARN INT,
        WALLET INT,
        TRADE INT,
        HOLD INT,
        SWAP INT
    )""")
    conn.commit()
    crsr.execute("""CREATE TABLE IF NOT EXISTS questComplete(
        user_id INT PRIMARY KEY,
        username TEXT,
        number TEXT,
        surname TEXT,
        name TEXT,
        individual_number INT
    )""")
    conn.commit()
    crsr.execute("""CREATE TABLE IF NOT EXISTS admins(
        admin_id INT PRIMARY KEY,
        username TEXT
    )""")
    conn.commit()
    
    crsr.execute("""
    SELECT * from admins
    """)
    info=crsr.fetchone()
    if info is None:
        crsr.execute(""" INSERT INTO admins VALUES(?,?)""",(cg.adminId,cg.adminUsername))
    conn.commit()
    return

def export(bot, chat):
#Команда экспорта БД
    try:
      info = crsr.execute('SELECT * FROM users')
    except Exception:
      bot.send_message(chat, 'Возникла ошибка')
    info = crsr.fetchall()
    titles= [x[1] for x in crsr.execute('PRAGMA table_info(users);').fetchall()]
    bot.send_document(chat,middleware.data_to_file(info,'users',titles))
    
    info = crsr.execute('SELECT * FROM registratedUsers').fetchall()
    titles= [x[1] for x in crsr.execute('PRAGMA table_info(registratedUsers);').fetchall()]
    bot.send_document(chat,middleware.data_to_file(info,'registratedUsers',titles))

    info = crsr.execute('SELECT * FROM questComplete').fetchall()
    titles= [x[1] for x in crsr.execute('PRAGMA table_info(questComplete);').fetchall()]
    bot.send_document(chat,middleware.data_to_file(info,'questComplete',titles))

def exportQuestLog(bot, chat):
  info = crsr.execute('SELECT * FROM questlog').fetchall()
  titles= [x[1] for x in crsr.execute('PRAGMA table_info(questlog);').fetchall()]
  bot.send_document(chat,middleware.data_to_file(info,'questlog',titles))

def changeUsersIndNum(message):
  crsr = conn.cursor()
  try:
    id,num=map(int,message.text.split())
    crsr.execute("UPDATE questComplete SET individual_number=? WHERE user_id=?", (num,id))
    conn.commit()
  except Exception:
    id,num=1,2
  

def add_user(message):
  info=crsr.execute('SELECT * FROM users WHERE user_id = ?' , (message.from_user.id,))
  data_BD=info.fetchone()
  if data_BD is None:
    sqlreqst="""INSERT INTO users (user_id,username) VALUES(?,?)"""
    user_data=(message.from_user.id, message.from_user.username)
    crsr.execute(sqlreqst,user_data)
  conn.commit()

def add_admin(id,username):
  info=crsr.execute('SELECT * FROM admins WHERE admin_id = ?' , (id,))
  data_BD=info.fetchone()
  if data_BD is None:
    sqlreqst="""INSERT INTO admins (admin_id, username) VALUES(?,?)"""
    user_data=(id, username)
    crsr.execute(sqlreqst,user_data)
  conn.commit()

def add_registrated(id,username,number):
  info=crsr.execute('SELECT * FROM registratedUsers WHERE user_id = ?' , (id,))
  data_BD=info.fetchone()
  if data_BD is None:
    sqlreqst="""INSERT INTO registratedUsers (user_id, username, number) VALUES(?,?,?)"""
    user_data=(id, username, number)
    crsr.execute(sqlreqst,user_data)
  conn.commit()

def add_quest(id):
  info=crsr.execute('SELECT * FROM questlog WHERE user_id = ?' , (id,))
  data_BD=info.fetchone()
  if data_BD is None:
    quest = get_questlog()
    sqlreqst="""INSERT INTO questlog (user_id, individual_number, TOKEN, SPACE, LEARN, WALLET, TRADE, HOLD, SWAP) VALUES(?,?, 0, 0, 0, 0, 0, 0, 0)"""
    try:
      user_data=(id, quest[-1][1]+1)
    except Exception:
      user_data=(id, 1)
    crsr.execute(sqlreqst,user_data)
  conn.commit()

def add_complete(id):
  info=crsr.execute('SELECT * FROM questComplete WHERE user_id = ?' , (id,))
  data_BD=info.fetchone()
  if data_BD is None:
    userlog = get_QuestComplete()
    user = get_userFromRegistrated(id)
    sqlreqst="""INSERT INTO questComplete (user_id, username, number, surname, name, individual_number) VALUES(?,?,?,?,?,?)"""
    try:
      user_data=(id, user[1], user[2], user[3], user[4], userlog[-1][-1]+1)
    except Exception:
      user_data=(id, user[1], user[2], user[3], user[4], 1)
    crsr.execute(sqlreqst,user_data)
  conn.commit()

def add_surname(id,message):
  crsr = conn.cursor()
  crsr.execute("UPDATE registratedUsers SET surname=? WHERE user_id=?", (message.text,id))
  conn.commit()

def add_name(id,message):
  crsr = conn.cursor()
  crsr.execute("UPDATE registratedUsers SET name=? WHERE user_id=?", (message.text,id))
  conn.commit()

def hintTOKEN(id):
  crsr = conn.cursor()
  crsr.execute("UPDATE questlog SET TOKEN=? WHERE user_id=?", (1,id))
  conn.commit()

def hintSPACE(id):
  crsr = conn.cursor()
  crsr.execute("UPDATE questlog SET SPACE=? WHERE user_id=?", (1,id))
  conn.commit()

def hintLEARN(id):
  crsr = conn.cursor()
  crsr.execute("UPDATE questlog SET LEARN=? WHERE user_id=?", (1,id))
  conn.commit()

def hintWALLET(id):
  crsr = conn.cursor()
  crsr.execute("UPDATE questlog SET WALLET=? WHERE user_id=?", (1,id))
  conn.commit()

def hintTRADE(id):
  crsr = conn.cursor()
  crsr.execute("UPDATE questlog SET TRADE=? WHERE user_id=?", (1,id))
  conn.commit()

def hintHOLD(id):
  crsr = conn.cursor()
  crsr.execute("UPDATE questlog SET HOLD=? WHERE user_id=?", (1,id))
  conn.commit()

def hintSWAP(id):
  crsr = conn.cursor()
  crsr.execute("UPDATE questlog SET SWAP=? WHERE user_id=?", (1,id))
  conn.commit()

def get_registrated():
  info=crsr.execute('SELECT * FROM registratedUsers')
  return info.fetchall()

def get_admins():
  info=crsr.execute('SELECT * FROM admins')
  return info.fetchall()

def get_users():
  info=crsr.execute('SELECT * FROM users')
  return info.fetchall()

def get_questlog():
  info=crsr.execute('SELECT * FROM questlog')
  return info.fetchall()

def get_userById(id):
  info=crsr.execute('SELECT * FROM users where user_id=?',(id,))
  return info.fetchone()

def get_userFromQuestLogById(id):
  info=crsr.execute('SELECT * FROM questlog where user_id=?',(id,))
  return info.fetchone()

def get_userFromQuestCompleteById(id):
  info=crsr.execute('SELECT * FROM questComplete where user_id=?',(id,))
  return info.fetchone()

def get_QuestComplete():
  info=crsr.execute('SELECT * FROM questComplete')
  return info.fetchone()

def get_userFromRegistrated(id):
  info=crsr.execute('SELECT * FROM registratedUsers where user_id=?',(id,))
  return info.fetchone()

def delete_admin(id):
  info=crsr.execute('DELETE FROM admins WHERE admin_id = ?' , (id,))
  conn.commit()

def delete_user_from_registrated(id):
  info=crsr.execute('DELETE FROM registratedUsers WHERE user_id = ?' , (id,))
  conn.commit()

def remakeRegistrated():
  crsr = conn.cursor()
  crsr.execute('DROP TABLE IF EXISTS registratedUsers')
  crsr.execute("""CREATE TABLE IF NOT EXISTS registratedUsers(
    user_id INT PRIMARY KEY,
    username TEXT,
    number TEXT,
    surname TEXT,
    name TEXT
  )""")
  conn.commit()

def removeDB():
  import os
  conn.close()
  os.remove('Event_users.db')
  DB_init()