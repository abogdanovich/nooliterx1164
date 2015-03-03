# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
Python stable code to work with noolite RX usb modules. Stable for RX1164 model.
"""

__author__ = "Alex Bogdnaovich"
__maintainer__ = "Alex Bogdanovich"
__email__ = "bogdanovich.alex@gmail.com"

DEV_VENDOR = 0x16c0
DEV_PRODUCT = 0x05dc

bmRequestType = 0xA1 #bmRequestType=10100001 == 1: Device-to-Host | 01: Class | 00001: Interface
bRequest = 0x09 #request number 9 to get data
wValue = 0x300 #request value 300 to get data
wIndex = 0x0
length_or_data = 8 #8bits buffer
togl = 0 # the first value to compare with buf[0]

dcommands = [
    'выключить нагрузку',
    'запускает плавное понижение яркости',
    'включить нагрузку '
    'запускает плавное повышение яркости',
    'включает или выключает нагрузку',
    'запускает плавное изменение яркости в обратном направлении',
    'установить заданную в «Данные к команде_0» яркость',
    'вызвать записанный сценарий',
    'записать сценарий',
    'запускает процедуру стирания адреса управляющего устройства из памяти исполнительного',
    'остановить регулировку',
    'включение плавного перебора цвета',
    'переключение цвета',
    'переключение режима работы',
    'переключение скорости эффекта для режима работы'
]


import usb

def unbind_channel(device, channel):
    
    if device is None:
        raise ("device is not conected")
    
    else:
        
        #RX1164 = 64 channel please modify if your device support more than 64 channels

        if channel >= 0 and channel <= 63:
            #bind device from channel
            command = [0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00]
            command[1] = int(channel)
            
            res = device.ctrl_transfer(0x21, 0x09, 0, 0, command)
           
        else:
           raise ("device channel range is wrong") 
       
    
    return res

def bind_channel(device, channel):
    
    if device is None:
        raise ("device is not conected")
    
    else:
        
        #RX1164 = 64 channel please modify if your device support more than 64 channels
        
        if channel >= 0 and channel <= 63: 
            #bind device from channel
            command = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
            command[1] = int(channel)
            
            res = device.ctrl_transfer(0x21, 0x09, 0, 0, command)
            
        else:
            raise ("device channel range is wrong") 
    
    return res

def init_rx():
    dev = usb.core.find(idVendor=DEV_VENDOR, idProduct=DEV_PRODUCT)

    if dev is None:
        raise ValueError('Device not found')
    else:
        print("Device found")
        
        if dev.is_kernel_driver_active(0) is True:
            print "but we need to detach kernel driver"
            dev.detach_kernel_driver(0)
            print 'Now reading data'
        
        
        #configure usb device
        dev.set_configuration()
        endpoint = dev[0][(0,0)][0]
        
        #print endpoint.bEndpointAddress
        #rint endpoint.wMaxPacketSize
        
    return dev
   
def read_rx_data(dev):
    """
    buffer noolite commands: http://www.noo.com.by/assets/files/software/RX1164_HID_API.pdf
    """
    result = dev.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, length_or_data)
    
    return result
        

devrx = init_rx()
buf = []

#test bind \unbind : channel 2

#bind_channel(devrx, 2)
#unbind_channel(devrx, 2)


while True:
    
    buf = read_rx_data(devrx)
    if buf[0] != togl:
        print "RX module event for channel [%d] with command: [%s]" % (buf[1], dcommands[buf[2]])
        togl = buf[0]
        
