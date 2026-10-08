"""Check a deliberately narrow GeoJSON delivery contract, without modifying data."""
import argparse
import json
import math
from pathlib import Path

TYPES = {"Point": 0, "MultiPoint": 1, "LineString": 1, "MultiLineString": 2,
         "Polygon": 2, "MultiPolygon": 3}


def number(x):
    return type(x) in (int, float) and math.isfinite(x)


def positions(g, path):
    if not isinstance(g, dict) or g.get("type") not in TYPES:
        raise ValueError(path + ": unsupported geometry; six coordinate geometry types supported")
    def walk(v, depth, p):
        if not isinstance(v, list) or not v:
            raise ValueError(p + ": nonempty coordinate array required")
        if depth == 0:
            if len(v) not in (2, 3) or not all(number(x) for x in v):
                raise ValueError(p + ": finite 2D/3D position required")
            if not -180 <= v[0] <= 180 or not -90 <= v[1] <= 90:
                raise ValueError(p + ": longitude/latitude out of range")
            yield p, v
        else:
            for i, item in enumerate(v):
                yield from walk(item, depth - 1, p + "/" + str(i))
    yield from walk(g.get("coordinates"), TYPES[g["type"]], path + "/coordinates")


def check(data, contract):
    if not isinstance(contract, dict) or set(contract) - {"geometry_types", "required_properties", "id_property", "bounds", "min_features"}:
        raise ValueError("unknown contract option")
    allowed = contract.get("geometry_types", list(TYPES))
    required = contract.get("required_properties", [])
    key = contract.get("id_property")
    minimum = contract.get("min_features", 1)
    if not isinstance(allowed, list) or not allowed or any(t not in TYPES for t in allowed):
        raise ValueError("geometry_types must name supported types")
    if not isinstance(required, list) or any(not isinstance(x, str) or not x for x in required):
        raise ValueError("required_properties must be nonempty strings")
    if key is not None and (not isinstance(key, str) or not key):
        raise ValueError("id_property must be a nonempty string")
    if type(minimum) is not int or minimum < 0:
        raise ValueError("min_features must be a nonnegative integer")
    bounds = contract.get("bounds", [-180, -90, 180, 90])
    if not isinstance(bounds, list) or len(bounds) != 4 or not all(number(x) for x in bounds):
        raise ValueError("bounds must be four finite numbers")
    west, south, east, north = bounds
    if not (-180 <= west <= 180 and -180 <= east <= 180 and -90 <= south <= north <= 90):
        raise ValueError("bounds outside supported longitude/latitude range")
    if not isinstance(data, dict) or data.get("type") != "FeatureCollection" or not isinstance(data.get("features"), list):
        raise ValueError("FeatureCollection required")
    findings, seen, count = [], {}, 0
    if len(data["features"]) < minimum:
        findings.append({"path": "/features", "code": "feature_count"})
    for i, f in enumerate(data["features"]):
        path = "/features/" + str(i)
        if not isinstance(f, dict) or f.get("type") != "Feature" or not isinstance(f.get("properties"), dict):
            raise ValueError(path + ": Feature with object properties required by this contract")
        p = f["properties"]
        for name in required:
            if name not in p or p[name] is None:
                findings.append({"path": path + "/properties/" + name.replace("~", "~0").replace("/", "~1"), "code": "missing_property"})
        if key:
            value = p.get(key)
            if type(value) not in (str, int) or value == "":
                findings.append({"path": path, "code": "invalid_id"})
            elif (type(value).__name__, value) in seen:
                findings.append({"path": path, "code": "duplicate_id", "first_feature": seen[(type(value).__name__, value)]})
            else:
                seen[(type(value).__name__, value)] = i
        g = f.get("geometry")
        if isinstance(g, dict) and g.get("type") not in allowed:
            findings.append({"path": path + "/geometry", "code": "geometry_type"})
        for loc, pos in positions(g, path + "/geometry"):
            count += 1
            lon_ok = west <= pos[0] <= east if west <= east else pos[0] >= west or pos[0] <= east
            if not lon_ok or not south <= pos[1] <= north:
                findings.append({"path": loc, "code": "outside_delivery_bounds"})
    return {"ok": not findings, "features": len(data["features"]), "positions": count, "findings": findings}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("geojson"); ap.add_argument("contract")
    args = ap.parse_args()
    try:
        result = check(json.loads(Path(args.geojson).read_text(encoding="utf-8")), json.loads(Path(args.contract).read_text(encoding="utf-8")))
        print(json.dumps(result, sort_keys=True, allow_nan=False)); return 0 if result["ok"] else 1
    except (ValueError, OSError, RecursionError) as e:
        print(json.dumps({"error": str(e)})); return 2


if __name__ == "__main__":
    raise SystemExit(main())
