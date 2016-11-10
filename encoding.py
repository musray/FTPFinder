#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, re, shutil, shelve 
import urllib.parse
import ftplib, ftputil

def getList():
    protocol = 'ftp://'
    server = '172.21.200.32'
    user   = 'churui@ctecdcs.net'
    password = '`1234qwert'
    # userMatch = re.compile(r'(\w\d)+@')
    urls = [r'/01.项目文件/00.CPR1000项目/00.CPR1000 PROJECT A/00_收发文件/SDM-ANE/000001-099999']

    with ftputil.FTPHost(server, user, password) as host:
        with open('result.txt', 'w') as f:
            for url in urls:
                # catagory = catagories[key]
                # print(type(url.encode('gbk').decode('latin1')))
                files = host.listdir(url.encode('gbk'))

                for file in files:
                    # print(file)
                    fileName = file.decode('gbk')
                    try:
                        # code, ver, title = parser(fileName)
                        fullUrl = host.path.join(protocol, server, url.strip('/'), fileName)
                        # f.write(file + ',' + urllib.parse.quote(fullUrl, safe='/:', encoding='gbk') + '\n')
                        f.write(fileName + ',' + urllib.parse.quote(fullUrl, safe='/:', encoding='gbk') + '\n')

                    except TypeError as e:
                        print(e)
                    # finally:
                    #     f.write(file + '\n');
                        

    # TODO: What will happen if the server is not reachable?
    # TODO: What will happen if the user is not exist? or the password is not correct?

getList()
