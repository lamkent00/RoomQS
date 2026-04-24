# 02 — PRD + Product Backlog Tổng

**Tên sản phẩm:** RoomQS — Công cụ tự động nhận diện phòng và bóc khối lượng từ bản vẽ mặt bằng  
**Phiên bản tài liệu:** v1.0  
**Nguồn gốc:** Dẫn xuất từ SRS v1.0 + Techstack đã chốt  
**Đối tượng đọc:** PM · BA · Tech Lead · QA Lead · Dev Team  
**Ngày:** _(cập nhật khi phát hành)_

---

## 1. Tổng quan sản phẩm

### Tên sản phẩm
**RoomQS** – Room Quantity Surveying Tool

### Bài toán cần giải quyết
Người làm bóc tách khối lượng (QS) hiện phải đo tay từng phòng trong bản vẽ AutoCAD: đọc text, chép kích thước, tính diện tích/chu vi bằng tay, rồi nhập lại vào Excel. Quy trình này chậm, dễ sai, và không tái sản xuất được khi bản vẽ thay đổi.

### Bối cảnh sử dụng
- Đầu vào: File bản vẽ mặt bằng kiến trúc (.DWG / .DXF) của một căn hộ hoặc một khu vực có nhiều phòng. Bản vẽ đã có sẵn text tên phòng, mã phòng và block cửa có thuộc tính.
- Môi trường: Máy tính Windows của kỹ sư/kỹ thuật viên QS có cài AutoCAD (2019+).
- Luồng chính: Người dùng mở AutoCAD → chạy công cụ (AutoLISP + Python desktop app) → click chọn phòng → nhận kết quả Excel.

### Giá trị mang lại
| Người dùng | Giá trị |
|---|---|
| Kỹ thuật viên QS | Giảm 70–80% thời gian đo bóc thủ công cho một mặt bằng |
| Kiểm tra viên | Kết quả truy vết được theo từng phòng, từng cạnh, từng cửa |
| PM / Chủ đầu tư | Số liệu nhất quán, chuẩn hóa giữa các dự án |

### Mục tiêu sản phẩm
1. Tự động hóa toàn bộ chuỗi: đọc bản vẽ → nhận diện phòng → nhận diện cửa → tính toán → xuất Excel trong một lần chạy.
2. Kết quả phải chính xác và kiểm tra lại được theo từng phòng, từng cửa, từng cạnh.
3. Đóng gói thành công cụ chạy được trên Windows mà không yêu cầu người dùng cài Python.

---

## 2. Mục tiêu business và mục tiêu vận hành

### Business goals
- **BG-01:** Rút ngắn chu kỳ bóc tách khối lượng cho một mặt bằng từ nhiều giờ xuống dưới 30 phút.
- **BG-02:** Loại bỏ sai sót nhập liệu thủ công, đảm bảo số liệu nhất quán qua các lần xử lý.
- **BG-03:** Tạo nền tảng để mở rộng sang các loại đối tượng khác (cột, dầm, hoàn thiện trần) ở giai đoạn sau.

### User goals
- **UG-01:** Xử lý toàn bộ phạm vi một căn hộ / mặt bằng trong một thao tác.
- **UG-02:** Nhận file Excel đầy đủ, có thể dùng ngay không cần chỉnh sửa thủ công.
- **UG-03:** Biết rõ phòng nào có lỗi dữ liệu để xử lý riêng, không bị âm thầm ra kết quả sai.

### Success metrics / KPI cho MVP
| Chỉ số | Mục tiêu |
|---|---|
| Thời gian xử lý một căn hộ ≤ 10 phòng | < 15 phút/căn (từ mở file đến có Excel) |
| Độ chính xác diện tích phòng so với đo tay | Sai lệch < 1% |
| Tỷ lệ phòng nhận diện thành công / tổng phòng trong test case | ≥ 90% |
| Tỷ lệ cửa được gán đúng phòng | ≥ 95% |
| Lỗi nghiêm trọng (crash, xuất sai mà không cảnh báo) | 0 trong test case UAT |

### Chỉ số đo hiệu quả sau go-live
- Số căn hộ xử lý thành công mỗi tuần (adoption).
- Số ticket báo lỗi số liệu từ người dùng (quality).
- Tỷ lệ người dùng cần can thiệp thủ công trên 1 file (automation coverage).

---

## 3. Phạm vi sản phẩm

### In scope cho MVP
- Đọc file DXF (export từ AutoCAD) và/hoặc tương tác trực tiếp với AutoCAD qua AutoLISP.
- Người dùng click chọn điểm bên trong từng phòng để hỗ trợ nhận diện (FR-02, FR-04).
- Tự động tạo đường bao khép kín (Polyline) cho từng phòng qua AutoLISP + lệnh BPOLY/Boundary (FR-05).
- Đọc tên phòng, mã phòng từ text có sẵn trong bản vẽ (FR-03, FR-07).
- Đọc thông tin cửa từ block thuộc tính trên bản vẽ và/hoặc từ file Excel đầu vào (FR-03, FR-08, FR-09).
- Gán cửa vào phòng hoặc cặp phòng (FR-10, FR-11).
- Tính diện tích, chu vi, chiều dài từng cạnh (FR-12, FR-13, FR-14).
- Tính khối lượng hoàn thiện sàn và xử lý bề mặt tường theo BR-04, BR-05, BR-06.
- Áp dụng quy tắc cửa trên ranh giới chung (BR-06).
- Xuất Excel multi-sheet: sheet theo phòng, theo cửa, theo cạnh (FR-18–FR-21).
- Cảnh báo dữ liệu không hợp lệ (FR-23).
- Giao diện desktop Python (PySide6) để cấu hình và xem kết quả (FR-22, FR-24).
- Đóng gói .exe chạy trên Windows (PyInstaller).

