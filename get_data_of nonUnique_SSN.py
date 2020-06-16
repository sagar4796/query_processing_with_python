import struct
from collections import namedtuple
from datetime import date 
import os


f=open("small.bin","rb")
fmt = '20s 20s 70s 40s 80s 25s 3i12s 25s 50s 50s'
block = '46s'
statinfo = os.stat('small.bin')
size = statinfo.st_size
print(size)
recrd = f.read(struct.calcsize(fmt))
fmtCount = 405
blockCount = 46
sizeCount = fmtCount;
count = 0
today = date.today()
i  = 1
Dict = {}
while(sizeCount < size):
    if count == 10 * i:
        i = i+1
        recrd = f.read(struct.calcsize(block))
    else:
        cleared_list = []
        unp = struct.unpack(fmt,recrd)
    for item in unp:
        if type(item) != int:
            cleared_list.append(item.decode('utf-8').strip('\0'))
        else:
            cleared_list.append(item)
    if cleared_list[9] in Dict:
        print(cleared_list[9].strip(' '))
    else:
        Dict[cleared_list[9]] = cleared_list[0]
    count = count + 1
    if(sizeCount >= size - 1):
        break
    else:
        recrd = f.read(struct.calcsize(fmt))
        sizeCount = sizeCount + fmtCount