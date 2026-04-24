# SPRINT BRIEF

Sprint: Sprint 5 — Export Excel + UI Hoàn thiện + Integration
Phase: GIAI ĐOẠN 4 — INTEGRATION & HARDENING (Tuần 9–10)
Mục tiêu sprint: Hoàn thiện luồng end-to-end từ DXF đến Excel. UI đầy đủ tính năng — chạy pipeline, hiển thị cảnh báo, xuất file, xem kết quả trước khi xuất. Integration test phát hiện edge case còn sót.

In-scope:
- BL-27: Tạo sheet "Dữ liệu theo phòng" trong file Excel xuất
- BL-28: Tạo sheet "Dữ liệu theo cửa" trong file Excel xuất
- BL-29: Tạo sheet "Dữ liệu theo cạnh" trong file Excel xuất
- BL-30: Format Excel: header bold, number format, merge cell tổng, số thập phân
- BL-32: UI nút chạy pipeline + QThread (không block UI) + progress bar
- BL-33: UI hiển thị cảnh báo dữ liệu không hợp lệ (phòng lỗi, cửa thiếu data, trùng lặp)
- BL-34: UI nút xuất Excel + dialog chọn thư mục + nút mở file
- BL-35: UI panel kiểm tra lại kết quả (preview table rooms + chi tiết phòng)
- Integration test end-to-end: toàn bộ pipeline DXF → Excel (QA)

Out-of-scope:
- Không thêm business rule mới (tất cả BR đã xong ở Sprint 4)
- Không thay đổi data model Room/Door/Edge
- Không sửa thuật toán tính toán (calc_engine)
- Không sửa LISP layer (đã xong từ Sprint 2–3)
- Preview DXF canvas đầy đủ (out of scope MVP)
- Chiều cao per-phòng khác nhau (Phase 2)
- Preview DXF inline trong app

Risks:
- Integration test lần đầu tiên chạy toàn bộ pipeline sẽ phát sinh bug data edge case (float precision, text ngoài polygon, cửa unassigned). Dành ≥ 3 ngày cuối sprint cho bug fix.
- openpyxl merge cell có thể conflict với frozen panes khi mở trên Excel cũ.
- Pipeline phải chạy trong QThread — không được gọi UI từ worker thread (dễ gây crash).
- File Excel đang mở bởi Excel.exe (locked) → export sẽ fail nếu không handle.

Dependencies:
- Sprint 4 exit criteria phải pass: 100% unit test BR-04/05/06, diện tích sai lệch < 1%, UAT checklist sẵn sàng.
- Template Excel đã được PM/end user xác nhận và đóng băng từ Sprint 3 (deadline cứng).
- Data model Room/Door/Edge từ Sprint 3–4 phải ổn định (không thay đổi interface).
- `config.yaml` với sheet_names, decimal_places, output_dir đã có từ Sprint 1.

Danh sách ticket:
1. T5-01: Implement Export Engine — 3 sheet Excel + Format (BL-27/28/29/30)
2. T5-02: Implement UI Pipeline Runner — QThread + Progress Bar (BL-32)
3. T5-03: Implement UI Warning Panel — Hiển thị cảnh báo dữ liệu (BL-33)
4. T5-04: Implement UI Export + Preview Panel (BL-34/35)
5. T5-05: Integration Test End-to-End DXF → Excel

---

# TICKET CONTEXT PACK

Ticket: T5-01 — Implement Export Engine: 3 sheet Excel + Format (BL-27/28/29/30)
Người phụ trách: Dev-A
Mục tiêu: Implement MOD-09 (Report Export Engine) xuất file Excel hợp lệ gồm đủ 3 sheet với format đúng template đã xác nhận. Đây là deliverable nghiệp vụ chính của sprint.

In scope:
- Tạo `src/export/export_engine.py` với class `ExcelExportEngine`
- Sheet "Du lieu Phong" (tên từ config: `sheet_names.rooms`): các cột bắt buộc theo US-EXP-002
- Sheet "Du lieu Cua" (tên từ config: `sheet_names.doors`): các cột theo US-EXP-003
- Sheet "Canh Phong" (tên từ config: `sheet_names.edges`): các cột theo US-EXP-003
- Format header: bold + background color
- Số thập phân: 2 chữ số (area, perimeter, chiều dài cạnh), 4 chữ số (diện tích cửa m²)
- Hàng tổng cộng (SUM) cuối sheet "Du lieu Phong" cho các cột số
- Tên file output: `BokTach_[timestamp].xlsx` tại `output_dir` từ config
- Không ghi ô None/NaN — thay bằng 0 hoặc chuỗi rỗng rõ ràng
- Unit test với fixture dữ liệu tổng hợp (≥ 3 phòng, ≥ 2 cửa, ≥ 6 cạnh)

