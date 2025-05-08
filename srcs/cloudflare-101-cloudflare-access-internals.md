---
title: 'Cloudflare Access Internals: Tìm hiểu luồng xác thực'
date: 2025-05-08 10:00
author: "Hung Hoang"
description: "Deep dive into Cloudflare Access internals, exploring how authentication and authorization work behind the scenes"
categories: ["cloudflare", "security"]
tags: ["cloudflare-access", "zero-trust", "authentication", "jwt", "oauth"]
hide: true
---

## Giới thiệu

Bài viết này là tài liệu tham khảo chuyên sâu về luồng xác thực (authentication flow) và cơ chế hoạt động nội bộ của Cloudflare Access. Không như các hướng dẫn cơ bản, tài liệu này đi sâu vào chi tiết kỹ thuật đằng sau mỗi bước trong quy trình xác thực, từ request ban đầu đến việc duy trì phiên làm việc.

## Cách thức hoạt động

<div class="embedded-content">
  <iframe
    src="https://static.ssan.me/Cloudflare+Access.drawio.html"
    width="100%"
    height="500px"
    frameborder="0"
    scrolling="auto">
  </iframe>
</div>


### 1. Người dùng gửi request ban đầu

Khi người dùng nhập URL ứng dụng nội bộ của bạn vào trình duyệt (ví dụ: https://internal-app.company.com):

- Request đầu tiên đi từ trình duyệt của người dùng
- Request này đến mạng edge của Cloudflare (thay vì đi thẳng đến máy chủ của bạn)
- Cloudflare edge kiểm tra và nhận ra rằng domain này được bảo vệ bởi Cloudflare Access

### 2. Chuyển hướng đến trang xác thực

- Cloudflare Access kiểm tra xem người dùng đã có cookie xác thực hợp lệ chưa
- Vì đây là lần truy cập đầu tiên, người dùng chưa có cookie xác thực
- Access chuyển hướng người dùng đến trang đăng nhập của Cloudflare
- Trang này hiển thị các Identity Provider (IdP) mà quản trị viên đã cấu hình (Okta, Azure AD, Google, v.v.)

### 3. Xác thực và xác nhận danh tính người dùng qua IdP

- Người dùng chọn IdP họ muốn sử dụng và được chuyển hướng đến trang đăng nhập của IdP
- Quá trình này sử dụng chuẩn OAuth/OIDC để trao đổi thông tin xác thực
- Người dùng nhập thông tin đăng nhập và có thể hoàn thành xác thực hai yếu tố (2FA) nếu được cấu hình
- IdP xác minh thông tin đăng nhập và tạo mã thông báo (authorization code)
- IdP chuyển hướng người dùng trở lại Cloudflare cùng với mã này
- Cloudflare Access đổi mã này lấy thông tin chi tiết về người dùng từ IdP (danh tính, nhóm, thuộc tính)

### 4. Tạo JWT, đánh giá chính sách và cấp quyền truy cập

- Cloudflare Access tạo JSON Web Token (JWT) chứa thông tin người dùng, nhóm, thời gian hết hạn và chữ ký số
- JWT được lưu dưới dạng cookie trong trình duyệt của người dùng
- Cloudflare Access kiểm tra JWT với các chính sách truy cập (policy) do quản trị viên thiết lập
- Access đánh giá nhiều yếu tố: email, nhóm, thiết bị, vị trí địa lý, thời gian truy cập
- Nếu người dùng vượt qua tất cả các kiểm tra, Access cấp quyền và chuyển hướng về URL ban đầu
- Nếu không đạt yêu cầu, Access hiển thị trang từ chối truy cập

### 5. Chuyển tiếp request và xử lý ứng dụng

- Trình duyệt người dùng gửi lại request ban đầu kèm theo cookie JWT
- Cloudflare edge xác minh cookie JWT là hợp lệ và chưa hết hạn
- Cloudflare thiết lập kết nối bảo mật với máy chủ ứng dụng nội bộ
- Cloudflare chuyển tiếp request kèm thông tin người dùng trong header HTTP
- Máy chủ ứng dụng xử lý request và gửi phản hồi
- Phản hồi được định tuyến ngược qua mạng Cloudflare đến người dùng

### 6. Duy trì phiên làm việc

- JWT cookie có thời gian sống nhất định (thường là vài giờ)
- Các request tiếp theo sẽ tự động sử dụng cookie này mà không cần đăng nhập lại
- Cloudflare kiểm tra chính sách với mỗi request (không chỉ lần đầu)
- Khi cookie sắp hết hạn, Cloudflare có thể làm mới nó một cách tự động
- Khi người dùng đóng trình duyệt hoặc đăng xuất, cookie sẽ bị xóa
