# QA REVIEW REPORT: SPRINT 2 PLAN

**Kết quả: [PASS WITH WARNINGS] — An toàn để thực thi, có 3 cảnh báo cần xác nhận trước Sprint Start**

**Ngày review:** 2026-04-24  
**Reviewer:** Sprint Plan Reviewer  
**Tài liệu được review:** `docs/1. sprint-plans/sprint2-plan.md`  
**Tài liệu đối chiếu:**
- `docs/02-PRD-Product-Backlog.md`
- `docs/04-Kien-Truc-Tech-Stack.md`
- `docs/05-Ke-Hoach-Sprint-Release.md`
- `docs/03-User-Stories.md`

---

## 1. Tóm tắt

Sprint 2 Plan định nghĩa 5 ticket (T2-01 → T2-05) thuộc Phase 2 (Prototype & Validate), tập trung vào:
- Config layer name (BL-08)
- Parser INSERT block cửa (BL-07)
- Prototype AutoLISP XR — phòng vuông vức (BL-10)
- Prototype AutoLISP GB — phòng L-shape (BL-11)
- Báo cáo prototype + Go/No-go decision (CP-1)

Kế hoạch **phù hợp tổng thể** với PRD Backlog, kiến trúc module boundary, và kế hoạch sprint/release. Tuy nhiên, có **3 cảnh báo** cần PM/Tech Lead xác nhận trước khi chính thức bắt đầu.

---

## 2. Chi tiết kết quả Review

### 2.1. Scope alignment — PRD Backlog ✅ PASS

| Ticket | Backlog Item | PRD Sprint | Kết luận |
|--------|-------------|------------|----------|
| T2-01 | BL-08 (Config layer name) | S2 ✅ | Đúng scope, đúng sprint |
| T2-02 | BL-07 (Parser INSERT block cửa) | S2 ✅ | Đúng scope, đúng sprint |
| T2-03 | BL-10 (Prototype XR) | S2 ✅ | Đúng scope, đúng sprint, đúng priority "CORE" |
| T2-04 | BL-11 (Prototype GB) | S2 ✅ | Đúng scope, đúng sprint |
| T2-05 | Checkpoint CP-1 | S2 ✅ | Đúng — PRD §9 và doc 05 §3 Sprint 2 đều yêu cầu demo + go/no-go |

**Không có ticket nào nằm ngoài scope PRD Sprint 2.** Tất cả đều thuộc EPIC-02 (DXF Ingestion) hoặc EPIC-03 (Room Recognition).

---

### 2.2. Module Boundary — Kiến trúc ✅ PASS (có 1 warning)

#### T2-01 — Config Loader

- **Module:** `src/config/config_loader.py` — thuộc MOD-12 (Config & Logging).
- **Phân tích:** Đúng boundary. Config loader chỉ đọc file YAML, không chứa logic nghiệp vụ. Tuân thủ ADR-04 (Config over hard-code).
- **Lưu ý nhỏ:** Kiến trúc doc 04 đặt file tại `src/config/loader.py`, sprint plan đặt tại `src/config/config_loader.py`. Không phải lỗi nghiêm trọng nhưng nên thống nhất naming.

> **Verdict: PASS**

#### T2-02 — Door Reader (Parser INSERT block cửa)

- **Module:** `src/door_engine/door_reader.py`.
- **Phân tích:** Kiến trúc doc 04 Section 5 - MOD-02 (CAD Parser) ghi rõ việc đọc INSERT entities + attributes là trách nhiệm của `cad_parser`. Tuy nhiên, doc 04 Section 5 - MOD-05 (Door Detection) cũng mô tả door parsing riêng trong `door_engine/door_parser.py`.
- **Đánh giá:** Sprint plan tạo `door_reader.py` trong `door_engine/` là **hợp lý** vì:
  1. `cad_parser/dxf_reader.py` (T1-03) đã đọc entities tổng thể
  2. `door_reader.py` nhận `doc` (ezdxf document) và filter INSERT theo config — đây là **specialization** của CAD parsing cho cửa
  3. Tuy nhiên, điều này có nghĩa `door_engine/door_reader.py` sẽ **import ezdxf trực tiếp**, vi phạm nguyên tắc MOD-02 là điểm duy nhất tương tác ezdxf

