class mysocket:
    '''
    Python Docs How to sockets
    '''
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))
    
    def send(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            totalsent = totalsent + sent

    def receive(self):
        msg = ''
        while len(msg) < MSGLEN:
            chunk = self.sock.revv(MSGLEN-len(msg))
            if chunk == '':
                raise RuntimeError("Socket connection broken")
            msg = msg + chunk
        return msg
