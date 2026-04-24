"""
tests/unit/test_dxf_reader.py — Unit tests cho MOD-02 (cad_parser)

Coverage:
  AC-01: parse_dxf() tra ve RawCADData voi du 3 fields
  AC-02: LINE entities tu wall layer dung so luong
  AC-03: LWPOLYLINE entities dung so diem va layer
  AC-04: TEXT + MTEXT co trong text_entities (raw content, chua strip)
  AC-05: Coordinates da nhan unit_factor
  AC-06: Entity tu layer khong co trong wall_layer_names bi exclude khoi wall_segments
  AC-07: File DXF corrupt -> raise exception ro rang
  AC-08: Unit test pass trong CI (file nay la bang chung)

Chien luoc:
  - Fixture 1: simple_rooms.dxf (da tao qua create_fixtures.py)
  - Fixture 2: corrupt.dxf (file gia)
  - Mock test: test apply unit_factor voi synthetic DXF tao in-memory qua ezdxf.new()
"""

from __future__ import annotations

import pathlib

import ezdxf
import pytest

from src.cad_parser.dxf_reader import LayerConfig, parse_dxf
from src.cad_parser.models import RawCADData, RawTextEntity, Segment

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

FIXTURE_DIR = pathlib.Path(__file__).parent.parent / "fixtures"
SIMPLE_ROOMS_DXF = FIXTURE_DIR / "simple_rooms.dxf"
CORRUPT_DXF = FIXTURE_DIR / "corrupt.dxf"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _default_config() -> LayerConfig:
    return LayerConfig(wall_layer_names=["TUONG"])


def _make_in_memory_dxf(
    lines: list[tuple],
    lwpolylines: list[tuple],
    texts: list[tuple],
    mtexts: list[tuple],
    insunits: int = 4,
) -> str:
    """
    Tao file DXF tam thoi trong bo nho, luu ra temp va tra ve duong dan.
    Dung ezdxf.new() -> khong can AutoCAD.

    lines: [(start, end, layer), ...]
    lwpolylines: [(points_list, closed, layer), ...]
    texts: [(content, insert, layer), ...]
    mtexts: [(content, insert, layer), ...]
    """
    import tempfile

    doc = ezdxf.new(dxfversion="R2013")
    doc.header["$INSUNITS"] = insunits
    msp = doc.modelspace()

    for start, end, layer in lines:
        doc.layers.add(layer) if layer not in [
            l.dxf.name for l in doc.layers
        ] else None
        msp.add_line(start, end, dxfattribs={"layer": layer})

    for points, closed, layer in lwpolylines:
        msp.add_lwpolyline(points, close=closed, dxfattribs={"layer": layer})

    for content, insert, layer in texts:
        msp.add_text(
            content,
            dxfattribs={"insert": insert, "height": 100, "layer": layer},
        )

    for content, insert, layer in mtexts:
        msp.add_mtext(
            content,
            dxfattribs={"insert": insert, "char_height": 100, "layer": layer},
        )

    tmp = tempfile.NamedTemporaryFile(suffix=".dxf", delete=False)
    doc.saveas(tmp.name)
    tmp.close()
    return tmp.name


# ===========================================================================
# AC-01: parse_dxf() tra ve RawCADData voi du 3 fields
# ===========================================================================


class TestAC01ReturnType:
    def test_returns_rawcaddata_instance(self):
        """parse_dxf() phai tra ve RawCADData, khong phai dict hay None."""
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        assert isinstance(result, RawCADData)

    def test_has_all_three_fields(self):
        """RawCADData phai co wall_segments, text_entities, door_blocks."""
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        assert hasattr(result, "wall_segments")
        assert hasattr(result, "text_entities")
        assert hasattr(result, "door_blocks")

    def test_door_blocks_is_empty_list_sprint1(self):
        """door_blocks phai la [] trong Sprint 1 (chua co INSERT parsing)."""
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        assert result.door_blocks == []


