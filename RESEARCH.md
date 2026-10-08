# User brief and research — 8 October 2026

State: RESEARCHED → BUILDING.

User: GIS data publishers delivering assets to a map application.

Painful task: A syntactically valid export can still ship duplicate IDs, missing application properties or coordinates outside the agreed delivery region.

Smallest useful capability: Read-only delivery contracts for FeatureCollections: IDs, required fields, allowed geometry types, feature counts, dateline-aware bounds.

Demand is inferred from the documented workflows and review risks. No verified request for this product, adoption, performance advantage or exhaustive feature gap is claimed. Search and repository/README/code/issue reads occurred on 8 October 2026; current exact stars and last-push timestamps below are observations, not quality scores.

Queries: `geojson validation sort:stars; geojson in:name sort:stars`. Live GitHub search used `sort:stars`. Broad queries return unrelated repository/readme matches; irrelevant results were excluded. Coverage is limited, not an exhaustive global ranking. The highest-star relevant comparable among those examined is [mapbox/geojsonhint](https://github.com/mapbox/geojsonhint) at 257 stars.

| Comparable | Stars | Last push (UTC) | License | Workflow, setup, capabilities and tradeoffs |
|---|---:|---|---|---|
| [mapbox/geojsonhint](https://github.com/mapbox/geojsonhint) | 257 | 2024-05-28T13:50:42Z | ISC | Node CLI/API, informative JSON and coordinate diagnostics. Archived since 2024; README recommends a successor. A complete validator is broader than our delivery-contract subset. |
| [placemark/check-geojson](https://github.com/placemark/check-geojson) | 86 | 2025-02-18T14:08:30Z | MIT | TypeScript GeoJSON-string validation with parser locations. README marks API unstable and excludes precision/winding warnings. It checks structure; our contract adds explicit application delivery expectations. |
| [chrieke/geojson-validator](https://github.com/chrieke/geojson-validator) | 41 | 2026-08-02T16:33:31Z | MIT | Python package and web UI check structure/topology and repair geometries. Clear examples and typed API; broader geometry capability than our read-only subset. |

Reliability/support observations are limited to public docs, latest source and open issue samples; alternatives were not installed or benchmarked in this run. Examples prove our behavior only. No comparative speed, memory, accuracy or time-to-result measurement was made. Licenses are metadata observations; no competitor implementation/prose was reused.

Acceptance: documented clean install; accepted example; meaningful rejected/input-error examples; deterministic JSON reports; core invariants covered by the unit tests; all remote matrix checks must pass on the intended default head before LIVE. The exact scope/non-goals are in README.md.

Discovery path: relevant GitHub topics and a clear README/linked portfolio index. No messages or third-party issue advertising planned, and no organic growth promise.

Portfolio distinction: compared against all 143 existing repository names/descriptions and relevant CSV/HTTP/parser tools. This is not a fork or a variant of an existing launch. The five candidates address spatial delivery, cache deployment intent, CSP inheritance changes, crawler route expectations and cross-export identifier mapping respectively. masklink-audit does not reconcile numeric CSV differences like table-reconcile, transform data or copy a redaction engine. They are separate user tasks, not subdivisions of one product.

## Commit-linked observations

- [mapbox/geojsonhint source snapshot](https://github.com/mapbox/geojsonhint/tree/7d720095e3095680dbc675833646f4a52f08454e) — open issue sample: [#96](https://github.com/mapbox/geojsonhint/issues/96), [#95](https://github.com/mapbox/geojsonhint/issues/95), [#93](https://github.com/mapbox/geojsonhint/issues/93).
- [placemark/check-geojson source snapshot](https://github.com/placemark/check-geojson/tree/5701f8fe832c10793275c9174dd387829c4b4c7b) — open issue sample: [#30](https://github.com/placemark/check-geojson/issues/30), [#17](https://github.com/placemark/check-geojson/issues/17), [#16](https://github.com/placemark/check-geojson/issues/16).
- [chrieke/geojson-validator source snapshot](https://github.com/chrieke/geojson-validator/tree/75c59752233bcc90a4b9d0f9d0ea0b9630a48d4a) — open issue sample: [#10](https://github.com/chrieke/geojson-validator/issues/10), [#8](https://github.com/chrieke/geojson-validator/issues/8).

Standards consulted: [GeoJSON RFC 7946](https://www.rfc-editor.org/rfc/rfc7946.html), [HTTP caching RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html), [Robots RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html), [CSP3](https://www.w3.org/TR/CSP3/). Only the relevant standard informs each bounded tool; conformance is not claimed.
