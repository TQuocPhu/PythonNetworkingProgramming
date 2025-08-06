# MessageClient.py
import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(f"\n👂 Từ {addr}: {data.decode()}")
        except Exception as e:
            print(f"Lỗi khi nhận: {e}")
            break

def send_messages(sock, server_ip, server_port):
    while True:
        try:
            message = input("Bạn: ")
            sock.sendto(message.encode(), (server_ip, server_port))
        except Exception as e:
            print(f"Lỗi khi gửi: {e}")
            break

def main():
    client_ip = "0.0.0.0"
    client_port = int(input("🔌 Nhập cổng để lắng nghe (VD: 20002): "))
    server_ip = input("Nhập IP server (VD: 192.168.1.1): ").strip()
    server_port = int(input("Nhập PORT server (VD: 20001): "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((client_ip, client_port))

    print(f"📡 Client đang lắng nghe tại {client_ip}:{client_port}...")

    # Thread nhận và gửi
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
    threading.Thread(target=send_messages, args=(sock, server_ip, server_port), daemon=True).start()

    while True:
        pass

if __name__ == "__main__":
    main()
