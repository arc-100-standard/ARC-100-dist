// ARC-100 master index — filter, expand/collapse, click-to-toggle,
// right-column hover description overlay, Book 00 visibility toggle.
// Source: _hooks/arc100_master_index.py (generates 00/index.md and
// 01/index.md depending on render mode).
// The tree HTML is plain divs scoped under `.arc100-tree`. This script:
//   1. Toggles `data-open` on `.book` when the user clicks/presses its
//      summary row (CSS hides `.chapters` when data-open is false).
//   2. Drives the filter dropdown (Active / Active+Draft / All) by
//      hiding chapters whose status doesn't match, and cascades the
//      hide up to books and bands that end up empty.
//   3. Implements expand-all / collapse-all on the filtered set.
//   4. Builds a fixed-position description overlay anchored over
//      Material's right-hand TOC sidebar that follows the mouse Y while
//      the pointer is over a row carrying `data-description`. The top
//      edge is clamped so the box stays fully in the viewport.
//   5. (Project copy only — phase 3.1c) Drives the Book 00 visibility
//      toggle: a "Show/Hide ARC-100 standard chapters" button. Default
//      state: HIDDEN (per V1_STRATEGY §6.3 Q5). Persisted in localStorage
//      at key `arc100-book00-visible`. The hook emits Book 00 .book divs
//      with inline `style="display:none"` + `data-book00-default-hidden`
//      in index render mode to eliminate the first-paint FOUC.

