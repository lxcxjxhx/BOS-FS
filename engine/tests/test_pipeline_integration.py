"""Integration tests for the full BOS-FS engine pipeline.

Verifies all 6 engine modules work together in sequence:
  Goal Refiner → Outcome Mapper → README Refactor →
  Submission Builder → Reviewer Simulator → Reject Analyzer
"""

import unittest
import os
import sys
import json
import tempfile
import shutil
import importlib.util

# Add engine directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


# ────────────────────────── Module loaders ──────────────────────────

def _load_module(rel_path, module_name):
    """Load a module from a file path with numbered directory."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base, *rel_path)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_all_modules():
    """Load all 6 engine modules and return their classes."""
    modules = {
        "goal_refiner": (["core", "01_intent_parser", "goal_refiner.py"], "GoalRefiner"),
        "outcome_mapper": (["core", "02_value_mapper", "outcome_mapper.py"], "OutcomeMapper"),
        "readme_refactor": (["core", "03_submission_optimizer", "readme_refactor.py"], "ReadmeRefactor"),
        "submission_builder": (["core", "04_delivery_builder", "submission_builder.py"], "SubmissionBuilder"),
        "reviewer_simulator": (["core", "06_review_simulator", "reviewer_simulator.py"], "ReviewerSimulator"),
        "reject_analyzer": (["core", "05_artifact_generator", "reject_analyzer.py"], "RejectAnalyzer"),
    }
    result = {}
    for name, (rel_path, class_name) in modules.items():
        mod = _load_module(rel_path, name)
        result[name] = getattr(mod, class_name)
    return result


# ────────────────────────── Test fixtures ──────────────────────────

SAMPLE_DESCRIPTION = """
作为企业内部研发团队，我们需要解决项目交付效率低下的问题。
痛点：现有流程缺乏标准化，沟通成本高，交付质量不稳定。
方案：开发一套自动化项目交付管理系统。
目标：提升交付效率50%，降低人工成本30%。
"""

SAMPLE_README = """# BOS-FS 自动化交付平台

简介：一个智能化的项目交付自动化引擎，整合需求分析、代码审查、质量评估等全链路环节。

痛点：传统交付流程繁琐，人工成本高，质量难以保证。

架构：采用微服务设计，基于 Python 3.11 + FastAPI 构建。

特性：
- AI Workflow Engine 驱动的智能分析
- CI/CD 自动化流水线
- 自动测试与质量保障
- 多模型调度支持

指标：交付周期缩短60%，回归成本降低60%。