Out of scope:
- Không implement UI (UI ở T5-04)
- Không xử lý progress bar (UI ở T5-02)
- Không thay đổi data model Room/Door/Edge
- Không merge format template từ file Excel bên ngoài

Story IDs: US-EXP-001, US-EXP-002, US-EXP-003
Acceptance Criteria IDs: US-EXP-001 AC-1 đến AC-6, US-EXP-002 AC tất cả, US-EXP-003 AC tất cả

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (US-EXP-001): File Excel được tạo với đúng 3 sheet tên khớp config
- AC-02 (US-EXP-001): Tổng số hàng sheet "Du lieu Phong" = số phòng hợp lệ đã xử lý
- AC-03 (US-EXP-001): Given 5 phòng + 8 cửa → sheet phòng có 5 hàng, sheet cửa có 8 hàng
- AC-04 (US-EXP-001): Không có ô None hoặc NaN trong cột số (thay bằng 0 hoặc rỗng)
- AC-05 (US-EXP-001): File mở được bằng Excel/LibreOffice không có warning corrupt
- AC-06 (US-EXP-002): Sheet "Du lieu Phong" có đủ các cột: Ma phong, Ten phong, Dien tich (m2), Chu vi (m), Chieu cao ap dung (m), So cua, Tong dien tich cua (m2), KL hoan thien san (m2), KL xu ly tuong (m2)
- AC-07 (US-EXP-002): Hàng tổng cộng cuối sheet — `sum(area)` khớp với cell tổng
- AC-08 (US-EXP-002): Header row được format (bold, background color); cột số format dạng number không phải text
- AC-09 (US-EXP-003): Sheet "Du lieu Cua" có cột: Ma cua, Ten cua, Chieu rong (mm), Chieu cao (mm), Dien tich cua (m2), Phong lien quan
- AC-10 (US-EXP-003): Cửa ranh giới chung: cột "Phong lien quan" hiển thị tên 2 phòng, phân cách " / "
- AC-11 (US-EXP-003): `Dien tich cua (m2)` = `width_mm × height_mm / 1_000_000`, làm tròn 4 chữ số
- AC-12 (US-EXP-003): Sheet "Canh Phong" có cột: Ma phong, Ten phong, Thu tu canh, Chieu dai canh (m)
- AC-13 (US-EXP-003): Tổng `Chieu dai canh` của 1 phòng = `Chu vi` phòng đó (±0.001m dung sai)

Module boundary:
- Chỉ chạm: `src/export/export_engine.py`, `src/export/__init__.py`
- Đọc từ: data model `Room`, `Door`, `Edge` (read-only), `Config` (singleton)
- KHÔNG chạm: `calc_engine`, `door_engine`, `room_engine`, `ui`, `pipeline`
- Dependency ngoài: `pandas ≥ 2.1`, `openpyxl ≥ 3.1`

Files/Modules dự kiến bị ảnh hưởng:
- `src/export/export_engine.py` — tạo mới
- `src/export/__init__.py` — tạo mới hoặc cập nhật
- `tests/test_export_engine.py` — tạo mới
- `config.yaml` — đọc section `export.sheet_names`, `export.decimal_places`, `export.output_dir`

Doc refs:
- /docs/03-User-Stories.md#US-EXP-001 đến US-EXP-003
- /docs/04-Kien-Truc-Tech-Stack.md#MOD-09
- /docs/02-PRD-Product-Backlog.md#BL-27-BL-28-BL-29-BL-30
- /docs/04-Kien-Truc-Tech-Stack.md#ADR-04 (config.yaml section export)

Dependencies:
- Sprint 4 done: data model Room/Door/Edge ổn định với đầy đủ fields (area, perimeter, edge_list, floor_finish_quantity, wall_finish_quantity, door assignments)
- Template Excel đã xác nhận bởi PM từ Sprint 3 (tên cột, số sheet, format tổng)
- `config.yaml` section `export` đã có

