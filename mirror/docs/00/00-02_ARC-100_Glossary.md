---
title: 00-02 ARC-100 Glossary
arc_100_id: "00-02"
status: active
keywords: [arc-100, glossary, terminology, ata-100, preemptive-indexing, book, chapter, band]
agent_summary: |
  Authoritative vocabulary for the ARC-100 documentation system.
  Disambiguates terms unique to ARC-100 (book, chapter, band,
  active-version-copy rule, etc.) from generic terms borrowed from
  preemptive-indexing systems in general (slot, reindex, append-only
  allocation, etc.). Cross-references the ARC-100 General chapter for
  prescriptive rules and the ARC-100 Index for the live chapter list.
prerequisites: ["00-00_ARC-100_General.md"]
companions: ["00-00_ARC-100_General.md", "00-01_ARC-100_Standard_Inventory.md"]
---

## 00-02 ARC-100 Glossary

> **What this chapter is.** The single authoritative vocabulary for
> "what ARC-100 means by X". Two sections: **§00-02.1 — Generic terms**
> (concepts shared with ATA 100 and similar preemptive-indexing
> systems) and **§00-02.2 — ARC-100-specific terms** (concepts unique
> to this implementation). Every defined term carries a back-reference
> to where it is normatively specified.
>
> **What this chapter is not.** A glossary for the application
> (workflows, processes, parameters, etc.) — that lives at
> `10-01 General Glossary`. A list of who-knows-what. A FAQ.
>
> **Convention.** Terms are listed alphabetically within each section.
> Where a term has both a generic and a ARC-100-specific meaning, the
> generic entry says "see also §00-02.2" and the ARC-100 entry refers
> back. Cross-references use chapter-section anchors (§00-00.X) into
> the ARC-100 General chapter.

### 00-02.1 — Generic terms (preemptive indexing in general)

These terms apply to any preemptive-indexing system in the ATA 100
family. Definitions here are deliberately implementation-agnostic.

#### Active

A status indicating an entry is in use as the authoritative reference
for its slot. Synonymous across most preemptive-indexing systems with
"published, current, not retired."

> **ARC-100 specifics**: see §00-02.2.

#### Append-only allocation

The discipline of filling **previously unused** slots without disturbing
existing assignments. Append-only allocation is normal operation in any
preemptive-indexing system and does **not** trigger a version bump,
because nothing already-assigned changes meaning.

Contrast with **reindex**.

#### ATA 100

The Air Transport Association of America's chapter-numbering standard
for aircraft maintenance documentation, originally published in 1956.
Every aircraft system has a stable two-level number (e.g. chapter 32 =
Landing Gear, sub-chapter 32-40 = Wheels and Brakes) that is consistent
across manufacturers, models, and decades — a Boeing 737 maintenance
manual and an Airbus A320 maintenance manual both use `32-40` to mean
"wheels and brakes," because the number is allocated by ATA, not by
the manufacturer. ATA 100 has since been folded into the broader iSpec
2200 standard, but the chapter-numbering convention remains in
universal use across the industry.

> **The analogous inspiration for ARC-100.** ARC-100 borrows the
> following ATA 100 conventions in spirit:
>
> - **Preemptive numbering** — the index is allocated up front, before
>   content exists, so a slot has identity even when empty.
> - **Two-level structure** — exactly one container level (chapter in
>   ATA, **book** in ARC-100) and one content level (sub-chapter in
>   ATA, **chapter** in ARC-100). No third structured level.
> - **Soft cap of 100** — the "100" names the cognitive ceiling, not a
>   hard limit on slots.
> - **Append-only allocation** — filling unused slots is normal; it
>   does not bump the index version.
> - **Burn, do not reuse** — once a slot is deprecated, its number is
>   never re-allocated.
> - **Reindex is rare and disruptive** — ATA 100 has been reindexed
>   historically; ARC-100.2 is reserved for the same scenario.
>
> What ARC-100 does **not** borrow: ATA 100's specific band layout
> (which is aviation-domain), its centralized governance (ARC-100 is
> single-project), or its physical-document orientation (ARC-100 is
> markdown-and-mkdocs-native).

