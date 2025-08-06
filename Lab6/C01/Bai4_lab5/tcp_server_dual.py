import socket
import threading
import os

HOST = '0.0.0.0'
CMD_PORT = 8000
DATA_PORT = 8001

pending_data_tasks = {}
pending_lock = threading.Lock()

def handle_data_connection(conn_data, addr):
    client_ip = addr[0]
    try:
        with pending_lock:
            if client_ip in pending_data_tasks:
                action, target = pending_data_tasks.pop(client_ip)
            else:
                conn_data.close()
                return

        if action == "GET":
            with open(target, "rb") as f:
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    conn_data.sendall(chunk)

        elif action == "LIST":
            files = "\n".join(os.listdir(target))
            conn_data.sendall(files.encode())

    except Exception as e:
        print(f"[DATA] Lỗi xử lý dữ liệu từ {addr}: {e}")
    finally:
        conn_data.close()

def data_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_socket:
        data_socket.bind((HOST, DATA_PORT))
        data_socket.listen(10)
        print(f"[DATA SERVER] Đang lắng nghe dữ liệu tại cổng {DATA_PORT}...")

        while True:
            conn_data, addr = data_socket.accept()
            threading.Thread(target=handle_data_connection, args=(conn_data, addr)).start()

def handle_command(conn_cmd, addr):
    client_ip = addr[0]
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
                    with pending_lock:
                        pending_data_tasks[client_ip] = ("GET", target)
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
                    with pending_lock:
                        pending_data_tasks[client_ip] = ("LIST", target)
                else:
                    conn_cmd.sendall("ERROR\n".encode())

            else:
                conn_cmd.sendall("ERROR\n".encode())
    except Exception as e:
        print(f"[COMMAND] Lỗi xử lý lệnh từ {addr}: {e}")
    finally:
        print(f"[COMMAND] Đóng kết nối với {addr}")
        conn_cmd.close()

def main():
    threading.Thread(target=data_server, daemon=True).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_cmd_socket:
        server_cmd_socket.bind((HOST, CMD_PORT))
        server_cmd_socket.listen(10)
        print(f"[SERVER] Đang lắng nghe lệnh tại cổng {CMD_PORT}...")

        while True:
            conn_cmd, addr = server_cmd_socket.accept()
            print(f"[SERVER] Kết nối mới từ {addr}")
            threading.Thread(target=handle_command, args=(conn_cmd, addr)).start()

if __name__ == "__main__":
    main()
