"""MkDocs hook: generate ARC-100 index landing pages from YAML.

Usage
-----
Registered by `mkdocs.arc100.yml` (red site, inventory mode) and
`mkdocs.arc100project.yml` (green site, index mode). The hook reads
`extra.arc100_render_mode` from the mkdocs config to choose between
the two modes:

- **inventory** (red site, default): renders the standard's prescribed
  slots only. Source: `<docs_dir>/00-01_ARC-100_Standard_Inventory.md`.
  Markers: `<!-- ARC-100-INDEX-START -->` / `END`. Generated home:
  `<docs_dir>/index.md`. Chapter files at docs_dir root.

- **index** (green site): renders the project's comprehensive index
  including Book 00 inherited rows + Book 01/02/10+ project rows.
  Source: `<docs_dir>/01/01-01_ARC-100-Project_Index.md`. Markers:
  `<!-- ARC-100-PROJECT-INDEX-START -->` / `END`. Generated home:
  `<docs_dir>/01/index.md`. Chapter files under per-book subfolders.

The hook is a no-op when its mode's source file is not present, so
either site can safely run the same hook registration without falling
over if the source is missing.

Layout assumptions
------------------
- Red site `docs_dir` = `master-vault/docs/00/` (post-phase-3.1b
  flatten). Chapter files sit at docs_dir root.
- Green site `docs_dir` = `docs/`. Chapter files sit under per-book
  subfolders: `01/`, `02/`, `10/`, ...

Mechanism (both modes)
----------------------
1. `on_pre_build` resolves the render mode and dispatches.
2. Each mode reads its source file and extracts YAML between its
   marker pair.
3. Renders the shared three-level HTML tree (band -> book -> chapter).
4. Renders the per-mode page wrapper (title + intro prose) and writes
   the generated home file (idempotent: only writes when content changed).
5. Overrides mkdocs `config['nav']` with the per-mode nav shape.

YAML schema (both modes)
------------------------
Top-level keys:

- `arc_100_version`: e.g. "100.1"
- `active_version`: slug of the active version, or null
- `bands`: list of `{range, title, description, unallocated_book_slots}`
- `books`: list of `{id, title, band, chapters: [...]}` — each book is a
  first-level container. The legacy key `chapters:` (with `sub_chapters:`
  nested) is also accepted for backwards compatibility.

Each chapter has `{id, title, status, location?, description, keywords?,
source_master_revision?}`.

The generated index files are gitignored — they are derivatives of the
source files and will be regenerated on every `mkdocs serve` rebuild.
"""

from __future__ import annotations

import re
from html import escape as h
from pathlib import Path

import yaml

# Repo root anchored on the hook file's own location: this module lives
# at `_hooks/arc100_master_index.py`, a fixed child of the worktree
# root. Resolving __file__ and walking .parent twice (through _hooks/
# then to the worktree root) gives an unambiguous anchor — no
# ancestor-walk, no `.git/` probing.
_REPO_ROOT = Path(__file__).resolve().parent.parent
_SHARED_ASSETS_SRC = _REPO_ROOT / "assets" / "arc100"

# Inventory mode (red site) — source at docs_dir root.
_INVENTORY_SOURCE = "00-01_ARC-100_Standard_Inventory.md"
_INVENTORY_HOME = "index.md"

# Index mode (green site) — the source under docs_dir/01/ is convention-derived
# per project in _build_project_index (01/01-01_<scheme_name>_Index.md); the hook
# output goes to docs_dir root so green and red have symmetric "/" canonical URLs.
# Phase 3.1c brings forward phase 3.1e's green-site root-index move.
_PROJECT_INDEX_HOME = "index.md"

def _build_marker_regex(marker_base: str) -> re.Pattern[str]:
    """Build the YAML-block-extraction regex for a marker pair.

    marker_base e.g. "ARC-100-INDEX" (ARC-100 Project inventory mode),
    "ARC-100-PROJECT-INDEX" (ARC-100 Project index mode), or
    "FLOW-100-INDEX" (downstream FLOW-100 index mode). Matches:

        <!-- {marker_base}-START -->
        ```yaml
        ...
        ```
        <!-- {marker_base}-END -->

    Mirrors arc_sync.py's extract_yaml regex for byte-shape
    parity with the sync engine. Replaces the two pre-D1 module-level
    constants (_MARKER_INVENTORY_RE / _MARKER_PROJECT_RE) so the marker
    base can be derived per-build from project_name (phase 4b D1).
    """
    start = re.escape(f"<!-- {marker_base}-START -->")
    end = re.escape(f"<!-- {marker_base}-END -->")
    return re.compile(rf"{start}\s*\n```yaml\n(.*?)\n```\s*\n{end}", re.DOTALL)

_BANNER_TEMPLATE = """<div class="arc100-critical-banner" markdown="1">

## CRITICAL {project_name} INDEX DECISIONS NEEDED

The ARC-100 conformance tool has queued one or more decisions that
require human judgment. Run `/resolve-arc-100-issues` in Claude Code
to begin guided resolution.

See `.arc100/PENDING-INDEX-DECISIONS.yml` for the queued decisions; set each `decision:` to accept or reject, then re-run the sync to apply.

</div>

"""