### Out of scope (MVP)
- Thiết kế 3D, lập tiến độ, dự toán tổng thể.
- Bóc tách các hạng mục ngoài phòng và cửa (cột, dầm, trần, MEP).
- Tự động nhận diện phòng hoàn toàn không cần click (zero-click room detection).
- Quản trị người dùng, phân quyền, multi-tenant.
- Tích hợp với hệ thống ERP / BIM.
- Preview DXF canvas đầy đủ tính năng trong app Python.
- Xử lý file DWG trực tiếp mà không qua export DXF hoặc AutoCAD COM.

### Giả định đầu vào
- Bản vẽ có layer tường rõ ràng, ranh giới phòng về cơ bản khép kín (có thể hở tại vị trí cửa — xử lý bằng Door Sealing).
- Text tên phòng và mã phòng nằm bên trong vùng phòng tương ứng.
- Block cửa có thuộc tính mã, tên, chiều rộng, chiều cao.
- Đơn vị bản vẽ là mm, nhất quán trong toàn file.
- Người dùng có AutoCAD 2019+ để chạy phần AutoLISP.
- Chiều cao thông thủy và chiều dày tường được nhập bởi người dùng trước khi chạy (không đọc tự động từ bản vẽ — **giả định**).

### Dependencies
- AutoCAD 2019+ cài trên máy người dùng (cho luồng AutoLISP + BPOLY).
- Python 3.12+, ezdxf, Shapely, pandas, openpyxl, PySide6 (được bundle vào .exe).
- File DXF export từ AutoCAD hoặc kết nối COM qua pyautocad.

---

## 4. Chân dung người dùng

### Nhóm 1 — Kỹ thuật viên QS (Người dùng chính)
- **Công việc:** Bóc tách khối lượng hoàn thiện (sàn, tường, cửa) cho các căn hộ từ bản vẽ kiến trúc.
- **Công cụ hiện tại:** AutoCAD (đo tay) + Excel (tổng hợp).
- **Pain points:**
  - Đo từng phòng bằng tay mất 20–40 phút/căn.
  - Hay nhầm đơn vị, sai khi ghi chu vi hoặc diện tích.
  - Không có cách kiểm tra lại số liệu nhanh nếu bản vẽ thay đổi.
- **Mục tiêu khi dùng công cụ:**
  - Click chọn phòng, nhận Excel ngay trong vài phút.
  - Biết ngay phòng nào lỗi dữ liệu để xử lý riêng.

### Nhóm 2 — Người kiểm tra / Tổng hợp báo cáo
- **Công việc:** Duyệt số liệu, lập báo cáo tổng hợp nhiều căn hộ.
- **Pain points:** Số liệu từ nhiều người khác nhau, không nhất quán format.
- **Mục tiêu:** Nhận Excel chuẩn format, dễ tổng hợp, dễ kiểm tra chéo.

### Nhóm 3 — Người nghiệm thu / PM kỹ thuật (Gián tiếp)
- **Mục tiêu:** Kết quả truy vết được, có audit trail từ số liệu đến từng cạnh phòng.

---

## 5. Product requirements summary

### Capability map và ưu tiên

| Capability | FR / BR liên quan | Ưu tiên |
|---|---|---|
| Đọc DXF và nhận dữ liệu hình học | FR-01, FR-03 | **Must** |
| Chọn phạm vi xử lý (vùng / căn hộ) | FR-02 | **Must** |
| Nhận diện phòng qua click + BPOLY | FR-04, FR-05 | **Must** |
| Loại bỏ phòng trùng lặp | FR-06 | **Must** |
| Gắn tên, mã phòng từ text | FR-07, BR-07 | **Must** |
| Nhận diện block cửa và đọc thuộc tính | FR-08, FR-09 | **Must** |
| Nhập cửa từ file Excel đầu vào | FR-03 (note) | **Should** |
| Gán cửa vào phòng / cặp phòng | FR-10, FR-11, BR-03 | **Must** |
| Tính diện tích, chu vi, cạnh | FR-12, FR-13, FR-14 | **Must** |
| Tính khối lượng sàn | FR-15, BR-04 | **Must** |
| Tính khối lượng tường (trừ cửa) | FR-16, FR-17, BR-05 | **Must** |
| Xử lý cửa trên ranh giới chung | BR-06 | **Must** |
| Xuất Excel multi-sheet | FR-18, FR-19, FR-20, FR-21 | **Must** |
| Xử lý toàn bộ mặt bằng 1 lần | FR-22 | **Must** |
| Cảnh báo dữ liệu không hợp lệ | FR-23, NFR-07 | **Must** |
| Kiểm tra lại kết quả trong app | FR-24, NFR-03 | **Should** |
| Nhận diện phòng không vuông vức (L-shape) | FR-04 (note GB algorithm) | **Should** |
| Preview DXF trong app | — | **Could** |
| Unit test bộ rule tính toán | NFR-04 | **Must (Dev)** |
| Đóng gói .exe Windows | — | **Must** |

---

## 6. Release strategy

### MVP (Phase 1)
**Mục tiêu:** Đủ để xử lý một căn hộ điển hình (phòng vuông vức đến giật cấp nhẹ) và xuất Excel đầy đủ.

**Phạm vi:**
- Toàn bộ capability đánh dấu **Must** ở bảng trên.
- Luồng AutoLISP: XR (phòng vuông vức) + GB (phòng L-shape cơ bản).
- Nhập cửa chủ yếu qua block thuộc tính; nhập từ Excel là fallback.
- Giao diện Python: nhập tham số (chiều cao, chiều dày tường), chạy, xem log, xuất Excel.
- Đóng gói .exe + .LSP bundle.

### Post-MVP / Phase 2
**Phạm vi:**
- Nhập cửa từ Excel đầu vào đầy đủ (FR-03 note).
- Preview DXF canvas trong app (matplotlib / QPainter).
- Nhận diện phòng tự động không cần click (zero-click room detection — R&D).
- Hỗ trợ bóc tách thêm hạng mục (trần, cột, dầm) — mở rộng scope SRS.
- Cấu hình rule nghiệp vụ qua UI (chiều cao theo từng phòng, hệ số vật liệu).

