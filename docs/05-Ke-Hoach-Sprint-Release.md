# 05 — Kế Hoạch Sprint & Release
## RoomQS — Công cụ tự động nhận diện phòng và bóc khối lượng từ bản vẽ mặt bằng

**Phiên bản tài liệu:** 1.0  
**Nguồn gốc:** Dẫn xuất từ SRS v1.0 + PRD/Backlog v1.0 + Techstack v1.0  
**Đối tượng đọc:** PM · Tech Lead · QA Lead  
**Trạng thái:** Draft – chờ review trước Sprint 1 Kickoff

---

## 1. Mục tiêu kế hoạch

### 1.1. Mục đích tài liệu

Tài liệu này là **bộ khung điều hành delivery** từ kickoff đến go-live cho MVP RoomQS. Nó không phải Gantt chart tĩnh — đây là tài liệu sống: PM và Tech Lead dùng để ra quyết định ưu tiên, QA Lead dùng để chuẩn bị test cycle, cả team dùng để biết mình đang ở đâu trong vòng đời sản phẩm.

Ba câu hỏi tài liệu này phải trả lời được tại mọi thời điểm:
1. Chúng ta đang ở sprint nào, còn bao lâu đến go-live?
2. Rủi ro nào đang sáng đèn đỏ cần xử lý ngay?
3. Gate nào chưa pass — và điều kiện để pass là gì?

### 1.2. Phạm vi áp dụng

- Bao phủ toàn bộ MVP RoomQS (6 sprint, ~12 tuần với team 2 Dev + 1 QA/BA part-time).
- Từ Sprint 0 (kickoff/preparation) đến go-live nội bộ.
- Không bao gồm Phase 2 (zero-click detection, thêm hạng mục, ERP integration).

### 1.3. Giả định planning

| # | Giả định | Rủi ro nếu sai |
|---|---|---|
| A1 | Sprint = 2 tuần | Nếu team part-time nhiều hơn → cần extend sprint length hoặc giảm scope |
| A2 | Team: 2 Dev (1 Python chính, 1 AutoLISP/Python), 1 QA/BA part-time | Thiếu người → tắc nghẽn ở Sprint 2 (LISP prototype) |
| A3 | Sample DXF thực từ khách hàng có được trong tuần 1–2 | Nếu chậm → dùng file synthetic nhưng rủi ro UAT cao |
| A4 | AutoCAD 2019+ khả dụng trên máy dev để test LISP | Không có → không test được thuật toán XR/GB |
| A5 | Template Excel output được PM/BA xác nhận xong trước Sprint 4 | Trễ → block Sprint 5 export |
| A6 | Chiều cao thông thủy và chiều dày tường nhập bởi user (không tự động đọc) | Nếu khách hàng yêu cầu tự động → scope change |
| A7 | Không có yêu cầu mới nào được thêm vào sau Sprint 3 (scope freeze) | Thêm scope → cần re-estimate toàn bộ |

---

## 2. Delivery approach

### 2.1. Phương pháp triển khai theo sprint

RoomQS dùng **iterative delivery với risk-first ordering**: sprint đầu tiên không chạy tính năng dễ nhất mà chạy task rủi ro cao nhất. Lý do: nếu sprint 5-6 mới phát hiện room recognition không ổn định trên bản vẽ thực, toàn bộ product bị delay — không còn thời gian xử lý.

Mỗi sprint kết thúc bằng một **working artifact** có thể demo hoặc test được, không phải chỉ code trong repo. Sprint review là cơ hội để phát hiện misalignment với người dùng thực trước khi tốn effort tiếp theo.

### 2.2. Vì sao technical spike phải đi trước

**Room recognition (EPIC-03) là bottleneck duy nhất của cả sản phẩm.** Không có Polyline phòng khép kín → không có gì để tính toán. Thuật toán XR và GB viết trên AutoLISP không thể test bằng unit test thuần Python — chúng phải chạy trên AutoCAD thực với bản vẽ thực.

Nếu không spike sớm, có hai kịch bản xấu:
- **Kịch bản 1:** Phát hiện thuật toán không ổn định ở Sprint 4–5 → phải rewrite LISP trong khi calculation engine đã build xong → delay toàn bộ.
- **Kịch bản 2:** Không có đủ sample DXF thực → build xong nhưng UAT với bản vẽ thực phát sinh hàng loạt edge case chưa handle → go-live bị block.

Spike Sprint 2 phải ra kết luận cụ thể: **"Thuật toán XR/GB chạy được trên bản vẽ thực — tiếp tục"** hoặc **"Cần điều chỉnh thuật toán — re-estimate Sprint 3"**. Không có trạng thái "có vẻ ổn" — phải có số liệu: X/Y phòng test pass.

### 2.3. Chiến lược phân giai đoạn

```
GIAI ĐOẠN 1 — DISCOVERY & FOUNDATION (Sprint 0–1)
├── Mục tiêu: Môi trường dev sẵn sàng, DXF parser cơ bản, PyInstaller prototype, sample data
├── Kết quả chấp nhận: Dev clone repo → chạy pytest → build .exe prototype thành công
└── Risk focus: Packaging stack (Shapely + PySide6) có DLL conflict không?

GIAI ĐOẠN 2 — PROTOTYPE & VALIDATE (Sprint 2)
├── Mục tiêu: Validate room recognition trên bản vẽ thực — đây là điểm không thể quay đầu
├── Kết quả chấp nhận: XR pass ≥ 4/5 phòng vuông; GB pass ≥ 2/3 phòng L-shape trên file thực
└── Risk focus: BPOLY bị "nhiễu" bởi nội thất/hatch; layer naming không khớp

GIAI ĐOẠN 3 — MVP BUILD (Sprint 3–4)
├── Mục tiêu: Hoàn thiện pipeline LISP→JSON→Python→Calculation; door assignment; unit test BR
├── Kết quả chấp nhận: 100% unit test BR pass; pipeline chạy end-to-end với fixture
└── Risk focus: BR-06 (cửa ranh giới chung) là edge case phức tạp nhất

GIAI ĐOẠN 4 — INTEGRATION & HARDENING (Sprint 5)
├── Mục tiêu: Export Excel hoàn chỉnh; UI đầy đủ; integration test end-to-end
├── Kết quả chấp nhận: Chạy toàn luồng DXF → click → Excel thành công
└── Risk focus: Integration phát lộ edge case data mà unit test không cover

GIAI ĐOẠN 5 — UAT & RELEASE (Sprint 6)
├── Mục tiêu: UAT với bản vẽ thực; .exe final; Quick Guide; PM sign-off
├── Kết quả chấp nhận: Tất cả MVP acceptance criteria pass; UAT sign-off
└── Risk focus: Bản vẽ thực phát sinh case mới; antivirus block .exe
```

---

## 3. Sprint plan tổng thể

> **Quy ước:** Sprint = 2 tuần. Team: Dev-A (Python chính) + Dev-B (AutoLISP/Python) + QA (part-time). Ngày bắt đầu Sprint 1 = Tuần 1 kể từ ngày kickoff.

