from iMessage import bot
from time import sleep

Bot = bot(['!'])

extensions = ['defaultExtension']

for i in extensions:
    Bot.import_extension(i)


Bot.start()

sleep(120)

Bot.stop()