> ⚠️ **WARNING W-01: `door_reader.py` import ezdxf trực tiếp**
>
> Theo kiến trúc, MOD-02 (`cad_parser`) là điểm duy nhất gọi ezdxf. Nếu `door_reader.py` cũng import ezdxf, sẽ có 2 module phụ thuộc ezdxf trực tiếp.
>
> **Hai phương án:**
> 1. **Giữ nguyên plan** — chấp nhận `door_engine` cũng là consumer ezdxf. Cập nhật doc kiến trúc ghi nhận exception này.
> 2. **Refactor** — mở rộng `cad_parser/dxf_reader.py` để đọc INSERT entities → trả về `RawCADData.door_blocks`, rồi `door_engine/door_reader.py` chỉ nhận `RawCADData.door_blocks` thuần Python.
>
> **Khuyến nghị:** Phương án 2 giữ boundary sạch hơn, nhưng **không block sprint start** vì door_reader vẫn là read-only, rủi ro thấp. PM/Tech Lead quyết định.

#### T2-03 & T2-04 — AutoLISP XR & GB

- **Module:** `lisp/xr.lsp`, `lisp/gb.lsp` — AutoCAD/AutoLISP Layer.
- **Phân tích:** Hoàn toàn đúng boundary. Kiến trúc doc 04 §2 rõ ràng: AutoLISP layer tách biệt hoàn toàn khỏi Python runtime. Không gọi Python, không phụ thuộc Python module nào. Prototype phase này LISP chạy standalone.
- **Ngưỡng pass:** XR ≥ 4/5, GB ≥ 2/3 — khớp với doc 05 §3 Sprint 2 và doc 05 §7 Gate 1.

> **Verdict: PASS**

#### T2-05 — Báo cáo Prototype

- **Module:** Documentation only — không chạm code.
- **Phân tích:** Đúng scope. Output là `docs/sprint2-prototype-report.md`.

> **Verdict: PASS**

---

### 2.3. Acceptance Criteria — Traceability ✅ PASS (có 1 warning)

| Ticket | Story IDs tham chiếu | AC Source | Kết luận |
|--------|----------------------|-----------|----------|
| T2-01 | US-INP-001 (ngầm định), US-ROOM-001 | ADR-04 dẫn xuất | ✅ AC rõ ràng, testable |
| T2-02 | US-DOOR-001 | AC-01→AC-04 | ✅ Khớp với doc 03 §US-DOOR-001 |
| T2-03 | US-ROOM-001, US-ROOM-002 | AC-01→AC-06 | ✅ Khớp với doc 03 + doc 05 ngưỡng prototype |
| T2-04 | US-ROOM-001, US-ROOM-002 | AC-01→AC-05 | ✅ Khớp |
| T2-05 | Sprint 2 Exit Criteria | AC-01→AC-05 | ✅ Khớp với doc 05 §7 Gate 1 |

> ⚠️ **WARNING W-02: T2-02 AC phạm vi kích thước cửa**
>
> T2-02 sprint plan ghi: *"Không tra cứu kích thước (width/height) trong ticket này — làm ở Sprint 4 BL-19"*.
>
> Tuy nhiên, `DoorBlock` dataclass trong plan chỉ có `door_code`, `position`, `raw_attributes` — **KHÔNG có `width_mm`, `height_mm`**. Điều này **nhất quán với out-of-scope** đã khai báo.
>
> **Nhưng**: PRD BL-07 ghi output kỳ vọng là *"List door objects với **code/name/width/height/position**"*. Có mâu thuẫn nhẹ giữa PRD expectation và sprint plan scope.
>
> **Đánh giá:** Sprint plan scope hợp lý hơn vì width/height thực tế phải đọc từ Excel (BL-19 Sprint 4) hoặc attribute block — và T2-02 ghi rõ `raw_attributes` dict sẽ chứa key-value nếu có. **Không block.**
>
> **Khuyến nghị:** PM xác nhận rằng BL-07 output trong PRD sẽ được chia: code/position/raw_attributes ở T2-02, width/height tra cứu ở BL-19.

