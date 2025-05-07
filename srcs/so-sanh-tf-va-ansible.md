---
title: 'TERRAFORM - ANSIBLE: SỰ PHÂN ĐỊNH TRONG MÔ HÌNH CẤU HÌNH DEVOPS'
date: 2025-05-07 10:00
description: Phân tích chi tiết sự khác biệt giữa mô hình cấu hình declarative của Terraform và procedural declarative của Ansible.
category: devops
---

# TERRAFORM - ANSIBLE: SỰ PHÂN ĐỊNH TRONG MÔ HÌNH CẤU HÌNH DEVOPS 🌐
![Tf and Ansible head to head](https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F5o4mzuyhqt9luao3i3eg.png)

## 1. Tổng quan 🛠️

### Terraform
Terraform là một công cụ Infrastructure as Code (IaC) mã nguồn mở được phát triển bởi HashiCorp, tập trung vào việc cung cấp và quản lý cơ sở hạ tầng cloud và on-premises. Terraform sử dụng phương pháp **declarative** thuần túy. 🌟

### Ansible
Ansible là một công cụ tự động hóa, mã nguồn mở được phát triển bởi Red Hat, khéo léo khoác lên mình chiếc áo choàng declarative nhưng thực chất vẫn tuân thủ triết lý imperative, nên thường được gán nhãn là **procedural declarative**. 🤖

## 2. Mô hình Declarative vs Imperative 🔄

### Declarative Configuration (Cấu hình khai báo) ✍️
- Mô tả **trạng thái mong muốn** của hệ thống
- Công cụ tự quyết định cách đạt được trạng thái đó
- Tập trung vào "CÁI GÌ" (what), không phải "LÀM THẾ NÀO" (how)
- Duy trì trạng thái (state) để biết những gì đã tồn tại

### Imperative Configuration (Cấu hình mệnh lệnh) 🧩
- Xác định **chuỗi các lệnh cụ thể** để thực hiện
- Người dùng đặc tả chính xác cách thực hiện từng bước
- Tập trung vào "LÀM THẾ NÀO" (how) để đạt được kết quả
- Thường không theo dõi trạng thái hiện tại của hệ thống

## 3. Phân tích sâu về Terraform: Declarative thuần túy 🌱

### Ưu điểm của cách tiếp cận Declarative
- **Idempotency**: Có thể chạy nhiều lần mà không gây ra tác dụng phụ 🔄
- **Consistency**: Đảm bảo trạng thái cuối cùng luôn nhất quán ✅
- **Dễ đọc**: Code mô tả chính xác cái gì sẽ được tạo ra 📖
- **Quản lý thay đổi**: Dễ dàng thêm, sửa, xóa tài nguyên qua mã dựa trên đồ thị phụ thuộc giữa các tài nguyên ✏️

## 4. Phân tích sâu về Ansible: "Procedural Declarative" ⚙️

### Tính chất "Procedural Declarative"
- **Declarative**: Mô tả trạng thái mong muốn trong modules (state: present, absent, etc.)
- **Task-based**: Thực thi các task theo thứ tự từ trên xuống 📋
- **Procedural**: Các task được thực thi tuần tự, không tự động giải quyết phụ thuộc
- **Agentless**: Không yêu cầu agent trên máy đích, sử dụng SSH/WinRM 🔒
- **Limited State Management**: Không duy trì trạng thái tổng thể của hệ thống
- **Idempotency**: Cố gắng đạt được idempotency nhưng đòi hỏi lập trình viên phải đảm bảo

## 5. So sánh qua ví dụ cụ thể 🔍

### Ví dụ 1: Triển khai máy chủ web 🌐

#### Cách tiếp cận Declarative (Terraform)
Với Terraform, bạn khai báo: "Tôi muốn có 3 máy chủ web, mỗi máy có 2GB RAM, sử dụng hệ điều hành Ubuntu 22.04, và tất cả đều nằm trong nhóm bảo mật web_servers."