def _apply_critical_banner(home_md: str, repo_root: Path, project_name: str) -> str:
    """Return home_md with a critical-decisions banner prepended if the
    transient decision file `.arc100/PENDING-INDEX-DECISIONS.yml` is present
    at repo_root (the `--target` root).

    Detection is by file PRESENCE only — arc_sync.py writes the file solely
    on escalation and archives + unlinks it on resolution, so its mere
    existence is the whole signal (no YAML parse, no status field).

    The banner inserts after the closing front-matter `---` and before
    the first H1. If no front-matter is present, the banner goes at the top.
    """
    pending = repo_root / ".arc100" / "PENDING-INDEX-DECISIONS.yml"
    if not pending.exists():
        return home_md
    # TM-4b-6: escape inside the helper so future call sites cannot
    # reintroduce the gap. .format() into rendered HTML is an injection
    # sink equivalent to a bare f-string substitution; pre-D1 this was
    # safe because project_name was a literal — post-D1 the value flows
    # from downstream-owned ARC-100-SYNC.config.yml.
    banner = _BANNER_TEMPLATE.format(project_name=h(project_name))
    parts = home_md.split("---", 2)
    if len(parts) >= 3 and parts[0].strip() == "":
        return f"---{parts[1]}---\n\n{banner}{parts[2].lstrip()}"
    return banner + home_md


def _load_project_name(project_root: Path, mode: str) -> str:
    """Read project_name (the marker SCHEME name) from
    ARC-100-SYNC.config.yml if present; else return the default "ARC-100".

    The scheme name is what arc_sync.py composes markers from
    (`f"{scheme_name}-INDEX-START"`). It differs from the user-facing
    DISPLAY name when ARC-100 renders its own in-repo project:

      ARC-100 standard (no config at master-vault/docs/):
        scheme_name = "ARC-100"  → markers "ARC-100-INDEX-{START,END}"
        display     = "ARC-100" Master Index (red site, inventory)

      ARC-100 Project (config at repo root sets project_name "ARC-100-PROJECT"):
        scheme_name = "ARC-100-PROJECT"
          → markers "ARC-100-PROJECT-INDEX-{START,END}"
          (the "-PROJECT" infix distinguishes ARC-100 Project's index
           source from the standard's inventory source on disk; both
           rendered under display name "ARC-100")
        display     = "ARC-100 Project Index" (green site, index)

      FLOW-100 downstream (config sets project_name "FLOW-100"):
        scheme_name = "FLOW-100" → markers "FLOW-100-INDEX-{START,END}"
        display     = "FLOW-100 Index" (single site, index)

    Caller (_build_project_index) extracts the display name by stripping
    a trailing "-PROJECT" from scheme_name, and uses that suffix as the
    is_arc100_project discriminator for the "Project" word in the rendered
    title.

    Narrow catch: parse / IO / decode failures fall back to the default.
    Programming errors (NameError, AttributeError, TypeError) deliberately
    propagate so they surface during ARC-100's own build instead of
    silently returning the default and producing confusing output.

    TM-4b-1: yaml.safe_load is the only YAML call (matches the hook's
    existing index-block parses and arc_sync.py's extract_yaml).
    """
    # mode is accepted for call-site symmetry (inventory vs index) but
    # the default scheme name is the same: "ARC-100".
    del mode  # explicit non-use
    default = "ARC-100"
    config_path = project_root / "ARC-100-SYNC.config.yml"
    if not config_path.exists():
        return default
    try:
        data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        name = data.get("project_name")
        if isinstance(name, str) and name.strip():
            return name.strip()
    except (yaml.YAMLError, OSError, UnicodeDecodeError):
        pass
    return default


def _load_project_display_name(project_root: Path) -> str | None:
    """Read project_display_name (the human-readable name) from
    ARC-100-SYNC.config.yml if present; else return None.

    Phase 5b D1: the rendered home-page title prefers this literal name
    over the marker SCHEME name (project_name). It is downstream-owned
    free-form text written by the installer as an escaped YAML scalar, so
    the only safe parse is yaml.safe_load (matches the sibling loaders).

    Returns None when the config is absent or the key is unset/empty so
    the caller falls back to the scheme-derived name — this is what keeps
    the 5a greenfield title ("TEST-100 Index") rendering when no display
    name is set (Stop Condition 1).
    """
    config_path = project_root / "ARC-100-SYNC.config.yml"
    if not config_path.exists():
        return None
    try:
        data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        raw = data.get("project_display_name")
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    except (yaml.YAMLError, OSError, UnicodeDecodeError):
        pass
    return None


def _load_local_index_path(project_root: Path) -> str | None:
    """Read local_index_path from ARC-100-SYNC.config.yml if present.

    Returns the raw string (caller resolves it relative to project_root,
    matching arc_sync.py which treats local_index_path as repo-root-
    relative against CWD = repo root). Returns None when the config is
    absent or the key is unset/empty — caller falls back to the
    docs_dir-relative working-index default parameterized from the scheme
    project_name (01/01-01_<scheme_name>_Index.md; convention-derivation).

    Joining local_index_path to docs_dir would double-prefix "docs/"
    (a downstream's "docs/00/00-01_…" would become "docs/docs/00/…");
    the project-root base is deliberate and must not be conflated with
    the derived default's docs_dir base.
    """
    config_path = project_root / "ARC-100-SYNC.config.yml"
    if not config_path.exists():
        return None
    try:
        data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        raw = data.get("local_index_path")
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    except (yaml.YAMLError, OSError, UnicodeDecodeError):
        pass
    return None


