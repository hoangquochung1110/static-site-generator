Q: Hỏi người trong cuộc: @giongto35
A đang muốn xem khả năng nhảy vào mảng ML/AI, giờ a thấy có 1 hướng cụ thể nhất là đi học lại từ đầu, nhưng cách này thì chắc phải tốn nhiều năm. E làm trong mảng này thì thấy có hướng nào cho những ng muốn focus vào engineering như a mà vẫn có đường để vào mảng này ko? AI engineering? cụ thể nó là làm cái gì nhỉ?

A: Em làm MLOps/Infra, ko khác gì làm DevOps cả. Em cũng là Engineer ko làm research. Và nó cũng ko kém phần quan trọng trong thời kì này bởi vì giờ AI là throw compute vào, scale rất lớn nên system cần reliable, những gì mình cần để maintain web service thì cũng tương tự với AI system vậy.

Có khác là deal với GPUs machines, AI Scheduler, Python ecosystem, File system (cần data load) nhiều hơn (edited)
Còn muốn làm close với research hơn, support researcher train model hoặc launch model, thì cần hiểu thêm về AI research + Optimize GPU performance (NCCL). Nếu là Engineer thì hiểu về GPUs, optimize GPU là highly valuable skill

Và AI modelling cũng ko còn quá khó như xưa. Xưa model rất phức tạp và tricky, nối edge này edge nọ các thứ, AI Framework thì chưa đủ mature để represent cái graph. E.g Tensorflow là 1 failure case làm mọi thứ trông rất phức tạp. Thời nay nhận ra AI model ko cần phức tạp đến vậy, LLM chứng minh là model càng generic mà chỉ cần throw compute vào là solve everything. các đời GPT cũng ko có thay đổi quá nhiều về model. Pytorch viết bằng Python cũng làm việc modeling dễ hơn rất nhiều.

Q: thank e, vậy là ko cần đi theo hướng research vẫn có đất để làm trước lúc nhảy qua làm MLOps thì e có làm gì liên quan đến cái này ko nhỉ?

A: Em nghĩ cứ start small, lấy cái LLM model về thử implement nếu muốn hiểu thôi (lý thuyết là vậy em còn chưa làm). Nhưng đa phần Engineer thì vẫn có nhiều đất ngày nay, AI hàn lâm cũng ko có quá nhiều người. May mắn vì AI hiện tại là running bigger infra for better result.
trc đó em làm backend với Video thôi ạ. Với internal transfer nên cũng thoải mái