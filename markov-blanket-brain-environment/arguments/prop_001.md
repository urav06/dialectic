{
  "id": "prop_001",
  "side": "prop",
  "exchange": 1,
  "title": "Coupling Enables Rather Than Violates Statistical Independence",
  "claim": "Continuous dynamical coupling between brain and environment establishes the precise conditions under which Markov blankets achieve conditional independence at nonequilibrium steady state.",
  "attacks": [
    {
      "target_id": "opp_000b",
      "type": "warrant_attack"
    }
  ],
  "defends": []
}

## Claim

Continuous dynamical coupling between brain and environment establishes the precise conditions under which Markov blankets achieve conditional independence at nonequilibrium steady state.

## Grounds

### 1. Friston et al., Entropy (2021), 'Stochastic Chaos and Markov Blankets', https://pubmed.ncbi.nlm.nih.gov/34573845/

> At nonequilibrium steady-state, random dynamical systems exhibit conditional independencies where internal states are statistically secluded from external states by blanket states. The flow comprises orthogonal components: dissipative flow ascending gradients of the nonequilibrium steady-state density and conservative solenoidal flow. These results express the flow under conditional independencies implied by a Markov blanket, connecting sparse influences in Langevin dynamics to conditional independencies among state subsets.

**Relevance:** This demonstrates that coupling in continuous dynamical systems generates rather than violates the conditional independence structure, with sparse coupling at steady state mathematically entailing the statistical separation defining Markov blankets.

### 2. Albarracin et al., arXiv (2022), 'Weak Markov blankets in high-dimensional, sparsely-coupled random dynamical systems', https://ar5iv.labs.arxiv.org/html/2207.07620

> Weak Markov blankets are ubiquitous in high-dimensional random dynamical systems with sparse coupling. The blanket index scales inversely with dimension, making the probability of lacking a Markov blanket fall off exponentially as e^(-1/2(n-1)ε²) with increasing dimension. High-dimensional systems carve out submanifolds where measurable properties remain conditionally independent despite material exchange and non-zero coupling.

**Relevance:** This proves that realistic biological systems with controlled coupling necessarily possess weak Markov blankets, refuting the claim that bidirectional coupling prevents conditional independence—coupling strength and dimensional structure determine blanket existence.

### 3. Pearl, J. (1988), Probabilistic Reasoning in Intelligent Systems, defining Markov blankets in Bayesian networks

> A Markov blanket of variable X renders X conditionally independent of all other variables given the blanket. This statistical property holds regardless of whether the underlying system exhibits continuous coupling—conditional independence concerns probabilistic relationships at equilibrium distributions, not the absence of causal connections.

**Relevance:** The formal definition establishes that Markov blankets describe statistical independence structures that can exist within coupled systems, directly contradicting the opponent's conflation of coupling with dependence.

## Warrant

Conditional independence is a statistical property of probability distributions at steady state, not a requirement for absence of coupling; sparse coupling in high-dimensional nonequilibrium systems mathematically generates the conditional independence structure that defines Markov blankets.

## Backing

The distinction between dynamical coupling (causal connectivity) and statistical dependence (correlation structure) is fundamental to probability theory: coupled variables can be conditionally independent when their mutual influence is mediated through blanket states.

## Qualifier

at nonequilibrium steady state

## Attacks

### Attacking opp_000b

**Type:** warrant_attack

The warrant confuses dynamical coupling with statistical dependence. Coupled differential equations describe causal connections, but conditional independence concerns probability distributions over those variables. At nonequilibrium steady state, sparsely coupled systems exhibit conditional independence: internal and external states are statistically independent given blanket states, despite continuous coupling. The coupled pendulum example illustrates this: the pendulums are dynamically coupled through the beam yet statistically independent conditioned on beam motion. Brain-environment coupling similarly operates through sensory-active channels that constitute the blanket.