---

### Sprint 0 — Kickoff & Preparation *(1 tuần, trước Sprint 1)*

**Mục tiêu:** Không một dòng code nào được viết khi chưa có sample data và chưa align về scope. Sprint 0 là điều kiện tiên quyết để Sprint 1 chạy được ngay từ ngày đầu.

**Hạng mục chính:**
- PM thu thập ít nhất 2 file bản vẽ DXF thực từ khách hàng (đa dạng: phòng vuông + L-shape)
- BA/PM xác nhận template Excel output (3 sheet, cột tối thiểu) với end user
- Tech Lead review và chốt cấu trúc repo, branching strategy, CI/CD pipeline cơ bản
- Cả team đọc SRS + PRD, align về scope MVP và out-of-scope
- Dev-B setup AutoCAD 2019+ trên máy dev, verify LISP load được

**Deliverables:**
- [ ] ≥ 2 file DXF thực được xác nhận (tên file, layer convention ghi chú lại)
- [ ] Template Excel draft được PM xác nhận (có thể còn sửa nhỏ sau)
- [ ] Repo template tạo xong (cấu trúc folder, README, .gitignore)
- [ ] Branching convention được team agree

**Entry criteria:** PM đã đọc PRD v1.0, kickoff meeting đã diễn ra  
**Exit criteria:** Sample DXF có, template Excel draft confirmed, repo khởi tạo xong

**Rủi ro chính:** Không lấy được file DXF thực từ khách hàng → Sprint 2 sẽ test trên file synthetic, tăng rủi ro UAT  
**Dependency:** Khách hàng / end user cung cấp bản vẽ mẫu

---

### Sprint 1 — Foundation & DXF Parsing *(Tuần 1–2)*

**Mục tiêu:** Môi trường dev hoàn chỉnh; đọc được geometry từ DXF; prototype packaging .exe thành công. Mọi sprint sau đều phụ thuộc vào nền tảng này.

**Hạng mục chính:**

| Backlog | Tên | Owner | Effort (ngày) |
|---|---|---|---|
| BL-01 | Khởi tạo repo, cấu trúc thư mục | Dev-A | 1 |
| BL-02 | Cấu hình pytest baseline + coverage | Dev-A | 1 |
| BL-03 | **Prototype PyInstaller** (Shapely + PySide6) | Dev-A | 2–3 |
| BL-04 | Chuẩn bị sample DXF test fixtures (≥ 3 file) | QA/BA | 2 |
| BL-05 | Parser DXF: LINE/LWPOLYLINE theo layer | Dev-A | 2 |
| BL-06 | Parser DXF: TEXT/MTEXT (tên, mã phòng) | Dev-A | 1 |
| BL-09 | Normalize đơn vị DXF ($INSUNITS) | Dev-A | 1 |

**Logic sắp xếp:** BL-03 (PyInstaller prototype) phải làm sớm nhất sprint — nếu có DLL conflict Shapely+PySide6, cần biết ngay để không bị tắc nghẽn ở cuối dự án. BL-05/06 làm song song với BL-03 vì không phụ thuộc nhau.

**Deliverables:**
- Repo có README, pre-commit hooks, pytest chạy CI pass
- Script Python đọc DXF in ra list entity (LINE, TEXT, INSERT)
- .exe prototype mở được UI empty (dù chưa có feature) trên máy sạch không có Python
- Unit test BL-05/06 pass với fixture

**Entry criteria:** Repo đã tạo (Sprint 0), sample DXF có ít nhất 1 file  
**Exit criteria:**
- [ ] CI pipeline chạy pytest pass (0 lỗi)
- [ ] .exe prototype mở được trên Windows 10/11 không cài Python — **hard gate**
- [ ] Parser DXF đọc được LINE, TEXT, INSERT từ file sample, unit test pass
- [ ] Đơn vị tọa độ normalize sang mm với ít nhất 2 loại $INSUNITS

**Dependency:** BL-04 cần sample DXF; nếu chưa có → dùng file synthetic tạm thời  
**Rủi ro chính:** PyInstaller + Shapely + PySide6 DLL conflict trên Windows  
**Mitigation:** Dành 3 ngày buffer cho BL-03; nếu fail → thử onedir mode, kiểm tra Shapely binary wheels

---

### Sprint 2 — Room Recognition Prototype *(Tuần 3–4)* ⚠️ SPRINT RỦI RO CAO NHẤT

**Mục tiêu:** Validate thuật toán nhận diện phòng trên bản vẽ thực. Đây là **go/no-go decision point** của toàn dự án. Nếu thuật toán không đạt ngưỡng, phải re-estimate trước khi tiếp tục.

**Hạng mục chính:**

| Backlog | Tên | Owner | Effort (ngày) |
|---|---|---|---|
| BL-07 | Parser DXF: INSERT block cửa + attributes | Dev-A | 1.5 |
| BL-08 | Cơ chế config layer name (không hard-code) | Dev-B | 1 |
| BL-10 | **[PROTOTYPE]** AutoLISP thuật toán XR | Dev-B | 3–4 |
| BL-11 | **[PROTOTYPE]** AutoLISP thuật toán GB | Dev-B | 3–4 |

**Logic sắp xếp:** Toàn bộ sprint dành cho EPIC-03 prototype. Không có gì quan trọng hơn việc biết room recognition có hoạt động thực tế không. Dev-A làm BL-07/08 để không block sprint sau; Dev-B tập trung 100% vào XR + GB LISP.

**Acceptance ngưỡng prototype (phải đạt trước khi sprint được đóng):**

| Test case | Loại | Pass threshold |
|---|---|---|
| Phòng hình chữ nhật 5 case từ DXF thực | XR algorithm | ≥ 4/5 tạo Polyline đúng |
| Phòng L-shape 3 case từ DXF thực | GB algorithm | ≥ 2/3 tạo Polyline đúng |
| Phòng có block cửa (không bị lẹm) | XR + Boundary Set | ≥ 2/2 không lẹm diện tích |

**Deliverables:**
- File .LSP (lệnh XR) chạy được trong AutoCAD 2019+, tạo LWPOLYLINE đỏ
- File .LSP (lệnh GB) chạy được cho phòng L-shape cơ bản
- Demo live cho PM/BA: click vào phòng → Polyline xuất hiện
- Báo cáo kết quả prototype: X/Y case pass, các case fail có ghi chú nguyên nhân

**Entry criteria:** Sprint 1 exit criteria pass; AutoCAD 2019+ trên máy Dev-B; sample DXF thực  
**Exit criteria:**
- [ ] XR pass ≥ 4/5 phòng vuông trên file thực — **hard gate**
- [ ] GB pass ≥ 2/3 phòng L-shape trên file thực — **hard gate**
- [ ] PM/BA đã xem demo và confirmed "tiếp tục Sprint 3"
- [ ] Báo cáo prototype ghi rõ case nào fail và tại sao