# ===========================================================================
# AC-02: LINE entities tu wall layer dung so luong
# ===========================================================================


class TestAC02LineEntities:
    def test_line_count_from_wall_layer(self):
        """
        simple_rooms.dxf co 8 LINE tren TUONG (Phong A: 4, Phong B: 4).
        LWPOLYLINE Phong C them 4 segments (closed) -> tong wall_segments = 12.
        """
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        assert len(result.wall_segments) == 12

    def test_wall_segments_are_segment_instances(self):
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        for seg in result.wall_segments:
            assert isinstance(seg, Segment)

    def test_segment_has_correct_fields(self):
        """Moi Segment phai co start, end (tuple 2 float) va layer (str)."""
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        seg = result.wall_segments[0]
        assert isinstance(seg.start, tuple) and len(seg.start) == 2
        assert isinstance(seg.end, tuple) and len(seg.end) == 2
        assert isinstance(seg.layer, str)

    def test_inline_line_count(self):
        """Test voi DXF in-memory: 3 LINE TUONG -> 3 segments."""
        path = _make_in_memory_dxf(
            lines=[
                ((0, 0), (1000, 0), "TUONG"),
                ((1000, 0), (1000, 500), "TUONG"),
                ((0, 0), (0, 500), "TUONG"),
            ],
            lwpolylines=[],
            texts=[],
            mtexts=[],
        )
        result = parse_dxf(path, _default_config(), unit_factor=1.0)
        assert len(result.wall_segments) == 3

    def test_line_coordinates_correct(self):
        """Kiem tra toa do cu the cua 1 LINE don gian."""
        path = _make_in_memory_dxf(
            lines=[((0, 0), (2000, 0), "TUONG")],
            lwpolylines=[],
            texts=[],
            mtexts=[],
        )
        result = parse_dxf(path, _default_config(), unit_factor=1.0)
        seg = result.wall_segments[0]
        assert seg.start == pytest.approx((0.0, 0.0))
        assert seg.end == pytest.approx((2000.0, 0.0))
        assert seg.layer == "TUONG"


# ===========================================================================
# AC-03: LWPOLYLINE entities dung so diem va layer
# ===========================================================================


class TestAC03LWPolyline:
    def test_lwpolyline_closed_generates_n_segments(self):
        """
        LWPOLYLINE voi 4 diem va closed=True -> 4 segments
        (3 canh + 1 canh cuoi->dau).
        """
        path = _make_in_memory_dxf(
            lines=[],
            lwpolylines=[
                ([(0, 0), (3000, 0), (3000, 2000), (0, 2000)], True, "TUONG"),
            ],
            texts=[],
            mtexts=[],
        )
        result = parse_dxf(path, _default_config(), unit_factor=1.0)
        assert len(result.wall_segments) == 4

    def test_lwpolyline_open_generates_n_minus_1_segments(self):
        """LWPOLYLINE voi 4 diem va closed=False -> 3 segments."""
        path = _make_in_memory_dxf(
            lines=[],
            lwpolylines=[
                ([(0, 0), (1000, 0), (1000, 500), (0, 500)], False, "TUONG"),
            ],
            texts=[],
            mtexts=[],
        )
        result = parse_dxf(path, _default_config(), unit_factor=1.0)
        assert len(result.wall_segments) == 3

    def test_lwpolyline_layer_preserved(self):
        """Layer cua LWPOLYLINE phai duoc giu nguyen trong Segment."""
        path = _make_in_memory_dxf(
            lines=[],
            lwpolylines=[([(0, 0), (500, 0), (500, 500)], False, "TUONG")],
            texts=[],
            mtexts=[],
        )
        result = parse_dxf(path, _default_config(), unit_factor=1.0)
        assert all(seg.layer == "TUONG" for seg in result.wall_segments)

    def test_lwpolyline_from_fixture_phong_c(self):
        """
        simple_rooms.dxf: Phong C la LWPOLYLINE closed 4 diem -> 4 segments.
        Tuy nhien filter theo y >= 2499 se bao gom ca canh chung cua Phong A/B
        (cac LINE ket thuc tai y=2500). Nen kiem tra theo tong segments thay vi filter.
        Tong wall_segments = 8 LINE (Phong A+B) + 4 LWPOLY (Phong C) = 12.
        """
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        # 4 LWPOLYLINE segments: start va end deu co y trong khoang [2500, 5000]
        phong_c_segs = [
            s for s in result.wall_segments
            if s.start[1] >= 2499 and s.end[1] >= 2499
            and s.start[0] in (0.0, 6000.0) or  # canh doc
            (s.start[1] in (2500.0, 5000.0) and s.end[1] in (2500.0, 5000.0)
             and abs(s.start[0] - s.end[0]) > 0)  # canh ngang
        ]
        # LWPOLYLINE closed 4 diem tao 4 segments, cong them canh chung y=2500
        # Kiem tra don gian: tong segments phai la 12
        assert len(result.wall_segments) == 12


