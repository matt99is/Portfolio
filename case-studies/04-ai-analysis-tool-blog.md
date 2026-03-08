# How I Built a Competitive Analysis Tool with AI

What started as a quick fix for a single project has become a production tool I continue to develop and use.

---

Competitive UX analysis is essential for almost any design project, but the manual process doesn't scale. You capture screenshots, work through evaluation criteria, document findings, and try to spot patterns across competitors. It's valuable work, but the time cost means you end up analysing three or four sites and hoping they're representative.

For the basket redesign project I needed to audit 16 competitor sites against Baymard Institute guidelines. Doing that manually would have taken the better part of a week, and the output would have been notes in a document rather than something structured enough to surface patterns automatically. I wanted a tool that could do it faster and at a scale that manual work couldn't match.

## What the tool does

The tool captures screenshots of competitor pages, analyses them against research-backed criteria using Claude's vision API in a two-pass process (observe first, then score), and generates interactive HTML reports with heatmaps, radar charts, and ranked competitor cards showing where the market is strong, where it's weak, and where opportunities exist. Criteria are configured in YAML files per page type, so different page types (homepage, product page, basket, checkout) get different evaluation criteria drawn from Baymard and Nielsen Norman Group research.

I built the initial version with Claude Code over a few days, and it's continued to evolve since. My role throughout has been product owner and director: I define problems, describe outcomes, and make decisions about direction and trade-offs. It's now at version 1.13, with automated deployment to Netlify and reports that are publicly accessible. The codebase lives on GitHub.

[LINK: GitHub repository → github.com/matt99is/UXMaturityAnalysis]
[LINK: Live reports → analysis.mattlelonek.co.uk]

## The honest pivot

The original plan was fully automated. The tool would visit each URL, capture screenshots, and analyse them without human intervention. But competitor sites kept blocking Playwright even with stealth mode enabled. Bot detection on major e-commerce sites is good enough now that automated browsers get caught reliably, with multiple layers of detection from IP reputation checks through to browser fingerprint analysis.

When that became clear, we pivoted to a supervised mode where the browser opens, I take control to navigate and prepare the page (closing cookie banners, adding products to baskets where needed), then hand back to the tool for screenshot capture and analysis. Since then I've also built an automated capture mode for sites with lighter protection, which handles the full pipeline unattended with retry logic, pacing controls, and preflight checks that validate the environment before a run starts.

The two modes reflect a practical reality: some sites need human intervention and some don't, and the tool now handles both rather than pretending one approach works everywhere.

## What it found

The tool's first real use was the competitor analysis for the basket redesign. 16 pet retail sites analysed against 11 basket-specific criteria in about 10 minutes.

It surfaced two market-wide weaknesses I might have missed doing this manually with a smaller sample. Subscription options were absent or poorly implemented across the majority of competitors, which is a significant gap in a category like pet food where repeat purchase is the norm. Express checkout options were weak across the market, with most competitors funnelling everyone through the same flow regardless of whether they were returning customers.

Both of these became priorities in the basket redesign, backed by evidence across 16 competitors rather than assumptions based on three or four. More data means more confidence in the patterns you're seeing.

[IMAGE: The competitor analysis heatmap/report output]
[LINK: View the full interactive competitor analysis report → analysis.mattlelonek.co.uk]

## What this means for how I work

The barrier to building tools like this has dropped significantly. Problems that would previously have required developer time or weeks of manual effort now have a third option. I'm not a developer and I don't pretend to be, but I can define problems clearly, describe the outcomes I need, and make good decisions about direction and trade-offs. That combination turns out to be enough to build things that are genuinely useful.

The fact that this tool started as a quick solution for one project and has grown into something I'm actively maintaining and improving says something about the approach. The initial build took days. The ongoing development, adding automated capture, improving scoring reliability, building proper reports with deployment infrastructure, has happened iteratively as I've used the tool on real work and understood what it needs next. That's a design process applied to tooling rather than interfaces, and it's become part of how I work now.