**Dependency:** Sample DXF thực (phòng vuông + L-shape); AutoCAD 2019+  
**Rủi ro chính:**
- BPOLY bị nhiễu bởi nội thất, hatch, rác ngắn
- Layer tường không đúng tên cấu hình
- Phòng L-shape phức tạp hơn dự kiến

**Nếu prototype fail:** PM triệu tập session khẩn — quyết định: (1) điều chỉnh thuật toán và extend thêm 1 sprint, hoặc (2) thu hẹp scope MVP xuống chỉ phòng vuông vức. **Không tiến sang Sprint 3 khi prototype chưa đạt ngưỡng.**

---

### Sprint 3 — Room Pipeline: LISP → Python + UI Form *(Tuần 5–6)*

**Mục tiêu:** Hoàn thiện luồng dữ liệu từ AutoLISP đến Shapely Polygon trong Python; gắn tên/mã phòng; loại trùng lặp; template Excel được xác nhận; UI form cơ bản.

**Hạng mục chính:**

| Backlog | Tên | Owner | Effort (ngày) |
|---|---|---|---|
| BL-12 | Door Sealing trước BPOLY | Dev-B | 2 |
| BL-13 | LISP → JSON: xuất tọa độ Polyline | Dev-B | 1.5 |
| BL-14 | Python: JSON → Shapely Polygon | Dev-A | 1.5 |
| BL-15 | Python: gắn text phòng vào Polygon | Dev-A | 1.5 |
| BL-16 | Python: loại bỏ Polygon trùng lặp | Dev-A | 1 |
| BL-17 | Python: spatial assignment cửa → phòng | Dev-A | 2 |
| BL-26 | Review và xác nhận template Excel | PM/QA | 1 |
| BL-31 | PySide6: UI form nhập tham số | Dev-A | 2 |

**Logic sắp xếp:** Sprint này là "integration layer" — nối LISP với Python. BL-13/14 phải đi theo cặp. BL-17 được kéo sớm vào đây (thay vì Sprint 4) vì spatial lookup cần Polygon có sẵn và đây là task không quá phức tạp. BL-26 (template Excel confirm) là **deadline cứng** — nếu trễ sang Sprint 4 sẽ block BL-27.

**Deliverables:**
- LISP viết ra `output.json` với tọa độ đỉnh mỗi phòng
- Python parse `output.json`, tạo Shapely Polygon hợp lệ cho từng phòng
- Room object có `room_name`, `room_code` gắn đúng từ text DXF
- Cửa có `related_room_a` từ spatial lookup cơ bản
- Template Excel được PM và ít nhất 1 end user xác nhận — **format đóng băng sau sprint này**
- UI form hiển thị, validate field bắt buộc (file DXF, layer, H, t)

**Entry criteria:** Sprint 2 exit criteria pass; prototype XR/GB đã validated  
**Exit criteria:**
- [ ] Polygon hợp lệ (`.is_valid == True`) cho ≥ 90% phòng trong test fixture
- [ ] `room_name` và `room_code` gắn đúng trong ≥ 95% trường hợp (text nằm trong vùng phòng)
- [ ] Cửa gán được vào phòng từ spatial lookup (không yêu cầu 100% — chỉ cần pipeline chạy)
- [ ] Template Excel được ký xác nhận (email hoặc comment trong issue tracker) — **hard gate**
- [ ] UI form validate: không cho chạy khi field bắt buộc trống

**Dependency:** Sprint 2 done; template Excel cần end user confirm  
**Rủi ro chính:** Float precision từ LISP tọa độ gây Polygon invalid; text phòng đặt sai vị trí

---

### Sprint 4 — Door Assignment + Calculation Engine *(Tuần 7–8)*

**Mục tiêu:** Hoàn thiện gán cửa (bao gồm cửa ranh giới chung BR-06); toàn bộ tính toán khối lượng; 100% unit test business rule pass.

**Hạng mục chính:**

| Backlog | Tên | Owner | Effort (ngày) |
|---|---|---|---|
| BL-18 | Python: phát hiện cửa trên ranh giới chung | Dev-A | 2 |
| BL-19 | Python: nhập cửa từ Excel (fallback) | Dev-A | 1.5 |
| BL-20 | Python: tính diện tích, chu vi (Shapely) | Dev-A | 1 |
| BL-21 | Python: chiều dài từng cạnh | Dev-A | 1 |
| BL-22 | Python: tính khối lượng sàn | Dev-A | 0.5 |
| BL-23 | Python: tính khối lượng tường (trừ cửa đơn) | Dev-A | 1.5 |
| BL-24 | Python: xử lý cửa ranh giới chung (BR-06) | Dev-A | 2 |
| BL-25 | **pytest: unit test BR-04/05/06** | QA/Dev | 2 |
| BL-36 | UAT preparation: test cases từ SRS Section 15 | QA | 2 |

**Logic sắp xếp:** BL-25 (unit test) phải viết **song song** với BL-22/23/24, không phải sau khi code xong. Rule: **không merge code tính toán nếu test chưa pass.** BL-36 (UAT prep) chạy song song — QA có thể chuẩn bị checklist độc lập với dev.

**Lưu ý đặc biệt BR-06:** Trước khi code BL-24, BA/PM phải viết ra test case cụ thể với số liệu:  
- Phòng A: perimeter=18m, H=2.8m, cửa D2 (0.9×2.1m) trên tường chung với phòng B  
- Kỳ vọng: Phòng A `wall_finish = 18×2.8 - 1.89 = 48.51 m²`, Phòng B tương tự trừ 1.89m²  
Dev code để test pass, không code để tính đúng rồi mới viết test.

**Deliverables:**
- Toàn bộ tính toán (diện tích, chu vi, cạnh, sàn, tường) chạy đúng với golden dataset
- Cửa ranh giới chung được detect và BR-06 áp dụng đúng
- 100% pytest BR-04/05/06 pass
- UAT checklist 13 tiêu chí từ SRS Section 15 sẵn sàng

**Entry criteria:** Sprint 3 exit criteria pass; template Excel đã xác nhận  
**Exit criteria:**
- [ ] 100% unit test BR-04, BR-05, BR-06 pass — **hard gate, không thể bỏ qua**
- [ ] Diện tích phòng sai lệch < 1% so với golden dataset
- [ ] BR-06 test case có số liệu cụ thể pass (phải có ít nhất 2 test case cửa chung)
- [ ] UAT checklist đầy đủ 13 tiêu chí, có cột pass/fail sẵn sàng

**Dependency:** Polygon hợp lệ từ Sprint 3; spatial assignment cửa từ BL-17  
**Rủi ro chính:** BR-06 bị hiểu sai (trừ chia đôi thay vì trừ từng phòng) — viết test trước để phòng tránh

---

### Sprint 5 — Export Excel + UI Hoàn thiện + Integration *(Tuần 9–10)*

**Mục tiêu:** Luồng end-to-end hoàn chỉnh từ DXF đến Excel. UI đầy đủ tính năng. Integration test phát hiện edge case còn sót.

**Hạng mục chính:**

