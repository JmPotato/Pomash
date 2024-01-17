#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tomllib

CONFIG_FILE = "config.toml"

with open(CONFIG_FILE, "rb") as f:
    config = tomllib.load(f)
