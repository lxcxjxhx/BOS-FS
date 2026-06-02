"""Tests for Configurable Reviewer Simulator.

Tests ReviewerSimulator with default config (backward compatible),
custom config, custom weights, thresholds, adversarial review,
and anti-sycophancy with custom thresholds.
"""

import sys
import os
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def _load_reviewer_simulator():
    base = os.path.join(os.path.dirname(__file__), "..", "core", "06_review_simulator", "reviewer_simulator.py")
    import importlib.util
    spec = importlib.util.spec_from_file_location("reviewer_simulator", base)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ReviewerSimulator


@pytest.fixture
def ReviewerSimulator():
    return _load_reviewer_simulator()


@pytest.fixture
def default_simulator(ReviewerSimulator):
    return ReviewerSimulator()


@pytest.fixture
def custom_config_dir(tmp_path):
    config_dir = tmp_path / "reviewer_config"
    config_dir.mkdir()

    reviewer_rules = {
        "review_types": {
            "technical": {
                "dimensions": {
                    "架构设计": {"weight": 30, "max": 10},
                    "技术栈": {"weight": 25, "max": 10},
                    "代码质量": {"weight": 20, "max": 10},
                    "安全性": {"weight": 15, "max": 10},
                    "依赖管理": {"weight": 10, "max": 10},
                }
            },
            "investment": {
                "dimensions": {
                    "市场规模": {"weight": 30, "max": 10},
                    "ROI估算": {"weight": 30, "max": 10},
                    "竞品分析": {"weight": 20, "max": 10},
                    "预算规划": {"weight": 10, "max": 10},
                    "时间线": {"weight": 10, "max": 10},
                }
            },
            "product": {
                "dimensions": {
                    "用户画像": {"weight": 20, "max": 10},
                    "价值主张": {"weight": 30, "max": 10},
                    "MVP范围": {"weight": 20, "max": 10},
                    "成功指标": {"weight": 15, "max": 10},
                    "反馈机制": {"weight": 15, "max": 10},
                }
            },
            "opensource": {
                "dimensions": {
                    "开源许可证": {"weight": 35, "max": 10},
                    "文档完整度": {"weight": 20, "max": 10},
                    "贡献指引": {"weight": 20, "max": 10},
                    "行为准则": {"weight": 10, "max": 10},
                    "第三方合规": {"weight": 15, "max": 10},
                }
            },
        },
        "thresholds": {
            "test_coverage": {"excellent": 90, "good": 70, "poor": 40},
            "text_length": {"detailed": 60, "moderate": 40, "brief": 25},
            "dependency_count": {"optimal": 8, "max_acceptable": 15},
        },
    }
    (config_dir / "reviewer_rules.json").write_text(
        json.dumps(reviewer_rules, ensure_ascii=False), encoding="utf-8"
    )

    anti_sycophancy = {
        "layer1_lexical": {
            "empty_praise_words": ["优秀", "完美", "出色"],
            "trust_penalty": 3,
        },
        "layer2_structural": {
            "trigger_keywords": ["未明确", "推断"],
        },
        "layer3_score": {
            "high_score_threshold": 8,
            "variance_threshold": 0.3,
            "fallback_score": 5.5,
            "evidence_coverage_min_len": 25,
        },
        "layer4_pattern": {
            "security_score_threshold": 6,
            "force_reduce_score": 3.5,
            "required_fields": ["security_design", "security_review"],
        },
    }
    (config_dir / "anti_sycophancy.json").write_text(
        json.dumps(anti_sycophancy, ensure_ascii=False), encoding="utf-8"
    )

    adversarial_rules = {
        "base_score": 30,
        "ceiling": 70,
        "floor": 5,
        "pass_probability_cap_with_kill_factors": 0.15,
    }
    (config_dir / "adversarial_rules.json").write_text(
        json.dumps(adversarial_rules), encoding="utf-8"
    )

    return str(config_dir)


@pytest.fixture
def custom_simulator(ReviewerSimulator, custom_config_dir):
    return ReviewerSimulator(config_path=custom_config_dir)