def _load_local_general_path(project_root: Path) -> str | None:
    """Read local_general_path from ARC-100-SYNC.config.yml if present.

    Optional sibling of local_index_path: the project-root-relative
    source path for the home page's "General introduction" sentence.
    Returns None when the config is absent or the key is unset/empty —
    the caller then omits the sentence entirely (downstream-safe, so a
    downstream that does not author this key gets no dangling link).
    """
    config_path = project_root / "ARC-100-SYNC.config.yml"
    if not config_path.exists():
        return None
    try:
        data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        raw = data.get("local_general_path")
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    except (yaml.YAMLError, OSError, UnicodeDecodeError):
        pass
    return None


def _load_local_chapter_root(project_root: Path) -> str:
    """Read local_chapter_root from ARC-100-SYNC.config.yml if present.

    Returns the configured chapter-root prefix (e.g. "docs") that, when
    stripped from a project-root-relative source path, yields the
    docs_dir-relative target used in generated links. Returns "" when
    the config is absent or the key is unset/empty (a downstream that
    omits it) — in that case nothing is stripped.
    """
    config_path = project_root / "ARC-100-SYNC.config.yml"
    if not config_path.exists():
        return ""
    try:
        data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        raw = data.get("local_chapter_root")
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    except (yaml.YAMLError, OSError, UnicodeDecodeError):
        pass
    return ""


def _strip_chapter_root(local_path: str, chapter_root: str) -> str:
    """Strip the chapter-root prefix from a project-root-relative path.

    Converts a config source path (e.g. "docs/01/01-01_…Index.md") into
    the docs_dir-relative target used in generated links
    (e.g. "01/01-01_…Index.md"). Only strips a leading segment when it
    matches `chapter_root`; an absent/empty chapter_root (downstream
    that omits the key) strips nothing.
    """
    if chapter_root:
        prefix = chapter_root.rstrip("/") + "/"
        if local_path.startswith(prefix):
            return local_path[len(prefix):]
    return local_path


def _resolve_render_mode(config) -> str:
    """Return the render mode for this build.

    Reads `extra.arc100_render_mode` from the mkdocs config; defaults
    to "inventory" if absent (preserves the pre-revision-4 single-mode
    behaviour for any config that hasn't declared a mode).
    """
    return config.get("extra", {}).get("arc100_render_mode", "inventory")


def on_pre_build(config, **kwargs):  # noqa: ARG001
    mode = _resolve_render_mode(config)
    if mode == "inventory":
        _build_inventory(config)
    elif mode == "index":
        _build_project_index(config)
    else:
        raise ValueError(
            f"Unknown arc100_render_mode: {mode!r} "
            "(expected 'inventory' or 'index')"
        )


def _build_inventory(config) -> None:
    """Render the standard's inventory page (red site).

    Source: `<docs_dir>/00-01_ARC-100_Standard_Inventory.md`. The hook
    is a no-op if the source is missing — keeps the registration safe
    across configs that don't expect inventory mode.
    """
    docs_dir = Path(config["docs_dir"])
    source = docs_dir / _INVENTORY_SOURCE
    if not source.exists():
        return

    _copy_shared_assets(docs_dir)

    project_root = docs_dir.parent
    project_name = _load_project_name(project_root, "inventory")
    marker_base = f"{project_name}-INDEX"
    marker_re = _build_marker_regex(marker_base)

    content = source.read_text(encoding="utf-8")
    match = marker_re.search(content)
    if not match:
        raise ValueError(
            f"{marker_base} markers not found in {source}. "
            f"The hook expects <!-- {marker_base}-START --> ... "
            f"<!-- {marker_base}-END --> bracketing a ```yaml block."
        )
    data = yaml.safe_load(match.group(1))

    counts = _count_statuses(data)
    # Inventory mode: chapter files at docs_dir root — book_id is
    # informational only (label resolution); the file lookup ignores it.
    tree_html = _render_tree(data, docs_dir, mode="inventory")
    page = _render_page_inventory(data, tree_html, counts, project_name)

    # project_root is already docs_dir.parent (the --target root). The standard's
    # own render is never a sync --target, so .arc100/ never exists here and this
    # banner is a permanent no-op.
    page = _apply_critical_banner(page, project_root, project_name=project_name)

    out = docs_dir / _INVENTORY_HOME
    _write_if_changed(out, page)
    config["nav"] = _build_nav_inventory(data, docs_dir)


