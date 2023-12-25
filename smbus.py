import time
from smbus2 import SMBus, i2c_msg
bus = SMBus(1)
#bus.write_byte(0x24,0xff)
lut=[0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f]
addr=[0x34,0x35,0x36,0x37]
def setnum(f,auto,direc):
    bus.write_byte(0x24,0x41)
    s=f
    n1=int(s)
    n2=round((s-float(n1))*10) % 10
    res = s
    for i in range(3):
        bus.write_byte(addr[2-i],lut[n1 % 10])
        if i ==0 :
            bus.write_byte(addr[2],0x80+lut[n1 % 10])
        n1 = n1 //10
    bus.write_byte(addr[3],lut[n2])
    print(res)
    if auto < 3 : setfreq(res,auto,direc) # auto>=3 means that auto search process is finished, just need to display the fatal frequency
def setfreq(f,sm,direction):
    cof=32768
    freq=f
    freq14bit = int (4*(freq *  1000000 + 225000) / cof)
    freqH = freq14bit >> 8
    freqL = freq14bit & 0xff
    print(bin(freq14bit))
    #self.muteflag=mute
    up=direction << 7
    if sm :searchflag=1 << 6
    else: searchflag=0
    #print(bin(up),' ',bin(searchflag))
    data=[0 for i in range(5)]
    data[0]=freqH & 0x3f | searchflag
    data[1]=freqL
    data[2]=0b00111000 | up
    data[3]=0b00010111
    data[4]=0b00000000
    try:
        write=i2c_msg.write(0x60,data)
        bus.i2c_rdwr(write)
        #for i in range(5): print(bin(data[i]))
    except:
        pass
    time.sleep(0.5)
    read = i2c_msg.read(0x60,2)
    bus.i2c_rdwr(read)
    s = read.__bytes__()
    pll = int.from_bytes(s, byteorder = 'big', signed = False)
    pll = pll  & 0x3fff
    frequency =float(( pll * cof / 4 - 225000) / 1000000)
    if sm or direction :
        sm += 1
        setnum(frequency,sm,direction)
        print(sm,direction)