@pytest.fixture
def complete_project():
    return {
        "tech_stack": "Python 3.11, FastAPI, PostgreSQL, React, Docker",
        "architecture": "微服务架构，前后端分离，API Gateway + 微服务集群，采用事件驱动架构",
        "test_coverage": 85,
        "dependencies": ["fastapi", "sqlalchemy", "pytest", "httpx"],
        "security_review": True,
        "market_size": "约500亿元，年增长率15%",
        "roi_estimate": "预计18个月回本，IRR 35%，NPV 500万",
        "competitor_analysis": True,
        "budget": 2000000,
        "timeline": "6个月完成MVP，12个月全面推广",
        "user_persona": "企业内部项目经理和开发人员，50-200人规模团队",
        "value_proposition": "提升项目交付效率50%，减少沟通成本40%",
        "mvp_scope": "需求管理+代码生成+质量审查",
        "success_metrics": ["交付周期缩短50%", "Bug率降低30%", "用户满意度>4.5"],
        "feedback_mechanism": True,
        "license": "MIT",
        "documentation": True,
        "contributing_guide": True,
        "code_of_conduct": True,
        "third_party_licenses": ["MIT", "Apache-2.0"],
    }


@pytest.fixture
def minimal_project():
    return {
        "tech_stack": "",
        "market_size": "",
        "user_persona": "",
        "license": "",
    }


class TestDefaultConfigBackwardCompatible:
    """Test ReviewerSimulator with default config (backward compatible)."""

    def test_default_init_no_config_path(self, default_simulator):
        result = default_simulator.simulate("technical", {"tech_stack": "Python", "architecture": "MVC"})
        assert "total_score" in result
        assert "dimension_scores" in result

    def test_default_config_returns_expected_fields(self, default_simulator):
        result = default_simulator.simulate("technical", {})
        expected_keys = {
            "dimension_scores", "total_score", "pass_probability",
            "rejection_reasons", "suggestions", "sycophancy_warnings",
            "hostile_questions", "weakness_chain", "kill_factors",
        }
        assert expected_keys.issubset(set(result.keys()))

    def test_default_technical_review_runs(self, default_simulator, complete_project):
        result = default_simulator.simulate("technical", complete_project)
        assert result["total_score"] >= 0
        assert result["total_score"] <= 10

    def test_default_investment_review_runs(self, default_simulator, complete_project):
        result = default_simulator.simulate("investment", complete_project)
        assert result["total_score"] >= 0

    def test_default_product_review_runs(self, default_simulator, complete_project):
        result = default_simulator.simulate("product", complete_project)
        assert result["total_score"] >= 0

    def test_default_opensource_review_runs(self, default_simulator, complete_project):
        result = default_simulator.simulate("opensource", complete_project)
        assert result["total_score"] >= 0


