<p align="center">
  <img src=".github/banner.png" alt="Dialectic Banner"/>
  <i>A computational argumentation system for exploring debate structure</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-5A67D8" alt="Claude Code Plugin"/>
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License"/>
  <img src="https://img.shields.io/badge/python-3.9+-blue" alt="Python 3.9+"/>
</p>

---

Human debates are often decided by preparation, rhetoric, and charisma rather than argument quality. Judges can be swayed by fallacies and performance. The better debater wins, not necessarily the better position.

Dialectic removes this imbalance. The same AI agent argues both sides with identical capabilities. No rhetorical tricks, no charisma bias, no skill gap. What remains is the raw structure of argumentation itself.

The goal here isn't to determine which side "wins." It's to explore the natural geometry of argument space. Which claims are inherently defensible? What attacks work against what defenses? Where do positions become unassailable, and where do they crumble? By grounding debates in formal structure, these patterns become visible and quantifiable.

---

<details>
<summary><b>Debate Theory</b></summary>

### Toulmin Framework

Every argument follows a structured schema:

| Component | Purpose |
|-----------|---------|
| **Claim** | Central assertion |
| **Grounds** | Evidence supporting the claim (1-3 pieces) |
| **Warrant** | Logical connection between grounds and claim |
| **Backing** | Support for the warrant (optional) |
| **Qualifier** | Scope limitations (optional) |

### Attack Types

Arguments can target specific components of opponent arguments:

- **claim_attack**: Challenge the assertion directly
- **grounds_attack**: Undermine the evidence
- **warrant_attack**: Break the logical connection
- **backing_attack**: Weaken warrant support

### Defense Types

Arguments can defend previously made arguments:

- **reinforce**: Strengthen with additional support
- **clarify**: Address misinterpretation
- **concede_and_pivot**: Acknowledge weakness, redirect

### Zero-Sum Scoring

Arguments compete for a fixed score pool. The judge distributes scores that sum to exactly **0** across all arguments in each exchange.

- **0** = Neutral (neither winning nor losing)
- **Positive** = Winning (took score from weaker arguments)
- **Negative** = Losing (gave score to stronger arguments)

This forces comparative evaluation. Arguments don't exist in isolation, they win or lose relative to each other.

</details>

---

## Prerequisites

Dialectic requires [Claude Code](https://claude.ai/code), Anthropic's agentic coding tool.

---

## Installation

### Clone and Go (Recommended)

```bash
git clone https://github.com/urav06/dialectic.git
cd dialectic
claude
```

Debates work immediately. No additional setup required.

### Plugin Marketplace

```
/plugin → Add Marketplace → urav06/dialectic
/plugin → Browse and install plugins → dialectic@dialectic-marketplace
```

With the plugin installed, you can create debates in any project.

### Optional: Graph Visualization

For automatic argument graph generation, install [mermaid-cli](https://github.com/mermaid-js/mermaid-cli):

```bash
npm install -g @mermaid-js/mermaid-cli
```

Or via Docker:

```bash
docker pull minlag/mermaid-cli
```

> [!NOTE]
> Docker requires setting up a shell alias for `mmdc` to work with Dialectic.
> `alias mmdc="docker run --rm -v \"\$(pwd):/data\" minlag/mermaid-cli"`

---

## Usage

### Commands

**`/debate-new`**: Create a new debate

```bash
/debate-new                                    # Interactive setup
/debate-new climate-policy                     # With slug
/debate-new climate-policy "This house..."     # With slug and motion
```

**`/debate-run <slug> <exchanges>`**: Run debate rounds

```bash
/debate-run climate-policy 5
```

**`/debate-report <slug>`**: Generate analysis and visualization

```bash
/debate-report climate-policy
```

### Output Structure

```
pineapples-on-pizza/
├── debate.md                 # Motion and state
├── scores.json               # Score history
├── arguments/
│   ├── prop_000a.md          # Opening arguments
│   ├── prop_000b.md
│   ├── prop_000c.md
│   ├── opp_000a.md
│   ├── opp_000b.md
│   ├── opp_000c.md
│   ├── prop_001.md           # Rebuttal arguments
│   ├── opp_001.md
│   └── ...
├── argument-graph.mmd        # Mermaid source
├── argument-graph.png        # Visual graph (if mmdc installed)
└── README.md                 # Debate analysis
```

---

## Example Debates

**[Halt AI Development](./halt-ai-development/)** — This house would pause the development of artificial general intelligence until robust safety frameworks are established.

<!-- Add more debates as they're created -->

---

<p align="center">
  🌿 ⚖️ 🌿
</p>

<p align="center">
  <i>Built to explore the geometry of argument</i>
</p>

<p align="center">
  <a href="LICENSE">MIT License</a>
</p>
