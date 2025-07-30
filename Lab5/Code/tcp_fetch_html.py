''' Viết chương trình nhận đối số là một URL (Ví dụ: www.cit.ctu.edu.vn).
Sử dụng TCP socket nối kết đến web server trong URL để lấy file HTML về,
và hiển thị nội dung file HTML đó ra màn hình.
'''

'''
Import thư viện
socket: dùng để tạo kết nối TCP giữa client và server.
ssl: để tạo kết nối bảo mật SSL/TLS (dùng cho HTTPS).
sys: để đọc đối số dòng lệnh (ví dụ: tên miền từ terminal).

'''
import socket
import ssl
import sys
import webbrowser
import os

# HTTP
# def fetch_html(url):
#     # Thêm tiền tố nếu chưa có
#     if not url.startswith("http"):
#         host = url
#     else:
#         host = url.split("//")[1]

#     port = 80  # Cổng mặc định cho HTTP

#     # Tạo socket TCP
#     try:
#         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     except socket.error as e:
#         print(f"Lỗi tạo socket: {e}")
#         return

#     try:
#         # Kết nối tới server
#         client_socket.connect((host, port))
#     except socket.gaierror:
#         print("Không thể phân giải tên miền.")
#         return
#     except socket.error as e:
#         print(f"Lỗi khi kết nối: {e}")
#         return

#     # Tạo HTTP GET request
#     request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
#     client_socket.send(request.encode())

#     # Nhận dữ liệu HTML
#     response = b""
#     while True:
#         data = client_socket.recv(4096)
#         if not data:
#             break
#         response += data

#     client_socket.close()

#     # Hiển thị nội dung HTML (loại bỏ phần header HTTP nếu cần)
#     response_str = response.decode(errors="ignore")
#     header_end = response_str.find("\r\n\r\n")
#     html_content = response_str[header_end+4:]

#     print(html_content)


