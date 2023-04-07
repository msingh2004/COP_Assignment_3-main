import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

with open('postvalues.csv','r') as file:
    postcount = 0
    # cur.execute("INSERT INTO posts VALUES (?,?,?,?,?,?,?)",file[0].split(","))
    for row in file:
        cur.execute("INSERT INTO posts VALUES (?,?,?,?,?,?,?)",row.split(",")[0:7])
        connection.commit()
        postcount+=1

with open('uservalues.csv','r') as file:
    usercount = 0
    for row in file:
        cur.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?)",row.split(",")[0:7])
        connection.commit()
        usercount+=1
    

# cur.execute("INSERT INTO posts (id, title, content) VALUES (?, ?, ?)", 
            # ('1', 'First', 'Neil'))

# cur.execute("INSERT INTO posts (id, title, content) VALUES (?, ?, ?)",
            # ('2', 'Second Post', 'Buzz Aldrin'))

# cur.execute("INSERT INTO comments (comment_id, post_id, content) VALUES (?, ?, ?)",
            # ('1', '1', 'I\'ll be fucked up if you can\'t be right here'))

connection.commit()
connection.close()