Known risks:
- `openpyxl` merge cell row tổng có thể conflict với auto-filter header. Test trên cả Excel 2016 và Excel 365.
- Phòng không có tên/mã → room_name/room_code có thể là None → phải normalize thành string rỗng hoặc placeholder trước khi ghi.
- Edge list của phòng phức tạp (L-shape 6+ đỉnh) → sheet "Canh Phong" có thể nhiều hàng, kiểm tra performance với > 100 phòng.

Open ambiguities:
- Thứ tự sheet trong workbook có quan trọng không? (Giả định: rooms → doors → edges)
- Nếu không có cửa nào (edge case): sheet "Du lieu Cua" ghi header rỗng hay bỏ qua? → cần xác nhận với PM trước khi code.
- Khi `room_code = None`, ghi gì vào cột "Ma phong"? Đề xuất: ghi "ROOM_[n]" như behavior định nghĩa trong EC-07.

Definition of Done:
- [ ] `ExcelExportEngine.export(rooms, doors, config)` tạo file .xlsx hợp lệ
- [ ] 3 sheet đúng tên từ config, đúng cấu trúc cột theo US-EXP-002/003
- [ ] Unit test pass: ≥ 5 test case covering happy path + edge case (phòng không có cửa, cửa ranh giới chung, room_code = None)
- [ ] File mở được bằng Excel không có warning
- [ ] Không có ô None/NaN trong cột số
- [ ] Code review approved
- [ ] Ghi chú update nếu interface export_engine thay đổi

---

# TICKET CONTEXT PACK

Ticket: T5-02 — Implement UI Pipeline Runner: QThread + Progress Bar (BL-32)
Người phụ trách: Dev-A (hoặc Dev-B nếu rảnh)
Mục tiêu: Implement nút "Chạy" pipeline trên PySide6 UI chạy toàn bộ pipeline trong QThread (không block UI). Progress bar cập nhật theo từng bước. UI vẫn responsive trong 30 giây xử lý.

In scope:
- Nút "Chay Pipeline" trên main window
- Tạo `PipelineWorker(QThread)` — wrap `pipeline.run(job_params)` trong worker thread
- Emit signals: `progress_updated(step: str, percent: int)`, `pipeline_finished(result: PipelineResult)`, `pipeline_error(error_msg: str)`
- Progress bar widget cập nhật khi nhận signal `progress_updated`
- Log panel append từng bước pipeline chạy đến đâu
- Sau khi done: kích hoạt nút "Xuat Excel" và "Panel ket qua"
- Disable nút "Chay" trong khi pipeline đang chạy
- Handle exception trong worker: emit `pipeline_error`, hiển thị dialog lỗi, không crash app

Out of scope:
- Không implement UI export (T5-04)
- Không implement warning panel (T5-03)
- Không implement preview panel (T5-04)
- Không thay đổi logic pipeline orchestrator (chỉ wrap trong QThread)

Story IDs: US-EXP-001 (FR-22, NFR-06)
Acceptance Criteria IDs: US-EXP-001 AC-6 (progress bar)

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: Pipeline chạy trong QThread, UI không bị freeze khi pipeline xử lý 30 giây
- AC-02: Progress bar cập nhật ít nhất tại 3 mốc: bắt đầu, giữa pipeline, hoàn thành
- AC-03: Nút "Chay" bị disable trong khi pipeline đang chạy
- AC-04: Sau khi pipeline hoàn thành, nút "Xuat Excel" và panel kết quả được kích hoạt
- AC-05: Nếu pipeline raise exception, app không crash — hiển thị error dialog với message rõ ràng

Module boundary:
- Chỉ chạm: `src/ui/main_window.py`, `src/ui/pipeline_worker.py` (tạo mới)
- Đọc/gọi: `src/pipeline/orchestrator.py` (không sửa nội bộ orchestrator)
- KHÔNG chạm: `calc_engine`, `export_engine`, `door_engine`, `room_engine`
- Dependency: PySide6 QThread, QObject signals/slots

Files/Modules dự kiến bị ảnh hưởng:
- `src/ui/pipeline_worker.py` — tạo mới
- `src/ui/main_window.py` — thêm widget progress bar + kết nối signals

