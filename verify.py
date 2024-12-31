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
        self.reset = 0
        self.override = 0
        self.lock = 0
        self.isLocked = 1
        
    def setLock(self, lock, isLocked = 1):
        self.lock = lock
        self.lock.value(isLocked)
        self.isLocked = isLocked
        
    def setControlKeys(self, resetId = 0, overrideId = 0):
        self.reset = resetId # Set a key that resets to locked
        self.override = overrideId # Set a key that opens the lock
   
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
                    if (self.reset == uid):
                        self.lock.value(1)
                        self.isLocked = 1
                        print("RESET - LOCKED")
                    if (self.override == uid):
                        self.lock.value(0)
                        self.isLocked = 0
                        print("OVERRIDE - UNLOCKED")
                    return (self.readerId[idx], uid, uid == self.cardId[idx])
                if uid != self.previousCard[idx]:
                    if stat == self.reader[idx].OK:
                        self.previousCard[idx] = uid
                        return (self.readerId[idx] , uid, uid == self.cardId[idx])
            else:
                self.previousCard[idx] = [0]
        return (-1, [0], False)
    
    
    def checkAnyReader(self):
        for idx in range(len(self.reader)):
            (readerID, uid, match) = self.checkReader(idx)
            #print(readerID, " match: ", match, ", card id: ", uid)
            self.good[idx] = match

        if (self.isLocked == 0):
            return
        
        if any(x == 0 for x in self.good):
            print(self.good)
        else:
            print("GOOD")
            self.isLocked = 0
            lock.value(0)
    
    
# define readers

readers = Readers()

# CS1 = Pin 2
reader1 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=1,rst=22)
# CS13 = Pin 17
reader2 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=13,rst=22)
# CS5 = Pin 7
reader3 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)
# CS9 = Pin 12
reader4 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=9,rst=22)
# CS17 = Pin 22
reader5 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=17,rst=22)

# Use the values from multi_readers here as the 3rd param
readers.add(reader1,"READER1", 2816952116)
readers.add(reader2,"READER2", 2814051636)
readers.add(reader3,"READER3", 2098114185)
readers.add(reader4,"READER4", 14561854)
readers.add(reader5,"READER5", 2804865828)

lock = Pin(0, Pin.OUT)

readers.setLock(lock)
readers.setControlKeys(526962319, 528401087)


print("")
print("Please place card on any reader")
print("")

try:
    while True:
        readers.checkAnyReader()
        utime.sleep_ms(50)
               

except KeyboardInterrupt:
    pass
