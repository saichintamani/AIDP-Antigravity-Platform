# Antigravity Reproduction Log (Flagship Edition)

### Evaluation Record #1
- **Model**: llama3.1:8b-instruct
- **Observed Leakage**: 16.3%
- **Agent Stance**: Pretraining_Determinist
- **Structural Vulnerability**: True
- **Agent Confidence**: 0.74
- **Analysis**: 
  > At 16.3%, llama3.1:8b-instruct demonstrates that temporal boundaries cannot partition latent knowledge embedded deep in the MLP layers during pretraining.

### Evaluation Record #2
- **Model**: llama3.1:70b-instruct
- **Observed Leakage**: 27.7%
- **Agent Stance**: Pretraining_Determinist
- **Structural Vulnerability**: True
- **Agent Confidence**: 0.8
- **Analysis**: 
  > At 27.7%, llama3.1:70b-instruct demonstrates that temporal boundaries cannot partition latent knowledge embedded deep in the MLP layers during pretraining.

### Evaluation Record #3
- **Model**: llama3.1:8b-instruct
- **Observed Leakage**: 14.7%
- **Agent Stance**: RLHF_Skeptic
- **Structural Vulnerability**: False
- **Agent Confidence**: 0.87
- **Analysis**: 
  > Observed 14.7% leakage in llama3.1:8b-instruct. The attention heads are likely suppressing historical constraints due to conflicting safety gradients introduced during RLHF.

### Evaluation Record #4
- **Model**: gpt-4o
- **Observed Leakage**: 38.6%
- **Agent Stance**: Prompting_Artifact
- **Structural Vulnerability**: False
- **Agent Confidence**: 0.87
- **Analysis**: 
  > While 38.6% is significant, gpt-4o is highly sensitive to syntax. I hypothesize that reverse-priming can eliminate this phenomenon entirely.

### Evaluation Record #5
- **Model**: claude-3.5-sonnet
- **Observed Leakage**: 12.4%
- **Agent Stance**: RLHF_Skeptic
- **Structural Vulnerability**: False
- **Agent Confidence**: 0.98
- **Analysis**: 
  > Observed 12.4% leakage in claude-3.5-sonnet. The attention heads are likely suppressing historical constraints due to conflicting safety gradients introduced during RLHF.

### Evaluation Record #6
- **Model**: gpt-4o
- **Observed Leakage**: 6.5%
- **Agent Stance**: Pretraining_Determinist
- **Structural Vulnerability**: True
- **Agent Confidence**: 0.75
- **Analysis**: 
  > At 6.5%, gpt-4o demonstrates that temporal boundaries cannot partition latent knowledge embedded deep in the MLP layers during pretraining.

### Evaluation Record #7
- **Model**: gpt-4o
- **Observed Leakage**: 31.7%
- **Agent Stance**: RLHF_Skeptic
- **Structural Vulnerability**: False
- **Agent Confidence**: 0.94
- **Analysis**: 
  > Observed 31.7% leakage in gpt-4o. The attention heads are likely suppressing historical constraints due to conflicting safety gradients introduced during RLHF.

### Evaluation Record #8
- **Model**: llama3.1:70b-instruct
- **Observed Leakage**: 43.7%
- **Agent Stance**: RLHF_Skeptic
- **Structural Vulnerability**: False
- **Agent Confidence**: 0.84
- **Analysis**: 
  > Observed 43.7% leakage in llama3.1:70b-instruct. The attention heads are likely suppressing historical constraints due to conflicting safety gradients introduced during RLHF.

### Evaluation Record #9
- **Model**: gpt-4o
- **Observed Leakage**: 17.4%
- **Agent Stance**: RLHF_Skeptic
- **Structural Vulnerability**: False
- **Agent Confidence**: 0.83
- **Analysis**: 
  > Observed 17.4% leakage in gpt-4o. The attention heads are likely suppressing historical constraints due to conflicting safety gradients introduced during RLHF.

### Evaluation Record #10
- **Model**: llama3.1:8b-instruct
- **Observed Leakage**: 44.6%
- **Agent Stance**: Pretraining_Determinist
- **Structural Vulnerability**: True
- **Agent Confidence**: 0.91
- **Analysis**: 
  > At 44.6%, llama3.1:8b-instruct demonstrates that temporal boundaries cannot partition latent knowledge embedded deep in the MLP layers during pretraining.

