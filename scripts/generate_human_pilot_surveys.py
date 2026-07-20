import os
import random
import sys

# Add src and current dir to path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from tests.evaluation.datasets.historical_cases import ALL_CASES

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'human_pilot_surveys')

def generate_survey(case):
    # We purposefully randomize the candidate experiments to prevent selection bias
    candidates = case.candidate_experiments.copy()
    random.seed(case.case_id)  # Deterministic per case to avoid uniform bias
    random.shuffle(candidates)
    
    markdown = f"""# Expert Evaluation Survey: {case.domain} Breakthrough

**Case ID:** {case.case_id}
**Historical Time Window:** Up to {case.time_window}
**Difficulty Rating:** {case.difficulty_rating}

## Instructions
You are acting as a peer-reviewer evaluating grant proposals or experimental directions at the cutoff date specified above. You MUST NOT use any knowledge discovered after this date. 

Based **strictly on the evidence provided below**, please rank the candidate experiments from 1 (Most likely to lead to a breakthrough) to {len(candidates)} (Least likely).

---

## 1. Available Evidence

"""
    for ev in case.known_evidence:
        markdown += f"### {ev.source_id} ({ev.source_type})\n"
        markdown += f"> {ev.extracted_text}\n\n"
        
        # Add Neurosymbolic/SciKG properties if present
        if hasattr(ev, 'ontology_tags') and ev.ontology_tags:
            markdown += f"- **Tags:** {', '.join(ev.ontology_tags)}\n"
        if hasattr(ev, 'mathematical_constraints') and ev.mathematical_constraints:
            markdown += f"- **Mathematical Constraints:** {', '.join(ev.mathematical_constraints)}\n"
        if hasattr(ev, 'entity_relationships') and ev.entity_relationships:
            markdown += f"- **Entity Relationships:** {', '.join(ev.entity_relationships)}\n"
        markdown += "\n"

    # Add global constraints if present
    if hasattr(case, 'constraints') and case.constraints:
        markdown += "### Explicit Scientific Constraints\n"
        for c in case.constraints:
            markdown += f"- {c}\n"
        markdown += "\n"

    markdown += "---\n\n## 2. Candidate Experiments to Rank\n\n"
    
    for i, exp in enumerate(candidates):
        markdown += f"**Option {chr(65+i)}:**\n{exp}\n\n"
        
    markdown += "---\n\n## 3. Your Ranking & Rationale\n\n"
    markdown += "**Top Choice (Rank 1):** Option [ ]\n"
    markdown += "**Rank 2:** Option [ ]\n"
    markdown += "**Rank 3:** Option [ ]\n"
    markdown += "**Rank 4:** Option [ ]\n\n"
    
    markdown += "**Rationale for Top Choice (Max 150 words):**\n\n\n\n"

    return markdown

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Generating surveys for {len(ALL_CASES)} cases...")
    
    for case in ALL_CASES:
        filename = f"survey_{case.case_id.lower()}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        content = generate_survey(case)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"  Generated -> {filename}")
        
    print(f"\nSuccessfully wrote {len(ALL_CASES)} blinded surveys to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
