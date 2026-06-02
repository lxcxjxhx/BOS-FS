"""Tests for delivery scenario and ROI framework document loading."""

import unittest
import os
import sys

# Add engine directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CASE_DIR = os.path.join(PROJECT_ROOT, "examples", "real-cases")
DELIVERY_SCENARIOS = os.path.join(PROJECT_ROOT, "knowledge", "adoption", "delivery_scenarios.md")
ROI_FRAMEWORK = os.path.join(PROJECT_ROOT, "knowledge", "adoption", "roi_framework.md")
GUIDE_DIR = os.path.join(PROJECT_ROOT, "guides")


def _load_file(file_path: str) -> str:
    """Load a file and return its content."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


class TestDeliveryScenarios(unittest.TestCase):
    """Test that delivery_scenarios.md can be loaded and contains required content."""

    def test_delivery_scenarios_exists(self):
        """delivery_scenarios.md file exists."""
        self.assertTrue(os.path.isfile(DELIVERY_SCENARIOS), f"File not found: {DELIVERY_SCENARIOS}")

    def test_delivery_scenarios_loadable(self):
        """delivery_scenarios.md can be loaded without errors."""
        content = _load_file(DELIVERY_SCENARIOS)
        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 100)

    def test_delivery_scenarios_has_five_scenarios(self):
        """delivery_scenarios.md contains at least 5 scenario sections."""
        content = _load_file(DELIVERY_SCENARIOS)
        scenario_count = content.count("## 场景 ")
        self.assertGreaterEqual(scenario_count, 5, f"Expected >= 5 scenarios, found {scenario_count}")

    def test_delivery_scenarios_has_core_sections(self):
        """delivery_scenarios.md has key structural sections."""
        content = _load_file(DELIVERY_SCENARIOS)
        self.assertIn("场景概览", content)
        self.assertIn("渗透测试服务交付", content)
        self.assertIn("代码审计服务交付", content)

    def test_delivery_scenarios_contains_efficiency_data(self):
        """delivery_scenarios.md contains efficiency improvement data."""
        content = _load_file(DELIVERY_SCENARIOS)
        self.assertIn("效率指标", content)
        self.assertIn("传统方式", content)
        self.assertIn("BOS-FS", content)


class TestROIFramework(unittest.TestCase):
    """Test that roi_framework.md can be loaded and contains required content."""

    def test_roi_framework_exists(self):
        """roi_framework.md file exists."""
        self.assertTrue(os.path.isfile(ROI_FRAMEWORK), f"File not found: {ROI_FRAMEWORK}")

    def test_roi_framework_loadable(self):
        """roi_framework.md can be loaded without errors."""
        content = _load_file(ROI_FRAMEWORK)
        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 200)

    def test_roi_framework_has_required_sections(self):
        """roi_framework.md has all required structural sections."""
        content = _load_file(ROI_FRAMEWORK)
        required = [
            "人工基线测量方法",
            "ROI 计算公式",
            "输出质量评估指标",
            "人员要求降低程度",
            "实际案例数据",
        ]
        for section in required:
            self.assertIn(section, content, f"Missing section: {section}")

    def test_roi_framework_has_formulas(self):
        """roi_framework.md contains ROI calculation formulas."""
        content = _load_file(ROI_FRAMEWORK)
        self.assertIn("T_manual", content)
        self.assertIn("T_tool", content)
        self.assertIn("ROI", content)


class TestRealCaseFiles(unittest.TestCase):
    """Test that all 3 real case files can be loaded."""

    EXPECTED_CASES = [
        "case-01-penetration-test.md",
        "case-02-code-audit.md",
        "case-03-vulnerability-ledger.md",
    ]

    REQUIRED_SECTIONS = [
        "场景描述",
        "输入数据",
        "处理流程",
        "输出交付物",
        "提效数据",
        "质量对比",
        "使用技能",
    ]

    def test_all_case_files_exist(self):
        """All 3 case files exist in examples/real-cases/."""
        for fname in self.EXPECTED_CASES:
            fpath = os.path.join(CASE_DIR, fname)
            self.assertTrue(os.path.isfile(fpath), f"Case file not found: {fpath}")

    def test_all_case_files_loadable(self):
        """All case files can be loaded without errors."""
        for fname in self.EXPECTED_CASES:
            with self.subTest(case=fname):
                fpath = os.path.join(CASE_DIR, fname)
                content = _load_file(fpath)
                self.assertGreater(len(content), 100)

    def test_case_01_has_required_sections(self):
        """case-01-penetration-test.md has all required sections."""
        content = _load_file(os.path.join(CASE_DIR, "case-01-penetration-test.md"))
        for section in self.REQUIRED_SECTIONS:
            self.assertIn(section, content, f"case-01 missing section: {section}")

    def test_case_02_has_required_sections(self):
        """case-02-code-audit.md has all required sections."""
        content = _load_file(os.path.join(CASE_DIR, "case-02-code-audit.md"))
        for section in self.REQUIRED_SECTIONS:
            self.assertIn(section, content, f"case-02 missing section: {section}")

    def test_case_03_has_required_sections(self):
        """case-03-vulnerability-ledger.md has all required sections."""
        content = _load_file(os.path.join(CASE_DIR, "case-03-vulnerability-ledger.md"))
        for section in self.REQUIRED_SECTIONS:
            self.assertIn(section, content, f"case-03 missing section: {section}")

    def test_case_files_contain_pipeline_reference(self):
        """All case files reference BOS-FS pipeline."""
        for fname in self.EXPECTED_CASES:
            with self.subTest(case=fname):
                content = _load_file(os.path.join(CASE_DIR, fname))
                self.assertIn("BOS-FS", content, f"{fname} should reference BOS-FS")

    def test_case_files_contain_efficiency_data(self):
        """All case files contain efficiency/ROI data."""
        for fname in self.EXPECTED_CASES:
            with self.subTest(case=fname):
                content = _load_file(os.path.join(CASE_DIR, fname))
                self.assertIn("提效", content, f"{fname} should contain efficiency data")


class TestGuideFiles(unittest.TestCase):
    """Test that guide files exist in guides/ directory."""

    def test_guides_directory_exists(self):
        """guides/ directory exists."""
        self.assertTrue(os.path.isdir(GUIDE_DIR), f"Directory not found: {GUIDE_DIR}")

    def test_guide_files_exist(self):
        """At least one guide file exists in guides/."""
        guide_files = [f for f in os.listdir(GUIDE_DIR) if f.endswith(".md")]
        self.assertGreater(len(guide_files), 0, "No .md files found in guides/ directory")

    def test_skill_usage_guide_exists(self):
        """skill_usage.md or cheatsheet.md exists in guides/."""
        candidates = ["skill_usage.md", "cheatsheet.md", "quickstart.md"]
        found = [f for f in candidates if os.path.isfile(os.path.join(GUIDE_DIR, f))]
        self.assertGreater(len(found), 0, f"No guide files found among {candidates}")


if __name__ == "__main__":
    unittest.main()