### Lý do chia phase
- Room recognition (FR-04, FR-05) là engineering core khó nhất. Cần prototype sớm và validate với bản vẽ thực trước khi mở rộng scope.
- MVP tập trung vào luồng bán tự động (user click chọn phòng) để kiểm soát rủi ro kỹ thuật.
- Zero-click detection cần thêm thời gian R&D; không đưa vào MVP để tránh delay.

---

## 7. Danh sách Epic

### EPIC-01 — Hạ tầng dự án & môi trường phát triển

| Trường | Nội dung |
|---|---|
| **Epic ID** | EPIC-01 |
| **Tên** | Project Foundation & Dev Environment |
| **Mục tiêu** | Thiết lập repo, cấu trúc thư mục, CI cơ bản, môi trường dev đồng nhất |
| **Phạm vi** | Repo setup, pre-commit hooks, pytest baseline, sample DXF test fixtures, packaging config |
| **Giá trị** | Mọi dev có thể clone và chạy ngay; test có thể chạy tự động |
| **Rủi ro chính** | PyInstaller config phức tạp (Shapely + PySide6 bundle); cần giải quyết sớm |
| **SRS liên quan** | NFR-02, NFR-04; Techstack: Python 3.12, pytest, PyInstaller |

---

### EPIC-02 — Đọc và chuẩn hóa dữ liệu DXF

| Trường | Nội dung |
|---|---|
| **Epic ID** | EPIC-02 |
| **Tên** | DXF Ingestion & Data Normalization |
| **Mục tiêu** | Đọc được toàn bộ entities liên quan từ DXF: layer tường, text phòng, block cửa |
| **Phạm vi** | Parser DXF bằng ezdxf; chuẩn hóa đơn vị (mm); trích xuất LINE/LWPOLYLINE, TEXT/MTEXT, INSERT |
| **Giá trị** | Cung cấp raw data sạch cho các module downstream |
| **Rủi ro chính** | Layer naming convention của từng khách hàng khác nhau; cần cơ chế config layer name |
| **SRS liên quan** | FR-01, FR-03; Techstack: ezdxf |

---

### EPIC-03 — Nhận diện phòng & tạo đường bao

| Trường | Nội dung |
|---|---|
| **Epic ID** | EPIC-03 |
| **Tên** | Room Recognition & Closed Boundary Generation |
| **Mục tiêu** | Tạo Polyline khép kín hợp lệ cho từng phòng; gắn tên/mã phòng |
| **Phạm vi** | AutoLISP: thuật toán XR (phòng vuông vức) + GB (phòng L-shape); BPOLY với Boundary Set lọc layer tường; Door Sealing; loại trùng lặp; gắn text phòng |
| **Giá trị** | Đây là core value của sản phẩm — không có Polyline khép kín, không có gì để tính |
| **Rủi ro chính** | Bản vẽ "bẩn" (nội thất, hatch, rác ngắn < 300mm) gây lỗi BPOLY; phòng L-shape phức tạp cần thuật toán GB; phòng nhiều ngóc ngách cần prototype trước |
| **SRS liên quan** | FR-02, FR-04, FR-05, FR-06, FR-07, BR-01, BR-07 |

> ⚠️ **Epic này là bottleneck của toàn dự án.** Cần prototype trên bản vẽ thực ngay Sprint 2.

---

### EPIC-04 — Nhận diện cửa & gán cửa-phòng

| Trường | Nội dung |
|---|---|
| **Epic ID** | EPIC-04 |
| **Tên** | Door Recognition & Room-Door Assignment |
| **Mục tiêu** | Đọc thông tin cửa từ block thuộc tính; gán cửa vào phòng hoặc cặp phòng; lưu quan hệ cửa-phòng |
| **Phạm vi** | Đọc INSERT entities có attribute (D1, D2, DW, S1, S2...); spatial lookup (block nằm trong/gần phòng nào); xử lý cửa trên ranh giới chung |
| **Giá trị** | Dữ liệu cửa chính xác là điều kiện bắt buộc để tính khối lượng tường đúng |
| **Rủi ro chính** | Block cửa không chuẩn layer/attribute name; cửa nằm chính xác trên biên (edge case geometry) |
| **SRS liên quan** | FR-08, FR-09, FR-10, FR-11, BR-02, BR-03 |

---

### EPIC-05 — Tính toán khối lượng

| Trường | Nội dung |
|---|---|
| **Epic ID** | EPIC-05 |
| **Tên** | Quantity Calculation Engine |
| **Mục tiêu** | Tính đầy đủ: diện tích, chu vi, cạnh, khối lượng sàn, tường (có trừ cửa, trừ tường chung) |
| **Phạm vi** | Shapely geometry (.area, .length, .exterior.coords); thuật toán Gross-Overlap Deduction; xử lý BR-06 (cửa ranh giới chung); chuẩn hóa đơn vị sang m² / m³ |
| **Giá trị** | Đây là lý do tồn tại của sản phẩm — output tính toán là deliverable chính |
| **Rủi ro chính** | Sai đơn vị DXF (mm vs m) nếu không normalize; thuật toán tường chung cần tolerance phù hợp |
| **SRS liên quan** | FR-12–FR-17, BR-04, BR-05, BR-06 |

---

### EPIC-06 — Xuất Excel

| Trường | Nội dung |
|---|---|
| **Epic ID** | EPIC-06 |
| **Tên** | Excel Export |
| **Mục tiêu** | Xuất báo cáo Excel đầy đủ theo 3 sheet: phòng, cửa, cạnh; định dạng dễ đọc và dùng tiếp |
| **Phạm vi** | pandas + openpyxl; multi-sheet; merge cells header; số liệu theo đúng cấu trúc Section 13 của SRS |
| **Giá trị** | Deliverable cuối cùng người dùng nhận và sử dụng |
| **Rủi ro chính** | Format Excel thay đổi theo yêu cầu khách hàng cụ thể — cần template review sớm |
| **SRS liên quan** | FR-18, FR-19, FR-20, FR-21, NFR-03 |

