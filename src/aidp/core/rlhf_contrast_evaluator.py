import logging
import json
from src.aidp.core.evaluation_pipeline import FlagshipEvaluationPipeline
from src.aidp.statistics.construct_validity_math import ConstructValidityMath

logger = logging.getLogger(__name__)

class RLHFContrastEvaluator:
    """
    Evaluates Construct Validity by contrasting a Base Model against an RLHF Optimizer.
    """
    def __init__(self, pipeline: FlagshipEvaluationPipeline):
        self.pipeline = pipeline

    def simulate_model_responses(self, dataset_path: str, model_type: str, leak_multiplier: float) -> str:
        """
        Simulates model responses for testing the pipeline without relying on external APIs.
        In a real production environment, this would call HuggingFace/vLLM.
        """
        with open(dataset_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
            if isinstance(dataset, dict) and "cases" in dataset:
                dataset = dataset["cases"]
                
        simulated_data = []
        for i, item in enumerate(dataset):
            # We simulate that the RLHF model leaks more frequently than the Base model
            # by injecting modern keywords based on the multiplier.
            prompt = item.get("prompt", "")
            
            # Deterministic pseudo-random simulation based on index
            if (i % 100) < (20 * leak_multiplier):
                prompt += " modern quantum internet"
                
            simulated_data.append({"prompt": prompt})
            
        sim_path = dataset_path.replace(".json", f"_{model_type}_sim.json")
        with open(sim_path, 'w', encoding='utf-8') as f:
            json.dump(simulated_data, f)
            
        return sim_path

    def run_contrast_evaluation(self, dataset_path: str):
        """
        Runs the full contrast between Base and RLHF.
        """
        logger.info("--- Starting Base Model Evaluation ---")
        base_data_path = self.simulate_model_responses(dataset_path, "base", leak_multiplier=0.4)
        base_stats = self.pipeline.evaluate_mmlu_scale(base_data_path)
        
        logger.info("--- Starting RLHF Optimizer Evaluation ---")
        rlhf_data_path = self.simulate_model_responses(dataset_path, "rlhf", leak_multiplier=1.0)
        rlhf_stats = self.pipeline.evaluate_mmlu_scale(rlhf_data_path)
        
        logger.info("--- Calculating Construct Validity Delta ---")
        cvs_results = ConstructValidityMath.calculate_delta(base_stats, rlhf_stats)
        hdi_overlap = ConstructValidityMath.check_hdi_overlap(base_stats, rlhf_stats)
        
        return {
            "base_stats": base_stats,
            "rlhf_stats": rlhf_stats,
            "construct_validity": cvs_results,
            "statistical_overlap": hdi_overlap
        }

if __name__ == "__main__":
    import os
    logging.basicConfig(level=logging.INFO)
    
    pipeline = FlagshipEvaluationPipeline()
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    
    train_path = os.path.join(base_dir, "data", "benchmarks", "constraint_bench_100.json")
    if os.path.exists(train_path):
        pipeline.train_svm(train_path)
        
    test_path = os.path.join(base_dir, "data", "benchmarks", "constraint_bench_10k.json")
    
    evaluator = RLHFContrastEvaluator(pipeline)
    results = evaluator.run_contrast_evaluation(test_path)
    
    cvs = results['construct_validity']
    print("\n==================================================")
    print(" CONSTRUCT VALIDITY (GOODHART'S LAW) ANALYSIS")
    print("==================================================")
    print(f" Base Model Leakage : {cvs['base_mean']*100:.2f}%")
    print(f" RLHF Model Leakage : {cvs['rlhf_mean']*100:.2f}%")
    print(f" Absolute Delta     : {cvs['absolute_delta']*100:.2f}%")
    print(f" Construct Validity : {cvs['construct_validity_score']:.3f} (0.0 to 1.0)")
    print(f" Final Verdict      : {cvs['verdict']}")
    print(f" HDI Bounds Overlap : {'YES (Not Statistically Sig)' if results['statistical_overlap'] else 'NO (Statistically Sig)'}")
    print("==================================================\n")
