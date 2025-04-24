---
title: 'Hands-on Workshops: AI Prompt From Basics to Automation 🚀+ Multimodal RAG with ollama & Milvus'
date: 2025-04-24 11:00
description: ​These workshops aim to cut through the noise of AI hypes to help you understand what are truly important for you to learn, offering attendees a unique opportunity to learn from industry leaders and people who really built and operated AI & ML systems in production.
category: blog
tags:
    - llm
    - prompt-engineering
---

Tháng 4 vừa rồi tại văn phòng AWS Việt Nam, Viet Engineers Stories đã phối hợp tổ chức workshop. Tôi đã tham gia và rất cảm ơn các chuyên gia đã chia sẻ kinh nghiệm và kiến thức.


![Workshop attendance](https://static.ssan.me/prompt-engineering-viet-eng-stories.JPG)

## 📚 Nội dung chính
Hội thảo gồm 2 phần workshops chính:

### 🔍 Workshop 1: Prompt Engineering (Bằng tiếng Việt)

Thời gian: 09:10 - 10:40
Người trình bày: Thai Tang (Cựu Lead ML Engineer tại MoMo)
Nội dung: Tìm hiểu sâu về nghệ thuật prompt engineering, từ thiết kế prompt cơ bản đến các chiến lược tối ưu hóa nâng cao.
Tài liệu tham khảo: Promptimize trên GitHub

### 🌐 Workshop 2: Multimodal RAG với ollama & Milvus (Bằng tiếng Anh)

Thời gian: 11:00 - 12:30
Người trình bày: Ivan Tang (Senior Solutions Architect từ Zilliz)
Nội dung: Hướng dẫn thực hành về việc tạo Multimodal RAG với Milvus và ollama, sử dụng vector database nguồn mở kết hợp với LLM inference nguồn mở.
Tài liệu tham khảo: https://zilliz.com/learn/milvus-notebooks

## Key takeaways
Mr. Thai Tang ở phiên đầu đã đưa đến khán giả:

### Các cấu trúc cơ bản, thường thấy của 1 prompt:

* Single-turn Prompts: Tương tác đơn lẻ (one time) với AI model.
* Multi-turn Prompts: Trao đổi thông tin tuần tự theo thời gian để giữ context.
* Prompt Templates: chuân hoá nội dung truy vấn.
* Conversation Chains: Các kĩ thuật để duy trì context xuyên suốt nhiều hội thoại/tương tác.

### Các phương thức Chuỗi và Trình tự hóa Prompt (Prompt Chaining and Sequencing) sử dụng LangChain

Các phương thức chính:
- Sequential Chaining: Liên kết output từ prompt này sang input của prompt khác. Lý tưởng cho các tiến trình tuyến tính.
- Dynamic Prompt Generation: Tương tự Sequential Chaining, tuy nhiên output từ prompt này sẽ được sử dụng để tạo prompt trung gian rồi tiếp tục truyền vào input của prompt sau. Giúp tăng tính linh hoạt trong chuỗi prompt.
- Error Handling and Validation: Kết hợp xử lí lỗi và valiadation để tăng tính cường tráng của hệ thống.

### Chain of Thought
Tinh chỉnh câu lệnh để yêu cầu LLM dành thời gian suy nghĩ và lập luận trước khi đưa ra câu trả lời.

### Structured Output
Sử dụng function calling kèm các thư viện như Pydantic, instructor để định dạng output của LLM.
