---
trigger: always_on
---

# GLOBAL TEAM RULE

Ngôn ngữ làm việc: Tiếng Việt.

Nguyên tắc chung:
- Không deploy, merge, publish hoặc thay đổi môi trường production nếu chưa được yêu cầu rõ ràng.
- Không thay đổi ngoài phạm vi ticket.
- Không tự suy diễn yêu cầu nghiệp vụ khi tài liệu hoặc ticket chưa đủ rõ.
- Nếu tài liệu mâu thuẫn, thiếu dữ kiện, hoặc boundary không rõ: trả về BLOCKED thay vì tự đoán.
- Ưu tiên dùng ngữ cảnh đã được PM đóng gói trong TICKET BRIEF / TICKET CONTEXT PACK.
- Chỉ đọc tài liệu tối thiểu theo Doc Router và section liên quan khi:
  1. Ticket Brief thiếu thông tin cần thiết
  2. Cần xác minh boundary kỹ thuật
  3. Phát hiện dấu hiệu brief/handoff sai hoặc mâu thuẫn
- Luôn ưu tiên thay đổi nhỏ nhất có thể để đạt Acceptance Criteria.
- Không đổi framework, thư viện nền, cấu trúc dữ liệu lõi, hoặc module boundary nếu chưa được cho phép rõ ràng.

Quy tắc báo cáo:
- Không báo “đã xong” nếu chưa có bằng chứng kiểm chứng phù hợp.
- Khi hoàn tất một bước, chỉ báo cáo ngắn gọn theo đúng template của skill tương ứng.
- Không kể lại dài dòng toàn bộ yêu cầu nếu nội dung đó đã có sẵn trong Ticket Brief.