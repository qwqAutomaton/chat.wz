import sqlite3
import base64
db = 'data.sql'
d = sqlite3.connect(db)
c = d.cursor()
c.execute('select * from data;')
data = c.fetchall()
decode = lambda x : base64.b64decode(x.encode()).decode('utf-8')
for i in data:
    id, ip, nick, time, val = i
    print('#%d from %s (%s) at time %d:\n%s\n' % (id, decode(nick), ip, time, decode(val)))