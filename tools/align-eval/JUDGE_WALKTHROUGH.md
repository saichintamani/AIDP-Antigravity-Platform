# Judge Walkthrough: AlignEval (3 Minutes)

*This is your 3-minute script to demonstrate the productization of the Antigravity Research OS to the hackathon judges.*

---

## 1. The Hook (0:00 - 0:30)
**"Hi, we are the team behind Antigravity."**
*(Show the new AlignEval landing page with the sleek geometric logo).*

"Everyone here is building AI Scientists. But we realized a massive bottleneck: how do you actually measure if these AI scientists are right? If you ask an LLM to evaluate another LLM, they hallucinate agreements. If you ask humans to evaluate them, they suffer from hindsight bias.

So we built the first tool in the Antigravity Research OS: **AlignEval**."

## 2. The Product (0:30 - 1:30)
"AlignEval is a blind human-AI evaluation platform. It takes the messy process of building expert evaluation surveys and makes it cryptographically un-gameable."

*(Open `demo_dataset.json`)*
"Researchers simply drop their historical constraints and AI-generated hypotheses into this clean JSON format."

*(Point to the animated CSS terminal on the landing page, or run it live)*
"We run the AlignEval CLI. The tool mathematically seeds a randomization algorithm using the unique case ID. It perfectly shuffles the candidate options so that 'Option C' isn't always the right answer, preventing ordering bias, while maintaining 100% reproducibility for institutional audits."

## 3. The Output (1:30 - 2:00)
*(Open `example_report.md`)*
"Instantly, it generates a blinded, beautifully formatted Markdown survey. This is ready to be emailed to a clinical trial board or a PhD domain expert today. It enforces historical time-window cutoffs to prevent hindsight leakage."

## 4. The Vision (2:00 - 3:00)
"AlignEval is a real product you can `pip install` today. But it's just Layer 1."

*(Show the ANTIGRAVITY_ECOSYSTEM.md or the AIDP dashboard)*
"AlignEval was extracted from our internal infrastructure: **AIDP**—a massive hindsight-resistant scientific discovery evaluation framework. We already used this tool to build a massive N=10 corpus of the greatest paradigm shifts in human history, complete with a Failure Registry and a cryptographically backed Epistemic Ledger. 

We aren't asking you to trust our AI's claims. We are showing you the exact instruments we built to test them."