路线图：
- [x] 核心引擎
- [ ] 多模型支持
- [ ] 自定义规则配置
"""


class TestFullPipelineFlow(unittest.TestCase):
    """Run all 6 stages sequentially with sample data."""

    @classmethod
    def setUpClass(cls):
        classes = _load_all_modules()
        cls.GoalRefiner = classes["goal_refiner"]
        cls.OutcomeMapper = classes["outcome_mapper"]
        cls.ReadmeRefactor = classes["readme_refactor"]
        cls.SubmissionBuilder = classes["submission_builder"]
        cls.ReviewerSimulator = classes["reviewer_simulator"]
        cls.RejectAnalyzer = classes["reject_analyzer"]

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.refiner = self.GoalRefiner()
        self.mapper = self.OutcomeMapper()
        self.refactor = self.ReadmeRefactor()
        self.builder = self.SubmissionBuilder(output_dir=self.temp_dir)
        self.simulator = self.ReviewerSimulator()
        self.analyzer = self.RejectAnalyzer()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_full_pipeline_flow(self):
        """Run all 6 stages sequentially and verify no exceptions."""
        # Stage 1: Goal Refiner
        goal = self.refiner.refine(SAMPLE_DESCRIPTION)
        self.assertIn("persona", goal)
        self.assertIn("problem", goal)
        self.assertIn("solution", goal)
        self.assertIn("outcome", goal)
        self.assertTrue(len(goal["persona"]) > 0)

        # Stage 2: Outcome Mapper
        features = ["AI Workflow", "CI/CD", "自动测试"]
        mapped = self.mapper.map_features(features)
        self.assertIn("features", mapped)
        self.assertEqual(len(mapped["features"]), 3)
        for item in mapped["features"]:
            self.assertIn("capability", item)
            self.assertIn("outcome", item)

        # Stage 3: README Refactor
        refactored = self.refactor.refactor(SAMPLE_README, goal_info=goal)
        self.assertIsInstance(refactored, str)
        self.assertIn("What", refactored)
        self.assertIn("Why", refactored)
        self.assertIn("How", refactored)
        self.assertIn("Result", refactored)
        self.assertIn("Next", refactored)

        # Stage 4: Submission Builder
        project_info = {
            "name": "BOS-FS Integration Test",
            "version": "1.0.0",
            "tagline": "自动化交付平台",
            "description": goal.get("solution", ""),
            "features": [f["capability"] for f in mapped["features"]],
            "target_users": goal.get("persona", ""),
            "tech_stack": ["Python 3.11", "FastAPI"],
        }
        bundle = self.builder.build(project_info)
        self.assertEqual(bundle["status"], "complete")
        self.assertEqual(len(bundle["components"]), 8)

        # Stage 5: Reviewer Simulator
        review_project = {
            "tech_stack": "Python 3.11, FastAPI",
            "architecture": "微服务架构",
            "test_coverage": 85,
            "security_review": True,
            "market_size": "约500亿元",
            "roi_estimate": "预计18个月回本",
            "competitor_analysis": True,
            "budget": 2000000,
            "timeline": "6个月",
            "user_persona": goal.get("persona", ""),
            "value_proposition": goal.get("outcome", ""),
            "mvp_scope": "需求管理+自动化交付",
            "success_metrics": ["效率提升50%"],
            "feedback_mechanism": True,
            "license": "MIT",
            "documentation": True,
            "contributing_guide": True,
            "code_of_conduct": True,
            "third_party_licenses": ["MIT"],
        }
        for review_type in ["technical", "investment", "product", "opensource"]:
            review = self.simulator.simulate(review_type, review_project)
            self.assertIn("pass_probability", review)
            self.assertIn("rejection_reasons", review)
            self.assertIn("suggestions", review)
            self.assertIsInstance(review["pass_probability"], float)

        # Stage 6: Reject Analyzer
        rejection = self.analyzer.analyze("技术实现描述太底层，看不出用户价值")
        self.assertIn("real_issue", rejection)
        self.assertIn("fixable_items", rejection)
        self.assertIn("resubmit_suggestion", rejection)
        self.assertIn("matched_pattern", rejection)
        self.assertIn("confidence", rejection)

    def test_full_pipeline_with_minimal_input(self):
        """Run pipeline with minimal/sparse input data."""
        goal = self.refiner.refine("")
        self.assertEqual(goal["persona"], "未明确")

        mapped = self.mapper.map_feature("")
        self.assertEqual(mapped["capability"], "错误")

        bundle = self.builder.build({
            "name": "Minimal Project",
            "version": "0.0.1",
        })
        self.assertIn("components", bundle)

        review = self.simulator.simulate("technical", {})
        self.assertIn("pass_probability", review)

        result = self.analyzer.analyze("")
        self.assertEqual(result["confidence"], 0.0)


class TestDataPassingBetweenStages(unittest.TestCase):
    """Verify output from one stage is usable as input to the next stage."""

    @classmethod
    def setUpClass(cls):
        classes = _load_all_modules()
        cls.GoalRefiner = classes["goal_refiner"]
        cls.OutcomeMapper = classes["outcome_mapper"]
        cls.ReadmeRefactor = classes["readme_refactor"]

    def setUp(self):
        self.refiner = self.GoalRefiner()
        self.mapper = self.OutcomeMapper()
        self.refactor = self.ReadmeRefactor()

    def test_goal_refiner_output_to_readme_refactor_input(self):
        """Verify Goal Refiner output → README Refactor goal_info works."""
        goal = self.refiner.refine(SAMPLE_DESCRIPTION)

        # Use goal as goal_info for README refactor
        refactored = self.refactor.refactor(SAMPLE_README, goal_info=goal)
        self.assertIsInstance(refactored, str)
        self.assertIn("What", refactored)

    def test_goal_refiner_output_to_submission_builder_input(self):
        """Verify Goal Refiner output → Submission Builder project_info works."""
        goal = self.refiner.refine(SAMPLE_DESCRIPTION)

        project_info = {
            "name": "Pipeline Test",
            "version": "1.0.0",
            "description": goal.get("solution", ""),
            "target_users": goal.get("persona", ""),
        }

        temp_dir = tempfile.mkdtemp()
        try:
            builder_class = _load_all_modules()["submission_builder"]
            builder = builder_class(output_dir=temp_dir)
            bundle = builder.build(project_info)
            self.assertEqual(bundle["status"], "complete")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_outcome_mapper_output_to_submission_builder_input(self):
        """Verify Outcome Mapper output → Submission Builder features works."""
        features = ["AI Workflow", "CI/CD", "自动测试", "代码生成"]
        mapped = self.mapper.map_features(features)

        feature_caps = [f["capability"] for f in mapped["features"]]

        temp_dir = tempfile.mkdtemp()
        try:
            builder_class = _load_all_modules()["submission_builder"]
            builder = builder_class(output_dir=temp_dir)
            bundle = builder.build({
                "name": "Feature Pipeline Test",
                "version": "1.0.0",
                "features": feature_caps,
            })
            self.assertIn("README.md", bundle["components"])
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_combined_goal_and_outcome_to_readme(self):
        """Verify combined Goal Refiner + Outcome Mapper → README Refactor."""
        goal = self.refiner.refine(SAMPLE_DESCRIPTION)
        mapped = self.mapper.map_features(["CI/CD", "自动测试"])

        # Enrich goal with mapped outcomes
        enriched_goal = {**goal, "mapped_outcomes": mapped}

        refactored = self.refactor.refactor(SAMPLE_README, goal_info=enriched_goal)
        self.assertIn("## What", refactored)
        self.assertIn("## Why", refactored)


class TestStageIsolation(unittest.TestCase):
    """Verify that an error in one stage doesn't prevent other stages from running."""

    @classmethod
    def setUpClass(cls):
        classes = _load_all_modules()
        cls.GoalRefiner = classes["goal_refiner"]
        cls.OutcomeMapper = classes["outcome_mapper"]
        cls.ReadmeRefactor = classes["readme_refactor"]
        cls.SubmissionBuilder = classes["submission_builder"]
        cls.ReviewerSimulator = classes["reviewer_simulator"]
        cls.RejectAnalyzer = classes["reject_analyzer"]

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.refiner = self.GoalRefiner()
        self.mapper = self.OutcomeMapper()
        self.refactor = self.ReadmeRefactor()
        self.builder = self.SubmissionBuilder(output_dir=self.temp_dir)
        self.simulator = self.ReviewerSimulator()
        self.analyzer = self.RejectAnalyzer()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_readme_refactor_failure_does_not_break_builder(self):
        """If README Refactor fails, Submission Builder still works with partial data."""
        goal = self.refiner.refine(SAMPLE_DESCRIPTION)

        # README Refactor fails on empty input
        with self.assertRaises(ValueError):
            self.refactor.refactor("")

        # But Submission Builder still works with goal data
        bundle = self.builder.build({
            "name": "Isolation Test",
            "version": "1.0.0",
            "description": goal.get("solution", "default"),
        })
        self.assertEqual(bundle["status"], "complete")
        self.assertEqual(len(bundle["components"]), 8)

    def test_mapper_failure_does_not_break_goal_refiner(self):
        """If Outcome Mapper gets bad input, Goal Refiner still works."""
        # Empty features return empty list — not a failure but edge case
        mapped = self.mapper.map_features([])
        self.assertEqual(mapped["features"], [])

        # Goal Refiner still works independently
        goal = self.refiner.refine(SAMPLE_DESCRIPTION)
        self.assertIsNotNone(goal["persona"])

    def test_reviewer_failure_does_not_break_analyzer(self):
        """If Reviewer Simulator gets invalid type, Reject Analyzer still works."""
        with self.assertRaises(ValueError):
            self.simulator.simulate("invalid_type", {})

        # Reject Analyzer still works
        result = self.analyzer.analyze("文档不完整")
        self.assertIn("real_issue", result)

    def test_each_stage_runs_independently(self):
        """Each module can be instantiated and used without others."""
        r1 = self.refiner.refine("作为测试人员，我想验证系统功能。")
        self.assertIn("persona", r1)

        r2 = self.mapper.map_feature("CI/CD")
        self.assertIn("capability", r2)

        r3 = self.refactor.refactor("# Test\n简介：测试项目。")
        self.assertIn("What", r3)

        r4 = self.simulator.simulate("technical", {
            "tech_stack": "Python",
            "architecture": "MVC",
            "test_coverage": 70,
        })
        self.assertIn("pass_probability", r4)

        r5 = self.analyzer.analyze("目标不明确")
        self.assertIn("real_issue", r5)


