---
name: sprint-plan
description: Create a sprint brief and ticket context packs from project documents, splitting work into 3 to 7 safe, parallelizable tickets with clear module boundaries and acceptance criteria references.
---

# sprint-plan

Dùng skill này khi user muốn tạo sprint plan, sprint brief hoặc bóc tách ticket từ tài liệu dự án.

## Inputs kỳ vọng
- Mục tiêu sprint / phase
- Các docs theo Doc Router mục Sprint Planning

## Không dùng skill này khi
- User chỉ muốn implement một ticket -> dùng `implement-ticket`
- User chỉ muốn QA verify một ticket -> dùng `qa-verify`
- Scope hiện tại mâu thuẫn hoặc không thể chia boundary an toàn -> `BLOCKED`

## Quy trình bắt buộc
1. Xác định phase hiện tại từ kế hoạch sprint/release.
2. Xác định scope đang in-scope cho sprint hiện tại.
3. Chia thành 3–7 ticket đủ nhỏ để làm song song, ít phụ thuộc, boundary rõ.
4. Với mỗi ticket, xác định:
   - Mục tiêu nghiệp vụ
   - Story IDs liên quan
   - Acceptance Criteria IDs liên quan
   - Module boundary
   - Files/modules có thể bị ảnh hưởng
   - Dependencies
   - Out-of-scope guardrail
   - Rủi ro / ambiguity nếu có
5. Phải trích xuất ngữ cảnh từ tài liệu lớn vào `TICKET BRIEF` / `TICKET CONTEXT PACK` để Dev và QA không phải đọc lại PRD một cách mặc định.
6. Kết thúc bằng đúng format **SPRINT BRIEF** và **TICKET CONTEXT PACK**.
7. Lưu file vào `./docs/1.sprint_plans/{sprint_id}-plan.md`

## Quy tắc
- Không tạo ticket quá lớn hoặc chạm nhiều module không cần thiết.
- Nếu scope mâu thuẫn hoặc không thể chia boundary an toàn: `BLOCKED`.
- Không yêu cầu Dev tự đi đào lại logic nghiệp vụ từ PRD nếu PM có thể đóng gói trước.

## Output format bắt buộc

# SPRINT BRIEF

Sprint:
Phase:
Mục tiêu sprint:
In-scope:
Out-of-scope:
Risks:
Dependencies:

Danh sách ticket:
1.
2.
3.

---

# TICKET CONTEXT PACK

Ticket:
Người phụ trách:
Mục tiêu:

In scope:
Out of scope:

Story IDs:
Acceptance Criteria IDs:

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01:
- AC-02:

Module boundary:
Files/Modules dự kiến bị ảnh hưởng:

Doc refs:
- /docs/...#section
- /docs/...#section

Dependencies:
Known risks:
Open ambiguities:

Definition of Done:
