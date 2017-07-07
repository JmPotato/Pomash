#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import string
import random
import dropbox
import hashlib
import pygments
import datetime

def to_md5(word):
    return hashlib.md5(word).hexdigest()

def make_token(username):
    key = ''.join(random.sample(string.letters+string.digits, 20))
    return key

def get_datetime():
    return str(datetime.datetime.now()).split('.')[0]

def backup(dbx, file_path, upload_path):
    path = '/' + upload_path
    mode = dropbox.files.WriteMode.overwrite
    mtime = os.path.getmtime(file_path)
    with open(file_path, 'rb') as f:
        data = f.read()
    try:
        res = dbx.files_upload(
            data, path, mode,
            client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
            mute=True)
    except dropbox.exceptions.ApiError as err:
        print '%s API error' % err
        return False
    return True

def restore(dbx, file_name, download_path):
    path = '/' + file_name
    try:
        res = dbx.files_download_to_file(download_path, path)
    except dropbox.exceptions.HttpError as err:
        print '%s API error' % err
        return False
    return True