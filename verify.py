from machine import Pin
from mfrc522 import MFRC522
import utime

reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=1,rst=22)
reader2 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)
reader3 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=9,rst=22)
reader4 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=17,rst=22)
reader5 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=13,rst=22)

lock = Pin(0, Pin.OUT)

 
print("Bring RFID TAG Closer...")
print("")
 
reader.init()
reader2.init()
reader3.init()
reader4.init()
reader5.init()

lock.value(1)
good = [0,0,0,0,0]

while True:
    print("START")
    #reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)  
            if card == 2816952116:
                #print("READER 1 GOOD")
                good[0] = 1
            else:
                #print("READER 1 BAD")
                good[0] = 0
    else:
        good[0] = 0
                
    #reader2.init()
    good[1] = 1 #temp -reader is broken
    (stat2, tag_type2) = reader2.request(reader2.REQIDL)
    if stat2 == reader2.OK:
        (stat2, uid2) = reader2.SelectTagSN()
        if stat2 == reader2.OK:
            card2 = int.from_bytes(bytes(uid2),"little",False)
            if card2 == 2814051636:
                #print("READER 2 GOOD")
                good[1] = 1
            else:
                #print ("READER 2 BAD")
                good[1] = 0
    #else:
     #   good[1] = 0
        
                 
    #reader3.init()
    (stat3, tag_type3) = reader3.request(reader3.REQIDL)
    if stat3 == reader3.OK:
        (stat3, uid3) = reader3.SelectTagSN()
        if stat3 == reader3.OK:
            card3 = int.from_bytes(bytes(uid3),"little",False)
            if card3 == 2098114185:
                #print("READER 3 GOOD")
                good[2] = 1
            else:
                #print ("READER 3 BAD")
                good[2] = 0
    else:
        good[2] = 0
                
    #reader4.init()
    (stat4, tag_type4) = reader4.request(reader4.REQIDL)
    if stat4 == reader4.OK:
        (stat4, uid4) = reader4.SelectTagSN()
        if stat4 == reader4.OK:
            card4 = int.from_bytes(bytes(uid4),"little",False)
            if card4 == 14561854:
                #print("READER 4 GOOD")
                good[3] = 1
            else:
                #print ("READER 4 BAD")
                good[3] = 0
    else:
        good[3] = 0
                
    #reader5.init()
    (stat5, tag_type5) = reader5.request(reader5.REQIDL)
    if stat5 == reader5.OK:
        (stat5, uid5) = reader5.SelectTagSN()
        if stat5 == reader5.OK:
            card5 = int.from_bytes(bytes(uid5),"little",False)
            if card5 == 2804865828:
                #print("READER 5 GOOD")
                good[4] = 1
            else:
                #print ("READER 5 BAD")
                good[4] = 0
    else:
        good[4] = 0
                
    print(good)
    
    if any(x == 0 for x in good):
        print("BAD")
        lock.value(1)
    else:
        print("GOOD")
        lock.value(0)

    utime.sleep_ms(500) 