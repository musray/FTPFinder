#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
负责获得五组FTP文件夹内的自开发工具清单。
ftp://172.21.200.32/05.二级组文件/04.工程部五组/021 设计工具/
'''

import os, sys, re, shutil, shelve 
import urllib.parse
import ftplib, ftputil
import logging

def getList():
    protocol = 'ftp://'
    server = '172.21.200.32'
    user   = 'churui@ctecdcs.net'
    password = '`1234qwert'
    userMatch = re.compile(r'(\w\d)+@')
    urls = {
            'tools': '/05.二级组文件/04.工程部五组/021 设计工具/', 
    }

    catagories = {'tools': 'tools' 
    }

    with ftputil.FTPHost(server, user, password) as host:
        with open('tools.txt', 'w') as f:
            for key in urls.keys():
                catagory = catagories[key]
                files = host.listdir(urls[key].encode('gbk').decode('latin1'))

                for file in files:
                    fileName = file.encode('latin1').decode('gbk')
                    try:
                        fullUrl = host.path.join(protocol, server, urls[key].strip('/'), fileName)
                        print(fullUrl)
                        f.write(fileName + ',' + urllib.parse.quote(fullUrl, safe='/:', encoding='gbk') + '\n')
                    except TypeError as e:
                        print(e)

    # TODO: What will happen if the server is not reachable?
    # TODO: What will happen if the user is not exist? or the password is not correct?

getList()
