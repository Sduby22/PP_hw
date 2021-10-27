from random import randint
import sqlite3
import names

SIZE=1000

conn = sqlite3.connect('./random_users.db')
cursor = conn.cursor()
with open('DDL.sql', 'r', encoding='utf8') as f:
    script = f.read()
cursor.executescript(script)
cursor.execute('delete from users')

for x in range(SIZE):
    name = names.get_full_name()
    number = '1' + str(randint(3300000000, 9999999999))
    balance = randint(-100, 1000)
    cursor.execute('insert into users values(?,?,?)', (name, number, balance))

conn.commit()
