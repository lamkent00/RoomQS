---
description: Implement exactly one ticket.
---

# implement-ticket

Mục tiêu:
Thực thi chính xác MỘT ticket dựa trên TICKET BRIEF / TICKET CONTEXT PACK và tài liệu kỹ thuật liên quan.

Tài liệu phải đọc:
- Theo DOC ROUTER / mục IMPLEMENT TICKET

Các bước thực hiện:
1. Đọc Ticket Brief / Ticket Context Pack.
2. Xác định:
   - Goal
   - In scope
   - Out of scope
   - Acceptance Criteria
   - Module boundary
   - Files/modules dự kiến bị ảnh hưởng
3. Đối chiếu tài liệu kỹ thuật để xác định chính xác nơi cần sửa.
4. Thực hiện thay đổi nhỏ nhất có thể để đạt Acceptance Criteria.
5. Không sửa file ngoài scope nếu không có lý do kỹ thuật thật sự rõ ràng.
6. Chạy các kiểm tra liên quan.
7. Chỉ xuất kết quả theo format DEV HANDOFF và lưu vào thư mục "docs/3. dev-handoff" với tên file là TicketID (vd S1-T01.md)

Quy tắc:
- Không tự suy diễn business logic ngoài Ticket Brief.
- Không mặc định đọc lại toàn bộ PRD.
- Nếu Ticket Brief thiếu hoặc mâu thuẫn logic quan trọng: BLOCKED.
- Nếu phải fallback sang tài liệu gốc, phải ghi rõ trong DEV HANDOFF.