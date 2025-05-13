---
title: "Cloudflare từ A sang Á: Cloudflare Access"
date: 2025-05-07 10:00
author: "Hung Hoang"
description: "Tìm hiểu về Cloudflare Access - giải pháp bảo mật truy cập ứng dụng của Cloudflare"
categories:
  - cloudflare
  - security
tags:
  - cloudflare-101
  - access
  - zero-trust
---


!!! info "Cloudflare từ A sang Á"
    Chuỗi bài viết về các dịch vụ nền tảng của Cloudflare


**Cloudflare Access** là một dịch vụ SaaS nhằm bảo vệ các tài nguyên, ứng dụng (thường là nội bộ) khỏi truy cập công cộng bằng cách xác minh các request dựa vào user identity và device context nâng cao (vị trí, thời gian, loại thiết bị).

**Cloudflare Access** đóng vai trò như một Reverse Proxy trang bị tính năng xác thực người dùng (Authentication) nhằm bảo vệ các ứng dụng nội bộ thông qua kiến trúc phân tán toàn cầu của mạng lưới Cloudflare. Khác với các giải pháp proxy truyền thống, Cloudflare Access:

- Xác thực người dùng tại edge node gần nhất với họ trong mạng lưới hơn 250+ trung tâm dữ liệu toàn cầu, chứ không phải tại một máy chủ proxy tập trung
- Chuyển tiếp các yêu cầu đã được xác thực đến ứng dụng nội bộ qua kết nối an toàn, tối ưu hóa về hiệu suất nhờ định tuyến thông minh trên hạ tầng backbone riêng của Cloudflare

Vì vậy dịch vụ này được cho là:

✅ Giảm độ trễ đáng kể bằng cách xử lý xác thực tại edge, gần với người dùng nhất, thay vì buộc traffic phải đi qua một điểm trung tâm duy nhất

✅ Cung cấp khả năng chống DDoS và các tấn công mạng ngay tại edge node, trước khi traffic có thể đến được ứng dụng nội bộ

✅ Tự động mở rộng quy mô để đáp ứng nhu cầu tăng vọt mà không cần điều chỉnh phần cứng như các proxy truyền thống

