import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (id, title, content, author) VALUES (?, ?, ?, ?)", 
            ('1', 'First', 'Neil', 'Armstrong'))

cur.execute("INSERT INTO posts (id, title, content, author) VALUES (?, ?, ?, ?)",
            ('2', 'Second Post', 'Buzz Aldrin', 'Me'))

cur.execute("INSERT INTO comments (comment_id, post_id, content, author) VALUES (?, ?, ?, ?)",
            ('1', '1', 'I\'ll be fucked up if you can\'t be right here', 'Me'))

cur.execute("INSERT INTO users (username, pass_key) VALUES (?, ?)", ('Manpreet', 'Manpreet@2004'))

connection.commit()
connection.close()