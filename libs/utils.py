import string
import random
import hashlib
import pygments

def to_md5(word):
    return hashlib.md5(word).hexdigest()

def make_token(username):
    key = ''.join(random.sample(string.letters+string.digits, 20))
    return key