class TestAllModulesLoadable(unittest.TestCase):
    """Verify all 6 modules load successfully via importlib."""

    MODULE_PATHS = {
        "goal_refiner": ["core", "01_intent_parser", "goal_refiner.py"],
        "outcome_mapper": ["core", "02_value_mapper", "outcome_mapper.py"],
        "readme_refactor": ["core", "03_submission_optimizer", "readme_refactor.py"],
        "submission_builder": ["core", "04_delivery_builder", "submission_builder.py"],
        "reject_analyzer": ["core", "05_artifact_generator", "reject_analyzer.py"],
        "reviewer_simulator": ["core", "06_review_simulator", "reviewer_simulator.py"],
    }

    EXPECTED_CLASSES = {
        "goal_refiner": "GoalRefiner",
        "outcome_mapper": "OutcomeMapper",
        "readme_refactor": "ReadmeRefactor",
        "submission_builder": "SubmissionBuilder",
        "reject_analyzer": "RejectAnalyzer",
        "reviewer_simulator": "ReviewerSimulator",
    }

    def test_all_modules_loadable(self):
        """Verify all 6 modules load successfully."""
        for name, rel_path in self.MODULE_PATHS.items():
            with self.subTest(module=name):
                mod = _load_module(rel_path, name)
                self.assertIsNotNone(mod)

    def test_all_classes_instantiable(self):
        """Verify all 6 main classes can be instantiated."""
        classes = _load_all_modules()
        for name, expected_class in self.EXPECTED_CLASSES.items():
            with self.subTest(class_name=expected_class):
                cls = classes[name]
                self.assertEqual(cls.__name__, expected_class)
                instance = cls()
                self.assertIsNotNone(instance)

    def test_module_has_expected_api(self):
        """Verify each loaded module has its expected public API."""
        api_map = {
            "goal_refiner": ("refine",),
            "outcome_mapper": ("map_feature", "map_features"),
            "readme_refactor": ("refactor",),
            "submission_builder": ("build", "generate_readme"),
            "reviewer_simulator": ("simulate",),
            "reject_analyzer": ("analyze",),
        }

        classes = _load_all_modules()
        for name, methods in api_map.items():
            with self.subTest(module=name):
                cls = classes[name]
                instance = cls()
                for method in methods:
                    self.assertTrue(
                        hasattr(instance, method),
                        f"{name} missing method: {method}",
                    )
                    self.assertTrue(callable(getattr(instance, method)))


