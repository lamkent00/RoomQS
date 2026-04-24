---
trigger: always_on
---

# DOC ROUTER

Mục tiêu:
Giảm token bằng cách chỉ đọc đúng tài liệu cần thiết cho từng loại tác vụ.

Luôn đọc:
- /docs/0.INSTRUCTION.md

---

## A. SPRINT PLANNING

PM Agent bắt buộc đọc:
- /docs/02-PRD-Product-Backlog.md
- /docs/03-User-Stories.md
- /docs/05-Ke-Hoach-Sprint-Release.md

PM Agent chỉ cần đọc lướt:
- /docs/04-Kien-Truc-Tech-Stack.md
Mục tiêu: lấy module names, boundary chính, dependency chính.

---

## B. IMPLEMENT TICKET

Dev Agent đọc theo thứ tự:
1. TICKET BRIEF / TICKET CONTEXT PACK
2. /docs/0.INSTRUCTION.md
3. /docs/04-Kien-Truc-Tech-Stack.md
   - CHỈ section của module liên quan
4. /docs/06-Setup-Moi-Truong-Trien-Khai.md
   - CHỈ khi ticket có đụng config/env/setup/build/deploy
5. Chỉ fallback sang /docs/03-User-Stories.md hoặc /docs/02-PRD-Product-Backlog.md nếu:
   - Ticket Brief thiếu AC
   - Logic nghiệp vụ chưa đủ rõ
   - Có dấu hiệu brief mâu thuẫn

Dev Agent KHÔNG mặc định đọc toàn bộ PRD/Backlog.

---

## C. QA VERIFY

QA Agent đọc theo thứ tự:
1. TICKET BRIEF / TICKET CONTEXT PACK
2. DEV HANDOFF
3. /docs/04-Kien-Truc-Tech-Stack.md
   - CHỈ section liên quan module bị ảnh hưởng
4. Chỉ fallback sang /docs/03-User-Stories.md hoặc /docs/02-PRD-Product-Backlog.md nếu:
   - Ticket Brief không đủ AC
   - Dev Handoff có dấu hiệu diễn giải sai ticket
   - Có mâu thuẫn giữa behavior và tài liệu gốc

QA Agent KHÔNG mặc định đọc lại toàn bộ PRD/User Stories.

---

## D. QUY TẮC FALLBACK

Chỉ fallback sang tài liệu gốc khi thật sự cần.
Ưu tiên thứ tự:
- Ticket Brief / Context Pack
- Handoff
- Section cụ thể của docs (section-level reading)
- Full doc chỉ là lựa chọn cuối cùng