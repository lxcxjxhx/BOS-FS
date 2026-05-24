"""Tests for GoalRefiner module."""

import unittest
import os
import sys
import importlib.util

# Add engine directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def _load_goal_refiner():
    """Load GoalRefiner module from file path."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base, "core", "01_intent_parser", "goal_refiner.py")
    spec = importlib.util.spec_from_file_location("goal_refiner", file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.GoalRefiner


class TestGoalRefiner(unittest.TestCase):
    def setUp(self):
        GoalRefiner = _load_goal_refiner()
        self.refiner = GoalRefiner()

    def test_extract_persona(self):
        desc = "作为企业内部研发团队，我们需要提高效率。"
        result = self.refiner.refine(desc)
        self.assertEqual(result["persona"], "企业内部研发团队")

    def test_extract_problem(self):
        desc = "痛点：现有流程缺乏标准化，沟通成本高。"
        result = self.refiner.refine(desc)
        self.assertEqual(result["problem"], "现有流程缺乏标准化，沟通成本高")

    def test_extract_solution(self):
        desc = "方案：开发一套自动化项目交付管理系统。"
        result = self.refiner.refine(desc)
        self.assertIn("自动化", result["solution"])

    def test_extract_outcome(self):
        desc = "目标：提升交付效率50%。"
        result = self.refiner.refine(desc)
        self.assertIn("50%", result["outcome"])

    def test_full_description(self):
        desc = """
        作为企业内部研发团队，我们希望解决当前项目交付效率低下的问题。
        痛点：现有流程缺乏标准化，沟通成本高，交付质量不稳定。
        方案：开发一套自动化项目交付管理系统。
        目标：提升交付效率50%，降低人工成本30%。
        """
        result = self.refiner.refine(desc)
        self.assertIsNotNone(result["persona"])
        self.assertIsNotNone(result["problem"])
        self.assertIsNotNone(result["solution"])
        self.assertIsNotNone(result["outcome"])

    def test_empty_description(self):
        result = self.refiner.refine("")
        self.assertEqual(result["persona"], "")
        self.assertEqual(result["problem"], "")
        self.assertEqual(result["solution"], "")
        self.assertEqual(result["outcome"], "")


if __name__ == "__main__":
    unittest.main()