Doc refs:
- /docs/04-Kien-Truc-Tech-Stack.md#MOD-10 (UI / Workflow Orchestration)
- /docs/04-Kien-Truc-Tech-Stack.md#MOD-11 (Pipeline Orchestrator)
- /docs/03-User-Stories.md#US-EXP-001

Dependencies:
- `src/pipeline/orchestrator.py` đã có (từ Sprint 3–4) — chỉ cần wrap
- `JobParams` data class đã định nghĩa

Known risks:
- **Critical rule:** Tuyệt đối không call UI widget method từ trong QThread worker — phải dùng signal/slot. Vi phạm gây crash ngẫu nhiên trên Windows.
- Nếu pipeline raise `CRITICAL` error (file DXF không đọc được) vs `WARNING` (một số phòng lỗi) → cần phân biệt hành vi: CRITICAL dừng hoàn toàn, WARNING cho phép tiếp tục.

Open ambiguities:
- Pipeline orchestrator hiện tại có emit progress signal không? Nếu chưa, cần thêm callback mechanism vào orchestrator để PipelineWorker nhận được tiến trình từng bước.

Definition of Done:
- [ ] `PipelineWorker` chạy pipeline trong QThread, không block UI thread
- [ ] Progress bar cập nhật live khi pipeline chạy
- [ ] UI không freeze — kiểm tra bằng cách click/scroll UI trong lúc pipeline đang chạy
- [ ] Exception handling: không crash app khi pipeline fail
- [ ] Code review approved

---

# TICKET CONTEXT PACK

Ticket: T5-03 — Implement UI Warning Panel: Hiển thị cảnh báo dữ liệu (BL-33)
Người phụ trách: Dev-A
Mục tiêu: Sau khi pipeline chạy xong, UI tổng hợp và hiển thị tất cả cảnh báo/lỗi từ `ValidationIssue` list — phòng lỗi, cửa thiếu data, dữ liệu trùng lặp. Người dùng biết chính xác cần kiểm tra lại gì trước khi xuất Excel.

In scope:
- Warning panel widget (QListWidget hoặc QTableWidget) hiển thị `List[ValidationIssue]` từ `PipelineResult`
- Tóm tắt trên UI: "X phòng hợp lệ, Y phòng cảnh báo, Z cửa invalid"
- Phân loại severity: ERROR (đỏ), WARNING (vàng), INFO (xám)
- Ghi toàn bộ warnings ra file `warnings_[timestamp].txt` tại output_dir
- Cảnh báo đặc thù cần xuất hiện đúng:
  - Phòng không có tên/mã: "Phong [ID] chua co ten hoac ma phong"
  - Cửa thiếu kích thước: "Cua D1: Thieu kich thuoc, khong tinh vao kq"
  - Cửa không gán được phòng: "Cua [ma]: Khong xac dinh duoc phong"
  - Polygon không valid: "Phong [ID] co ranh gioi khong hop le, bo qua"
  - Dữ liệu trùng lặp: "Phong [ID] duoc nhan dien nhieu lan, giu 1 ket qua"

Out of scope:
- Không implement fix lỗi trong UI (chỉ hiển thị cảnh báo, không sửa)
- Không thay đổi logic validation trong MOD-08
- Không implement filter/search cảnh báo (Phase 2)

Story IDs: US-ALERT-001, US-ALERT-002, US-ALERT-003
Acceptance Criteria IDs: US-ALERT-001 AC tất cả, US-ALERT-002 AC tất cả, US-ALERT-003 AC-1,2,3

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (US-ALERT-001): Given phòng không có text tên/mã → cảnh báo "Phong [ID] chua co ten hoac ma phong" hiển thị trên UI
- AC-02 (US-ALERT-001): Given polygon không valid → cảnh báo "Phong [ID] co ranh gioi khong hop le, bo qua"
- AC-03 (US-ALERT-001): Toàn bộ cảnh báo được ghi vào file `warnings_[timestamp].txt`
- AC-04 (US-ALERT-001): UI hiển thị tóm tắt: "X phong hop le, Y phong canh bao" trước khi cho xuất Excel
- AC-05 (US-ALERT-002): Given cửa D1 không có width/height → cảnh báo "Cua D1: Thieu kich thuoc, khong tinh vao kq"
- AC-06 (US-ALERT-002): Given cửa nằm ngoài mọi phòng → cảnh báo "Cua [ma]: Khong xac dinh duoc phong"
- AC-07 (US-ALERT-002): Cửa invalid/unassigned không xuất hiện trong tổng số cửa của phòng
- AC-08 (US-ALERT-002): Số lượng cảnh báo cửa được hiển thị trên UI
- AC-09 (US-ALERT-003): Given click 2 lần cùng phòng → cảnh báo "Phong [ID] duoc nhan dien nhieu lan, giu 1 ket qua"
- AC-10 (US-ALERT-003): Cảnh báo trùng lặp được ghi vào warning log, không block luồng xử lý