---

### 2.4. Dependencies & Entry Criteria ✅ PASS

| Dependency | Status | Risk |
|-----------|--------|------|
| Sprint 1 exit criteria pass | Cần verify trước Sprint 2 start | ✅ Ghi đúng |
| AutoCAD 2019+ trên máy Dev-B | T0-06 đã confirm | ✅ |
| Sample DXF thực (phòng vuông + L-shape) | T0-01 | ✅ — `banve.dxf` đã có |
| `config.yaml` có section cad | T0-03 đã tạo template | ✅ |

---

### 2.5. Ticket Parallelism & Sequencing ✅ PASS

```
T2-01 (Config loader) ──┬──→ T2-03 (XR — cần wall_layer_names)
                         └──→ T2-04 (GB — cần wall_layer_names + threshold)
T2-02 (Door reader) ────────→ T2-03/T2-04 (implicit: block cửa ảnh hưởng boundary)
T2-03 (XR) ──┬──→ T2-05 (Báo cáo)
T2-04 (GB) ──┘
```

- **Dev-B**: T2-01 → T2-03 → T2-04 (tuần tự, critical path ~8–9 ngày)
- **Dev-A**: T2-02 (song song, ~1.5 ngày)

**Đánh giá:** Sequencing hợp lý. T2-01 phải xong trước T2-03/T2-04 vì LISP cần biết wall_layer_names. Dev-A và Dev-B có thể làm song song.

> ⚠️ **WARNING W-03: Effort Dev-B vượt capacity sprint 2 tuần**
>
> Dev-B phụ trách: T2-01 (1 ngày) + T2-03 (3–4 ngày) + T2-04 (3–4 ngày) = **7–9 ngày effort**.
>
> Sprint 2 tuần = 10 ngày làm việc. Nếu tính buffer meeting, review, debugging trên AutoCAD thực: capacity thực tế ~7–8 ngày.
>
> **Risk:** T2-04 (GB) có thể bị delay hoặc không đủ thời gian test đủ 3 case L-shape.
>
> **Khuyến nghị:**
> 1. Dev-B ưu tiên T2-03 (XR) trước vì đây là priority cao nhất
> 2. Nếu T2-04 không đủ thời gian: ghi nhận kết quả sơ bộ, extend sang Sprint 2.5 nếu cần
> 3. PM chuẩn bị phương án dự phòng theo doc 05 §3: *"thu hẹp scope MVP xuống chỉ phòng vuông vức"*

---

### 2.6. Risk Assessment ✅ PASS

Risks được liệt kê trong sprint plan **khớp** với doc 05 §6 (R-01, R-02, R-08) và doc 02 §11:

| Risk trong Sprint Plan | Mapping PRD/Doc 05 | Có mitigation | Verdict |
|----------------------|---------------------|---------------|---------|
| BPOLY nhiễu bởi nội thất/hatch | R-01 ✅ | GB filter 300mm ✅ | PASS |
| Layer tường không khớp | R-01/R-08 ✅ | BL-08 config ✅ | PASS |
| Phòng L-shape phức tạp | R-02 ✅ | PM thu hẹp MVP ✅ | PASS |
| Không có AutoCAD 2019+ | BLOCKER ✅ | T0-06 confirm ✅ | PASS |

---

### 2.7. Open Ambiguities ⚠️ NEEDS ATTENTION