class TestCustomConfigLoading:
    """Test ReviewerSimulator with custom config."""

    def test_custom_config_dir_loaded(self, custom_simulator):
        result = custom_simulator.simulate("technical", {"tech_stack": "Python", "architecture": "MVC pattern"})
        assert "dimension_scores" in result
        assert "架构设计" in result["dimension_scores"]

    def test_custom_weights_applied_to_technical(self, custom_simulator):
        result = custom_simulator.simulate("technical", {"tech_stack": "Python", "architecture": "MVC pattern"})
        dimensions = result["dimension_scores"]
        assert "架构设计" in dimensions
        assert "技术栈" in dimensions
        assert "代码质量" in dimensions
        assert "安全性" in dimensions
        assert "依赖管理" in dimensions
        total_weight = sum(d["weight"] for d in dimensions.values())
        assert total_weight == 100

    def test_custom_weights_applied_to_investment(self, custom_simulator):
        result = custom_simulator.simulate("investment", {"market_size": "100亿", "roi_estimate": "18个月回本"})
        dimensions = result["dimension_scores"]
        assert "市场规模" in dimensions
        assert "ROI估算" in dimensions
        total_weight = sum(d["weight"] for d in dimensions.values())
        assert total_weight == 100

    def test_custom_weights_applied_to_product(self, custom_simulator):
        result = custom_simulator.simulate("product", {"user_persona": "开发者", "value_proposition": "提升效率"})
        dimensions = result["dimension_scores"]
        assert "用户画像" in dimensions
        assert "价值主张" in dimensions
        total_weight = sum(d["weight"] for d in dimensions.values())
        assert total_weight == 100

    def test_custom_weights_applied_to_opensource(self, custom_simulator):
        result = custom_simulator.simulate("opensource", {"license": "MIT", "documentation": True})
        dimensions = result["dimension_scores"]
        assert "开源许可证" in dimensions
        assert "文档完整度" in dimensions
        total_weight = sum(d["weight"] for d in dimensions.values())
        assert total_weight == 100

    def test_custom_thresholds_applied(self, custom_simulator):
        custom_simulator.config.reload()
        tc = custom_simulator.config.get("reviewer_rules.thresholds.test_coverage")
        assert tc["excellent"] == 90
        assert tc["good"] == 70
        assert tc["poor"] == 40

    def test_custom_text_length_thresholds(self, custom_simulator):
        custom_simulator.config.reload()
        tl = custom_simulator.config.get("reviewer_rules.thresholds.text_length")
        assert tl["detailed"] == 60
        assert tl["moderate"] == 40
        assert tl["brief"] == 25


class TestCustomWeightsApplied:
    """Test custom weights applied correctly."""

    def test_higher_weight_dimension_has_more_impact(self, custom_simulator):
        project_high_arch = {
            "tech_stack": "Python 3.11, FastAPI, PostgreSQL, React",
            "architecture": "微服务架构，前后端分离，API Gateway + 微服务集群，采用事件驱动架构，包含服务网格",
            "test_coverage": 50,
            "security_review": False,
        }
        project_low_arch = {
            "tech_stack": "Python 3.11, FastAPI, PostgreSQL, React",
            "architecture": "",
            "test_coverage": 95,
            "security_review": True,
        }
        result_high = custom_simulator.simulate("technical", project_high_arch)
        result_low = custom_simulator.simulate("technical", project_low_arch)
        assert result_high["dimension_scores"]["架构设计"]["score"] > result_low["dimension_scores"]["架构设计"]["score"]

    def test_total_score_reflects_custom_weights(self, custom_simulator, complete_project):
        result = custom_simulator.simulate("technical", complete_project)
        dims = result["dimension_scores"]
        total_weight = sum(d["weight"] for d in dims.values())
        assert total_weight == 100


class TestCustomThresholdsApplied:
    """Test custom thresholds applied correctly."""

    def test_higher_coverage_threshold_lower_score(self, custom_simulator):
        project = {
            "tech_stack": "Python",
            "architecture": "MVC architecture pattern with layers and modules",
            "test_coverage": 75,
            "security_review": True,
            "dependencies": ["fastapi"],
        }
        result = custom_simulator.simulate("technical", project)
        quality_score = result["dimension_scores"]["代码质量"]["score"]
        assert quality_score <= 7.0

    def test_stricter_dependency_threshold(self, custom_simulator):
        project = {
            "tech_stack": "Python",
            "architecture": "MVC architecture pattern with layers and modules",
            "test_coverage": 95,
            "security_review": True,
            "dependencies": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
        }
        result = custom_simulator.simulate("technical", project)
        dep_score = result["dimension_scores"]["依赖管理"]["score"]
        assert dep_score <= 7.0

    def test_longer_text_required_for_high_score(self, custom_simulator):
        short_arch = "简单架构"
        long_arch = "微服务架构，前后端分离，API Gateway + 微服务集群，采用事件驱动架构，包含服务网格和消息队列"
        project_short = {
            "tech_stack": "Python 3.11, FastAPI, PostgreSQL",
            "architecture": short_arch,
            "test_coverage": 90,
            "security_review": True,
            "dependencies": ["fastapi"],
        }
        project_long = {
            "tech_stack": "Python 3.11, FastAPI, PostgreSQL",
            "architecture": long_arch,
            "test_coverage": 90,
            "security_review": True,
            "dependencies": ["fastapi"],
        }
        result_short = custom_simulator.simulate("technical", project_short)
        result_long = custom_simulator.simulate("technical", project_long)
        assert result_long["dimension_scores"]["架构设计"]["score"] >= result_short["dimension_scores"]["架构设计"]["score"]


