from struct import *
from collections import namedtuple
from datetime import date
import shelve
import itertools
import time
import json

format = '20s 20s 70s 40s 80s 25siii 12s 25s 50s 50s'
Result = namedtuple('Result',['fName','lName','job','company','address','phone','day','month','year','ssn','uname','email','url'])

#function Age() for find out current age
today = date.today()
def age(year, month, day):
    age = today.year - year - ((today.month, today.day) < (month, day))
    print(age)
    return age

#function CreatId() to add index in database 

def CreateId(Fname):
    R_read =0
    b_read = 0
    Datbaseindex = shelve.open('index.db' , 'n')
    with open(Fname,'rb') as File:
        while True:
            TotalLength = calcsize(format)
            R_read +=1
            recrd = File.read(calcsize(format))
            if not recrd:
                break
            if(len(recrd) == calcsize(format)):
                ResultC = Result._make(unpack(format,recrd)) 
                Birthdate= date(ResultC.year, ResultC.month, ResultC.day)
                if str(Birthdate) in Datbaseindex:
                    Datbaseindex["{}".format(Birthdate)].append(b_read)
                else:
                    Datbaseindex["{}".format(Birthdate)] = [b_read]
                b_read+=calcsize(format)
            if(R_read%10==0):
                File.read(46)
                b_read+=46
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

    with open(Fname,'rb') as File:
        for offset in Finalrows:
            ResultR = []
            File.seek(offset,0)
            FileData = File.read(calcsize(format))
            if FileData:
                Record = Result._make(unpack(format,FileData))
                ResultR.append(Record.ssn.decode('ascii','ignore').replace('\x00',''))
                ResultR.append(Record.fName.decode('ascii','ignore').replace('\x00',''))
                ResultR.append(Record.lName.decode('ascii','ignore').replace('\x00',''))
                finalResult.append(ResultR)
    Databaseread.close()
    print(finalResult)

Fname = 'small.bin'

startTime = time.time()
CreateId(Fname)
ReadId(Fname)
print('\n execution time of query 3 ' + str(time.time() - startTime))