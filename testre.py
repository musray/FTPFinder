import re, pprint, os

def parser(string):
    match = re.compile(r'''
        (\d{3}-\w{2}-\w{1}-.+-\d{3}|   # match the document id such as 030-GN-P-BP-G11-EMD-004, or 
        E\d{2}-\w\d{2}-\d{5,7})          # match the document id such as E09-P13-000013
        ([A-Z]+_CFC|CFC_[A-Z]+)          # match the version CFC_A or A_CFC 
        (\s*.+)
        ''', re.VERBOSE) 

    result = match.findall(string) 
    pprint.pprint(result)

    # return identifier, version, title

def parser(string):
    match = re.compile(r'''
        (\d{3}-\w{2}-\w{1}-.+-\d{3}|    # match the doc id using new convension 030-GN-P-BP-G11-EMD-004
        E\d{2}-\w\d{2}-\d{5,7})         # match the doc id using old convention E09-P13-000013
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

with open('result.txt', 'r') as source:
    with open('split.txt', 'w') as destination:
        testContent = source.readlines()
        for item in testContent:
            try:
                code, ver, title = parser(item)
                destination.write(code + ',' + ver + ',' + title + '\n')
            except TypeError as e:
                print(e)
                

