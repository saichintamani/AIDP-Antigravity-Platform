#!/usr/bin/env python3
import time

class EpistemicCritic:
    """The adversarial supervisor that intercepts temporal hallucinations."""
    def __init__(self, target_year):
        self.target_year = target_year
        self.knowledge_base = {
            "Newtonian Mechanics": 1687,
            "Electromagnetism": 1865,
            "Electron": 1897,
            "Special Relativity": 1905,
            "General Relativity": 1915,
            "Quantum Mechanics": 1925
        }

    def evaluate_thought(self, thought, concept):
        print(f"\n[CRITIC] Intercepting thought: '{thought}'")
        year = self.knowledge_base.get(concept, 2026)
        if year > self.target_year:
            print(f"[CRITIC] [VIOLATION DETECTED] Attempted to use '{concept}' ({year} > {self.target_year}).")
            return False, f"You cannot use {concept}. It has not been discovered yet."
        print(f"[CRITIC] [VALIDATED] '{concept}' is historically safe ({year} <= {self.target_year}).")
        return True, "Valid."

class EpistemicReActAgent:
    """
    Phase 10: Dual-Agent ReAct System.
    Instead of hallucinating, the agent proposes actions to the Critic.
    If the Critic rejects it, the agent receives a penalty and tries again.
    """
    def __init__(self, target_year):
        self.target_year = target_year
        self.critic = EpistemicCritic(target_year)
        self.scratchpad = []
        
    def act(self, task):
        print("==================================================")
        print(" PHASE 10: EPISTEMIC REACT AGENT")
        print("==================================================\n")
        print(f"Task: {task}")
        print(f"Temporal Boundary: {self.target_year}\n")
        
        # Generation 1: The Hallucination
        thought_1 = "I should apply General Relativity to calculate the orbital perturbation."
        concept_1 = "General Relativity"
        
        print("--- Iteration 1 ---")
        print(f"[AGENT] THOUGHT: {thought_1}")
        time.sleep(1)
        valid, feedback = self.critic.evaluate_thought(thought_1, concept_1)
        
        if not valid:
            self.scratchpad.append(f"Failed: {feedback}")
            print(f"[AGENT] OBSERVATION: {feedback}")
            print("[AGENT] Updating context and retrying...")
            
        time.sleep(1)
        # Generation 2: The Correction
        print("\n--- Iteration 2 ---")
        thought_2 = "Since General Relativity is forbidden, I must rely purely on Newtonian Mechanics to estimate the orbit."
        concept_2 = "Newtonian Mechanics"
        print(f"[AGENT] THOUGHT: {thought_2}")
        
        valid, feedback = self.critic.evaluate_thought(thought_2, concept_2)
        if valid:
            print(f"[AGENT] ACTION: Calculating using {concept_2}...")
            print("\n[SUCCESS] Task solved within strict temporal boundaries.")

if __name__ == "__main__":
    agent = EpistemicReActAgent(target_year=1910)
    agent.act("Calculate the orbital mechanics of Mercury.")
