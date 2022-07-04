'''
data.sql
- table data (id prikey autoincr int, time int, address text, nickname text, message text)
- table user (id prikey autoincr int, address text, grp text)
'''
import sqlite3, datetime
DATABASE = 'data.sql'
def init() -> None:
    d = sqlite3.connect(DATABASE)
    c = d.cursor()
    c.execute('create table if not exists data(id integer primary key autoincrement not null, time int not null, address text not null, nickname text not null, message text not null);')
    c.execute('create table if not exists user(id integer primary key autoincrement not null, address text not null, grp text not null);')
    d.commit()
    c.close()
    d.close()
def insertMessage(timestamp: int, address: str, nickname: str, message: str) -> None:
    '''
    insert a msg into the database
    '''
    d = sqlite3.connect(DATABASE)
    c = d.cursor()
    c.execute('insert into data(time, address, nickname, message) values(%d, \'%s\', \'%s\', \'%s\');' % (timestamp, address, nickname, message))
    d.commit()
    c.close()
    d.close()
def getMessage(timestamp: int, count: int) -> list:
    '''
    get [count] message(s) before the time from the database
    '''
    d = sqlite3.connect(DATABASE)
    c = d.cursor()
    c.execute('select * from data where time <= %d order by time desc limit %d;' % (timestamp, count))
    res = c.fetchall()
    c.close()
    d.close()
    return res
def queryGroup(ip: str) -> list:
    '''
    get user group
    '''
    d = sqlite3.connect(DATABASE)
    c = d.cursor()
    c.execute('select grp from user where address = \'%s\';' % ip)
    raw = c.fetchall()[0][0]
    raw = raw.split('|')
    c.close()
    d.close()
    return raw