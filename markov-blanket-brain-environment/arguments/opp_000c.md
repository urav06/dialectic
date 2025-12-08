{
  "id": "opp_000c",
  "side": "opp",
  "exchange": 0,
  "title": "Sensorimotor Channels Exhibit Bidirectional Information Flow",
  "claim": "Sensory channels transmit motor-influenced predictions outward while motor channels receive environmental feedback, preventing unidirectional blanket architecture.",
  "attacks": [],
  "defends": []
}

## Claim

Sensory channels transmit motor-influenced predictions outward while motor channels receive environmental feedback, preventing unidirectional blanket architecture.

## Grounds

### 1. Research on bidirectional brain-machine interfaces and predictive sensing, https://pmc.ncbi.nlm.nih.gov/articles/PMC6733654/

> Bidirectional brain-machine interfaces establish two-way direct communication where decoders translate neural activity into motor commands and encoders deliver sensory information from environment to brain, creating closed-loop systems. Motor signals modulate sensory processing, with motor outputs used to modify sensory system responses to future stimuli. The integration allows animals to use sensory information for motor actions while motor outputs reshape sensory responses.

**Relevance:** This demonstrates that the channels proposed as constituting the Markov blanket actually exhibit bidirectional information flow, contradicting the blanket's requirement that sensory states only receive from external and motor states only output to external.

### 2. Experimental neuroscience on sensory-motor coupling, https://en.wikipedia.org/wiki/Sensory-motor_coupling

> Sensory-motor coupling is the bidirectional process by which sensory inputs from the environment are combined with motor outputs to generate adaptive actions and perceptions. Intelligent behaviors result from continuous and intense interaction of brain with external world mediated by the body, not unidirectional information processing.

**Relevance:** The fundamental bidirectionality of sensorimotor processes means that proposed blanket states themselves exhibit the kind of mutual influence that violates the structural assumptions of Markov blankets.

## Warrant

In Markov blanket formalism, sensory states should only be influenced by external states while active states should only influence external states, but empirical neuroscience shows both types of states exhibit bidirectional coupling with multiple system components.

## Backing

The Markov blanket architecture requires partitioning variables into sensory (parent-less internal nodes) and active (child-less internal nodes) states mediating influence, but this assumes unidirectional causal structure incompatible with feedback loops.

## Qualifier

in embodied neural systems