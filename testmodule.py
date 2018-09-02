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
    
    def __sendMessage(self, sendMessage, waitMessage, replyTimeOut):
        self.__writeText(sendMessage)
        self.__waitForText(waitMessage, replyTimeOut)
    
    def Disconnect(self):
        self.__serialPort.close()
        
    def WaitForReady(self):
        self.__waitForText(waitString="ready\r\n", timeOut=50)
    
    def WaitForWIFICONNECT(self):
        self.__waitForText(waitString="WIFI CONNECTED\r\n", timeOut=50)
    
    def WaitForGOTIP(self):
        self.__waitForText(waitString="WIFI GOT IP\r\n", timeOut=100)
    
    def SendAT(self):
        self.__sendMessage(sendMessage="AT\r\n", waitMessage="OK\r\n", replyTimeOut=50)
        
    def SendCIFSR(self):
        self.__sendMessage(sendMessage="AT+CIFSR\r\n", waitMessage="OK\r\n", replyTimeOut=100)
    
    def EnableCIPMUX(self):
        self.__sendMessage(sendMessage="AT+CIPMUX=1\r\n", waitMessage="OK\r\n", replyTimeOut=100)
    
    def DisableCPIMUX(self):
        self.__sendMessage(sendMessage="AT+CIPMUX=0\r\n", waitMessage="OK\r\n", replyTimeOut=100) 
    
    def TCPServerEnable(self, port):
        self.__sendMessage(sendMessage="AT+CIPSERVER=1,%d\r\n" % port, waitMessage="OK\r\n", replyTimeOut=100)
    
    def CheckClientConnection(self):
        result = False
        if self.__serialPort.in_waiting > 0:
            responseText = self.__serialPort.readline()
            print(responseText)
                
            if responseText.decode().find(",CONNECT\r\n") >= 0:
                result = True
                print("Client detected %s" % responseText.decode().split(",")[0])
            
        return result
    
    def ReplyHTTPMessage(self, clientID):
        headerToReply1 = "HTTP/1.1 200 OK\r\n"
        headerToReply2 = "Date: Sat, 1 Sep 2018 15:08:05 GMT\r\n"
        headerToReply3 = "Content-type: text/html\r\n"
        headerToReply4 = "\r\n"

        htmlToShow = "<html><body>It works!</body></html>\r\n"
        
        self.__sendMessage(sendMessage="AT+CIPSEND=%d,%d\r\n" % (clientID, len(headerToReply1)), waitMessage="> ", replyTimeOut=100)
        self.__sendMessage(sendMessage=headerToReply1, waitMessage="Recv %d bytes\r\n" % len(headerToReply1), replyTimeOut=100)
        
        self.__sendMessage(sendMessage="AT+CIPSEND=%d,%d\r\n" % (clientID, len(headerToReply2)), waitMessage="> ", replyTimeOut=100)
        self.__sendMessage(sendMessage=headerToReply2, waitMessage="Recv %d bytes\r\n" % len(headerToReply2), replyTimeOut=100)
        
        self.__sendMessage(sendMessage="AT+CIPSEND=%d,%d\r\n" % (clientID, len(headerToReply3)), waitMessage="> ", replyTimeOut=100)
        self.__sendMessage(sendMessage=headerToReply3, waitMessage="Recv %d bytes\r\n" % len(headerToReply3), replyTimeOut=100)
        
        self.__sendMessage(sendMessage="AT+CIPSEND=%d,%d\r\n" % (clientID, len(headerToReply4)), waitMessage="> ", replyTimeOut=100)
        self.__sendMessage(sendMessage=headerToReply4, waitMessage="Recv %d bytes\r\n" % len(headerToReply4), replyTimeOut=100)
        
        self.__sendMessage(sendMessage="AT+CIPSEND=%d,%d\r\n" % (clientID, len(htmlToShow)), waitMessage="> ", replyTimeOut=100)
        self.__sendMessage(sendMessage=htmlToShow, waitMessage="Recv %d bytes\r\n" % len(htmlToShow), replyTimeOut=100)
        
        #self.__sendMessage(sendMessage="AT+CIPSEND=%d,%d\r\n" % (clientID, len(headerToReply1 + headerToReply2 + headerToReply3 + headerToReply4 + htmlToShow)), waitMessage="> ", replyTimeOut=100)
        #self.__sendMessage(sendMessage=headerToReply1 + headerToReply2 + headerToReply3 + headerToReply4 + htmlToShow, waitMessage="Recv %d bytes\r\n" % len(headerToReply1 + headerToReply2 + headerToReply3 + headerToReply4 + htmlToShow), replyTimeOut=100)
    
    
    def RoutineLoop(self):
        responseText = None
        
        if self.__serialPort.in_waiting > 0:
            responseByte = self.__serialPort.readline()
            responseText = responseByte.decode()
        if responseText != None:
            # detect CONNECT
            if responseText.find(",CONNECT\r\n") >= 0:
                print("detected client connection : key is %s" % responseText.split(",")[0])
            # detect CLOSED
            if responseText.find(",CLOSED\r\n") >= 0:
                print("detected client disconnection : key is %s" % responseText.split(",")[0])
            # detect +IPD
            if responseText.find("+IPD,") >= 0:
                print("detected client message send : client key is %s, byte size is %s" % (responseText.split(":")[0].split(",")[1], responseText.split(":")[0].split(",")[2]))
                print(responseText.split(":")[1])
                wholeLength = int(responseText.split(":")[0].split(",")[2])
                leftLength = wholeLength - len(responseText.split(":")[1])
                leftBytes = self.__serialPort.read(leftLength)
                leftText = leftBytes.decode()
                print(leftText)
                
                self.ReplyHTTPMessage(0)
    
def TxTest():
    
    test = Test()
    
    test.Connect()
    
    print("push reset button")
    
    print("type OK when button is pushed")
    print(">>> ")
    
    input_text = raw_input()
    
    if input_text == "OK":  
        # ready待ち
        test.WaitForReady()
        
        # WIFI CONNECTED待ち
        test.WaitForWIFICONNECT()
        
        # WIFI GOT IP待ち
        test.WaitForGOTIP()
        
        # AT transmit
        test.SendAT()
        
        # CIFSR
        test.SendCIFSR()
        
        # CIPMUX
        test.EnableCIPMUX()
        
        # TCPServer
        test.TCPServerEnable(8888)
        
        while True:
            # test.CheckClientConnection()
            sleep(0.1)
            test.RoutineLoop()
        
        
        # disconnect
        test.Disconnect()
                
if __name__ == '__main__':
    TxTest()
    
    
    
    