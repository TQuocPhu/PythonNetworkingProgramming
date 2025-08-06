import urllib.request
import re
from urllib.parse import urljoin, urlparse
from collections import deque

visited_urls = set()
found_emails = set()

def is_same_domain(base_url, target_url):
    return urlparse(base_url).netloc == urlparse(target_url).netloc

def crawl(start_url):
    queue = deque([start_url])

    while queue:
        url = queue.popleft()
        if url in visited_urls:
            continue

        print(f"\n Đang kiểm tra: {url}")
        visited_urls.add(url)

        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                content_type = response.headers.get("Content-Type", "")
                if "text/html" not in content_type:
                    continue

                html = response.read().decode(errors='ignore')


                print("\n--- Nội dung HTML ---")
                print(html[:500])  # In 500 ký tự đầu tiên
                print("--- Kết thúc trích HTML ---\n")

                # Tìm email
                emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', html)
                found_emails.update(emails)

                # Tìm URL
                urls = re.findall(
                    r'https?://(?:[a-zA-Z0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F]{2}))+',
                    html
                )

                for link in urls:
                    full_url = urljoin(url, link)
                    if is_same_domain(start_url, full_url) and full_url not in visited_urls:
                        queue.append(full_url)

        except Exception as e:
            print(f"Lỗi khi truy cập {url}: {e}")

def main():
    start_url = input("Nhập URL trang web (VD: https://example.com): ").strip()
    print("Bắt đầu tìm kiếm email...\n")
    crawl(start_url)

    print("\nHoàn tất. Các email tìm thấy:")
    if found_emails:
        for email in sorted(found_emails):
            print("📧", email)
    else:
        print("Không tìm thấy email nào.")

if __name__ == "__main__":
    main()