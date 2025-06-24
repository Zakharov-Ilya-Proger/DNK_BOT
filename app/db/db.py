import sqlite3


async def get_data_from_db(user_id: int) -> list:
    conn = sqlite3.connect('app/user_dialogs.sqlite')
    try:
        cur = conn.cursor()
        cur.execute(f'''
        SELECT role, message
        FROM dialogs
        WHERE user_id = {user_id}
        ORDER BY id
        ''')
        data = cur.fetchall()
        if data is None:
            return [{'role':"system", 'message':'Начало Диалога!'}]
        response = [{'role':row[0], 'message':row[1]} for row in data]
        return response
    except Exception as e:
        print(e)
        return []
    finally:
        conn.close()


async def insert(user_id: int, role: str, message: str):
    conn = sqlite3.connect('app/user_dialogs.sqlite')
    try:
        cur = conn.cursor()
        cur.execute('''
        INSERT INTO dialogs (user_id, role, message)
        VALUES (?, ?, ?)
        ''', (user_id, role, message))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()
