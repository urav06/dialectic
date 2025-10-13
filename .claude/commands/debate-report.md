---
description: Generate comprehensive debate report with analysis and visualization
argument-hint: [slug]
---

# Generate Debate Report

Analyzes the debate and generates a comprehensive report with argument graph visualization.

## Arguments

- `$1`: Debate slug (optional if only 1 debate exists)

## Step 1: Determine Debate

**If `$1` provided:**
- Use it

**If no `$1`:**
- List debates
- If 0: "No debates found."
- If 1: Auto-use that debate
- If 2+: "Which debate? {list}"

## Step 2: Convert Argument Graph to PNG

Try to convert `{debate}/argument-graph.mmd` to PNG image:

```bash
mmdc -i {debate}/argument-graph.mmd -o {debate}/argument-graph.png -t dark -b transparent -s 4
```

**If conversion succeeds:**
- Note: "✓ Graph visualization created"
- Set `image_exists = true`
- Continue to Step 3

**If conversion fails:**

Check if `mmdc` (mermaid-cli) is installed:
```bash
which mmdc || command -v mmdc
```

**If not installed, present options:**

"**Graph visualization requires mermaid-cli (not currently installed).**

Choose how to proceed:

**1. Install and retry** - Install [mermaid-cli](https://github.com/mermaid-js/mermaid-cli) then run this command again
   - npm: `npm install -g @mermaid-js/mermaid-cli`
   - Docker: `docker pull minlag/mermaid-cli` (requires creating a shell alias for `mmdc`)

**2. Convert manually** - Convert the graph yourself and continue
   - Copy contents of `{debate}/argument-graph.mmd`
   - Convert online at: https://mermaid.live
   - Download PNG and save as `{debate}/argument-graph.png`
   - Reply: **'Image provided, continue'**

**3. Skip visualization** - Generate report without the graph image
   - Reply: **'Skip image, continue'**"

Wait for user input:
- If "1": Exit with message "Install mermaid-cli and re-run `/debate-report {slug}`"
- If "2": Set `image_exists = true`, continue to Step 3
- If "3": Set `image_exists = false`, continue to Step 3

## Step 3: Generate Comprehensive Report

Use Task tool with subagent_type "general-purpose" to generate analysis:

**Prompt:**

```
Generate a comprehensive debate report for the debate at {debate}/.

Read and analyze:
- Motion from @{debate}/debate.md
- All arguments in @{debate}/arguments/
- Scores from @{debate}/scores.json
- Debate state and cumulative scores from @{debate}/debate.md frontmatter

Your task is to write a compelling, high-level analysis in **500-600 words** that captures the intellectual battle and hooks readers. This is a summary for someone who hasn't read the full debate yet—make it engaging and insightful, not exhaustive.

**Required structure:**

# [Motion Title]

## The Question
1-2 sentences capturing what's at stake and why it matters

## The Clash
100-150 words on the fundamental disagreement. What core assumptions or frameworks divide the sides?

## Turning Points
150-200 words on 2-3 key moments that shifted the debate's trajectory. Focus on the most dramatic or intellectually significant developments.

## The Verdict
100-150 words: Final scores (zero-sum totals), strongest/weakest arguments with IDs, and your assessment of who won and why

{if image_exists:}
## Argument Graph

![Argument Graph](./argument-graph.png)
{/if}

**Style guidelines:**
- Use rich markdown: headings (##, ###), **bold**, *italic*
- Match tone to debate topic (serious debates = analytical tone, lighter topics = can be more engaging)
- Strictly avoid em-dashes and en-dashes
- Focus on clarity and intellectual substance over exhaustive detail
- 500-600 words total (strictly enforced)

Output ONLY the complete markdown content for the README.md file.
```

Save agent output to `{debate}/README.md`.

## Step 4: Completion Message

**If image exists:**
```
✓ Debate report generated successfully!

**Generated files:**
- {debate}/README.md (comprehensive analysis)
- {debate}/argument-graph.png (visual graph)

View the report: `cat {debate}/README.md`
```

**If image skipped:**
```
✓ Debate report generated successfully!

**Generated file:**
- {debate}/README.md (comprehensive analysis)

Note: Graph visualization was skipped. You can generate it later by:
1. Installing [mermaid-cli](https://github.com/mermaid-js/mermaid-cli): `npm install -g @mermaid-js/mermaid-cli`
2. Running: `mmdc -i {debate}/argument-graph.mmd -o {debate}/argument-graph.png -t dark -b transparent`

View the report: `cat {debate}/README.md`
```