Sprint plan ghi nhận 3 open ambiguities, tất cả đều hợp lý và **không block sprint start**:

1. **T2-01:** LISP đọc config từ đâu? → Plan đề xuất Python write ra file hoặc LISP prompt — cần quyết định trước khi Dev-B bắt đầu T2-03.
2. **T2-03:** Chiều dày tường — LISP đo đến mép LINE hay tâm tường? → Ảnh hưởng accuracy, cần quyết định trong tuần đầu sprint.
3. **T2-04:** GB tạo boundary theo tọa độ thực hay selection set? → Cần thống nhất approach với XR.

**Đánh giá:** Các ambiguities được ghi nhận rõ ràng, không bị giấu đi. Tuy nhiên, **cả 3 đều phải được resolve trong tuần đầu sprint** để không block Dev-B.

---

## 3. Out-of-scope check ✅ PASS

Sprint plan liệt kê out-of-scope:

| Out-of-scope item | PRD Sprint gốc | Khớp? |
|-------------------|----------------|-------|
| LISP → JSON export (BL-13) | S3 ✅ | ✅ |
| Python parse JSON (BL-14) | S3 ✅ | ✅ |
| Door Sealing (BL-12) | S3 ✅ | ✅ |
| Gắn tên phòng (BL-15) | S3 ✅ | ✅ |
| Unit test tính toán | S4 ✅ | ✅ |
| Feature UI | S3–S5 ✅ | ✅ |

**Không có scope leak** — sprint plan không kéo thêm bất kỳ item nào từ sprint khác.

---

## 4. Tổng kết Findings

| # | Loại | Mô tả | Mức độ | Action Required |
|---|------|--------|--------|-----------------|
| W-01 | ⚠️ WARNING | `door_reader.py` có thể import ezdxf trực tiếp — vi phạm nhẹ MOD-02 boundary | Thấp | PM/Tech Lead quyết định: giữ nguyên hay refactor qua cad_parser |
| W-02 | ⚠️ WARNING | PRD BL-07 kỳ vọng width/height nhưng T2-02 scope không bao gồm | Thấp | PM confirm chia output BL-07 giữa T2-02 và BL-19 |
| W-03 | ⚠️ WARNING | Dev-B effort 7–9 ngày / 10 ngày sprint — tight capacity | Trung bình | PM chuẩn bị phương án dự phòng nếu T2-04 không kịp |

**Không có BLOCKED item.** Tất cả warnings đều có thể resolve trong Sprint Planning meeting.

---

## 5. Kết luận & Khuyến nghị

### Verdict: **[PASS WITH WARNINGS]**

Sprint 2 Plan đạt tiêu chuẩn chất lượng để thực thi. Cụ thể:

- ✅ **Scope** khớp chính xác với PRD Backlog Sprint 2
- ✅ **Module boundary** tuân thủ kiến trúc (trừ W-01 minor)
- ✅ **Acceptance criteria** rõ ràng, testable, có hard gate
- ✅ **Dependencies** đã verify, entry criteria hợp lý
- ✅ **Risks** được ghi nhận đầy đủ với mitigation
- ✅ **Out-of-scope** được khai báo rõ, không scope leak
- ✅ **Go/No-go checkpoint** (T2-05) được thiết kế đúng theo doc 05

### Next Steps trước Sprint Start:

1. **PM resolve 3 open ambiguities** (T2-01, T2-03, T2-04) — tốt nhất trong Sprint Planning meeting
2. **Tech Lead quyết định W-01** — door_reader import ezdxf hay đi qua cad_parser
3. **PM confirm W-02** — chia output BL-07 giữa T2-02 / BL-19
4. **PM chuẩn bị contingency plan** cho W-03 (Dev-B capacity tight)
5. **Verify Sprint 1 exit criteria pass** trước khi start Sprint 2

Sau khi 5 items trên được xác nhận, team có thể bắt đầu nhận ticket Sprint 2.
