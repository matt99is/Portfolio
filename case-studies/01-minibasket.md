# Increasing AOV by 4.4% Through a High-Intent Touchpoint

A focused intervention at the moment of commitment. From proposal to production in one month.

---

**What:** Redesigned the added-to-basket interaction to include product recommendations and a free delivery progress bar
**My role:** UX design, prototyping, user research. Collaborated with a UI designer on visual design
**Timeline:** One month, proposal to production
**Outcome:** 4.4% AOV increase, live across web and app

---

[IMAGE: Hero — the shipped minibasket on web and/or app, real screenshot not a mockup]

## A dead end at the highest-intent moment

The site had no minibasket. When a customer added a product, they got a basic confirmation modal with two options: view the basket or close it. No visibility of what was already in the basket, no reason to continue shopping, and nothing to suggest they might want to add more. It was a dead end at the exact moment a customer had just committed to buying something.

When a company-wide initiative launched to protect profitability by increasing average order value, I spotted an opportunity sitting on the Buy it Again roadmap and proposed pulling it forward. The concept was two interventions working together: a free delivery progress bar that gives customers a reason to add more, and product recommendations that give them the means to do it, both surfaced at the point of highest purchase intent.

## Testing four interaction variants

The delivery bar was straightforward and tested well immediately. The recommendations raised harder questions. When a user adds a recommended product from within the modal, what should happen? Should it move into the basket area? Should they be able to adjust quantity? These details matter because getting them wrong creates confusion instead of conversions.

I built four fully functional prototypes using AI-assisted development, each testing a different combination of two variables: whether the product moves to the basket area when added, and whether users can adjust the quantity. These weren't wireframes or click-throughs. They were working prototypes with ARIA labels, keyboard navigation, and screen reader support, because I wanted to test with assistive technology users as well as regular customers.

[IMAGE: Variant comparison — side-by-side of the four prototypes or a clear diagram showing the two variables]

I ran the research through usertesting.com with two separate groups. Regular customers tested all four interaction variants plus two layout options (central modal versus side panel). Assistive technology users validated that the interactions were navigable and clear. Running accessibility testing at this stage was a first for the design team, and I wanted to make sure the design actually worked for everyone rather than assuming it did based on guidelines alone.

## Why Variant C won and the others failed

Both user groups pointed to the same winner, and the principle behind it was simple. Users need two things when they add a product: visual feedback confirming it happened, and quantity control so they can adjust it. Variant C was the only one that delivered both.

When a user adds a recommendation in Variant C, the product moves up into the basket area, which confirms the action visually. The "Add to basket" button becomes a quantity selector, giving immediate control. The total updates straight away.

The other variants each broke one of these rules, and users noticed every time.

| Variant | Visual Feedback | Quantity Control | Result |
|---------|----------------|-----------------|--------|
| C | ✓ | ✓ | Winner |
| B | ✗ | ✓ | Confusing — users weren't sure the add had worked |
| E | ✓ | ✗ | Frustrating — users expected to adjust quantities |
| D | ✗ | ✗ | Failed on both counts |

Users described Variant C as "straightforward" and "simple." One participant compared it to ASOS, which was a good signal that the interaction matched established mental models from other e-commerce sites they already used.

[IMAGE: The variant comparison table as a visual element, or the embedded Figma prototype if still live]

## Shipped in a month

The minibasket shipped to web first, then app. Total time from proposal to live: one month. AOV increased by 4.4% across platforms. The free delivery progress bar and recommendations work together: one gives customers the motivation to add more, the other gives them the means.

[LINK: Embedded Figma prototype if available]

## What I took away from this

Including assistive technology users in the research was a first for the team, and it validated that the design worked for everyone rather than relying on an assumption based on WCAG compliance alone. The fact that both user groups converged on the same winner added confidence that the design principles were sound, not just the implementation.

AI-assisted prototyping made it possible to build four accessible, functional prototypes fast enough to test properly and still ship within a month. That workflow is now part of how I approach problems, and it changed what's realistic to achieve within a sprint cycle.

This wasn't a full redesign. It was a focused change at a high-value moment in the customer journey, and the fact that it moved a meaningful commercial metric shows that targeted interventions grounded in research can outperform larger, slower projects when the opportunity is right.
