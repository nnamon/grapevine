import socket
import sys

def __send_cmd(sock, data):
    sock.sendto(data, ('<broadcast>', 10001))

def main():
    sock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1 )
    while True:
        sys.stdout.write("input> ")
        msg = raw_input().rstrip()
        __send_cmd(sock, msg)

if __name__ == "__main__" :
    main()
