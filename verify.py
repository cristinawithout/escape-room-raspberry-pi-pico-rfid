from machine import Pin
from mfrc522 import MFRC522
import utime

def uidToString(uid):
    return int.from_bytes(bytes(uid),"little",False)
    

class Readers:
    
    def __init__(self):
        self.reader = []
        self.readerId = []
        self.previousCard = []
        self.cardId = []
        self.good = []

   
    def add(self, reader, readerID="", cardId=""):
        self.reader.append(reader)
        if len(readerID)==0:
            readerID= "RFID #"+str(len(self.reader))
        self.readerId.append(readerID)
        self.previousCard.append([0])
        self.cardId.append(cardId)
        self.good.append(False)
    
    def checkReader(self,idx=0):
        if len(self.reader)> idx:
            self.reader[idx].init()
            (stat, tag_type) = self.reader[idx].request(self.reader[idx].REQIDL)
            if stat == self.reader[idx].OK:
                (stat, uidRaw) = self.reader[idx].SelectTagSN()
                uid = uidToString(uidRaw)
                if stat == self.reader[idx].OK:
                    return (self.readerId[idx] , uid, uid == self.cardId[idx])
               # if uid != self.previousCard[idx]:
               #     if stat == self.reader[idx].OK:
               #         self.previousCard[idx] = uid
               #         return (self.readerId[idx] , uid, uid == self.cardId[idx])
            else:
                self.previousCard[idx] = [0]
        return (-1, [0], False)
    
    
    def checkAnyReader(self):
        for idx in range(len(self.reader)):
            (readerID, uid, match) = self.checkReader(idx)
            print(idx, " match: ", match, ", card id: ", uid)
            self.good[idx] = match

        print(self.good)
        if any(x == 0 for x in self.good):
            return False
        else:
            return True
    
    
# define readers

readers = Readers()

# CS1 = Pin 2
reader1 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=1,rst=22)
# CS5 = Pin 7
reader2 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)
# CS9 = Pin 12
reader3 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=9,rst=22)
# CS17 = Pin 22
reader4 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=17,rst=22)
# CS13 = Pin 17
reader5 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=13,rst=22)


readers.add(reader1,"READER1", 2816952116)
readers.add(reader2,"READER2", 2814051636)
readers.add(reader3,"READER3", 2098114185)
readers.add(reader4,"READER4", 14561854)
readers.add(reader5,"READER5", 2804865828)

lock = Pin(0, Pin.OUT)

print("")
print("Please place card on any reader")
print("")

try:
    while True:
        allGood = readers.checkAnyReader()
        print(allGood)
        if(allGood):
            lock.value(0)
        else:
            lock.value(1)
               

except KeyboardInterrupt:
    pass