Module boundary:
- Chỉ chạm: `src/ui/warning_panel.py` (tạo mới), `src/ui/main_window.py`
- Đọc từ: `PipelineResult.issues: List[ValidationIssue]` (read-only)
- Ghi tới: `warnings_[timestamp].txt` qua `utils/logger.py` (infrastructure)
- KHÔNG chạm: `validation/`, `room_engine`, `door_engine`, `calc_engine`

Files/Modules dự kiến bị ảnh hưởng:
- `src/ui/warning_panel.py` — tạo mới
- `src/ui/main_window.py` — thêm warning panel widget
- `src/utils/warning_writer.py` — tạo mới hoặc mở rộng logger

Doc refs:
- /docs/03-User-Stories.md#US-ALERT-001 đến US-ALERT-003
- /docs/03-User-Stories.md#Edge-Cases (Section 5: EC-01 đến EC-23)
- /docs/04-Kien-Truc-Tech-Stack.md#MOD-08 (Validation Engine)
- /docs/04-Kien-Truc-Tech-Stack.md#severity-table (CRITICAL/ERROR/WARNING/INFO)

Dependencies:
- `ValidationIssue` data class và `PipelineResult` đã định nghĩa (Sprint 3–4)
- MOD-08 Validation Engine đã produce `List[ValidationIssue]` (Sprint 4)
- T5-02 phải done trước để có `PipelineResult` trả về

Known risks:
- Severity CRITICAL (file không đọc được) vs WARNING (phòng lỗi) có UI flow khác nhau — CRITICAL phải block xuất Excel, WARNING chỉ inform. Cần rõ ràng trong implementation.
- File `warnings_[timestamp].txt` ghi thất bại nếu output_dir không có quyền write → bắt exception, log console, không crash.

Open ambiguities:
- Khi không có cảnh báo nào → warning panel ẩn hoàn toàn hay hiển thị "Khong co canh bao"? Đề xuất: hiển thị "Khong co canh bao" (tốt hơn cho user experience).

Definition of Done:
- [ ] Warning panel hiển thị đúng từng loại cảnh báo với màu theo severity
- [ ] Tóm tắt "X phong hop le, Y phong canh bao" xuất hiện đúng
- [ ] File warnings_*.txt được ghi sau mỗi lần pipeline chạy
- [ ] Cửa invalid không xuất hiện trong tổng cửa của phòng (verify qua preview panel T5-04)
- [ ] Code review approved

---

# TICKET CONTEXT PACK

Ticket: T5-04 — Implement UI Export + Preview Panel (BL-34/35)
Người phụ trách: Dev-A
Mục tiêu: Nút "Xuat Excel" mở dialog chọn thư mục, gọi ExportEngine, hiển thị progress và thông báo kết quả, cho phép mở file ngay. Panel "Kiem tra ket qua" hiển thị bảng tổng hợp phòng + chi tiết từng phòng để user review trước khi xuất.

In scope:
- Nút "Xuat Excel": disable cho đến khi pipeline hoàn thành thành công
- Dialog chọn thư mục xuất (mặc định: `output_dir` từ config)
- Tên file: `BokTach_[timestamp].xlsx`
- Gọi `ExcelExportEngine.export()` trong QThread hoặc đồng bộ (nếu nhanh)
- Progress indicator khi ghi Excel
- Thông báo thành công + đường dẫn file
- Nút "Mo file": gọi `os.startfile(output_path)` (Windows)
- Handle lỗi ghi file: permission denied, disk full, file locked by Excel
- Preview panel (QTableWidget): hiển thị danh sách phòng với area, perimeter, số cửa, KL sàn, KL tường
- Click vào hàng phòng trong preview → hiển thị chi tiết: danh sách cửa liên quan, danh sách cạnh
- Phòng có cảnh báo: highlight màu vàng/đỏ trong bảng