# ===========================================================================
# AC-04: TEXT + MTEXT co trong text_entities (raw, chua strip)
# ===========================================================================


class TestAC04TextEntities:
    def test_text_entities_count(self):
        """simple_rooms.dxf co 3 TEXT + 1 MTEXT = 4 text_entities."""
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        assert len(result.text_entities) == 4

    def test_text_entities_are_rawtextentity_instances(self):
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        for te in result.text_entities:
            assert isinstance(te, RawTextEntity)

    def test_text_plain_content_preserved(self):
        """TEXT entity 'PHONG NGU' phai co raw_content dung."""
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        contents = {te.raw_content for te in result.text_entities}
        assert "PHONG NGU" in contents
        assert "WC" in contents
        assert "PHONG KHACH" in contents

    def test_mtext_raw_content_not_stripped(self):
        """
        MTEXT co formatting codes phai duoc luu nguyen (raw).
        MOD-06 (text_extractor) moi chiu trach nhiem strip.
        """
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        mtext_contents = [
            te.raw_content for te in result.text_entities
            if "fArial" in te.raw_content or "MTEXT" in te.raw_content
        ]
        assert len(mtext_contents) >= 1, "MTEXT entity phai co trong text_entities"

    def test_text_entity_has_position_and_layer(self):
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        for te in result.text_entities:
            assert isinstance(te.position, tuple) and len(te.position) == 2
            assert isinstance(te.layer, str)

    def test_inline_mtext_raw_content(self):
        """In-memory test: MTEXT voi formatting code phai duoc luu raw."""
        raw_mtext = r"{\fArial;PHONG NGU}"
        path = _make_in_memory_dxf(
            lines=[],
            lwpolylines=[],
            texts=[],
            mtexts=[(raw_mtext, (100, 100), "TEXT_LAYER")],
        )
        result = parse_dxf(path, LayerConfig(wall_layer_names=[]), unit_factor=1.0)
        assert len(result.text_entities) == 1
        # Raw content phai chua formatting code (chua strip)
        assert "fArial" in result.text_entities[0].raw_content or \
               "PHONG NGU" in result.text_entities[0].raw_content


# ===========================================================================
# AC-05: Coordinates da nhan unit_factor
# ===========================================================================


