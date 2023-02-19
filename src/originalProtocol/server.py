# 参考：https://qiita.com/note-tech/items/c3e1e497d231ea1e7ca7

import socket
import time
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

MESSAGE_SIZE = 256

SOURCE_ID_START_INDEX = 0
SOURCE_ID_END_INDEX = 3
SEND_ID_START_INDEX = 4
SEND_ID_END_INDEX = 7
DATA_TYPE_START_INDEX = 8
DATA_TYPE_END_INDEX = 11
DATA_LENGTH_START_INDEX = 12
DATA_LENGTH_END_INDEX = 15
DATA_START_INDEX = 16

host = '127.0.0.1'
port = 8890
localAddr = (host, port)

def getNumberParseBytes(startIndex, endIndex, byte:bytes):
    dataLength = (endIndex - startIndex) + 1
    intNum : int = 0

    for i in range(dataLength):
        intNum = intNum + (byte[startIndex + i] << (i*8))

    return intNum

def getStringParseBytes(startIndex, endIndex, byte:bytes):
    bArray:bytearray = bytearray()

    for i in range(startIndex, endIndex):
        bArray.append(byte[i])
    
    return bArray.decode()

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
    print('create socket')

    sock.bind(localAddr)

    while True:
        try :
            print('Waiting message')
            message, cli_addr = sock.recvfrom(MESSAGE_SIZE)
            sourceID = getNumberParseBytes(SOURCE_ID_START_INDEX, SOURCE_ID_END_INDEX, message)
            print("送信元ID : " + str(sourceID))
            
            sendID = getNumberParseBytes(SEND_ID_START_INDEX, SEND_ID_END_INDEX, message)
            print("送信先ID : " + str(sendID))
            dataType = getNumberParseBytes(DATA_TYPE_START_INDEX, DATA_TYPE_END_INDEX, message)
            print("データタイプ : " + str(dataType))
            
            dataLength = getNumberParseBytes(DATA_LENGTH_START_INDEX, DATA_LENGTH_END_INDEX, message)
            print("データ長 : " + str(dataLength))

            data = getStringParseBytes(DATA_START_INDEX, (DATA_START_INDEX + dataLength), message)
            print("データ : " + str(data))

            time.sleep(1)

            print('Send response to Client')
            sock.sendto('Success to receive message'.encode(encoding='utf-8'), cli_addr)

        except KeyboardInterrupt:
            print ('\n . . .\n')
            sock.close()
            break