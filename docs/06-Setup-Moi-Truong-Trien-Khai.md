# 06 – Setup Môi Trường & Triển Khai

> **Phiên bản:** 1.0  
> **Cập nhật:** 2026-04-24  
> **Đối tượng:** Dev · QA · Build/Release Engineer  
> **Giả định chung:** Stack đã chốt – Python 3.11, ezdxf, Shapely, openpyxl, PyInstaller, pytest. GUI: tkinter (mặc định) hoặc PyQt6 tùy quyết định team. Platform chính: Windows 10/11 x64.

---

## 1. Mục tiêu tài liệu

### 1.1 Ai sử dụng

| Vai trò | Mục đích |
|---|---|
| **Dev** | Setup local, chạy app & test, hiểu cấu trúc thư mục |
| **QA** | Setup môi trường kiểm thử độc lập, chạy regression |
| **Build / Release Engineer** | Build artifact, đóng gói, phát hành bản production |

### 1.2 Phạm vi

- Môi trường **local development** trên Windows (chính) và macOS/Linux (hỗ trợ hạn chế cho dev).
- **Build & package** thành file thực thi `.exe` bằng PyInstaller cho Windows.
- **Release workflow** từ build candidate → QA → phát hành.
- **Backup & rollback** thực tế cho desktop app (không có server/cloud).
- **Observability** cơ bản: log file, error trace, playbook xử lý nhanh.

### 1.3 Nguyên tắc setup

1. **Reproducible** – Mọi thành viên setup từ `requirements.txt` + tài liệu này phải ra cùng kết quả.
2. **Isolation** – Dùng virtual environment, không dùng global Python.
3. **Minimal privilege** – App chạy không cần admin; chỉ ghi vào thư mục do người dùng sở hữu.
4. **Config tách khỏi code** – Mọi tham số nghiệp vụ / đường dẫn đặt trong file config, không hardcode.
5. **Không commit dữ liệu thực** – DXF thực tế của khách hàng không được vào repo.

---

## 2. Yêu cầu hệ thống

### 2.1 Hệ điều hành hỗ trợ

| Môi trường | OS | Ghi chú |
|---|---|---|
| **Production** | Windows 10 / 11 x64 | Platform chính, bắt buộc test |
| **Dev / CI** | Windows 10/11, macOS 13+, Ubuntu 22.04 | GUI test chỉ Windows |
| Không hỗ trợ | Windows 32-bit, Windows 7/8 | Shapely wheel không có |

### 2.2 Python

```
Python 3.11.x (khuyến nghị 3.11.9)
```

- **Không dùng** Python 3.12+ cho đến khi tất cả dependencies xác nhận tương thích (đặc biệt ezdxf và Shapely).
- Tải từ: https://www.python.org/downloads/release/python-3119/  
- Khi cài trên Windows: chọn ☑ **Add Python to PATH**, ☑ **pip**.

### 2.3 Công cụ bắt buộc

| Công cụ | Phiên bản | Mục đích |
|---|---|---|
| Git | ≥ 2.40 | Source control |
| Python | 3.11.x | Runtime |
| pip | ≥ 24.0 | Package manager (upgrade sau khi cài Python) |
| PyInstaller | 6.x | Build .exe |
| Make / Invoke | tuỳ | Task runner (xem §11) |

### 2.4 IDE / Editor gợi ý

- **VS Code** + extension: Python (Microsoft), Pylance, Ruff, GitLens.
- **PyCharm Professional** – nếu team quen; cấu hình interpreter trỏ vào `.venv`.

### 2.5 Dependencies chính

| Package | Phiên bản tối thiểu | Mục đích |
|---|---|---|
| `ezdxf` | 1.3.x | Parse DXF/DWG (qua DXF export) |
| `Shapely` | 2.0.x | Geometry: polygon, union, area, perimeter |
| `openpyxl` | 3.1.x | Xuất file Excel (.xlsx) |
| `xlsxwriter` | 3.2.x | Xuất Excel có format nâng cao (dùng song song openpyxl nếu cần) |
| `pydantic` | 2.x | Validation config / data model |
| `loguru` | 0.7.x | Logging |
| `pytest` | 8.x | Unit & integration test |
| `pytest-cov` | 5.x | Coverage report |
| `pyinstaller` | 6.x | Packaging |
| `tkinter` | built-in | GUI (có sẵn trong CPython Windows) |

> **Giả định:** Nếu GUI chuyển sang PyQt6 thì bổ sung `PyQt6>=6.7` vào requirements và cập nhật hook PyInstaller tương ứng.

