# SPRINT BRIEF

Sprint: Sprint 0 — Kickoff & Preparation
Phase: GIAI ĐOẠN 1 — DISCOVERY & FOUNDATION (Sprint 0–1)
Mục tiêu sprint: Đảm bảo toàn bộ điều kiện tiên quyết sẵn sàng trước khi Sprint 1 bắt đầu viết code. Không một dòng code nào được viết khi chưa có sample data, chưa align scope, chưa có repo chuẩn.

In-scope:
- Thu thập ≥ 2 file DXF thực từ khách hàng (đa dạng: phòng vuông + L-shape)
- Xác nhận draft template Excel output (3 sheet, cột tối thiểu) với end user
- Khởi tạo repo, cấu trúc thư mục, branching strategy, CI/CD pipeline cơ bản
- Cả team align về scope MVP vs out-of-scope qua tài liệu PRD/SRS
- Dev-B setup AutoCAD 2019+ trên máy dev, xác minh LISP load được

Out-of-scope:
- Viết bất kỳ dòng code Python/LISP nào
- Định nghĩa chi tiết format cột Excel (chỉ cần draft đủ để không block Sprint 3)
- Setup CI/CD pipeline đầy đủ (chỉ cần cấu trúc cơ bản đủ cho Sprint 1 dùng)
- Cài đặt dependency Python hay pytest (làm ở Sprint 1)

Risks:
- Khách hàng không cung cấp được file DXF thực trong tuần → Sprint 2 sẽ phải test trên file synthetic, tăng rủi ro UAT đáng kể
- Template Excel thay đổi sau khi đã xác nhận → sẽ block Sprint 5 hoặc cần rework Sprint 3
- AutoCAD không khả dụng trên máy Dev-B → không thể validate LISP ở Sprint 2

Dependencies:
- Khách hàng / end user cung cấp bản vẽ mẫu (bên ngoài team)
- Kickoff meeting đã diễn ra, PM đã đọc PRD v1.0

Danh sách ticket:
1. T0-01: Thu thập và xác nhận file DXF mẫu từ khách hàng
2. T0-02: Xác nhận draft template Excel output với end user
3. T0-03: Khởi tạo repo + cấu trúc thư mục chuẩn
4. T0-04: Thiết lập branching strategy + quy ước làm việc
5. T0-05: Team alignment PRD/SRS — align scope MVP vs out-of-scope
6. T0-06: Setup AutoCAD 2019+ trên máy Dev-B + verify LISP load

---

# TICKET CONTEXT PACK

Ticket: T0-01 — Thu thập và xác nhận file DXF mẫu từ khách hàng
Người phụ trách: PM
Mục tiêu: Có được ≥ 2 file DXF thực từ khách hàng đủ đa dạng (ít nhất 1 file có phòng vuông, 1 file có phòng L-shape hoặc giật cấp), được ghi chú layer convention, để Sprint 2 có thể validate thuật toán XR/GB trên data thực.

In scope:
- Liên hệ khách hàng/end user, thu thập file DXF bản vẽ mặt bằng kiến trúc
- Ghi chú: tên file, AutoCAD version, tên layer tường, tên layer text phòng, convention block cửa
- Xác nhận file không bị corrupt (ezdxf đọc được — QA/Dev-A verify nhanh)
- Lưu vào thư mục `samples/real-dxf/` trong repo (chú ý: không commit dữ liệu nhạy cảm)

Out of scope:
- Phân tích nội dung chi tiết file DXF (Sprint 1 làm)
- Tạo file DXF synthetic (chỉ làm nếu không lấy được file thực)
- Chạy bất kỳ script nào trên file

Story IDs: Không có story riêng (prerequisite cho US-INP-001, US-ROOM-001)
Acceptance Criteria IDs: Dẫn xuất từ Exit Criteria Sprint 0

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: ≥ 2 file DXF thực được lưu trong repo hoặc thư mục chia sẻ team, tên file ghi chú nguồn gốc
- AC-02: Mỗi file có ghi chú kèm: tên layer tường, tên layer text phòng, version AutoCAD xuất
- AC-03: Ít nhất 1 file có phòng hình chữ nhật; ít nhất 1 file có phòng L-shape hoặc có hơn 4 cạnh
- AC-04: Dev-A xác nhận file đọc được bằng ezdxf (không raise exception khi mở)
- AC-05: Nếu không lấy được file thực → PM thông báo toàn team chậm nhất ngày 3 của Sprint 0; team quyết định dùng synthetic và ghi nhận rủi ro UAT