#HTTPS:
def fetch_html_https(url): #Hàm chính để lấy HTML từ trang web
    # Xử lý domain
    '''
    Nếu người dùng chỉ nhập www.cit.ctu.edu.vn, thì dùng luôn.
    Nếu người dùng nhập https://www.cit.ctu.edu.vn, thì cắt bỏ https:// để lấy tên host.
    '''
    if not url.startswith("http"):
        host = url
    else:
        host = url.split("//")[1]

    port = 443  # Cổng HTTPS mặc định

    #Kiểm tra và kết nối
    '''
    socket.create_connection(...): mở kết nối TCP tới server.

    ssl.create_default_context(): tạo ngữ cảnh bảo mật SSL.

    wrap_socket(...): bọc socket thường thành socket SSL an toàn.
    '''
    try:
        # Tạo socket TCP
        raw_socket = socket.create_connection((host, port))
        context = ssl.create_default_context()

        # Bọc socket với SSL
        secure_socket = context.wrap_socket(raw_socket, server_hostname=host)

        # Gửi HTTP GET request
        request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        
        '''
        request = ...: Tạo một chuỗi đại diện cho một yêu cầu HTTP GET, được lưu vào biến request.
            f"...": Sử dụng f-string trong Python để tạo chuỗi, cho phép chèn giá trị của biến {host} vào chuỗi một cách dễ dàng.
            Cấu trúc yêu cầu HTTP:
            GET / HTTP/1.1\r\n:
            Đây là dòng yêu cầu (request line) của giao thức HTTP.
            GET: Phương thức HTTP, yêu cầu lấy dữ liệu từ máy chủ.
            /: Đường dẫn (path) của tài nguyên, ở đây là thư mục gốc của máy chủ.
            HTTP/1.1: Phiên bản giao thức HTTP được sử dụng.
            \r\n: Ký tự xuống dòng theo chuẩn HTTP (CRLF - Carriage Return Line Feed).
            Host: {host}\r\n:
            Đây là tiêu đề HTTP (header) bắt buộc trong HTTP/1.1, chỉ định tên miền hoặc địa chỉ của máy chủ (giá trị của biến host, ví dụ: example.com).
            Giúp máy chủ biết yêu cầu được gửi đến tên miền nào, đặc biệt khi máy chủ lưu trữ nhiều tên miền (virtual hosting).
            {host}: Biến được thay thế bằng tên miền thực tế (do f-string).
            \r\n: Kết thúc dòng tiêu đề.
            Connection: close\r\n:
            Tiêu đề HTTP chỉ định rằng kết nối sẽ được đóng sau khi máy chủ phản hồi.
            close: Yêu cầu máy chủ đóng kết nối TCP sau khi gửi phản hồi, thay vì giữ kết nối mở (như keep-alive).
            \r\n: Kết thúc dòng tiêu đề.
            \r\n\r\n:
            Chuỗi này gồm hai cặp CRLF, đánh dấu kết thúc phần tiêu đề của yêu cầu HTTP.
            Trong trường hợp yêu cầu GET, không có phần thân (body), nên chuỗi này báo hiệu rằng yêu cầu đã hoàn tất.
        '''
        secure_socket.send(request.encode())
        '''
        **`secure_socket`**: Đây là một đối tượng `ssl.SSLSocket`, tức là một socket đã được bọc với SSL/TLS (thường được tạo bởi `ssl.SSLContext.wrap_socket()`).
        -**`request.encode()`**:
        - Chuyển đổi chuỗi `request` thành dạng bytes (yêu cầu của phương thức `send`).
        - Theo mặc định, phương thức `encode()` sử dụng mã hóa UTF-8 để chuyển chuỗi thành bytes.
        - **`.send(...)`**:
        - Gửi dữ liệu bytes của yêu cầu HTTP đến máy chủ thông qua socket bảo mật.
        - Socket SSL/TLS đảm bảo dữ liệu được mã hóa trước khi gửi qua mạng.

        ### Tổng quan
        - Đoạn code này thực hiện một yêu cầu HTTP GET đơn giản đến máy chủ (được xác định bởi biến `host`) thông qua một kết nối bảo mật SSL/TLS.
        - Yêu cầu được định dạng theo chuẩn HTTP/1.1, bao gồm phương thức GET, tiêu đề Host, và Connection: close.
        - Socket bảo mật (`secure_socket`) được sử dụng để gửi yêu cầu một cách an toàn, thường trong ngữ cảnh kết nối HTTPS.
        '''

        # Nhận phản hồi
        response = b"" 
        
        '''
        response = b"":
        Khởi tạo biến response là một chuỗi bytes rỗng (b"").
        Biến này sẽ được sử dụng để tích lũy toàn bộ dữ liệu phản hồi nhận được từ máy chủ qua socket.
        Sử dụng kiểu bytes thay vì chuỗi thông thường (str) vì dữ liệu mạng được truyền dưới dạng bytes.
        '''
        
        while True:
            data = secure_socket.recv(4096)
            if not data:
                break
            response += data

        secure_socket.close()

        # Tách header và nội dung HTML
        response_str = response.decode(errors="ignore") #Chuyển đổi bytes thành chuỗi (errors="ignore"): nếu có bất kì bytes nào không chuyển đổi đc => bỏ qua chứ không để lỗi
        header_end = response_str.find("\r\n\r\n")
        '''
        Tìm vị trí của chuỗi \r\n\r\n (hai cặp CRLF - Carriage Return Line Feed) trong response_str.
        Trong phản hồi HTTP, \r\n\r\n đánh dấu ranh giới giữa phần tiêu đề (headers) và phần thân (body) của phản hồi.
        Phương thức find trả về chỉ số (index) của ký tự đầu tiên của \r\n\r\n nếu tìm thấy, hoặc -1 nếu không tìm thấy.
        Biến header_end lưu chỉ số này, biểu thị vị trí bắt đầu của \r\n\r\n.
        Ý nghĩa:
        Phần trước \r\n\r\n bao gồm dòng trạng thái (status line, ví dụ: HTTP/1.1 200 OK) và các tiêu đề HTTP (như Content-Type, Content-Length).
        Phần sau \r\n\r\n là nội dung thực tế (thường là HTML trong trường hợp yêu cầu GET đến một trang web).
        '''
        html_content = response_str[header_end + 4:]
        '''
        header_end + 4:
        header_end là vị trí bắt đầu của \r\n\r\n.
        Chuỗi \r\n\r\n có độ dài 4 ký tự, nên header_end + 4 là vị trí ngay sau \r\n\r\n, tức là bắt đầu của phần thân (body) của phản hồi HTTP.
        response_str[header_end + 4:]:
        Lấy một lát cắt (slice) của chuỗi response_str từ vị trí header_end + 4 đến cuối chuỗi.
        Kết quả là html_content, chứa phần thân của phản hồi HTTP, thường là nội dung HTML trong trường hợp yêu cầu GET đến một trang web.
        '''

        return(html_content)

    except socket.gaierror: #Xử lý ngoại lệlệ
        print(" Không thể phân giải tên miền.")
    except Exception as e:
        print(f" Lỗi: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Cách sử dụng: python tcp_fetch_html.py <url>")
        print("Ví dụ: python tcp_fetch_html.py www.cit.ctu.edu.vn")
    else:
        #fetch_html(sys.argv[1])
        html = fetch_html_https(sys.argv[1])
    
        if html.startswith("Lỗi:") or html.startswith("Không"):
            print(html)
        else:
            # Lưu HTML vào file
            with open("output.html", "w", encoding="utf-8") as f:
                f.write(html)
            
            # Mở file HTML trong trình duyệt
            webbrowser.open(f"file://{os.path.abspath('output.html')}")
	
#Kiểm tra yêu cầu:
# import requests
# r = requests.get("http://www.cit.ctu.edu.vn")
# print(r.text)

'''Run
%%bash
python tcp_fetch_html.py www.cit.ctu.edu.vn
'''