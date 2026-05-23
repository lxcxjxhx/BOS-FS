"""Tests for Reject Analyzer engine."""

import sys
import os
import pytest
import importlib.util

# Add engine directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load_reject_analyzer():
    """Load RejectAnalyzer module from file path."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base, "core", "05_artifact_generator", "reject_analyzer.py")
    spec = importlib.util.spec_from_file_location("reject_analyzer", file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.RejectAnalyzer


@pytest.fixture
def analyzer():
    return _load_reject_analyzer()()


# ── 10 rejection pattern test data ──

REJECTION_CASES = [
    ("表达太底层", "技术实现描述太底层，看不出用户价值", "表达太底层"),
    ("目标不明确", "不清楚这个项目要解决什么问题，目标不明确", "目标不明确"),
    ("差异化不足", "又一个同类AI工具，没看出与竞品有什么差异和独特优势", "差异化不足"),
    ("文档不完整", "缺少安装说明和README文档，交付物不全", "文档不完整"),
    ("安全风险", "未说明数据安全和隐私保护措施，存在安全风险", "安全风险"),
    ("价值模糊", "看不出项目相比现有方案的优势和量化收益", "价值模糊"),
    ("场景缺失", "不知道这个项目在什么真实场景下使用，缺少用户故事", "场景缺失"),
    ("路线图不清", "规划不清晰，没有明确的执行路径和里程碑", "路线图不清"),
    ("技术可行性", "方案过于复杂，与要解决的问题不匹配，缺乏技术可行性验证", "技术可行性"),
    ("合规问题", "许可证不明确，缺少合规声明和开源授权信息", "合规问题"),
]


class TestRejectionPatternMatching:
    """Test 10 rejection pattern matching."""

    @pytest.mark.parametrize("desc,input_text,expected_pattern", REJECTION_CASES)
    def test_pattern_match(self, analyzer, desc, input_text, expected_pattern):
        result = analyzer.analyze(input_text)
        assert result["matched_pattern"] == expected_pattern, f"Failed for: {desc}"

    def test_all_patterns_have_keywords(self, analyzer):
        RA = _load_reject_analyzer()
        for pattern in RA.REJECTION_PATTERNS:
            assert len(pattern["keywords"]) > 0
            assert "name" in pattern
            assert "real_issue" in pattern
            assert "fixable_items" in pattern
            assert "suggestion" in pattern


class TestConfidenceScore:
    """Test confidence score range (0.0-1.0)."""

    def test_confidence_within_range(self, analyzer):
        for _, input_text, _ in REJECTION_CASES:
            result = analyzer.analyze(input_text)
            assert 0.0 <= result["confidence"] <= 1.0

    def test_empty_input_zero_confidence(self, analyzer):
        result = analyzer.analyze("")
        assert result["confidence"] == 0.0

    def test_high_keyword_overlap_high_confidence(self, analyzer):
        text = "技术实现描述太底层，技术工具用技术语言，看不出用户价值，功能feature实现"
        result = analyzer.analyze(text)
        assert result["confidence"] > 0.3

    def test_no_match_low_confidence(self, analyzer):
        text = "这是一段完全不相关的文本"
        result = analyzer.analyze(text)
        assert result["confidence"] <= 0.3


class TestEmptyInputHandling:
    """Test empty input handling."""

    def test_empty_string(self, analyzer):
        result = analyzer.analyze("")
        assert result["matched_pattern"] == "无"
        assert result["confidence"] == 0.0
        assert "输入为空" in result["real_issue"]

    def test_whitespace_only(self, analyzer):
        result = analyzer.analyze("   ")
        assert result["matched_pattern"] == "无"
        assert result["confidence"] == 0.0

    def test_empty_fixable_items(self, analyzer):
        result = analyzer.analyze("")
        assert len(result["fixable_items"]) > 0
        assert isinstance(result["checklist_results"], dict)


class TestOutputFormat:
    """Test output format contains all required keys."""

    def test_all_required_keys_present(self, analyzer):
        result = analyzer.analyze("技术实现太底层，看不出用户价值")
        expected_keys = {
            "real_issue",
            "fixable_items",
            "resubmit_suggestion",
            "matched_pattern",
            "confidence",
            "checklist_results",
        }
        assert set(result.keys()) == expected_keys

    def test_fixable_items_is_list(self, analyzer):
        result = analyzer.analyze("缺少安装说明和使用文档")
        assert isinstance(result["fixable_items"], list)
        assert len(result["fixable_items"]) > 0

    def test_checklist_results_is_dict_of_bools(self, analyzer):
        result = analyzer.analyze("技术太底层")
        assert isinstance(result["checklist_results"], dict)
        for key, value in result["checklist_results"].items():
            assert isinstance(value, bool)

    def test_resubmit_suggestion_is_string(self, analyzer):
        result = analyzer.analyze("技术太底层")
        assert isinstance(result["resubmit_suggestion"], str)
        assert len(result["resubmit_suggestion"]) > 0


class TestHighConfidenceScenario:
    """Test high-confidence match scenario."""

    def test_pattern_name_in_text_boosts_confidence(self, analyzer):
        text = "表达太底层：技术实现描述太底层，看不出用户价值"
        result = analyzer.analyze(text)
        assert result["confidence"] >= 0.3

    def test_multiple_keywords_boost_confidence(self, analyzer):
        text = "文档不完整：缺少安装说明、README和Demo指南，交付物不全"
        result = analyzer.analyze(text)
        assert result["matched_pattern"] == "文档不完整"
        assert result["confidence"] > 0.3

    def test_exact_match_real_issue(self, analyzer):
        text = "技术实现描述太底层，看不出用户价值"
        result = analyzer.analyze(text)
        assert result["real_issue"] != ""
        assert "价值" in result["real_issue"]

    def test_high_confidence_has_fixable_items(self, analyzer):
        text = "缺少安装说明和使用文档，交付物不全"
        result = analyzer.analyze(text)
        assert len(result["fixable_items"]) >= 3
        assert isinstance(result["resubmit_suggestion"], str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
