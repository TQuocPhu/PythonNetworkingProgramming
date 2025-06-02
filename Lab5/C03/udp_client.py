import socket

SERVER_IP = 'localhost'  # hoặc thay bằng địa chỉ IP của server nếu chạy khác máy
PORT = 8888

def parse_input(expr):
    # Tách biểu thức kiểu: "100 + 200"
    try:
        parts = expr.strip().split()
        if len(parts) != 3:
            return None
        operand1, operator, operand2 = parts
        return f"{operator} {operand1} {operand2}\n"
    except:
        return None

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        expr = input("Nhập phép toán (ví dụ: 100 + 200), hoặc 'exit' để thoát: ")
        if expr.lower() == 'exit':
            break

        message = parse_input(expr)
        if not message:
            print("Biểu thức không hợp lệ. Vui lòng thử lại.")
            continue

        client_socket.sendto(message.encode(), (SERVER_IP, PORT))
        result, _ = client_socket.recvfrom(1024)
        print("Kết quả:", result.decode())

    client_socket.close()

if __name__ == "__main__":
    main()