| Backlog | Tên | Owner | Effort (ngày) |
|---|---|---|---|
| BL-27 | Excel: sheet "Dữ liệu theo phòng" | Dev-A | 1.5 |
| BL-28 | Excel: sheet "Dữ liệu theo cửa" | Dev-A | 1 |
| BL-29 | Excel: sheet "Dữ liệu theo cạnh" | Dev-A | 1 |
| BL-30 | Format Excel: header, merge cell, số thập phân | Dev-A | 1 |
| BL-32 | UI: nút chạy pipeline + progress bar | Dev-A/B | 1 |
| BL-33 | UI: hiển thị cảnh báo dữ liệu không hợp lệ | Dev-A | 1.5 |
| BL-34 | UI: nút xuất Excel + mở file | Dev-A | 0.5 |
| BL-35 | UI: panel kiểm tra lại kết quả | Dev-A | 1.5 |
| — | Integration test end-to-end | QA | 3 |

**Logic sắp xếp:** BL-27/28/29/30 làm trước và song song; UI pieces BL-32/33/34/35 có thể parallelize với Dev-B nếu rảnh. **Dành ít nhất 3 ngày cuối sprint cho integration test** — đây là lần đầu tiên toàn bộ pipeline chạy thực sự end-to-end và sẽ phát sinh bug.

**Deliverables:**
- File Excel xuất được với đủ 3 sheet, format đúng template đã confirm
- Chạy toàn luồng: load DXF → click phòng trong AutoCAD → Python xử lý → Excel xuất → mở file
- UI không bị freeze khi chạy pipeline; progress indicator hiển thị đúng
- Cảnh báo hiện ra khi phòng không nhận diện được, cửa thiếu data

**Entry criteria:** Sprint 4 exit criteria pass; template Excel đã xác nhận (Sprint 3)  
**Exit criteria:**
- [ ] End-to-end test chạy thành công với ít nhất 1 file DXF đầy đủ (≥ 5 phòng, ≥ 3 cửa)
- [ ] File Excel đầu ra mở được bằng Excel, không có warning corrupt
- [ ] Tất cả cảnh báo (phòng lỗi, cửa invalid, trùng lặp) hiển thị đúng trên UI
- [ ] UI responsive: pipeline chạy 30 giây không freeze, progress bar cập nhật
- [ ] Tổng `area` trong sheet phòng khớp với tổng trong cell tổng cộng

**Dependency:** Toàn bộ module upstream (Sprint 1–4) done  
**Rủi ro chính:** Integration phát lộ data edge case (float precision, text ngoài polygon, cửa unassigned) → buffer 2–3 ngày bug fix trong sprint

---

### Sprint 6 — UAT + Packaging + Release *(Tuần 11–12)*

**Mục tiêu:** Nghiệm thu với bản vẽ thực; đóng gói .exe final; viết Quick Guide; PM sign-off. **Không thêm feature mới trong sprint này.**

**Hạng mục chính:**

| Backlog | Tên | Owner | Effort (ngày) |
|---|---|---|---|
| BL-37 | UAT thực tế với ≥ 2 file bản vẽ thực | QA + PM | 4 |
| — | Bug fix P0/P1 từ UAT | Dev-A/B | 3 (buffer) |
| BL-38 | Đóng gói .exe final + smoke test 2 máy | Dev-A | 2 |
| BL-39 | Quick Guide (PDF/Markdown, ≤ 2 trang) | PM/BA | 2 |
| — | Release checklist review | PM + Tech Lead | 0.5 |

**Logic sắp xếp:** UAT trước tiên — kết quả UAT quyết định có bug fix gì không. Sau khi bug critical được fix, mới build .exe final. Quick Guide viết song song với bug fix.

**Triage rule cho bug UAT:**
- **P0 (Blocker):** Crash, xuất sai không cảnh báo → phải fix trong sprint này trước khi go-live
- **P1 (MVP):** Tính năng Must có kết quả sai → fix nếu còn thời gian, nếu không → delay go-live
- **P2+ (Backlog):** UI không đẹp, edge case hiếm gặp → ghi backlog, không block go-live

**Deliverables:**
- UAT report: kết quả từng tiêu chí SRS Section 15, số phòng nhận diện đúng / tổng
- .exe chạy được trên 2 máy Windows sạch (không cài Python, không cài Shapely)
- Quick Guide: cài .exe, load .LSP, chạy lần đầu, hiểu log cảnh báo
- PM sign-off (email xác nhận go-live)

**Entry criteria:** Sprint 5 exit criteria pass; UAT checklist (BL-36) hoàn chỉnh; ≥ 2 file bản vẽ thực xác nhận  
**Exit criteria = Go-live criteria (xem Mục 8)**

---

## 4. Timeline và milestone

> **Giả định baseline:** Kickoff = Tuần 0. Mỗi sprint = 2 tuần. Sprint 0 = 1 tuần.

```
TUẦN 0        Sprint 0 Kickoff & Preparation
│              ↳ Sample DXF thu thập, template Excel draft, repo init
│
TUẦN 1–2      Sprint 1 — Foundation & DXF Parsing
│              ↳ MILESTONE M1: Môi trường dev + .exe prototype + DXF parser cơ bản
│
TUẦN 3–4      Sprint 2 — Room Recognition Prototype
│              ↳ MILESTONE M2 (GO/NO-GO): XR ≥ 4/5 + GB ≥ 2/3 pass trên file thực
│              ↳ ⚠️ Checkpoint bắt buộc với PM trước khi sang Sprint 3
│
TUẦN 5–6      Sprint 3 — Room Pipeline LISP→Python + UI Form
│              ↳ MILESTONE M3: Polygon hợp lệ + tên phòng gắn đúng + template Excel confirm
│
TUẦN 7–8      Sprint 4 — Door Assignment + Calculation Engine
│              ↳ MILESTONE M4 (CORE ENGINE COMPLETE): 100% unit test BR pass
│              ↳ ↳ Tính toán đúng trên golden dataset
│
TUẦN 9–10     Sprint 5 — Export + UI + Integration
│              ↳ MILESTONE M5: End-to-end pipeline chạy được DXF → Excel
│              ↳ ↳ Feature complete — không thêm feature sau đây
│
TUẦN 11–12    Sprint 6 — UAT + Packaging + Release
│              ↳ MILESTONE M6 (UAT SIGN-OFF): ≥ 13/13 tiêu chí pass
│              ↳ ↳ .exe final smoke test pass
│              ↳ ↳ MILESTONE M7 (GO-LIVE): PM sign-off
│
TUẦN 13+      Post-release support (Xem Mục 9)
```

### Bảng milestone chi tiết

