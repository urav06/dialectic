---
description: Run debate exchanges between proposition and opposition
argument-hint: [slug] [num-exchanges]
---

# Run Debate

List available debates by checking for directories with debate.md files.

## Arguments

- `$1`: Debate slug (optional if only 1 debate exists)
- `$2`: Number of exchanges (optional, will ask if not provided)

## Behavior

### Determine Debate Slug

**If `$1` provided:**
- Validate it exists
- Use it

**If no `$1`:**
- List debates from context above
- If 0: "No debates found. Create one with `/debate-new`"
- If 1: Auto-use that debate
- If 2+: "Which debate? {list}"

### Determine Exchange Count

**If `$2` provided:**
- Use it

**If no `$2`:**
- Ask: "How many exchanges?"

## Execution

Once both parameters are validated:

Invoke the debate-orchestrator skill with:
- Debate slug: {slug}
- Number of exchanges: {N}

The skill manages:
- State machine progression (awaiting_arguments → awaiting_judgment cycles)
- Parallel debater coordination and judge evaluation
- Argument file creation and scoring
- State persistence across interruptions

## Completion

The skill reports final scores when all exchanges complete.

Run `/debate-report {slug}` to generate comprehensive debate report and visualization.
