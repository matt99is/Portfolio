# Quantifying a Problem Nobody Was Looking At

How I identified a high-impact revenue problem through behaviour data, built the business case from scratch, and designed the solution now moving into engineering delivery.

---

**What:** Full basket page redesign for a major e-commerce retailer, from discovery through to hi-fi prototype
**My role:** Self-initiated. Owned research, business case, UX design. Collaborated with engineering from discovery
**Timeline:** 3 months discovery and design, currently in engineering delivery
**Outcome:** Business case approved, project prioritised on roadmap, conservative projections show significant annual revenue recovery

---

[IMAGE: Hero — the hi-fi prototype, real screenshot showing the basket page design]

## The most familiar customers were struggling the most

Behaviour data showed that nearly half of customers who viewed their basket left without clicking checkout, and only a small fraction returned organically to complete their purchase. Those numbers alone made it worth investigating, but the insight that turned this from a general conversion concern into a clear UX problem was in the user segments.

Returning users, people who know the site and trust the brand, were abandoning at a higher rate than first-time visitors. When your most experienced customers struggle more than newcomers, the problem isn't trust or product awareness. It's the experience itself.

Nobody had flagged this. The basket page wasn't on any team's roadmap. I built the case for a full discovery project from scratch.

## Building from multiple evidence streams

I started with a Baymard Institute audit against their usability guidelines for basket pages, which surfaced multiple high-impact violations and only a couple of areas meeting best practice. That established the baseline: we weren't just underperforming, we were failing against established e-commerce standards.

[IMAGE: Baymard audit visualisation — the audit results showing violations vs best practice]

Competitor analysis came next. I analysed 16 pet retail sites against 11 UX criteria using the automated benchmarking tool I built with Claude Code, which would have been a week of manual work compressed into a single session. The tool surfaced market-wide weaknesses in subscription UX and express checkout options, which became differentiation opportunities rather than just catch-up fixes.

[IMAGE: Competitor analysis heatmap or summary from the automated tool]
[LINK: Full interactive competitor analysis report at resources.mattlelonek.co.uk]

Feature importance rankings with real users showed that the two things customers valued most, the checkout CTA and basket totals, weren't prominent above the fold on our current page. Card sorting revealed that no two participants organised basket features the same way, which pointed to fundamental information architecture problems rather than surface-level layout issues.

## Every change traced to evidence

The redesign isn't decorative. Every change in the prototype maps directly to a Baymard guideline, a competitor analysis finding, or a user research insight, and I can trace the lineage for each one. I started with wireframes focused on information architecture before moving to interactions, and engineering was involved from discovery onwards because leaving feasibility conversations until handover creates problems that are entirely avoidable.

[IMAGE: Early IA wireframes with annotations showing the rationale]

The hi-fi prototype is a fully functional, accessible React build with real interactions and configurable variants for A/B testing. It covers the full checkout flow including save for later, subscription setup, delivery method selection, and undo functionality.

I should be clear: this is a prototype, not a shipped product. The phased implementation approach was deliberate because shipping everything at once would be risky. The plan was always to implement piece by piece, measuring the impact of each change before moving to the next.

[LINK: Live Figma prototype if available]

## Testing and external validation

The lo-fi prototype was tested on usertesting.com and internally. Users described the experience as intuitive, and the ability to edit product details from within the basket rather than navigating back to the product page was consistently highlighted as a significant improvement. One piece of feedback that drove iteration: the "Save" label for moving items out of the active basket was unclear to multiple participants, which led to a language change that made the action more explicit.

I also shared the hi-fi prototype with a senior researcher at the Baymard Institute, whose usability guidelines had formed the foundation of the audit. Their assessment was that the redesign would take the basket most of the way toward a "perfect" rating on the Baymard scale, which is a significant shift from the current baseline that sits firmly in "poor" territory. That kind of third-party validation from the people who wrote the standards gave the business case considerably more weight.

## Approved and moving into delivery

The research was strong enough to get the project prioritised on the roadmap. Conservative projections showed meaningful annual revenue recovery, and the phased approach means each change can be measured for impact before committing to the next. The project was delayed by a period of organisational change but is now moving into engineering delivery.

## What this project taught me

The most valuable thing about this project was the process of self-initiating it. Nobody asked me to look at the basket. I found the problem in the data, built the evidence, and made the case. That's the difference between a designer who waits for a brief and one who creates the brief.

The returning-user insight was the moment that changed the conversation from "the basket could be better" to "the basket is actively costing us money," and it came from asking a question nobody else had asked: are experienced users actually finding this easier? The answer was no, and that reframing is what got the project funded.

I also learned that getting engineering involved early doesn't just reduce handover friction, it changes the quality of the design decisions. Having an engineer in the room during discovery meant I could test the feasibility of ideas in real time rather than designing something that would need to be compromised later.
