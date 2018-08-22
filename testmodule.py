# coding: UTF-8
'''
Created on 2018/08/22

@author: Shuji
'''

import serial
from pip._vendor.distlib.compat import raw_input

def TxTest():
    serialPort = serial.Serial(port="/dev/tty.usbserial-AH01KQHK", baudrate=115200, timeout=5, parity=serial.PARITY_NONE)
    
    serialPort.reset_input_buffer()
    
    if serialPort.out_waiting > 0:
        serialPort.reset_output_buffer()
    
    print("push reset button")
    
    print("type OK when button is pushed")
    print(">>> ")
    input_text = raw_input()
    
    if input_text == "OK":      
        while serialPort.in_waiting > 0:
            responseText = serialPort.readline()
            print(responseText)
        
        serialPort.write(bytes("AT\r\n", 'UTF-8'))
        
        while serialPort.in_waiting > 0:
            responseText = serialPort.readline()
            print(responseText)
if __name__ == '__main__':
    TxTest()
    
    
    
    