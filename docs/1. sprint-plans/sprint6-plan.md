# SPRINT BRIEF

Sprint: Sprint 6 — UAT + Packaging + Release
Phase: GIAI ĐOẠN 5 — UAT & RELEASE (Tuần 11–12)
Mục tiêu sprint: Nghiệm thu sản phẩm với bản vẽ thực; fix bug P0/P1 từ UAT; đóng gói .exe final chạy trên máy sạch Windows; viết Quick Guide; PM sign-off để go-live. KHÔNG thêm feature mới trong sprint này.

In-scope:
- BL-37: UAT thực tế với ≥ 2 file bản vẽ thực — QA + PM thực hiện, verify 13 tiêu chí SRS Section 15
- Bug fix P0/P1 phát sinh từ UAT (buffer 3 ngày — chỉ fix issue UAT phát hiện)
- BL-38: Đóng gói .exe final từ main branch, smoke test trên ≥ 2 máy Windows sạch
- BL-39: Quick Guide (PDF/Markdown, ≤ 2 trang): cài .exe, load .LSP, chạy lần đầu, hiểu cảnh báo
- Release checklist review (PM + Tech Lead)
- PM sign-off email go-live

Out-of-scope:
- Tuyệt đối không thêm feature mới, không thay đổi UI/UX ngoài bug fix
- Không thêm cột/sheet mới vào Excel (template đã đóng băng từ Sprint 3)
- Không thay đổi business rule
- Không làm Phase 2 items (zero-click detection, chiều cao per-phòng, ERP integration)
- Bug P2/P3 từ UAT → vào backlog Phase 2, không fix trong sprint này