#### Band

A contiguous range of slot numbers reserved up front for a single topic
area. Bands are the lowest unit of structural organization above
individual slots. Once a band is allocated, its boundaries are
considered immutable for the lifetime of the index version (changing
band boundaries triggers a reindex).

> **ARC-100 specifics**: see §00-02.2.

#### Burn (a number)

To permanently retire a slot from re-allocation, even after its content
is removed. Once burned, a slot number is never reused. ATA 100 burns
deprecated chapter numbers; ARC-100 inherits this discipline. The
opposite of burning is **reuse**, which preemptive-indexing systems
generally forbid.

#### Deprecated

A status indicating an entry has been retired from active use. Its slot
number stays burned (per the precedent above) and the entry remains
discoverable for historical context, but is no longer authoritative.

#### Index

The single document or data structure that lists every slot in the
system, its status, and its description. The index is the bootstrap
artifact: every other document in a preemptive-indexing system traces
its identity through the index. In ARC-100 the index is a YAML block
inside `00-01_ARC-100_Standard_Inventory.md`.

#### Placeholder

A status indicating a slot is reserved in the index but has no content
yet. Placeholders are how preemptive-indexing systems "block out" the
shape of future work without committing to it. A placeholder may or may
not ever transition to **active**.

#### Preemptive index