---

## 3. Setup Local Development

### 3.1 Clone repo

```bash
git clone https://github.com/<org>/<repo>.git
cd <repo>
```

Nếu repo dùng SSH:
```bash
git clone git@github.com:<org>/<repo>.git
```

### 3.2 Tạo virtual environment

```bash
# Windows – PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1

# Windows – CMD
python -m venv .venv
.venv\Scripts\activate.bat

# macOS / Linux
python3.11 -m venv .venv
source .venv/bin/activate
```

Kiểm tra:
```bash
python --version   # phải ra Python 3.11.x
which python       # phải trỏ vào .venv
```

### 3.3 Cài dependency

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Nếu có dependency dev-only:
```bash
pip install -r requirements-dev.txt
```

> `requirements-dev.txt` chứa: `pytest`, `pytest-cov`, `ruff`, `pyinstaller`, `pre-commit`, v.v.

### 3.4 Cấu hình env

```bash
# Sao chép template
cp config/app.config.template.toml config/app.config.toml

# Chỉnh sửa nếu cần (đường dẫn sample, log level, v.v.)
notepad config/app.config.toml
```

Chi tiết biến cấu hình xem §4.

### 3.5 Chạy app ở local

```bash
# Chạy GUI
python -m src.main

# Chạy CLI (nếu có headless mode)
python -m src.main --input samples/floor_plan_01.dxf --output output/
```

### 3.6 Chạy test

```bash
# Toàn bộ test suite
pytest

# Với coverage
pytest --cov=src --cov-report=term-missing

# Chỉ test một module
pytest tests/test_room_detector.py -v

# Chỉ test nhanh (bỏ qua integration test chậm)
pytest -m "not slow"
```

### 3.7 Chạy sample input

```bash
python -m src.main --input samples/floor_plan_01.dxf --output output/
```

File DXF mẫu đặt tại `samples/` (xem §5).

### 3.8 Kiểm tra output Excel

- File Excel xuất ra tại `output/<timestamp>_result.xlsx`.
- Mở bằng Excel / LibreOffice Calc để verify:
  - Sheet "Phòng": tên phòng, diện tích, chu vi, danh sách cạnh.
  - Sheet "Tường": khối lượng tường (m²/m³).
  - Sheet "Cửa": số lượng cửa, phân loại theo rule ranh giới chung.
  - Sheet "Tổng hợp": tổng hợp toàn bộ mặt bằng.

---

## 4. Quản lý Cấu hình Môi trường

### 4.1 File cấu hình

App dùng **TOML** làm định dạng config chính (dễ đọc, không cần parser nặng).

```
config/
├── app.config.toml          # Config thực tế (KHÔNG commit)
├── app.config.template.toml # Template mẫu (commit vào repo)
└── rules/
    ├── door_rules.toml      # Rule nghiệp vụ cửa (commit)
    └── layer_mapping.toml   # Mapping tên layer DXF → loại phần tử
```

### 4.2 Biến cấu hình quan trọng

```toml
# app.config.toml

[app]
version = "1.0.0"
log_level = "INFO"          # DEBUG | INFO | WARNING | ERROR
log_dir = "logs/"
output_dir = "output/"
temp_dir = "temp/"

[dxf]
default_encoding = "utf-8"  # hoặc "cp1258" nếu file DXF tiếng Việt
wall_layer_patterns = ["WALL", "TUONG", "A-WALL"]
room_tag_layer = "TEXT_ROOM"
door_layer_patterns = ["DOOR", "CUA"]
unit = "mm"                 # đơn vị trong DXF: mm | m

[geometry]
snap_tolerance = 1.0        # mm – tolerance khi nối đường bao phòng
min_room_area = 0.5         # m² – lọc bỏ vùng quá nhỏ (noise)
wall_thickness_default = 200  # mm – dùng khi không tách được độ dày tường

[excel]
template_path = "assets/excel_template.xlsx"
decimal_places = 2

[door_rules]
shared_boundary_tolerance = 50  # mm – khoảng cách coi là ranh giới chung
```

### 4.3 Nguyên tắc tách config theo môi trường

| Môi trường | File config | Ghi chú |
|---|---|---|
| Local dev | `config/app.config.toml` | Từ template, không commit |
| QA | `config/app.config.qa.toml` | Commit với path QA |
| Production | Đóng gói trong build artifact | Xem §6 |

### 4.4 Secrets handling