def _build_project_index(config) -> None:
    """Render the project's comprehensive index page (green site).

    Source: `<docs_dir>/01/01-01_ARC-100-Project_Index.md`. The hook
    is a no-op if the source is missing.
    """
    docs_dir = Path(config["docs_dir"])

    # Q2: index-mode source is config-aware. local_index_path resolves
    # against project_root (= docs_dir.parent) to match arc_sync.py's
    # repo-root-relative convention; default falls back to the docs_dir-
    # relative working-index default below. Joining local_index_path
    # to docs_dir would double-prefix "docs/" — see _load_local_index_path.
    project_root = docs_dir.parent
    # Convention-derivation (hook-side half; mirrors arc_sync.py load_config):
    # when the config omits local_index_path / local_chapter_root, derive them
    # from the scheme project_name. scheme_name is loaded ONCE here (reused for
    # the display-name / marker-base derivation below — NOT a second
    # _load_project_name call, which would change the red/no-config contract).
    # project_index_default parameterizes the canonical 01/01-01 slot's name
    # segment per project: a hardcoded "ARC-100-Project" name would be wrong for
    # a downstream like FLOW-100, whose working index is 01/01-01_FLOW-100_Index.md.
    scheme_name = _load_project_name(project_root, "index")
    project_index_default = f"01/01-01_{scheme_name}_Index.md"  # docs_dir-relative
    local_index_path = _load_local_index_path(project_root)
    if local_index_path is not None:
        source = project_root / local_index_path
    else:
        source = docs_dir / project_index_default
    if not source.exists():
        return

    _copy_shared_assets(docs_dir)

    # Resolve the config's scheme project_name (used by arc_sync.py to
    # compose markers as f"{scheme_name}-INDEX") and derive the
    # user-facing display name + the ARC-100-Project flag:
    #
    #   ARC-100 Project:    scheme_name = "ARC-100-PROJECT"
    #                       display    = "ARC-100"      (suffix stripped)
    #                       is_arc100_project = True    (suffix detected)
    #
    #   ARC-100 standard:   scheme_name = "ARC-100"     (default; no config exists
    #                                                    at master-vault/docs/)
    #                       display    = "ARC-100"
    #                       is_arc100_project = False
    #
    #   FLOW-100 downstream: scheme_name = "FLOW-100"
    #                        display    = "FLOW-100"
    #                        is_arc100_project = False
    #
    # The "-PROJECT" suffix is the unique discriminator: it appears
    # only in ARC-100's own in-repo-project scheme_name (deliberately,
    # so arc_sync.py's marker base "ARC-100-PROJECT-INDEX" distinguishes
    # ARC-100 Project's index source file from the standard's inventory
    # source file on disk — same project_name "ARC-100" rendered as
    # two sites). A downstream's scheme_name never carries the suffix
    # (its single site needs no on-disk differentiation from itself).
    # scheme_name was resolved above (convention-derivation needs it before the
    # source resolution); derive the display name + ARC-100-Project flag from it.
    is_arc100_project = scheme_name.endswith("-PROJECT")
    project_name = scheme_name[: -len("-PROJECT")] if is_arc100_project else scheme_name
    # Phase 5b D1: the rendered home-page title prefers the human-readable
    # project_display_name over the scheme-derived name. Absent -> fall back
    # to project_name, so a greenfield install with no display name still
    # renders "<scheme> Index" (Stop Condition 1 / 5a gate). The display name
    # feeds ONLY the title text in _render_page_project; the -PROJECT-strip /
    # " Project" discriminator above (and the marker_base below) stay on the
    # scheme name.
    display_name = _load_project_display_name(project_root) or project_name
    marker_base = f"{scheme_name}-INDEX"
    marker_re = _build_marker_regex(marker_base)

    content = source.read_text(encoding="utf-8")
    match = marker_re.search(content)
    if not match:
        raise ValueError(
            f"{marker_base} markers not found in {source}. "
            f"The hook expects <!-- {marker_base}-START --> ... "
            f"<!-- {marker_base}-END --> bracketing a ```yaml block."
        )
    data = yaml.safe_load(match.group(1))

    counts = _count_statuses(data)
    # Index mode: chapter files sit under docs_dir/<book_id>/ — the
    # tree-render resolves each chapter URL relative to the generated
    # home at docs_dir/01/index.md.
    tree_html = _render_tree(data, docs_dir, mode="index")

    # Derive the home-page index/general pointers from config so they
    # resolve for any downstream (not just the dogfood's Book-01 tree).
    # local_index_path / local_general_path are project-root-relative;
    # stripping local_chapter_root yields the docs_dir-relative target,
    # and the basename is the link's display text. local_general_path is
    # optional — None omits the "General introduction" sentence.
    # Convention default: an absent local_chapter_root falls to "docs" (mirrors
    # arc_sync.py load_config; matches the dogfood — NOT scheme_name).
    chapter_root = _load_local_chapter_root(project_root) or "docs"
    index_link_target = (
        _strip_chapter_root(local_index_path, chapter_root)
        if local_index_path is not None
        else project_index_default
    )
    index_link_display = Path(index_link_target).name
    local_general_path = _load_local_general_path(project_root)
    if local_general_path is not None:
        general_link_target = _strip_chapter_root(local_general_path, chapter_root)
        general_link_display = Path(general_link_target).name
    else:
        general_link_target = None
        general_link_display = None

    page = _render_page_project(
        data,
        tree_html,
        counts,
        display_name,  # title prefers project_display_name; falls back to scheme name
        is_arc100_project,
        index_link_target=index_link_target,
        index_link_display=index_link_display,
        general_link_target=general_link_target,
        general_link_display=general_link_display,
    )

    # .arc100/ sits at the --target root (= docs_dir.parent when docs_dir is
    # "docs"), not under docs_dir; pass the repo root so the presence probe
    # resolves. (Pre-3a this passed docs_dir — the green-site probe bug.)
    page = _apply_critical_banner(page, docs_dir.parent, project_name=project_name)

    out = docs_dir / _PROJECT_INDEX_HOME
    _write_if_changed(out, page)
    config["nav"] = _build_nav_project(data, docs_dir, is_arc100_project)


def _write_if_changed(out: Path, content: str) -> None:
    """Idempotent write: mkdocs serve watches docs_dir, so writing
    unconditionally would cause the watcher to fire on the generated
    file, re-trigger this hook, and loop forever. Only write when the
    content has actually changed.
    """
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists() or out.read_text(encoding="utf-8") != content:
        out.write_text(content, encoding="utf-8")