---

### EPIC-07 — Giao diện người dùng & vận hành

| Trường | Nội dung |
|---|---|
| **Epic ID** | EPIC-07 |
| **Tên** | UI & Operational UX |
| **Mục tiêu** | Giao diện Python desktop để nhập tham số, chạy pipeline, xem log, xuất Excel; cảnh báo lỗi |
| **Phạm vi** | PySide6: form nhập tham số (chiều cao, chiều dày, file path), progress indicator, log panel, nút xuất Excel, cảnh báo dữ liệu lỗi |
| **Giá trị** | Người dùng không cần biết Python; vận hành được qua GUI |
| **Rủi ro chính** | PySide6 bundle trong .exe làm tăng kích thước đáng kể |
| **SRS liên quan** | FR-22, FR-23, FR-24, NFR-06, NFR-07 |

---

### EPIC-08 — Kiểm thử & Đóng gói

| Trường | Nội dung |
|---|---|
| **Epic ID** | EPIC-08 |
| **Tên** | Testing & Packaging |
| **Mục tiêu** | Unit test đủ các business rule; UAT với bản vẽ thực; đóng gói .exe chạy được trên Windows sạch |
| **Phạm vi** | pytest cho EPIC-05; fixture test DXF; UAT checklist theo Section 15 SRS; PyInstaller .exe; smoke test sau packaging |
| **Giá trị** | Đảm bảo MVP không bị lỗi nghiêm trọng khi go-live |
| **Rủi ro chính** | Antivirus false positive; DLL missing khi chạy trên máy không có AutoCAD |
| **SRS liên quan** | NFR-03, NFR-04, NFR-07; SRS Section 15 |

---

## 8. Product backlog tổng

> **Quy ước độ ưu tiên:** P1 = Phải có (MVP blocker) · P2 = Nên có (MVP quality) · P3 = Tốt có (Post-MVP)

