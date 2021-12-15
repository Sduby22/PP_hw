from src import *
import sys
import logging
import sqlite3

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: [%(name)s] %(message)s'
)


def select_rand_number():
    conn = sqlite3.connect('data/random_users.db')
    cur = conn.cursor()
    cur.execute("SELECT number FROM users ORDER BY RANDOM() LIMIT 1")
    number = cur.fetchone()[0]
    conn.close()
    return number

def welcome():
    print(
r"""
 ___       _                           _            
|_ _|_ __ | |_ ___ _ __ _ __  _ __ ___| |_ ___ _ __ 
 | || '_ \| __/ _ \ '__| '_ \| '__/ _ \ __/ _ \ '__|
 | || | | | ||  __/ |  | |_) | | |  __/ ||  __/ |   
|___|_| |_|\__\___|_|  | .__/|_|  \___|\__\___|_|   
                       |_|                          
""")
    input("按回车从数据库中抽取一位随机用户模拟通话:")

if __name__ == '__main__':
    conf = ConfigLoader('./config.yaml')

    interpreter = Interpreter(conf)

    while True:
        welcome()
        number = select_rand_number()
        runtime = Runtime(number, conf)
        interpreter.accept(runtime)
