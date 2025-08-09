---
title: Triển khai AWS Lambda functions nay đã dễ dàng hơn với Github Actions
date: 2025-08-09 21:00
description: Sứ dụng action aws-actions/aws-lambda-deploy để triển khai Lambda function nhanh chóng thay vì các bước thủ công sử dụng AWS CLI
category: blog
tags:
    - aws
    - github
---

## Tin vui cho cộng đồng Serverless! 🚀

Ngày 07 tháng 8 vừa rồi, AWS vừa release action `aws-actions/aws-lambda-deploy` tích hợp trong Github Actions nhằm cập nhật cấu hình và mã nguồn của Lambda functions trên môi trường AWS.

!!! ìnfo Việc deploy Lambda trước kia như thế nào?
    Developers cần định nghĩa thủ công các dòng lệnh AWS SDK (hoặc IaC như Terraform hay SAM) để thực hiện build, đóng gói code artifact rồi upload ở dạng zip hoặc thông qua S3 bucket để triển khai Lambda function:
    1. **Build code** từ source
    2. **Đóng gói** thành file ZIP hoặc container image
    3. **Upload** lên S3 bucket hoặc ECR hoặc zip file
    4. **Update** Lambda function configuration

### Giải pháp mới: Chỉ cần 1 action duy nhất!

Giờ đây bạn chỉ cần khai báo `aws-actions/aws-lambda-deploy` trong Github Actions workflow kèm các tham số như: `function-name`, `code-artifacts-dir` (thư mục chứa mã nguồn Lambda function), `handler`, `runtime`

Xem chi tiết thông báo release [tại đây](https://docs.aws.amazon.com/lambda/latest/dg/deploying-github-actions.html)


### Thực hành với dự án thực tế

Dưới đây là một Github Actions workflow lấy từ dự án [Instagram Post Extractor](https://github.com/hoangquochung1110/insta-post-extractor), một Lambda function để extract metadata từ Instagram posts.


```yaml
name: Lambda CD Pipeline
permissions:
  id-token: write # Cần thiết cho OIDC authentication


on:
  push:
    branches: [ development ]
  workflow_dispatch:


env:
  AWS_REGION: ap-southeast-1
  S3_BUCKET: ig-post-extractor-artifact
  LAMBDA_NAME: IgPostExtractor

jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Configure AWS credentials with OIDC
      # use OpenID Connect (OIDC) to authenticate with AWS to avoid
      # storing AWS credentials as long-lived GitHub secrets.
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Deploy Lambda Function
      id: deploy
      uses: aws-actions/aws-lambda-deploy@v1
      with:
        function-name: ${{ env.LAMBDA_NAME }}
        code-artifacts-dir: src/functions/
        s3-bucket: ${{ env.S3_BUCKET }}
        # Tạo unique S3 key với timestamp và git commit hash
        s3-key: functions/"$(date +%Y%m%d%H%M%S)-${{ github.sha }}"
        handler: ig_post_extractor.lambda_handler
        runtime: python3.12
```
