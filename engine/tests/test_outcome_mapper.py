"""Tests for Outcome Mapper engine."""

import sys
import os
import pytest
import importlib.util

# Add engine directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load_outcome_mapper():
    """Load OutcomeMapper module from file path."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base, "core", "02_value_mapper", "outcome_mapper.py")
    spec = importlib.util.spec_from_file_location("outcome_mapper", file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.OutcomeMapper


@pytest.fixture
def mapper():
    return _load_outcome_mapper()()


class TestExactMatch:
    """Test exact match conversion."""

    def test_multi_model_scheduling(self, mapper):
        result = mapper.map_feature("多模型调度")
        assert result["feature"] == "多模型调度"
        assert result["capability"] == "智能资源分配"
        assert result["outcome"] == "减少重复配置"

    def test_ai_workflow(self, mapper):
        result = mapper.map_feature("AI Workflow")
        assert result["capability"] == "交付自动化平台"
        assert result["outcome"] == "交付周期缩短60%"

    def test_auto_test(self, mapper):
        result = mapper.map_feature("自动测试")
        assert result["capability"] == "质量保障自动化"
        assert result["outcome"] == "回归成本降低60%"


class TestFuzzyMatch:
    """Test fuzzy match conversion."""

    def test_partial_match_contains_keyword(self, mapper):
        result = mapper.map_feature("支持多模型调度功能")
        assert result["capability"] == "智能资源分配"
        assert result["outcome"] == "减少重复配置"

    def test_case_insensitive_match(self, mapper):
        result = mapper.map_feature("ai workflow")
        assert result["capability"] == "交付自动化平台"

    def test_fuzzy_rag_match(self, mapper):
        result = mapper.map_feature("基于RAG的知识库")
        assert result["capability"] == "知识增强"


class TestGenericFallback:
    """Test generic fallback for unknown features."""

    def test_unknown_feature(self, mapper):
        result = mapper.map_feature("实时数据同步")
        assert result["feature"] == "实时数据同步"
        assert "让用户" in result["capability"]
        assert "提升" in result["outcome"]

    def test_empty_input(self, mapper):
        result = mapper.map_feature("")
        assert result["feature"] == ""
        assert result["capability"] == "未明确"
        assert result["outcome"] == "未明确"

    def test_whitespace_only(self, mapper):
        result = mapper.map_feature("   ")
        assert result["capability"] == "未明确"


class TestMultiFeature:
    """Test multi-feature input."""

    def test_multiple_features(self, mapper):
        features = ["AI Workflow", "自动测试", "CI/CD"]
        result = mapper.map_features(features)
        assert "features" in result
        assert len(result["features"]) == 3
        assert result["features"][0]["capability"] == "交付自动化平台"
        assert result["features"][1]["capability"] == "质量保障自动化"
        assert result["features"][2]["capability"] == "交付流水线"

    def test_empty_list(self, mapper):
        result = mapper.map_features([])
        assert result["features"] == []

    def test_mixed_known_and_unknown(self, mapper):
        features = ["多模型调度", "自定义未知功能"]
        result = mapper.map_features(features)
        assert len(result["features"]) == 2
        assert result["features"][0]["capability"] == "智能资源分配"
        assert "让用户" in result["features"][1]["capability"]


class TestOutputFormat:
    """Test output format matches expected schema."""

    def test_single_feature_keys(self, mapper):
        result = mapper.map_feature("CI/CD")
        assert set(result.keys()) == {"feature", "capability", "outcome"}
        assert all(isinstance(v, str) for v in result.values())

    def test_multiple_features_schema(self, mapper):
        result = mapper.map_features(["RAG", "Agent协作"])
        assert set(result.keys()) == {"features"}
        for item in result["features"]:
            assert set(item.keys()) == {"feature", "capability", "outcome"}

    def test_all_known_categories_covered(self, mapper):
        OM = _load_outcome_mapper()
        for rule in OM.CONVERSION_RULES:
            result = mapper.map_feature(rule["feature"])
            assert result["capability"] == rule["capability"]
            assert result["outcome"] == rule["outcome"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
