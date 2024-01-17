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
    return hashlib.md5(word.encode("utf-8")).hexdigest()


def make_token():
    key = "".join(random.sample(string.ascii_letters + string.digits, 20))
    return key


def get_datetime():
    return str(datetime.datetime.now()).split(".")[0]


def backup(dbx, file_name):
    dropbox_path = "/" + file_name
    with open(file_name, "rb") as f:
        data = f.read()
    try:
        dbx.files_upload(
            data,
            dropbox_path,
            mode=dropbox.files.WriteMode.overwrite,
            client_modified=datetime.datetime(
                *time.gmtime(os.path.getmtime(file_name))[:6]
            ),
            mute=True,
        )
    except dropbox.exceptions.ApiError as err:
        print("%s API error" % err)
        return False
    return True


def restore(dbx, file_name):
    dropbox_path = "/" + file_name
    try:
        dbx.files_download_to_file(file_name, dropbox_path)
    except dropbox.exceptions.HttpError as err:
        print("%s API error" % err)
        return False
    return True


def trim(string):
    return string.strip().lstrip()
