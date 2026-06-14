---
title: 00-00 ARC-100 General
arc_100_id: "00-00"
status: active
keywords: [arc-100, ata-100, indexing, chapter-numbering, master, version, documentation-system]
agent_summary: |
  Canonical specification of the ARC-100 documentation indexing system.
  Defines the two-level chapter numbering, filename pattern, status
  lifecycle, master/version split, the reserved 00-xx chapters, and the
  active-version-copy rule for 00-01. The companion machine-parseable
  index is at 00-01_ARC-100_Standard_Inventory.md.
prerequisites: []
companions: ["00-01_ARC-100_Standard_Inventory.md", "00-02_ARC-100_Glossary.md"]
---

## 00-00 ARC-100 General

> **What this chapter is.** The canonical specification of the ARC-100
> documentation indexing system. Numbering, lifecycle, master/version
> split, and the rules every agent must follow when reading or writing
> chapters under `docs/master/architecture/` or `docs/versions/<v>/architecture/`.
>
> **What this chapter is not.** A list of chapters — that lives in the
> companion file [`00-01_ARC-100_Standard_Inventory.md`](00-01_ARC-100_Standard_Inventory.md).
> A specification of any chapter content. A roadmap of when chapters are
> filled in.
>
> **What ARC-100 is.** A generic, project-agnostic starting point for
> any software project's architecture documentation. A project adopting
> ARC-100 inherits the structure, then adds, skips, or extends books and
> chapters as the project's domain requires. The ARC-100 index lists
> only the chapters common to most networked applications; project-
> specific chapters are added in unallocated slots without amending
> ARC-100 itself.

### 00-00.1 — Why ARC-100 exists

Two pain points motivate the system:

1. **No stable identity for chapters across versions.** A chapter in
   `docs/versions/<v>/architecture/` and its eventual home in
   `docs/master/architecture/` are linked only by title and human
   judgement. After successive versions reorganize overlapping
   concepts, the implicit mapping becomes a liability. A chapter
   needs a stable ID that survives version migrations.
2. **Documentation drift from implementation.** Plans get written, code
   ships, plans get marked Done — and the architecture chapters that
   *describe* the shipped behavior drift quietly out of sync. ARC-100
   gives the documentation-maintenance subagents a stable handle on
   "where does X live right now?" so the gap can be closed without
   human-driven scavenger hunts.

The numbering system is borrowed in spirit from aviation's ATA 100.
Every chapter has a stable two-level number allocated up front, so the
same conceptual chapter has the same path whether it lives in the
version working folder or the master archive.

### 00-00.2 — Name and versioning

- **System name**: ARC-100 (analogous to ATA 100). A project adopting
  ARC-100 typically renames its instance to `<PROJECT>-100`
  (e.g., `FLOW-100`, `CS-100`); the structural rules are unchanged.
- **Active index version**: starts at **ARC-100.1**.
- **Adding chapters or chapters in unused index positions does NOT
  produce a new version.** The index is append-only at the slot level;
  chronological growth is normal operation.
- A **ARC-100.2** (or higher) version is reserved for the rare event of
  a full reindex — re-purposing existing chapter numbers. This is
  disruptive and should ideally never happen. ATA 100 has been
  reindexed historically; precedent exists, but the cost is real.

### 00-00.3 — Two structural levels: book and chapter

- **First level — book**: the topic container. Examples: `40 Server`,
  `93 Security`. **A book never has content of its own** — it is a
  container for chapters. Anything one might say "about server in
  general" lives in `40-01 Overview`, not in the book itself.
  A book has a number (e.g., `40`) and a title; its sole purpose is to
  group related chapters under a stable identity.
- **Second level — chapter**: the actual `.md` file. Examples:
  `40-01_Overview.md`, `93-02_Authentication.md`. Chapters carry the
  content. Their numbers are book-scoped (`40-01`, `40-02`, ...
  within book `40`).
- **No third structural level.** A chapter has no sub-chapter `.md`
  files. Internal organization within a chapter uses sections (see
  §00-00.3.1) — these are markdown headings, not separate files.

