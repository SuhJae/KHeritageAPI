# Changelog

All notable changes to this project are documented in this file.

## [2.0.0] - 2026-03-01

### Breaking / Behavior Changes
- Reworked core models and parsing logic for stronger schema tolerance.
- Standardized package exports in `kheritageapi.__init__` and removed recursive import behavior.
- `HeritageSearcher` now uses HTTPS base endpoint by default.

### Added
- Compatibility parsing for legacy and current event schemas:
  - `sn` or `seqNo`
  - `siteName` or `subTitle`
  - `subDesc1` or `subDesc_2`
  - `subDesc2` or `subDesc_3`
- New optional heritage search filters:
  - `era_code` (`ccbaPcd1`)
  - `modified_start` (`stRegDt`)
  - `modified_end` (`enRegDt`)
- Additional `HeritageType` values from current docs (`55`, `66`).
- Comprehensive local tests and CI matrix.

### Fixed
- Event parsing breakage caused by upstream field-name changes.
- Fragile XML field access patterns that could throw on sparse payloads.
- Packaging metadata for modern PEP 621 builds.

### Migration Notes
- If you depended on implicit recursive import behavior from `kheritageapi`, switch to explicit imports from package exports.
- If you filtered by era/modified date via raw params previously, use `era_code`, `modified_start`, and `modified_end`.
- Event objects still keep compatibility fields (`audiance`, `etc`) and now also provide clearer aliases in `dict()` output.
