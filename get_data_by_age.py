import struct
from struct import *
from collections import namedtuple
from datetime import date
import shelve
import time
import os
import itertools


f=open("small.bin","rb")
fmt = '20s 20s 70s 40s 80s 25s 3i12s 25s 50s 50s'
Result = namedtuple('Result',['fName','lName','job','company','address','phone','day','month','year','ssn','uname','email','url'])
block = '46s'
statinfo = os.stat('small.bin')
size = statinfo.st_size
recrd = f.read(struct.calcsize(fmt))
fmtCount = 405
blockCount = 46
sizeCount = fmtCount
count = 0
today = date.today()
i  = 1
R_read =0
b_read = 0

Datbaseindex = shelve.open('index.db' , 'n')

def age(year, month, day):
    age = today.year - year - ((today.month, today.day) < (month, day))
    return age

while(sizeCount < size):
    R_read += 1
    if count == 10 * i:
        i = i+1
        recrd = f.read(struct.calcsize(block))
        sizeCount = sizeCount + blockCount
    else:
        cleared_list = []
        unp = struct.unpack(fmt,recrd)
    for item in unp:
        if type(item) != int:
            cleared_list.append(item.decode('utf-8').strip('\0'))
        else:
            cleared_list.append(item)
    Birthdate = date(cleared_list[8], cleared_list[7], cleared_list[6])
    if str(Birthdate) in Datbaseindex:
        Datbaseindex["{}".format(Birthdate)].append(b_read)
    else:
        Datbaseindex["{}".format(Birthdate)] = [b_read]
    b_read+=calcsize(fmt)
    if(R_read%10==0):
        b_read+=46
    count = count + 1
    if(sizeCount >= size - 1):
        break
    else:
        recrd = f.read(struct.calcsize(fmt))
        sizeCount = sizeCount + fmtCount


Datbaseindex.close()



def ReadId(Fname):
    Databaseread = shelve.open('index.db' , 'r')
    Final = []
    for i in Databaseread:
        year  = int(i.split('-')[0])
        month = int(i.split('-')[1])
        day   = int(i.split('-')[2])
        if(age(year, month, day)<21):
            Final.append(Databaseread[i])
    Finalrows = list(itertools.chain(*Final))

    finalResult = []
    File = open(Fname,'rb')
    for offset in Finalrows:
        ResultR = []
        File.seek(offset,0)
        FileData = File.read(struct.calcsize(fmt))
        if FileData:
            Record = Result._make(unpack(fmt,FileData))
            ResultR.append(Record.ssn.decode('utf-8','replace').strip('\x00'))
            ResultR.append(Record.fName.decode('utf-8','replace').strip('\x00'))
            ResultR.append(Record.lName.decode('utf-8','replace').strip('\x00'))
            finalResult.append(ResultR)
    Databaseread.close()
    print(finalResult)

ReadId('small.bin')
