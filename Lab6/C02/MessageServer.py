# MessageServer.py
import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(f"\n Từ {addr}: {data.decode()}")
        except Exception as e:
            print(f"Lỗi khi nhận: {e}")
            break

def send_messages(sock, client_ip, client_port):
    while True:
        try:
            message = input("Bạn: ")
            sock.sendto(message.encode(), (client_ip, client_port))
        except Exception as e:
            print(f"Lỗi khi gửi: {e}")
            break

def main():
    server_ip = "0.0.0.0"
    server_port = int(input("🔌 Nhập cổng để lắng nghe (VD: 20001): "))
    client_ip = input(" Nhập IP client (VD: 192.168.1.2): ").strip()
    client_port = int(input(" Nhập PORT client (VD: 20002): "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((server_ip, server_port))

    print(f"📡 Server đang lắng nghe tại {server_ip}:{server_port}...")

    # Thread nhận và gửi
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
    threading.Thread(target=send_messages, args=(sock, client_ip, client_port), daemon=True).start()

    # Giữ chương trình chạy
    while True:
        pass

if __name__ == "__main__":
    main()