def _copy_shared_assets(docs_dir: Path) -> None:
    """Copy `<repo_root>/assets/arc100/**` into `<docs_dir>/assets/arc100/`.

    Phase 3.1c D0 split: master-vault now carries its own tracked
    source tree at `master-vault/docs/00/assets/arc100/`. This helper
    only writes for the green site; master-vault is self-managed.

    Idempotent byte-compare gate: skip the write when source and
    destination already match. Without this gate mkdocs serve's
    docs_dir watcher would re-fire on every copy, triggering an
    infinite build loop.
    """
    if not _SHARED_ASSETS_SRC.exists():
        return
    # D0 (phase 3.1c): skip the red site. Master-vault's copy at
    # `master-vault/docs/00/assets/arc100/` is the production-of-
    # record version, tracked in git. Copying from the project
    # source (`assets/arc100/`, repo root, which is the in-flight
    # ARC-100 Project copy) would clobber it.
    master_vault_docs = (_REPO_ROOT / "master-vault" / "docs" / "00").resolve()
    if docs_dir.resolve() == master_vault_docs:
        return
    dst_dir = docs_dir / "assets" / "arc100"
    for src in _SHARED_ASSETS_SRC.rglob("*"):
        if not src.is_file():
            continue
        rel = src.relative_to(_SHARED_ASSETS_SRC)
        dst = dst_dir / rel
        src_bytes = src.read_bytes()
        if dst.exists() and dst.read_bytes() == src_bytes:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src_bytes)


def on_serve(server, config, builder, **kwargs):  # noqa: ARG001
    """Register the canonical shared-assets directory with the
    mkdocs-serve watcher so edits to `<repo_root>/assets/arc100/**`
    livereload on both sites. Each canonical edit fires the build,
    which runs `_copy_shared_assets`, which writes the new bytes into
    `<docs_dir>/assets/arc100/**`, which fires the docs_dir watcher,
    which reaches the browser.
    """
    if _SHARED_ASSETS_SRC.exists():
        server.watch(str(_SHARED_ASSETS_SRC))
    return server


def _books(data) -> list:
    """Return the list of books, accepting either the new `books:` key or
    the legacy `chapters:` key during the rename transition."""
    return data.get("books") or data.get("chapters") or []


def _chapters(book) -> list:
    """Return chapters under a book, accepting either `chapters:` (new) or
    `sub_chapters:` (legacy)."""
    return book.get("chapters") or book.get("sub_chapters") or []


def _normalize_status(raw: str) -> str:
    """Map raw status to a CSS-class-friendly bucket.

    `checked-out-to-vN` collapses to `checked-out`; everything else is
    returned unchanged.
    """
    if raw.startswith("checked-out-to-"):
        return "checked-out"
    return raw


def _count_statuses(data) -> dict[str, int]:
    counts = {
        "active": 0,
        "draft": 0,
        "placeholder": 0,
        "checked-out": 0,
        "superseded": 0,
        "deprecated": 0,
        "other": 0,
    }
    for book in _books(data):
        for chapter in _chapters(book):
            bucket = _normalize_status(chapter.get("status", "other"))
            counts[bucket] = counts.get(bucket, 0) + 1
    return counts


def _chapter_count_phrase(n: int) -> str:
    """Just the integer — the word 'chapters' is rendered once per band
    in the band-title row as a column header (see _render_tree)."""
    return str(n)


def _data_desc_attr(text: str | None) -> str:
    """Render a ` data-description="…"` attribute (with leading space) for
    consumption by the right-column hover overlay in arc100.js. Returns
    an empty string when text is missing — the JS treats absence of the
    attribute as 'no overlay for this row'."""
    if not text:
        return ""
    return f" data-description=\"{h(text)}\""


def _data_desc_label_attr(text: str | None) -> str:
    """Render a ` data-desc-label="…"` attribute consumed by arc100.js
    as the small red heading above the description body. The hook
    pre-formats the label per row type (see _band_label / _book_label /
    _chapter_label) so the JS never has to reconstruct identifiers."""
    if not text:
        return ""
    return f" data-desc-label=\"{h(text)}\""


def _band_label(band_range: str) -> str:
    """Human-readable band label for the overlay heading. `00-09`
    becomes `Band 00 thru 09` — the literal hyphen would look like a
    chapter id (e.g. `00-09`) and miscue readers as 'chapter 9 of book
    00' rather than a band range."""
    return f"Band {band_range.replace('-', ' thru ')}" if band_range else "Band"


def _book_label(book_id: str) -> str:
    return f"Book {book_id}" if book_id else "Book"


def _chapter_label(chapter_id: str) -> str:
    return f"Chapter {chapter_id}" if chapter_id else "Chapter"


def _book_id_from_chapter(chapter_id: str) -> str:
    """Extract the book-id prefix from a chapter id (e.g. "01-03" -> "01").
    Returns empty string for malformed ids."""
    if "-" not in chapter_id:
        return ""
    return chapter_id.split("-", 1)[0]


def _chapter_file_md(docs_dir: Path, chapter_id: str, mode: str) -> str | None:
    """Return the chapter's `.md` path relative to docs_dir, or None if
    no file matches.

    - inventory mode: chapter files sit at docs_dir root (the red site's
      docs_dir IS the book-00 folder post-D0.2 flatten). Glob at docs_dir
      and return the bare filename.
    - index mode: chapter files sit under docs_dir/<book_id>/, where
      book_id is the chapter id's prefix (e.g. "01" for "01-03"). Glob in
      the book subfolder and return "<book_id>/<filename>".
    """
    if not chapter_id:
        return None
    if mode == "inventory":
        matches = list(docs_dir.glob(f"{chapter_id}_*.md"))
        if len(matches) == 1:
            return matches[0].name
        return None
    # index mode
    book_id = _book_id_from_chapter(chapter_id)
    if not book_id:
        return None
    book_dir = docs_dir / book_id
    matches = list(book_dir.glob(f"{chapter_id}_*.md"))
    if len(matches) == 1:
        return f"{book_id}/{matches[0].name}"
    return None