| Milestone | Mô tả | Sprint | Tuần | Điều kiện pass |
|---|---|---|---|---|
| **M0** | Kickoff + sample data có | S0 | 0–1 | Sample DXF ≥ 2 file thực |
| **M1** | Dev environment + .exe prototype | S1 | 2 | CI pass, .exe mở được trên máy sạch |
| **M2 ⚠️** | **Room recognition prototype validated** | S2 | 4 | XR ≥ 4/5, GB ≥ 2/3 trên file thực |
| **M3** | Room pipeline hoàn chỉnh + template Excel frozen | S3 | 6 | Polygon valid ≥ 90%, template confirm |
| **M4** | Core calculation engine + 100% unit test BR | S4 | 8 | 100% BR test pass, accuracy < 1% |
| **M5** | Feature complete + integration OK | S5 | 10 | End-to-end pass, UI đầy đủ |
| **M6** | UAT sign-off | S6 | 12 | 13/13 tiêu chí SRS Section 15 pass |
| **M7** | **Go-live** | S6 | 12 | Release checklist 100%, PM sign-off |

### Điểm no-return

- **Sau M2:** Nếu fail → stop và re-scope (không tiến sang M3 mà không có quyết định rõ ràng)
- **Sau M3:** Template Excel frozen — không thay đổi format cột sau milestone này
- **Sau M5:** Feature freeze — không thêm story mới, chỉ fix bug

---

## 5. Release scope theo giai đoạn

### 5.1. MVP (Phase 1) — Target: Tuần 12

**Phạm vi MVP = Toàn bộ Must-have từ PRD:**

| Capability | FR/BR | Sprint |
|---|---|---|
| Đọc DXF, normalize đơn vị | FR-01, FR-03 | S1 |
| Click chọn phòng + BPOLY boundary | FR-02, FR-04, FR-05 | S2–S3 |
| Gắn tên/mã phòng từ text | FR-07, BR-07 | S3 |
| Nhận diện block cửa + thuộc tính | FR-08, FR-09 | S2 |
| Gán cửa 1 phòng và 2 phòng (ranh giới chung) | FR-10, FR-11, BR-03 | S3–S4 |
| Tính diện tích, chu vi, cạnh | FR-12, FR-13, FR-14 | S4 |
| Tính khối lượng sàn | FR-15, BR-04 | S4 |
| Tính khối lượng tường (trừ cửa, BR-06) | FR-16, FR-17, BR-05, BR-06 | S4 |
| Xuất Excel 3 sheet | FR-18–FR-21 | S5 |
| Cảnh báo dữ liệu không hợp lệ | FR-23, NFR-07 | S5 |
| Preview kết quả trong UI | FR-24 | S5 |
| Đóng gói .exe Windows | — | S6 |

**Không có trong MVP (dứt khoát):**
- Zero-click room detection (không cần click)
- Preview DXF canvas đầy đủ
- Chiều cao per-phòng khác nhau
- Nhập cửa từ Excel là primary (chỉ là fallback)
- Tích hợp BIM/ERP

### 5.2. Stabilization / Hardening (2–4 tuần sau go-live)

Sau go-live, không phát triển feature mới ngay. Team dành thời gian:
- Thu thập bug reports từ người dùng thực
- Fix P0/P1 bugs phát sinh từ bản vẽ thực đa dạng hơn
- Cải thiện UX dựa trên feedback (text cảnh báo, tốc độ xử lý)
- Viết thêm regression test cho các edge case phát hiện trong production

### 5.3. Phase 2 (Post-Stabilization, 4–6 tháng sau go-live)

| Capability | Lý do defer | Priority |
|---|---|---|
| Preview DXF canvas trong app | R&D QPainter / matplotlib; không block MVP | High |
| Nhập cửa từ Excel là primary flow | Chờ feedback từ UAT; MVP đã có fallback | Medium |
| Phòng L-shape phức tạp nhiều ngóc ngách | Cần thêm data thực; không khả thi trong MVP timeframe | High |
| Zero-click room detection | R&D dài; không có trong SRS v1.0 | Low |
| Chiều cao thông thủy per-phòng | Cần thay đổi data model; cần research use case | Medium |
| Bóc tách trần, cột, dầm | Mở rộng SRS — cần PRD riêng | TBD |

---

## 6. Rủi ro và Mitigation plan

### R-01: Dữ liệu CAD thực tế không sạch

| | |
|---|---|
| **Mô tả** | Bản vẽ thực có hatch, nội thất (giường, tủ, bàn), ký hiệu kỹ thuật, rác ngắn < 300mm nằm trên layer tường hoặc trong vùng phòng, gây BPOLY tạo vùng sai |
| **Xác suất** | **Cao** — Đây là thực tế phổ biến với bản vẽ kiến trúc Việt Nam |
| **Tác động** | **Rất cao** — Polyline phòng sai → toàn bộ tính toán sai → kết quả vô nghĩa |
| **Tín hiệu cảnh báo sớm** | Sprint 2 prototype: Polyline tạo ra có hình dạng bất thường; diện tích bé hơn nhiều thực tế |
| **Mitigation** | (1) Thuật toán GB lọc object < 300mm; (2) Boundary Set chỉ gồm layer tường; (3) Door Sealing trước BPOLY; (4) Hướng dẫn chuẩn bị bản vẽ trong Quick Guide |
| **Owner** | Dev-B (AutoLISP) |

---

### R-02: Room recognition không ổn định

| | |
|---|---|
| **Mô tả** | Tỷ lệ phòng nhận diện thành công thấp hơn 90% khi test với bản vẽ đa dạng; phòng phức tạp (nhiều ngóc ngách, cột thụt vào) không được xử lý đúng |
| **Xác suất** | **Cao** (Sprint 2 chưa validate) |
| **Tác động** | **Critical** — Nếu sprint 2 fail, toàn bộ timeline bị ảnh hưởng |
| **Tín hiệu cảnh báo sớm** | Sprint 2: XR fail > 2/5 phòng vuông, hoặc GB fail > 1/3 phòng L-shape |
| **Mitigation** | (1) Sprint 2 là go/no-go gate bắt buộc; (2) Chuẩn bị phương án thu hẹp scope MVP (chỉ phòng vuông) nếu GB không ổn định; (3) Semi-manual fallback: user có thể vẽ Polyline tay nếu cần |
| **Owner** | Tech Lead + Dev-B |

---

### R-03: Mapping cửa-phòng sai

| | |
|---|---|
| **Mô tả** | Block cửa có insertion point không nằm rõ ràng trong vùng phòng (nằm trên tường, nằm hành lang, attribute name không khớp) → cửa không được gán hoặc gán sai phòng |
| **Xác suất** | **Trung bình** |
| **Tác động** | **Cao** — Sai gán cửa → tính toán tường sai → kết quả xuất ra sai mà không rõ ràng |
| **Tín hiệu cảnh báo sớm** | Sprint 3/4: unassigned door rate > 10%; test case cửa ranh giới chung fail |
| **Mitigation** | (1) Config mapping attribute name (không hard-code); (2) Buffer distance 50mm cho spatial lookup; (3) Cảnh báo rõ ràng "X cua chua gan duoc phong" trong UI; (4) Fallback: nhập cửa từ Excel |
| **Owner** | Dev-A |

---

### R-04: Chênh lệch đơn vị đo

