Git Rebase vs Merge
Khi muốn update branch hiện tại của mình để có thể lấy được code mới từ dev branch thì có 2 trường phái: dùng Git pull (Merge) hoặc là Rebase. Mình thì trước h chỉ toàn dùng Merge thôi, nhưng có đồng nghiệp bảo là nó toàn dùng rebase thôi. Khi mình hỏi là tại sao ko dùng merge cho nó đơn giản mà dùng rebase thì chưa nhận được lời giải thích thoả đáng. Mình có một số câu hỏi về Merge và Rebase:

> Merge tạo ra thêm 1 Merge commit. Việc này thì có vấn đề gì và tại sao phải quan tâm đến Merge commit?

Trả lời: Giả sử bạn từ master checkout ra branch A. Trong lúc đang develop thì có changes từ master, và cái changes này nó ảnh hưởng đến 1 hoặc vài commit trong A. Lúc này bạn có thể 1) đơn giản là cứ merge master vô A, xong add thêm commit mới, hoặc 2) rebase interactively với master, lúc này bạn có thể đổi history tuỳ ý. A của bạn lúc này nhìn giống như mới được checkout từ cái master mới nhất.
Có thể lợi ích của 2 không quá rõ ràng nếu A nhỏ gọn, hoặc là khi master không có gì đổi nhiều.
Nhưng tưởng tượng nếu project lớn, code được thêm vô master liên tục, A cứ phải merge master rồi tạo ra 4 5 cái merge commits thì nó khá khó chịu + khó review theo commit hơn.

> Rebase làm cho Git tree (history) clean hơn. Tại sao chúng ta phải quan tâm đến Git tree? Nếu nó không clean thì sẽ gặp điều gì? Ae cho mình ít usecase của việc Git tree ko clean dẫn đến những vấn đề ae đã gặp với ạ

Trả lời: Clean history giúp dễ dùng mấy features khác của git hơn. Đơn cử nhất là việc revert, hoặc 1 ví dụ khác là git bisect. Bisect nó sẽ chạy binary search trên 1 cái range của good + bad commits (do mình input) để tìm ra cái commit nào introduce bug. Với clean history thì bisect hoạt động khá tốt, vì cái range nó linear.

Ngoài ra: dùng rebase nhìn git tree clean hơn và cũng giúp ích nhiều trong việc trace lại commits. trước đây mình làm 1 dự án dài hơi (kéo dài nhiều năm) mà doc cũng ko đầy đủ, việc rebase kết hợp với commit theo convention ticket name, giúp mình dễ trace lại những commit liên quan hơn và hiểu hơn về quá trình implement của 1 feature.

Tóm lại merge hay rebase đều có pros và cons thôi, tuỳ project tuỳ workflow của mình mà dùng