def _chapter_file_url(docs_dir: Path, chapter_id: str, mode: str) -> str | None:
    """Return the URL for an active chapter relative to the generated
    index page, or None if no matching file exists.

    Both mkdocs configs use `use_directory_urls: true` (set in phase 3.1c
    for URL consistency), so a file like `01-03_*.md` is served at
    `.../01-03_*/` (no `.html` suffix; mkdocs writes `01-03_*/index.html`
    and routes the directory URL to it).

    - inventory mode: generated index sits at docs_dir/index.md (root);
      chapter files are siblings. URL is the bare filename stem followed
      by a trailing slash.
    - index mode (post-phase-3.1c): generated index also sits at
      docs_dir/index.md (root); chapter files live under `<book_id>/`
      sub-directories. URL is `<book_id>/<filename-stem>/`.
    """
    md = _chapter_file_md(docs_dir, chapter_id, mode)
    if not md:
        return None
    if mode == "inventory":
        return md[:-3] + "/"
    # index mode — md is "<book_id>/<filename>.md"; the generated index
    # also sits at docs_dir root, so the relative URL is the md path
    # with .md → /.
    return md[:-3] + "/"


def _build_nav_inventory(data, docs_dir: Path) -> list:  # noqa: ARG001
    """Emit the top-level mkdocs nav for the red (inventory) site.

    Structure:

        - Master Index: index.md             (the generated chapter tree)
        - Architectural Model: architectural-model.md  (LikeC4 entry view)
        - Getting Started: 00-07_ARC-100_Getting_Started.md  (onboarding chapter)

    Post-D0 the red docs_dir is `master-vault/docs/00/`; phase 3.1b
    revision 4 (D0.5) relocated `architectural-model.md` into this
    docs_dir, so it sits as a sibling of the generated `index.md`.

    `Getting Started` is the one Book 00 chapter promoted to a top-level
    nav entry (it is also reachable as a row in the Master Index tree like
    every other chapter): it is the a-priori onboarding doc, so it earns a
    prominent left-column shortcut. It still matches the `not_in_nav`
    `/00-*.md` glob in the mkdocs config, which is harmless — a page that
    IS in the nav is simply not subject to the orphan-file check, and
    `--strict` accepts the overlap (verified: red site builds clean with
    00-07 both in the nav and matched by the glob).

    The other chapter pages (`00-NN_*.md`) are intentionally NOT listed in
    the sidebar — they are discoverable via the Master Index tree; the
    `not_in_nav` glob silences the strict-mode orphan-file warnings the
    explicit omission would otherwise trigger.
    """
    return [
        {"Master Index": _INVENTORY_HOME},
        {"Architectural Model": "architectural-model.md"},
        {"Getting Started": "00-07_ARC-100_Getting_Started.md"},
    ]


def _build_nav_project(data, docs_dir: Path, is_arc100_project: bool) -> list:  # noqa: ARG001
    """Emit the single-item top-level mkdocs nav for the index site.

    Structure (ARC-100 Project):    [{"Project Index": "index.md"}]
    Structure (downstream / standard): [{"Index":         "index.md"}]

    The "Project" differentiator matches the rendered title's
    differentiator (see _render_page_project): ARC-100 Project gets
    one, every downstream and the standard's inventory get none.

    Phase 3.1b note: the plan's §6.5 narrative anticipated a second
    "Architectural Model" entry mirroring the red-site shape, but
    `docs/architectural-model.md` does not exist (phase 3.1a left the
    file at `master-vault/docs/architectural-model.md`; phase 3.1b D0.5
    relocated it to `master-vault/docs/00/architectural-model.md` —
    inside the red docs_dir only). The green tree gains its own
    architectural-model surface in phase 3.1d (V1_STRATEGY §6.8) once
    the project tree has its own scoped LikeC4 install + DSL.

    Chapter pages (`01/01-NN_*.md`, `02/02-NN_*.md`, `10/10-NN_*.md`,
    etc.) are intentionally NOT listed in the sidebar — they are
    discoverable via the Index tree. The `not_in_nav` glob in the
    mkdocs config silences the strict-mode orphan-file warnings.
    """
    label = "Project Index" if is_arc100_project else "Index"
    return [
        {label: _PROJECT_INDEX_HOME},
    ]


