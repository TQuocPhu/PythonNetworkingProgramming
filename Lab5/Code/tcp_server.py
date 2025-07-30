# Viết chương trình theo mô hình Client-Server sử dụng TCP Socket.
# Trong đó:
# Server lắng nghe ở cổng 8888, làm nhiệm vụ đọc một ký tự số từ '0' đến '9'.
# (Ví dụ: nhận số 0, trả về "khong"; 1, trả về "mot" ; 9, trả về "chin"; nhận ký tự khác số thì trả về "Không phải số nguyên" ).
# Client sẽ nhập vào 1 ký tự, gửi qua Server, nhận kết quả trả về từ Server và thể hiện lên màn hình.


import socket

# Bảng ánh xạ số sang chữ
num_to_word = {
    '0': "khong",
    '1': "mot",
    '2': "hai",
    '3': "ba",
    '4': "bon",
    '5': "nam",
    '6': "sau",
    '7': "bay",
    '8': "tam",
    '9': "chin"
}

HOST = '0.0.0.0'  # Lắng nghe trên tất cả các địa chỉ IP
PORT = 8888


def main():
    # Tạo socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server đang lắng nghe tại cổng {PORT}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Client kết nối từ {addr}")

        data = conn.recv(1024).decode().strip()
        print(f"Nhận từ client: '{data}'")

        if data in num_to_word:
            response = num_to_word[data]
        else:
            response = "Không phải số nguyên"

        conn.send(response.encode())
        conn.close()

if __name__ == "__main__":
    main()