- App này **không có** secret vận hành (không có API key, không có DB password).
- Nếu tương lai cần license key: lưu trong Windows Registry hoặc file `%APPDATA%\<AppName>\license.key`, **không** trong thư mục cài đặt.
- `.gitignore` phải có:

```gitignore
config/app.config.toml
*.dxf
output/
logs/
temp/
*.exe
dist/
build/
```

### 4.5 Sample config template

```toml
# app.config.template.toml – COMMIT FILE NÀY
[app]
version = "FILL_IN"
log_level = "INFO"
log_dir = "logs/"
output_dir = "output/"
temp_dir = "temp/"

[dxf]
default_encoding = "utf-8"
wall_layer_patterns = ["WALL", "TUONG"]
room_tag_layer = "TEXT_ROOM"
door_layer_patterns = ["DOOR", "CUA"]
unit = "mm"

[geometry]
snap_tolerance = 1.0
min_room_area = 0.5
wall_thickness_default = 200

[excel]
template_path = "assets/excel_template.xlsx"
decimal_places = 2

[door_rules]
shared_boundary_tolerance = 50
```

---

## 5. Dữ liệu mẫu và Thư mục làm việc

### 5.1 Cấu trúc thư mục dự án

```
<repo>/
├── src/                    # Source code
│   ├── main.py
│   ├── parser/             # DXF parser
│   ├── detector/           # Room & door detector
│   ├── geometry/           # Shapely wrappers
│   ├── rules/              # Business rules engine
│   ├── exporter/           # Excel exporter
│   └── ui/                 # GUI (tkinter / PyQt6)
├── tests/                  # Pytest
│   ├── fixtures/           # DXF fixtures nhỏ, synthetic
│   └── ...
├── samples/                # DXF mẫu đã sanitize (không có dữ liệu thực)
│   ├── floor_plan_01.dxf   # Mặt bằng đơn giản
│   ├── floor_plan_02.dxf   # Nhiều phòng, nhiều cửa
│   └── README.md
├── assets/                 # Resource đóng gói vào app
│   ├── excel_template.xlsx
│   ├── icons/
│   └── fonts/
├── config/
├── output/                 # KHÔNG commit – gitignored
├── logs/                   # KHÔNG commit – gitignored
├── temp/                   # KHÔNG commit – gitignored
├── dist/                   # PyInstaller output – KHÔNG commit
├── build/                  # PyInstaller build cache – KHÔNG commit
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── app.spec                # PyInstaller spec file – COMMIT
└── Makefile / tasks.py
```

### 5.2 Quy tắc từng thư mục

| Thư mục | Mô tả | Commit? |
|---|---|---|
| `samples/` | DXF mẫu đã sanitize (ẩn thông tin dự án thực) | ✅ Có |
| `tests/fixtures/` | DXF nhỏ, synthetic, dùng cho pytest | ✅ Có |
| `output/` | Kết quả Excel do app sinh ra | ❌ Không |
| `logs/` | Log runtime | ❌ Không |
| `temp/` | File trung gian (intermediate geometry) | ❌ Không |
| `assets/` | Template Excel, icon, font | ✅ Có |

### 5.3 Nguyên tắc không commit dữ liệu nhạy cảm

- DXF từ dự án thực của khách hàng: **tuyệt đối không commit**.
- Nếu cần test với file thực: đặt ngoài repo, chỉ dẫn path qua `app.config.toml`.
- Pre-commit hook kiểm tra file `.dxf` > 500KB trong staging → block commit.

---

## 6. Build và Package

### 6.1 Tổng quan

App được đóng gói bằng **PyInstaller 6.x** thành dạng **one-folder** (khuyến nghị).

```
dist/
└── FloorPlanTool_v1.0.0/
    ├── FloorPlanTool.exe   # Entry point
    ├── _internal/          # Runtime Python, DLLs, packages
    ├── config/             # Config mặc định đóng gói cùng
    ├── assets/             # Excel template, icon, font
    └── samples/            # DXF mẫu (tuỳ chọn)
```

### 6.2 Cấu hình PyInstaller – `app.spec`

```python
# app.spec
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=['.'],
    binaries=collect_dynamic_libs('shapely'),
    datas=[
        ('assets/',  'assets'),
        ('config/app.config.template.toml', 'config'),
        ('config/rules/', 'config/rules'),
        ('samples/', 'samples'),
    ],
    hiddenimports=[
        'ezdxf.addons',
        'shapely.geometry',
        'openpyxl.styles',
        'pydantic.v1',
        'tkinter',
        'tkinter.filedialog',
    ],
    hookspath=['hooks/'],
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'scipy'],  # loại bỏ nếu không dùng
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name='FloorPlanTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,              # UPX có thể kích hoạt antivirus – tắt
    console=False,          # Không hiện cmd window
    icon='assets/icons/app.ico',
)

coll = COLLECT(
    exe, a.binaries, a.zipfiles, a.datas,
    strip=False,
    upx=False,
    name='FloorPlanTool_v1.0.0',  # Cập nhật version trước mỗi release
)
```