def _render_tree(data, docs_dir: Path, mode: str) -> str:
    """Emit the tree as plain `<div>`s with bare class names scoped under
    `.arc100-tree`. No `<details>` / `<summary>` / `<ul>` / `<li>`: the
    semantic elements drag in browser-default margins that fight the
    tight-row visual. Collapse is driven by `data-open` and JS.

    Active chapters with a matching file in `docs_dir` are rendered as
    `<a class="chapter" href="...">` so the entire row is a navigation
    link. Non-active rows stay as `<div class="chapter">`.

    The `mode` parameter ("inventory" or "index") drives
    `_chapter_file_url` resolution per the layout differences documented
    on that helper.
    """
    bands = data.get("bands", [])
    books_by_band: dict[str, list] = {}
    for book in _books(data):
        books_by_band.setdefault(book.get("band", ""), []).append(book)

    parts: list[str] = ["<div class=\"arc100-tree\">"]
    for band in bands:
        band_range = band.get("range", "")
        parts.append(f"<div class=\"band\" data-band=\"{h(band_range)}\">")
        band_desc_attr = _data_desc_attr(band.get("description"))
        band_label_attr = _data_desc_label_attr(_band_label(band_range))
        parts.append(
            f"<div class=\"band-title\"{band_desc_attr}{band_label_attr}>"
            f"<span class=\"title\">{h(band.get('title', ''))}</span>"
            "<span class=\"count-label\">chapters</span>"
            "</div>"
        )
        for book in books_by_band.get(band_range, []):
            book_id = h(book.get("id", ""))
            book_title = h(book.get("title", ""))
            chapters = _chapters(book)
            count_phrase = _chapter_count_phrase(len(chapters))
            # D1.4 (phase 3.1c): in `index` render mode (the project /
            # green site), emit Book 00 books with inline display:none
            # and a marker attribute so JS can find them on init. This
            # eliminates the first-paint FOUC before the localStorage-
            # gated visibility toggle applies the default-hidden state.
            # Discriminator is the book id literal "00" — in the project
            # YAML, books 01/02/10/... also carry arc_100: true (the
            # whole project IS an ARC-100 instance), so the arc_100 flag
            # alone over-selects.
            book_book00_attrs = (
                ' style="display:none" data-book00-default-hidden="true"'
                if mode == "index" and book.get("id") == "00"
                else ""
            )
            parts.append(
                f"<div class=\"book\" data-book-id=\"{book_id}\" data-open=\"false\"{book_book00_attrs}>"
            )
            book_id_raw = book.get("id", "")
            book_desc_attr = _data_desc_attr(book.get("description"))
            book_label_attr = _data_desc_label_attr(_book_label(book_id_raw))
            book_arc_100_badge = (
                '<span class="arc-100-badge">ARC-100</span>'
                if book.get("arc_100")
                else ""
            )
            parts.append(
                "<div class=\"book-title\""
                " role=\"button\""
                " tabindex=\"0\""
                f" aria-controls=\"book-{book_id}-chapters\""
                f"{book_desc_attr}"
                f"{book_label_attr}"
                ">"
                f"<span class=\"id\">{book_id}</span>"
                f"<span class=\"title\">{book_title}</span>"
                f"{book_arc_100_badge}"
                f"<span class=\"count\">{count_phrase}</span>"
                "</div>"
            )
            parts.append(
                f"<div class=\"chapters\" id=\"book-{book_id}-chapters\">"
            )
            for chapter in chapters:
                ch_id_raw = chapter.get("id", "")
                ch_id = h(ch_id_raw)
                ch_title = h(chapter.get("title", ""))
                status_raw = chapter.get("status", "other")
                status_class = _normalize_status(status_raw)
                desc = h(chapter.get("description", ""))
                badge = (
                    ""
                    if status_class == "active"
                    else f"<span class=\"status\">{h(status_raw.upper())}</span>"
                )
                arc_100_badge = (
                    '<span class="arc-100-badge">ARC-100</span>'
                    if chapter.get("arc_100")
                    else ""
                )
                url = (
                    _chapter_file_url(docs_dir, ch_id_raw, mode)
                    if status_class == "active"
                    else None
                )
                desc_attr = _data_desc_attr(chapter.get("description"))
                label_attr = _data_desc_label_attr(_chapter_label(ch_id_raw))
                if url:
                    open_tag = (
                        f"<a class=\"chapter\" href=\"{h(url)}\""
                        f" data-status=\"{h(status_class)}\""
                        f" data-status-raw=\"{h(status_raw)}\""
                        f"{desc_attr}"
                        f"{label_attr}"
                        f" title=\"{desc}\">"
                    )
                    close_tag = "</a>"
                else:
                    open_tag = (
                        "<div class=\"chapter\""
                        f" data-status=\"{h(status_class)}\""
                        f" data-status-raw=\"{h(status_raw)}\""
                        f"{desc_attr}"
                        f"{label_attr}"
                        f" title=\"{desc}\">"
                    )
                    close_tag = "</div>"
                parts.append(
                    f"{open_tag}"
                    f"<span class=\"id\">{ch_id}</span>"
                    f"<span class=\"title\">{ch_title}</span>"
                    f"{arc_100_badge}"
                    f"{badge}"
                    f"{close_tag}"
                )
            parts.append("</div>")  # .chapters
            parts.append("</div>")  # .book
        parts.append("</div>")  # .band
    parts.append("</div>")  # .arc100-tree
    return "\n".join(parts)


