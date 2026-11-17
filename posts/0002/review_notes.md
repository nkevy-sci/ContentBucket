# Post 0002: implementation and review

## Current editorial status

At the author’s subsequent request, the webpage text and quiz feedback have been restored to the Word specification’s substantive wording, including statistical errors. Only light spelling, grammar, punctuation, and typographic edits remain (for example, Moura → Maura and effect → affect). The reversed Mann–Whitney feedback, rank-sum wording, and 62.5% forecast are deliberately retained. A later equation-aware inspection recovered seven Word equations (OMML), which the initial text extraction had missed. These are now included as native MathML. The author confirmed 3/12; the adjacent 3/10 typo is corrected. The feedback fraction was present in Word and is restored as 3/12. The source inequality 22.5 > 31 remains verbatim pending the author’s revision.

The prior statistical revisions described below are historical and no longer describe the current webpage. Proposed corrections are now maintained separately in `statistical_corrections.md`. The source Word document and image remain unchanged. The CDN, responsive styles, keyboard-operable controls, unique IDs, and ARIA relationships are retained. Auxiliary reveal-button and screen-reader instructions remain implementation text. The no-JavaScript message was updated to reflect that the reveal also requires JavaScript.

Checks for this text-restoration pass: ten answer-feedback choices, unique IDs, ARIA targets, local resource paths, preserved original numerical claims, and removal of the previously added permutation-test and strict-win explanations. Earlier browser/accessibility checks below apply to the earlier revision; they were not rerun for this text-only pass.

Built locally from `spec.docx`, using post 0001 as the style reference. The source document, original basketball photograph, and post 0001 remain unchanged. No publishing or deployment was performed.

## Design and resources

- Files: `index.html`, `script.js`, and `style.css`. jQuery 4.0.0 loads from the official CDN with Subresource Integrity and anonymous cross-origin loading. The downloaded copy was removed at the user’s request; interactive features require the CDN to be reachable.
- jQuery 4.0.0 was verified against the official download page: https://jquery.com/download/.
- Photo-derived accents: rust `#963d20` from the basketballs and deep red `#8b2028` from the stands, darkened for contrast. Pale warm surfaces use `#f3e5dc` and `#fcf0e7`.
- Background: `#f8f8f8`; default text: `#222`. System font, article proportions, tables, credits, and question patterns follow post 0001.
- Game cells use native buttons with single selection and hover/focus highlighting. The test-statistic reveal uses a native button, dashes, expanded state, and a polite status announcement. Question feedback does not move keyboard focus.

## Historical copyediting and approved statistical corrections (superseded)

The user explicitly approved correcting and documenting substantive statistical issues.

- Standardized Moura/Maura to Maura, corrected affect/effect and other spelling/grammar, and repaired incomplete pseudocode/HTML.
- Corrected `1/12 + 2/12 = 3/10` to `3/12 = 25%`, and restored the missing probability in the incorrect-answer explanation.
- Explained that twelve separate games follow from the stated setup, not from statistical independence alone. Stated the equal-selection-probability assumption.
- Kept independence as an assumption: separate teams alone do not establish it.
- Replaced the claim that a lower bound of zero rules out normal modeling. Explained that nonparametric methods also require assumptions.
- Distinguished equal distributions, a directional alternative, and the role of ties in a 50% null benchmark.
- Corrected the reversed Mann–Whitney quiz answer key and gave each feedback area a unique ID.
- Preserved all scores and U contributions: 4.5, 4, 4.5, 1.5, 4, 4; total U_M = 22.5, U_K = 13.5, 36 comparisons.
- Corrected “ranked sums” to U statistics. Explained smaller/larger-U table conventions and identified 31 as the linked table’s 6-by-6 critical value at one-sided 0.025 / two-sided 0.05. Flagged that untied tables are insufficient for these tied scores.
- Added a tie-aware exact label-permutation calculation rather than relying on the untied critical table. Enumerating all C(12,6) = 924 index allocations, 260 have U_M >= 22.5: one-sided p = 260/924 = 0.281385… . This calculation assumes exchangeability under the equal-distributions null; it is not proof of equal performance.
- Corrected the suggestion that CLES is an inferior substitute used only after a failed test. Effect size and significance answer different questions.
- Distinguished tie-adjusted CLES, 22.5/36 = 62.5%, from strict observed superiority, 20/36 ≈ 55.6%. There are five ties and eleven losses. Removed the claim that 62.5% is a reliable next-game forecast.
- Used the detailed photo description rather than the contradictory “basketball hoop” shorthand.

Technical sources checked: Shier’s guide (https://www.statstutor.ac.uk/resources/uploaded/mannwhitney.pdf) and the George Mason U table (https://mason.gmu.edu/~alaemmer/bio214/mwu-table2.pdf). Original reference entries were retained. The Vargha/Delaney DOI did not resolve through the research tool during this review; its original citation remains for reader access. Hooke/Stark remain linked in the introduction as in the source/sample convention.

## Verification

- Confirmed local resource paths, unique IDs, and ARIA reference targets.
- Browser tested all ten answer choices and both number-input feedback paths; Enter and Space activation tested.
- Verified one selected game at a time, test-statistic reveal/hide, expanded state, and value visibility. No browser console warnings or errors observed during interaction checks.
- Traversed the full page’s forward and reverse Tab order, including the skip link, game buttons, input, question choices, and references. Verified skip-link destination focus. No keyboard traps or positive tabindex values.
- Responsive checks at effective CSS widths of 320, approximately 769, and approximately 1282 pixels: document width matched viewport width. Wide tables scroll within labeled, keyboard-focusable regions. An additional narrower viewport check also showed no page overflow. Visible interactive controls meet the 24-by-24 CSS-pixel minimum; buttons and input use a 44-pixel minimum height.
- WCAG relative-luminance contrast calculations: rust/background 6.62:1; red/background 8.47:1; rust/button surface 6.28:1; white/rust 7.03:1; muted text/background 6.53:1. Focus outlines use deep red with spacing from the control.
- axe-core 4.10.3 audit of the final page structure: zero violations, 47 passing rules, with color contrast marked incomplete. Covered WCAG 2 A/AA, 2.1 A/AA, 2.2 AA, and best-practice tags. Temporary audit files were removed.
- Static review: semantic headings/tables, meaningful image alternative, native buttons, labeled number input, polite status messages, underlined links, reduced-motion treatment, no fixed overlays, and no animation.

Limits: Browser viewport reflow was checked, but a separate 200%/400% browser-zoom run and screen-reader announcement testing were not completed. Browser screenshots were affected by the app’s preview scaling, limiting full-width visual inspection. The automated scan and manual checks do not constitute a complete WCAG 2.2 conformance certification. External destinations were not exhaustively link-checked. The original 10 MB photo is used unchanged, so first-load image transfer is relatively large.