| ID | Epic | Tên hạng mục | Mô tả ngắn | Loại | Ưu tiên | Phụ thuộc | Output kỳ vọng | Acceptance note | Sprint |
|---|---|---|---|---|---|---|---|---|---|
| BL-01 | EPIC-01 | Khởi tạo repo & cấu trúc thư mục | Tạo repo Git, cấu trúc src/tests/data/lisp/packaging | DevOps | P1 | — | Repo có README, .gitignore, requirements.txt | Dev clone và chạy pytest thành công | S1 |
| BL-02 | EPIC-01 | Cấu hình pytest baseline | Setup pytest, fixture thư mục, coverage config | Dev | P1 | BL-01 | pytest chạy 0 lỗi trên test suite rỗng | CI chạy được | S1 |
| BL-03 | EPIC-01 | Prototype PyInstaller bundle | Build thử .exe với PySide6 + Shapely trên Windows | DevOps | P1 | BL-01 | .exe chạy được trên máy sạch (không có Python) | Không crash khi mở | S1 |
| BL-04 | EPIC-01 | Chuẩn bị sample DXF test fixtures | Thu thập/tạo ít nhất 3 file DXF test: phòng đơn giản, phòng L-shape, mặt bằng nhiều phòng | Data | P1 | — | 3 file DXF đại diện, có layer tường/text/block cửa rõ ràng | PM + Dev xác nhận đủ case | S1 |
| BL-05 | EPIC-02 | Parser DXF: đọc LINE/LWPOLYLINE theo layer | ezdxf đọc entities hình học từ layer tường được cấu hình | Dev | P1 | BL-04 | Trả về list segments với tọa độ đã normalize sang mm | Unit test pass với fixture | S1 |
| BL-06 | EPIC-02 | Parser DXF: đọc TEXT/MTEXT (tên, mã phòng) | Đọc tất cả text trong phạm vi bản vẽ, lưu vị trí + nội dung | Dev | P1 | BL-05 | List {text_content, position} | Unit test pass | S1 |
| BL-07 | EPIC-02 | Parser DXF: đọc INSERT block cửa + attributes | Đọc các block INSERT có attribute (D1, D2, DW...), trích xuất attribute values | Dev | P1 | BL-05 | List door objects với code/name/width/height/position | Unit test pass với fixture có block cửa | S2 |
| BL-08 | EPIC-02 | Cơ chế config layer name | Cho phép user cấu hình tên layer tường (không hard-code) | Product | P2 | BL-05 | Config file hoặc form UI nhập layer name | Layer name thay đổi không cần sửa code | S2 |
| BL-09 | EPIC-02 | Normalize đơn vị DXF | Detect và convert đơn vị (mm/m/inch) về mm thống nhất | Dev | P1 | BL-05 | Geometry output luôn tính bằng mm | Test với file DXF có $INSUNITS khác nhau | S1 |
| BL-10 | EPIC-03 | **[PROTOTYPE]** AutoLISP: thuật toán XR (phòng vuông vức) | Triển khai lệnh XR: bắn 4 tia, lọc layer tường, tìm chiều dày tường tiêu chuẩn, tạo Polyline | Dev | P1 | BL-04 | File .LSP chạy được trong AutoCAD, tạo LWPOLYLINE đỏ cho phòng vuông vức | Test trên 5 phòng thực, ≥ 4/5 thành công | S2 |
| BL-11 | EPIC-03 | **[PROTOTYPE]** AutoLISP: thuật toán GB (phòng L-shape) | Triển khai lệnh GB: quét chọn vùng, lọc rác < 300mm, ghost boundary set, chạy BPOLY | Dev | P1 | BL-10 | File .LSP chạy được, tạo Polyline cho phòng giật cấp | Test trên 3 phòng L-shape thực | S2 |
| BL-12 | EPIC-03 | AutoLISP: Door Sealing trước BPOLY | Tự động tìm block cửa trên biên tường, vẽ Line tạm đóng lỗ hở, xóa sau khi tạo Boundary | Dev | P1 | BL-11 | Phòng có cửa không bị lẹm diện tích | Test với phòng có 2–3 cửa trên tường | S3 |
| BL-13 | EPIC-03 | AutoLISP: Xuất dữ liệu Polyline ra file trung gian JSON | LISP ghi coordinates của tất cả Polyline phòng ra output.json | Dev | P1 | BL-10, BL-11 | output.json đủ tọa độ đỉnh của mỗi phòng | Python đọc được và tái tạo geometry đúng | S3 |
| BL-14 | EPIC-03 | Python: đọc Polyline từ JSON, tạo Shapely Polygon | Parse output.json từ LISP, tạo Shapely Polygon cho mỗi phòng | Dev | P1 | BL-13 | Dict {room_id: Polygon} | Polygon hợp lệ (.is_valid == True) | S3 |
| BL-15 | EPIC-03 | Python: gắn text phòng (tên/mã) vào Polygon | Với mỗi text position từ DXF, kiểm tra nằm trong Polygon nào → gắn tên/mã | Dev | P1 | BL-06, BL-14 | Room object có room_code, room_name | BR-07 pass: ưu tiên text có sẵn | S3 |
| BL-16 | EPIC-03 | Python: loại bỏ Polygon trùng lặp | Detect Polygon có overlap > ngưỡng → giữ lại một, log warning | Dev | P1 | BL-14 | Mỗi phòng chỉ có 1 Polygon | FR-06 pass | S3 |
| BL-17 | EPIC-04 | Python: spatial assignment cửa → phòng | Với mỗi block cửa (position), kiểm tra nằm trong/gần Polygon nào | Dev | P1 | BL-07, BL-14 | Mỗi cửa có related_room_a (và optional related_room_b) | FR-10, FR-11 pass | S3 |
| BL-18 | EPIC-04 | Python: phát hiện cửa trên ranh giới chung | Detect cửa nằm trên biên chung giữa 2 Polygon → gắn cả 2 phòng | Dev | P1 | BL-17 | Cửa ranh giới có related_room_a VÀ related_room_b | BR-03 pass | S4 |
| BL-19 | EPIC-04 | Python: nhập cửa từ file Excel đầu vào (fallback) | Đọc danh sách cửa từ Excel nếu block thuộc tính không đủ dữ liệu | Dev | P2 | BL-07 | Cửa từ Excel được merge vào danh sách cửa tổng | FR-03 note pass | S4 |
| BL-20 | EPIC-05 | Python: tính diện tích, chu vi từ Shapely Polygon | polygon.area, polygon.length; convert sang m² | Dev | P1 | BL-14 | Room.area (m²), Room.perimeter (m) | Sai lệch < 1% so với đo tay | S4 |
| BL-21 | EPIC-05 | Python: trích xuất và tính chiều dài từng cạnh | exterior.coords → list edge vectors → .length mỗi cạnh | Dev | P1 | BL-14 | Room.edge_list [{edge_index, length}] | FR-14 pass | S4 |
| BL-22 | EPIC-05 | Python: tính khối lượng hoàn thiện sàn | floor_finish = area × hệ số (mặc định = 1.0) | Dev | P1 | BL-20 | Room.floor_finish_quantity (m²) | BR-04 pass | S4 |
| BL-23 | EPIC-05 | Python: tính khối lượng tường (trừ cửa đơn) | wall_finish = perimeter × H − Σ(door.width × door.height) | Dev | P1 | BL-20, BL-17 | Room.wall_finish_quantity (m²) | BR-05 pass | S4 |
| BL-24 | EPIC-05 | Python: xử lý cửa trên ranh giới chung (BR-06) | Cửa chung: trừ 1 lần ở tường; trừ 2 lần bề mặt nếu cả 2 phòng trong phạm vi | Dev | P1 | BL-18, BL-23 | Kết quả tính toán đúng per BR-06 | Test case rõ ràng với 1 cửa chung 2 phòng | S4 |
| BL-25 | EPIC-05 | pytest: unit test toàn bộ business rule BR-04/05/06 | Viết test case cho từng BR, dùng fixture Polygon và Door đã biết sẵn | QA/Dev | P1 | BL-22, BL-23, BL-24 | 100% BR test pass | Không merge code tính toán nếu test fail | S4 |
| BL-26 | EPIC-06 | Thiết kế và review template Excel output | Xác định format 3 sheet (phòng / cửa / cạnh) cùng khách hàng / PM | Product/UX | P1 | — | Template Excel được PM + user xác nhận | Trước khi BL-27 bắt đầu | S3 |
| BL-27 | EPIC-06 | Python: xuất sheet "Dữ liệu theo phòng" | pandas → openpyxl, ghi đủ các cột per Section 13.1 SRS | Dev | P1 | BL-26, BL-22, BL-23 | Sheet phòng đúng cấu trúc, đủ cột | FR-19 pass | S5 |
| BL-28 | EPIC-06 | Python: xuất sheet "Dữ liệu theo cửa" | Ghi đủ các cột per Section 13.2 SRS | Dev | P1 | BL-26, BL-17 | Sheet cửa đúng cấu trúc | FR-20 pass | S5 |
| BL-29 | EPIC-06 | Python: xuất sheet "Dữ liệu theo cạnh" | Ghi đủ các cột per Section 13.3 SRS | Dev | P1 | BL-26, BL-21 | Sheet cạnh đúng cấu trúc | FR-21 pass | S5 |
| BL-30 | EPIC-06 | Format Excel: header, merge cell, số thập phân | Định dạng header in đậm, merge cells nhóm, số làm tròn 2 chữ số | Dev | P2 | BL-27, BL-28, BL-29 | File Excel "sạch" không cần chỉnh tay | UAT user xác nhận | S5 |
| BL-31 | EPIC-07 | PySide6: form nhập tham số đầu vào | Nhập: file DXF path, layer tường, chiều cao thông thủy H, chiều dày tường t | UX/Dev | P1 | BL-03 | Form hiển thị đúng, validate input | Không cho chạy nếu field bắt buộc trống | S3 |
| BL-32 | EPIC-07 | PySide6: nút chạy pipeline + progress indicator | Nút "Chạy", progress bar/log panel thể hiện các bước xử lý | UX/Dev | P1 | BL-31 | User thấy trạng thái xử lý, không bị treo màn hình | | S5 |
| BL-33 | EPIC-07 | PySide6: hiển thị cảnh báo dữ liệu không hợp lệ | Log hoặc dialog cảnh báo khi: phòng không nhận diện được, cửa thiếu data, phòng trùng | UX/Dev | P1 | BL-15, BL-16, BL-17 | Mỗi loại lỗi có message rõ ràng | FR-23 pass; không crash | S5 |
| BL-34 | EPIC-07 | PySide6: nút xuất Excel + mở file sau khi xong | Sau khi pipeline chạy xong, user click "Xuất Excel" và mở file | UX/Dev | P1 | BL-29 | Excel được tạo và mở ra | FR-18 pass | S5 |
| BL-35 | EPIC-07 | PySide6: tab/panel kiểm tra lại kết quả | Hiển thị bảng room list với diện tích, chu vi, số cửa để review nhanh | UX/Dev | P2 | BL-20, BL-17 | User xem được tổng quan số liệu trước khi xuất | FR-24 pass | S5 |
| BL-36 | EPIC-08 | UAT preparation: test cases từ SRS Section 15 | Chuyển 13 tiêu chí nghiệm thu SRS thành test script có pass/fail | QA | P1 | BL-04 | UAT checklist hoàn chỉnh | Mỗi tiêu chí có test case cụ thể | S4 |
| BL-37 | EPIC-08 | UAT thực tế với bản vẽ thực | Chạy toàn luồng với ≥ 2 file bản vẽ thực từ khách hàng | QA | P1 | BL-34, BL-36 | ≥ 90% phòng nhận diện đúng; 0 lỗi nghiêm trọng | Sign-off từ PM hoặc end user | S6 |
| BL-38 | EPIC-08 | Đóng gói .exe final + smoke test | PyInstaller build final; smoke test trên máy sạch Windows 10/11 | DevOps | P1 | BL-37 | .exe chạy được, không phụ thuộc Python | Smoke test pass trên 2 máy khác nhau | S6 |
| BL-39 | EPIC-08 | Hướng dẫn sử dụng ngắn (Quick Guide) | Tài liệu 1–2 trang: cài .exe, load .LSP, chạy lần đầu | Product | P1 | BL-38 | Quick Guide PDF hoặc Markdown | User mới chạy được sau 15 phút đọc | S6 |

