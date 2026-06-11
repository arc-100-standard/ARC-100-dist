# /docs/00/model/

This directory exists to host `likec4.config.json`, the mkdocs-likec4 plugin's
discovery file. The actual `.c4` source files live at `architecture/LikeC4/`
in the repository root. This config is a thin pointer; do not put diagrams or
prose here.

`<PROJECT>-100` projects inherit this layout from the ARC-100 standard via
ARC-100-SYNC's `install.sh` (phase 4a deliverable). The upstream ARC-100
project itself uses a per-tree LikeC4 toolchain split (phase 3.1d:
`master-vault/likec4/` for the standard, `docs/likec4/` for the project) that
downstreams do NOT inherit — the singleton `architecture/LikeC4/` layout is
the downstream-facing standard (V1_STRATEGY §7A item 9).
