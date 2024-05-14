<h1>Бот для регистрирации написавших ему пользователей на мероприятие и ответов на вопросы. Бот написан на python3.9 с использованием библиотеки pyTelegramBotAPI.</h1>
Для развертывания необходимо выполнить команды:

```
apt-get update
apt-get install python3
apt-get install python3-setuptools
apt-get install python3-pip
pip3 install pyTelegramBotAPI
```


Создать systemd файл с перезапуском или воспользоваться докером (как удобнее).
Содержимое systemd может быть следующим:

```
[Unit]
Description=Telegram bot 'MeetingBot'
After=syslog.target
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/usr/local/bin/bot
ExecStart=/usr/bin/python3 /usr/local/bin/bot/bot.py
RestartSec=10
Restart=always
 
[Install]
WantedBy=multi-user.target
```

Перенести файл в нужный каталог и запустить:

```
systemctl daemon-reload
systemctl enable bot
systemctl start bot
systemctl status bot
```

Для работы бота необходим config.py файл, содержащий данные:

```
TOKEN = '50000000:AAFaaaaaa-uuuuuuuuuu'  # bot token
TIMEZONE = 'Europe/Moskow'
TIMEZONE_COMMON_NAME = 'Msk'
Admins_chat = -1234567890000
password = 'password'
adminId='900000000'
adminUsername='username'
```