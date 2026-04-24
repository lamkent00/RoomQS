"""
Smoke test — T1-01
Mục đích: xác nhận các package cốt lõi có thể import thành công.
Không test business logic; đây là baseline CI check.
"""


def test_import_ezdxf() -> None:
    """ezdxf phải import được (DXF parsing library)."""
    import ezdxf  # noqa: F401

    assert ezdxf.__version__, "ezdxf version should not be empty"


def test_import_shapely() -> None:
    """Shapely phải import được (geometry library)."""
    from shapely.geometry import Polygon  # noqa: F401

    poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    assert poly.area == 1.0, "Basic Shapely Polygon area should be 1.0"


def test_import_openpyxl() -> None:
    """openpyxl phải import được (Excel export library)."""
    import openpyxl  # noqa: F401

    wb = openpyxl.Workbook()
    assert wb is not None


def test_src_modules_importable() -> None:
    """
    Các src sub-packages phải tồn tại dưới dạng package (có __init__.py).
    Kiểm tra cơ bản để phát hiện sớm lỗi cấu trúc thư mục.
    """
    import pathlib

    src_root = pathlib.Path(__file__).parent.parent / "src"
    packages = [
        p.name
        for p in src_root.iterdir()
        if p.is_dir() and (p / "__init__.py").exists()
    ]
    assert len(packages) > 0, (
        "Không tìm thấy sub-package nào trong src/. "
        "Kiểm tra lại __init__.py trong từng module."
    )


def test_no_syntax_errors_in_src() -> None:
    """
    Compile tất cả .py files trong src/ để phát hiện syntax error sớm.
    """
    import pathlib
    import py_compile

    src_root = pathlib.Path(__file__).parent.parent / "src"
    py_files = list(src_root.rglob("*.py"))
    assert len(py_files) > 0, "Không tìm thấy .py file nào trong src/"

    errors = []
    for py_file in py_files:
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"{py_file}: {exc}")

    assert not errors, "Syntax errors found in src/:\n" + "\n".join(errors)