Out of scope:
- Không implement export multi-format (chỉ .xlsx)
- Không edit trực tiếp dữ liệu từ preview panel
- Không implement filter/sort trong preview table (Phase 2)

Story IDs: US-EXP-001, US-EXP-004
Acceptance Criteria IDs: US-EXP-001 AC-5,6, US-EXP-004 AC tất cả

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (US-EXP-001): Nút "Xuat Excel" chỉ kích hoạt sau khi pipeline thành công
- AC-02 (US-EXP-001): File Excel được tạo với tên BokTach_[timestamp].xlsx
- AC-03 (US-EXP-001): Thư mục xuất không quyền write → thông báo lỗi, gợi ý chọn thư mục khác
- AC-04 (US-EXP-001): File cùng tên đã tồn tại → hỏi user ghi đè hay tạo tên mới
- AC-05 (US-EXP-001): Progress bar cập nhật khi ghi Excel, UI không freeze
- AC-06 (US-EXP-004): UI hiển thị bảng kết quả tổng hợp sau khi xử lý xong (trước khi xuất Excel)
- AC-07 (US-EXP-004): Có thể click vào từng phòng để xem chi tiết: diện tích, chu vi, danh sách cửa, danh sách cạnh
- AC-08 (US-EXP-004): Phòng có cảnh báo (thiếu tên, cửa invalid) được highlight màu khác trong bảng
- AC-09 (US-EXP-004): User có thể scroll qua toàn bộ danh sách phòng
- AC-10 (EC-20/21/22): Handle: permission denied → lỗi + gợi ý; disk full → "Khong du dung luong dia"; file locked → "File dang duoc mo boi chuong trinh khac"

Module boundary:
- Chỉ chạm: `src/ui/export_panel.py` (tạo mới), `src/ui/result_preview.py` (tạo mới), `src/ui/main_window.py`
- Gọi: `src/export/export_engine.py` (T5-01 phải done)
- Đọc: `PipelineResult` (rooms, doors, issues)
- KHÔNG chạm: `calc_engine`, `room_engine`, `door_engine`, `pipeline`

Files/Modules dự kiến bị ảnh hưởng:
- `src/ui/export_panel.py` — tạo mới
- `src/ui/result_preview.py` — tạo mới
- `src/ui/main_window.py` — integrate các panel mới

Doc refs:
- /docs/03-User-Stories.md#US-EXP-001 và US-EXP-004
- /docs/03-User-Stories.md#Edge-Cases EC-20 đến EC-23 (lỗi export file)
- /docs/04-Kien-Truc-Tech-Stack.md#MOD-10 (UI)

Dependencies:
- T5-01 (ExcelExportEngine) phải done
- T5-02 (PipelineWorker, PipelineResult) phải done
- T5-03 (ValidationIssue severity) nên done để highlight đúng màu

Known risks:
- `os.startfile()` chỉ có trên Windows — nếu test trên Linux/Mac sẽ crash. Wrap trong `if sys.platform == "win32"`.
- Preview table với > 50 phòng: performance có thể chậm nếu dùng naive QTableWidget. Xem xét lazy loading nếu cần.

Open ambiguities:
- Chi tiết phòng khi click: hiển thị trong separate dialog hay trong expandable row? Đề xuất: side panel hoặc dialog đơn giản.

Definition of Done:
- [ ] Nút "Xuat Excel" hoạt động đúng sau khi pipeline done
- [ ] Handle đầy đủ 3 lỗi export: permission denied, disk full, file locked
- [ ] Preview table hiển thị đúng tất cả phòng, highlight phòng có cảnh báo
- [ ] Click vào phòng xem được chi tiết
- [ ] Nút "Mo file" mở được file Excel vừa tạo
- [ ] Code review approved

---

# TICKET CONTEXT PACK

Ticket: T5-05 — Integration Test End-to-End: DXF → Excel
Người phụ trách: QA
Mục tiêu: Chạy toàn bộ pipeline từ DXF thực → click phòng trong AutoCAD → Python xử lý → xuất Excel và verify end-to-end. Đây là lần đầu tiên toàn bộ pipeline được chạy thực sự và sẽ phát hiện edge case mà unit test không cover.

