"""Tests for 8-scenario expansion verification.

验证 BOS-FS 从 5 类安全交付扩展为 8 类通用交付的完整性。
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CASE_DIR = os.path.join(PROJECT_ROOT, "examples", "real-cases")
DELIVERY_SCENARIOS = os.path.join(PROJECT_ROOT, "knowledge", "adoption", "delivery_scenarios.md")
README_PATH = os.path.join(PROJECT_ROOT, "README.md")
GUIDE_DIR = os.path.join(PROJECT_ROOT, "guides")
DELIVERY_USAGE = os.path.join(GUIDE_DIR, "delivery_usage.md")


def _load(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# 1. TestDeliveryScenariosExpansion - 验证 delivery_scenarios.md 包含 8 类场景
# ---------------------------------------------------------------------------


class TestDeliveryScenariosExpansion(unittest.TestCase):
    """验证 delivery_scenarios.md 包含 8 类场景的完整定义。"""

    def test_delivery_scenarios_exists(self):
        """delivery_scenarios.md 文件存在。"""
        self.assertTrue(os.path.isfile(DELIVERY_SCENARIOS), f"File not found: {DELIVERY_SCENARIOS}")

    def test_contains_product_positioning(self):
        """包含"产品交付辅助 Skill"定位描述。"""
        content = _load(DELIVERY_SCENARIOS)
        self.assertIn("产品交付辅助 Skill", content)

    def test_contains_8_scenarios(self):
        """包含 8 个场景标题。"""
        content = _load(DELIVERY_SCENARIOS)
        count = content.count("## 场景 ")
        self.assertEqual(count, 8, f"Expected 8 scenarios, found {count}")

    def test_scenario_1_software_product(self):
        """场景1: 软件产品交付存在。"""
        content = _load(DELIVERY_SCENARIOS)
        self.assertIn("软件产品交付", content)

    def test_scenario_2_tech_docs(self):
        """场景2: 技术文档交付存在。"""
        content = _load(DELIVERY_SCENARIOS)
        self.assertIn("技术文档交付", content)

    def test_scenario_3_opensource(self):
        """场景3: 开源项目交付存在。"""
        content = _load(DELIVERY_SCENARIOS)
        self.assertIn("开源项目交付", content)

    def test_scenario_4_security(self):
        """场景4: 安全服务交付存在。"""
        content = _load(DELIVERY_SCENARIOS)
        self.assertIn("安全服务交付", content)

    def test_scenario_5_consulting(self):
        """场景5: 咨询报告交付存在。"""
        content = _load(DELIVERY_SCENARIOS)
        self.assertIn("咨询报告交付", content)

    def test_scenario_6_review_materials(self):
        """场景6: 项目评审材料存在。"""
        content = _load(DELIVERY_SCENARIOS)
        self.assertIn("项目评审材料", content)

    def test_scenario_7_data_processing(self):
        """场景7: 数据处理脚本交付存在。"""
        content = _load(DELIVERY_SCENARIOS)
        self.assertIn("数据处理脚本交付", content)

    def test_scenario_8_knowledge(self):
        """场景8: 团队知识沉淀存在。"""
        content = _load(DELIVERY_SCENARIOS)
        self.assertIn("团队知识沉淀", content)

    def test_scenario_has_input_output(self):
        """每个场景包含输入输出说明。"""
        content = _load(DELIVERY_SCENARIOS)
        self.assertGreaterEqual(content.count("输入"), 8)
        self.assertGreaterEqual(content.count("输出"), 8)

    def test_scenario_has_efficiency_metrics(self):
        """每个场景包含效率指标。"""
        content = _load(DELIVERY_SCENARIOS)
        self.assertIn("效率指标", content)

    def test_scenario_has_decision_guide(self):
        """包含决策指南。"""
        content = _load(DELIVERY_SCENARIOS)
        self.assertIn("决策指南", content)


# ---------------------------------------------------------------------------
# 2. TestRealCaseFiles - 验证 6 个真实案例文件存在
# ---------------------------------------------------------------------------


class TestRealCaseFiles(unittest.TestCase):
    """验证 6 个真实案例文件存在且包含提效数据。"""

    EXPECTED_CASES = [
        "case-01-penetration-test.md",
        "case-02-code-audit.md",
        "case-03-vulnerability-ledger.md",
        "case-04-product-delivery.md",
        "case-05-opensource-delivery.md",
        "case-06-consulting-report-delivery.md",
    ]

    def _assert_case_exists(self, fname: str):
        fpath = os.path.join(CASE_DIR, fname)
        self.assertTrue(os.path.isfile(fpath), f"Case file not found: {fpath}")

    def test_case_01_penetration(self):
        """case-01-penetration-test.md 存在。"""
        self._assert_case_exists("case-01-penetration-test.md")

    def test_case_02_code_audit(self):
        """case-02-code-audit.md 存在。"""
        self._assert_case_exists("case-02-code-audit.md")

    def test_case_03_vulnerability_ledger(self):
        """case-03-vulnerability-ledger.md 存在。"""
        self._assert_case_exists("case-03-vulnerability-ledger.md")

    def test_case_04_product_delivery(self):
        """case-04-product-delivery.md 存在。"""
        self._assert_case_exists("case-04-product-delivery.md")

    def test_case_05_opensource_delivery(self):
        """case-05-opensource-delivery.md 存在。"""
        self._assert_case_exists("case-05-opensource-delivery.md")

    def test_case_06_consulting_delivery(self):
        """case-06-consulting-report-delivery.md 存在。"""
        self._assert_case_exists("case-06-consulting-report-delivery.md")

    def test_case_has_efficiency_data(self):
        """每个案例包含提效数据。"""
        for fname in self.EXPECTED_CASES:
            with self.subTest(case=fname):
                fpath = os.path.join(CASE_DIR, fname)
                content = _load(fpath)
                self.assertIn("提效", content, f"{fname} should contain 提效 data")


# ---------------------------------------------------------------------------
# 3. TestReadmeScenarioTable - 验证 README.md 场景表更新
# ---------------------------------------------------------------------------


class TestReadmeScenarioTable(unittest.TestCase):
    """验证 README.md 场景表更新为 8 类场景。"""

    def test_readme_mentions_product_positioning(self):
        """README 包含产品交付辅助定位。"""
        content = _load(README_PATH)
        self.assertIn("产品交付辅助", content)

    def test_readme_contains_8_scenarios(self):
        """README 适用场景表包含 8 类。"""
        content = _load(README_PATH)
        scenario_markers = [
            "软件产品交付",
            "技术文档交付",
            "开源项目交付",
            "安全服务交付",
            "咨询报告交付",
            "项目评审材料",
            "数据处理脚本交付",
            "团队知识沉淀",
        ]
        found = 0
        for marker in scenario_markers:
            if marker in content:
                found += 1
        self.assertGreaterEqual(found, 8, f"README should mention >= 8 scenarios, found {found}")

    def test_readme_links_to_cases(self):
        """README 场景表链接到真实案例。"""
        content = _load(README_PATH)
        self.assertIn("examples/real-cases/case-01", content)
        self.assertIn("examples/real-cases/case-04", content)
        self.assertIn("examples/real-cases/case-05", content)
        self.assertIn("examples/real-cases/case-06", content)


# ---------------------------------------------------------------------------
# 4. TestGuideFiles - 验证指南文件
# ---------------------------------------------------------------------------


class TestGuideFiles(unittest.TestCase):
    """验证 delivery_usage.md 等指南文件包含 8 类场景。"""

    def test_delivery_usage_exists(self):
        """delivery_usage.md 文件存在。"""
        self.assertTrue(os.path.isfile(DELIVERY_USAGE), f"File not found: {DELIVERY_USAGE}")

    def test_delivery_usage_mentions_8_scenarios(self):
        """delivery_usage.md 提到 8 类场景。"""
        content = _load(DELIVERY_USAGE)
        scenario_markers = [
            "软件产品交付",
            "技术文档交付",
            "开源项目交付",
            "安全服务交付",
            "咨询报告交付",
            "项目评审材料",
            "数据处理脚本交付",
            "团队知识沉淀",
        ]
        for marker in scenario_markers:
            self.assertIn(marker, content, f"delivery_usage.md missing scenario: {marker}")

    def test_delivery_usage_mentions_product_positioning(self):
        """delivery_usage.md 包含产品交付辅助定位。"""
        content = _load(DELIVERY_USAGE)
        self.assertIn("产品交付辅助", content)


if __name__ == "__main__":
    unittest.main()
