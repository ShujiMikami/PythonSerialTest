# coding: UTF-8
'''
Created on 2018/08/22

@author: Shuji
'''

import serial
from pip._vendor.distlib.compat import raw_input
from time import sleep

class Test:
    __serialPort = 0
    
    def Connect(self):
        self.__serialPort = serial.Serial(port="/dev/tty.usbserial-AH01KQHK", baudrate=115200, timeout=5, parity=serial.PARITY_NONE)
        self.__serialPort.reset_input_buffer()
    
        if self.__serialPort.out_waiting > 0:
            self.__serialPort.reset_output_buffer()
    
    def __waitForText(self, waitString, timeOut):
        flag = False
        cnt = 0
        while flag == False:
            if self.__serialPort.in_waiting > 0:
                responseText = self.__serialPort.readline()
                print(responseText)
                
                if responseText == waitString.encode():
                    flag = True
            
            sleep(0.1)
            cnt = cnt + 1
            
            if cnt > timeOut:
                print("timeout")
                flag = True
    
    def __writeText(self, sendMessage):
        self.__serialPort.write(sendMessage.encode())
    
    def SendMessage(self, sendMessage, waitMessage, replyTimeOut):
        self.__writeText(sendMessage)
        self.__waitForText(waitMessage, replyTimeOut)
    
    def Disconnect(self):
        self.__serialPort.close()
def TxTest():
    processStatus = True
    
    serialPort = serial.Serial(port="/dev/tty.usbserial-AH01KQHK", baudrate=115200, timeout=5, parity=serial.PARITY_NONE)
    
    serialPort.reset_input_buffer()
    
    if serialPort.out_waiting > 0:
        serialPort.reset_output_buffer()
    
    print("push reset button")
    
    print("type OK when button is pushed")
    print(">>> ")
    
    input_text = raw_input()
    
    if input_text == "OK":  
        # ready待ち
        flag = False
        cnt = 0
        while flag == False:
            if serialPort.in_waiting > 0:
                responseText = serialPort.readline()
                print(responseText)
                
                if responseText == b"ready\r\n":
                    flag = True
            
            sleep(0.1)
            cnt = cnt + 1
            
            if cnt > 50:
                print("timeout")
                processStatus = False
                flag = True
        
        if processStatus == True:    
            # WIFI CONNECTED待ち
            flag = False
            cnt = 0
            while flag == False:
                if serialPort.in_waiting > 0:
                    responseText = serialPort.readline()
                    print(responseText)
                    
                    if responseText == b"WIFI CONNECTED\r\n":
                        flag = True
                
                sleep(0.1)
                cnt = cnt + 1
                
                if cnt > 50:
                    print("timeout")
                    processStatus = False
                    flag = True
        
        if processStatus == True:    
            # WIFI GOT IP待ち
            flag = False
            cnt = 0
            while flag == False:
                if serialPort.in_waiting > 0:
                    responseText = serialPort.readline()
                    print(responseText)
                    
                    if responseText == b"WIFI GOT IP\r\n":
                        flag = True
                
                sleep(0.1)
                cnt = cnt + 1
                
                if cnt > 50:
                    print("timeout")
                    processStatus = False
                    flag = True
        
        serialPort.write(bytes("AT\r\n", 'UTF-8'))
        
        if processStatus == True:    
            # OK待ち
            flag = False
            cnt = 0
            while flag == False:
                if serialPort.in_waiting > 0:
                    responseText = serialPort.readline()
                    print(responseText)
                    
                    if responseText == b"OK\r\n":
                        flag = True
                
                sleep(0.1)
                cnt = cnt + 1
                
                if cnt > 50:
                    print("timeout")
                    processStatus = False
                    flag = True
    serialPort.close()        
if __name__ == '__main__':
    TxTest()
    
    
    
    