Module boundary: Không có module code — đây là task quản lý dữ liệu

Files/Modules dự kiến bị ảnh hưởng:
- `samples/real-dxf/` (thư mục chứa file mẫu, không commit)
- `samples/real-dxf/README.md` (ghi chú layer convention)
- `.gitignore` (đảm bảo DXF thực không bị commit lên public repo)

Doc refs:
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 0 — Deliverables
- /docs/02-PRD-Product-Backlog.md#Giả định đầu vào
- /docs/02-PRD-Product-Backlog.md#Rủi ro dữ liệu DXF

Dependencies: Khách hàng phản hồi và cung cấp file (dependency ngoài team)

Known risks:
- Khách hàng chậm → phải dùng file synthetic → rủi ro UAT tăng cao ở Sprint 6
- File DXF có thể không đúng convention layer → ghi nhận để Sprint 1 xử lý BL-08 (config layer)

Open ambiguities:
- File DXF có được commit vào repo không hay lưu riêng? (Cần quyết định trước khi tạo repo)

Definition of Done:
- [ ] ≥ 2 file DXF lưu và accessible cho toàn team
- [ ] File đọc được bằng ezdxf (Dev-A verify)
- [ ] Ghi chú layer convention đi kèm mỗi file
- [ ] PM ghi nhận trạng thái vào Sprint 0 log (có / không lấy được)

---

# TICKET CONTEXT PACK

Ticket: T0-02 — Xác nhận draft template Excel output với end user
Người phụ trách: PM / BA
Mục tiêu: Có được draft template Excel (3 sheet: Dữ liệu theo Phòng, Dữ liệu theo Cửa, Cạnh Phòng) được end user xác nhận về cột tối thiểu, để Sprint 3 có thể đóng băng format và Sprint 5 không bị block bởi thay đổi muộn.

In scope:
- Soạn draft template Excel với 3 sheet theo tên đã định nghĩa trong config:
  - Sheet "Du lieu Phong": room_id, room_name, room_code, area_m2, perimeter_m, floor_finish_m2, wall_finish_m2
  - Sheet "Du lieu Cua": door_code, door_name, width_mm, height_mm, area_m2, related_room_a, related_room_b
  - Sheet "Canh Phong": room_id, edge_index, length_m, wall_finish_m2
- Gửi draft cho end user review và confirm qua email / comment
- Ghi nhận phản hồi: cột nào cần thêm, thứ tự cột, header naming

Out of scope:
- Format màu sắc, merge cell, số thập phân (đóng băng ở Sprint 3)
- Thêm sheet thứ 4 hoặc báo cáo tổng hợp (out of MVP scope)
- Công thức tính toán trong Excel (tool xuất số liệu, không xuất công thức)

Story IDs: US-EXP-001, US-EXP-002, US-EXP-003, US-EXP-004
Acceptance Criteria IDs: Dẫn xuất từ AC của US-EXP-001 và Exit Criteria Sprint 0

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: Draft template có đủ 3 sheet với tên đúng theo config.yaml: "Du lieu Phong", "Du lieu Cua", "Canh Phong"
- AC-02: Mỗi sheet có đủ cột header tối thiểu (xem In scope ở trên)
- AC-03: End user hoặc PM xác nhận draft qua email / comment trong issue tracker — đây là hard gate
- AC-04: Danh sách cột được lưu vào tài liệu nội bộ (wiki / Google Doc) để làm chuẩn cho Sprint 3

Module boundary: Không có module code — đây là task nghiệp vụ / UX

Files/Modules dự kiến bị ảnh hưởng:
- `samples/template-excel/template_v0.xlsx` (file mẫu để review)
- `docs/excel-template-spec.md` (ghi chú cột confirmed)

Doc refs:
- /docs/02-PRD-Product-Backlog.md#Xuất Excel multi-sheet
- /docs/04-Kien-Truc-Tech-Stack.md#ADR-04 (config export.sheet_names)
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 3 — BL-26

