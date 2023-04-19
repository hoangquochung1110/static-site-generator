> em đang research về dbms và có câu hỏi muốn đc giải đáp ạ:
giả sử có 1 transaction ghi xuống db, và 1 lí do nào đó transaction này crash, vậy thì có cách nào để identify đc đã có crash xảy ra với transaction đó ko ạ ?
Em search thì thấy họ đề cập đến checksum đc chèn trong database pages. Ko biết thực tế production mn implement thế nào ạ

Để mình tách từng ý để discuss nhé:
1/ Cần phân biệt transaction failed và crashed: failed là khi có lỗi trong câu SQL, khi đó database sẽ rollback lại trạng thái trước khi chạy các câu lệnh sql, ví dụ chạy 5 câu insert, fail ở câu 3, thì database sẽ rollback trạng thái về trước câu đầu tiên. Còn crashed là những lỗi ko mong muốn, ví dụ mất điện đột ngột, server bị crash, tràn memory, etc; khi đó có thể gây corrupt data.
2/ Hầu hết các database đều có cơ chế durable, tức là hạn chế mức thấp nhất corrupt data nếu crash, ví dụ postgres sẽ write vào WAL (write ahead log), theo cơ chế MVCC, rồi sau đó mới commit transaction
https://www.postgresql.org/files/developer/transactions.pdf
3/ Dữ liệu trong database thường sẽ chia làm các block cùng kích cỡ (gọi là các data page - ví dụ 8KB/page), khi write xuống sẽ dùng cơ chế fsync để flush cả một page xuống; và checksum sẽ đóng vai trò ở đây : )
4/ checksum sẽ được ghi ở header mỗi data page, để đảm bảo dữ liệu ở page đó ko bị thay đổi bên ngoài database (hỏng ổ đĩa, etc), default thì postgres ko bật cơ chế này
https://www.crunchydata.com/blog/fun-with-pg_checksums
5/ Nếu muốn battle test database trong trường hợp crash, bạn có thể thử set fsync = off, khi đó dữ liệu sẽ dc ghi trước khi ghi WAL file https://www.cybertec-postgresql.com/en/how-to-corrupt-your-postgresql-database/

em hiểu là data và cả index sẽ được lưu dưới nhiều data page, checksum sẽ là 2 byte nằm ở header, khi checksum ko khớp là data page đó bị corrupt
