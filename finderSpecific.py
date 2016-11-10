#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
负责获得五组FTP文件夹内的流程、规范和设计表格。
相应的FTP文件夹，在url变量内。
'''

import os, sys, re, shutil, shelve
import urllib.parse
import ftplib, ftputil
import logging

logging.basicConfig(filename='log.txt',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.CRITICAL)
logging.debug('Start of program')


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
    password = '4321`trewq'
    userMatch = re.compile(r'(\w\d)+@')
    urls = {
            'guidelines': '/00.部门文件/01.技术文件/00.标准化文件/04.五组标准化文件/广利核 安全级系统设计流程及规范/操作指导/',
            'templates': '/00.部门文件/01.技术文件/00.标准化文件/04.五组标准化文件/广利核 安全级系统设计流程及规范/模板表格/',
            'procedures': '/00.部门文件/01.技术文件/00.标准化文件/04.五组标准化文件/广利核 安全级系统设计流程及规范/设计规范/'
    }

    catagories = {'guidelines': '操作指导',
            'templates': '模板表格',
            'procedures': '设计流程'}

    with ftputil.FTPHost(server, user, password) as host:
        with open('result.txt', 'w') as f:
            for key in urls.keys():
                catagory = catagories[key]
                files = host.listdir(urls[key].encode('gbk').decode('latin1'))

                for file in files:
                    fileName = file.encode('latin1').decode('gbk')
                    try:
                        code, ver, title = parser(fileName)
                        fullUrl = host.path.join(protocol, server, urls[key].strip('/'), fileName)
                        print(fullUrl)
                        f.write(code + ',' + ver + ',' + title + ',' + catagory + ',' + urllib.parse.quote(fullUrl, safe='/:', encoding='gbk') + '\n')
                    except TypeError as e:
                        print(e)

    # TODO: What will happen if the server is not reachable?
    # TODO: What will happen if the user is not exist? or the password is not correct?

logging.debug('End of program')

getList()
