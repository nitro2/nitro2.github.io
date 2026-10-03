# Ghi chép kinh tế

Blog tĩnh host trên GitHub Pages: https://nitro2.github.io

## Đăng bài mới
1. Đặt file HTML tự chứa vào `posts/`, đặt tên theo dạng `YYYY-MM-DD-slug.html`.
   Trong `<head>` của file phải có ba thẻ: `<title>`, `<meta name="description">` và `<meta name="date" content="YYYY-MM-DD">`.
2. Chạy `python3 build.py` để tạo lại trang chủ, `feed.xml` và `sitemap.xml`.
3. Chạy `git add -A && git commit -m "Bài mới: ..." && git push`. GitHub Pages tự cập nhật sau khoảng 1 phút.

Muốn đổi tên hoặc mô tả blog, sửa `SITE_TITLE` và `SITE_DESC` ở đầu `build.py`.

## Trang theo dõi `/monitor/`
Thư mục `monitor/` do máy luca tự sinh và tự push sau mỗi phiên giao dịch: thứ 2 đến thứ 6, lúc 15:40 và 17:30 giờ Việt Nam. Máy luca dùng deploy key riêng cho repo này. Code nằm ở `~/Projects/Dreamer/econo/vnmonitor`. Vì luca push vào repo hằng ngày, anh nhớ chạy `git pull` trước khi sửa blog trên Mac. Không sửa tay thư mục `monitor/`.

Bài "Dòng tiền và chứng khoán Việt Nam" được sinh từ `~/Projects/Dreamer/econo/build_article.py`.
