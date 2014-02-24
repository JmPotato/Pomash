#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from tools import *
from utils import *

class DatabaseError(Exception):
    def __init__(self, content):
        Exception.__init__(self)

if os.path.exists("blog.db"):
    db = Connection("blog.db")
else:
    raise DatabaseError("Database file not found !")

def get_article(id):
    article = db.get("SELECT * FROM articles WHERE id = ?;", id)
    return article

def get_articles(page):
    articles = db.query("SELECT * FROM articles ORDER BY id DESC LIMIT ?, 3;",(page - 1) * 3)
    return articles

def get_all_articles():
    articles = db.query("SELECT * FROM articles;")
    return articles

def get_article_count():
    count = db.query('''SELECT COUNT(*) AS count FROM articles''')
    return count[0].count

def creat_article(**kwargs):
    sql = '''INSERT INTO articles (title, content, datetime) VALUES (?,?,?);'''
    article_id = db.execute(sql, kwargs["title"], kwargs["content"], get_date())
    return article_id

def update_article(id, **kwargs):
    today = datetime.date.today()
    sql = '''UPDATE articles SET title=?, content=?, datetime=? WHERE id=?;'''
    db.execute(sql, kwargs["title"], kwargs["content"], str(today), id)
    return True

def delete_article(id):
    db.execute("DELETE FROM articles WHERE id=?;", id)
    return True

def update_token(username, token):
    sql = '''UPDATE admin_config SET token=? WHERE username=?;'''
    db.execute(sql, token, username)
    return True

def verify_user(username, password_md5):
    information = db.get("SELECT * FROM admin_config WHERE username = ?;", username)
    if information.password == password_md5:
        return True
    else:
        return False

def verify_token(username, token):
    information = db.get("SELECT * FROM admin_config WHERE username = ?;", username)
    if information.token == token:
        return True
    else:
        return False