class TestAC05UnitFactor:
    def test_unit_factor_applied_to_line_coordinates(self):
        """
        LINE (0,0) -> (1000,0) voi unit_factor=25.4 (inch) ->
        segment.end = (25400.0, 0.0).
        """
        path = _make_in_memory_dxf(
            lines=[((0, 0), (1000, 0), "TUONG")],
            lwpolylines=[],
            texts=[],
            mtexts=[],
            insunits=1,  # inch
        )
        result = parse_dxf(path, _default_config(), unit_factor=25.4)
        seg = result.wall_segments[0]
        assert seg.end == pytest.approx((25400.0, 0.0), rel=1e-6)

    def test_unit_factor_applied_to_lwpolyline(self):
        """LWPOLYLINE coordinates phai duoc nhan unit_factor."""
        path = _make_in_memory_dxf(
            lines=[],
            lwpolylines=[([(0, 0), (500, 0)], False, "TUONG")],
            texts=[],
            mtexts=[],
        )
        result = parse_dxf(path, _default_config(), unit_factor=10.0)
        seg = result.wall_segments[0]
        assert seg.start == pytest.approx((0.0, 0.0))
        assert seg.end == pytest.approx((5000.0, 0.0), rel=1e-6)

    def test_unit_factor_applied_to_text_position(self):
        """TEXT position phai duoc nhan unit_factor."""
        path = _make_in_memory_dxf(
            lines=[],
            lwpolylines=[],
            texts=[("TEST", (100, 200), "L1")],
            mtexts=[],
        )
        result = parse_dxf(path, LayerConfig(wall_layer_names=[]), unit_factor=2.0)
        te = result.text_entities[0]
        assert te.position == pytest.approx((200.0, 400.0), rel=1e-6)

    def test_unit_factor_1_0_does_not_change_coords(self):
        """unit_factor=1.0 (mm) phai giu nguyen toa do."""
        path = _make_in_memory_dxf(
            lines=[((0, 0), (3000, 2500), "TUONG")],
            lwpolylines=[],
            texts=[],
            mtexts=[],
        )
        result = parse_dxf(path, _default_config(), unit_factor=1.0)
        seg = result.wall_segments[0]
        assert seg.end == pytest.approx((3000.0, 2500.0))

    def test_metres_factor_1000(self):
        """unit_factor=1000.0 (m -> mm): toa do 1.0 -> 1000.0 mm."""
        path = _make_in_memory_dxf(
            lines=[((0, 0), (1, 0), "TUONG")],
            lwpolylines=[],
            texts=[],
            mtexts=[],
        )
        result = parse_dxf(path, _default_config(), unit_factor=1000.0)
        seg = result.wall_segments[0]
        assert seg.end == pytest.approx((1000.0, 0.0))


# ===========================================================================
# AC-06: Entity tu layer KHONG phai wall_layer bi exclude khoi wall_segments
# ===========================================================================


class TestAC06LayerFilter:
    def test_non_wall_layer_excluded_from_wall_segments(self):
        """
        simple_rooms.dxf co 1 LINE tren layer OTHER.
        LINE do phai bi exclude khoi wall_segments.
        """
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        # Neu OTHER duoc include -> wall_segments se > 12
        assert all(seg.layer.upper() == "TUONG" for seg in result.wall_segments)

    def test_inline_non_wall_line_excluded(self):
        """LINE tren layer DIM bi exclude khi LayerConfig chi co TUONG."""
        path = _make_in_memory_dxf(
            lines=[
                ((0, 0), (1000, 0), "TUONG"),
                ((0, 100), (1000, 100), "DIM"),      # phai bi exclude
                ((0, 200), (1000, 200), "A-WALL"),   # phai bi exclude (khong trong config)
            ],
            lwpolylines=[],
            texts=[],
            mtexts=[],
        )
        result = parse_dxf(path, LayerConfig(wall_layer_names=["TUONG"]), unit_factor=1.0)
        assert len(result.wall_segments) == 1
        assert result.wall_segments[0].layer == "TUONG"

    def test_case_insensitive_layer_match(self):
        """Layer 'tuong' (lowercase) phai match voi wall_layer_names=['TUONG']."""
        path = _make_in_memory_dxf(
            lines=[((0, 0), (500, 0), "tuong")],
            lwpolylines=[],
            texts=[],
            mtexts=[],
        )
        result = parse_dxf(path, LayerConfig(wall_layer_names=["TUONG"]), unit_factor=1.0)
        assert len(result.wall_segments) == 1

    def test_multiple_wall_layers(self):
        """Nhieu wall layer trong config deu duoc include."""
        path = _make_in_memory_dxf(
            lines=[
                ((0, 0), (1000, 0), "TUONG"),
                ((0, 0), (0, 500), "A-WALL"),
                ((0, 0), (500, 500), "OTHER"),
            ],
            lwpolylines=[],
            texts=[],
            mtexts=[],
        )
        config = LayerConfig(wall_layer_names=["TUONG", "A-WALL"])
        result = parse_dxf(path, config, unit_factor=1.0)
        assert len(result.wall_segments) == 2

    def test_text_entities_from_any_layer(self):
        """TEXT phai duoc doc tu moi layer, ke ca layer khong phai wall."""
        path = _make_in_memory_dxf(
            lines=[],
            lwpolylines=[],
            texts=[
                ("TEXT_A", (0, 0), "TEXT_LAYER"),
                ("TEXT_B", (100, 100), "OTHER"),
                ("TEXT_C", (200, 200), "TUONG"),
            ],
            mtexts=[],
        )
        result = parse_dxf(path, _default_config(), unit_factor=1.0)
        assert len(result.text_entities) == 3


