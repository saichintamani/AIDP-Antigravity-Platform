from typing import Any

from aidp.cognitive_core.strategy_planner import StrategyPlanner
from aidp.meta_learning.memory_system import MemorySystem


class AdaptivePlanner(StrategyPlanner):
    """
    An evolution of the StrategyPlanner that actively queries historical failure 
    memory before generating a plan. If it finds applicable lessons, it injects them 
    as mandatory constraints.
    """
    
    def __init__(self, memory_system: MemorySystem):
        super().__init__()
        self.memory = memory_system
        
    def query_experience(self, context: str) -> list[str]:
        """
        Asks: 'Have I failed like this before?'
        Returns a list of strict constraints to append to the system prompt.
        """
        lessons = self.memory.learning.get_applicable_lessons(context)
        if not lessons:
            return []
            
        return [lesson.rule for lesson in lessons]
        
    def generate_plan(self, context: str, hypotheses: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Overrides the base planner to inject memory constraints.
        """
        historical_constraints = self.query_experience(context)
        
        # In a real LLM call, these constraints would be appended to the System Prompt.
        # For the prototype, we simply attach them to the generated plan structure.
        
        # Call base implementation (which just returns a mock right now)
        base_plan = super().rank_and_select(hypotheses, top_n=len(hypotheses))
        
        plan = {
            "context": context,
            "selected_hypotheses": base_plan,
            "injected_constraints": historical_constraints
        }
        
        if historical_constraints:
            print(f"[AdaptivePlanner] Injected {len(historical_constraints)} learned constraints into the plan.")
            
        return plan