Dependencies: End user / PM phải available để review (ngoài team dev)

Known risks:
- End user muốn thêm cột phức tạp → cần negotiate xuống đúng scope MVP
- Không xác nhận được trước Sprint 3 → sẽ block BL-27 (sheet "Dữ liệu theo Phòng")

Open ambiguities:
- Header tên cột bằng tiếng Việt hay tiếng Anh? (Cần quyết định trong sprint này)
- Cột tổng cộng dưới mỗi sheet có trong MVP không?

Definition of Done:
- [ ] Draft template Excel có 3 sheet đúng tên
- [ ] End user xác nhận qua email/comment (evidence lưu lại)
- [ ] Danh sách cột final được document

---

# TICKET CONTEXT PACK

Ticket: T0-03 — Khởi tạo repo + cấu trúc thư mục chuẩn
Người phụ trách: Tech Lead / Dev-A
Mục tiêu: Repo được tạo với cấu trúc thư mục đúng theo kiến trúc đã định, README cơ bản, .gitignore đầy đủ, để Sprint 1 có thể clone và bắt đầu ngay mà không cần setup thêm.

In scope:
- Tạo repo trên GitHub (private)
- Tạo cấu trúc thư mục theo module map:
  ```
  src/intake/, src/cad_parser/, src/geometry/, src/room_engine/,
  src/door_engine/, src/text_extractor/, src/calc_engine/,
  src/validation/, src/export/, src/ui/, src/pipeline/,
  src/config/, src/utils/
  lisp/
  tests/
  samples/
  packaging/
  docs/
  ```
- Tạo README.md: mô tả project, yêu cầu hệ thống, cách setup
- Tạo .gitignore: Python, venv, .exe, *.dxf thực tế, output/
- Tạo requirements.txt với các dependency chính (version lock)
- Tạo config.yaml template với giá trị mặc định

Out of scope:
- CI/CD pipeline setup (T0-04)
- Cài đặt thực tế dependency trên máy dev (Sprint 1)
- Pre-commit hooks (Sprint 1 BL-02)

Story IDs: Liên quan gián tiếp US-OPS-001
Acceptance Criteria IDs: Dẫn xuất từ Exit Criteria Sprint 0 + Sprint 1 Entry Criteria

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: Repo tồn tại trên GitHub, tất cả team member có quyền clone
- AC-02: Cấu trúc thư mục đúng theo module map trong kiến trúc (04-Kien-Truc-Tech-Stack.md §5)
- AC-03: README.md có: mô tả project, requirements (Python 3.11.x, AutoCAD 2019+), bước clone và setup cơ bản
- AC-04: .gitignore bao gồm: `*.dxf`, `output/`, `dist/`, `*.exe`, `.venv/`, `__pycache__/`
- AC-05: requirements.txt có ezdxf>=1.3, Shapely>=2.0, openpyxl>=3.1, PySide6>=6.6, pytest>=7.4, PyInstaller>=6.0
- AC-06: config.yaml template có đủ các section: `cad`, `calculation`, `export` với giá trị mặc định

Module boundary: Infrastructure — không chứa logic; chỉ là scaffold

Files/Modules dự kiến bị ảnh hưởng:
- Toàn bộ cấu trúc repo (file mới, không edit file có sẵn)
- `config/config.yaml`
- `requirements.txt`
- `README.md`
- `.gitignore`

Doc refs:
- /docs/04-Kien-Truc-Tech-Stack.md#Module Breakdown — Module map tổng thể
- /docs/04-Kien-Truc-Tech-Stack.md#ADR-04
- /docs/06-Setup-Moi-Truong-Trien-Khai.md#2.5 Dependencies chính

Dependencies: Không có (task đầu tiên, không phụ thuộc ticket nào)

Known risks:
- Module map thay đổi nếu Tech Lead muốn điều chỉnh sau khi đọc lại kiến trúc → làm sớm để còn thời gian align

Open ambiguities: Không có — cấu trúc đã được định nghĩa rõ trong tài liệu kiến trúc

