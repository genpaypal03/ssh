import socket, threading, threadpoolctl

# Settings
LISTENING_PORT = 80
SSH_HOST = '127.0.0.1'
SSH_PORT = 22

def handler(clientsock, addr):
    try:
        msg = clientsock.recv(1024).decode()
        if "Upgrade: websocket" in msg:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((SSH_HOST, SSH_PORT))
            clientsock.send(b"HTTP/1.1 101 Switching Protocols\r\n\r\n")
            
            def forward(source, destination):
                while True:
                    data = source.recv(1024)
                    if not data: break
                    destination.sendall(data)
            
            threading.Thread(target=forward, args=(clientsock, server)).start()
            threading.Thread(target=forward, args=(server, clientsock)).start()
    except:
        pass

def main():
    print(f"Proxy running on port {LISTENING_PORT}...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', LISTENING_PORT))
    server.listen(100)
    while True:
        clientsock, addr = server.accept()
        threading.Thread(target=handler, args=(clientsock, addr)).start()

if __name__ == '__main__':
    main()