Terraform sẽ:
- Tự động xác định có cần tạo mới, cập nhật hay xóa máy chủ nào không
- Tự quản lý trình tự tạo tài nguyên (ví dụ: tạo network trước, sau đó mới tạo máy chủ)
- Đảm bảo trạng thái cuối cùng luôn khớp với mô tả, bất kể trạng thái ban đầu

#### Cách tiếp cận Procedural Declarative (Ansible)
Với Ansible, bạn sẽ viết:
1. "Tạo 3 máy chủ web với 2GB RAM và Ubuntu 22.04"
2. "Cấu hình mỗi máy chủ để chạy dịch vụ web"
3. "Thêm các máy chủ vào nhóm bảo mật web_servers"

Ansible sẽ:
- Thực hiện tuần tự từng bước theo thứ tự đã định
- Sử dụng các module để đạt được trạng thái mong muốn cho từng bước
- Không tự động theo dõi trạng thái tổng thể của hệ thống

### Ví dụ 2: Triển khai ứng dụng 📦

#### Cách tiếp cận Declarative (Terraform)
Với Terraform: "Ứng dụng của tôi cần 1 cơ sở dữ liệu, 2 máy chủ ứng dụng, và 1 cân bằng tải ở phía trước. Cơ sở dữ liệu cần kết nối với các máy chủ ứng dụng, và cân bằng tải cần phân phối lưu lượng đến các máy chủ ứng dụng."

Terraform sẽ:
- Tạo một đồ thị phụ thuộc giữa các tài nguyên
- Xác định thứ tự tạo tài nguyên (cơ sở dữ liệu → máy chủ ứng dụng → cân bằng tải)
- Đảm bảo tất cả các kết nối và quan hệ phụ thuộc được đáp ứng

#### Cách tiếp cận Procedural Declarative (Ansible)
Với Ansible:
1. "Tạo cơ sở dữ liệu với cấu hình X"
2. "Tạo 2 máy chủ ứng dụng với cấu hình Y"
3. "Cấu hình kết nối giữa cơ sở dữ liệu và máy chủ ứng dụng"
4. "Tạo cân bằng tải với cấu hình Z"
5. "Cấu hình cân bằng tải để phân phối lưu lượng đến các máy chủ ứng dụng"

Ansible sẽ:
- Thực hiện từng bước theo thứ tự đã định
- Nhà phát triển phải xác định rõ thứ tự thực hiện
- Sử dụng các biến và đăng ký kết quả để truyền thông tin giữa các bước

## 6. Triết lý Immutable vs Mutable Infrastructure 🏗️

### Immutable Infrastructure: "Không sửa, chỉ thay" 🔄
Immutable Infrastructure là phương pháp trong đó các thành phần cơ sở hạ tầng **không bao giờ được sửa đổi** sau khi triển khai. Thay vì cập nhật cấu hình trên máy chủ đang chạy, toàn bộ máy chủ được thay thế bằng phiên bản mới đã được cấu hình sẵn.

**Đặc điểm chính:**
- Máy chủ được xem như "gia súc" (cattle), không phải "thú cưng" (pet) 🐄
- Cập nhật = Hủy cũ + Tạo mới
- Dựa vào các template, image, snapshot 📸
- Loại bỏ "configuration drift" và "snowflake servers" ❄️

### Mutable Infrastructure: "Sửa chữa tại chỗ" 🔧
Mutable Infrastructure là phương pháp truyền thống, trong đó các thành phần cơ sở hạ tầng được **cập nhật và sửa đổi tại chỗ** khi cần thiết.

**Đặc điểm chính:**
- Máy chủ được xem như "thú cưng" cần chăm sóc 🐕
- Thực hiện các thay đổi trực tiếp trên hệ thống đang chạy
- Dễ dẫn đến "configuration drift"
- Lịch sử thay đổi có thể không được ghi lại đầy đủ