Definition of Done:
- [ ] Repo public/private tạo xong, team clone được
- [ ] Tất cả thư mục trong module map tồn tại (có file `__init__.py` hoặc `.gitkeep`)
- [ ] README, .gitignore, requirements.txt, config.yaml template đã commit
- [ ] Tech Lead review và approve cấu trúc

---

# TICKET CONTEXT PACK

Ticket: T0-04 — Thiết lập branching strategy + quy ước làm việc nhóm
Người phụ trách: Tech Lead
Mục tiêu: Cả team agree về cách làm việc trên Git để tránh conflict và không block nhau khi Sprint 1 bắt đầu song song.

In scope:
- Quyết định và document branching model (gợi ý: `main` + `develop` + `feature/xxx` + `hotfix/xxx`)
- Quy ước đặt tên branch: `feature/BL-03-pyinstaller-prototype`, `fix/xxx`
- Quy ước commit message: `[BL-xx] mô tả ngắn`
- Quy tắc merge: PR cần ít nhất 1 reviewer approve trước khi merge vào `develop`
- Quy ước CI gate: không merge nếu pytest fail
- Document vào `docs/CONTRIBUTING.md` hoặc README section

Out of scope:
- Setup CI/CD pipeline thực tế (chỉ document quy ước; pipeline cơ bản sẽ do Dev-A setup ở Sprint 1 BL-01/02)
- Code review checklist chi tiết

Story IDs: Không có story riêng (operational prerequisite)
Acceptance Criteria IDs: Dẫn xuất từ Exit Criteria Sprint 0

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: Branching model được document rõ ràng trong repo (CONTRIBUTING.md hoặc README section)
- AC-02: Dev-A và Dev-B đã đọc và confirm không có câu hỏi mở
- AC-03: Ví dụ tên branch và commit message được ghi cụ thể (không chỉ lý thuyết)
- AC-04: Quy tắc merge (PR + reviewer) và CI gate được ghi rõ

Module boundary: Không có module code — quy trình nhóm

Files/Modules dự kiến bị ảnh hưởng:
- `docs/CONTRIBUTING.md` (tạo mới)

Doc refs:
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 0 — Hạng mục chính

Dependencies: T0-03 (repo phải tồn tại trước)

Known risks: Không có rủi ro kỹ thuật; rủi ro là team không follow convention → cần Tech Lead enforce

Open ambiguities: Không có

Definition of Done:
- [ ] CONTRIBUTING.md commit vào repo
- [ ] Dev-A và Dev-B đã đọc và sign-off (comment trong PR hoặc Slack)

---

# TICKET CONTEXT PACK

Ticket: T0-05 — Team alignment: đọc PRD/SRS, align scope MVP vs out-of-scope
Người phụ trách: PM (tổ chức), tất cả thành viên (tham dự)
Mục tiêu: Cả team (Dev-A, Dev-B, QA) có cùng hiểu biết về scope MVP, những gì out-of-scope, và các giả định quan trọng — để không xây sai thứ trong Sprint 1–6.

In scope:
- PM tóm tắt các điểm then chốt từ PRD + SRS (không yêu cầu dev đọc hết 50 trang)
- Làm rõ 4 giả định quan trọng nhất:
  - A3: Sample DXF thực phải có trước Sprint 2
  - A4: AutoCAD 2019+ phải có trên máy Dev-B
  - A5: Template Excel phải confirm trước Sprint 4
  - A6: Chiều cao thông thủy và chiều dày tường do user nhập (không tự động đọc)
- Thống nhất out-of-scope: zero-click detection, ERP integration, preview DXF, xử lý DWG trực tiếp
- Xác nhận định nghĩa "MVP done" (xem 02-PRD §10 MVP acceptance)

Out of scope:
- Review chi tiết từng FR/BR (làm trong từng sprint)
- Ước lượng effort chi tiết (đã có trong kế hoạch sprint)

Story IDs: Không có story riêng — prerequisite cho toàn bộ project
Acceptance Criteria IDs: N/A

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: Session alignment diễn ra (≥ 1 giờ), có notes ghi lại câu hỏi và quyết định
- AC-02: Không có câu hỏi mở về scope MVP còn treo sau session
- AC-03: Tất cả thành viên biết rõ 4 giả định A3/A4/A5/A6 và hệ quả nếu sai
- AC-04: Team đồng ý với danh sách out-of-scope (đặc biệt: không xây zero-click detection trong MVP)

