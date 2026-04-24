---
description: Create a sprint plan from the user's goal.
---

# sprint-plan

Mục tiêu:
Tạo Sprint Brief và bóc tách ticket rõ ràng, an toàn để Dev/QA không phải đọc lại tài liệu tổng quan không cần thiết.

Tài liệu phải đọc:
- Theo DOC ROUTER / mục SPRINT PLANNING

Các bước thực hiện:
1. Xác định phase hiện tại từ kế hoạch sprint/release.
2. Xác định scope đang in-scope cho sprint hiện tại.
3. Chia thành 3–7 ticket đủ nhỏ để làm song song, ít phụ thuộc, boundary rõ.
4. Với mỗi ticket:
   - Xác định mục tiêu nghiệp vụ
   - Story IDs liên quan
   - Acceptance Criteria IDs liên quan
   - Module boundary
   - Files/modules có thể bị ảnh hưởng
   - Dependencies
   - Out-of-scope guardrail
   - Rủi ro / ambiguity nếu có
5. PHẢI trích xuất ngữ cảnh từ tài liệu lớn vào TICKET BRIEF/TICKET CONTEXT PACK để Dev và QA không phải đọc lại PRD một cách mặc định.
6. Chỉ xuất kết quả theo format:
   - SPRINT BRIEF
   - TICKET BRIEF / TICKET CONTEXT PACK
7. Lưu file kết quả vào thư mục "docs/1. sprint-plans" với tên file là sprintID (vd sprint1.md)
Quy tắc:
- Không tạo ticket quá lớn hoặc chạm nhiều module không cần thiết.
- Nếu scope mâu thuẫn hoặc không thể chia boundary an toàn: BLOCKED.
- Không yêu cầu Dev tự đi “đào lại” logic nghiệp vụ từ PRD nếu PM có thể đóng gói trước.