---

## 9. Backlog theo sprint

> **Giả định:** Sprint 2 tuần. Team: 2 dev (Python + AutoLISP) + 1 QA/BA part-time.

---

### Sprint 1 — Foundation & DXF Parsing
**Mục tiêu:** Môi trường dev sẵn sàng; đọc được entities cơ bản từ DXF; prototype đóng gói .exe.

**Backlog:** BL-01, BL-02, BL-03, BL-04, BL-05, BL-06, BL-09

**Vì sao nhóm cùng nhau:** Không thể làm bất kỳ bước nào tiếp theo nếu thiếu: (1) môi trường dev, (2) DXF parser cơ bản, (3) test fixtures. BL-03 (PyInstaller prototype) đưa vào sớm để phát hiện vấn đề packaging trước khi có nhiều code.

**Rủi ro:** PyInstaller + Shapely + PySide6 bundle có thể gặp vấn đề DLL. Dành buffer để debug.

**Deliverable cuối sprint:**
- Repo khởi tạo xong, CI chạy được.
- Script Python đọc DXF, in ra list LINE entities và TEXT entities.
- .exe prototype mở được (dù chưa có feature).

---

### Sprint 2 — Room Recognition Prototype (CORE)
**Mục tiêu:** Có prototype AutoLISP tạo được Polyline phòng cho các trường hợp phổ biến. Đây là sprint rủi ro cao nhất — cần validate sớm.

**Backlog:** BL-07, BL-08, BL-10 *(PROTOTYPE XR)*, BL-11 *(PROTOTYPE GB)*

**Vì sao nhóm cùng nhau:** Room recognition là blocking item cho mọi tính toán. Prototype XR và GB phải chạy được trên bản vẽ thực trước khi tiếp tục.

**Rủi ro cao:**
- Thuật toán XR không tìm được chiều dày tường nếu layer naming sai → cần BL-08 config.
- GB phức tạp hơn dự kiến với mặt bằng nhiều rác → cần buffer.
- Cần bản vẽ thực từ khách hàng để test; nếu chưa có phải dùng file tự tạo.

**Deliverable cuối sprint:**
- Lệnh XR chạy được trong AutoCAD, tạo Polyline đỏ cho phòng vuông vức.
- Lệnh GB chạy được cho phòng L-shape cơ bản.
- Demo review với PM/BA.

---

### Sprint 3 — Room Pipeline (LISP → Python) + UI Form
**Mục tiêu:** Hoàn thiện luồng LISP → JSON → Python Polygon; gán text phòng; UI form cơ bản.

**Backlog:** BL-12 *(Door Sealing)*, BL-13 *(LISP → JSON)*, BL-14 *(JSON → Shapely)*, BL-15 *(gắn text phòng)*, BL-16 *(loại trùng lặp)*, BL-26 *(review template Excel)*, BL-31 *(UI form)*

**Vì sao nhóm cùng nhau:** Cần hoàn thiện toàn bộ room recognition pipeline trước khi làm door assignment và calculation. UI form và template Excel review có thể chạy song song.