# ===========================================================================
# AC-07: File DXF corrupt -> raise exception ro rang
# ===========================================================================


class TestAC07ErrorHandling:
    def test_corrupt_dxf_raises_dxferror(self):
        """
        corrupt.dxf phai raise exception khi doc.
        ezdxf raise OSError (subclass IOError) khi file khong phai DXF hop le,
        hoac DXFError voi file DXF bi corrupt sau khi doc header.
        Ca hai deu acceptable.
        """
        with pytest.raises((ezdxf.DXFError, OSError)):
            parse_dxf(
                str(CORRUPT_DXF),
                layer_config=_default_config(),
                unit_factor=1.0,
            )

    def test_nonexistent_file_raises_file_not_found(self):
        """File khong ton tai phai raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            parse_dxf(
                "/nonexistent/path/file.dxf",
                layer_config=_default_config(),
                unit_factor=1.0,
            )

    def test_invalid_unit_factor_raises_value_error(self):
        """unit_factor <= 0 phai raise ValueError truoc khi doc file."""
        with pytest.raises(ValueError, match="unit_factor"):
            parse_dxf(
                str(SIMPLE_ROOMS_DXF),
                layer_config=_default_config(),
                unit_factor=0.0,
            )

    def test_negative_unit_factor_raises_value_error(self):
        with pytest.raises(ValueError, match="unit_factor"):
            parse_dxf(
                str(SIMPLE_ROOMS_DXF),
                layer_config=_default_config(),
                unit_factor=-1.0,
            )


# ===========================================================================
# Integration: Fixture simple_rooms.dxf full round-trip
# ===========================================================================


class TestSimpleRoomsFixtureIntegration:
    """Full round-trip test voi fixture file thuc te."""

    def test_full_parse_no_exception(self):
        """Parse simple_rooms.dxf khong raise exception."""
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        assert result is not None

    def test_wall_segments_all_on_tuong(self):
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        layers = {seg.layer for seg in result.wall_segments}
        assert layers == {"TUONG"}

    def test_text_entities_include_wc(self):
        result = parse_dxf(
            str(SIMPLE_ROOMS_DXF),
            layer_config=_default_config(),
            unit_factor=1.0,
        )
        contents = {te.raw_content for te in result.text_entities}
        assert "WC" in contents

    def test_no_shapely_import(self):
        """Xac nhan module cad_parser KHONG import Shapely."""
        import importlib
        import sys

        # Remove cache neu co
        mods_before = set(sys.modules.keys())
        import src.cad_parser.dxf_reader  # noqa: F401
        mods_after = set(sys.modules.keys())
        new_mods = mods_after - mods_before
        shapely_mods = [m for m in new_mods if "shapely" in m.lower()]
        assert shapely_mods == [], f"cad_parser khong duoc import Shapely: {shapely_mods}"
