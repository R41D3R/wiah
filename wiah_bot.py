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
    fb = fc.FritzHosts( password = fritzpw )
    message = "Connected devices:"
    for device in fb.get_hosts_info():
        if device['status'] == "1":

            ip = device['ip']
            if (ip == None): ip = "None"

            message = message + '\n{} ({})'.format(device['name'], ip)
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
        print("home recieved")
        if str(chat_id) in authusers_list:
            bot.sendMessage(chat_id, "This takes a second.")
            bot.sendMessage(chat_id=chat_id, text=getDevices(), parse_mode='markdown')
    elif command == '/log':
        if str(chat_id) in authusers_list:
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

botkey_file = open("botkey.txt")
botkey = botkey_file.read()
print(botkey)
bot = telepot.Bot(botkey)


authusers = open("users.txt")
authusers_list = authusers.read().splitlines()
print(len(authusers_list))
print(authusers_list[1])
print(authusers_list[0])

fritzbox_pw_file = open("fritzbox_pw.txt")
fritzpw = fritzbox_pw_file.read()
print(fritzpw)

MessageLoop(bot, handle).run_as_thread()
print('********************************************')
print('* Who_is_at_home_bot erfolgreich gestartet *')
print('********************************************')


while 1:
    time.sleep(10)
