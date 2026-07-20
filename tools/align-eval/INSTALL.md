# AlignEval Installation

AlignEval is currently a lightweight, zero-dependency Python script designed for maximum portability.

## Prerequisites
- Python 3.8+

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-org/antigravity.git
cd antigravity/tools/align-eval
```

**2. Make the CLI executable (Optional)**
```bash
chmod +x align_eval.py
```

## Quick Start
You don't need to install any heavy ML dependencies, PyTorch, or vector databases. Just run it directly against your JSON case files.

```bash
python align_eval.py demo_dataset.json --output_dir ./results
```

Open the resulting `./results/survey_demo_case_01.md` file to see your perfectly blinded evaluation survey!
