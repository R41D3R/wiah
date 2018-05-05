import sqlite3
import fritzconnection as fc
import datetime

fb = fc.FritzHosts(password='losen9842')

db = sqlite3.connect('fritzbox.db')

cursor = db.cursor()

#Tabellen löschen
#cursor.execute("DROP TABLE devices")
#cursor.execute("DROP TABLE status")
#db.commit

# Gerätetabelle
devices_sql = """
CREATE TABLE IF NOT EXISTS devices (
    mac text,
    name text PRIMARY KEY,
    ip text,
    status text)"""
# Statustabelle
status_sql = """
CREATE TABLE IF NOT EXISTS status (
    name text,
    datetime text,
    status text)"""

cursor.execute(devices_sql)
cursor.execute(status_sql)
db.commit()

#bekannte Geräte auslesen
known_devices_sql = "SELECT name FROM devices"
cursor.execute(known_devices_sql)
known_devices = cursor.fetchall()

status_of_devices_sql = "SELECT name, status FROM devices"
cursor.execute(status_of_devices_sql)
fetch_devices = dict(cursor.fetchall())


date = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#Fritzboxabfrage und Daten eintragen
for device in fb.get_hosts_info():
    #Neues Gerät hinzufügen
    if device['name'] not in known_devices:
        cursor.execute("INSERT OR REPLACE INTO devices(mac, name, ip, status) VALUES (?,?,?,?)", (device['mac'], device['name'], device['ip'], device['status']))

    if fetch_devices.get(device['name']) != device['status']:
        cursor.execute("UPDATE devices SET status = ? WHERE name = ?", (device['status'], device['name']))
        cursor.execute("INSERT INTO status(name, datetime, status) VALUES (?,?,?)", (device['name'], date, device['status']))


    #Daten in Status eintragen
    #cursor.execute("INSERT INTO status(name, datetime, status) VALUES (?,?,?)", (device['name'], date, device['status']))
db.commit()

"""
#Daten auslesen zum Tets
devicedaten = "SELECT * FROM devices"
cursor.execute(devicedaten)
rows = cursor.fetchall()
for row in rows:
    print(row)

statusdaten = "SELECT * FROM status"
cursor.execute(statusdaten)
jensen = cursor.fetchall()
for row in jensen:
    print(row)
"""




db.close()
