---
name: implement-ticket
description: Implement exactly one engineering ticket from a TICKET BRIEF or TICKET CONTEXT PACK, with minimal in-scope changes, architecture compliance, relevant checks, and a final DEV HANDOFF.
---

# implement-ticket

Dùng skill này khi user muốn thực thi chính xác **một** ticket.

## Inputs kỳ vọng
- `TICKET BRIEF` hoặc `TICKET CONTEXT PACK`
- Tài liệu kỹ thuật liên quan theo Doc Router

## Không dùng skill này khi
- User đang yêu cầu chia sprint / bóc tách ticket -> dùng `sprint-plan`
- User đang yêu cầu nghiệm thu một implementation đã xong -> dùng `qa-verify`
- Ticket thiếu thông tin cốt lõi hoặc boundary mâu thuẫn -> trả về `BLOCKED`

## Quy trình bắt buộc
1. Đọc Ticket Brief / Ticket Context Pack.
2. Xác định rõ:
   - Goal
   - In scope
   - Out of scope
   - Acceptance Criteria
   - Module boundary
   - Files/modules dự kiến bị ảnh hưởng
3. Đối chiếu tài liệu kỹ thuật để xác định đúng nơi cần sửa.
4. Thực hiện thay đổi nhỏ nhất có thể để đạt Acceptance Criteria.
5. Không sửa file ngoài scope nếu không có lý do kỹ thuật thật sự rõ ràng.
6. Chạy các kiểm tra liên quan.
7. Kết thúc bằng đúng format **DEV HANDOFF**.
8. Lưu file vào `./docs/2.dev_handoff/{ticket_id}.md`

## Quy tắc
- Không tự suy diễn business logic ngoài Ticket Brief.
- Không mặc định đọc lại toàn bộ PRD.
- Nếu Ticket Brief thiếu hoặc mâu thuẫn logic quan trọng: `BLOCKED`.
- Nếu phải fallback sang tài liệu gốc, phải ghi rõ trong DEV HANDOFF.
- Không kết luận READY FOR QA nếu chưa có bằng chứng kiểm chứng phù hợp.

## Output format bắt buộc

# DEV HANDOFF

Ticket:
Mục tiêu:

Nguồn ngữ cảnh đã dùng:
- Ticket Brief / Context Pack
- Docs đã đọc thêm (nếu có)

Story / AC refs:
- Story IDs:
- AC IDs:

Files changed:
- 
- 

Thay đổi chính:
- 
- 

Checks đã chạy:
- 
- 

Kết quả:
- 

Fallback docs consulted (nếu có):
- 

Known risks:
- 

Open questions:
- 

Decision:
READY FOR QA | BLOCKED
