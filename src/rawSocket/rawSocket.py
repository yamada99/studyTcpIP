import socket
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

MYHOST = '192.168.24.17'

mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
file = open('rawSocketLog.txt','x',encoding='UTF-8')

def prepare():
    mySocket.bind((MYHOST, 0))
    mySocket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON) # ソケットがネットワークインタフェースを通過するすべてのパケットを受信するために必要な設定

def hexdump(data):
    result = []
    for i in range(0, len(data), 16):
        hex = " ".join(["%02X" % x for x in data[i:i+16]])
        # text = "".join(chr(x) if 0x20 <= x <= 0x7E else "." for x in data[i:i+16]) # ASCIIに変換
        result.append("[%04X] %-48s" % (i, hex))
        file.write("[%04X] %-48s" % (i, hex))
        file.write('\n')
    print("\n".join(result))


if __name__ == '__main__':
    prepare()

    try:
        while True:
            data = mySocket.recv(65536)
            hexdump(data)
            print("\n")
            file.write('\n')
            # print(data)
    finally:
        mySocket.close()
        file.close()
