import socket

SERVER_IP = 'localhost'
CMD_PORT = 8000
DATA_PORT = 8001

def receive_data_to_file(filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, DATA_PORT))
        with open("client_" + filename, "wb") as f:
            while True:
                data = s.recv(1024)
                if not data:
                    break
                f.write(data)
    print(f"[CLIENT] Đã lưu vào client_{filename}")

def receive_data_to_screen():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, DATA_PORT))
        data = s.recv(4096)
        print("[CLIENT] Nội dung thư mục:")
        print(data.decode())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cmd_socket:
        cmd_socket.connect((SERVER_IP, CMD_PORT))
        while True:
            command = input("Nhập lệnh (GET/DELETE/LIST <tên file hoặc thư mục>) hoặc EXIT: ").strip()
            if command.upper() == "EXIT":
                break

            cmd_socket.sendall((command + "\n").encode())
            response = cmd_socket.recv(1024).decode().strip()
            print(f"[CLIENT] Phản hồi: {response}")

            if response == "OK":
                if command.startswith("GET"):
                    filename = command.split()[1]
                    receive_data_to_file(filename)
                elif command.startswith("LIST"):
                    receive_data_to_screen()

if __name__ == "__main__":
    main()
