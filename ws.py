import socket, threading

# Settings
LISTENING_PORT = 80
SSH_HOST = '127.0.0.1'
SSH_PORT = 22

def forward(source, destination):
    while True:
        try:
            data = source.recv(4096)
            if not data: break
            destination.sendall(data)
        except: break

def handler(clientsock, addr):
    try:
        data = clientsock.recv(1024).decode(errors='ignore')
        if "Upgrade: websocket" in data or "CONNECT" in data:
            # Server ဆီ ချိတ်မယ်
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((SSH_HOST, SSH_PORT))
            
            # NetMod ဆီကို 200 OK အရင်ပြန်ပို့မယ်
            clientsock.sendall(b"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n\r\n")
            
            # Data စီးဆင်းအောင် လုပ်မယ်
            threading.Thread(target=forward, args=(clientsock, server), daemon=True).start()
            threading.Thread(target=forward, args=(server, clientsock), daemon=True).start()
    except Exception as e:
        print(f"Error: {e}")

def main():
    print(f"Websocket Proxy running on port {LISTENING_PORT}...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', LISTENING_PORT))
    server.listen(100)
    while True:
        clientsock, addr = server.accept()
        threading.Thread(target=handler, args=(clientsock, addr), daemon=True).start()

if __name__ == '__main__':
    main()
