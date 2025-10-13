---
description: Create a new debate with interactive setup
argument-hint: [slug] (optional)
---

# Create New Debate

## Step 1: Motion

"**What's your debate motion?**

You can write it in any of these formats:

**Formal styles:**
- `This house believes that` [proposition] — British Parliamentary
- `This house would` [action] — Policy debate
- `Resolved:` [statement] — American Parliamentary

**Or state it directly** (we'll keep it as-is)

Your motion:"

## Step 2: Slug

**If `$1` argument provided:**
1. Use `$1` as the slug
2. Validate format (lowercase, numbers, hyphens only)
3. Check it doesn't exist as a directory
4. If valid: skip to Step 3
5. If invalid format: explain requirements and ask for new slug
6. If exists: list existing debates and ask for different name

**If no argument provided:**
1. After receiving motion, auto-generate 2-3 slug suggestions from motion keywords
2. Present: "Suggested slugs:
   1. [auto-generated-1]
   2. [auto-generated-2]
   3. [auto-generated-3]

   Pick a number, or type your own (lowercase, hyphens only):"
3. Validate chosen/custom slug:
   - Check format (lowercase, numbers, hyphens only)
   - Check doesn't exist as a directory
   - If format invalid: explain and ask again
   - If exists: list existing debates and ask for different name

## Step 3: Definitions & Scope (Optional)

"**Optional refinements:**

Type 'definitions' to define key terms, 'scope' to set debate focus, or 'skip' to continue:"

**If user types 'definitions':**
- Suggest 2-3 key terms from the motion that might need defining
- For each term: "Define '[term]':" (record definition)

**If user types 'scope':**
- Ask: "Specify the debate's scope or focus:"
- Record scope

**If user types 'skip':**
- Proceed to creation

## Step 4: Create Debate

Once all information is gathered:

1. Create directory: `{slug}/`
2. Create `{slug}/arguments/` directory
3. Create `{slug}/debate.md` with JSON frontmatter:

```markdown
{
  "debate_id": "{slug}",
  "current_exchange": 0,
  "current_phase": "awaiting_arguments",
  "cumulative_scores": {
    "proposition": {"total": 0, "count": 0},
    "opposition": {"total": 0, "count": 0}
  }
}

# Motion

{formalized motion}

## Definitions

{if any definitions were provided:}
- **{term}**: {definition}

## Scope

{scope if provided}
```

4. Create `{slug}/scores.json`:

```json
{}
```

5. Confirm to user:

"✓ Debate '{slug}' created successfully!

**Motion**: {full formalized motion}
{if definitions: **Definitions**: {count} terms defined}
{if scope: **Scope**: {scope}}

Run `/debate-run {slug} 8` to start the debate. Exchange 0 (opening statements) runs automatically, then specify how many rebuttal exchanges to run."