(function () {
  "use strict";

  const BOOK00_LS_KEY = "arc100-book00-visible";

  // Material's `navigation.instant` feature swaps page content via XHR
  // and never re-fires DOMContentLoaded, so listeners attached on first
  // load do not re-bind when the user clicks a left-nav link. Material
  // exposes a `document$` RxJS observable that DOES fire on every page
  // nav (including the initial load). We subscribe to it when present
  // and fall back to DOMContentLoaded otherwise.
  //
  // init() is idempotent: the singleton overlay is reused if it already
  // exists in the document, and the window-level scroll listener is
  // re-bound (after removing any prior binding) on each call. All other
  // listeners live on elements inside `.arc100-tree`, which Material
  // replaces wholesale on each navigation, so they neither leak nor
  // accumulate.
  let prevScrollListener = null;

  function getBook00Visible() {
    // Default: hidden. The toggle is for power-users / contributors
    // curious about the standard's inventory; typical readers focus on
    // the project content.
    const stored = localStorage.getItem(BOOK00_LS_KEY);
    if (stored === "true") return true;
    if (stored === "false") return false;
    return false;
  }

  function setBook00Visible(value) {
    localStorage.setItem(BOOK00_LS_KEY, value ? "true" : "false");
  }

  function init() {
    const tree = document.querySelector(".arc100-tree");
    if (!tree) return;

    const filter = document.getElementById("arc100-filter");
    const expandBtn = document.getElementById("arc100-expand-all");
    const collapseBtn = document.getElementById("arc100-collapse-all");
    const book00Btn = document.getElementById("arc100-book00-toggle");

    const books = Array.from(tree.querySelectorAll(".book"));
    const chapters = Array.from(tree.querySelectorAll(".chapter"));
    const bands = Array.from(tree.querySelectorAll(".band"));

    // ---------- Book 00 visibility (project / index render mode) ----------
    //
    // book00Hidden is the single source of truth for "should the Book
    // 00 books be hidden?" applyFilter consults it on every run; the
    // toggle button mutates it and triggers a re-apply.
    //
    // The toggle button is only emitted on the green / project site
    // (by the hook's _render_page_project). On the red / master-vault
    // site, the toggle has no meaning — Book 00 IS the inventory the
    // page exists to render. Default book00Hidden to false on the red
    // side so applyFilter does not silently hide Book 00 there.

    let book00Hidden = book00Btn ? !getBook00Visible() : false;

    // ---------- Click / keyboard toggle on book summaries ----------

    function toggleBook(book) {
      const open = book.getAttribute("data-open") === "true";
      book.setAttribute("data-open", open ? "false" : "true");
    }

    tree.querySelectorAll(".book-title").forEach((summary) => {
      summary.addEventListener("click", () => {
        toggleBook(summary.parentElement);
      });
      summary.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          toggleBook(summary.parentElement);
        }
      });
    });

    // ---------- Filter dropdown ----------

    function applyFilter() {
      if (!filter) return;
      const mode = filter.value;
      chapters.forEach((ch) => {
        const status = ch.dataset.status;
        const isActive = status === "active" || status === "checked-out";
        const isDraft = status === "draft";
        let show;
        if (mode === "all") show = true;
        else if (mode === "active-draft") show = isActive || isDraft;
        else show = isActive;
        ch.style.display = show ? "" : "none";
      });

      books.forEach((book) => {
        // The Book 00 toggle composes AND with the filter: if the
        // toggle says "hide Book 00", the Book 00 .book stays hidden
        // regardless of how many chapters its filter match would
        // otherwise reveal. Discriminator is the book id literal "00"
        // (data-book-id="00" emitted by the hook) — in the project
        // YAML, Books 01/02/10 also carry arc_100: true (the project
        // IS an ARC-100 instance), so the arc-100-badge presence
        // alone over-selects.
        if (book00Hidden && book.dataset.bookId === "00") {
          book.style.display = "none";
          return;
        }
        const visible = book.querySelectorAll(
          ".chapter:not([style*='display: none'])"
        ).length;
        book.style.display = visible > 0 ? "" : "none";
      });

      bands.forEach((band) => {
        const visibleBooks = band.querySelectorAll(
          ".book:not([style*='display: none'])"
        ).length;
        band.style.display = visibleBooks > 0 ? "" : "none";
      });
    }

    if (filter) filter.addEventListener("change", applyFilter);

    // ---------- Expand-all / collapse-all ----------

    if (expandBtn) {
      expandBtn.addEventListener("click", () => {
        books.forEach((book) => {
          if (book.style.display !== "none") {
            book.setAttribute("data-open", "true");
          }
        });
      });
    }

    if (collapseBtn) {
      collapseBtn.addEventListener("click", () => {
        books.forEach((book) => {
          book.setAttribute("data-open", "false");
        });
      });
    }

    // ---------- Book 00 visibility toggle ----------
    //
    // Mutates the single book00Hidden flag, then calls applyFilter
    // (which owns visibility). On every call, also clears any
    // server-rendered inline `display:none` that the hook emitted on
    // Book 00 books to eliminate the first-paint FOUC — once JS has
    // taken over, the filter is the only authority for visibility.

    function applyBook00Visibility() {
      book00Hidden = !getBook00Visible();
      tree
        .querySelectorAll('[data-book00-default-hidden="true"]')
        .forEach((book) => {
          book.style.display = "";
          book.removeAttribute("data-book00-default-hidden");
        });
      applyFilter();
      if (book00Btn) {
        const visible = !book00Hidden;
        book00Btn.textContent = visible
          ? "Hide ARC-100 standard chapters"
          : "Show ARC-100 standard chapters";
        book00Btn.dataset.book00State = visible ? "visible" : "hidden";
      }
    }

    if (book00Btn) {
      book00Btn.addEventListener("click", () => {
        setBook00Visible(!getBook00Visible());
        applyBook00Visibility();
      });
      applyBook00Visibility();
    }

    // ---------- Right-column hover description overlay ----------
    //
    // One fixed-position panel is shared across all rows. We mutate
    // its text/position on pointermove and toggle the `.visible` class
    // to show/hide. It lives outside `.arc100-tree` so the tree's
    // `overflow: hidden` cannot clip it.
    //
    // Positioning:
    //   - Horizontal: anchored over Material's right-hand TOC sidebar
    //     (`.md-sidebar--secondary`). If that sidebar isn't laid out
    //     (mobile breakpoint, no TOC), fall back to a right-anchored
    //     panel against the viewport edge.
    //   - Vertical: top edge tracks the mouse Y so the overlay reads
    //     next to the row the cursor is over. If the panel would
    //     overflow the bottom of the viewport, raise it until it fits;
    //     never let it go above a small top inset.

    // Reuse a prior overlay if present (Material navigation.instant
    // re-runs init() but does NOT swap document.body, so the overlay
    // div persists across navigations). Falling through to "create
    // new" only on the first init.
    let overlay = document.querySelector(".arc100-desc-overlay");
    let overlayLabel;
    let overlayBody;
    if (overlay) {
      overlayLabel = overlay.querySelector(".arc100-desc-label");
      overlayBody = overlay.querySelector(".arc100-desc-body");
      // Reset visibility state on re-init.
      overlay.classList.remove("visible");
      overlay.setAttribute("aria-hidden", "true");
    } else {
      overlay = document.createElement("div");
      overlay.className = "arc100-desc-overlay";
      overlay.setAttribute("role", "tooltip");
      overlay.setAttribute("aria-hidden", "true");
      // Two children: the red "Band/Book/Chapter NN" label (heading) and
      // the body description. Reusing the same DOM rather than rebuilding
      // it on every hover avoids reflow churn during pointermove.
      overlayLabel = document.createElement("span");
      overlayLabel.className = "arc100-desc-label";
      overlayBody = document.createElement("span");
      overlayBody.className = "arc100-desc-body";
      overlay.appendChild(overlayLabel);
      overlay.appendChild(overlayBody);
      document.body.appendChild(overlay);
    }

    const VIEWPORT_INSET = 12;
    const FALLBACK_WIDTH = 360;
    const MIN_WIDTH = 220;

    function positionOverlay(mouseY) {
      const sb = document.querySelector(".md-sidebar--secondary");
      let leftPx;
      let widthPx;
      if (sb) {
        const r = sb.getBoundingClientRect();
        if (r.width > 0) {
          leftPx = r.left + VIEWPORT_INSET;
          widthPx = Math.max(MIN_WIDTH, r.width - VIEWPORT_INSET * 2);
        }
      }
      if (leftPx === undefined) {
        // Mobile / TOC-less fallback: pin against the right edge.
        widthPx = Math.min(FALLBACK_WIDTH, window.innerWidth * 0.6);
        leftPx = window.innerWidth - widthPx - 24;
      }
      overlay.style.left = leftPx + "px";
      overlay.style.width = widthPx + "px";

      // Measurement requires the overlay to be laid out. The
      // `.visible` class supplies `display: block`; this runs after
      // the class is added in showOverlay.
      const h = overlay.offsetHeight;
      const maxTop = window.innerHeight - h - VIEWPORT_INSET;
      let topPx = mouseY;
      if (topPx > maxTop) topPx = maxTop;
      if (topPx < VIEWPORT_INSET) topPx = VIEWPORT_INSET;
      overlay.style.top = topPx + "px";
    }

    function showOverlay(row, mouseY) {
      const text = row.dataset.description;
      if (!text) {
        hideOverlay();
        return;
      }
      // Hook supplies the heading per row type via `data-desc-label`.
      // Empty string is fine — the `:empty` CSS rule collapses the
      // label slot so the body sits flush against the top padding.
      overlayLabel.textContent = row.dataset.descLabel || "";
      overlayBody.textContent = text;
      overlay.classList.add("visible");
      overlay.setAttribute("aria-hidden", "false");
      positionOverlay(mouseY);
    }

    function hideOverlay() {
      overlay.classList.remove("visible");
      overlay.setAttribute("aria-hidden", "true");
    }

    tree.addEventListener("pointermove", (e) => {
      // Touch and pen drive their own UX (tap-to-navigate, long-press
      // tooltips); the overlay is a mouse-only affordance.
      if (e.pointerType && e.pointerType !== "mouse") return;
      const row = e.target.closest("[data-description]");
      if (!row || !tree.contains(row)) {
        hideOverlay();
        return;
      }
      showOverlay(row, e.clientY);
    });

    tree.addEventListener("pointerleave", hideOverlay);
    // Scrolling shifts mouseY relative to content rows; rather than
    // chasing the cursor through reflow, hide on scroll and let the
    // next pointermove re-show against the new layout.
    //
    // Each init() binds a fresh hideOverlay (closure over the current
    // overlay element); detach the prior binding so the window does
    // not accumulate one listener per navigation.
    if (prevScrollListener) {
      window.removeEventListener("scroll", prevScrollListener);
    }
    prevScrollListener = hideOverlay;
    window.addEventListener("scroll", hideOverlay, { passive: true });

    applyFilter();
  }

  if (
    typeof document$ !== "undefined" &&
    typeof document$.subscribe === "function"
  ) {
    // Material's RxJS BehaviorSubject: subscribers receive the current
    // value immediately AND every subsequent emission (including each
    // navigation.instant page swap). One subscribe covers both initial
    // load and all later navigations.
    document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
