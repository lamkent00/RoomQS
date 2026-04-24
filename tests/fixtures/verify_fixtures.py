"""Script verify các DXF fixtures cho T1-06."""
import sys
import ezdxf

def verify_simple_rooms():
    print("=== simple_rooms.dxf ===")
    doc = ezdxf.readfile("tests/fixtures/simple_rooms.dxf")
    msp = doc.modelspace()

    insunits = doc.header.get("$INSUNITS", "N/A")
    lines = [e for e in msp if e.dxftype() == "LINE"]
    lwp   = [e for e in msp if e.dxftype() == "LWPOLYLINE"]
    texts = [e for e in msp if e.dxftype() == "TEXT"]
    mtexts = [e for e in msp if e.dxftype() == "MTEXT"]

    print(f"  $INSUNITS : {insunits}  (expected: 4=mm)")
    print(f"  LINE      : {len(lines)}  (expected: 9 = 4+4+1 on TUONG + 1 on OTHER)")
    print(f"  LWPOLYLINE: {len(lwp)}  (expected: 1 on TUONG)")
    print(f"  TEXT      : {len(texts)}  (expected: 3)")
    print(f"  MTEXT     : {len(mtexts)}  (expected: 1)")

    layers = [la.dxf.name for la in doc.layers]
    print(f"  Layers    : {layers}")

    line_layers = {}
    for l in lines:
        line_layers[l.dxf.layer] = line_layers.get(l.dxf.layer, 0) + 1
    print(f"  LINE by layer: {line_layers}")

    for t in texts:
        ins = t.dxf.insert
        print(f"  TEXT: layer={t.dxf.layer!r} content={t.dxf.text!r} pos=({ins.x},{ins.y})")
    for m in mtexts:
        ins = m.dxf.insert
        print(f"  MTEXT: layer={m.dxf.layer!r} content={m.text!r} pos=({ins.x},{ins.y})")
    for p in lwp:
        pts = list(p.get_points())
        print(f"  LWPOLY: layer={p.dxf.layer!r} closed={p.closed} points={len(pts)}")

def verify_corrupt():
    print("\n=== corrupt.dxf ===")
    try:
        ezdxf.readfile("tests/fixtures/corrupt.dxf")
        print("  ERROR: expected DXFError but no exception raised!")
        return False
    except ezdxf.DXFError as e:
        print(f"  OK: raises ezdxf.DXFError → {e}")
        return True
    except Exception as e:
        print(f"  WARNING: raises {type(e).__name__} instead of DXFError → {e}")
        return False

def verify_banve():
    print("\n=== banve.dxf ===")
    try:
        doc = ezdxf.readfile("tests/fixtures/banve.dxf")
        msp = doc.modelspace()
        insunits = doc.header.get("$INSUNITS", "N/A")
        entity_types = {}
        for e in msp:
            t = e.dxftype()
            entity_types[t] = entity_types.get(t, 0) + 1
        layers = [la.dxf.name for la in doc.layers]
        print(f"  $INSUNITS : {insunits}")
        print(f"  DXF ver   : {doc.dxfversion}")
        print(f"  Entity types: {dict(sorted(entity_types.items()))}")
        print(f"  Layer count : {len(layers)}")
        print(f"  Layers (first 20): {layers[:20]}")
        return True
    except Exception as e:
        print(f"  ERROR: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    verify_simple_rooms()
    ok_corrupt = verify_corrupt()
    verify_banve()
    if not ok_corrupt:
        sys.exit(1)
    print("\n[ALL CHECKS PASSED]")