**Rủi ro:** Geometry từ LISP có thể không clean (tọa độ float precision) → cần tolerance handling trong Shapely.

**Deliverable cuối sprint:**
- Python nhận JSON từ LISP, tạo Shapely Polygon hợp lệ cho từng phòng.
- Room có tên và mã phòng gắn đúng.
- Template Excel được xác nhận.
- UI form cơ bản hiển thị và validate input.

---

### Sprint 4 — Door Assignment + Calculation Engine + UAT Prep
**Mục tiêu:** Hoàn thiện gán cửa, toàn bộ tính toán khối lượng, unit test business rule.

**Backlog:** BL-17 *(door spatial)*, BL-18 *(cửa ranh giới)*, BL-19 *(Excel input)*, BL-20, BL-21, BL-22, BL-23, BL-24, BL-25 *(unit test BR)*, BL-36 *(UAT prep)*

**Vì sao nhóm cùng nhau:** Calculation engine cần door assignment xong mới có thể tính đúng. Unit test BR viết song song với implementation — không merge code tính toán nếu test chưa pass.

**Rủi ro:** BR-06 (cửa ranh giới chung) là edge case phức tạp nhất — cần test case rõ ràng được viết trước khi code.

**Deliverable cuối sprint:**
- Toàn bộ tính toán chạy đúng với test fixture.
- 100% unit test BR pass.
- UAT checklist sẵn sàng.

---

### Sprint 5 — Export Excel + UI Hoàn thiện + Integration
**Mục tiêu:** Luồng end-to-end hoàn chỉnh: từ DXF đến Excel, có UI đầy đủ.

**Backlog:** BL-27, BL-28, BL-29, BL-30, BL-32, BL-33, BL-34, BL-35

**Vì sao nhóm cùng nhau:** Excel export và UI cùng phục vụ deliverable cuối. Cần integration test end-to-end với pipeline đầy đủ.

**Rủi ro:** Integration có thể phát lộ edge case data mà unit test không cover → buffer 2–3 ngày cho bug fix.

**Deliverable cuối sprint:**
- Chạy toàn luồng: load DXF → click phòng trong AutoCAD → Python xử lý → xuất Excel → mở file.
- UI hiển thị cảnh báo đúng khi có phòng lỗi.

---

### Sprint 6 — UAT + Packaging + Release
**Mục tiêu:** Nghiệm thu với bản vẽ thực, đóng gói .exe final, viết hướng dẫn.

**Backlog:** BL-37 *(UAT thực)*, BL-38 *(đóng gói)*, BL-39 *(Quick Guide)*

**Vì sao nhóm cùng nhau:** Sprint cuối tập trung vào quality assurance và delivery — không thêm feature mới.

**Rủi ro:** Bản vẽ thực phát hiện case chưa được handle → triage nghiêm túc: fix nếu MVP blocker, backlog nếu không.

**Deliverable cuối sprint:**
- .exe chạy được trên máy sạch, smoke test pass.
- UAT sign-off từ PM.
- Quick Guide hoàn chỉnh.
- **MVP READY TO SHIP.**

---

## 10. MVP acceptance

### Điều kiện coi là xong MVP (phải đạt tất cả)
- [ ] Nhập được file DXF hợp lệ qua UI.
- [ ] Nhận diện được ≥ 90% phòng trong test case UAT.
- [ ] Gắn đúng tên và mã phòng từ text có sẵn.
- [ ] Nhận diện cửa và gán vào phòng / cặp phòng đúng ≥ 95% trường hợp.
- [ ] Tính đúng diện tích (sai lệch < 1%), chu vi, chiều dài cạnh.
- [ ] Tính đúng khối lượng sàn và tường (có trừ cửa).
- [ ] Áp dụng đúng BR-06 (cửa ranh giới chung) trong test case có cửa chung.
- [ ] Xuất Excel đủ 3 sheet, dữ liệu khớp với số liệu tính toán.
- [ ] Cảnh báo hiện ra khi phòng không nhận diện được hoặc cửa thiếu data.
- [ ] Xử lý toàn bộ mặt bằng trong 1 lần chạy (không bị crash).
- [ ] .exe chạy được trên Windows 10/11 không cài Python.
- [ ] 100% unit test BR-04, BR-05, BR-06 pass.
- [ ] UAT sign-off từ PM hoặc end user đại diện.

### Điều kiện chưa nên go-live
- Phòng L-shape phức tạp bị nhận diện sai > 20% trường hợp trong test thực.
- Có lỗi crash khi xử lý file bản vẽ thực (bất kỳ lỗi unhandled exception nào).
- Số liệu diện tích sai > 1% mà không có cảnh báo.
- .exe bị antivirus block trên máy test của khách hàng (chưa có workaround).
- Template Excel chưa được PM / end user xác nhận format.

---

## 11. Rủi ro delivery

### Rủi ro nghiệp vụ
| Rủi ro | Mức độ | Biện pháp |
|---|---|---|
| Chiều cao thông thủy và chiều dày tường thay đổi theo từng phòng (không đồng nhất) | Trung bình | MVP nhập 1 giá trị chung; Phase 2 hỗ trợ per-phòng |
| Rule nghiệp vụ BR-06 bị hiểu sai khi implement | Cao | Viết test case BR-06 trước khi code; BA review |
| Khách hàng muốn thêm cột / thay đổi format Excel sau khi template đã xác nhận | Trung bình | Confirm template sớm (Sprint 3); đóng băng format trước Sprint 5 |

### Rủi ro dữ liệu DXF
| Rủi ro | Mức độ | Biện pháp |
|---|---|---|
| Layer naming không nhất quán giữa các file / dự án khác nhau | Cao | BL-08: cơ chế config layer name; không hard-code |
| File DXF export bị mất entity so với DWG gốc | Trung bình | Test với nhiều phiên bản AutoCAD; dùng DXF 2013 làm chuẩn |
| Đơn vị DXF không xác định ($INSUNITS = 0) | Trung bình | BL-09: detect và hỏi user nếu không rõ đơn vị |