| | |
|---|---|
| **Mô tả** | File DXF có `$INSUNITS = 0` (unitless) hoặc người dùng vẽ bằng đơn vị m thay vì mm → tọa độ bị nhân sai 10³ hoặc 10⁶ → diện tích sai hàng triệu lần |
| **Xác suất** | **Trung bình** |
| **Tác động** | **Rất cao** — Số liệu sai hoàn toàn, khó detect nếu không có validation |
| **Tín hiệu cảnh báo sớm** | Sprint 1/2: diện tích phòng tính ra vài m² hoặc vài triệu m²; tọa độ polygon có giá trị bất thường |
| **Mitigation** | (1) BL-09: detect `$INSUNITS` và cảnh báo nếu không phải mm; (2) Validate range diện tích sau tính toán (< 0.5m² hoặc > 500m² → cảnh báo bất thường); (3) Hiển thị đơn vị rõ ràng trong log |
| **Owner** | Dev-A |

---

### R-05: Độ chính xác tính toán không đạt

| | |
|---|---|
| **Mô tả** | Diện tích / chu vi tính từ Shapely sai > 1% so với đo tay do float precision từ LISP coordinates hoặc Polygon không clean |
| **Xác suất** | **Thấp** (Shapely đủ chính xác) nhưng có thể xảy ra với Polygon phức tạp |
| **Tác động** | **Cao** — MVP KPI yêu cầu < 1% sai lệch |
| **Tín hiệu cảnh báo sớm** | Sprint 4: golden dataset test thấy sai lệch 1–3% trên phòng L-shape |
| **Mitigation** | (1) `polygon.buffer(0)` để clean geometry trước khi tính; (2) Golden dataset 5 phòng với kết quả đo tay → regression test; (3) `simplify(tolerance=0.1mm)` nếu cần |
| **Owner** | Dev-A |

---

### R-06: UX không đủ để người dùng kiểm tra kết quả

| | |
|---|---|
| **Mô tả** | Người dùng nhận Excel mà không có cách kiểm tra nhanh trong app → không biết phòng nào tính sai, cảnh báo không rõ ràng → mất niềm tin vào tool |
| **Xác suất** | **Trung bình** |
| **Tác động** | **Trung bình** — Không block MVP về kỹ thuật nhưng ảnh hưởng adoption |
| **Tín hiệu cảnh báo sớm** | UAT: end user nói "không biết có tính đúng không"; phải mở Excel rồi so sánh thủ công |
| **Mitigation** | (1) BL-35: panel tóm tắt room list trong app trước khi xuất; (2) Cảnh báo có count "X phong hop le, Y phong co van de"; (3) Warning log có thể mở và đọc được |
| **Owner** | PM/UX + Dev-A |

---

### R-07: Packaging và deployment trên Windows

| | |
|---|---|
| **Mô tả** | PyInstaller bundle Shapely + PySide6 có DLL conflict; antivirus block .exe; .LSP file cần load thủ công mỗi khi mở AutoCAD |
| **Xác suất** | **Cao** (DLL conflict đã được ghi nhận trong PRD) |
| **Tác động** | **Cao** — .exe không chạy được = sản phẩm không deliver được |
| **Tín hiệu cảnh báo sớm** | Sprint 1 BL-03: .exe crash khi mở; hoặc import error trong console |
| **Mitigation** | (1) BL-03 prototype sớm Sprint 1 là hard gate; (2) Dùng `--onedir` thay `--onefile` để tránh extraction issue; (3) Hướng dẫn whitelist trong Quick Guide; (4) Hướng dẫn dùng APPLOAD / startup suite cho .LSP |
| **Owner** | Dev-A |

---

### R-08: Thiếu sample data representative

| | |
|---|---|
| **Mô tả** | File DXF mẫu không đại diện cho bản vẽ thực tế của khách hàng (layer naming khác, block cửa khác, phong cách vẽ khác) → UAT phát sinh hàng loạt case mới |
| **Xác suất** | **Trung bình** |
| **Tác động** | **Cao** — UAT Sprint 6 phát hiện nhiều case → không đủ thời gian fix → delay go-live |
| **Tín hiệu cảnh báo sớm** | Sprint 0: chỉ có file synthetic, không có file thực; Sprint 2: file thực từ khách hàng rất khác file test |
| **Mitigation** | (1) Sprint 0 ưu tiên cao: thu thập ≥ 2 file DXF thực từ khách hàng, đa dạng phong cách; (2) Nếu không có → document rõ giả định, tăng buffer UAT Sprint 6; (3) Layer config cơ chế linh hoạt (BL-08) |
| **Owner** | PM |

---

## 7. Milestone Quality Gates

### Gate 1 — Prototype Gate (sau Sprint 2 / M2)

**Mục đích:** Xác nhận room recognition đủ ổn định để tiếp tục build. Đây là gate quan trọng nhất.

| Tiêu chí | Ngưỡng | Đo bằng cách nào |
|---|---|---|
| XR pass rate trên file thực | ≥ 4/5 phòng vuông | Demo live + ghi kết quả |
| GB pass rate trên file thực | ≥ 2/3 phòng L-shape | Demo live + ghi kết quả |
| .exe prototype chạy được | 100% | Smoke test trên máy Dev sạch |
| DXF parser đọc đúng entity | Unit test pass | CI pipeline |
| PM review và confirm | Go decision | Meeting notes / email |

**Hành động nếu fail:**
- Fail XR/GB ngưỡng → họp khẩn 24h: quyết định điều chỉnh thuật toán (extend 1 sprint) hoặc thu hẹp scope MVP
- Fail .exe prototype → investigate DLL issue, không tiến sang Sprint 3 khi chưa resolve

---

### Gate 2 — Development Complete Gate (sau Sprint 4 / M4)

**Mục đích:** Tất cả business logic đã implement và test đúng trước khi vào integration.

| Tiêu chí | Ngưỡng | Đo bằng cách nào |
|---|---|---|
| Unit test BR-04, BR-05, BR-06 | **100% pass** | pytest CI report |
| Diện tích golden dataset | Sai lệch < 1% | Test script so sánh output vs expected |
| BR-06 test case cửa chung | Ít nhất 2 case pass | pytest |
| Template Excel đã xác nhận | Signed off | Issue tracker / email |
| UAT checklist 13 tiêu chí | Sẵn sàng (chưa run) | Document review |

**Hard gate:** 100% BR unit test pass là điều kiện bắt buộc — không negotiate.

---

### Gate 3 — QA Gate (sau Sprint 5 / M5)

**Mục đích:** Integration test xác nhận end-to-end pipeline hoạt động trên data thực.

| Tiêu chí | Ngưỡng | Đo bằng cách nào |
|---|---|---|
| End-to-end test với DXF đầy đủ | Pass 100% | QA test report |
| File Excel đầu ra | Mở được, không corrupt, 3 sheet | Mở thủ công trên Excel + LibreOffice |
| Tổng diện tích trong Excel | Khớp với sum từng phòng | Formula check trong Excel |
| Cảnh báo phòng/cửa lỗi | Hiển thị đúng loại | Test với input có phòng thiếu text, cửa thiếu size |
| UI không freeze 30 giây | Pass | Thực tế chạy pipeline đếm thời gian |
| Open bug P0 | 0 | Bug tracker |
| Open bug P1 | ≤ 3, có kế hoạch fix trong S6 | Bug tracker |