An index where slot numbers are allocated **before** content exists, so
that future content has a stable identity from the moment it is named.
Preemptive indexes contrast with retrospective indexes (where numbers
are assigned after the fact, e.g., a publisher's back-of-book index).
The defining property is: a number is meaningful even when the slot is
empty.

#### Reindex

A disruptive event where existing slot numbers are re-purposed —
typically because a band has overflowed or a structural reorganization
is needed. Reindexes always trigger a system-version bump (ARC-100.1 →
ARC-100.2) because old documents and links become invalid. ATA 100 has
been reindexed historically; the cost is real, and well-designed
preemptive indexes try to make reindexes ideally never necessary.

#### Slot

A numbered position in the index. A slot may be filled (has content) or
unfilled (placeholder), allocated (assigned a topic) or unallocated
(reserved for future use). The total slot count is fixed by the system
design — for ARC-100, seven bands × roughly ten to twenty slots each.

#### Soft cap

The numerical ceiling that names the system (the "100" in ATA 100 and
ARC-100). The cap is conceptual, not structural: allocation can spill
beyond it (101, 102, ...) without breaking parsers, but doing so signals
that pressure is building toward a reindex. The cap exists primarily to
limit cognitive load.

#### Two-level numbering

A numbering scheme with exactly two structured levels: a top-level slot
(e.g., `40`) and a child slot scoped to it (e.g., `40-01`, `40-02`).
Sections within the second-level entry are unstructured (freeform
markdown headings, in ARC-100's case). Two-level numbering is the ATA
100 convention; deeper nesting was rejected in ARC-100 for cognitive-
load reasons.

#### Unallocated slot

A slot whose number exists in the index range but has no topic
assigned. Unallocated slots are the safety margin — every band keeps a
minimum of unallocated slots reserved so that future chapters can be
added without reindex pressure.

### 00-02.2 — ARC-100-specific terms

Terms unique to this implementation. Where a term collides with general
English usage (notably "chapter" and "book"), the ARC-100 sense is
binding within this documentation system.

#### Active version

The single version slug whose folder currently holds the working copy
of `00-01 ARC-100 Index`. Resolved by reading `mkdocs.yml`'s
`docs_dir:` value: if it points at `docs/versions/<slug>`, the slug is
the active version. If it points at `docs/master/`, there is no active
version. See §00-00.9 for the active-version-copy rule.

#### Active-version-copy rule

The dedicated rule for `00-01 ARC-100 Index` (and only `00-01`) that
breaks the master-vs-version split: master always holds an `00-01`,
the active version optionally holds a working copy, and agents resolve
the index by lookup order (active first, master fallback). Specified
in §00-00.9. The rule exists because the index is edited continuously
during a version's life — treating it as a normal chapter would mean
the check-out signal never resets.

#### Band (ARC-100 sense)

A contiguous range of book numbers reserved for a part of the system —
e.g., `00-09` is the application + ARC-100 system, `40-59` is the
server, `60-79` is the data architecture. ARC-100 has seven
bands; their ranges and intent are listed in §00-00.7 and detailed per
band in [`00-01_ARC-100_Standard_Inventory.md`](00-01_ARC-100_Standard_Inventory.md). Band
boundaries are immutable except at ARC-100.2 reindex.

#### Book

**A first-level entry in the index** — a topic container with a
two-digit number (e.g., `40 Server`, `93 Security`) that
has no content of its own. A book is the parent structure for one or
more chapters. The choice of "book" over the older "first-level
chapter" reflects the actual semantics: a book groups chapters under a
stable identity, exactly like a published book groups chapters under a
title.

> **Why not just "chapter"?** Because a book has no `.md` file and no
> body content — calling it a "chapter" overloaded the word with two
> meanings (the container and the file inside). Renaming to "book" lets
> "chapter" mean exactly one thing: a content-bearing `.md` file.

#### Chapter (ARC-100 sense)

**A second-level entry in the index** — the actual `.md` file that
carries content. A chapter has a hyphenated number (`40-01`, `93-02`),
a title, a status, and (when its file exists) a body. Chapters are
scoped to their parent book: chapter `40-01` lives under book `40`.

> **Filename pattern**: `<book-id>-<chapter-id>_<title>.md`. See §00-00.4.

#### Check-out

The librarian-performed operation that moves a chapter from master to
the active version's folder for modification. On check-out: the
chapter file is copied, `source_master_revision: <git-sha>` is recorded
in the version copy's front-matter, and the master `00-01` index entry
is updated to `status: checked-out-to-<slug>`. Granularity is **the
chapter, never the book** — a book is never checked out, only its
chapters are. See §00-00.8.2.

#### `checked-out-to-vN`

A status indicating a chapter has been checked out for modification by
version `vN`. Master is frozen on this chapter until promotion. Other
versions cannot also check it out.

#### Draft

A status indicating a chapter file exists but is not yet authoritative.
Plans may not cite a `draft` chapter as ground truth. The transition
`placeholder → draft → active` is the typical lifecycle for a new
chapter; the librarian and the promote-version command are the only
agents authorized to make these transitions.

#### ARC-100

**The name of this system.** Pronounced "Gen one hundred." The "100"
is borrowed from ATA 100's soft cap and serves the same purpose. The
canonical specification is `00-00_ARC-100_General.md`; the canonical
chapter list is `00-01_ARC-100_Standard_Inventory.md`; this glossary is `00-02`.
A project adopting ARC-100 typically renames its instance to
`<PROJECT>-100` (e.g., `FLOW-100`, `CS-100`).

#### ARC-100.N (version)

The version number of the index itself. **ARC-100.1** is the initial
version. A ARC-100.2 (or higher) is reserved for a full reindex —
re-purposing existing book or chapter numbers. Adding new chapters in
unused slots does NOT bump the version (that is append-only allocation,
normal operation). See §00-00.2.

#### Hard rules

The non-negotiable invariants every ARC-100 agent must obey, listed in
§00-00.11. Examples: only the librarian may add to `00-01`;
only the promote-version command may write to `docs/master/`; subagents
that need a chapter ruling must emit `LIBRARIAN_REQUIRED:` and return.

#### Librarian

The subagent responsible for chapter-identity questions and maintenance
of `00-01 ARC-100 Index`. The librarian resolves "what chapter does
concept X belong to?", performs check-out from master to the active
version, and returns one of four ruling kinds (`existing_chapter`,
`new_chapter`, `new_book`, `check_out_recommended`). The librarian is
the **only** agent authorized to add to the index. A project adopting
ARC-100 typically names this agent `<project>-100-librarian`.

#### LIBRARIAN_REQUIRED

The escalation token a subagent emits when it encounters a chapter-
identity question it cannot answer autonomously. The parent receives
the token, dispatches the librarian, and re-invokes the original
agent with the ruling pre-resolved. The parent owns the loop because
subagents cannot dispatch subagents.

#### Master

The canonical archive at `docs/master/architecture/`. Every ARC-100
chapter that is not currently checked out to a version lives here.
**Only the promote-version command may write to master**, with one
carve-out: the librarian may update `00-01` index entries to record
check-outs. Master is always-trustworthy by construction — the
strictness is the point.

#### Promote-version

The slash command that promotes a version's checked-out chapters back
to master and (optionally, with `--next <slug>`) opens a new active
version. Combines version-completion and next-activation into one
workflow.

#### Reserved chapter

A chapter in the `00-XX` range that documents the ARC-100 system
itself. The reserved chapters are:

- `00-00 ARC-100 General` — system specification
- `00-01 ARC-100 Index` — chapter list
- `00-02 ARC-100 Glossary` — this chapter
- `00-03..00-99` — reserved for future cross-cutting documentation-
  system concerns; do not allocate without deliberation.

#### Source-of-truth integrity

The principle that the YAML block in `00-01_ARC-100_Standard_Inventory.md` is the
single authoritative source for chapter identity. Generated views (the
home-page tree, mkdocs nav, agent reports) are **derivatives**; the
YAML is canonical. Marker-based extraction
(`<!-- ARC-100-INDEX-START --> ... <!-- ARC-100-INDEX-END -->`)
exists so machine consumers never depend on prose around the block.

#### Status (ARC-100 sense)

The lifecycle state of a chapter, drawn from a fixed taxonomy:
`placeholder`, `draft`, `active`, `checked-out-to-vN`, `superseded`,
`deprecated`. See §00-00.6 for the lifecycle diagram. Only the
librarian and the promote-version command may transition status; other
agents read it.

#### Superseded

A status indicating a chapter has been replaced by another (referenced
via `superseded_by` in the index entry). The superseded chapter is
kept for history and not loaded as agent context. Distinct from
**deprecated**, which means "removed entirely."

#### Two-level numbering (ARC-100 sense)

The ARC-100 numbering structure: book at the first level
(`<book-id>`, e.g. `40`), chapter at the second level
(`<book-id>-<chapter-id>`, e.g. `40-01`). Sections within a chapter are
freeform markdown headings — there is **no third structured level**.

#### Version (ARC-100 sense)

A documentation version slug like `v4`, `v5`. A version's folder
(`docs/versions/<slug>/architecture/`) holds chapters checked out from
master for modification. When a version completes,
the promote-version command returns those chapters to master.

> **Disambiguation**: not the same as **ARC-100.N**. ARC-100.N is the
> version of the *index system*; `vN` is the version of the
> *application/architecture* using the index.

### 00-02.3 — Term-collision table

A quick-reference for the two terms that collide most often with
general English:

| Term | General English | ARC-100 sense |
|---|---|---|
| **Book** | A bound publication. | A two-digit numbered container in the index (`40`, `93`); has no `.md` file. |
| **Chapter** | A section of a book or document. | A two-level-numbered `.md` file with content (`40-01`, `93-02`). |

When in doubt, "book" and "chapter" in any ARC-100 documentation refer
to the ARC-100 sense above. The application's own glossary (planned
location: `10-01 General Glossary`) uses neither term in the ARC-100
sense; if you see "chapter" outside ARC-100 documentation, it
typically means a section of a doc, not an `.md` file.

### 00-02.4 — Pointers

- **System spec**: [`00-00_ARC-100_General.md`](00-00_ARC-100_General.md)
- **Chapter index**: [`00-01_ARC-100_Standard_Inventory.md`](00-01_ARC-100_Standard_Inventory.md)
- **Application glossary** (planned location):
  `10-01 General Glossary` — distinct from this glossary, scoped to the
  application's domain (workflows, processes, parameters, etc.).

---

> **Maintenance.** When new ARC-100-specific terminology is
> introduced, add it to §00-02.2. When generic preemptive-indexing
> conventions are clarified, add to §00-02.1. Cross-link any term that
> has both a generic and a ARC-100 meaning. Removed or renamed terms
> stay in the glossary with a `> Renamed to:` or `> Removed:`
> annotation — do not silently delete vocabulary that historical docs
> may still reference.