Module boundary: Không có module code

Files/Modules dự kiến bị ảnh hưởng:
- `docs/sprint0-alignment-notes.md` (ghi lại Q&A và decisions)

Doc refs:
- /docs/02-PRD-Product-Backlog.md#3. Phạm vi sản phẩm
- /docs/02-PRD-Product-Backlog.md#10. MVP acceptance
- /docs/05-Ke-Hoach-Sprint-Release.md#1.3 Giả định planning

Dependencies: T0-03 (repo phải có để commit notes)

Known risks: Không có rủi ro kỹ thuật — rủi ro là session bị hoãn hoặc thiếu người

Open ambiguities:
- Nếu Dev-B không có AutoCAD trên máy → cần escalate ngay trong session này, không đợi Sprint 2

Definition of Done:
- [ ] Session diễn ra và có notes
- [ ] Notes commit vào `docs/`
- [ ] PM xác nhận không có câu hỏi mở nghiêm trọng về scope

---

# TICKET CONTEXT PACK

Ticket: T0-06 — Setup AutoCAD 2019+ trên máy Dev-B + verify LISP load được
Người phụ trách: Dev-B
Mục tiêu: Máy Dev-B có AutoCAD 2019+ chạy được, LISP load thành công, để Sprint 2 Dev-B có thể bắt đầu viết và test thuật toán XR/GB ngay ngày đầu.

In scope:
- Cài AutoCAD 2019+ (hoặc xác nhận đã cài) trên máy Dev-B
- Tạo file .lsp stub đơn giản (ví dụ: `(defun c:TEST () (alert "LISP OK"))`)
- Load file .lsp vào AutoCAD bằng lệnh APPLOAD
- Chạy lệnh `TEST` trong AutoCAD command line → verify hoạt động
- Ghi chú phiên bản AutoCAD, OS, cách load LISP vào startup suite

Out of scope:
- Viết bất kỳ logic thuật toán nào (Sprint 2)
- Setup pyautocad hoặc COM bridge (Phase 2)
- Test với file DXF thực (Sprint 2)

Story IDs: Liên quan gián tiếp US-ROOM-001, US-ROOM-002
Acceptance Criteria IDs: Dẫn xuất từ Exit Criteria Sprint 0 (A4)

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: AutoCAD 2019 trở lên cài đặt và mở được trên máy Dev-B
- AC-02: File `.lsp` stub load thành công qua APPLOAD không báo lỗi
- AC-03: Lệnh `TEST` chạy trong AutoCAD command line và hiện dialog "LISP OK"
- AC-04: Dev-B ghi chú: AutoCAD version, OS version, đường dẫn APPLOAD, cách add vào startup suite
- AC-05: Ghi chú được commit vào `lisp/README.md`

Module boundary: AutoCAD/AutoLISP Layer — hoàn toàn tách biệt khỏi Python runtime

Files/Modules dự kiến bị ảnh hưởng:
- `lisp/README.md` (tạo mới — ghi chú setup)
- `lisp/test_stub.lsp` (file stub test, có thể xóa sau)

Doc refs:
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 0 — Hạng mục chính (Dev-B)
- /docs/05-Ke-Hoach-Sprint-Release.md#1.3 Giả định A4
- /docs/06-Setup-Moi-Truong-Trien-Khai.md (phần setup AutoCAD)

Dependencies: Không có (có thể làm song song với T0-03/T0-04)

Known risks:
- Không có license AutoCAD → cần escalate ngay với PM; đây là blocker cứng cho Sprint 2
- Antivirus block LISP execution → ghi nhận workaround vào README

Open ambiguities:
- AutoCAD LT không hỗ trợ LISP — nếu Dev-B chỉ có LT → blocker nghiêm trọng, cần đổi máy hoặc license

Definition of Done:
- [ ] AutoCAD 2019+ mở được trên máy Dev-B
- [ ] LISP stub load và chạy thành công
- [ ] lisp/README.md có ghi chú setup và verified
- [ ] Dev-B báo cáo kết quả cho PM (OK / blocked)
