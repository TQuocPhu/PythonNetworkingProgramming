import socket

HOST = 'localhost'  # hoặc IP của server
PORT = 8888

def main():
    # Nhập 1 ký tự
    ch = input("Nhập một ký tự số (0-9): ").strip()

    # Tạo socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    client_socket.send(ch.encode())
    response = client_socket.recv(1024).decode()

    print("Phản hồi từ Server:", response)

    client_socket.close()

if __name__ == "__main__":
    main()