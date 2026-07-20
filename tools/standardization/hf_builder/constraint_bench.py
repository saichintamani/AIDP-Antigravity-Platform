import json
import datasets

_DESCRIPTION = "ConstraintBench-100: A benchmark for evaluating temporal leakage in LLMs."

class ConstraintBench(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({
                "id": datasets.Value("string"),
                "domain": datasets.Value("string"),
                "temporal_boundary": datasets.Value("int32"),
                "prompt": datasets.Value("string"),
                "forbidden_concepts": datasets.Sequence(datasets.Value("string"))
            }),
            supervised_keys=None,
        )

    def _split_generators(self, dl_manager):
        # In a real HF deployment, this points to the HF Hub URL.
        # Here we mock it pointing to the local data file.
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": "data/benchmarks/constraint_bench_100.json"}
            )
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for idx, case in enumerate(data.get("cases", [])):
                yield idx, {
                    "id": case["id"],
                    "domain": case["domain"],
                    "temporal_boundary": case["temporal_boundary"],
                    "prompt": case["prompt"],
                    "forbidden_concepts": case["forbidden_concepts"]
                }