![Cloudflare Access Overview](https://static.ssan.me/Cloudflare-access-thumbnail-01.png)


### 💡 Các đối tượng Cloudflare Access có thể bảo vệ

Họ quy ước gọi là "Application", các đối tượng chính sau:

- SaaS Application
- Self-hosted Application

Ngoài ra còn hỗ trợ

- Private Network
- Infrastructure: Database, Kubernetes Cluster, a server, .etc


## Cách thức hoạt động

<div class="embedded-content">
  <iframe
    src="https://static.ssan.me/Cloudflare+Access.drawio.html"
    width="100%"
    height="600px"
    scrolling="auto">
  </iframe>
</div>


Luồng bắt đầu khi người dùng nhập URL ứng dụng nội bộ của bạn vào trình duyệt (ví dụ: https://internal-app.company.com):

Cloudflare Access bảo vệ ứng dụng nội bộ bằng cách chặn request ban đầu, chuyển hướng người dùng chưa xác thực đến IdP được cấu hình, và tạo JWT cookie chứa thông tin định danh sau khi xác thực thành công. Sau đó, Access đánh giá JWT này với các chính sách bảo mật được thiết lập, chỉ chuyển tiếp request đến ứng dụng gốc nếu tất cả kiểm tra đều thành công, kèm theo thông tin người dùng trong HTTP header. Cloudflare duy trì phiên làm việc thông qua JWT cookie có thời hạn, kiểm tra chính sách với mỗi request và tự động làm mới token khi cần, tạo nên hệ thống bảo mật Zero Trust hoàn chỉnh không cần VPN.

Chi tiết xem tại [đây](./cloudflare-101-cloudflare-access-internals.html)

## 🧩 Các thành phần chính

### 🖥️ Applications

Như đã giới thiệu phần trên, đây là thành phần chính chúng ta cần cấu hình. Applications trong Cloudflare Access đại diện cho các ứng dụng nội bộ cần được bảo vệ. Mỗi Application được định nghĩa bởi một tập hợp domain hoặc path cụ thể (ví dụ: internal-app.company.com/* hoặc company.com/admin/*). Khi cấu hình Application, bạn cần xác định:

- 📝 Tên ứng dụng để nhận diện trong dashboard
- 🌐 Domain và path pattern cần bảo vệ
- ⏱️ Session duration (thời lượng phiên làm việc)
- 🚀 App Launcher visibility (hiển thị trong App Launcher)
- 🎨 Logo và mô tả (tùy chọn nhằm cá nhân hoá trang đăng nhập)

### 🛡️ Chính sách truy cập

Chính sách truy cập (Access Policies) là tập hợp các quy tắc xác định ai có thể truy cập vào Application. Mỗi Application có thể có nhiều chính sách, được đánh giá theo thứ tự ưu tiên. Mỗi chính sách bao gồm:

- ✅ Include rules: Xác định người dùng/nhóm được phép truy cập (điều kiện cho phép)
- ❌ Exclude rules: Xác định người dùng/nhóm bị chặn truy cập (điều kiện từ chối)
- 🔍 Require rules: Các điều kiện bổ sung mà người dùng phải đáp ứng (2FA, địa điểm, thiết bị...)

Cloudflare Access hỗ trợ nhiều loại điều kiện trong chính sách:
- 📧 Email/Domain/Group từ IdP
- 🌎 Country/IP Range giới hạn vị trí địa lý
- 📱 Device Posture kiểm tra tình trạng thiết bị
- 🕒 Time constraints giới hạn thời gian truy cập
- 🔐 Authentication method yêu cầu phương thức xác thực cụ thể

Chính sách được đánh giá theo nguyên tắc "first match": khi một request khớp với chính sách đầu tiên trong danh sách, quyết định cho phép/từ chối sẽ được áp dụng ngay lập tức.

### 🔑 Phương thức xác thực

Ngoài các Identity Provider (IdP) truyền thống như Okta, Azure AD, Google Workspace, chúng ta còn có thể sử dụng:

- **📧 One-time Code thông qua Email**: Người dùng nhập email, Cloudflare gửi mã xác thực tạm thời, người dùng nhập mã để được cấp quyền truy cập. Phù hợp cho khách/đối tác không nằm trong IdP của tổ chức.

- **🔖 Service Tokens**: Token tĩnh dùng cho các ứng dụng, API hoặc service-to-service communication, không liên kết với người dùng cụ thể.

- **🐙 GitHub**: Xác thực thông qua tài khoản GitHub, cho phép giới hạn truy cập theo tổ chức/team GitHub.

- **🔢 PIN Code**: Mã số cố định được cấu hình trước, thường dùng cho môi trường demo/POC.

- **🔄 SAML Authentication**: Tích hợp với bất kỳ Identity Provider hỗ trợ SAML 2.0.

- **🔐 Mutual TLS (mTLS)**: Xác thực dựa trên certificate, thường dùng cho IoT và service-to-service.

Cloudflare Access cho phép kết hợp nhiều phương thức xác thực, tạo nên mô hình xác thực đa lớp. Ví dụ, bạn có thể yêu cầu người dùng đăng nhập qua Okta VÀ phải truy cập từ IP công ty, hoặc đăng nhập qua Azure AD VÀ sử dụng thiết bị được quản lý bởi công ty.

## 🚀 Kết luận: Triển khai cực kỳ nhanh chóng!
Điểm cực kỳ ấn tượng về Cloudflare Access là tốc độ triển khai siêu nhanh! Sau khi cấu hình các mục trên, chỉ sau **5-10 phút** thôi là dịch vụ đã sẵn sàng hoạt động ! Không cần chờ đợi lâu, không setup phức tạp, mọi thứ đều được Cloudflare xử lý một cách mượt mà trong thời gian bạn uống hết một ly cà phê. ☕

Quan trọng hơn: siêu hời - Cloudflare còn có **Free Plan** để bạn test thử! Triển khai, thử nghiệm, xem có hợp với team không mà chẳng tốn xu nào! 💸 Thử ngay nào
