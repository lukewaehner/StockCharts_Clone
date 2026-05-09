# Product

## Register

product

## Users

Recruiters, hiring managers, and engineers reviewing Luke's portfolio. They land here from a portfolio index, spend somewhere between thirty seconds and three minutes, and are mentally comparing this surface against twenty others they saw the same day. Secondary user: Luke himself, occasional stock checks.

The job-to-be-done is not "use this to make trading decisions". It is "form an opinion about Luke's frontend taste and execution within ninety seconds". Every design choice should be evaluated against that test, not against a real trading workflow.

## Product Purpose

Demonstrate that a familiar, often-cluttered problem (stock charts) can be executed with restraint and craft. The product is the proof: the same data that is usually presented as a wall of indicators, ticker tape, and red/green noise is presented here calmly. Success is the reviewer pausing on this page longer than they normally would on a portfolio entry, because something about it feels considered.

## Brand Personality

Modern, minimalistic, precise. Three words, ranked.

Voice and tone are quiet. No exclamation points, no "Welcome to" greetings, no animated dopamine. The interface speaks the way a well-set financial report reads: confident, unhurried, dense with information but not noisy. Numerals are tabular. Whitespace is the primary luxury.

The emotional target is the inverse of most consumer finance apps. Where Robinhood says "trade NOW", this should feel like sitting down with a coffee and a printed paper.

## Anti-references

- **Robinhood**: gamified, dopamine-driven, confetti animations, sale-pitch energy. The opposite of calm.
- **Bloomberg terminal**: hostile density, screen-screaming-data, ugly-on-purpose as a flex. Information at the cost of legibility.
- **Generic SaaS dashboards**: rounded cards in 12-column grids, hero-metric templates, blue gradients, icon-plus-title-plus-body card walls. The default frontend slop.
- **Default TradingView**: everything-everywhere, every indicator on by default, drawing tools in your face. Powerful but loud.

Any aggressive, busy, or "in your face" treatment is wrong, regardless of how technically impressive it looks.

## Design Principles

1. **Calm is the loudest signal.** When nine out of ten finance tools are shouting, restraint reads as confidence. Resist the reflex to add "one more thing" to a screen.
2. **The data is the subject. Chrome defers.** Every UI element competes with the chart for attention. If it cannot justify the cost, it is removed or quieted.
3. **Refuse the category reflex.** Finance design converges on navy and gold, or neon on black. This one does not. Lean editorial and typographic; let type and whitespace do what color does in cliché finance design.
4. **Polish lives in the small details.** Engineers click around. Tooltip easing, hover states, the way the price color flips on range change, the focus ring on a ticker input. These are where taste is judged.
5. **One voice per surface.** The chart is the primary surface; the hero stat block defers to it; the simple mode defers to the line itself. No competing emphases on the same screen.

## Accessibility & Inclusion

No formal WCAG target. Default to the basics that come for free with good design: legible type sizes, sufficient contrast in both themes, keyboard-reachable form controls, native focus indicators. Respect `prefers-reduced-motion` if and when motion is added.
