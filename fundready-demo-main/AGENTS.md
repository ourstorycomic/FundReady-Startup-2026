# AGENTS.md

## Project overview

Static Vietnamese marketing/demo site for "FundReady AI" — two self-contained HTML files, no build system, no backend, no tests. Deployed on Vercel.

## Critical constraints

- **No build/test/lint commands exist.** Preview by opening files in a browser or running `python3 -m http.server` from repo root.
- **Two files only:** `index.html` (landing page) and `danh-gia.html` (assessment tool). Both are fully self-contained with inline CSS/JS.
- **All content is Vietnamese** (`lang="vi"`).
- **Vercel `cleanUrls: true`** means `/danh-gia` serves `danh-gia.html`. This rewrite only works on Vercel, not local static servers.

## Architecture gotchas

- `danh-gia.html` contains **two merged scoring engines** (qualitative document assessment + quantitative financial calculator) that share one result surface. Don't re-split them or add a second reset button/CTA.
- **Hand-maintained DOM IDs** — typos fail silently at runtime. Click through both halves of `danh-gia.html` after editing IDs.
- **Shared design tokens** — both files duplicate the same CSS custom properties. When changing colors/spacing/components, update both files.
- **No external dependencies** except Google Fonts and GSAP from CDN. No `package.json`, no bundler.

## Detailed guidance

Read `CLAUDE.md` for comprehensive architecture documentation, scoring model details, and editing conventions.