def _render_page_inventory(
    data, tree_html: str, counts: dict[str, int], project_name: str
) -> str:
    arc_version = data.get("arc_100_version", "unknown")
    active_version = data.get("active_version") or "(none — master only)"
    total = sum(counts.values())
    # TM-4b-2: HTML-escape project_name at every render-page substitution
    # site. The literal `ARC-` Version prefix below is the scheme label
    # of the ARC-100 version-numbering convention and stays unchanged.
    return f"""---
title: {h(project_name)} Master Index (Home)
generated: true
hook: _hooks/arc100_master_index.py
note: |
  This file is generated from 00-01_ARC-100_Standard_Inventory.md on every mkdocs build.
  Do not hand-edit. Edit the YAML block in 00-01 instead.
---

# {h(project_name)} Master Index

> Generated from [`00-01_ARC-100_Standard_Inventory.md`](00-01_ARC-100_Standard_Inventory.md).
> The YAML block in that file remains the source of truth for agents.

<div class="arc100-meta">
  <span class="arc100-meta-item"><strong>Version:</strong> ARC-{h(str(arc_version))}</span>
  <span class="arc100-meta-item"><strong>Active version:</strong> {h(str(active_version))}</span>
  <span class="arc100-meta-item"><strong>Chapters:</strong> {total} total ({counts['active']} active, {counts['draft']} draft, {counts['placeholder']} placeholder)</span>
</div>

<div class="arc100-controls">
  <label for="arc100-filter">Show:</label>
  <select id="arc100-filter">
    <option value="active">Active only ({counts['active']})</option>
    <option value="active-draft">Active + Draft ({counts['active'] + counts['draft']})</option>
    <option value="all" selected>All chapters ({total})</option>
  </select>
  <button type="button" id="arc100-expand-all" class="arc100-action">Expand all</button>
  <button type="button" id="arc100-collapse-all" class="arc100-action">Collapse all</button>
</div>

{tree_html}

---

For the canonical YAML and per-band prose, see [`00-01_ARC-100_Standard_Inventory.md`](00-01_ARC-100_Standard_Inventory.md).
For the ARC-100 system specification, see [`00-00_ARC-100_General.md`](00-00_ARC-100_General.md).
For the ARC-100 Glossary, see [`00-02_ARC-100_Glossary.md`](00-02_ARC-100_Glossary.md).
"""


def _render_page_project(
    data,
    tree_html: str,
    counts: dict[str, int],
    project_name: str,
    is_arc100_project: bool,
    index_link_target: str,
    index_link_display: str,
    general_link_target: str | None,
    general_link_display: str | None,
) -> str:
    arc_version = data.get("arc_100_version", "unknown")
    active_version = data.get("active_version") or "(none — master only)"
    total = sum(counts.values())
    # The "Project" differentiator distinguishes the ARC-100 Project
    # index site from the ARC-100 standard inventory site (ARC-100
    # Project is the in-repo instance that exercises the standard
    # against ARC-100's own development — it renders TWO sites with
    # the same project_name, so it needs a differentiator). Every
    # downstream <PROJECT>-100 renders ONE site (no inventory mode),
    # so no differentiator: "FLOW-100 Index", not "FLOW-100 Project
    # Index".
    #
    # User direction 2026-05-29: ensure exactly one instance of the
    # word "Project" in ARC-100 Project's rendered title, and zero in
    # any downstream's rendered title.
    #
    # TM-4b-2: see _render_page_inventory above. The `ARC-` Version
    # prefix is the scheme-label of the ARC-100 version-numbering
    # convention (a downstream's "Version: ARC-100.1" surfaces the sync
    # relationship to upstream ARC-100) and stays unchanged.
    discriminator = " Project" if is_arc100_project else ""
    # The note's shorthand chapter id is the BB-CC prefix of the index
    # source basename (everything before the first "_"): e.g.
    # "01-01_ARC-100-Project_Index.md" -> "01-01".
    index_chapter_id = index_link_display.split("_", 1)[0]
    # The "General introduction" footer sentence is optional: it renders
    # only when a general-introduction source is configured
    # (general_link_target/display non-None). The leading newline
    # reconstructs the line break after the canonical-YAML sentence; when
    # omitted the canonical line stands alone.
    if general_link_target is not None:
        general_intro_line = (
            f"\nFor the {h(project_name)}{discriminator} General introduction, "
            f"see [`{general_link_display}`]({general_link_target})."
        )
    else:
        general_intro_line = ""
    return f"""---
title: {h(project_name)}{discriminator} Index (Home)
generated: true
hook: _hooks/arc100_master_index.py
note: |
  This file is generated from {index_link_target} on every
  mkdocs build, written to docs_dir root (so the canonical URL is "/"
  matching the red site's master-index location). Do not hand-edit.
  Edit the YAML block in {index_chapter_id} instead.
---

# {h(project_name)}{discriminator} Index

> Generated from [`{index_link_display}`]({index_link_target}).
> Book 00 rows are inherited from the standard inventory at
> `master-vault/docs/00/00-01_ARC-100_Standard_Inventory.md`; project
> rows (Book 01 / 02 / 10 / ...) are project-authored. The YAML block
> in `01-01` remains the source of truth.

<div class="arc100-meta">
  <span class="arc100-meta-item"><strong>Version:</strong> ARC-{h(str(arc_version))}</span>
  <span class="arc100-meta-item"><strong>Active version:</strong> {h(str(active_version))}</span>
  <span class="arc100-meta-item"><strong>Chapters:</strong> {total} total ({counts['active']} active, {counts['draft']} draft, {counts['placeholder']} placeholder)</span>
</div>

<div class="arc100-controls">
  <label for="arc100-filter">Show:</label>
  <select id="arc100-filter">
    <option value="active">Active only ({counts['active']})</option>
    <option value="active-draft">Active + Draft ({counts['active'] + counts['draft']})</option>
    <option value="all" selected>All chapters ({total})</option>
  </select>
  <button type="button" id="arc100-expand-all" class="arc100-action">Expand all</button>
  <button type="button" id="arc100-collapse-all" class="arc100-action">Collapse all</button>
  <button type="button" id="arc100-book00-toggle" class="arc100-action" data-book00-state="hidden">Show ARC-100 standard chapters</button>
</div>

{tree_html}

---

For the canonical YAML, see [`{index_link_display}`]({index_link_target}).{general_intro_line}
"""
