import datetime

from tools import *

db = Connection("blog.db")

def get_article(id):
    article = db.get("SELECT * FROM articles WHERE id = ?;", id)
    return article

def get_article_by_category(category_name):
    articles = db.get("SELECT articles_id FROM category WHERE name = ?;", category_name)
    return articles

def update_article(id, **kwargs):
    sql = '''UPDATE articles SET title=?, content=?, category=?, WHERE id=?;'''
    db.execute(sql, kwargs["title"], kwargs["content"], kwargs["category"], id)
    return True

def creat_article(**kwargs):
    today = datetime.date.today()
    sql = '''INSERT INTO article (title, content, category) VALUES (?,?,?,?);'''
    article_id = db.execute(sql, kwargs["title"], kwargs["content"], kwargs["category"], today)
    return article_id

def creat_category(name):
    category_id = db.execute('''INSERT INTO category (name) VALUES (?);''', name)
    return category_id


def delete_article(id):
    db.execute("DELETE FROM articles WHERE id=?;", id)
    db.execute("DELETE FROM category WHERE articles_id=?;", id)
    return True

def delete_category(category_name):
    db.execute("DELETE FROM category WHERE id=?;", category_name)
    return True
