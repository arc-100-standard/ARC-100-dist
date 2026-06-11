---
title: 00-07 ARC-100 Getting Started
arc_100_id: "00-07"
status: active
keywords: [getting-started, install, onboarding, adopt, downstream, conform, likec4, agents]
agent_summary: |
  The single a-priori onboarding chapter for adopting ARC-100 in a
  project. Covers what ARC-100 and a `<PROJECT>-100` instance are, how
  to install ARC-100-SYNC (prerequisites, the curl one-liner, post-install
  copy steps), the first conform run and keeping the standard current,
  where a project's own books and chapters go, the two Claude Code agents
  (arc-100-librarian, likec4-author), removal, and troubleshooting. It is
  deliberately concise: the depth lives in the chapters it links to
  (00-00 numbering/lifecycle, 00-05 synchronization, 00-06 architectural
  modeling), which a reader of the rendered site can open directly.
prerequisites: ["00-00_ARC-100_General.md"]
companions: ["00-05_ARC-100_Synchronization.md", "00-06_ARC-100_Architectural_Modeling.md"]
---

## 00-07 ARC-100 Getting Started

> **What this chapter is.** The one place to start when you want to give
> some *other* software project a well-organized, machine-indexable
> documentation tree using ARC-100. No prior ARC-100 experience is
> assumed. By the end you will have installed the toolkit, run your first
> sync, and know where your own docs go and which agents write them.
>
> **What this chapter is not.** A deep reference. It states the essentials
> and links to the chapters that own the detail —
> [00-00 General](00-00_ARC-100_General.md) (numbering, bands, lifecycle,
> hard rules), [00-05 Synchronization](00-05_ARC-100_Synchronization.md)
> (the conform engine), and
> [00-06 Architectural Modeling](00-06_ARC-100_Architectural_Modeling.md)
> (LikeC4). Open those for anything this chapter summarises.

### 00-07.1 — What ARC-100 is, and what a `<PROJECT>-100` is

**ARC-100** is two things working together:

1. **A documentation-indexing standard** — a fixed, numbered chapter
   scheme (books and chapters grouped into seven topic *bands*), a
   machine-parseable master index, an immutable-ULID identity model, and
   conventions for embedding C4 architecture diagrams. The standard ships
   as the "Book 00" chapters (`00-00`…`00-07`). See
   [00-00 General](00-00_ARC-100_General.md) for the full specification
   and [00-02 Glossary](00-02_ARC-100_Glossary.md) for vocabulary.
2. **A sync toolkit (ARC-100-SYNC)** — a runtime-light bundle of shell +
   Python scripts, Claude Code agent and slash-command templates, and a
   LikeC4 modeling toolchain that installs the standard into your repo and
   keeps it in step with upstream as the standard evolves
   ([00-05 Synchronization](00-05_ARC-100_Synchronization.md)).

When you adopt ARC-100 you create **your project's own instance**, named
`<PROJECT>-100` — e.g. `FLOW-100`, `CS-100`, `ACME-100`. Your instance
*inherits* the Book 00 chapters verbatim (kept fresh by the conform
engine) and *adds* your own books and chapters in the slots the standard
reserves for you (§00-07.5).

| Thing | Where it lands | Who owns it |
| --- | --- | --- |
| The Book 00 standard chapters | `docs/00/00-00…00-07_*.md` | Upstream (synced; do not hand-edit) |
| Your master index | `docs/00/00-01_<PROJECT>-100_Index.md` | The librarian agent only |
| Your project chapters | `docs/01/`, `docs/02/`, `docs/10/`, … | You |
| LikeC4 architecture model | `architecture/LikeC4/<project>.c4` | You (via `likec4-author`) |
| The sync toolkit | `ARC-100-SYNC/` | Upstream (overwritten on reinstall) |
| Two agents + two slash commands | `.claude/agents/`, `.claude/commands/` | You (copies of templates) |

> **Whose rule is "do not hand-edit"?** This table describes *your*
> downstream `<PROJECT>-100`: there, Book 00 is a synced, **read-only
> mirror**, so the conform engine — not you — maintains it. Inside the
> ARC-100 standard's *own* repository, Book 00 is the source of record and
> is authored directly. See the hard rule in 00-00 §00-00.11.

### 00-07.2 — Install ARC-100-SYNC

**Prerequisites.**

- **macOS** — v1 of the installer is macOS-only. On any non-Darwin
  platform it exits cleanly with **code 2** *before fetching anything*
  ("platform support is planned but not yet implemented"). Linux /
  Windows-WSL are reserved in the layout but not yet built.