class TestAdversarialReviewWithCustomRules:
    """Test adversarial review with custom rules."""

    def test_adversarial_review_with_custom_ceiling(self, custom_simulator):
        project = {
            "architecture": "完整的微服务架构图，包含安全设计",
            "security_review": True,
            "competitor_analysis": True,
            "team_background": "核心团队10年经验",
            "cost_estimate": "500万",
            "exit_strategy": "灰度下线方案",
            "user_persona": "企业开发者",
            "success_metrics": ["DAU 10万"],
        }
        result = custom_simulator.simulate("adversarial", project)
        assert result["total_score"] <= 7.0

    def test_adversarial_returns_hostile_questions(self, custom_simulator):
        project = {"security_review": False, "competitor_analysis": False, "architecture": ""}
        result = custom_simulator.simulate("adversarial", project)
        assert len(result["hostile_questions"]) >= 5

    def test_adversarial_returns_weakness_chain(self, custom_simulator):
        project = {"security_review": False, "competitor_analysis": False}
        result = custom_simulator.simulate("adversarial", project)
        assert len(result["weakness_chain"]) >= 1
        for chain in result["weakness_chain"]:
            assert "original_defect" in chain
            assert "layer1_inferred" in chain
            assert "layer2_inferred" in chain

    def test_adversarial_returns_kill_factors(self, custom_simulator):
        project = {"security_review": False, "architecture": "", "competitor_analysis": False}
        result = custom_simulator.simulate("adversarial", project)
        assert len(result["kill_factors"]) >= 1

    def test_adversarial_multiple_kill_factors_cap_probability(self, custom_simulator):
        project = {"architecture": "", "security_review": False, "competitor_analysis": False, "user_persona": ""}
        result = custom_simulator.simulate("adversarial", project)
        if len(result["kill_factors"]) >= 2:
            assert result["pass_probability"] <= 0.15


class TestAntiSycophancyWithCustomThresholds:
    """Test anti-sycophancy with custom thresholds."""

    def test_custom_empty_praise_words_detected(self, custom_simulator):
        project = {
            "tech_stack": "Python 优秀",
            "architecture": "MVC pattern",
            "test_coverage": 85,
            "security_review": True,
        }
        result = custom_simulator.simulate("technical", project)
        assert len(result["sycophancy_warnings"]) >= 1

    def test_custom_trust_penalty_applied(self, custom_simulator):
        custom_simulator.config.reload()
        penalty = custom_simulator.config.get("anti_sycophancy.layer1_lexical.trust_penalty")
        assert penalty == 3

    def test_custom_high_score_threshold(self, custom_simulator):
        custom_simulator.config.reload()
        threshold = custom_simulator.config.get("anti_sycophancy.layer3_score.high_score_threshold")
        assert threshold == 8

    def test_custom_variance_threshold(self, custom_simulator):
        custom_simulator.config.reload()
        variance = custom_simulator.config.get("anti_sycophancy.layer3_score.variance_threshold")
        assert variance == 0.3

    def test_custom_security_threshold_enforced(self, custom_simulator):
        custom_simulator.config.reload()
        sec_threshold = custom_simulator.config.get("anti_sycophancy.layer4_pattern.security_score_threshold")
        assert sec_threshold == 6

    def test_perfect_project_no_warnings_with_custom_config(self, custom_simulator, complete_project):
        result = custom_simulator.simulate("technical", complete_project)
        assert not any("[抗讨好]" in s or "[非线性惩罚]" in s for s in result["suggestions"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
