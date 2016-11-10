#!/usr/bin/python
# -*- coding: utf-8 -*-
'''

'''

import os, sys, re, shutil, shelve 
import urllib.parse
import ftplib, ftputil

# import logging
# logging.basicConfig(filename='log.txt', 
#         level=logging.DEBUG,
#         format='%(asctime)s - %(levelname)s - %(message)s')
# # logging.disable(logging.CRITICAL)
# logging.debug('Start of program')


def parser(string):
    '''
    Description:
    Parse the document title, then return
    document code, version and title, respectively.
    '''

    match = re.compile(r'''
        (\d{3}-\w{2}-\w{1}-.+-\d{3}|    # match the doc id using new convension 030-GN-P-BP-G11-EMD-004
        E\d{0,2}-\w\d{2}-\d{5,7})         # match the doc id using old convention E09-P13-000013
        [-_]*\s*                        # match seperation char(-, _ or space) between id and version
        ([A-Z]+_CFC|CFC_[A-Z]+)         # match version like CFC_A or A_CFC
        [-_]*\s*                        # match seperation char(-, _ or space) between ver and title
        ''', re.VERBOSE) 
    
    matchResult = match.findall(string)
    if len(matchResult) > 0:
        code = match.findall(string)[0][0]
        version = match.findall(string)[0][1]
        remains = match.sub('', string)

        if os.path.splitext(remains)[1] == '':
            title = remains.strip('\n')        # since the remains part has a trailing \n
        else:
            title = os.path.splitext(remains)[0]

        return code, version, title

def getList():
    protocol = 'ftp://'
    server = '172.21.200.32'
    user   = 'churui@ctecdcs.net'
    password = '`1234qwert'
    # userMatch = re.compile(r'(\w\d)+@')
    urls = [
            r'/01.项目文件/00.CPR1000项目/00.CPR1000 PROJECT A/00_收发文件/SDM-ANE/000001-099999'
    ]

    # catagories = {'guidelines': '操作指导', 
    #         'templates': '模板表格', 
    #         'procedures': '设计流程'}

    with ftputil.FTPHost(server, user, password) as host:
        with open('result.txt', 'w') as f:
            for url in urls:
                # catagory = catagories[key]
                files = host.listdir(url.encode('gbk'))

                for file in files:
                    fileName = file.decode('gbk')
                    try:
                        # code, ver, title = parser(fileName)
                        fullUrl = host.path.join(protocol, server, url.strip('/'), fileName)
                        f.write(fileName + ',' + urllib.parse.quote(fullUrl, safe='/:', encoding='gbk') + '\n')
                    except:
                        # print(fullUrl)
                        pass
                    # finally:
                    #     f.write(file + '\n');
                        

    # TODO: What will happen if the server is not reachable?
    # TODO: What will happen if the user is not exist? or the password is not correct?

getList()