### Rủi ro nhận diện phòng / cửa
| Rủi ro | Mức độ | Biện pháp |
|---|---|---|
| Bản vẽ "bẩn": hatch, nội thất, rác ngắn gây lỗi BPOLY | Cao | Thuật toán GB lọc object < 300mm; Door Sealing (BL-12) |
| Phòng không vuông vức phức tạp (nhiều ngóc ngách) | Cao | Thuật toán GB xử lý được L-shape; case phức tạp hơn là manual input |
| Block cửa không chuẩn attribute name | Trung bình | Config mapping attribute name; fallback nhập từ Excel |
| Cửa nằm đúng trên biên hình học (edge case) | Trung bình | Dùng buffer distance khi spatial lookup; test case riêng |

### Rủi ro độ chính xác số liệu
| Rủi ro | Mức độ | Biện pháp |
|---|---|---|
| Float precision từ LISP coordinates gây Polygon không hợp lệ | Trung bình | Shapely simplify + tolerance; validate .is_valid trước tính toán |
| Tường chung bị tính sai nếu 2 phòng không chia sẻ đúng segment | Trung bình | Thuật toán Gross-Overlap với cross product + fuzz 5mm |

### Rủi ro packaging / deployment
| Rủi ro | Mức độ | Biện pháp |
|---|---|---|
| PyInstaller bundle Shapely + PySide6 có DLL conflict | Cao | BL-03 prototype sớm Sprint 1; test trên máy sạch |
| Antivirus false positive với .exe | Trung bình | Ghi nhận; hướng dẫn whitelist; Phase 2 xem xét code signing |
| .LSP file cần được load thủ công vào AutoCAD mỗi lần | Thấp | Hướng dẫn dùng APPLOAD / startup suite trong Quick Guide |

---

## 12. Phụ lục traceability

| FR / BR / NFR | Epic | Backlog Item(s) | Sprint |
|---|---|---|---|
| FR-01 (Nhập DXF) | EPIC-02 | BL-05 | S1 |
| FR-02 (Chọn phạm vi) | EPIC-03 | BL-10, BL-11 (click bên trong phòng) | S2 |
| FR-03 (Đọc text/cửa) | EPIC-02 | BL-06, BL-07, BL-19 | S1–S4 |
| FR-04 (Nhận diện phòng) | EPIC-03 | BL-10 (XR), BL-11 (GB) | S2 |
| FR-05 (Đường bao khép kín) | EPIC-03 | BL-12, BL-13, BL-14 | S2–S3 |
| FR-06 (Loại trùng lặp) | EPIC-03 | BL-16 | S3 |
| FR-07 (Gắn tên/mã phòng) | EPIC-03 | BL-15 | S3 |
| FR-08 (Nhận diện cửa) | EPIC-04 | BL-07 | S2 |
| FR-09 (Đọc thuộc tính cửa) | EPIC-04 | BL-07 | S2 |
| FR-10 (Gán cửa vào phòng) | EPIC-04 | BL-17 | S4 |
| FR-11 (Quan hệ cửa-phòng) | EPIC-04 | BL-17, BL-18 | S4 |
| FR-12 (Diện tích) | EPIC-05 | BL-20 | S4 |
| FR-13 (Chu vi) | EPIC-05 | BL-20 | S4 |
| FR-14 (Chiều dài cạnh) | EPIC-05 | BL-21 | S4 |
| FR-15 (Khối lượng sàn) | EPIC-05 | BL-22 | S4 |
| FR-16 (Khối lượng tường) | EPIC-05 | BL-23 | S4 |
| FR-17 (Diện tích cửa trong tính toán) | EPIC-05 | BL-23, BL-24 | S4 |
| FR-18 (Xuất báo cáo tổng hợp) | EPIC-06 | BL-27, BL-28, BL-29 | S5 |
| FR-19 (Chi tiết theo phòng) | EPIC-06 | BL-27 | S5 |
| FR-20 (Chi tiết theo cửa) | EPIC-06 | BL-28 | S5 |
| FR-21 (Cấu trúc kiểm tra được) | EPIC-06 | BL-30 | S5 |
| FR-22 (Xử lý 1 lần chạy) | EPIC-07 | BL-32 | S5 |
| FR-23 (Cảnh báo lỗi) | EPIC-07 | BL-33 | S5 |
| FR-24 (Kiểm tra lại kết quả) | EPIC-07 | BL-35 | S5 |
| BR-01 (Phòng hợp lệ mới tính) | EPIC-03 | BL-14 + validation | S3 |
| BR-02 (Cửa có data tối thiểu) | EPIC-04 | BL-07, BL-17 | S2, S4 |
| BR-03 (Cửa 1 hoặc 2 phòng) | EPIC-04 | BL-18 | S4 |
| BR-04 (Sàn theo diện tích) | EPIC-05 | BL-22, BL-25 | S4 |
| BR-05 (Tường theo chu vi × H − cửa) | EPIC-05 | BL-23, BL-25 | S4 |
| BR-06 (Cửa ranh giới chung) | EPIC-05 | BL-24, BL-25 | S4 |
| BR-07 (Ưu tiên text có sẵn) | EPIC-03 | BL-15 | S3 |
| NFR-03 (Truy vết được) | EPIC-06, EPIC-07 | BL-30, BL-35 | S5 |
| NFR-04 (Nhất quán) | EPIC-05, EPIC-08 | BL-25, BL-37 | S4, S6 |
| NFR-06 (Xử lý 1 lần) | EPIC-07 | BL-32 | S5 |
| NFR-07 (Chịu lỗi có kiểm soát) | EPIC-07 | BL-33 | S5 |

---

*Tài liệu này cần được review bởi PM + Tech Lead trước Sprint 1 kickoff. Bất kỳ thay đổi scope nào phải được cập nhật lại traceability table.*
