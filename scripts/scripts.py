from src import RunPy
import sqlite3

runpy = RunPy.getInstance()

@runpy.register('GetName')
def getname(number):
    conn = sqlite3.connect('data/random_users.db')
    cur = conn.cursor()
    cur = cur.execute('select name from users where number = (?)', (number,))
    res = cur.fetchone()[0]
    conn.close()
    return res

@runpy.register('GetBalance')
def getbalance(number):
    conn = sqlite3.connect('data/random_users.db')
    cur = conn.cursor()
    cur = cur.execute('select balance from users where number = (?)', (number,))
    res = cur.fetchone()[0]
    conn.close()
    return res

@runpy.register('UploadComplaint')
def uploadcomplaint(complaint):
    conn = sqlite3.connect('data/complaints.db')
    cur = conn.cursor()
    cur = cur.execute('insert into complaints values (?)', (complaint,))
    conn.commit()
    conn.close()

@runpy.register('Topup')
def topup(number):
    conn = sqlite3.connect('data/random_users.db')
    cur = conn.cursor()
    cur = cur.execute('update users set balance = balance + (?)', (int(number),))
    conn.commit()
    conn.close()
