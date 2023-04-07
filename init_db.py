import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (id, title, content) VALUES (?, ?, ?)", 
            ('1', 'First', 'Neil'))

cur.execute("INSERT INTO posts (id, title, content) VALUES (?, ?, ?)",
            ('2', 'Second Post', 'Buzz Aldrin'))

cur.execute("INSERT INTO comments (comment_id, post_id, content) VALUES (?, ?, ?)",
            ('1', '1', 'I\'ll be fucked up if you can\'t be right here'))

cur.execute("INSERT INTO users (username, pass_key) VALUES (?, ?)", ('Manpreet', 'Manpreet@2004'))

connection.commit()
connection.close()