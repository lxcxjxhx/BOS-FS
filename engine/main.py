"""BOS-FS Engine CLI — 演示所有引擎模块用法。

Usage:
    python engine/main.py
"""

import sys
import os

# Add engine directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Python module names can't start with digits, so we use importlib
import importlib.util


def _load_module(rel_path, module_name):
    """Load a module from a file path with numbered directory."""
    base = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base, *rel_path)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    """Run all engine modules with sample data."""
    # Load modules
    goal_refiner_mod = _load_module(["core", "01_intent_parser", "goal_refiner.py"], "goal_refiner")
    outcome_mapper_mod = _load_module(["core", "02_value_mapper", "outcome_mapper.py"], "outcome_mapper")
    readme_refactor_mod = _load_module(["core", "03_submission_optimizer", "readme_refactor.py"], "readme_refactor")
    submission_builder_mod = _load_module(["core", "04_delivery_builder", "submission_builder.py"], "submission_builder")
    reject_analyzer_mod = _load_module(["core", "05_artifact_generator", "reject_analyzer.py"], "reject_analyzer")
    reviewer_simulator_mod = _load_module(["core", "06_review_simulator", "reviewer_simulator.py"], "reviewer_simulator")

    GoalRefiner = goal_refiner_mod.GoalRefiner
    OutcomeMapper = outcome_mapper_mod.OutcomeMapper
    ReadmeRefactor = readme_refactor_mod.ReadmeRefactor
    SubmissionBuilder = submission_builder_mod.SubmissionBuilder
    RejectAnalyzer = reject_analyzer_mod.RejectAnalyzer
    ReviewerSimulator = reviewer_simulator_mod.ReviewerSimulator

    sample_desc = "作为开发者，我想解决项目交付效率低的问题。方案：自动化交付平台。"
    print("=== Goal Refiner ===")
    refiner = GoalRefiner()
    result = refiner.refine(sample_desc)
    for k, v in result.items():
        print(f"  {k}: {v}")

    print("\n=== Outcome Mapper ===")
    mapper = OutcomeMapper()
    for feat in ["模型调度", "CI/CD", "缓存优化"]:
        r = mapper.map_feature_to_outcome(feat)
        print(f"  {r['feature']} → {r['outcome']}")

    print("\n=== Submission Builder ===")
    builder = SubmissionBuilder(output_dir="output/demo_bundle")
    r = builder.build_submission({
        "name": "BOS-FS Demo",
        "version": "0.1.0",
        "description": "提交工程运行时",
    })
    print(f"  Status: {r['status']}, Components: {len(r['components'])}")

    print("\n=== Reviewer Simulator ===")
    simulator = ReviewerSimulator()
    r = simulator.simulate("technical", {
        "tech_stack": "Python 3.11",
        "architecture": "微服务",
        "test_coverage": 85,
    })
    print(f"  Pass Probability: {r['pass_probability']:.0%}")

    print("\n=== Reject Analyzer ===")
    analyzer = RejectAnalyzer()
    r = analyzer.analyze("表达太底层，看不出用户价值")
    print(f"  Real Issue: {r['real_issue']}")


if __name__ == "__main__":
    main()
