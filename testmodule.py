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
    
    def WaitForText(self, waitString, timeOut):
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
        self.WaitForText(waitMessage, replyTimeOut)
    
    def Disconnect(self):
        self.__serialPort.close()
def TxTest():
    
    test = Test()
    
    test.Connect()
    
    print("push reset button")
    
    print("type OK when button is pushed")
    print(">>> ")
    
    input_text = raw_input()
    
    if input_text == "OK":  
        # ready待ち
        test.WaitForText(waitString="ready\r\n", timeOut=5)
        
        # WIFI CONNECTED待ち
        test.WaitForText(waitString="WIFI CONNECTED\r\n", timeOut=5)
        
        # WIFI GOT IP待ち
        test.WaitForText(waitString="WIFI GOT IP\r\n", timeOut=10)
        
        # AT transmit
        test.SendMessage(sendMessage="AT\r\n", waitMessage="OK\r\n", replyTimeOut=5)
        
        # disconnect
        test.Disconnect()
                
if __name__ == '__main__':
    TxTest()
    
    
    
    