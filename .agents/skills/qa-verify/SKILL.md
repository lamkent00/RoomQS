---
name: qa-verify
description: Verify one completed ticket against the TICKET BRIEF, DEV HANDOFF, acceptance criteria, regression risk, and architecture boundaries, then produce a QA REPORT.
---

# qa-verify

Dùng skill này khi user muốn nghiệm thu hoặc verify một ticket đã implement.

## Inputs kỳ vọng
- `TICKET BRIEF / TICKET CONTEXT PACK`
- `DEV HANDOFF`
- Mã nguồn hiện tại / diff liên quan

## Không dùng skill này khi
- User muốn implement ticket -> dùng `implement-ticket`
- User muốn lên sprint plan -> dùng `sprint-plan`
- Thiếu brief/handoff đủ để verify -> trả về `BLOCKED`

## Quy trình bắt buộc
1. Đọc Ticket Brief / Ticket Context Pack.
2. Đọc DEV HANDOFF.
3. Đối chiếu từng Acceptance Criteria.
4. Kiểm tra regression trên module bị ảnh hưởng.
5. Kiểm tra boundary kỹ thuật theo tài liệu kiến trúc.
6. Chỉ fallback sang tài liệu gốc nếu brief hoặc handoff có dấu hiệu sai, thiếu, hoặc mâu thuẫn.
7. Kết thúc bằng đúng format **QA REPORT**.
8. Lưu file vào `./docs/3.qa_report/{ticket_id}.md`

## Quy tắc
- Thiếu 1 Acceptance Criteria chưa đạt => `FAIL`.
- Sửa file ngoài scope không có lý do rõ => `NEEDS REVIEW`.
- Vi phạm boundary, tech stack hoặc data model => `FAIL`.
- Nếu Ticket Brief sai hoặc thiếu so với tài liệu gốc => `NEEDS PM DECISION` hoặc `BLOCKED`.

## Output format bắt buộc

# QA REPORT

Ticket:

Báo cáo ngắn gọn nguồn ngữ cảnh đã dùng:
- Ticket Brief / Context Pack
- DEV HANDOFF
- Docs đã đọc thêm (nếu có)

Story / AC refs:
- Story IDs:
- AC IDs:

Acceptance Criteria Status:
- AC-01: PASS | FAIL
- AC-02: PASS | FAIL

Regression checks:
- [module/check]: PASS | FAIL

Boundary / Architecture check:
- PASS | FAIL
- Ghi chú:

Bugs / Issues:
- 
- 

Fallback docs consulted (nếu có):
- 

Decision:
PASS | FAIL | BLOCKED | NEEDS PM DECISION

Next action:
- 
