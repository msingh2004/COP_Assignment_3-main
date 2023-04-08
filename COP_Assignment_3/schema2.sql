DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    postId INTEGER PRIMARY KEY,
    -- created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    gender TEXT NOT NULL,
    age TEXT NOT NULL,
    topic TEXT NOT NULL,
    sign TEXT NOT NULL,
    dat TEXT NOT NULL,
    content TEXT NOT NULL
    -- id,gender,age,topic,sign,date,text
);

-- sp_configure 'show advanced options', 1;
-- RECONFIGURE;
-- GO
-- sp_configure 'ad hoc distributed queries', 1;
-- RECONFIGURE;
-- GO


-- USE ImportFromExcel;
-- GO
-- SELECT * INTO posts
-- FROM OPENDATASOURCE('Microsoft.ACE.OLEDB.12.0',
--     'Data Source=blogtext.xlsx;Extended Properties=Excel 12.0')...[Sheet1$];
-- GO

DROP TABLE IF EXISTS comments;

CREATE TABLE comments (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    post_id INTEGER NOT NULL,
    content TEXT NOT NULL
);

DROP TABLE IF EXISTS email_ids_subscriptions;

CREATE TABLE email_ids_subscriptions (
    email_id TEXT PRIMARY KEY
);

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id TEXT PRIMARY KEY DEFAULT "hahanonexistent.com",
    -- pass_key TEXT DEFAULT "BADPASS"
    screen_name TEXT,
    tags TEXT,
    avatar TEXT,
    followers_count INTEGER,
    friends_count INTEGER,
    lang TEXT
    -- id,screenName,tags,avatar,followersCount,friendsCount,lang,lastSeen,tweetId,friends
);


-- USE ImportFromExcel;
-- GO
-- INSERT INTO users (screen_name, followers_count, friends_count)
-- SELECT screen_name, followers_count, friends_count
-- FROM OPENROWSET('Microsoft.ACE.OLEDB.12.0',
--     'Excel 12.0; Database=data.xlsx', [Sheet1$]);
-- GO
