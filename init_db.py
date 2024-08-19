#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os
import sqlite3
import tomllib

CONFIG_FILE = "config.toml"
DB_FILE = "blog.db"

if not os.path.exists(CONFIG_FILE):
    print("Unable to find config file.")
    print("Failed to create database.")
    exit(1)
if not os.path.exists(DB_FILE):
    print("No database file found, creating database...")
    config = tomllib.loads(open(CONFIG_FILE, "r").read())
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    print("Initializing admin config......")
    c.execute(
        """CREATE TABLE admin_config 
             (username text NOT NULL PRIMARY KEY, password text NOT NULL, token text);"""
    )
    c.execute(
        """INSERT INTO admin_config VALUES (\"%s\", \"%s\", "token");"""
        % (
            config["admin"]["username"],
            hashlib.md5("admin".encode("utf-8")).hexdigest(),
        )
    )

    print("Initializing articles table...")
    c.execute(
        """CREATE TABLE articles 
             (id integer NOT NULL PRIMARY KEY autoincrement, title text NOT NULL, content text NOT NULL, tag text NOT NULL, datetime text NOT NULL);"""
    )
    c.execute("CREATE UNIQUE INDEX articles_id ON articles(id);")
    c.execute(
        """CREATE TABLE pages 
             (id integer NOT NULL PRIMARY KEY, title text NOT NULL, content text NOT NULL);"""
    )

    print("Initializing tags table...")
    c.execute(
        """CREATE TABLE tags 
             (id integer NOT NULL PRIMARY KEY autoincrement, name text NOT NULL, article_id integer NOT NULL);"""
    )

    conn.commit()
    conn.close()
    print("Database created successfully.")
else:
    print("Skip creating database due to existing database file.")
