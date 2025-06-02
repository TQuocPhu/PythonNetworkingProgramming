import socket

HOST = '0.0.0.0'
PORT = 8888

def calculate(operation, op1, op2):
    try:
        op1 = float(op1)
        op2 = float(op2)
        if operation == '+':
            return str(op1 + op2)
        elif operation == '-':
            return str(op1 - op2)
        elif operation == '*':
            return str(op1 * op2)
        elif operation == '/':
            if op2 == 0:
                return "Lỗi: chia cho 0"
            return str(op1 / op2)
        else:
            return "Phép toán không hợp lệ"
    except ValueError:
        return "Đối số không hợp lệ"

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    print(f"UDP Server đang chạy tại cổng {PORT}...")

    while True:
        message, client_addr = server_socket.recvfrom(1024)
        msg = message.decode().strip()
        print(f"Nhận từ {client_addr}: '{msg}'")

        parts = msg.split()
        if len(parts) != 3:
            response = "Định dạng không hợp lệ"
        else:
            op, operand1, operand2 = parts
            response = calculate(op, operand1, operand2)

        server_socket.sendto(response.encode(), client_addr)

if __name__ == "__main__":
    main()