In scope:
- Integration test với ít nhất 1 file DXF đầy đủ (≥ 5 phòng, ≥ 3 cửa, có ít nhất 1 cửa ranh giới chung)
- Verify exit criteria Sprint 5:
  - End-to-end chạy thành công, Excel xuất được
  - Tất cả cảnh báo hiển thị đúng trên UI
  - UI responsive (không freeze 30 giây)
  - Tổng `area` trong sheet phòng khớp với cell tổng cộng
  - File Excel mở được không có warning corrupt
- Bug triage: phân loại P0/P1/P2 cho mọi issue phát sinh
- Test edge cases: phòng không có tên, cửa thiếu kích thước, thư mục xuất bị lock
- Regression test: chạy lại test fixture từ Sprint 4 qua pipeline đầy đủ

Out of scope:
- UAT với người dùng thực (Sprint 6)
- Test trên bản vẽ phức tạp hơn (Sprint 6)
- Performance test scale lớn (> 50 phòng)

Story IDs: US-EXP-001, US-EXP-002, US-EXP-003, US-EXP-004, US-ALERT-001, US-ALERT-002
Acceptance Criteria IDs: Sprint 5 Exit Criteria (từ 05-Ke-Hoach-Sprint-Release.md)

Acceptance Criteria (copy/tóm tắt chính xác — Sprint 5 Exit Criteria):
- AC-01: End-to-end test chạy thành công với ít nhất 1 file DXF đầy đủ (≥ 5 phòng, ≥ 3 cửa)
- AC-02: File Excel đầu ra mở được bằng Excel, không có warning corrupt
- AC-03: Tất cả cảnh báo (phòng lỗi, cửa invalid, trùng lặp) hiển thị đúng trên UI
- AC-04: UI responsive: pipeline chạy 30 giây không freeze, progress bar cập nhật
- AC-05: Tổng `area` trong sheet phòng khớp với tổng trong cell tổng cộng
- AC-06: Tất cả P0/P1 bug từ integration test được ghi nhận với reproduction steps, file DXF gây lỗi, expected vs actual

Module boundary:
- QA test cross-module: toàn bộ pipeline từ input đến output
- Không sửa code — chỉ report bug với đủ thông tin để Dev fix

Files/Modules dự kiến bị ảnh hưởng:
- Test artifacts: `tests/integration/test_e2e_pipeline.py` (nếu có tự động hoá)
- UAT checklist từ BL-36 (Sprint 4) — dùng làm framework test

Doc refs:
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint-5-Exit-Criteria
- /docs/02-PRD-Product-Backlog.md#Sprint-5
- /docs/03-User-Stories.md#Edge-Cases (Section 5)
- /docs/05-Ke-Hoach-Sprint-Release.md#Demo-Checklist (S5: End-to-end DXF → click → Excel)

Dependencies:
- T5-01, T5-02, T5-03, T5-04 tất cả phải done
- File DXF test (≥ 5 phòng, ≥ 3 cửa, 1 cửa ranh giới chung) đã sẵn sàng từ Sprint 0–2
- AutoCAD 2019+ có sẵn trên máy test
- UAT checklist BL-36 đã hoàn chỉnh từ Sprint 4

Known risks:
- Integration test có thể phát hiện bug data edge case từ tọa độ float precision LISP, text ngoài polygon, cửa unassigned → buffer 2–3 ngày bug fix cuối sprint.
- Nếu phát sinh P0 bug, Dev phải fix trong sprint này trước khi sprint demo.

Open ambiguities:
- Cần xác nhận file DXF test có đủ case không: có cửa ranh giới chung, có phòng L-shape, có phòng không có text. QA cần kiểm tra với PM/BA trước khi bắt đầu test.

Definition of Done:
- [ ] Toàn bộ Sprint 5 exit criteria được verify và ghi kết quả rõ ràng (pass/fail + evidence)
- [ ] Bug report đầy đủ cho mọi P0/P1 issue với reproduction steps
- [ ] Sprint demo artifact sẵn sàng: chạy live DXF → click → Excel xuất → mở file trước PM
- [ ] PM xác nhận exit criteria pass trong Sprint Review meeting
