#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import hashlib
import sqlite3

from settings import *

if not os.path.exists("blog.db"):
    conn = sqlite3.connect("blog.db")
    c = conn.cursor()
    print("Did not find any database file.")
    c.execute('''CREATE TABLE admin_config 
             (username text NOT NULL PRIMARY KEY, password text NOT NULL, token text);''')
    print("Creat Admin Config......")
    c.execute('''CREATE TABLE articles 
             (id integer NOT NULL PRIMARY KEY autoincrement, title text NOT NULL, content text NOT NULL, tag text NOT NULL, datetime text NOT NULL);''')
    c.execute('''INSERT INTO admin_config VALUES (\"%s\", \"%s\", "token");''' % (login_username, hashlib.md5("admin").hexdigest()))
    c.execute("CREATE UNIQUE INDEX articles_id ON articles(id);")
    print("Creat Article Database......")
    c.execute('''CREATE TABLE pages 
             (id integer NOT NULL PRIMARY KEY, title text NOT NULL, content text NOT NULL);''')
    print("Creat Page Database......")
    c.execute('''CREATE TABLE tags 
             (id integer NOT NULL PRIMARY KEY autoincrement, name text NOT NULL, article_id integer NOT NULL);''')
    print("Creat Tag Database......")
    c.execute('''''')
    print("Creat Index......")
    conn.commit()
    conn.close()
    print("Successful to creat database file.")
else:
    print("Database File already exists.")
    print("Failed to create database file.")