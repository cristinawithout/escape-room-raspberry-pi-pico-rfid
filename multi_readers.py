from mfrc522 import MFRC522
import utime


# youtube short video about it https://www.youtube.com/watch?v=wE2AamTF5dg

def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring
    

class Readers:
    
    def __init__(self):
        self.reader = []
        self.readerId = []
        self.previousCard = []

   
    def add(self, reader, readerID=""):
        self.reader.append(reader)
        if len(readerID)==0:
            readerID= "RFID #"+str(len(self.reader))
        self.readerId.append(readerID)
        self.previousCard.append([0])
    
    def checkReader(self,idx=0):
        if len(self.reader)> idx:
            self.reader[idx].init()
            (stat, tag_type) = self.reader[idx].request(self.reader[idx].REQIDL)
            if stat == self.reader[idx].OK:
                (stat, uid) = self.reader[idx].SelectTagSN()
                if uid != self.previousCard[idx]:
                    if stat == self.reader[idx].OK:
                        self.previousCard[idx] = uid
                        return (self.readerId[idx] , uid)
            else:
                self.previousCard[idx] = [0]
        return (-1, [0])
    
    
    def checkAnyReader(self):
        for idx in range(len(self.reader)):
            (readerID, uid ) = self.checkReader(idx)
            if readerID != -1:
                return (readerID, uid)
        return (-1 , [0])
    
    
# define readers

readers = Readers()

              
reader1 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=1,rst=22)
#reader2 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)
reader3 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=9,rst=22)
reader4 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=17,rst=22)
reader5 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=13,rst=22)


readers.add(reader1,"READER1")
#readers.add(reader2,"READER2")
readers.add(reader3,"READER3")
readers.add(reader4,"READER4")
readers.add(reader5,"READER5")


print("")
print("Please place card on any reader")
print("")

try:
    while True:
        (readerID, uid) = readers.checkAnyReader()
        if readerID != -1:
            print(" RFID card:", uidToString(uid), " from ",readerID)
        utime.sleep_ms(50)                

except KeyboardInterrupt:
    pass