#### 00-00.3.1 — Sections within a chapter

A chapter may carry numbered **sections** for in-chapter organization
and citation. Sections are markdown headings inside the chapter file,
not separate files, and are not allocated through the index.

- **Numbering**: dotted-decimal suffix on the chapter ID. The chapter's
  own ID `BB-CC` is treated as `BB-CC` (the implicit "section 0" /
  whole-chapter scope). First explicit section is `BB-CC.1`, then
  `BB-CC.2`, etc.
- **Heading shape**: section headings are `### BB-CC.N — Title` to
  match the convention used in this chapter (`### 00-00.3 — Two
  structural levels`). The `BB-CC.N` prefix in the heading text makes
  the section grep-able and citation-friendly.
- **Sub-sections** (a fourth level): `BB-CC.N.M`, with heading
  `#### BB-CC.N.M — Title`. Use sparingly; sub-sections are useful
  for chapters where an agent's findings need to cite a specific rule
  within a section. Do not nest a fifth level — flatten or split the
  chapter instead.
- **Allocation**: sections are author-allocated within a chapter and
  are NOT tracked in `00-01_ARC-100_Standard_Inventory.md`. The librarian's job
  ends at chapters; section structure is local to each chapter.
- **Stability**: section numbers are stable once the chapter is
  `active`. Renumbering sections in an `active` chapter breaks
  external citations (agent findings, plan references) and should be
  treated as a chapter-level revision (note in `## Revisions`
  footer).

**When to use sections**: any chapter whose body contains multiple
distinct rules, decisions, or sub-topics that other artifacts (agents,
plans, other chapters) need to cite individually. A chapter with one
indivisible idea does not need numbered sections — leave it as
freeform markdown.

**Citation format**: `[BB-CC §N]` for a section (e.g., `[93-02 §3]`
for `93-02.3 Cookies`); `[BB-CC §N.M]` for a sub-section.

### 00-00.4 — Filename pattern

Files are named `<book>-<chapter>_<title>.md`, for example:

```text
00-00_ARC-100_General.md
00-01_ARC-100_Standard_Inventory.md
40-01_Overview.md
93-02_Authentication.md
```

Pattern-matching regex should expect two-digit zero-padded numbers
normally but tolerate three or more digits:

```text
^(0\d|[1-9]\d|\d{3,})-(0\d|[1-9]\d|\d{3,})_[A-Za-z0-9_.-]+\.md$
```

The "100" in ARC-100 is a soft cap on cognitive load, not a hard cap
on slots. If a band genuinely exhausts 01–99, allocation can spill into
101–199 — but doing so is a smell that the band has outgrown its
allocation and the situation should be raised as a candidate trigger
for a future ARC-100.2 reindex.

### 00-00.5 — Book 00 chapter overview

