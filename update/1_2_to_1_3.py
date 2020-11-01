import sqlite3

try:
    conn = sqlite3.connect('faka.sqlite3')
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE trade ADD COLUMN out_trade_no text")
    conn.commit()
    conn.close()
except Exception as e:
    print(e)
    if 'duplicate column name' in str(e):
        print('您已经执行过此脚本，无需再次执行')
