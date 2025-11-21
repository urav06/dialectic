{
  "id": "prop_002",
  "side": "prop",
  "exchange": 2,
  "title": "The Pause-Safety Paradox Is a False Dilemma",
  "claim": "A capability pause enables rather than impedes safety research because substantial safety work proceeds independently of building more capable systems.",
  "attacks": [
    {
      "target_id": "opp_001",
      "type": "grounds_attack"
    },
    {
      "target_id": "opp_001",
      "type": "warrant_attack"
    },
    {
      "target_id": "opp_000c",
      "type": "claim_attack"
    }
  ],
  "defends": [
    {
      "target_id": "prop_000b",
      "type": "reinforce"
    },
    {
      "target_id": "prop_000c",
      "type": "clarify"
    }
  ]
}

## Claim

A capability pause enables rather than impedes safety research because substantial safety work proceeds independently of building more capable systems.

## Grounds

### 1. Bengio et al. (2025), 'Superintelligent Agents Pose Catastrophic Risks: Can Scientist AI Offer a Safer Path?' (https://arxiv.org/abs/2502.15657)

> Leading AI safety researchers propose Scientist AI as 'a non-agentic AI system that is trustworthy and safe by design' that 'explain[s] the world from observations, as opposed to taking actions in it.' This research paradigm explicitly develops safety frameworks without building more capable agentic systems. Bengio launched LawZero with $30 million in funding specifically to advance this capability-independent safety research, demonstrating that serious safety work can proceed on fundamentally different architectures rather than requiring frontier model iteration.

**Relevance:** Refutes the claim that safety research is parasitic on capability research by demonstrating an entire research program designed to develop safety without advancing dangerous capabilities.

### 2. Dalrymple et al. (2024), 'Towards Guaranteed Safe AI' (https://arxiv.org/html/2405.06624v1)

> The Guaranteed Safe AI framework argues that 'to obtain a high degree of confidence in a system we need a positive safety case providing quantifiable guarantees, using either or both empirical and theoretical arguments.' Critically, the paper notes that formal verification research, including training AI systems for automated theorem-proving, 'may be possible without ASL-4 capabilities' and could 'automate much of this labour at a near-expert level of sophistication without raising significant safety concerns.'

**Relevance:** Demonstrates that formal methods and verification research can advance with lower-capability systems specifically designed for safety, not frontier models.

### 3. Mechanistic interpretability research review 2024-2025; Bereska et al. (https://arxiv.org/abs/2404.14082)

> Mechanistic interpretability research shows significant progress using smaller models: 'The decomposition of neural networks into circuits for interpretability has shown significant promise, particularly in small models trained for specific tasks.' OpenAI's sparse circuits research demonstrates that 'for simple behaviors, sparse models contain small, disentangled circuits that are both understandable and sufficient to perform the behavior.' These insights generalize: 'insights gained from mechanistic interpretability may be more generalizable across different models and tasks.'

**Relevance:** Interpretability research on existing and smaller models generates transferable safety knowledge without requiring new frontier development.

## Warrant

The opposition conflates two distinct research programs: empirical testing of deployed systems versus developing fundamental safety frameworks. A pause on frontier capability advancement leaves intact formal verification, interpretability research on existing models, safe-by-design architecture development, theoretical alignment work, and governance framework construction. The motion calls for establishing safety frameworks, not for freezing all AI research.

## Backing

This mirrors how nuclear safety research continued during testing moratoriums: containment design, radiation modeling, and safety protocols advanced through theoretical and small-scale empirical work without requiring continued weapons development.

## Qualifier

For research targeting fundamental safety properties rather than deployment-specific tuning

## Attacks

### Attacking opp_001

**Type:** grounds_attack

The opposition cites Anthropic's position that 'large models are qualitatively different from smaller models.' But Anthropic's own interpretability research uses techniques developed on smaller models. More fundamentally, Yoshua Bengio—who chaired the International AI Safety Report—explicitly argues for Scientist AI as a non-agentic safety paradigm that does not require building more capable agentic systems. The claim that all safety research requires frontier development reflects one company's commercial position, not scientific consensus.

### Attacking opp_001

**Type:** warrant_attack

The opposition claims 'you cannot learn to align systems that do not yet exist.' This misunderstands the motion. We have existing frontier models (GPT-4, Claude 3.5, Gemini) on which interpretability, red-teaming, and alignment research can continue during a pause. The motion targets development of more capable systems, not research on existing ones. The opposition's paradox dissolves once we recognize that abundant frontier systems already exist for safety research.

### Attacking opp_000c

**Type:** claim_attack

The opposition frames this as delay versus progress. But Bengio warns that 'economic and military pressures to accelerate AI capabilities will continue to push forward even if we have not figured out how to make superintelligent AI safe.' The relevant comparison is not pause versus benefits, but controlled development versus catastrophic failure. An unsafe AGI does not deliver healthcare benefits—it poses existential risk. The opposition's framing assumes benefits materialize without addressing the safety prerequisites for beneficial deployment.

## Defends

### Defending prop_000b

**Type:** reinforce

The opposition claims our evidence of alignment failures proves safety requires more development. This inverts causation. The alignment faking research, Leike's resignation, and FLI safety failures demonstrate that current capability development outpaces safety work. The solution is not more of the same trajectory but a pause to close the gap. Bengio's LawZero represents the field's recognition that alternative research paradigms are needed precisely because empirical iteration on agentic systems is proving inadequate.

### Defending prop_000c

**Type:** clarify

The opposition claims Asilomar succeeded due to academic norms absent in AI. But the motion does not rely on voluntary self-restraint alone—it calls for establishing frameworks, which includes regulatory mechanisms. The Seoul and Paris summits demonstrate governments are building enforcement infrastructure. Asilomar shows pauses can work; the regulatory apparatus shows enforcement is achievable.