Risks:
- Bản vẽ thực phát sinh case mới chưa handle → triage nghiêm túc: P0/P1 fix, còn lại backlog.
- Antivirus false positive block .exe trên máy khách hàng → cần hướng dẫn whitelist trong Quick Guide.
- UAT dùng file synthetic (không có bản vẽ thực) → đây là blocker go-live (GLC-blocker #5).
- .exe build từ dev branch thay vì main → lỗi version không đồng nhất. Build chỉ từ main branch.
- Code signing chưa có → SmartScreen Windows có thể cảnh báo. Ghi rõ workaround trong Quick Guide.

Dependencies:
- Sprint 5 exit criteria phải pass: end-to-end test pass, file Excel hợp lệ, UI responsive.
- UAT checklist BL-36 từ Sprint 4 phải hoàn chỉnh (13 tiêu chí).
- ≥ 2 file bản vẽ thực được PM xác nhận để dùng trong UAT (thu thập từ Sprint 0).
- AutoCAD 2019+ trên máy test UAT.

Danh sách ticket:
1. T6-01: Thực hiện UAT với ≥ 2 file bản vẽ thực + lập UAT Report (BL-37)
2. T6-02: Bug fix P0/P1 từ UAT
3. T6-03: Đóng gói .exe final + smoke test 2 máy sạch (BL-38)
4. T6-04: Viết Quick Guide (BL-39) + Release Checklist + PM Sign-off

---

# TICKET CONTEXT PACK

Ticket: T6-01 — Thực hiện UAT với ≥ 2 file bản vẽ thực + lập UAT Report (BL-37)
Người phụ trách: QA + PM
Mục tiêu: Verify toàn bộ 13 tiêu chí nghiệm thu SRS Section 15 với file bản vẽ thực. Lập UAT report đầy đủ pass/fail cho từng tiêu chí. Đây là gate 4 (UAT Gate) — điều kiện tiên quyết cho go-live.

In scope:
- Chạy UAT với ≥ 2 file bản vẽ DXF thực tế (đa dạng: phòng vuông + L-shape, có cửa ranh giới chung)
- Verify 13 tiêu chí UAT checklist (BL-36 từ Sprint 4):
  - GLC-01: Tất cả 13 tiêu chí SRS Section 15 pass
  - GLC-02: Tỷ lệ phòng nhận diện đúng ≥ 90%
  - GLC-03: Tỷ lệ cửa gán đúng phòng ≥ 95%
  - GLC-04: Sai lệch diện tích < 1% so với đo tay
  - GLC-05: BR-06 áp dụng đúng ít nhất 2 test case cửa chung
  - GLC-07: 0 crash (unhandled exception)
  - GLC-08: 0 xuất sai số mà không cảnh báo
- Phân loại toàn bộ bug phát hiện: P0 (crash/data loss), P1 (tính sai không cảnh báo), P2+ (UI, edge case hiếm)
- Ghi UAT report: kết quả từng tiêu chí + số phòng nhận diện đúng/tổng + danh sách bug

Out of scope:
- Không test trên file DXF synthetic (chỉ file bản vẽ thực mới có giá trị UAT)
- Không fix code trong ticket này — chỉ report

Story IDs: US-INP-001, US-ROOM-001, US-DOOR-001, US-DOOR-002, US-DOOR-003, US-CALC-001 đến US-CALC-005, US-EXP-001 đến US-EXP-004, US-ALERT-001, US-ALERT-002
Acceptance Criteria IDs: Go-live criteria GLC-01 đến GLC-10

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (GLC-01): Tất cả 13 tiêu chí SRS Section 15 pass — ghi rõ pass/fail từng tiêu chí
- AC-02 (GLC-02): Tỷ lệ phòng nhận diện đúng ≥ 90% (đếm tay trên bản vẽ thực)
- AC-03 (GLC-03): Tỷ lệ cửa gán đúng phòng ≥ 95%
- AC-04 (GLC-04): Sai lệch diện tích < 1% so với đo tay ít nhất 3 phòng đại diện
- AC-05 (GLC-05): BR-06 đúng trong ≥ 2 test case cửa ranh giới chung: trừ `door.area` mỗi phòng 1 lần (không chia đôi)
- AC-06 (GLC-07): 0 crash (unhandled exception) qua toàn bộ test cases
- AC-07 (GLC-08): 0 trường hợp số liệu sai > 1% mà không có cảnh báo trên UI
- AC-08: UAT report hoàn chỉnh: kết quả từng tiêu chí, số phòng đúng/tổng, danh sách bug có P0/P1/P2 classification

Module boundary:
- Không chạm code — activity thuần QA/PM
- Artifacts: `uat_report_[date].xlsx` hoặc `uat_report_[date].md`
- Tool: UAT checklist BL-36 từ Sprint 4

Files/Modules dự kiến bị ảnh hưởng:
- Không sửa code
- Output: `docs/uat/uat_report_[date].md` và `issues/uat_bugs_[date].md`

Doc refs:
- /docs/05-Ke-Hoach-Sprint-Release.md#Gate-4-UAT
- /docs/05-Ke-Hoach-Sprint-Release.md#Go-live-criteria (GLC-01 đến GLC-11)
- /docs/05-Ke-Hoach-Sprint-Release.md#Pre-release-checklist
- /docs/02-PRD-Product-Backlog.md#MVP-Acceptance

Dependencies:
- Sprint 5 exit criteria pass (xác nhận từ Sprint 5 Review)
- ≥ 2 file DXF bản vẽ thực có sẵn (thu thập từ Sprint 0)
- UAT checklist BL-36 đã hoàn chỉnh từ Sprint 4
- AutoCAD 2019+ trên máy UAT

Known risks:
- Nếu tỷ lệ phòng nhận diện < 90% trên file thực → P0 blocker cho go-live, cần session triage khẩn với PM + Tech Lead.
- Bản vẽ thực có thể có layer naming khác convention → kiểm tra config.yaml trước khi chạy UAT.
- File DXF thực chưa được PM cung cấp từ Sprint 0 → đây là blocker UAT, phải escalate ngay.

Open ambiguities:
- 13 tiêu chí SRS Section 15 cụ thể là gì? → QA cần lấy từ file SRS v1.0 và đối chiếu với UAT checklist BL-36. Nếu không có file SRS, báo cáo PM ngay.
- "Đo tay" để verify diện tích: QA dùng công cụ gì? (Đề xuất: AutoCAD AREA command hoặc đo polygon trong DXF)

Definition of Done:
- [ ] UAT chạy xong với ≥ 2 file DXF thực
- [ ] UAT report có kết quả rõ ràng (pass/fail) cho từng GLC-01 đến GLC-10
- [ ] Toàn bộ bug được phân loại P0/P1/P2 với reproduction steps đầy đủ
- [ ] PM đọc UAT report và đưa ra quyết định: go/no-go với T6-02

---

# TICKET CONTEXT PACK

Ticket: T6-02 — Bug fix P0/P1 từ UAT
Người phụ trách: Dev-A / Dev-B
Mục tiêu: Fix toàn bộ P0 và P1 bugs phát hiện trong T6-01. Bug P0 phải fix trong 24 giờ. Bug P1 fix trong 3 ngày. Không fix P2+ trong sprint này — ghi vào backlog Phase 2.

In scope:
- P0 (Blocker): Crash / data loss / xuất sai số không cảnh báo → phải fix 100% trước go-live
- P1 (MVP): Tính năng Must-have cho kết quả sai → fix nếu còn trong sprint, nếu không → delay go-live
- Mỗi fix phải có: unit test hoặc regression test pass + QA verify lại
- Không thêm feature mới dù được yêu cầu trong quá trình UAT
- CI pipeline phải green sau mỗi fix

Out of scope:
- Không fix P2+ (UI không đẹp, edge case hiếm) trong sprint này
- Không refactor code ngoài scope bug fix
- Không thay đổi template Excel hoặc business rule

Story IDs: Phụ thuộc vào bug phát hiện — xác định sau T6-01
Acceptance Criteria IDs: Phụ thuộc vào bug — mỗi bug có reproduction case riêng

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: Tất cả P0 bug fix xong và QA verify pass trước khi build .exe final
- AC-02: Tất cả P1 bug fix xong (nếu còn thời gian) hoặc PM đưa ra quyết định explicit về P1 chưa fix
- AC-03: CI pipeline green (pytest 100% pass) sau mỗi fix commit
- AC-04: Không có open TODO/FIXME trong code path critical sau sprint
- AC-05: Mỗi bug fix có regression test đi kèm để tránh tái phát

Module boundary:
- Phụ thuộc vào bug cụ thể từ T6-01
- Rule: mỗi fix chỉ chạm module liên quan đến bug, không spread sang module khác
- Bất kỳ fix nào chạm `calc_engine` hoặc `door_engine` phải có unit test pass kèm theo

Files/Modules dự kiến bị ảnh hưởng:
- Xác định sau khi có UAT report từ T6-01

Doc refs:
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint-6-Triage-Rule
- /docs/05-Ke-Hoach-Sprint-Release.md#Bug-triage-sau-release

Dependencies:
- T6-01 phải done — cần UAT report với danh sách bug đã phân loại
- Dev phải có file DXF gây lỗi từ QA để reproduce

Known risks:
- Nếu P0 phức tạp cần > 3 ngày fix → PM phải quyết định: delay go-live hoặc thu hẹp scope UAT.
- Fix P0 có thể introduce regression → QA phải verify lại toàn bộ sprint 5 exit criteria sau fix.
- Buffer chỉ có 3 ngày — cần triage nhanh và không ôm nhiều fix cùng lúc.

Open ambiguities:
- Nếu phát sinh P0 bug mới sau khi fix P0 cũ → sprint sẽ bị overrun. PM cần có quyết định rõ ràng về threshold.

Definition of Done:
- [ ] 0 open P0 bug
- [ ] Tất cả P1 bug hoặc đã fix + QA verify, hoặc PM accept explicitly với documented risk
- [ ] CI pipeline green (pytest 100%)
- [ ] QA chạy lại smoke test sau fix: không có regression mới

---

# TICKET CONTEXT PACK

Ticket: T6-03 — Đóng gói .exe final + Smoke test 2 máy Windows sạch (BL-38)
Người phụ trách: Dev-A
Mục tiêu: Build .exe final từ main branch sau khi tất cả P0/P1 bug đã fix. Smoke test trên 2 máy Windows sạch (không cài Python, không cài Shapely). Đây là deliverable kỹ thuật cuối cùng trước khi go-live.

In scope:
- Build .exe từ main branch (không phải dev/feature branch)
- PyInstaller `--onedir` mode (không dùng --onefile để tránh antivirus false positive)
- Bundle kèm: file .LSP (xr.lsp, gb.lsp, export_rooms.lsp) trong thư mục `lisp/`
- Bundle kèm: `config.yaml` mặc định
- Smoke test checklist trên 2 máy sạch:
  - Windows 10 64-bit (Core i5, 8GB RAM hoặc tương đương)
  - Windows 11 64-bit
  - Máy sạch = không cài Python, không cài Shapely, không cài ezdxf
- Verify: UI PySide6 mở trong ≤ 5 giây
- Verify: chạy được 1 file DXF test nhỏ end-to-end trên máy sạch
- Update version number trong app trước khi build
- Ghi file size .exe: kiểm tra < 300 MB

Out of scope:
- Code signing (code signing là nice-to-have, không block go-live nếu có hướng dẫn SmartScreen)
- Build cho macOS/Linux
- Auto-update mechanism

Story IDs: US-OPS-001
Acceptance Criteria IDs: US-OPS-001 AC tất cả + Release Gate GLC-09

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (US-OPS-001): File .exe build bằng PyInstaller chạy được trên Windows 10/11 (64-bit)
- AC-02 (US-OPS-001): Không yêu cầu cài Python hoặc bất kỳ dependency nào
- AC-03 (US-OPS-001): Giao diện PySide6 mở trong ≤ 5 giây trên máy Core i5 8GB
- AC-04 (US-OPS-001): .LSP files được distribute kèm đúng thư mục
- AC-05 (US-OPS-001): Có hướng dẫn bypass SmartScreen hoặc code signing (nếu chưa ký)
- AC-06 (GLC-09): .exe chạy được trên ≥ 2 máy Windows sạch, smoke test pass
- AC-07: File size .exe < 300 MB
- AC-08: Build từ main branch — commit hash được ghi nhận trong release notes
- AC-09: Version number trong app đã cập nhật trước build

Module boundary:
- Chỉ chạm: `packaging/` config (PyInstaller .spec file), `src/__version__.py` (version number)
- Không sửa source code module nào khác
- Dependency: toàn bộ `src/` đã xong + T6-02 done (không còn P0/P1)

Files/Modules dự kiến bị ảnh hưởng:
- `packaging/roomqs.spec` — PyInstaller spec file (tạo mới hoặc cập nhật)
- `src/__version__.py` — cập nhật version
- `lisp/` — bundle kèm theo đúng thư mục
- `config.yaml` — bundle kèm theo

Doc refs:
- /docs/04-Kien-Truc-Tech-Stack.md (PyInstaller section)
- /docs/06-Setup-Moi-Truong-Trien-Khai.md (nếu có hướng dẫn build)
- /docs/05-Ke-Hoach-Sprint-Release.md#Pre-release-checklist (mục Build)
- /docs/03-User-Stories.md#US-OPS-001

Dependencies:
- T6-02 done (không còn P0 open)
- main branch sạch: CI green, không còn open TODO/FIXME trong code path critical
- Có sẵn 2 máy Windows sạch để smoke test (hoặc VM clean)

Known risks:
- PyInstaller + Shapely + PySide6 DLL conflict: đã validate từ Sprint 1 (BL-03) nhưng cần re-verify sau khi thêm tất cả module Sprint 2–5.
- Antivirus false positive (đặc biệt Windows Defender) có thể block .exe trên máy khách hàng → document workaround rõ trong Quick Guide.
- File size > 300 MB: nếu vượt, kiểm tra `--exclude-module` để loại dev-only packages (matplotlib, numpy nếu không dùng trong production).

Open ambiguities:
- .exe distribute theo thư mục onedir hay nén thành ZIP? Đề xuất: ZIP kèm README cài đặt ngắn.

Definition of Done:
- [ ] .exe build thành công từ main branch
- [ ] Smoke test pass trên Windows 10 và Windows 11 (máy sạch)
- [ ] Giao diện mở ≤ 5 giây
- [ ] Chạy được 1 test DXF nhỏ end-to-end trên máy sạch
- [ ] File size < 300 MB
- [ ] .LSP files bundle đúng thư mục
- [ ] Commit hash được ghi nhận

---

# TICKET CONTEXT PACK

Ticket: T6-04 — Viết Quick Guide (BL-39) + Release Checklist + PM Sign-off
Người phụ trách: PM/BA (Quick Guide) + PM + Tech Lead (Release Checklist + Sign-off)
Mục tiêu: Viết tài liệu hướng dẫn ngắn gọn để người dùng mới cài đặt và sử dụng RoomQS trong 15 phút. Hoàn thiện release checklist. PM ký go-live.

In scope:
- Quick Guide (PDF hoặc Markdown, ≤ 2 trang A4) bao gồm:
  1. Cài đặt: extract .exe, chạy RoomQS.exe
  2. Load .LSP vào AutoCAD: hướng dẫn dùng APPLOAD hoặc startup suite
  3. Chạy lần đầu: chọn DXF, nhập chiều cao và chiều dày tường, chạy pipeline
  4. Hiểu cảnh báo trên UI: phân biệt ERROR vs WARNING
  5. Xuất Excel và kiểm tra kết quả
  6. Xử lý SmartScreen bypass (nếu chưa có code signing)
  7. Known limitations: case nào tool chưa xử lý được (layer không chuẩn, phòng hình thù phức tạp)
- Release checklist review (PM + Tech Lead): duyệt toàn bộ pre-release checklist mục 8.4 trong tài liệu kế hoạch
- PM sign-off: gửi email xác nhận go-live

Out of scope:
- User manual đầy đủ (Phase 2)
- Video tutorial
- Multi-language guide

Story IDs: US-OPS-001 (một phần), không có story riêng — deliverable từ BL-39
Acceptance Criteria IDs: GLC-10 (PM sign-off), Release Gate

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: Quick Guide ≤ 2 trang A4, đủ 7 mục liệt kê trên
- AC-02: Người dùng mới đọc Quick Guide và chạy được tool trong 15 phút (verify với 1 người dùng)
- AC-03: Layer convention mặc định được document trong Quick Guide
- AC-04: Attribute block cửa expected được document
- AC-05: Known limitations list có ít nhất 3 case tool chưa xử lý
- AC-06 (GLC-10): PM sign-off email nhận được xác nhận go-live
- AC-07: Pre-release checklist mục 8.4 hoàn thành 100%: Code ✓, Build ✓, Data & Test ✓, Documentation ✓, Sign-off ✓

Module boundary:
- Không chạm source code
- Output: `docs/quick_guide.md` (hoặc `quick_guide.pdf`)
- Release checklist: dùng template từ Section 8.4 trong tài liệu kế hoạch

Files/Modules dự kiến bị ảnh hưởng:
- `docs/quick_guide.md` — tạo mới
- `docs/known_limitations.md` — tạo mới (hoặc section trong quick guide)
- `docs/layer_convention.md` — tạo mới hoặc append vào quick guide

Doc refs:
- /docs/05-Ke-Hoach-Sprint-Release.md#Pre-release-checklist (Section 8.4)
- /docs/05-Ke-Hoach-Sprint-Release.md#Go-live-criteria (GLC-10)
- /docs/04-Kien-Truc-Tech-Stack.md#ADR-04 (config.yaml — layer convention)
- /docs/02-PRD-Product-Backlog.md#Out-of-scope (Known limitations reference)

Dependencies:
- T6-03 done (có .exe final để guide người dùng cài đặt)
- T6-01 done (biết known limitations từ UAT)
- T6-02 done (không còn P0 — đảm bảo guide không hướng dẫn tính năng còn lỗi)

Known risks:
- Quick Guide viết trước khi .exe final có thể lỗi thời nếu smoke test (T6-03) phát hiện issue và cần thay đổi UX/flow nhỏ.
- Người dùng thực cần có AutoCAD để test Quick Guide — cần arrange sớm.

Open ambiguities:
- Quick Guide phân phối dưới dạng gì: in kèm vào thư mục .exe, hay email riêng? Đề xuất: để trong thư mục cùng .exe + gửi kèm email.

Definition of Done:
- [ ] Quick Guide hoàn chỉnh ≤ 2 trang, đủ 7 mục
- [ ] Ít nhất 1 người dùng mới đọc và chạy được tool trong 15 phút (verify)
- [ ] Pre-release checklist 100% complete (PM + Tech Lead ký)
- [ ] PM sign-off email đã gửi và nhận được xác nhận
- [ ] Sprint 6 — MILESTONE M7 (GO-LIVE) đạt được
