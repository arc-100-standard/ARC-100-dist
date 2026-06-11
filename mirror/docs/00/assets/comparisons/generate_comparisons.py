#!/usr/bin/env python3
"""Generate ARC-100 vs standard Venn comparison SVGs.

Run: python3 tmp/generate_comparisons.py
Output: tmp/comparison_*.svg
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

OUTPUT_DIR = Path(__file__).parent

CANVAS_W = 900
CANVAS_H = 720
ARC_CX = 370
ARC_CY = 240
ARC_R = 160


@dataclass
class Standard:
    key: str
    name: str
    subtitle: str
    topic_count_label: str
    overlap_std_pct: int       # % of standard covered by ARC-100
    overlap_arc_pct: int       # % of ARC-100 covered by standard
    std_radius: int
    std_cx: int
    std_label_x: int           # external label x position
    overlap_text: str          # one-line description of the overlap counts
    arc_only: List[str] = field(default_factory=list)
    shared: List[str] = field(default_factory=list)
    std_only: List[str] = field(default_factory=list)


STANDARDS: List[Standard] = [
    Standard(
        key="01_arc42",
        name="arc42",
        subtitle="Widely-used architecture documentation template (12 sections)",
        topic_count_label="12 sections",
        overlap_std_pct=75,
        overlap_arc_pct=12,
        std_radius=53,
        std_cx=480,
        std_label_x=620,
        overlap_text="9 of 12 arc42 sections find a home in ARC-100",
        arc_only=[
            "Client band (20-21)",
            "Data band (60-66)",
            "Tooling band (80-86)",
            "API contract detail (Book 42)",
            "Wire shapes (Book 62)",
            "Audit (48, 64)",
            "Compliance / SCA (94, 95)",
        ],
        shared=[
            "Goals & identity (01)",
            "ADRs (12)",
            "Building blocks (40-03)",
            "Runtime view (40-02, 41)",
            "Deployment view (92)",
            "Cross-cutting (93)",
            "Glossary (00-02, 10-01)",
        ],
        std_only=[
            "Context & system boundary",
            "Quality requirements (NFRs)",
            "Risks & technical debt",
            "Quality scenarios",
        ],
    ),
    Standard(
        key="02_c4",
        name="C4 model",
        subtitle="Structural decomposition only: System Context to Code (4 levels)",
        topic_count_label="4 levels",
        overlap_std_pct=100,
        overlap_arc_pct=5,
        std_radius=30,
        std_cx=490,
        std_label_x=630,
        overlap_text="All 4 C4 levels are addressed in ARC-100 (conceptually)",
        arc_only=[
            "Everything outside structural views:",
            "  Security, Identity, Audit",
            "  Wire shapes, API contract",
            "  Testing, CI, Repository",
            "  Operations, Compliance",
            "  Application philosophy",
            "  Versioning, Migrations",
        ],
        shared=[
            "System Context (01, 40-01)",
            "Container (40-03 Services)",
            "Component (40-03, 20-02)",
            "Code (80-03 Project Structure)",
        ],
        std_only=[
            "Explicit diagramming notation",
            "Level-specific drawing rules",
            "Modeling-tool conventions",
        ],
    ),
    Standard(
        key="03_4plus1",
        name="4+1 View (Kruchten)",
        subtitle="Five architectural views unified by scenario view (5 views)",
        topic_count_label="5 views",
        overlap_std_pct=100,
        overlap_arc_pct=7,
        std_radius=34,
        std_cx=485,
        std_label_x=625,
        overlap_text="All 5 views map to ARC-100 chapters",
        arc_only=[
            "Security & Identity bands",
            "API contract & Wire shapes",
            "Audit, Compliance, SCA",
            "Testing modes (82, 83, 84)",
            "Repository, CI",
            "Versioning, Migrations",
            "Application philosophy detail",
        ],
        shared=[
            "Logical view (60-01, 40-03)",
            "Process view (40-02, 41)",
            "Development view (80-03, 20-02)",
            "Physical view (92)",
            "Scenarios (01-02, 01-03)",
        ],
        std_only=[
            "Use-case-driven methodology",
            "Viewpoint correspondence rules",
            "Scenario-as-cross-cutter discipline",
        ],
    ),
    Standard(
        key="04_iso42010",
        name="IEEE/ISO/IEC 42010",
        subtitle="Meta-framework for architecture descriptions (structural)",
        topic_count_label="meta-framework",
        overlap_std_pct=70,
        overlap_arc_pct=10,
        std_radius=38,
        std_cx=505,
        std_label_x=640,
        overlap_text="ARC-100 conforms to ~70% of 42010's structural conventions",
        arc_only=[
            "All actual topic content",
            "Concrete book/chapter taxonomy",
            "Status lifecycle",
            "Master/version split",
            "Indexing & numbering rules",
            "Agent-readable index format",
            "Every domain chapter",
        ],
        shared=[
            "Architecture description shape",
            "Viewpoints as bands",
            "Views as chapters",
            "Concerns as book topics",
            "Glossary (00-02)",
        ],
        std_only=[
            "Explicit stakeholder catalog",
            "Model kinds taxonomy",
            "Correspondence rules",
            "Viewpoint definition discipline",
            "AD framework conformance",
        ],
    ),
    Standard(
        key="05_aws_waf",
        name="AWS Well-Architected",
        subtitle="Cloud workload framework (6 pillars, ~40 effective topics)",
        topic_count_label="6 pillars",
        overlap_std_pct=67,
        overlap_arc_pct=28,
        std_radius=97,
        std_cx=495,
        std_label_x=680,
        overlap_text="4 of 6 pillars overlap; Cost & Sustainability absent in ARC-100",
        arc_only=[
            "Application identity (01)",
            "API contract (Book 42)",
            "Wire shapes (Book 62)",
            "Identity / Auth (47, 65)",
            "Audit (48, 64)",
            "Repository (86)",
            "Versioning (13)",
        ],
        shared=[
            "Operational Excellence (90, 91, 92)",
            "Security (93, 47, 84)",
            "Reliability (91, 93-15)",
            "Performance Efficiency (83, 91-02)",
        ],
        std_only=[
            "Cost Optimization (pillar)",
            "Sustainability (pillar)",
            "Cloud-specific lenses",
            "Service-by-service guidance",
            "AWS-vendor tooling",
        ],
    ),
    Standard(
        key="06_swebok",
        name="SWEBOK",
        subtitle="IEEE Software Engineering Body of Knowledge (15 knowledge areas)",
        topic_count_label="15 KAs",
        overlap_std_pct=45,
        overlap_arc_pct=50,
        std_radius=148,
        std_cx=560,
        std_label_x=735,
        overlap_text="~7 of 15 SWEBOK KAs find a substantive home in ARC-100",
        arc_only=[
            "API contract detail (Book 42)",
            "Wire shapes (Book 62)",
            "Auth flows detail (47, 65)",
            "Audit (48, 64)",
            "Deployment topologies (92)",
            "Compliance (94)",
            "SCA (95)",
        ],
        shared=[
            "Design (40, 60, 20 foundations)",
            "Construction (80, 81, 86)",
            "Testing (82, 83, 84)",
            "Maintenance (13, 66)",
            "Configuration Mgmt (86)",
            "Quality (93, 82)",
            "Engineering Process (13, 85)",
        ],
        std_only=[
            "Requirements engineering KA",
            "Engineering Management KA",
            "Engineering Models & Methods",
            "Professional Practice",
            "Engineering Economics",
            "Computing / Math / Eng Foundations",
        ],
    ),
    Standard(
        key="07_itil",
        name="ITIL 4",
        subtitle="IT service management framework (~34 practices)",
        topic_count_label="~34 practices",
        overlap_std_pct=28,
        overlap_arc_pct=18,
        std_radius=110,
        std_cx=555,
        std_label_x=720,
        overlap_text="~9 of 34 ITIL practices have ARC-100 coverage",
        arc_only=[
            "API contract & Wire shapes",
            "Identity / Auth detail",
            "Persistence & Data model",
            "All dev-tooling specifics",
            "Audit (48, 64)",
            "Application philosophy",
            "Testing methodology",
        ],
        shared=[
            "Information Security (93)",
            "Capacity & Performance (91)",
            "Monitoring & Event (90)",
            "Release Management (92, 86-06)",
            "Deployment (92)",
            "Architecture Management (ARC-100)",
            "Software Dev & Mgmt (80-89)",
        ],
        std_only=[
            "Incident Management",
            "Problem Management",
            "Change Enablement",
            "Service Desk",
            "Service Catalogue",
            "Service Continuity",
            "IT Asset Mgmt",
            "Supplier & Strategy Mgmt",
            "Workforce & Talent Mgmt",
        ],
    ),
    Standard(
        key="08_owasp_samm",
        name="OWASP SAMM",
        subtitle="Software Assurance Maturity Model (5 functions, 15 practices)",
        topic_count_label="15 practices",
        overlap_std_pct=67,
        overlap_arc_pct=17,
        std_radius=70,
        std_cx=510,
        std_label_x=655,
        overlap_text="10 of 15 SAMM practices have ARC-100 coverage",
        arc_only=[
            "Everything outside security:",
            "  API contract, Wire shapes",
            "  Identity bands (47, 65)",
            "  Data, Migrations",
            "  Testing modes (82, 83)",
            "  Repository (86), CI (85)",
            "  Versioning, Audit",
        ],
        shared=[
            "Policy & Compliance (94, 93-12)",
            "Security Requirements (93)",
            "Secure Architecture (93-01)",
            "Secure Build (93-08, 85)",
            "Secure Deployment (92)",
            "Security Testing (84)",
            "Defect Mgmt (95-01)",
            "Environment / Ops Mgmt (80, 90-92)",
        ],
        std_only=[
            "Strategy & Metrics",
            "Education & Guidance",
            "Threat Assessment",
            "Architecture Assessment",
            "Incident Management",
        ],
    ),
    Standard(
        key="09_dora",
        name="DORA / Accelerate",
        subtitle="High-performance engineering capabilities (24 capabilities)",
        topic_count_label="24 capabilities",
        overlap_std_pct=46,
        overlap_arc_pct=17,
        std_radius=88,
        std_cx=525,
        std_label_x=670,
        overlap_text="11 of 24 DORA capabilities map to ARC-100",
        arc_only=[
            "API contract (Book 42)",
            "Wire shapes (Book 62)",
            "Identity / Auth (47, 65)",
            "Audit (48, 64)",
            "Compliance (94)",
            "SCA (95)",
            "Application philosophy (01)",
        ],
        shared=[
            "Version Control (86)",
            "Trunk-Based Dev (86-03)",
            "CI (85)",
            "Deployment Automation (85, 92)",
            "Test Automation (82)",
            "Test Data Mgmt (82-05)",
            "Shift-Left Security (84, 93)",
            "Loosely Coupled Arch (40-03)",
            "Monitoring (90)",
            "Database Change Mgmt (66)",
            "Code Maintainability (81, 82)",
        ],
        std_only=[
            "Empowered Teams",
            "Customer Feedback",
            "Value Stream Visibility",
            "Working in Small Batches",
            "Lightweight Change Approval",
            "Limit WIP / Visual Mgmt",
            "Westrum Org Culture",
            "Job Satisfaction",
            "Transformational Leadership",
        ],
    ),
]


def render(s: Standard) -> str:
    """Render a single ARC-100 vs Standard Venn SVG."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
        f'width="{CANVAS_W}" height="{CANVAS_H}">'
    )
    lines.append("""  <style>
    .bg { fill: #f2f2f2; }
    .title { font: bold 22px -apple-system, Segoe UI, sans-serif; fill: #111; }
    .subtitle { font: 13px -apple-system, Segoe UI, sans-serif; fill: #666; }
    .arc-lbl { font: bold 14px -apple-system, Segoe UI, sans-serif; fill: #1e40af; }
    .std-lbl { font: bold 14px -apple-system, Segoe UI, sans-serif; fill: #991b1b; }
    .count { font: 11px -apple-system, Segoe UI, sans-serif; fill: #555; }
    .pct-lbl { font: bold 14px -apple-system, Segoe UI, sans-serif; fill: #111; }
    .pct-val { font: 13px -apple-system, Segoe UI, sans-serif; fill: #333; }
    .col-h { font: bold 13px -apple-system, Segoe UI, sans-serif; }
    .col-h-arc { fill: #1e40af; }
    .col-h-shared { fill: #333; }
    .col-h-std { fill: #991b1b; }
    .item { font: 11px -apple-system, Segoe UI, sans-serif; }
    .item-arc { fill: #1e40af; }
    .item-shared { fill: #333; }
    .item-std { fill: #991b1b; }
    .arc-circ { fill: #2563eb; fill-opacity: 0.16; stroke: #1e40af; stroke-width: 2; }
    .std-circ { fill: #dc2626; fill-opacity: 0.16; stroke: #991b1b; stroke-width: 2; }
  </style>""")

    lines.append(
        f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" class="bg"/>'
    )
    lines.append(
        f'  <text x="{CANVAS_W // 2}" y="35" text-anchor="middle" class="title">'
        f'ARC-100 vs {escape(s.name)}</text>'
    )
    lines.append(
        f'  <text x="{CANVAS_W // 2}" y="58" text-anchor="middle" class="subtitle">'
        f'{escape(s.subtitle)}</text>'
    )

    # Circles
    lines.append(
        f'  <circle cx="{ARC_CX}" cy="{ARC_CY}" r="{ARC_R}" class="arc-circ"/>'
    )
    lines.append(
        f'  <circle cx="{s.std_cx}" cy="{ARC_CY}" r="{s.std_radius}" class="std-circ"/>'
    )

    # Circle labels (above)
    lines.append(
        f'  <text x="{ARC_CX - ARC_R + 10}" y="85" class="arc-lbl">ARC-100</text>'
    )
    lines.append(
        f'  <text x="{ARC_CX - ARC_R + 10}" y="102" class="count">'
        f'~110 chapters across 7 bands</text>'
    )
    lines.append(
        f'  <text x="{s.std_label_x}" y="85" class="std-lbl">{escape(s.name)}</text>'
    )
    lines.append(
        f'  <text x="{s.std_label_x}" y="102" class="count">'
        f'{escape(s.topic_count_label)}</text>'
    )
    # Leader line from std label to std circle edge
    leader_x = s.std_cx + s.std_radius * 0.7
    leader_y = ARC_CY - s.std_radius * 0.7
    lines.append(
        f'  <line x1="{s.std_label_x + 30}" y1="108" x2="{leader_x:.0f}" '
        f'y2="{leader_y:.0f}" stroke="#991b1b" stroke-width="1" '
        f'stroke-dasharray="3,2" stroke-opacity="0.6"/>'
    )

    # Overlap stats
    overlap_y = 440
    lines.append(
        f'  <text x="{CANVAS_W // 2}" y="{overlap_y}" text-anchor="middle" '
        f'class="pct-lbl">Overlap quantification</text>'
    )
    lines.append(
        f'  <text x="{CANVAS_W // 2}" y="{overlap_y + 22}" text-anchor="middle" '
        f'class="pct-val">{escape(s.overlap_text)}</text>'
    )
    lines.append(
        f'  <text x="{CANVAS_W // 2}" y="{overlap_y + 42}" text-anchor="middle" '
        f'class="pct-val">'
        f'<tspan font-weight="bold">{s.overlap_std_pct}%</tspan> of {escape(s.name)} '
        f'topics map into ARC-100 &#160;&#160;|&#160;&#160; '
        f'<tspan font-weight="bold">{s.overlap_arc_pct}%</tspan> of ARC-100 chapters '
        f'map back to {escape(s.name)}</text>'
    )

    # Three columns
    col_arc_x = 65
    col_shared_x = 370
    col_std_x = 645
    header_y = 530
    item_start_y = 552
    item_dy = 16

    lines.append(
        f'  <text x="{col_arc_x}" y="{header_y}" class="col-h col-h-arc">'
        f'ARC-100 unique</text>'
    )
    for i, item in enumerate(s.arc_only):
        lines.append(
            f'  <text x="{col_arc_x}" y="{item_start_y + i * item_dy}" '
            f'class="item item-arc">{escape(bullet(item))}</text>'
        )

    lines.append(
        f'  <text x="{col_shared_x}" y="{header_y}" class="col-h col-h-shared">'
        f'Shared</text>'
    )
    for i, item in enumerate(s.shared):
        lines.append(
            f'  <text x="{col_shared_x}" y="{item_start_y + i * item_dy}" '
            f'class="item item-shared">{escape(bullet(item))}</text>'
        )

    lines.append(
        f'  <text x="{col_std_x}" y="{header_y}" class="col-h col-h-std">'
        f'{escape(s.name)} unique</text>'
    )
    for i, item in enumerate(s.std_only):
        lines.append(
            f'  <text x="{col_std_x}" y="{item_start_y + i * item_dy}" '
            f'class="item item-std">{escape(bullet(item))}</text>'
        )

    lines.append("</svg>")
    return "\n".join(lines)


