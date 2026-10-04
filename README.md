# Ghi chép kinh tế

Blog tĩnh host trên GitHub Pages: https://nitro2.github.io

## Đăng bài mới
1. Đặt file HTML tự chứa vào `posts/`, đặt tên theo dạng `YYYY-MM-DD-slug.html`.
   Trong `<head>` của file phải có ba thẻ: `<title>`, `<meta name="description">` và `<meta name="date" content="YYYY-MM-DD">`.
2. Chạy `python3 build.py` để tạo lại trang chủ, `feed.xml` và `sitemap.xml`.
3. Chạy `git add -A && git commit -m "Bài mới: ..." && git push`. GitHub Pages tự cập nhật sau khoảng 1 phút.

Muốn đổi tên hoặc mô tả blog, sửa `SITE_TITLE` và `SITE_DESC` ở đầu `build.py`.

## Trang tự động `/monitor/` và `/stablecoin/`
Hai thư mục này do một máy chủ tự sinh và tự push mỗi ngày. Vì vậy cần chạy `git pull` trước khi sửa blog, và không sửa tay hai thư mục này.

Code sinh trang và các bài viết nằm trong repo riêng `econo`.