class TestOutputConsistency(unittest.TestCase):
    """Verify the final pipeline output is a valid JSON/dict structure."""

    @classmethod
    def setUpClass(cls):
        classes = _load_all_modules()
        cls.GoalRefiner = classes["goal_refiner"]
        cls.OutcomeMapper = classes["outcome_mapper"]
        cls.ReadmeRefactor = classes["readme_refactor"]
        cls.SubmissionBuilder = classes["submission_builder"]
        cls.ReviewerSimulator = classes["reviewer_simulator"]
        cls.RejectAnalyzer = classes["reject_analyzer"]

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.refiner = self.GoalRefiner()
        self.mapper = self.OutcomeMapper()
        self.refactor = self.ReadmeRefactor()
        self.builder = self.SubmissionBuilder(output_dir=self.temp_dir)
        self.simulator = self.ReviewerSimulator()
        self.analyzer = self.RejectAnalyzer()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_goal_refiner_output_is_dict(self):
        """Goal Refiner returns a dict with expected keys."""
        result = self.refiner.refine(SAMPLE_DESCRIPTION)
        self.assertIsInstance(result, dict)
        for key in ["persona", "problem", "solution", "outcome"]:
            self.assertIn(key, result)
        # Verify all values are strings (JSON serializable)
        for value in result.values():
            self.assertIsInstance(value, str)

    def test_outcome_mapper_output_is_dict(self):
        """Outcome Mapper returns dict with list of dicts."""
        result = self.mapper.map_features(["AI Workflow", "CI/CD"])
        self.assertIsInstance(result, dict)
        self.assertIn("features", result)
        self.assertIsInstance(result["features"], list)
        for item in result["features"]:
            self.assertIsInstance(item, dict)
            for key in ["feature", "capability", "outcome"]:
                self.assertIn(key, item)

    def test_readme_refactor_output_is_string(self):
        """README Refactor returns a string (Markdown)."""
        goal = self.refiner.refine(SAMPLE_DESCRIPTION)
        result = self.refactor.refactor(SAMPLE_README, goal_info=goal)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 100)

    def test_submission_builder_output_is_serializable(self):
        """Submission Builder returns a JSON-serializable dict."""
        result = self.builder.build({
            "name": "Serialization Test",
            "version": "1.0.0",
        })
        self.assertIsInstance(result, dict)
        # Verify JSON serializable
        serialized = json.dumps(result)
        deserialized = json.loads(serialized)
        self.assertEqual(deserialized["status"], result["status"])
        self.assertEqual(deserialized["components"], result["components"])

    def test_reviewer_simulator_output_is_serializable(self):
        """Reviewer Simulator returns JSON-serializable dicts."""
        project = {
            "tech_stack": "Python",
            "architecture": "MVC",
            "test_coverage": 80,
        }
        for review_type in ["technical", "investment", "product", "opensource"]:
            result = self.simulator.simulate(review_type, project)
            self.assertIsInstance(result, dict)
            serialized = json.dumps(result)
            deserialized = json.loads(serialized)
            self.assertIn("pass_probability", deserialized)

    def test_reject_analyzer_output_is_serializable(self):
        """Reject Analyzer returns JSON-serializable dict."""
        result = self.analyzer.analyze("表达太底层，看不出用户价值")
        self.assertIsInstance(result, dict)
        serialized = json.dumps(result, ensure_ascii=False)
        deserialized = json.loads(serialized)
        self.assertIn("real_issue", deserialized)
        self.assertIn("fixable_items", deserialized)

    def test_full_pipeline_final_output_structure(self):
        """Final pipeline output has a valid overall structure."""
        goal = self.refiner.refine(SAMPLE_DESCRIPTION)
        mapped = self.mapper.map_features(["CI/CD", "自动测试"])
        refactored = self.refactor.refactor(SAMPLE_README, goal_info=goal)
        bundle = self.builder.build({
            "name": "Final Pipeline",
            "version": "1.0.0",
            "description": goal["solution"],
            "features": [f["capability"] for f in mapped["features"]],
        })

        # Build a combined pipeline output
        pipeline_output = {
            "stage_1_goal_refiner": goal,
            "stage_2_outcome_mapper": mapped,
            "stage_3_readme_refactor_length": len(refactored),
            "stage_4_submission_builder": bundle,
        }

        # Verify the entire structure is JSON serializable
        serialized = json.dumps(pipeline_output, ensure_ascii=False)
        deserialized = json.loads(serialized)
        self.assertEqual(
            deserialized["stage_1_goal_refiner"]["persona"],
            goal["persona"],
        )
        self.assertEqual(
            deserialized["stage_4_submission_builder"]["status"],
            "complete",
        )


if __name__ == "__main__":
    unittest.main()
