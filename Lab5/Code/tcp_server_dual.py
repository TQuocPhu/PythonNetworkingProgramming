import socket
import threading
import os

HOST = '0.0.0.0'
CMD_PORT = 8000
DATA_PORT = 8001

def handle_command(conn_cmd, addr):
    try:
        while True:
            data = conn_cmd.recv(1024).decode().strip()
            if not data:
                break
            print(f"[COMMAND] Nhận từ {addr}: {data}")

            parts = data.split()
            if len(parts) != 2:
                conn_cmd.sendall("ERROR\n".encode())
                continue

            cmd, target = parts
            if cmd == "GET":
                if os.path.isfile(target):
                    conn_cmd.sendall("OK\n".encode())
                    # Gửi file qua cổng dữ liệu
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_socket:
                        data_socket.bind((HOST, DATA_PORT))
                        data_socket.listen(1)
                        conn_data, _ = data_socket.accept()
                        with open(target, "rb") as f:
                            while True:
                                chunk = f.read(1024)
                                if not chunk:
                                    break
                                conn_data.sendall(chunk)
                        conn_data.close()
                else:
                    conn_cmd.sendall("ERROR\n".encode())

            elif cmd == "DELETE":
                if os.path.isfile(target):
                    os.remove(target)
                    conn_cmd.sendall("OK\n".encode())
                else:
                    conn_cmd.sendall("ERROR\n".encode())

            elif cmd == "LIST":
                if os.path.isdir(target):
                    conn_cmd.sendall("OK\n".encode())
                    # Gửi nội dung thư mục qua cổng dữ liệu
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_socket:
                        data_socket.bind((HOST, DATA_PORT))
                        data_socket.listen(1)
                        conn_data, _ = data_socket.accept()
                        files = "\n".join(os.listdir(target))
                        conn_data.sendall(files.encode())
                        conn_data.close()
                else:
                    conn_cmd.sendall("ERROR\n".encode())

            else:
                conn_cmd.sendall("ERROR\n".encode())
    except Exception as e:
        print(f"Lỗi xử lý lệnh: {e}")
    finally:
        conn_cmd.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_cmd_socket:
        server_cmd_socket.bind((HOST, CMD_PORT))
        server_cmd_socket.listen(5)
        print(f"[SERVER] Đang lắng nghe lệnh tại cổng {CMD_PORT}...")

        while True:
            conn_cmd, addr = server_cmd_socket.accept()
            print(f"[SERVER] Kết nối mới từ {addr}")
            threading.Thread(target=handle_command, args=(conn_cmd, addr)).start()

if __name__ == "__main__":
    main()