---

### Gate 4 — UAT Gate (Sprint 6 / M6)

**Mục đích:** End user xác nhận sản phẩm đáp ứng nhu cầu nghiệp vụ thực tế.

| Tiêu chí | Ngưỡng | Đo bằng cách nào |
|---|---|---|
| 13 tiêu chí SRS Section 15 | Tất cả pass | UAT checklist sign-off |
| Tỷ lệ phòng nhận diện đúng | ≥ 90% trong test case UAT | UAT report |
| Tỷ lệ cửa gán đúng | ≥ 95% trong test case UAT | UAT report |
| Lỗi crash (unhandled exception) | 0 | Chạy toàn bộ test cases UAT |
| Số liệu diện tích sai > 1% không cảnh báo | 0 | Review chi tiết từng phòng |
| PM / end user đại diện ký off | Bắt buộc | Email / document sign-off |

---

### Gate 5 — Release Gate (M7)

**Mục đích:** Xác nhận .exe final sẵn sàng distribute.

| Tiêu chí | Ngưỡng | Đo bằng cách nào |
|---|---|---|
| .exe chạy trên Windows 10 (64-bit) | Pass | Smoke test |
| .exe chạy trên Windows 11 (64-bit) | Pass | Smoke test |
| Không cần cài Python / Shapely / PySide6 | Verified | Test trên máy clean (fresh Windows install) |
| Quick Guide: user mới chạy được trong 15 phút | Verified | 1 người dùng mới đọc + thực hành |
| Pre-release checklist (Mục 8) | 100% | PM review |

---

## 8. Go-live criteria

### 8.1. Điều kiện bắt buộc (phải đạt 100% trước go-live)

- [ ] **GLC-01:** Tất cả 13 tiêu chí nghiệm thu SRS Section 15 pass trong UAT
- [ ] **GLC-02:** Tỷ lệ phòng nhận diện đúng ≥ 90% trong test case UAT với file bản vẽ thực
- [ ] **GLC-03:** Tỷ lệ cửa gán đúng phòng ≥ 95%
- [ ] **GLC-04:** Sai lệch diện tích < 1% so với đo tay trong golden dataset
- [ ] **GLC-05:** BR-06 áp dụng đúng trong ít nhất 2 test case cửa trên ranh giới chung
- [ ] **GLC-06:** 100% unit test BR-04/05/06 pass (CI report)
- [ ] **GLC-07:** 0 lỗi crash (unhandled exception) trong toàn bộ test case UAT
- [ ] **GLC-08:** 0 trường hợp xuất sai số liệu mà không có cảnh báo
- [ ] **GLC-09:** .exe chạy được trên Windows 10/11 không cài Python, smoke test pass ≥ 2 máy
- [ ] **GLC-10:** PM hoặc end user đại diện ký xác nhận UAT sign-off
- [ ] **GLC-11:** Template Excel đã được PM/end user xác nhận format trước Sprint 5

### 8.2. Điều kiện nên có (tốt nhất là có, không block go-live)

- [ ] Quick Guide được end user thực hành và confirm chạy được trong 15 phút
- [ ] Panel kiểm tra kết quả trong app hiển thị được tổng quan (BL-35)
- [ ] Antivirus không block .exe trên máy test (nếu block → có hướng dẫn whitelist trong Quick Guide)
- [ ] Warning log file xuất ra readable (không chỉ hiện trên UI)

### 8.3. Blocker không được bỏ qua

Các điều kiện sau **tự động block go-live** dù PM muốn ship:
1. Có lỗi crash với file bản vẽ thực (bất kỳ unhandled exception nào)
2. Số liệu diện tích sai > 1% mà không có cảnh báo trong bất kỳ phòng nào trong UAT
3. BR-06 chưa được test với case cụ thể (không có test case cửa chung)
4. .exe không chạy được trên máy sạch Windows
5. UAT chưa có file bản vẽ thực (chỉ test trên file synthetic)

### 8.4. Pre-release checklist

```
PRE-RELEASE CHECKLIST — phải complete trước khi ship
□ Code
  □ Tất cả P0/P1 bug từ UAT đã fix và verified
  □ CI pipeline green (pytest 100% pass)
  □ Không có open TODO/FIXME trong code path critical
  □ Version số trong app đã cập nhật

□ Build
  □ .exe build từ main branch (không phải branch dev)
  □ Smoke test trên Windows 10 (máy sạch) — pass
  □ Smoke test trên Windows 11 (máy sạch) — pass
  □ File size .exe trong khoảng hợp lý (< 300 MB)
  □ .LSP files bundle kèm theo đúng thư mục

□ Data & Test
  □ Golden dataset test pass (diện tích sai < 1%)
  □ UAT report hoàn chỉnh (kết quả từng tiêu chí)
  □ Bug tracker: không có open P0/P1

□ Documentation
  □ Quick Guide hoàn chỉnh (cài, load .LSP, chạy lần đầu, hiểu cảnh báo)
  □ Layer convention mặc định được document
  □ Attribute block cửa được document (tên attribute expected)
  □ Known limitations list (case nào tool chưa xử lý được)

□ Sign-off
  □ PM sign-off email nhận được
  □ Ít nhất 1 end user thực tế confirm dùng được
  □ Tech Lead xác nhận code quality gate pass
```

---

## 9. Rollout & Support plan

### 9.1. Rollout nội bộ

**Giai đoạn 1 — Soft launch (2 tuần sau go-live):**
- Distribute .exe và .LSP bundle cho 1–2 người dùng thực tế (người đã tham gia UAT)
- Yêu cầu họ dùng trên ≥ 3 file bản vẽ thực khác nhau trong 2 tuần
- Thu thập feedback qua form đơn giản hoặc email (không cần issue tracker phức tạp)

**Giai đoạn 2 — Full rollout (sau soft launch không có P0 bug):**
- Distribute cho toàn bộ nhóm QS của khách hàng
- PM gửi Quick Guide kèm theo
- Tổ chức session demo 30 phút nếu nhóm > 5 người

### 9.2. Thu thập feedback sớm

Sau mỗi lần người dùng xử lý một file, yêu cầu trả lời 3 câu hỏi:
1. Tỷ lệ phòng nhận diện đúng (ước tính %)?
2. Có phòng/cửa nào cần can thiệp thủ công không?
3. Kết quả Excel có thể dùng ngay không hay cần chỉnh?

Feedback được collect vào spreadsheet tracking. Nếu câu 1 < 80% hoặc câu 3 = "không" liên tục → bug triage ngay.

### 9.3. Xử lý bug sau release

**Bug triage hàng tuần (15 phút):**

| Level | Thời gian fix | Quy trình |
|---|---|---|
| P0 – Crash / data loss | ≤ 24h | Hotfix branch → test → release patch ngay |
| P1 – Tính sai không cảnh báo | ≤ 3 ngày | Hotfix branch → test → release trong tuần |
| P2 – UI/UX issue | Sprint tiếp theo | Backlog, prioritize theo impact |
| P3 – Nice-to-have | Phase 2 | Backlog, không commit timeline |

