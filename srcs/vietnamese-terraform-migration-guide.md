---
title: 'Tái Cấu Trúc Terraform: Chuyển Đổi Từ State Monolithic Sang Kiến Trúc Mô-đun Theo Môi Trường'
date: 2025-04-20 10:00
description: 'Hướng dẫn sơ khai tái cấu trúc Terraform từ state đơn lẻ sang kiến trúc module theo môi trường, giúp quản lý state hiệu quả, tái sử dụng mã và giảm rủi ro triển khai.'
category: terraform
tags:
  - terraform
  - migration
  - module
  - môi-trường
  - IaC
---

Trong quá trình phát triển công cụ tự đông hoá truy vấn Google Maps theo địa chỉ dưới dạng văn bản trên nền tảng Instagram (chi tiết tại [đây](https://www.facebook.com/groups/j2team.community/posts/2642859852712785/)), nhận thấy sự cần thiết trong việc chuyển đổi cấu trúc quản lí trạng thái của Terraform từ dạng phẳng, phi cấu trúc, monolith sang dạng mô-đun, phân tách môi trường theo file directory

# Tái Cấu Trúc Terraform: Chuyển Đổi Từ State Monolithic Sang Kiến Trúc Mô-đun Theo Môi Trường

Hướng dẫn sơ khai các bước để tổ chức lại codebase Terraform của bạn để có sự tách biệt, tái sử dụng và triển khai an toàn hơn.

---

## 1. Tổ Chức State Ban Đầu

**Cấu Trúc & Quy Trình**
- Một thư mục gốc `terraform/` với `main.tf`, `variables.tf`, v.v.
- Một file state duy nhất (`terraform.tfstate`), thường được lưu trữ trong S3 hoặc cục bộ.
- Sử dụng `.tfvars` (`dev.tfvars`, `prod.tfvars`) ghi đè biến để phân tách môi trường.

**Lợi ích**
- Cấu trúc đơn giản, trực quan đối với người mới và dự án nhỏ.

**Hạn Chế & Nhược Điểm**
Sẽ bộc lộ khi số lượng tài nguyên tăng lên:
- State phình to: tất cả tài nguyên (dev/staging/prod) đều nằm trong một file.
- Triển khai rủi ro: vô tình thay đổi tài nguyên production.
- Mô-đun hóa kém: mọi thay đổi đối với API, IAM, Lambda đều nằm trong cùng một file.
- Không có ranh giới rõ ràng: khó để đào tạo thành viên mới hoặc phân chia trách nhiệm.

---

![Modularize Terraform management](https://static.ssan.me/tf_modularization_dont_do.png)

## 2. Giới Thiệu Về Module Terraform

**Module Là Gì?**
Một thư mục chứa mã Terraform (resources, inputs, outputs) mà bạn có thể gọi từ một cấu hình khác.
- **Root module**: `main.tf` cấp cao nhất và các file liên quan.
- **Child modules**: các khối xây dựng có thể tái sử dụng (ví dụ: `modules/lambda/`).

**Kiến Trúc và Giao Tiếp Của Module**

Một module Terraform không chỉ là một thư mục mã—nó là một đối tượng đóng gói độc lập với một hợp đồng (ràng buộc) rõ ràng về cách tương tác với thế giới bên ngoài thông qua biến (`var`):

```
modules/lambda/
├── **main.tf**         # Định nghĩa tài nguyên chính
├── **variables.tf**    # Tham số đầu vào (API của module)
├── **outputs.tf**      # Giá trị được hiển thị cho module cha
├── locals.tf       # Tính toán và biến đổi nội bộ
├── data.tf         # Data sources và lookups
└── README.md       # Tài liệu về mục đích, inputs, và outputs
```

Mỗi file có một mục đích cụ thể:

**main.tf** - Chứa và tập hợp các định nghĩa tài nguyên cốt lõi (thường đi kèm với nhau) để thực hiện một hành động/tính năng hoàn chỉnh mà module tạo và quản lý. Đối với module Lambda, nó sẽ bao gồm:

```
resource "aws_lambda_function" "functions" {
  for_each = var.functions

  function_name = "${var.name_prefix}-${each.key}"
  handler       = each.value.handler
  runtime       = each.value.runtime
  role          = var.execution_role_arn

  filename         = each.value.source_file
  source_code_hash = filebase64sha256(each.value.source_file)

  memory_size = each.value.memory_size
  timeout     = each.value.timeout

  environment {
    variables = merge(var.common_environment_variables, each.value.environment_variables)
  }

  tags = merge(var.common_tags, each.value.tags)
}

# Các tài nguyên bổ sung như permissions, CloudWatch log groups, v.v.
```

**variables.tf** - Định nghĩa các tham số đầu vào của module, với mô tả và ràng buộc kiểu:

```
variable "name_prefix" {
  description = "Tiền tố được thêm vào trước tất cả tên tài nguyên"
  type        = string
}

variable "functions" {
  description = "Bản đồ các hàm Lambda cần tạo"
  type = map(object({
    handler               = string
    runtime               = string
    source_file           = string
    memory_size           = number
    timeout               = number
    environment_variables = map(string)
    tags                  = map(string)
  }))
}

variable "execution_role_arn" {
  description = "ARN của IAM role được sử dụng bởi các hàm Lambda"
  type        = string
}

variable "common_environment_variables" {
  description = "Biến môi trường áp dụng cho tất cả các hàm"
  type        = map(string)
  default     = {}
}

variable "common_tags" {
  description = "Tags áp dụng cho tất cả tài nguyên"
  type        = map(string)
  default     = {}
}
```

**outputs.tf** - Định nghĩa các giá trị mà module hiển thị cho các module cha:

```
output "function_arns" {
  description = "ARNs của các hàm Lambda đã tạo"
  value = {
    for name, function in aws_lambda_function.functions : name => function.arn
  }
}

output "function_names" {
  description = "Tên của các hàm Lambda đã tạo"
  value = {
    for name, function in aws_lambda_function.functions : name => function.function_name
  }
}

output "invoke_urls" {
  description = "URLs cơ sở để gọi các hàm Lambda (nếu tích hợp API Gateway được bật)"
  value = {
    for name, _ in var.functions :
    name => aws_apigatewayv2_stage.api[name].invoke_url
    if contains(keys(aws_apigatewayv2_stage.api), name)
  }
}
```

![Module with input and output](https://static.ssan.me/tf_module_input_output.png)

**Sự Kết Hợp và Tái Sử Dụng Module**

Các module có thể gọi các module khác, tạo thành một mẫu kết hợp. Điều này cho phép bạn xây dựng các trừu tượng cấp cao hơn:

```
# Bên trong một module "serverless_api" kết hợp các module khác
module "lambda" {
  source = "../lambda"

  name_prefix        = var.name_prefix
  functions          = var.functions
  execution_role_arn = module.iam.lambda_execution_role_arn
}

module "api_gateway" {
  source = "../api_gateway"

  name_prefix     = var.name_prefix
  api_name        = "${var.name_prefix}-api"
  lambda_function = module.lambda.function_arns["api_handler"]
  stage_name      = var.environment
}

module "iam" {
  source = "../iam"

  name_prefix = var.name_prefix
  services    = ["lambda.amazonaws.com"]
}
```

**Phiên Bản Module**

Để đảm bảo tính ổn định, bạn nên đánh phiên bản cho các module của mình bằng một trong những cách tiếp cận sau:

1. **Tham chiếu Git** - Gắn với một commit hoặc tag cụ thể:
   ```
   module "lambda" {
     source = "git::https://github.com/company/terraform-modules.git//modules/lambda?ref=v1.2.3"
     # Cấu hình module...
   }
   ```

2. **Terraform Registry** - Cho các module trong registry công khai hoặc riêng tư:
   ```
   module "lambda" {
     source  = "terraform-aws-modules/lambda/aws"
     version = "2.7.0"
     # Cấu hình module...
   }
   ```

3. **Đường dẫn cục bộ với phiên bản** - Cho phát triển nội bộ:
   ```
   module "lambda" {
     source = "../../modules/lambda"  # Với quy trình kiểm soát phiên bản nội bộ
     # Cấu hình module...
   }
   ```

**Lợi Ích**
- Đóng gói: nhóm các tài nguyên liên quan (Lambda + aliases + permissions).
- Tái sử dụng: chia sẻ các mẫu tiêu chuẩn giữa các dự án.
- Tùy biến: hiển thị inputs (`var.memory_size`, `var.aliases`) và outputs.
- Đánh phiên bản: gắn nguồn module với một Git tag hoặc phiên bản registry.

**Cách Sử Dụng**
```
module "lambda" {
  source             = "../../modules/lambda"
  functions          = local.lambda_functions
  execution_role_arn = module.iam.execution_role_arn
}
```
- Định nghĩa inputs (maps, lists, primitives).
- Sử dụng outputs (`module.lambda.alias_arns["myfunc_dev"]`).
- Tận dụng `for_each` / `count` cho tính năng động.

---

## 3. Cấu Trúc Mới: Mô-đun Hóa, Hướng Theo Môi Trường

```text
terraform/
├── environments/
│   ├── dev/
│   │   └── main.tf
│   ├── staging/
│   │   └── main.tf
│   └── prod/
│       └── main.tf
└── modules/
    ├── lambda/
    ├── iam/
    ├── api_gateway/
    └── cloudwatch/
```

- **Thư mục theo môi trường**: cô lập state, vars, backends.
- **Modules**: triển khai các vấn đề cốt lõi (compute, IAM, logging, API).
- **Locals & tagging**: định nghĩa `local.project`, `local.environment`, `local.common_tags` trong mỗi môi trường.

---

## 4. Migrate & Quản Lý State
Ở phần phần này, mính sẽ giới thiệu qua các lệnh phổ biển của Terraform CLI để dịch chuyển state và các tài nguyên liên quan.

Có it nhất 2 cách để thực hiện:
- `terraform state rm` và `terraform import` để import tài nguyên vào module mới.
- Sử dụng `terraform state mv` để di chuyển tài nguyên vào module mới.

📌 Đi kèm là 2 công cụ đắc lực để theo dõi hiện trạng state: `terraform state list` và `terraform state show`.


### **Sử dụng `terraform state rm` và `terraform import` để import tài nguyên vào module mới**

Flow cơ bản:
1. khởi tạo state cho từng môi trường, ở đây là `dev`

```bash
cd terraform/environments/dev
terraform init \
  -backend-config="key=dev/terraform.tfstate"
```

2. Định nghĩa module ở môi trường mới

```
# my_project/terraform/modules/lambda/main.tf
resource "aws_lambda_function" "my_lambda_function" {
  function_name = var.function_name

  # Function-specific configuration
  handler          = var.handler
  runtime          = var.runtime
}
```

3. Định nghĩa các biến đầu vào cho module trên
```
# my_project/terraform/modules/lambda/variables.tf
variable "function_name" {
  type = string
}

variable "handler" {
  type = string
}

variable "runtime" {
  type = string
}
```

4. Gọi module lambda trong file `main.tf` của môi trường mới

Để đơn giản, chúng ta hardcode các tham số đầu vào, tuy nhiên thực tế chúng ta nên định nghĩa các biến đầu vào trong `variables.tf` kết hợp `terraform.tfvars` của module.
```
# my_project/terraform/environments/dev/main.tf
module "lambda" {
  source = "../../modules/lambda"

  function_name = "my_lambda_function"
  handler       = "index.handler"
  runtime       = "python3.8"
}
```

5. Xác định tài nguyên cần di chuyển ở môi trường cũ`
Tại môi trường cũ, hãy xem các tài nguyên hiện có rồi xoá tài nguyên khỏi file trạng thái:
```
# my_project/
> terraform state list
> terraform state show aws_lambda_function.my_lambda_function
> terraform state rm aws_lambda_function.my_lambda_function
```
Rồi xoá thủ công tài nguyên trên khỏi code ở môi trường cũ.

6. Import tài nguyên vào module mới
```
# my_project/terraform/environments/dev
> terraform import module.lambda.aws_lambda_function.my_lambda_function <resource_id>
```
Bạn có thể phải cần truyền các tham số đầu vào thông qua flag `--var` hoặc `--var-file`.
Ví dụ:
```
> terraform import module.lambda.aws_lambda_function.my_lambda_function <resource_id> --var "function_name = 'my_lambda_function'" --var "handler = 'index.handler'" --var "runtime = 'python3.8'"
```

---

## 5. Xác Minh Quá Trình Chuyển Đổi
**Xác Thực Bằng Plan**
   ```bash
   terraform plan
   ```
   - Xác nhận không có thay đổi (các tài nguyên trỏ đến cùng một cơ sở hạ tầng vật lý).

- **Liệt kê state**
  ```bash
  terraform state list
  ```
- **Hiển thị chi tiết tài nguyên**
  ```bash
  terraform state show module.lambda.aws_lambda_function.functions["ig_post_extractor"]
  ```
- **Kết quả plan**
  - Không có thay đổi đồng nghĩa với thành công.
  - Bất kỳ sự khác biệt nào cho thấy một sự ánh xạ sai cần phải sửa bằng `state mv` hoặc cập nhật biến.
- **Triển Khai Qua Các Môi Trường**
   - Lặp lại init/import/plan trong `staging` và `prod`.
   - Mỗi môi trường sử dụng khóa backend state riêng (`staging/terraform.tfstate`, v.v.).

**Cấu Trúc Cuối Cùng Thành Công**

Sau khi di chuyển, cấu trúc của chúng ta trông như thế này:

```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   └── terraform.tfstate (trong S3)
│   ├── staging/
│   │   ├── main.tf
│   │   └── terraform.tfstate (trong S3)
│   └── prod/
│       ├── main.tf
│       └── terraform.tfstate (trong S3)
└── modules/
    ├── lambda/
    ├── api_gateway/
    ├── iam/
    └── cloudwatch/
```

---

## 6. Kết Quả

- **Tách biệt**: mỗi môi trường có state riêng, không có sự nhiễm chéo.
- **Mô-đun hóa**: các module đóng gói các phương pháp hay nhất và dễ dàng đánh phiên bản.
- **Lặp lại**: tạo môi trường mới bằng cách sao chép một thư mục và điều chỉnh các biến.
- **An toàn**: các lệnh `plan` + `state` đảm bảo di chuyển có kiểm soát, không bị gián đoạn.
- **Dễ bảo trì**: thành viên mới trong nhóm có thể nhanh chóng hiểu cấu trúc codebase.
- **Quản trị**: dễ dàng triển khai quy trình phê duyệt cho từng môi trường.

Sau khi di chuyển, các nhóm có thể làm việc độc lập trên các môi trường hoặc module khác nhau, với ranh giới rõ ràng và giảm nguy cơ thay đổi vô tình các tài nguyên sản xuất.
