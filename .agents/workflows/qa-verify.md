---
description: Verify a ticket implementation.
---

# qa-verify

Mục tiêu:
Nghiệm thu ticket bằng cách đối chiếu Ticket Brief, Dev Handoff và boundary kỹ thuật liên quan.

Tài liệu phải đọc:
- Theo DOC ROUTER / mục QA VERIFY

Các bước thực hiện:
1. Đọc Ticket Brief / Ticket Context Pack.
2. Đọc DEV HANDOFF.
3. Đối chiếu từng Acceptance Criteria.
4. Kiểm tra regression trên module bị ảnh hưởng.
5. Kiểm tra boundary kỹ thuật theo tài liệu kiến trúc.
6. Chỉ fallback sang tài liệu gốc nếu brief hoặc handoff có dấu hiệu sai, thiếu, hoặc mâu thuẫn.
7. Chỉ xuất kết quả theo format QA REPORT và lưu vào thư mục "docs/4. qa-report" với tên file là TiketID.

Quy tắc:
- Thiếu 1 Acceptance Criteria chưa đạt => FAIL.
- Sửa file ngoài scope không có lý do rõ => NEEDS REVIEW.
- Vi phạm boundary, tech stack hoặc data model => FAIL.
- Nếu Ticket Brief sai hoặc thiếu so với tài liệu gốc => NEEDS PM DECISION hoặc BLOCKED.