### 6.3 One-folder vs One-file

| Chế độ | Ưu điểm | Nhược điểm | Quyết định |
|---|---|---|---|
| **One-folder** ✅ | Khởi động nhanh, dễ debug, dễ rollback | Phải zip/copy cả folder khi phân phối | **Dùng** |
| One-file | Phân phối tiện (1 file) | Khởi động chậm, antivirus hay block, khó debug | Không dùng mặc định |

### 6.4 Asset / Resource bundling

Truy cập asset trong code phải dùng helper:

```python
# src/utils/resource.py
import sys
from pathlib import Path

def resource_path(relative: str) -> Path:
    """Trả về path đúng khi chạy từ source lẫn PyInstaller bundle."""
    if getattr(sys, 'frozen', False):
        base = Path(sys._MEIPASS)  # noqa: SLF001
    else:
        base = Path(__file__).parent.parent.parent
    return base / relative
```

Dùng trong code:
```python
template = resource_path("assets/excel_template.xlsx")
```

### 6.5 Lưu ý dependency native

| Library | Vấn đề native | Giải pháp |
|---|---|---|
| **Shapely** | Cần `geos_c.dll` trên Windows | `collect_dynamic_libs('shapely')` trong spec |
| **ezdxf** | Thuần Python, không vấn đề | – |
| **openpyxl** | Thuần Python | – |
| **tkinter** | Built-in nhưng cần `tcl/tk` DLL | PyInstaller tự xử lý với CPython Windows |

Nếu dùng PyQt6: thêm hook `--collect-all PyQt6` hoặc dùng `pyinstaller --collect-all PyQt6`.

### 6.6 Versioning build

Version theo **Semantic Versioning**: `MAJOR.MINOR.PATCH`  
Ví dụ: `1.0.0`, `1.1.0`, `1.1.1`

Version được đặt tại **một nơi duy nhất**:

```toml
# pyproject.toml
[project]
name = "FloorPlanTool"
version = "1.0.0"
```

Và đọc vào app:
```python
from importlib.metadata import version
APP_VERSION = version("FloorPlanTool")
```

Trước khi build: cập nhật `version` trong `pyproject.toml` và `COLL name` trong `app.spec`.

### 6.7 Naming convention cho package phát hành

```
FloorPlanTool_v{MAJOR}.{MINOR}.{PATCH}_{YYYYMMDD}.zip
```

Ví dụ:
```
FloorPlanTool_v1.0.0_20260424.zip
FloorPlanTool_v1.1.0_20260530.zip
```

Nội dung ZIP:
```
FloorPlanTool_v1.0.0_20260424.zip
└── FloorPlanTool_v1.0.0/
    ├── FloorPlanTool.exe
    ├── _internal/
    ├── config/
    ├── assets/
    └── RELEASE_NOTES.md
```

---

## 7. Quy trình Release

### 7.1 Các bước

```
[Dev] Code freeze → Tag Git → Build candidate → Smoke test (Dev) 
    → QA verification → Sign-off → Package ZIP → Phát hành
```

### 7.2 Chi tiết từng bước

#### Bước 1 – Code freeze & Tag

```bash
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

#### Bước 2 – Build candidate

```bash
# Trên Windows, trong .venv
pip install -r requirements.txt
pip install pyinstaller

# Cập nhật version trong app.spec COLL name nếu chưa
pyinstaller app.spec --clean

# Artifact nằm tại: dist/FloorPlanTool_v1.0.0/
```

#### Bước 3 – Smoke test (Dev tự làm)

Checklist nhanh (≤ 15 phút):

- [ ] `.exe` khởi động không lỗi
- [ ] Mở được file DXF mẫu `floor_plan_01.dxf`
- [ ] Nhận diện được ít nhất 3 phòng
- [ ] Xuất Excel thành công, file mở được
- [ ] Log file được tạo tại `logs/`

#### Bước 4 – QA verification

QA chạy test case theo Test Plan (tài liệu riêng), tối thiểu:

- [ ] 2 file DXF mẫu phức tạp (nhiều phòng, nhiều cửa)
- [ ] Verify diện tích phòng đúng với tính tay ±1%
- [ ] Verify rule cửa ranh giới chung đúng
- [ ] Verify Excel format, công thức tổng

#### Bước 5 – Sign-off

PM / Tech Lead ký duyệt trên ticket release (Jira / Notion).

#### Bước 6 – Package & Phát hành

```bash
# Zip artifact
Compress-Archive -Path "dist\FloorPlanTool_v1.0.0" `
    -DestinationPath "releases\FloorPlanTool_v1.0.0_20260424.zip"
```

