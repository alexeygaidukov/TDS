#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Инициализация сервиса
# Папка prefs.DATA_PATH должна иметь владельца пользователя и группу апача
# После создания базы reports.db этому файлу надо установить владельца - пользователя и группу апача

import sqlite3
import os
import pwd
import grp
import os.path
import sys

local_path = os.path.split(__file__)[0]
if local_path not in sys.path:
    sys.path.insert(0, local_path)

import prefs

conn = sqlite3.connect(prefs.DATA_PATH+'/templates.db')
conn.execute("PRAGMA foreign_keys=OFF;")
cur = conn.cursor()

#createNewVersion используется при получении ШМД клиентом. По ней смотрится — будет ли создаваться новая версия ШМД или заменяться старая.
cur.execute("""create table if not exists template (
    configName TEXT NOT NULL,
    configVersion TEXT NOT NULL,
    id TEXT NOT NULL,
    fileName TEXT NOT NULL,
    checkSum TEXT NOT NULL,
    typeMDCode TEXT NOT NULL,
    typeMDCodeSystem TEXT NOT NULL,
    UUIDTemplate TEXT NOT NULL,
    TemplateDesc TEXT NOT NULL,
    typeREMDCode TEXT NOT NULL,
    typeREMDCodeSystem TEXT NOT NULL,
    createNewVersion TEXT NOT NULL CHECK (createNewVersion IN ('false', 'true')),
    itsLogin TEXT NOT NULL,
    dateUploaded TEXT NOT NULL,
    UNIQUE(configName, configVersion, UUIDTemplate),
    UNIQUE(UUIDTemplate)
);""")

cur.execute("""create table if not exists session (
    uuid TEXT NOT NULL,
    tillDate INTEGER NOT NULL,
    itsTicket TEXT NOT NULL,
    itsLogin TEXT NOT NULL,
    UNIQUE(uuid)
);""")

conn.commit()

uid = pwd.getpwnam(prefs.APACHE_USER).pw_uid
gid = grp.getgrnam(prefs.APACHE_GROUP).gr_gid
os.chown(prefs.DATA_PATH+"/templates.db", uid, gid)
