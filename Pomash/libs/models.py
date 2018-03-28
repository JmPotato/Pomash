#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from .tools import *
from .utils import *

class DatabaseError(Exception):
    def __init__(self, content):
        Exception.__init__(self)

if os.path.exists("blog.db"):
    db = Connection("blog.db")
else:
    raise DatabaseError("Database file not found !")

def gat_page(id):
    page = db.get("SELECT * FROM pages WHERE id = ?", id)
    return page

def get_all_pages():
    pages = db.query("SELECT * FROM pages")
    return pages

def get_article(id):
    article = db.get("SELECT * FROM articles WHERE id = ?;", id)
    return article

def get_articles(page, post_per_page):
    articles = db.query("SELECT * FROM articles ORDER BY id DESC LIMIT ?, ?;",(page - 1) * post_per_page, post_per_page)
    return articles

def get_all_articles():
    articles = db.query("SELECT * FROM articles ORDER BY id DESC;")
    return articles

def get_article_count():
    count = db.query('''SELECT COUNT(*) AS count FROM articles''')
    return count[0].count

def get_tag_articles(tag_name):
    sql = """SELECT * FROM articles AS a INNER JOIN tags AS t ON a.id = t.article_id WHERE t.name = ? ORDER BY id DESC;"""
    articles = db.query(sql, tag_name)
    return articles

def get_all_tags():
    tags = db.query("SELECT name, COUNT(name) AS num FROM tags GROUP BY name ORDER BY num DESC;")
    return tags

def creat_page(**kwargs):
    count = db.query('''SELECT COUNT(*) AS count FROM pages''')
    if count[0].count < 5: 
        sql = '''INSERT INTO pages (title, content) VALUES (?,?);'''
        id = db.execute(sql, kwargs["title"], kwargs["content"])
        return id
    else:
        return False

def update_page(id, **kwargs):
    sql = '''UPDATE pages SET title=?, content=? WHERE id=?;'''
    db.execute(sql, kwargs["title"], kwargs["content"], id)
    return True

def delete_page(id):
    db.execute("DELETE FROM pages WHERE id=?;", id)
    return True

def creat_article(**kwargs):
    sql = '''INSERT INTO articles (title, content, tag, datetime) VALUES (?,?,?,?);'''
    id = db.execute(sql, kwargs["title"], kwargs["content"], kwargs["tags"], get_datetime())
    tags = [tag.strip() for tag in kwargs["tags"].split(",")]
    for tag in tags:
        db.execute("INSERT INTO tags (name, article_id) VALUES (?,?);", tag, id)
    return id

def update_article(id, **kwargs):
    db.execute("DELETE FROM tags WHERE article_id=?;", id)
    sql = '''UPDATE articles SET title=?, content=?, tag=? WHERE id=?;'''
    db.execute(sql, kwargs["title"], kwargs["content"], kwargs["tags"], id)
    tags = [tag.strip() for tag in kwargs["tags"].split(",")]
    for tag in tags:
        db.execute("INSERT INTO tags (name, article_id) VALUES (?,?);", tag, id)
    return True

def delete_article(id):
    db.execute("DELETE FROM articles WHERE id=?;", id)
    db.execute("DELETE FROM tags WHERE article_id=?;", id)
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

def change_password(username, n_password_md5):
    sql = '''UPDATE admin_config SET password=? WHERE username=?;'''
    db.execute(sql, n_password_md5, username)
    return True