def render_summary(standards: List[Standard]) -> str:
    """Render a horizontal-bar summary of all overlaps."""
    n = len(standards)
    row_h = 50
    chart_top = 110
    chart_left = 240
    chart_width = 560
    chart_height = n * row_h + 30
    canvas_h = chart_top + chart_height + 60

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {CANVAS_W} {canvas_h}" '
        f'width="{CANVAS_W}" height="{canvas_h}">'
    )
    lines.append("""  <style>
    .bg { fill: #f2f2f2; }
    .title { font: bold 22px -apple-system, Segoe UI, sans-serif; fill: #111; }
    .subtitle { font: 13px -apple-system, Segoe UI, sans-serif; fill: #666; }
    .row-label { font: bold 13px -apple-system, Segoe UI, sans-serif; fill: #111; text-anchor: end; }
    .axis { font: 11px -apple-system, Segoe UI, sans-serif; fill: #666; }
    .bar-std { fill: #1e40af; }
    .bar-arc { fill: #dc2626; }
    .bar-lbl { font: 11px -apple-system, Segoe UI, sans-serif; fill: #fff; font-weight: bold; }
    .legend { font: 12px -apple-system, Segoe UI, sans-serif; fill: #333; }
    .gridline { stroke: #e5e7eb; stroke-width: 1; }
  </style>""")

    lines.append(
        f'  <rect x="0" y="0" width="{CANVAS_W}" height="{canvas_h}" class="bg"/>'
    )
    lines.append(
        f'  <text x="{CANVAS_W // 2}" y="35" text-anchor="middle" class="title">'
        f'ARC-100 overlap with each standard</text>'
    )
    lines.append(
        f'  <text x="{CANVAS_W // 2}" y="58" text-anchor="middle" class="subtitle">'
        f'Two bars per standard: blue = % of standard covered by ARC-100 &#160;|&#160; '
        f'red = % of ARC-100 covered by standard</text>'
    )

    # Legend
    lines.append(
        f'  <rect x="280" y="78" width="14" height="12" class="bar-std"/>'
    )
    lines.append(
        f'  <text x="300" y="89" class="legend">% of standard in ARC-100</text>'
    )
    lines.append(
        f'  <rect x="500" y="78" width="14" height="12" class="bar-arc"/>'
    )
    lines.append(
        f'  <text x="520" y="89" class="legend">% of ARC-100 in standard</text>'
    )

    # X axis grid
    for pct in (0, 25, 50, 75, 100):
        gx = chart_left + chart_width * pct / 100
        lines.append(
            f'  <line x1="{gx}" y1="{chart_top}" x2="{gx}" y2="{chart_top + n * row_h}" '
            f'class="gridline"/>'
        )
        lines.append(
            f'  <text x="{gx}" y="{chart_top + n * row_h + 18}" text-anchor="middle" '
            f'class="axis">{pct}%</text>'
        )

    # Rows
    bar_h = 14
    bar_gap = 2
    for i, s in enumerate(standards):
        y0 = chart_top + i * row_h + 8
        # Label
        lines.append(
            f'  <text x="{chart_left - 12}" y="{y0 + 12}" class="row-label">'
            f'{escape(s.name)}</text>'
        )
        lines.append(
            f'  <text x="{chart_left - 12}" y="{y0 + 28}" class="row-label" '
            f'style="font-weight: normal; fill: #666;">'
            f'({escape(s.topic_count_label)})</text>'
        )
        # std-in-arc bar (blue)
        w1 = chart_width * s.overlap_std_pct / 100
        lines.append(
            f'  <rect x="{chart_left}" y="{y0}" width="{w1:.1f}" height="{bar_h}" '
            f'class="bar-std"/>'
        )
        lines.append(
            f'  <text x="{chart_left + w1 - 4:.1f}" y="{y0 + 11}" text-anchor="end" '
            f'class="bar-lbl">{s.overlap_std_pct}%</text>'
        )
        # arc-in-std bar (red)
        w2 = chart_width * s.overlap_arc_pct / 100
        y1 = y0 + bar_h + bar_gap
        lines.append(
            f'  <rect x="{chart_left}" y="{y1}" width="{w2:.1f}" height="{bar_h}" '
            f'class="bar-arc"/>'
        )
        if w2 > 30:
            lines.append(
                f'  <text x="{chart_left + w2 - 4:.1f}" y="{y1 + 11}" text-anchor="end" '
                f'class="bar-lbl">{s.overlap_arc_pct}%</text>'
            )
        else:
            lines.append(
                f'  <text x="{chart_left + w2 + 4:.1f}" y="{y1 + 11}" text-anchor="start" '
                f'class="bar-lbl" style="fill: #991b1b;">{s.overlap_arc_pct}%</text>'
            )

    # Footer note
    foot_y = chart_top + n * row_h + 42
    lines.append(
        f'  <text x="{CANVAS_W // 2}" y="{foot_y}" text-anchor="middle" class="subtitle">'
        f'Asymmetry: ARC-100 covers most narrow standards well; '
        f'no single standard covers most of ARC-100.</text>'
    )

    lines.append("</svg>")
    return "\n".join(lines)


def bullet(s: str) -> str:
    if s.startswith("  "):
        return s  # sub-bullet, keep leading spaces
    return "• " + s


def escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main() -> None:
    for s in STANDARDS:
        out = OUTPUT_DIR / f"comparison_{s.key}.svg"
        out.write_text(render(s))
        print(f"wrote {out}")
    summary = OUTPUT_DIR / "comparison_00_summary.svg"
    summary.write_text(render_summary(STANDARDS))
    print(f"wrote {summary}")


if __name__ == "__main__":
    main()