### Terraform: Người ủng hộ trung thành của Immutable Infrastructure 🌟

Terraform, với triết lý declarative thuần túy, là công cụ lý tưởng cho Immutable Infrastructure:
- **Quản lý toàn diện**: Tạo và quản lý toàn bộ vòng đời của tài nguyên
- **Tất cả hoặc không có gì**: Thay đổi tài nguyên thường đồng nghĩa với việc tạo mới và hủy cái cũ
- **Nhất quán**: Đảm bảo môi trường luôn ở trạng thái đã định nghĩa
- **Dễ dàng roll back**: Quay lại version cũ chỉ đơn giản là apply lại cấu hình cũ

Terraform giống như một kiến trúc sư khó tính: "Nếu cần thay đổi, tôi sẽ xây lại từ đầu!" 🏗️

### Ansible: "Kẻ đa năng" trong thế giới infrastructure 🔧

Ansible, với bản chất procedural declarative, thích nghi tốt với Mutable Infrastructure nhưng cũng có thể hỗ trợ Immutable:

**Trong thế giới Mutable:**
- **Chuyên gia "chỉnh sửa"**: Thay đổi cấu hình trên các máy chủ đang chạy
- **Linh hoạt**: Thực hiện các thay đổi nhỏ mà không cần rebuild toàn bộ
- **Nhanh chóng**: Không cần chu kỳ tạo-hủy cho mỗi thay đổi nhỏ

**Hỗ trợ Immutable khi cần:**
- Xây dựng các image (AMI, Docker)
- Cấu hình ban đầu cho các instance mới
- Phần của pipeline CI/CD cho immutable deployments

Ansible giống như một thợ sửa chữa đa năng: có thể xây mới, nhưng cũng rất giỏi trong việc sửa chữa tại chỗ! 🛠️

![Tf and Ansible as Human](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/gtfrobfeekkxrwnmqiji.png)


## 7. Trường hợp sử dụng phù hợp 🎯

### Khi nào nên sử dụng Terraform
- **Provisioning hạ tầng**: Tạo mới toàn bộ cơ sở hạ tầng 🏗️
- **Quản lý tài nguyên cloud**: AWS, Azure, GCP, etc. ☁️
- **Kiến trúc bất biến (Immutable Infrastructure)**: Tạo mới thay vì cập nhật 🔄
- **Quản lý trạng thái phức tạp**: Nhiều tài nguyên phụ thuộc lẫn nhau 🔗

### Khi nào nên sử dụng Ansible
- **Cấu hình máy chủ**: Cài đặt phần mềm, cập nhật cấu hình 🖥️
- **Triển khai ứng dụng**: Deployment pipelines 🚀
- **Tự động hóa tác vụ lặp đi lặp lại**: Patches, updates 🔄
- **Điều phối nhiều máy chủ**: Các tác vụ cần thực hiện đồng thời trên nhiều máy ⚡

### Kết hợp cả hai công cụ 🤝
Mô hình phổ biến:
1. Sử dụng **Terraform** để provision infrastructure
2. Sử dụng **Ansible** để cấu hình và triển khai ứng dụng

## 8. Kết luận 🏁

Terraform và Ansible đại diện cho hai triết lý khác nhau trong quản lý hạ tầng và tự động hóa:

- **Terraform**: Declarative thuần túy, tập trung vào việc quản lý trạng thái và mối quan hệ phụ thuộc giữa các tài nguyên.
- **Ansible**: Procedural declarative, kết hợp giữa mô tả trạng thái mong muốn và thực thi tuần tự.

Cả hai công cụ đều có giá trị riêng và thường được sử dụng bổ sung cho nhau trong các pipeline DevOps hiện đại. Hiểu rõ sự khác biệt giữa cách tiếp cận declarative và imperative giúp đội ngũ DevOps lựa chọn công cụ phù hợp cho từng loại tác vụ. 🚀
