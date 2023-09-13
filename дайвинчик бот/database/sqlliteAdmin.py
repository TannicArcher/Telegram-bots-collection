import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('sql.db')
    cur = base.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS admins(id INT PRIMARY KEY, login Text, password Text)")
    base.commit()


def check_if_admin(id):
    cur.execute("SELECT * FROM admins WHERE id=?", (id, ))
    info = cur.fetchall()
    return info


async def add_admin(state):
    async with state.proxy() as data:
        cur.execute("INSERT OR REPLACE INTO admins VALUES(?, ?, ?)", tuple(data.values()))
        base.commit()