Upload lên kênh phát hành (shared drive / GitHub Releases / link nội bộ).

---

## 8. Production / Runtime Setup

### 8.1 Giả định môi trường người dùng cuối

- Windows 10 / 11 x64, **không cài Python**.
- Không có quyền admin thường xuyên (chỉ cần khi cài lần đầu nếu cần).
- Có thể có antivirus (Windows Defender, BKAV, Kaspersky).
- Màn hình ≥ 1366×768.

### 8.2 Yêu cầu runtime

- Không cần cài Python (đã bundle trong `_internal/`).
- Không cần cài Microsoft Visual C++ Redistributable riêng (PyInstaller bundle đủ DLL).
- RAM tối thiểu: **4 GB** (file DXF lớn có thể tốn 500 MB–1 GB trong quá trình xử lý).
- Disk: ≥ 500 MB cho app + output.

### 8.3 Thư mục cài đặt

Không cần "cài đặt" theo nghĩa truyền thống. Người dùng:

1. Nhận file ZIP.
2. Giải nén vào thư mục tùy chọn, ví dụ `C:\Tools\FloorPlanTool\`.
3. Tạo shortcut `FloorPlanTool.exe` ra Desktop.

> **Không đặt tại** `C:\Program Files\` (cần quyền write để ghi log/output).  
> **Khuyến nghị:** `C:\Users\<username>\FloorPlanTool\` hoặc `D:\Tools\FloorPlanTool\`.

### 8.4 Quyền truy cập file

| Thao tác | Quyền cần | Ghi chú |
|---|---|---|
| Đọc DXF input | Read | Bất kỳ nơi nào user có quyền |
| Ghi Excel output | Write | Thư mục output trong app folder hoặc Desktop |
| Ghi log | Write | `logs/` trong app folder |
| Đọc config | Read | `config/` trong app folder |

App **không** ghi vào Registry, không cần UAC.

### 8.5 Logging

- Log file: `<app_dir>/logs/app_YYYYMMDD.log`
- Rotate: mỗi ngày 1 file, giữ 30 ngày.
- Level mặc định production: `INFO`.

### 8.6 Output location

- Mặc định: `<app_dir>/output/`
- Người dùng có thể đổi qua UI hoặc `app.config.toml`.

### 8.7 Update strategy

- **Không có auto-update** (desktop app offline, scope hiện tại).
- Khi có bản mới: phát hành ZIP mới, người dùng giải nén đè vào thư mục cũ (xem §9 về backup trước khi đè).
- Cân nhắc bổ sung **version check dialog** (so sánh `version.json` từ shared drive) ở sprint sau.

---

## 9. Backup và Rollback

### 9.1 Những gì cần backup

| Loại | Vị trí | Tần suất | Ai làm |
|---|---|---|---|
| **Config người dùng** | `config/app.config.toml` | Trước mỗi lần update | Người dùng / IT |
| **Rule files** | `config/rules/*.toml` | Khi thay đổi rule | Dev / PM |
| **Excel template** | `assets/excel_template.xlsx` | Khi thay đổi template | Dev |
| **Output Excel** | `output/` | Sau mỗi phiên làm việc | Người dùng |
| **Build artifact cũ** | `releases/` trên shared drive | Mỗi release | Release engineer |

### 9.2 Backup trước khi update

```powershell
# Script đơn giản – chạy trước khi giải nén bản mới
$src = "C:\Users\user\FloorPlanTool"
$bak = "C:\Users\user\FloorPlanTool_backup_$(Get-Date -Format 'yyyyMMdd_HHmm')"
Copy-Item -Recurse $src $bak
Write-Host "Backup xong: $bak"
```

### 9.3 Rollback sang bản build trước

#### Cách 1 – Từ backup thư mục

```powershell
# Đổi tên bản lỗi
Rename-Item "C:\Users\user\FloorPlanTool" "FloorPlanTool_broken"
# Khôi phục backup
Rename-Item "C:\Users\user\FloorPlanTool_backup_20260424_1430" "FloorPlanTool"
```

#### Cách 2 – Từ artifact ZIP cũ

1. Xóa / rename thư mục hiện tại.
2. Giải nén ZIP của bản cũ từ `releases/` shared drive.
3. Sao chép lại `config/app.config.toml` từ backup.

### 9.4 Checklist rollback

- [ ] Xác định bản build cần rollback về (version, ngày build).
- [ ] Backup thư mục hiện tại (kể cả bản lỗi, để phân tích).
- [ ] Giải nén / copy bản cũ vào thư mục làm việc.
- [ ] Sao chép lại `config/app.config.toml` từ backup (không dùng config mặc định).
- [ ] Chạy smoke test nhanh (mở app, mở 1 DXF mẫu, xuất Excel).
- [ ] Thông báo cho người dùng và ghi ticket lỗi.

### 9.5 Cơ chế khôi phục khi bản build lỗi hoàn toàn (không chạy được)

1. Log crash thường nằm tại `logs/app_YYYYMMDD.log` hoặc `%TEMP%\FloorPlanTool_crash.log`.
2. Nếu không có log: chạy `.exe` từ CMD để xem stderr:
   ```cmd
   cd C:\Users\user\FloorPlanTool
   FloorPlanTool.exe > crash_output.txt 2>&1
   ```
3. Gửi `crash_output.txt` + `logs/` cho Dev để phân tích.
4. Thực hiện rollback theo §9.3.

---

## 10. Quan sát và Xử lý Sự cố

### 10.1 Vị trí log

| Môi trường | Đường dẫn |
|---|---|
| Dev | `<repo>/logs/app_YYYYMMDD.log` |
| Production | `<app_dir>/logs/app_YYYYMMDD.log` |
| Crash (fallback) | `%TEMP%\FloorPlanTool_crash.log` |

### 10.2 Mức log

| Level | Khi nào |
|---|---|
| `DEBUG` | Parse từng entity DXF, tính toán geometry từng bước |
| `INFO` | Bắt đầu / kết thúc xử lý file, số phòng nhận diện, output path |
| `WARNING` | Layer không nhận diện được, snap miss, phòng không khép kín |
| `ERROR` | Exception có handle được (file không mở được, encode lỗi) |
| `CRITICAL` | Exception không handle được – app crash |

Dev / QA: set `log_level = "DEBUG"` trong config.  
Production: `log_level = "INFO"`.

### 10.3 Thu thập log phục vụ support

Khi người dùng báo lỗi, yêu cầu cung cấp:
1. File log ngày xảy ra lỗi: `logs/app_YYYYMMDD.log`.
2. File DXF input (nếu không nhạy cảm).
3. Màn hình chụp lỗi.
4. Version app (hiển thị trong title bar hoặc menu About).

### 10.4 Lỗi thường gặp & cách xử lý nhanh

#### Parse DXF

| Lỗi | Nguyên nhân | Xử lý |
|---|---|---|
| `ezdxf.DXFStructureError` | File DXF corrupt hoặc version quá cũ (R12) | Mở lại trong AutoCAD, Save As DXF R2010+ |
| Phòng không nhận diện | Layer tường sai tên | Kiểm tra `wall_layer_patterns` trong config, thêm tên layer thực tế |
| Text phòng không đọc được | Encoding sai | Đổi `default_encoding = "cp1258"` (tiếng Việt ANSI) |
| Đường bao không khép kín | Geometry gap | Tăng `snap_tolerance`, hoặc clean DXF trong AutoCAD trước |

#### Export Excel

| Lỗi | Nguyên nhân | Xử lý |
|---|---|---|
| `PermissionError` khi ghi xlsx | File Excel đang mở trong Excel | Đóng file Excel trước khi xuất |
| Cell format lỗi | Template xlsx không tương thích | Dùng template chuẩn từ `assets/` |
| Số thập phân sai | `decimal_places` chưa cấu hình | Kiểm tra config |

#### Package / Runtime

| Lỗi | Nguyên nhân | Xử lý |
|---|---|---|
| `ModuleNotFoundError` khi chạy exe | Missing hidden import | Thêm vào `hiddenimports` trong `app.spec`, rebuild |
| `OSError: cannot load library geos_c.dll` | Shapely DLL không bundle | Kiểm tra `collect_dynamic_libs('shapely')` trong spec |
| App chạy khác local | Path asset sai | Dùng `resource_path()` helper (§6.4) |
| Antivirus quarantine exe | False positive | Xem §13 |

### 10.5 Playbook xử lý nhanh

```
Người dùng báo lỗi
    ↓
1. Hỏi version app + OS
2. Lấy log ngày lỗi
3. Tái hiện với file DXF đó trên máy dev (DEBUG mode)
4. Nếu tái hiện được → fix bug → hotfix release
5. Nếu không tái hiện → kiểm tra config, encoding, layer mapping
6. Nếu crash hoàn toàn → rollback, mở ticket P1
```

---

## 11. CI/CD / Build Automation

### 11.1 Mức automation tối thiểu

App này là desktop, không cần pipeline phức tạp. Tối thiểu cần:

| Bước | Trigger | Tool |
|---|---|---|
| Lint & format check | Push / PR | `ruff check src/` |
| Unit test | Push / PR | `pytest tests/unit/` |
| Integration test | PR vào main | `pytest tests/integration/ -m slow` |
| Build artifact | Tag `v*.*.*` | `pyinstaller app.spec --clean` |

### 11.2 Build pipeline gợi ý (GitHub Actions)

```yaml
# .github/workflows/build.yml
name: Build & Test

on:
  push:
    branches: [main, develop]
  pull_request:
  release:
    types: [created]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: ruff check src/
      - run: pytest --cov=src --cov-report=xml -m "not slow"

  build:
    needs: test
    runs-on: windows-latest
    if: startsWith(github.ref, 'refs/tags/v')
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt pyinstaller
      - run: pyinstaller app.spec --clean
      - name: Zip artifact
        run: |
          $ver = "${{ github.ref_name }}"
          $date = Get-Date -Format "yyyyMMdd"
          Compress-Archive -Path "dist\FloorPlanTool_*" `
            -DestinationPath "releases\FloorPlanTool_${ver}_${date}.zip"
        shell: pwsh
      - uses: actions/upload-artifact@v4
        with:
          name: FloorPlanTool-release
          path: releases/*.zip
```

> **Giả định:** Nếu team không dùng GitHub Actions, có thể dùng GitLab CI hoặc script Makefile/Invoke chạy thủ công.  
> Runner phải là **Windows** (không build `.exe` trên Linux).

### 11.3 Artifact management

- Build artifact lưu trên: GitHub Releases (nếu public) hoặc shared drive nội bộ.
- Giữ tối thiểu **3 bản release gần nhất** để rollback.
- Bản cũ hơn archive vào folder `archive/` với naming chuẩn (§6.7).

---

## 12. Checklist Bàn giao Môi trường

### 12.1 Dev machine

- [ ] Python 3.11.x cài và kiểm tra `python --version`
- [ ] Git cài, SSH key hoặc HTTPS token đã cấu hình
- [ ] Clone repo thành công
- [ ] Virtual env `.venv` tạo trong repo root
- [ ] `pip install -r requirements.txt` không lỗi
- [ ] `pip install -r requirements-dev.txt` không lỗi
- [ ] `config/app.config.toml` tạo từ template, các path hợp lệ
- [ ] `python -m src.main` khởi động GUI không lỗi
- [ ] Mở `samples/floor_plan_01.dxf`, xử lý, xuất Excel thành công
- [ ] `pytest` chạy, tất cả test PASS (hoặc biết rõ test nào skip có lý do)
- [ ] VS Code / PyCharm nhận đúng interpreter `.venv`
- [ ] Pre-commit hooks cài: `pre-commit install`

### 12.2 QA machine

- [ ] Python 3.11.x hoặc dùng trực tiếp build artifact (không cần Python)
- [ ] Nhận ZIP artifact bản cần test
- [ ] Giải nén vào `C:\QA\FloorPlanTool_vX.X.X\`
- [ ] Tạo shortcut `.exe`
- [ ] Chạy được file DXF mẫu QA (có trong `samples/`)
- [ ] Có test data DXF dùng riêng cho QA (không phải sample dev)
- [ ] Biết cách đọc log tại `logs/`
- [ ] Biết cách báo lỗi: version + log + DXF + screenshot

### 12.3 Trước production release

- [ ] Code đã merge vào `main`, không có open PR liên quan
- [ ] Git tag `vX.X.X` đã push
- [ ] Build từ tag (không từ working directory chưa commit)
- [ ] Smoke test pass trên máy build sạch (máy chưa có source Python)
- [ ] QA sign-off có trong ticket
- [ ] `RELEASE_NOTES.md` cập nhật
- [ ] ZIP artifact đặt tên đúng convention
- [ ] Artifact upload lên shared drive / GitHub Releases
- [ ] Thông báo phát hành gửi đến người nhận

---

## 13. Troubleshooting FAQ

### Q: `python` không nhận sau khi cài?

**A:** Kiểm tra PATH:
```powershell
$env:PATH -split ";" | Select-String -Pattern "Python"
```
Nếu thiếu: vào *System Properties → Environment Variables*, thêm `C:\Users\<user>\AppData\Local\Programs\Python\Python311\` và `Scripts\`.

---

### Q: `pip install shapely` lỗi `error: Microsoft Visual C++ 14.0 is required`?

**A:** Shapely 2.x dùng binary wheel, không cần build. Lỗi này xảy ra khi pip tải source thay vì wheel:
```bash
pip install shapely --only-binary=shapely
```
Nếu vẫn lỗi: kiểm tra Python architecture (phải là 64-bit):
```bash
python -c "import struct; print(struct.calcsize('P')*8)"
```

---

### Q: Thiếu quyền ghi file / `PermissionError` khi xuất Excel?

**A:**
1. Kiểm tra `output/` folder có tồn tại chưa (tạo thủ công nếu thiếu).
2. Kiểm tra file Excel output đang mở trong Excel → đóng lại.
3. Không đặt app trong `C:\Program Files\` (cần quyền admin để ghi).

---

### Q: Text tiếng Việt trong DXF bị lỗi / hiển thị `??`?

**A:** File DXF lưu encoding ANSI (Windows-1258). Đổi trong config:
```toml
[dxf]
default_encoding = "cp1258"
```
Nếu vẫn lỗi: mở DXF trong AutoCAD, `SAVEAS` → chọn format DXF, đảm bảo Unicode encoding (DXF R2007+).

---

### Q: App build bằng PyInstaller chạy khác trên máy khác (path lỗi, asset không tìm thấy)?

**A:** Nguyên nhân: code dùng `__file__` hoặc relative path thay vì `resource_path()`.  
Kiểm tra toàn bộ nơi load asset trong code, thay bằng:
```python
from src.utils.resource import resource_path
path = resource_path("assets/excel_template.xlsx")
```

---

### Q: Antivirus (BKAV / Kaspersky) cảnh báo / quarantine `.exe`?

**A:** False positive phổ biến với PyInstaller do cách bundle Python.
Giải pháp:
1. **Không dùng UPX** (đã tắt trong spec: `upx=False`).
2. **Không dùng one-file mode**.
3. Thêm whitelist trong antivirus: đường dẫn app folder.
4. Nếu cần ký số: liên hệ mua **Code Signing Certificate** (Sectigo, DigiCert) và ký `.exe` bằng `signtool.exe` trước khi phát hành.

---

### Q: `pytest` pass local nhưng fail trên CI?

**A:** Nguyên nhân hay gặp:
- CI dùng Python version khác → cố định `python-version: '3.11'` trong workflow.
- Test phụ thuộc file DXF ở path tuyệt đối → dùng `tmp_path` fixture của pytest.
- Encoding khác nhau giữa Windows/Linux → force `utf-8` trong test fixture.

---

## Rủi ro & Lưu ý

| Rủi ro | Mức | Giải pháp |
|---|---|---|
| DXF từ AutoCAD version cũ (R12) không parse được bằng ezdxf | Cao | Yêu cầu xuất DXF R2010+ từ phía người dùng; ghi vào user guide |
| Shapely DLL thiếu trong bundle → crash khi chạy exe | Trung bình | Đã xử lý trong spec, kiểm tra bằng smoke test trên máy sạch |
| Antivirus block exe trên máy khách hàng | Trung bình | Tài liệu hướng dẫn whitelist; xem xét code signing |
| File DXF lớn (>50 MB) xử lý chậm / OOM | Trung bình | Monitor trong integration test; thêm progress bar & streaming parse nếu cần |
| Config người dùng bị đè khi update | Thấp | Hướng dẫn backup trước update; release note nhấn mạnh |

---

## Definition of Done – Tài liệu này hoàn tất khi

- [ ] Dev mới có thể setup từ đầu và chạy được app trong < 30 phút theo tài liệu này.
- [ ] QA có thể cài bản build và chạy test case không cần hỏi Dev.
- [ ] Release engineer có thể build, đóng gói, phát hành độc lập.
- [ ] Rollback có thể thực hiện trong < 10 phút khi có sự cố.
- [ ] Tài liệu được review bởi ít nhất 1 Dev + 1 QA và không còn mục "TBD" quan trọng.
