> Em đang làm cái app xài Nodejs/React. Người dùng upload hình ảnh sẽ lưu trực tiếp vô AWS EC2 server folder, còn filename sẽ lưu vô database. Em thấy cách này tốn nhiều tài nguyên cho server quá, nên đang nghĩ cách để lưu hình lên CDN. Cho em hỏi flow như này có ổn ko ạ: hình sẽ upload lên S3 thay vì EC2 -> sau đó CDN (CloudFront) sẽ lấy hình từ S3 rồi trả về frontend để cache trên local?

Không những được mà còn là recommended