The table below is a courtesy description of what each Book 00
chapter contains. The authoritative slot inventory — every book and
chapter across every band, with status and lineage fields — lives in
`00-01`. The body-ownership and slot-identity rules that govern
which books may host project-authored content are defined in
[§00-00.7.1](#00-0071-chapter-and-book-lineage) and
[§00-00.7.2](#00-0072-body-ownership-implied-by-book-number).

| Chapter | Purpose |
|---|---|
| `00-00 ARC-100 General` | This chapter. Describes the ARC-100 system itself — concepts, conventions, agent rules, version policy. |
| `00-01 ARC-100 Index` | The machine-parseable + human-readable master index. Lists every band, every book, every chapter with status, description, and check-out state. (Renamed to ARC-100 Standard Inventory in phase 3.1b.) |
| `00-02 ARC-100 Glossary` | Disambiguates ARC-100-specific terminology from generic preemptive-indexing terminology. The single authoritative vocabulary for "what ARC-100 means by X". |
| `00-03 Documentation Site` | Architecture of the mkdocs site that hosts these chapters: configuration, the index-generator hook, the css/js customisations, and the fork recipe. |
| `00-04 Standards Comparisons` | Comparisons of ARC-100 against widely-cited external standards (arc42, C4, 4+1, ISO 42010, AWS Well-Architected, SWEBOK, ITIL, OWASP SAMM, DORA). Refreshed via the reassess-standards-comparisons command. |
| `00-05 ARC-100 Synchronization` | The ARC-100-SYNC system: portable toolkit for keeping a downstream `<PROJECT>-100` documentation index in step with upstream ARC-100. Identity model, conform contract, judgment surface, distribution, security posture. Lives under `ARC-100-SYNC/` at the repo root. |
| `00-06 ARC-100 Architectural Modeling` | LikeC4 conventions, view-class taxonomy, embedding mechanics, theme. Promoted to `status: active` in phase 3c. |

### 00-00.6 — Status lifecycle

Every chapter carries a `status` in the index:

| Status | Meaning |
|---|---|
| `placeholder` | Number reserved in the index; no `.md` file exists yet. |
| `draft` | File exists, not yet authoritative. Plans may not cite it as ground truth. |
| `active` | Authoritative. The default state. |
| `checked-out-to-vX` | A version has taken ownership of this chapter for modification. Master copy is frozen until promotion. |
| `superseded` | Replaced by another chapter (referenced by `superseded_by`). Kept for history; not loaded as context. |
| `deprecated` | Removed from active use. Number stays burned (per ATA precedent — never re-allocated). |

Transitions are enforced by the librarian agent and the promote-version
command. Other agents and commands may only **read** status.

### 00-00.7 — Band allocation

Top-level structure of the index. See [`00-01_ARC-100_Standard_Inventory.md`](00-01_ARC-100_Standard_Inventory.md)
for the per-band book and chapter listing.

| Range | Area |
|---|---|
| `00-09` | Application — the application's fundamental identity (mission, users, value, design principles); topics that stand apart from technology choices. Hosts the ARC-100 documentation-indexing system itself (Book 00, upstream-owned and body-synced) and the active project's documentation-system instance + project identity (Books 01–02, upstream-prescribed slot identity with project-authored body content). Books 03–09 open for project allocation. |
| `10-19` | Governance — glossary, roadmap, decisions, versioning policy |
| `20-39` | Client — UI, rendering, browser-side concerns, user-facing surfaces (optional) |
| `40-59` | Server — transport, handlers, identity, runtime, audit (optional) |
| `60-79` | Data — schema, persistence, migrations, identity data, audit data, asset data |
| `80-89` | Tooling — the materials, instruments, and conventions used to build, validate, and integrate the application; contributor-facing |
| `90-99` | Operations — cross-cutting operational concerns (observability, capacity, deployment, security, compliance) |

**Four structural rules**:

1. Every band keeps **at least 5 unallocated book slots** at all
   times. Filling a band past this threshold is itself a signal that
   reindex pressure is building.
2. **Bands are renumbered only at ARC-100.2.** New books slot into
   existing bands. The librarian halts at any proposal that would
   require a new band.
3. **ARC-100 allocates books from the low end of each band; downstream
   projects allocate from the high end and work downward.** ARC-100's
   next free book number grows up from the lowest unused slot in the
   band; a project's next free book number grows down from the band's
   highest unused slot. This minimises rebase collisions when ARC-100
   evolves.
4. **Within a book, ARC-100 uses chapter slots 01–49; downstream
   projects allocate chapters from 50 upward.** ARC-100 wins on any
   contested slot. At rebase time, the librarian flags collisions and
   the downstream project renumbers its conflicting chapter to an
   unused 50+ slot.

#### 00-00.7.1 — Chapter and book lineage

Every book and chapter entry in `00-01_ARC-100_Standard_Inventory.md` (and in any
downstream **working index** — chapter `01-01`,
`docs/01/01-01_<PROJECT>-100_Index.md`; see
[§00-00.10.1](#00-00101-one-standard-two-indexes)) that originates with
ARC-100 carries two related YAML fields:

```yaml
arc_100: true
arc_100_ulid: 01KRRRDWAM60X0V0F4DX53AFG4
```

**`arc_100: true`** — boolean lineage flag. Marks the entry as
inherited from ARC-100 itself. The master-index generator hook
renders this as an "ARC-100" badge on every tagged book and chapter
row.

**`arc_100_ulid`** — the 26-character ULID (Crockford base32,
time-ordered) that uniquely identifies this entry across upstream
releases and across projects. Generated once at allocation time and
**never changed**. Slot numbers, titles, and descriptions can mutate
freely under upstream evolution; the ULID is the only stable identity
key. The conformance tool (see `ARC-100-SYNC/` at the repository root)
uses the ULID to match upstream entries against local entries
unambiguously when applying upstream updates — without it, the
question "is this the same chapter as before?" devolves into
fuzzy-string matching on title and description.

ULIDs are generated by `ARC-100-SYNC/scripts/ulid.py` (at the
repository root, outside the rendered doc tree) — the same generator
is used by ARC-100 itself and by every downstream project for
consistency. See `00-05` §00-05.7 for the language-choice rationale.

**What these fields promise a reader.** The slot number, title, and
high-level intent of this entry are inherited from ARC-100 and are
stable across upstream releases; they remain compatible with any
other ARC-100-derived project. A downstream project may fill in the
chapter's body content, but the slot identity is upstream-owned and
the `arc_100_ulid` is the canonical handle on that identity.

**Lineage rules:**

- Both fields are **preserved** when a downstream project fills in
  the chapter's body content — ARC-100 provides the slot, intent,
  title, and ULID; the downstream project provides the substance.
- Both fields are **preserved** on a chapter whose status becomes
  `deprecated` or `superseded` (per [§00-00.6](#00-006-status-lifecycle)).
  They record lineage, not endorsement: a deprecated
  ARC-100-inherited chapter retains its lineage so future readers
  (and the conformance tool) can trace where the slot came from.
- Both fields are **omitted** on a chapter or book that the
  downstream project allocated itself (i.e., in slots 50+ within a
  book, or in books above the band's ARC-100 range per rule 3).
  Downstream projects may independently assign their own ULID to
  project-specific entries if they want stable identity for their
  own internal tracking — but it would use a project-specific field
  name (e.g., `<project>_100_ulid`), never `arc_100_ulid`.
- **Renaming an `arc_100: true` chapter is forbidden.** If a
  downstream project needs a different chapter title or intent,
  allocate a new slot at 50+ and deprecate the inherited one —
  never rename in place. Renaming would break the cross-project
  compatibility the lineage tag promises.
- **The `arc_100_ulid` is immutable for the life of the entry.**
  Even when ARC-100 renumbers, retitles, or moves an entry between
  bands, the ULID stays the same. The librarian rejects any
  operation that would change an existing ULID.

**Optionality**: client-, server-, and data-band books are optional —
a CLI tool may have no client band, a static site may have no server
band, a stateless library may have no data band. Empty bands are
normal; allocation is per-project as the project requires.

**Body-ownership clause** (added phase 3.1a, 2026-05-25):
`arc_100: true` entries in Books 01, 02, and 10 carry
upstream-prescribed slot identity (ULID + slot number + title shape)
but downstream-authored body content. This refines the lineage-tag
contract: the slot identity is stable across projects (a
downstream's `01-01 <NAME> Index` is the same conceptual slot as
ARC-100's `01-01 ARC-100 Project Index`, sharing a ULID), but the
chapter body, description, keywords, and any sub-section structure
are project-flavoured. The "fully inherited" semantic (body synced
verbatim) applies only to Book 00 entries. See
[§00-00.7.2](#00-0072-body-ownership-implied-by-book-number).

#### 00-00.7.2 — Body ownership implied by book number

Book 00 chapters are upstream-owned: ARC-100 authors them in the
master vault; downstreams sync them wholesale (bodies and inventory
entries). Books 01, 02, and 10 carry `arc_100: true` slot identities
prescribed by ARC-100 (the ULID, slot number, and title shape come
from upstream) but their bodies are project-authored — each
downstream fills in its own project-system, project-philosophy, and
project-glossary content. Other `arc_100: true` entries in bands 20+
follow the existing 01–49 / 50+ slot-split rule (see
[§00-00.7](#00-007-band-allocation) rule 4 above).

**Rule of thumb**: if the chapter belongs in Book 00 it is
upstream-owned (synced verbatim); otherwise it is project-owned
regardless of `arc_100` status.

### 00-00.8 — Master vs version split

#### 00-00.8.1 — Master is the canonical archive

- `docs/master/architecture/` holds every chapter that is not currently
  checked out to a version.
- **Master is written ONLY by the promote-version command**. No agent,
  no other command, no human direct edit. The strictness is the point —
  it makes master always-trustworthy as ground truth.

#### 00-00.8.2 — Version checks out at the chapter level

- `docs/versions/<vX>/architecture/` holds chapters that vX is
  actively modifying.
- Check-out granularity is **the chapter, never the book
  container**. If v5 modifies `40-03`, only `40-03` moves into the
  version folder; `40-01`, `40-02`, etc. stay in master.
- On check-out, `00-01 ARC-100 Index` in master is updated to mark
  `40-03` as `checked-out-to-v5`, and the version copy carries
  `source_master_revision: <git-sha>` in its front-matter.
- **No symbolic links** in the version folder. Reading "all of band 40
  cohesively" requires consulting both folders. Two coping mechanisms:
  1. The librarian agent — its job is to resolve "where does
     X live right now?" without a human searching both folders.
  2. The version's `mkdocs.yml` may compose a build view that
     references master paths so the served site looks cohesive without
     duplicating files on disk. Implementation detail; out of scope
     here.

### 00-00.9 — Active-version-copy rule for `00-01`

Every other chapter in the ARC-100 system follows the standard
master/version rule above. **`00-01` is the one exception**, because
the librarian modifies the index continuously throughout active
version development (allocating new chapter numbers, recording
check-outs, updating descriptions). Treating `00-01` as a normal
chapter would mean it would be checked out for every version's entire
lifetime — making the check-out signal meaningless.

The dedicated rule:

1. **Master always holds a `00-01`**, which is the canonical,
   frozen-at-last-promotion index.
2. **Exactly one version folder at a time may hold a working copy of
   `00-01`** — the *active* version's folder.
3. **The active version is whatever `mkdocs.yml` `docs_dir:` points
   at.** No separate marker file. `mkdocs.yml` already encodes the
   single source of truth for "which documentation set is the working
   set right now" — reusing it avoids a second authority that could
   disagree. Agents read `mkdocs.yml` once per invocation, extract the
   version slug from `docs_dir:`, and use that for everything below.
   If `docs_dir:` points at master directly, there is no active
   version and `00-01` lives only in master.
4. **Future-version folders do not receive a copy of `00-01`.** A
   `docs/versions/v5/` may exist for early planning while v4 is active;
   it must NOT contain `00-01_ARC-100_Standard_Inventory.md`. Any agent that finds
   one there must HALT and surface it as a structural error.
5. **All agents resolve the index by lookup order**:
   1. If `mkdocs.yml` `docs_dir:` points at a version folder, look
      under that folder first:
      `<docs_dir>/architecture/00/00-01_ARC-100_Standard_Inventory.md`.
   2. Otherwise (or if not found there), read
      `docs/master/architecture/00/00-01_ARC-100_Standard_Inventory.md`.

   The first hit wins. Agents never read both and merge — the active
   copy is authoritative for the duration of the version.
6. **Activation and promotion share one command**. There is no
   separate `/activate-version`. Closing one version and opening the
   next — if a next is being opened — is one workflow with one set of
   invariants.
7. **Pause is not unactivation.** If active version work pauses
   temporarily (e.g., a hotfix while planning a future spike), the
   `mkdocs.yml` `docs_dir:` and the version's `00-01` stay put. Only
   the promote-and-optionally-activate workflow changes them.

### 00-00.10 — Adoption and bootstrap

When a project adopts ARC-100, two starting paths are normal:

- **Greenfield**: bootstrap ARC-100 directly in `docs/master/`, with
  `mkdocs.yml` `docs_dir:` pointing at master (no active version) until
  the first version branch opens.
- **Migration from existing docs**: a project with a pre-existing,
  ad-hoc documentation tree can bootstrap ARC-100 in `docs/master/`
  alongside the existing tree. The existing tree retains its current
  ad-hoc structure for the remainder of the in-flight version's
  lifetime; the ARC-100 path captures only the chapters being newly
  authored or actively migrated. Bulk migration of legacy chapters into
  ARC-100 paths is a single planned operation at version closeout, not
  incremental during version development.

In both paths, the ARC-100 system is bootstrapped directly in master.
No version folder receives a copy of `00-01` until the first
promote-version `--next <slug>` activates a version.

#### 00-00.10.1 — One standard, two indexes

ARC-100 is an **index standard**, not a documentation set. An adopting
project therefore always holds **two** index files, with different
owners and different jobs:

| Index | Chapter | Downstream path | Owner | Job |
|---|---|---|---|---|
| The **ARC-100 index** | `00-01` | `docs/00/00-01_ARC-100_Standard_Inventory.md` | ARC-100 (upstream) | The standard itself. A read-only mirror, refreshed wholesale on every sync like all of Book 00. Reference material — never the basis of the project's site. |
| The **working index** | `01-01` | `docs/01/01-01_<PROJECT>-100_Index.md` | The project | The project's table of contents — the single index its documentation site renders from, and the only index the project's librarian writes. |

**Day zero: the two indexes are identical.** Bootstrap copies the
ARC-100 index into the working index verbatim — same books, same
chapters, same ULIDs; only the marker pair changes
(`ARC-100-INDEX` → `<PROJECT>-100-INDEX`). At that instant `00-01`
and `01-01` say exactly the same thing. This is the starting point,
not the steady state.

**Then they diverge — by design.** Exactly two motions drive the
divergence, and both happen in the working index only:

1. **The project fills inherited slots.** Chapters that ARC-100
   pre-allocated (in Books 01 and up) get real `.md` files and
   project-authored bodies; each slot's working-index status flips
   from `placeholder` to `active` as its body is written. The slot
   identity — number, title shape, ULID — stays upstream-owned
   ([§00-00.7.2](#00-0072-body-ownership-implied-by-book-number)).
2. **The project allocates new entries.** The librarian assigns the
   chapters (and books) the project needs into the unallocated slots
   ARC-100 deliberately left open (see `00-01` §00-01.4). These
   entries exist **only** in the working index.

**The `arc_100` flag is the discriminator**
([§00-00.7.1](#00-0071-chapter-and-book-lineage)). Read any
working-index entry and you know which world it belongs to:

- `arc_100: true` — inherited from the ARC-100 index. Every entry of
  the ARC-100 index remains present in the working index for the life
  of the project — deprecated entries keep the flag, and numbers are
  never re-allocated. The sync tool keeps these entries in step with
  upstream and escalates anything that needs judgment.
- `arc_100: false` — or the lineage fields omitted entirely, which
  means the same thing — allocated by the project. Unique to the
  working index; the sync never touches these entries.

The invariant, stated plainly: **the working index is always a
superset of the ARC-100 index** (as of its last sync with upstream).
The mirrored `00-01` shows the pristine upstream standard; the
difference between the two files is precisely the project's own
documentation.

**The ATA 100 lineage makes this concrete.** ATA 100 is an index, not
a manual: chapter 32 means Landing Gear on every aircraft, and there
are tens of thousands of aircraft maintenance manuals built on that
numbering — none of which *is* ATA 100. Each manual keeps the shared
chapter spine and adds its own aircraft's content. A `<PROJECT>-100`
works the same way: the ARC-100 index is the shared spine
(`arc_100: true`); the working index is the project's manual built on
that spine — the standard's numbers where the standard speaks, the
project's own chapters (`arc_100: false`) where it does not. (See the
ATA 100 entry in `00-02`.)

Three rules fall out of this:

- **Never hand-edit the mirrored `00-01`** — it is Book 00, replaced
  wholesale on the next sync ([§00-00.11](#00-0011-hard-rules)).
- **Never delete an `arc_100: true` entry from the working index** —
  deprecate it instead. The sync detects deletions of inherited
  entries and escalates them for explicit human judgment.
- **Never render the project's site from `00-01`** — a project has
  exactly one `mkdocs.yml`, and its site renders from the working
  index at `01-01`. (Only the ARC-100 repository itself runs a second
  site, to publish the standard.)

### 00-00.11 — Hard rules

These rules govern every agent and human that touches ARC-100:

- **Only the librarian agent may add to `00-01_ARC-100_Standard_Inventory.md`.**
  - **Bootstrap exception.** When a reviewed plan creates or
    fundamentally adapts the librarian agent itself, and the runtime
    dispatcher cannot resolve the freshly-defined agent within the
    same session, the plan's parent may execute the librarian's
    documented protocols (e.g., Schema-sweep) verbatim within that
    session. The exception applies only when (i) the operation is
    defined in the librarian's body within the same plan and atomic
    commit, (ii) the operation satisfies all authorising conditions
    documented in the librarian's body, and (iii) the commit message
    includes an explicit "bootstrap exception under §00-00.11" audit
    note naming the librarian skill being executed. The exception is
    narrow by design: it covers the canonical chicken-and-egg case
    (a plan that creates the librarian it would otherwise need to
    dispatch) and nothing else.
- **Only the promote-version command may write to `docs/master/`**
  (other than the librarian updating `00-01` and the bootstrap
  creation of `00-00`, `00-01`, and `00-02` themselves).
- **Only the promote-version command's `--next <slug>` mode may copy
  `00-01` into a version folder.**
- **Subagents that need a chapter ruling MUST emit `LIBRARIAN_REQUIRED:
  <question>` and return** — never proceed with a guessed chapter.
- **Documentation subagents never invent a new chapter number.** They
  must escalate to the parent who dispatches the librarian.
- **Subagents cannot dispatch subagents.** The parent owns the loop.
- **Never read both copies of `00-01` and merge** — first hit wins
  per §00-00.9 lookup order.
- **Book 00 is authored *here*; it is a read-only mirror *downstream*.**
  Within the ARC-100 standard repository — *this* repo: the canonical
  `master-vault/docs/00/` chapters are the single source of record. There
  is no second in-repo copy: the published distribution mirror is assembled
  from `master-vault/docs/00/` at release time, so the chapters cannot
  drift against an in-repo twin. Adopters obtain Book 00 by a depth-1 clone
  of that published mirror, which `arc_sync.py` syncs (relpath-preserving)
  into the downstream `docs/00/`. The standard's author has full
  create/read/update/delete authority over them, subject only to the
  chapter-numbering rules (§00-00.4) and the `00-01` librarian rule above.
  In an adopting project (a `<PROJECT>-100` instance), those same chapters
  are **read-only mirrors** delivered and refreshed by the ARC-100-SYNC
  tool (`arc_sync.py`); adopters must not hand-edit them, because local
  edits are overwritten on the next sync. The "do not hand-edit Book 00"
  guidance in `00-07` and the next-steps output of `arc_sync.py` is
  therefore the *downstream* rule — it does **not** constrain authoring
  inside this repository.

### 00-00.12 — ARC-100 out-of-scope topics

ARC-100 is a documentation taxonomy for *an application's
architecture and intent*. It is deliberately not a taxonomy for the
*business that builds the application* nor for the *operations team
that runs it*. This section enumerates the categories of topic that
ARC-100 will not standardize, and the reason for each.

There are two distinct senses of "out of scope" in any
ARC-100-derived project, and they must not be confused:

| Sense | What it means | Where it lives |
| --- | --- | --- |
| **ARC-100 out of scope** | Topics that the ARC-100 system will never standardize, regardless of any adopting project's needs. Enumerated here. | This section (00-00.12). |
| **Application out of scope** | Features or behaviours that an adopting project's application deliberately will not implement (e.g., "we will not support multi-tenancy", "we will not offer single sign-on until v3"). | Per-project chapter `11-02 Out-of-Scope`. |

The categories below are out of scope for ARC-100 the system.
Adopting projects that need documentation in these categories must
document them in a system separate from their `<PROJECT>-100`.

#### 00-00.12.1 — Support operations and incident response

Runbooks, paging rotations, escalation paths, incident-commander
roles, post-mortem templates, on-call schedules, war-room cadence,
service-desk procedures, ticket workflows, and customer-support
processes.

**Reason.** These describe what *people* do when the application
breaks, not what the application *is*. Two organisations running the
same ARC-100-documented application would write very different
incident-response procedures. The architectural foundations *that
enable* response — telemetry signals (Book 90 Observability),
rollback mechanisms (Book 92 Deployment), graceful degradation and
kill switches (93-15 Resource Limits, 93-17 RASP) — are in scope and
already covered. The response procedures themselves belong in an
ops-runbook system separate from the project's `<PROJECT>-100`.

#### 00-00.12.2 — Business plans, budgeting, and funding

Revenue models, pricing strategies, sales playbooks, financial
forecasts, budget approvals, vendor procurement, contract
negotiations, fundraising, and investor communications.

**Reason.** These describe the *business* that builds the
application, not the application's architecture or intent. An
ARC-100-documented application is the same application whether it
is a free open-source project, a B2B SaaS, or an internal tool —
the business context is orthogonal. Business and finance
documentation belongs in a separate business-operations system.

#### 00-00.12.3 — Employee relations and team operations

Hiring practices, onboarding programmes, performance reviews,
compensation frameworks, organisational charts, team-structure
decisions, professional-development plans, team culture, and
employee satisfaction surveys.

**Reason.** These describe the *team* that builds the application,
not the application. Cultural and people-management concerns vary
by employer and jurisdiction; they are not properties of the
application's architecture. People-operations documentation belongs
in a separate human-resources system.

#### 00-00.12.4 — Service-management and IT operations

Service-desk operations, supplier management, vendor relationships,
service-level-agreement negotiation with customers, IT-asset
inventory of non-application infrastructure, change-advisory-board
processes, and service-catalogue maintenance. This is the territory
covered by ITIL and adjacent service-management frameworks (see
[`00-04 Standards Comparisons`](00-04_ARC-100_Standards_Comparisons.md)
§00-04.9).

**Reason.** These describe the *IT service organisation* that
operates the application alongside other applications, not the
application itself. ARC-100 stops at the application's boundary.
ITIL or an internal service-management framework documents the
operations side; the two are companion systems, not overlapping.

#### 00-00.12.5 — When the line blurs

When a topic feels borderline, apply this test: *would this content
survive a complete reimplementation of the application in a different
language, runtime, or stack?* If yes, it likely belongs in ARC-100 —
it is identity-level. If no — if the content describes a person,
team, process, or business context that is orthogonal to the
application's identity — it belongs in a companion system, not in
ARC-100. This is the same hinge expressed implicitly in the
Application (00-09) and Tooling (80-89) band descriptions.

### 00-00.13 — Pointers

- **Index**: [`00-01_ARC-100_Standard_Inventory.md`](00-01_ARC-100_Standard_Inventory.md) — the
  full book + chapter list with statuses.
- **ARC-100 Glossary**: [`00-02_ARC-100_Glossary.md`](00-02_ARC-100_Glossary.md)
  — terminology disambiguation (ARC-100-specific vs generic
  preemptive-indexing terms).
- **Standards Comparisons**: [`00-04_ARC-100_Standards_Comparisons.md`](00-04_ARC-100_Standards_Comparisons.md)
  — relationship of ARC-100 to nine widely-cited external standards.
- **Project glossaries** (Book 10): Book 10 hosts the project's
  glossary. `10-01 General Glossary` is the first content slot.
  Additional sub-glossaries (technical, user, domain) allocate at
  10-02+ as the project requires. Distinct from the ARC-100 Glossary
  at `00-02`, which covers documentation-system terminology only.
- **Roadmap / future architecture** (planned location): `11-01 Roadmap`.

---

> **Maintenance.** This chapter is the canonical home for the ARC-100
> system specification. When the system evolves, edit this chapter
> directly via the promote-version workflow. Substantive additions
> (new statuses, new lifecycle rules, new agent contracts) should also
> update the agent files under `.claude/agents/` if they change agent
> behavior.