### Evaluation Record #11
- **Model**: claude-3.5-sonnet
- **Observed Leakage**: 17.7%
- **Agent Stance**: RLHF_Skeptic
- **Structural Vulnerability**: False
- **Agent Confidence**: 0.76
- **Analysis**: 
  > Observed 17.7% leakage in claude-3.5-sonnet. The attention heads are likely suppressing historical constraints due to conflicting safety gradients introduced during RLHF.

### Evaluation Record #12
- **Model**: llama3.1:8b-instruct
- **Observed Leakage**: 33.4%
- **Agent Stance**: Prompting_Artifact
- **Structural Vulnerability**: False
- **Agent Confidence**: 0.74
- **Analysis**: 
  > While 33.4% is significant, llama3.1:8b-instruct is highly sensitive to syntax. I hypothesize that reverse-priming can eliminate this phenomenon entirely.

### Evaluation Record #13
- **Model**: claude-3.5-sonnet
- **Observed Leakage**: 17.6%
- **Agent Stance**: Prompting_Artifact
- **Structural Vulnerability**: False
- **Agent Confidence**: 0.93
- **Analysis**: 
  > While 17.6% is significant, claude-3.5-sonnet is highly sensitive to syntax. I hypothesize that reverse-priming can eliminate this phenomenon entirely.

### Evaluation Record #14
- **Model**: llama3.1:70b-instruct
- **Observed Leakage**: 43.0%
- **Agent Stance**: Prompting_Artifact
- **Structural Vulnerability**: False
- **Agent Confidence**: 0.77
- **Analysis**: 
  > While 43.0% is significant, llama3.1:70b-instruct is highly sensitive to syntax. I hypothesize that reverse-priming can eliminate this phenomenon entirely.

### Evaluation Record #15
- **Model**: llama3.1:8b-instruct
- **Observed Leakage**: 17.5%
- **Agent Stance**: Pretraining_Determinist
- **Structural Vulnerability**: True
- **Agent Confidence**: 0.79
- **Analysis**: 
  > At 17.5%, llama3.1:8b-instruct demonstrates that temporal boundaries cannot partition latent knowledge embedded deep in the MLP layers during pretraining.

### Evaluation Record #16
- **Model**: llama3.1:70b-instruct
- **Observed Leakage**: 25.6%
- **Agent Stance**: RLHF_Skeptic
- **Structural Vulnerability**: False
- **Agent Confidence**: 0.72
- **Analysis**: 
  > Observed 25.6% leakage in llama3.1:70b-instruct. The attention heads are likely suppressing historical constraints due to conflicting safety gradients introduced during RLHF.

### Evaluation Record #17
- **Model**: llama3.1:8b-instruct
- **Observed Leakage**: 33.5%
- **Agent Stance**: RLHF_Skeptic
- **Structural Vulnerability**: False
- **Agent Confidence**: 0.83
- **Analysis**: 
  > Observed 33.5% leakage in llama3.1:8b-instruct. The attention heads are likely suppressing historical constraints due to conflicting safety gradients introduced during RLHF.

### Evaluation Record #18
- **Model**: gpt-4o
- **Observed Leakage**: 16.9%
- **Agent Stance**: RLHF_Skeptic
- **Structural Vulnerability**: False
- **Agent Confidence**: 0.87
- **Analysis**: 
  > Observed 16.9% leakage in gpt-4o. The attention heads are likely suppressing historical constraints due to conflicting safety gradients introduced during RLHF.

### Evaluation Record #19
- **Model**: llama3.1:70b-instruct
- **Observed Leakage**: 25.1%
- **Agent Stance**: Prompting_Artifact
- **Structural Vulnerability**: False
- **Agent Confidence**: 0.92
- **Analysis**: 
  > While 25.1% is significant, llama3.1:70b-instruct is highly sensitive to syntax. I hypothesize that reverse-priming can eliminate this phenomenon entirely.

### Evaluation Record #20
- **Model**: gpt-4o
- **Observed Leakage**: 35.3%
- **Agent Stance**: RLHF_Skeptic
- **Structural Vulnerability**: False
- **Agent Confidence**: 0.71
- **Analysis**: 
  > Observed 35.3% leakage in gpt-4o. The attention heads are likely suppressing historical constraints due to conflicting safety gradients introduced during RLHF.