- **`curl`** and **Python 3.10+** (the conform engine, the ULID
  generator, and mkdocs all run on Python).
- **Node ≥ 22** (v24.x recommended) — required by the LikeC4 toolchain
  (`likec4@~1.57.0`). The installer detects Node and **prompts before**
  installing it via Homebrew or `nvm` — never silently.
- **No `git`, `gh`, or npm needed to bootstrap.**

**The one-line install** (run from the root of your project repo).

Two choices shape the command. First, **how you reach the ARC-100
repository**: a *public* repository (anyone can fetch it; no credentials)
or a *private* one (only granted users can fetch it; needs a token).
Second, **which version** you download: a pinned version (Option A) or the
moving latest (Option B). The version choice is identical in both access
modes — only the fetch host and the credential differ. The *same*
`install.sh` handles both: it takes the authenticated path the moment a
token is present in the environment, and the public path otherwise. There
is no separate installer.

> **Which access mode applies to me?** The canonical upstream
> `titanium4638/ARC-100` is **currently a private repository**, so today
> the **private (authenticated)** commands below are the ones that
> resolve. The public commands are for when a repository hosting ARC-100
> is public — your own fork, an internal mirror, or the canonical repo if
> it is opened later.

#### 00-07.2.1 — Install from a public repository

> **Note — `titanium4638/ARC-100` is NOT yet public.** These commands
> fetch over `raw.githubusercontent.com`, which serves only *public*
> repositories. Against the canonical (private) upstream they **404** —
> use the **private** commands in [§00-07.2.2](#00-0722--install-from-a-private-repository)
> instead. Use the public commands only against a repository you have
> made public (e.g. your own fork or mirror).

*Option A — install a specific version (recommended for real projects).*
This downloads one exact version (below, `ARC-100.1`) and stays on it: run
the same command tomorrow, next month, or next year and you get the
*identical* files — nothing shifts underneath you. You move to a newer
version on your own schedule, by changing the version number when you are
ready.

```bash
UPSTREAM_TAG=ARC-100.1 bash <(curl -sSL --fail --proto '=https' --tlsv1.2 --max-redirs 2 \
  https://raw.githubusercontent.com/titanium4638/ARC-100/ARC-100.1/ARC-100-SYNC/scripts/install.sh)
```

*Option B — always install the latest (handy for trying it out).* This
follows a "latest" pointer, so each run gives you the newest release —
which may differ from what you got last time. It is the fastest way to
kick the tires; switch to Option A once you are past experimenting.

```bash
bash <(curl -sSL --fail --proto '=https' --tlsv1.2 --max-redirs 2 \
  https://raw.githubusercontent.com/titanium4638/ARC-100/ARC-100-CURRENT/ARC-100-SYNC/scripts/install.sh)
```

> **Not sure which?** Use **Option A** with the current version number.
> You can re-run the installer any time to move to a newer version.

#### 00-07.2.2 — Install from a private repository

This is the path that resolves against the canonical upstream **today**.
It fetches over the GitHub **Contents API** at `api.github.com` with a
**Bearer token**, so it never touches `raw.githubusercontent.com`. The
*same* `install.sh` auto-selects this path the instant a token is present
in the environment.

*Prerequisite — a token with read access.* Provide a GitHub token in the
environment as `GH_TOKEN` (or `GITHUB_TOKEN`). The simplest source is the
GitHub CLI: `gh auth token`. Prefer a **fine-grained, read-only,
single-repository Personal Access Token** scoped to just the ARC-100
repository (Contents: Read-only) — the least-privilege credential for the
job. The token is read from the environment **only**: it is never passed
on the command line (where `ps` could see it), never written to disk, and
never echoed.

*Access-grant model — how a person gets read access.* The repository owner
grants read access by one of:

- **Repository collaborator** — invite the user as a read collaborator
  (Settings → Collaborators), for a personal-account repo.
- **Organisation team** — add the user to a team with Read on the
  repository, for an org-owned repo.
- **Fine-grained PAT** — the granted user mints a fine-grained,
  read-only, single-repo token (recommended for automation/CI).
- **Deploy key** — a read-only deploy key for a machine context that
  should not carry a user identity.

*Option A — pinned version (recommended).* Export the token once, then run
the bootstrap. The outer fetch passes the token to `curl` through a `-K`
config on **stdin** (never argv), and the exported `GH_TOKEN` is inherited
by `install.sh` so its own per-file fetches authenticate too:

```bash
export GH_TOKEN=$(gh auth token)
UPSTREAM_TAG=ARC-100.1 bash <(
  printf 'header = "Authorization: Bearer %s"\n' "$GH_TOKEN" |
  curl -sSL --fail --proto '=https' --tlsv1.2 --max-redirs 0 \
    -H "Accept: application/vnd.github.raw" -H "X-GitHub-Api-Version: 2022-11-28" -K - \
    "https://api.github.com/repos/titanium4638/ARC-100/contents/ARC-100-SYNC/scripts/install.sh?ref=ARC-100.1"
)
```

*Option B — always install the latest.* Identical, with the moving tag:

```bash
export GH_TOKEN=$(gh auth token)
UPSTREAM_TAG=ARC-100-CURRENT bash <(
  printf 'header = "Authorization: Bearer %s"\n' "$GH_TOKEN" |
  curl -sSL --fail --proto '=https' --tlsv1.2 --max-redirs 0 \
    -H "Accept: application/vnd.github.raw" -H "X-GitHub-Api-Version: 2022-11-28" -K - \
    "https://api.github.com/repos/titanium4638/ARC-100/contents/ARC-100-SYNC/scripts/install.sh?ref=ARC-100-CURRENT"
)
```

> **Prefer `gh`?** If you have the GitHub CLI, the outer fetch can be the
> shorter `bash <(gh api -H "Accept: application/vnd.github.raw"
> "/repos/titanium4638/ARC-100/contents/ARC-100-SYNC/scripts/install.sh?ref=ARC-100.1")`
> — `gh` supplies the credential itself (nothing in `ps`). Keep the
> `export GH_TOKEN=$(gh auth token)` line so the installer authenticates
> its own per-file fetches.

The authenticated fetch uses `--max-redirs 0` on purpose: a redirect must
not be allowed to carry the `Authorization` header off `api.github.com` to
another host. The public fetch keeps `--max-redirs 2`; the two modes are
deliberately host-disjoint. See [00-05 §00-05.11](00-05_ARC-100_Synchronization.md)
for the full security posture.

**What "a version" pins — and what still changes.** A version fixes the
**chapter index**: the set of ARC-100 chapter slots (their IDs, bands, and
stable ULIDs). That is the part your `<PROJECT>-100` builds on top of, so
it stays put until you choose to move. The **content** of the Book 00
chapters (the ARC-100 standard's own text, which you do not edit inside
your project) is delivered by the installer and refreshed when you re-run
it — see "Keeping current" in [§00-07.4](#00-074--first-sync-and-keeping-arc-100-updated).
You can apply a newer ARC-100 version manually at any time by re-running
the installer with a higher version number, then running
`/conform-to-arc-100`. If a new version's chapters ever collide with
chapters your project has authored, the **arc-100-librarian** agent walks
you through resolving each collision (see [§00-07.6](#00-076--the-two-agents)).

**What the installer sets up for you — and what you set up yourself.**

| Component | Installer's role |
| --- | --- |
| **The ARC-100 toolkit** (conform engine, agents, templates, Book 00 chapters) | **Installed** — downloaded into `ARC-100-SYNC/` and copied into place. |
| **Node.js** (≥ 22, for the LikeC4 diagram tools) | **Offers to install it** — if Node is missing or too old, it asks first, then uses Homebrew or `nvm`. Decline and it skips, leaving a note. |
| **LikeC4 diagram tools** | **Set up automatically** — *only if Node is available* — via `npm ci`. |
| **`curl`** | **Not installed — required already** (it is how the install command runs). |
| **Python 3.10+** | **Not installed — required already** (the conform engine and the docs site both run on it). |
| **mkdocs** (the docs-site builder) and its plugins | **Not installed.** The installer hands you a pinned `requirements.txt` and prints the one command to install them: `python3 -m pip install --user --require-hashes -r requirements.txt`. You run that yourself (it is step 7 of the post-install setup). |

In short: you bring **`curl` + Python 3** before you start; the installer
brings the ARC-100 toolkit and (with your OK) Node; and you finish by
pip-installing mkdocs from the pinned `requirements.txt`.

Either way, the installer downloads the toolkit into `ARC-100-SYNC/`,
copies the starter content into place (anything you have already written
is preserved, never overwritten), and sets up the LikeC4 diagram tools.
If you want the full story — how versioning works, and why running a
script straight from the web is done safely here — see
[00-05 §00-05.9](00-05_ARC-100_Synchronization.md) and
[§00-05.11](00-05_ARC-100_Synchronization.md). The complete list of what
gets installed is in [00-05 §00-05.8](00-05_ARC-100_Synchronization.md).

### 00-07.3 — Post-install setup

The installer prints these steps; do them in order. (Paths under
`ARC-100-SYNC/` are upstream-owned; everything you copy out of it is
yours.)

1. **Agents + slash commands** — `cp ARC-100-SYNC/templates/agents/*.md
   .claude/agents/` and `cp ARC-100-SYNC/templates/commands/*.md
   .claude/commands/` (arc-100-librarian + likec4-author; the two slash
   commands).
2. **Sync config** — copy `ARC-100-SYNC/templates/config/ARC-100-SYNC.config.example.yml`
   to `ARC-100-SYNC.config.yml` at the repo root and edit two lines:
   `project_name: <PROJECT>-100` (must be a case-insensitive substring of
   `mkdocs.yml`'s `site_name`, or the conform engine refuses to run) and
   `local_index_path: docs/00/00-01_<PROJECT>-100_Index.md`.
3. **Site config** — `cp ARC-100-SYNC/templates/config/mkdocs.yml.template
   mkdocs.yml`; edit the `<PROJECT>` / `<PROJECT_DESC>` placeholders and
   tune the `not_in_nav` globs to your book numbers.
4. **Master-index hook** — `cp ARC-100-SYNC/templates/hooks/arc100_master_index.py
   _hooks/` (generates your rendered home page and prepends the
   critical-decisions banner). Your home renders as `"<PROJECT>-100 Index"`.
5. **Home-page assets + fonts** — `cp -r ARC-100-SYNC/templates/assets/arc100
   assets/arc100` (the styles, light/dark themes, and Inter fonts the
   `mkdocs.yml` references).
6. **Standalone Architectural-Model page** — `cp
   ARC-100-SYNC/templates/docs/architectural-model.md.template
   docs/00/architectural-model.md`; edit the `<PROJECT>` title and the
   `project=<slug>` fence argument.
7. **Python deps** — `python3 -m pip install --user --require-hashes -r
   requirements.txt` (the `--require-hashes` flag is non-negotiable; the
   installer never runs pip for you).
8. **LikeC4 placeholders** (only if you will author a model — §00-07.6) —
   set the `name` field to your project slug in both
   `architecture/LikeC4/package.json` and
   `docs/00/model/likec4.config.json`, then verify with
   `architecture/LikeC4/bin/likec4 --version` (expect 1.57.0) and
   `… validate` (expect ✓ Valid).
9. **(Optional) sync-check hook** — `cp
   ARC-100-SYNC/templates/hooks/arc100_sync_check.py _hooks/` and register
   it in `mkdocs.yml` under `hooks:` so every mkdocs startup re-checks
   sync ([§00-05.10](00-05_ARC-100_Synchronization.md)).

### 00-07.4 — First sync, and keeping ARC-100 updated

In Claude Code, run `/conform-to-arc-100`. The engine auto-detects its
mode:

- **Bootstrap** (your index does not exist yet): copies the upstream
  index verbatim, swaps the marker pair to `<PROJECT>-100-INDEX`, and
  exits `0` — no decisions.
- **Update** (your index exists): diffs upstream against your local index
  **keyed by ULID** (so a renumber reads as a move, not a delete-plus-add),
  auto-applies the safe changes, and queues the judgment-bound ones.

**Exit codes:** `0` clean · `1` decisions queued (run
`/resolve-arc-100-issues`) · `2` hard error. Four classes auto-apply
(capped at 20/run); six queue for human review. The full classification
tables and the two-mode contract live in
[00-05 §00-05.4](00-05_ARC-100_Synchronization.md) and
[§00-05.5](00-05_ARC-100_Synchronization.md); the pending-decisions
banner and resolution flow are in
[§00-05.6](00-05_ARC-100_Synchronization.md).

**Keeping current.** Re-run the installer to pick up new files. Discipline:

- `ARC-100-SYNC/` is upstream-owned — re-running overwrites it; never
  edit files there.
- Files you own are never touched: `.claude/`, `ARC-100-SYNC.config.yml`,
  `_hooks/`, `mkdocs.yml`, `assets/arc100/`, `docs/architectural-model.md`,
  and `ARC-100-SYNC/state/`.
- Canonical-location files (including the Book 00 chapters under
  `docs/00/`) are preserved on a re-run: if a file you authored would be
  overwritten, the installer moves your copy aside into a timestamped
  backup folder and reports it, rather than clobbering it. To pull a fresh
  copy of a Book 00 chapter, delete the target first, then re-run. After
  updating, re-copy the agent/command templates into `.claude/`, then run
  `/conform-to-arc-100` to flow any new index changes in.

### 00-07.5 — Where your `<PROJECT>-100` documentation goes

Files follow `<book>-<chapter>_<title>.md` with two-digit zero-padded
numbers (e.g. `40-50_Architecture_Reference.md`); section headings inside
a chapter follow `### BB-CC.N — Title`; cite other chapters as
`[BB-CC §N]`. Every book number falls into one of seven bands
(Application, Governance, Client, Server, Data, Tooling, Operations) —
the band table and the four structural rules are in
[00-00 §00-00.7](00-00_ARC-100_General.md).

The two rules you will use constantly:

- **Chapters in an inherited (`arc_100: true`) book:** ARC-100 uses slots
  01–49; **you allocate from 50 upward.**
- **New project books in a band:** ARC-100 allocates from the low end;
  **you allocate from the high end and work downward** (99, 98, …). This
  minimises rebase collisions when the standard adds a book.

Each index entry carries an immutable `arc_100_ulid` (the join key the
conform engine matches on — never invent or edit one by hand) and a
`status` (`placeholder` → `draft` → `active` → `superseded`/`deprecated`).
Only the librarian (§00-07.6) writes the index or changes status. You do
not migrate everything at once: bootstrap ARC-100 alongside your existing
tree and bulk-migrate legacy docs as a single planned operation at version
closeout ([00-00 §00-00.10](00-00_ARC-100_General.md)).

### 00-07.6 — The two agents

ARC-100 ships two Claude Code agents you drive by asking questions; they
do the disciplined parts so you do not memorise the rules.

- **`arc-100-librarian` — the only writer of the index.** It does
  chapter-identity rulings, slot allocation, ULID minting, schema sweeps,
  and resolution of queued sync decisions. You never invent a chapter
  number; you ask the librarian ("Where does concept X belong?" /
  "Allocate the next chapter in band 40") and it commits the entry. It
  emits one of three ruling shapes (`existing_chapter`, `new_chapter`,
  `new_book` — the last is a halt for human review) and never allocates a
  new book autonomously, edits chapter content, renames an `arc_100: true`
  chapter, or mutates a ULID by hand.
- **`likec4-author` — the architecture model.** It authors the LikeC4 DSL
  model, defines views, applies theme/styling, and produces the
  `likec4-view` fences you embed in chapters. The element vocabulary, view
  taxonomy, theming, embedding mechanics, hosting-cost disciplines, and a
  full worked example are in
  [00-06 Architectural Modeling](00-06_ARC-100_Architectural_Modeling.md).

The migration loop ties them together: ask the librarian to place an
existing doc as a chapter → author the chapter body → ask `likec4-author`
to model the system and embed per-chapter views → `mkdocs build --strict`
→ `/conform-to-arc-100` keeps the inherited standard fresh over time.

### 00-07.7 — Removing ARC-100-SYNC

```bash
rm -rf ARC-100-SYNC/
rm .claude/agents/arc-100-librarian.md .claude/agents/likec4-author.md
rm .claude/commands/conform-to-arc-100.md .claude/commands/resolve-arc-100-issues.md
rm ARC-100-SYNC.config.yml
rm _hooks/arc100_sync_check.py    # if you registered it
```

Then remove the `_hooks/arc100_sync_check.py` line from `mkdocs.yml`. Your
own chapters, `mkdocs.yml`, and `assets/` are untouched.

### 00-07.8 — Troubleshooting

- **Network failures** are non-fatal: the conform engine logs and exits
  `0`, leaving the index untouched; the next tick retries.
- **`project_name` vs `site_name` mismatch** — the engine reads
  `mkdocs.yml`'s `site_name` and matches it against the config's
  `project_name`; if they disagree it refuses to run with a clear error.
  Edit one so they agree.
- **Malformed upstream rows** (HTML, control bytes, descriptions > 200
  chars) are refused at the boundary and queued under `malformed_upstream`
  — they never auto-apply ([§00-05.5](00-05_ARC-100_Synchronization.md)).
- **Banner renders as raw `##` text** — the banner `<div>` needs
  `markdown="1"` for Python-Markdown's `md_in_html`
  ([§00-05.6](00-05_ARC-100_Synchronization.md)).
- **Sync-check hook seems silent** — it is fire-and-forget by design;
  watch it with `tail -f ARC-100-SYNC/state/sync_check.log` (the `state/`
  directory is gitignored).

### 00-07.9 — Pointers

- [00-00 General](00-00_ARC-100_General.md) — numbering, the band table,
  status lifecycle, ULID/lineage rules, and the §00-00.11 hard rules.
- [00-03 Documentation Site](00-03_ARC-100_Documentation_Site.md) — the
  mkdocs rendering layer and theme conventions.
- [00-05 Synchronization](00-05_ARC-100_Synchronization.md) — the conform
  engine, the two modes, classifications, the security/TOFU posture.
- [00-06 Architectural Modeling](00-06_ARC-100_Architectural_Modeling.md)
  — LikeC4 conventions, the view taxonomy, embedding, and the Inter
  typography schedule.
- [Architectural Model](architectural-model.md) — the interactive C4
  SystemContext view of ARC-100-SYNC.

### 00-07.10 — Current limitations

- **macOS-only (v1).** The installer exits cleanly (code 2) on Linux /
  Windows-WSL; those platforms are reserved but not yet implemented.
- **Diagram fonts fall back outside the standard's CSS.** LikeC4 1.57.0
  has no font-family theme primitive, so the Inter weight schedule is a
  CSS override; environments that do not load
  `docs/00/assets/likec4-typography.css` see the default font.
- **A few setup steps are deliberately manual** (config placement, the
  mkdocs/hook/asset copies, the `<PROJECT>` edits, and `pip`) — they are
  one-time human decisions, not curl-one-liner automation.

## Revisions

| Date | Change |
| --- | --- |
| 2026-05-30 | Initial creation. Consolidates the two previously-fragmented a-priori onboarding documents — the standalone `website/GETTING_STARTED.md` and the offline `ARC-100-SYNC/docs/README.md` — into a single Book 00 chapter that renders on the ARC-100 site and links to 00-00 / 00-05 / 00-06 for depth rather than duplicating them. Folds in the Removal and Troubleshooting material that previously lived only in `ARC-100-SYNC/docs/README.md`. Allocated at 00-07 via the `arc-100-librarian`; distributed to downstreams as part of Book 00. |
| 2026-06-01 | Revision 2: phase 6b threat-modeler hardening. Hardened both documented bootstrap one-liners in §00-07.2 (Option A pinned-version + Option B latest) from a bare `curl -sSL` to `curl -sSL --fail --proto '=https' --tlsv1.2 --max-redirs 2` — matching `install.sh`'s already-pinned internal per-file fetches (TM-2b-2) and its L5 usage comment. Closes a protocol-downgrade / off-host-redirect gap on the *outer* bootstrap fetch, and lets the phase-6b published-install gate (`test_publish.sh`) exercise the EXACT flag string real adopters run (the "gate tests the real path" requirement). Distributed `templates/book-00/00-07` twin updated byte-identically. No change to install behaviour or chapter content. See `versions/v1/implementation/phase_6b.md`. |
| 2026-06-01 | Revision 3: clarified the context-based switch on the "do not hand-edit Book 00" directive (user direction). Added a note after the §00-07 ownership table making explicit that the table — and its "do not hand-edit" guidance — describes a *downstream* `<PROJECT>-100`, where Book 00 is a synced read-only mirror the conform engine maintains; inside the ARC-100 standard's *own* repository Book 00 is the source of record and is authored directly. Cross-references the canonical hard rule newly added to 00-00 §00-00.11. No install-behaviour or numbering change. Distributed twin updated byte-identically. |
| 2026-06-01 | Revision 4: phase 7 authenticated private-repo install. Split §00-07.2 into §00-07.2.1 — Install from a public repository (the existing Option A/B `raw.githubusercontent.com` commands, with a prominent note that `titanium4638/ARC-100` is NOT yet public, so those 404 against the canonical upstream) and §00-07.2.2 — Install from a private repository (the authenticated path that resolves today: `GH_TOKEN=$(gh auth token)`, `api.github.com` Contents API, Bearer token via a `curl -K` stdin config so the token never touches argv/disk, `--max-redirs 0` so a redirect cannot carry the auth header off-host, the collaborator/Team/fine-grained-PAT/deploy-key access-grant model, and a `gh api` convenience). The *same* `install.sh` auto-selects authenticated vs public by token presence — no second installer. No numbering change to existing sections (anchors preserved); two new `BB-CC.N.M` subsections added. Distributed `templates/book-00/00-07` twin updated byte-identically. See `versions/v1/implementation/phase_7.md`. |
