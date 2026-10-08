# geojson-delivery-contract

Read-only delivery contracts for FeatureCollections: IDs, required fields, allowed geometry types, feature counts, dateline-aware bounds.

For gis data publishers delivering assets to a map application. A syntactically valid export can still ship duplicate IDs, missing application properties or coordinates outside the agreed delivery region.

## Install and first useful result

Python 3.10+; no runtime dependencies, accounts, API keys or network requests from the tool.
Installation may download setuptools from PyPI. No package has been published to a registry.

```sh
git clone https://github.com/nripankadas07/geojson-delivery-contract.git
cd geojson-delivery-contract
python -m venv .venv
# POSIX; Windows: .venv\Scripts\activate
. .venv/bin/activate
python -m pip install .
geojson-delivery-contract data.json contract.json
```

The included fixtures are synthetic. `python demo.py` prints the same real example.
CLI exit codes: 0 = accepted/unchanged, 1 = findings/changed, 2 = invalid input or read failure.
Reports are JSON. Input contracts are explicit; see the included JSON files for their schemas.
Use `--help` for arguments. Paths are local and UTF-8. The tool never writes input/output data.

## Check the implementation

```sh
python verify.py
```

Runs 10 meaningful unit checks, Python compilation, then installs this package into a
new virtual environment and exercises accepted, findings and invalid-input CLI cases outside
the source directory. CI repeats this on Python 3.10, 3.12 and 3.14.

## Limits

This is an application delivery gate, not full GeoJSON validation. GeometryCollection, null geometry/properties, topology, winding, ring closure, projections, bounding-box members and geometric repair are unsupported. Coordinate positions are checked but minimum vertex counts are not. Inputs are held in memory; duplicate JSON object members are not detected. Do not infer RFC conformance from a pass.

See [RESEARCH.md](RESEARCH.md) for the user brief, dated alternatives and tradeoffs;
[VALIDATION.md](VALIDATION.md) for observed check coverage and
[SUPPORT.md](SUPPORT.md) for contribution/security reporting. MIT licensed;
original implementation using the Python standard library, with no competitor code or prose copied.
