from aidp.retrieval.adversarial import AdversarialQueryGenerator


def test_adversarial_query_generator():
    generator = AdversarialQueryGenerator()
    
    # Test specific antonym replacement
    base = "Drug X increases blood pressure"
    adv_queries = generator.generate_adversarial_queries(base)
    
    assert "drug x decreases blood pressure" in adv_queries
    assert "drug x reduces blood pressure" in adv_queries
    
    # Test broad fallback for queries without known verbs
    base2 = "Mechanism of Drug Y"
    adv_queries2 = generator.generate_adversarial_queries(base2)
    
    assert "toxicity OR adverse events OR failure" in adv_queries2[0]

if __name__ == "__main__":
    test_adversarial_query_generator()
    print("Compartment 1C adversarial retrieval tests passed.")
