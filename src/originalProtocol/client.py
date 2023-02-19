# 参考：https://qiita.com/note-tech/items/c3e1e497d231ea1e7ca7

import socket
import struct
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

MESSAGE_SIZE = 256
SOURCE_ID = 999
SEND_ID = 1024
DATA_TYPE = 1

host = '127.0.0.1'
port = 8890
localAddr = (host, port)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            print('Input any messages, Type [end] to exit')
            message = input()
            if message != 'end':
                data = message.encode('utf-8')
                dataLength = len(data)
                message = struct.pack('4I' + str(dataLength) + 's', SOURCE_ID, SEND_ID, DATA_TYPE, dataLength, data)
                sock.sendto(message, localAddr)

                print('Waiting response from Server')
                rx_meesage, addr = sock.recvfrom(MESSAGE_SIZE)
                print(f"[Server]: {rx_meesage.decode(encoding='utf-8')}")

            else:
                print('closing socket')
                sock.close()
                print('done')
                break

        except KeyboardInterrupt:
            print('closing socket')
            sock.close()
            print('done')
            break
