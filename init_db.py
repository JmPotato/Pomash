import os
import hashlib
import sqlite3

from settings import *

if not os.path.exists("blog.db"):
    conn = sqlite3.connect("blog.db")
    c = conn.cursor()
    print "Did not find any database file."
    c.execute('''CREATE TABLE admin_config
             (username text NOT NULL PRIMARY KEY, password text NOT NULL, token text);''')
    print "Creat Admin Config......"
    c.execute('''CREATE TABLE articles 
             (id integer NOT NULL PRIMARY KEY autoincrement, title text NOT NULL, content text NOT NULL, category text NOT NULL, datetime date NOT NULL);''')
    print "Creat Article Database......"
    c.execute('''CREATE TABLE category
             (id integer NOT NULL PRIMARY KEY autoincrement, name text NOT NULL, articles_id integer);''')
    print "Creat Category......"
    c.execute('''INSERT INTO admin_config VALUES (\"%s\", \"%s\", "token");''' % (login_username, hashlib.md5(login_password).hexdigest()))
    c.execute("CREATE UNIQUE INDEX articles_id ON articles(id);")
    print "Creat Articles Index......"
    c.execute("CREATE UNIQUE INDEX category_id ON category(id);")
    print "Creat Category Index......"
    conn.commit()
    conn.close()
    print "Successful to creat database file."
    print "Please move your database file to libs file!!"
else:
    print "Database File already exists."
    print "Failed to create database file."
    print "Please remove database file first."