**Release patch:** build lại .exe từ hotfix branch, smoke test 2 máy, distribute kèm changelog ngắn.

### 9.4. Quản lý backlog bug/hotfix

- Dùng issue tracker (GitHub Issues hoặc bất kỳ tool nào team đang dùng)
- Label: `bug-p0`, `bug-p1`, `bug-p2`, `phase2`
- Mỗi bug P0/P1 phải có: reproduction steps, file DXF gây lỗi (nếu có), expected vs actual
- Weekly bug triage: PM + Tech Lead review open P1+, quyết định fix trong tuần hay không

---

## 10. Governance & Ceremony

### Sprint Planning (đầu mỗi sprint — 1.5–2 giờ)

**Thành phần:** PM, Tech Lead, Dev-A, Dev-B, QA  
**Input:** Backlog items đã refined, exit criteria sprint trước đã pass  
**Output:** Sprint backlog confirmed, story points ước tính, dependency rõ ràng  
**Rule:** Không bắt đầu sprint nếu exit criteria sprint trước chưa pass đủ

### Backlog Refinement (giữa sprint — 45–60 phút)

**Thành phần:** PM, BA, Tech Lead  
**Tần suất:** 1 lần/sprint, tuần lẻ (giữa sprint)  
**Output:** Stories Sprint tiếp theo đã có acceptance criteria rõ ràng, đủ DoR  
**Focus đặc biệt Sprint 3–4:** BA review business rule BR-06 test case trước khi Dev code

### Sprint Demo / Review (cuối sprint — 1 giờ)

**Thành phần:** Toàn team + PM + ít nhất 1 end user nếu có  
**Format:** Demo working artifact (không phải slide), sau đó Q&A  
**Kết quả bắt buộc:** PM xác nhận exit criteria pass/fail trong meeting; ghi notes

**Demo checklist theo sprint:**

| Sprint | Demo artifact |
|---|---|
| S1 | Script chạy → in entity list từ DXF; .exe prototype mở được |
| S2 | **Live demo:** click phòng trong AutoCAD → LWPOLYLINE đỏ xuất hiện |
| S3 | Pipeline LISP→JSON→Python: show Polygon + room_name trong console |
| S4 | pytest report 100% BR pass; show golden dataset comparison |
| S5 | End-to-end: DXF → click → Excel xuất → mở file |
| S6 | UAT report; .exe smoke test live |

### Retrospective (cuối sprint — 30 phút)

**Format:** Start/Stop/Continue, 1 action item per person  
**Output:** ≤ 3 improvement items, ghi vào backlog với label `retro`

### Bug Triage (hàng tuần sau go-live — 15 phút)

**Thành phần:** PM, Tech Lead  
**Input:** Danh sách bug mới từ issue tracker  
**Output:** Priority được gán, owner được gán, ETA sơ bộ

### Checkpoint với Stakeholder (sau M2, M4, M7)

| Checkpoint | Thời điểm | Nội dung | Thành phần |
|---|---|---|---|
| CP-1 (Go/No-go) | Cuối Sprint 2 | Kết quả prototype, quyết định tiếp tục/re-scope | PM + Stakeholder + Tech Lead |
| CP-2 (Core Done) | Cuối Sprint 4 | Demo tính toán đúng, review business rule accuracy | PM + end user đại diện |
| CP-3 (Release) | Cuối Sprint 6 | UAT sign-off, release decision | PM + Stakeholder |

---

## 11. Traceability: Sprint → Epic → SRS → Deliverable

| Sprint | Epic(s) | SRS FR/BR/NFR chính | Backlog Items | Deliverable |
|---|---|---|---|---|
| S0 (Prep) | — | — | — | Sample DXF thực; template Excel draft; repo init |
| **S1** | EPIC-01, EPIC-02 | FR-01, FR-03; NFR-02, NFR-04 | BL-01, BL-02, BL-03, BL-04, BL-05, BL-06, BL-09 | Repo + CI; DXF parser (LINE/TEXT); .exe prototype |
| **S2** | EPIC-03 (Prototype) | FR-02, FR-04, FR-05; BR-01 | BL-07, BL-08, BL-10, BL-11 | AutoLISP XR + GB prototype validated; block cửa parser |
| **S3** | EPIC-03 (Build), EPIC-06 (prep) | FR-05, FR-06, FR-07, FR-10; BR-07 | BL-12, BL-13, BL-14, BL-15, BL-16, BL-17, BL-26, BL-31 | Room pipeline LISP→Python; door spatial assignment; template Excel frozen; UI form |
| **S4** | EPIC-04, EPIC-05, EPIC-08 (prep) | FR-10, FR-11, FR-12–FR-17; BR-03, BR-04, BR-05, BR-06 | BL-18, BL-19, BL-20, BL-21, BL-22, BL-23, BL-24, BL-25, BL-36 | Calculation engine hoàn chỉnh; 100% BR unit test pass; UAT checklist sẵn sàng |
| **S5** | EPIC-06, EPIC-07 | FR-18–FR-24; NFR-03, NFR-06, NFR-07 | BL-27, BL-28, BL-29, BL-30, BL-32, BL-33, BL-34, BL-35 | Excel 3 sheet; UI đầy đủ; end-to-end integration pass |
| **S6** | EPIC-08 | NFR-04, NFR-06; SRS Section 15 | BL-37, BL-38, BL-39 | UAT report; .exe final; Quick Guide; PM sign-off |

### Coverage FR/BR theo sprint

| FR/BR | Sprint cover | Gate kiểm tra |
|---|---|---|
| FR-01, FR-03 | S1 | Gate 1 (unit test) |
| FR-02, FR-04, FR-05 | S2 prototype → S3 build | Gate 1 (prototype rate) |
| FR-06, FR-07 | S3 | Gate 2 (pipeline test) |
| FR-08, FR-09 | S2 | Gate 1 |
| FR-10, FR-11 | S3 (basic) → S4 (ranh giới) | Gate 2 |
| FR-12, FR-13, FR-14 | S4 | Gate 2 (golden dataset) |
| FR-15, FR-16, FR-17 | S4 | Gate 2 (unit test BR) |
| FR-18–FR-21 | S5 | Gate 3 (QA integration) |
| FR-22, FR-23, FR-24 | S5 | Gate 3 |
| BR-04, BR-05, BR-06 | S4 | Gate 2 (**hard gate: 100%**) |
| NFR-03, NFR-04 | S4 (unit test) + S5 (integration) | Gate 3 |
| NFR-07 | S5 | Gate 3 |

---

*Tài liệu này phải được PM + Tech Lead review và ký xác nhận trước Sprint 1 Kickoff.*  
*Mọi thay đổi scope (thêm story, thay đổi sprint assignment) phải cập nhật vào đây và notify toàn team.*

*Version 1.0 — Last updated: _(điền ngày kickoff)_*
