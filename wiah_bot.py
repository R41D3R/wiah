import telepot, time, sqlite3, datetime
from telepot.loop import MessageLoop
import fritzconnection as fc



def executeSQL(sql, data):
    db = sqlite3.connect('fritzbox.db')
    cursor = db.cursor()
    cursor.execute(sql, data)
    db.commit()
    db.close()

def fetchSQL(sql):
    db = sqlite3.connect('fritzbox.db')
    cursor = db.cursor()
    cursor.execute(sql)
    fetched = cursor.fetchall()
    db.commit()
    db.close()
    return fetched


def getDevices():
    fb = fc.FritzHosts(password='losen9842')
    message = "Connected Devices:"
    for device in fb.get_hosts_info():
        if device['status'] == "1":
            message = message + "\n" + device['name']
    return message

def saveCommand(user, command):
    executeSQL("INSERT INTO commands(user, time, command) VALUES (?,?,?)", (user, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), command))

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    #print('Got command {} from user {}'.format(command, chat_id))
    saveCommand(chat_id, command)
    if command == "/help":
        bot.sendMessage(chat_id, "/home - get a list of Devices\n/log - get the last 10 evnets")
    elif command == '/start':
        bot.sendMessage(chat_id, "Hello, this is the who_is_at_home_bot.\nCommands are:\n/help - get a list of Commands\n/home - get a list of devices\n/log - get the last 10 evnets")

    elif command == '/home':
        if chat_id == 467561553 or chat_id == 432535063:
            bot.sendMessage(chat_id, "This takes a second.")
            bot.sendMessage(chat_id, getDevices())
    elif command == '/log':
        if chat_id == 467561553 or chat_id == 432535063:
            lastten = list(fetchSQL("SELECT * from status ORDER BY datetime DESC limit 10"))
            formatted_message = "Last 10 Changes:"
            for i in lastten:
                formatted_message = formatted_message + "\n" + i[0] + " changed " + i[1] + " to " + i[2]
            bot.sendMessage(chat_id, formatted_message)
    else:
        bot.sendMessage(chat_id, "The Command : {} is unknown.".format(command))


db = sqlite3.connect('fritzbox.db')
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS commands (user text, time text, command text)")
db.commit()
db.close()


bot = telepot.Bot('583575964:AAGOrOmzpfmblckwEJH9x3CoifdcQCRhFPI')

MessageLoop(bot, handle).run_as_thread()
#print('Listening ...')


while 1:
    time.sleep(10)
