# AGENTS.md

Ngôn ngữ làm việc mặc định: **Tiếng Việt**.

## Working agreement chung

- Không deploy, merge, publish hoặc thay đổi môi trường production nếu chưa được yêu cầu rõ ràng.
- Không thay đổi ngoài phạm vi ticket.
- Không tự suy diễn yêu cầu nghiệp vụ khi tài liệu hoặc ticket chưa đủ rõ.
- Nếu tài liệu mâu thuẫn, thiếu dữ kiện, hoặc boundary không rõ: trả về **BLOCKED** thay vì tự đoán.
- Ưu tiên dùng ngữ cảnh đã được PM đóng gói trong **TICKET BRIEF / TICKET CONTEXT PACK**.
- Chỉ đọc tài liệu tối thiểu theo **Doc Router** và đúng section liên quan khi:
  1. Ticket Brief thiếu thông tin cần thiết
  2. Cần xác minh boundary kỹ thuật
  3. Phát hiện dấu hiệu brief/handoff sai hoặc mâu thuẫn
- Luôn ưu tiên thay đổi nhỏ nhất có thể để đạt Acceptance Criteria.
- Không đổi framework, thư viện nền, cấu trúc dữ liệu lõi, hoặc module boundary nếu chưa được cho phép rõ ràng.
- Không báo “đã xong” nếu chưa có bằng chứng kiểm chứng phù hợp.
- Khi hoàn tất một bước, báo cáo ngắn gọn theo đúng template của skill tương ứng.
- Không kể lại dài dòng toàn bộ yêu cầu nếu nội dung đó đã có sẵn trong Ticket Brief.

## Workspace baseline

Nguồn chuẩn kỹ thuật:
- `/docs/0.INSTRUCTION.md`
- `/docs/04-Kien-Truc-Tech-Stack.md`

Ràng buộc kỹ thuật:
- Phải bám đúng tech stack đã được phê duyệt.
- Phải bám đúng module boundary, data flow, API contract và cấu trúc tổng thể trong tài liệu kiến trúc.
- Chỉ đọc `/docs/06-Setup-Moi-Truong-Trien-Khai.md` nếu ticket liên quan config, env, build, deploy, integration hoặc setup môi trường.
- Không thêm thư viện, service hoặc pattern mới nếu không thật sự cần cho ticket.
- Nếu phát hiện yêu cầu ticket mâu thuẫn với kiến trúc: **BLOCKED** hoặc **NEEDS REVIEW**.

## Doc Router

Mục tiêu: giảm token bằng cách chỉ đọc đúng tài liệu cần thiết cho từng loại tác vụ.

Luôn đọc:
- `/docs/0.INSTRUCTION.md`

### A. Sprint planning

Bắt buộc đọc:
- `/docs/02-PRD-Product-Backlog.md`
- `/docs/03-User-Stories.md`
- `/docs/05-Ke-Hoach-Sprint-Release.md`

Chỉ đọc lướt:
- `/docs/04-Kien-Truc-Tech-Stack.md`
  - Mục tiêu: lấy module names, boundary chính, dependency chính.

### B. Implement ticket

Đọc theo thứ tự:
1. `TICKET BRIEF / TICKET CONTEXT PACK`
2. `/docs/0.INSTRUCTION.md`
3. `/docs/04-Kien-Truc-Tech-Stack.md`
   - Chỉ section của module liên quan
4. `/docs/06-Setup-Moi-Truong-Trien-Khai.md`
   - Chỉ khi ticket có đụng config/env/setup/build/deploy
5. Chỉ fallback sang `/docs/03-User-Stories.md` hoặc `/docs/02-PRD-Product-Backlog.md` nếu:
   - Ticket Brief thiếu AC
   - Logic nghiệp vụ chưa đủ rõ
   - Có dấu hiệu brief mâu thuẫn

Không mặc định đọc toàn bộ PRD/Backlog.

### C. QA verify

Đọc theo thứ tự:
1. `TICKET BRIEF / TICKET CONTEXT PACK`
2. `DEV HANDOFF`
3. `/docs/04-Kien-Truc-Tech-Stack.md`
   - Chỉ section liên quan module bị ảnh hưởng
4. Chỉ fallback sang `/docs/03-User-Stories.md` hoặc `/docs/02-PRD-Product-Backlog.md` nếu:
   - Ticket Brief không đủ AC
   - Dev Handoff có dấu hiệu diễn giải sai ticket
   - Có mâu thuẫn giữa behavior và tài liệu gốc

Không mặc định đọc lại toàn bộ PRD/User Stories.

### D. Quy tắc fallback

Chỉ fallback sang tài liệu gốc khi thật sự cần.
Ưu tiên thứ tự:
- Ticket Brief / Context Pack
- Handoff
- Section cụ thể của docs (section-level reading)
- Full doc chỉ là lựa chọn cuối cùng

## Output discipline

- Khi user yêu cầu thực thi ticket: ưu tiên dùng skill `implement-ticket`.
- Khi user yêu cầu nghiệm thu / verify/ qa : ưu tiên dùng skill `qa-verify`.
- Khi user yêu cầu chia sprint / lập kế hoạch: ưu tiên dùng skill `sprint-plan`.
- Nếu thiếu Ticket Brief, thiếu Dev Handoff, hoặc boundary tài liệu không rõ, phải nêu rõ thiếu gì và trả về `BLOCKED` hoặc `NEEDS PM DECISION` tùy trường hợp.
