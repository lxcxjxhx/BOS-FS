"""Tests for Reviewer Simulator engine."""

import sys
import os
import importlib.util
import pytest

_reviewer_simulator_path = os.path.join(os.path.dirname(__file__), "..", "core", "06_review_simulator", "reviewer_simulator.py")
_spec = importlib.util.spec_from_file_location("reviewer_simulator", _reviewer_simulator_path)
_reviewer_simulator_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_reviewer_simulator_module)
ReviewerSimulator = _reviewer_simulator_module.ReviewerSimulator


@pytest.fixture
def simulator():
    return ReviewerSimulator()


@pytest.fixture
def complete_project():
    return {
        "tech_stack": "Python 3.11, FastAPI, PostgreSQL, React",
        "architecture": "微服务架构，前后端分离，API Gateway + 微服务集群",
        "test_coverage": 85,
        "dependencies": ["fastapi", "sqlalchemy", "pytest"],
        "security_review": True,
        "market_size": "约500亿元",
        "roi_estimate": "预计18个月回本，IRR 35%",
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
        "third_party_licenses": ["MIT", "Apache-2.0", "BSD-3-Clause"],
    }


@pytest.fixture
def minimal_project():
    return {
        "tech_stack": "",
        "market_size": "",
        "user_persona": "",
        "license": "",
    }


class TestTechnicalReview:
    """Technical review tests."""

    def test_high_score_complete_project(self, simulator, complete_project):
        result = simulator.simulate("technical", complete_project)
        assert result["total_score"] >= 6.0
        assert result["pass_probability"] >= 0.6

    def test_low_score_minimal_project(self, simulator, minimal_project):
        result = simulator.simulate("technical", minimal_project)
        assert result["pass_probability"] < 0.5
        assert len(result["rejection_reasons"]) >= 1

    def test_low_test_coverage_penalty(self, simulator):
        project = {
            "tech_stack": "Python 3.11",
            "architecture": "MVC",
            "test_coverage": 30,
            "security_review": False,
        }
        result = simulator.simulate("technical", project)
        assert result["total_score"] < 8.0

    def test_security_review_bonus(self, simulator):
        project_a = {"tech_stack": "Python", "architecture": "MVC pattern with layers", "test_coverage": 80, "security_review": True}
        project_b = {"tech_stack": "Python", "architecture": "MVC pattern with layers", "test_coverage": 80, "security_review": False}
        result_a = simulator.simulate("technical", project_a)
        result_b = simulator.simulate("technical", project_b)
        assert result_a["total_score"] > result_b["total_score"]

    def test_dimension_scores_present(self, simulator, complete_project):
        result = simulator.simulate("technical", complete_project)
        assert "dimension_scores" in result
        assert len(result["dimension_scores"]) >= 4
        for dim_name, dim_data in result["dimension_scores"].items():
            assert "score" in dim_data
            assert "weight" in dim_data
            assert 0 <= dim_data["score"] <= 10


class TestInvestmentReview:
    """Investment review tests."""

    def test_high_score_complete_project(self, simulator, complete_project):
        result = simulator.simulate("investment", complete_project)
        assert result["total_score"] >= 7.0

    def test_low_score_minimal_project(self, simulator, minimal_project):
        result = simulator.simulate("investment", minimal_project)
        assert result["pass_probability"] < 0.5
        assert any("市场" in r for r in result["rejection_reasons"])

    def test_competitor_analysis_required(self, simulator):
        project = {"market_size": "100亿", "roi_estimate": "24个月回本详细分析", "competitor_analysis": False, "budget": 1000000, "timeline": "12个月"}
        result = simulator.simulate("investment", project)
        assert any("竞品" in r for r in result["rejection_reasons"])


class TestProductReview:
    """Product review tests."""

    def test_high_score_complete_project(self, simulator, complete_project):
        result = simulator.simulate("product", complete_project)
        assert result["total_score"] >= 6.0

    def test_low_score_minimal_project(self, simulator, minimal_project):
        result = simulator.simulate("product", minimal_project)
        assert result["pass_probability"] < 0.5

    def test_value_proposition_required(self, simulator):
        project = {"user_persona": "开发者", "value_proposition": "", "mvp_scope": "MVP", "success_metrics": ["DAU"], "feedback_mechanism": True}
        result = simulator.simulate("product", project)
        assert any("价值" in r or "核心" in r for r in result["rejection_reasons"])


class TestOpensourceReview:
    """Open source review tests."""

    def test_high_score_complete_project(self, simulator, complete_project):
        result = simulator.simulate("opensource", complete_project)
        assert result["total_score"] >= 6.0

    def test_no_license_penalty(self, simulator):
        project = {"license": "", "documentation": True, "contributing_guide": True, "code_of_conduct": True, "third_party_licenses": ["MIT"]}
        result = simulator.simulate("opensource", project)
        assert result["total_score"] < 8.0
        assert any("许可证" in r for r in result["rejection_reasons"])

    def test_minimal_project_fails(self, simulator, minimal_project):
        result = simulator.simulate("opensource", minimal_project)
        assert result["pass_probability"] < 0.5


class TestBoundaryConditions:
    """Boundary condition tests."""

    def test_invalid_review_type(self, simulator):
        with pytest.raises(ValueError, match="Invalid review_type"):
            simulator.simulate("invalid_type", {})

    def test_empty_project_info(self, simulator):
        result = simulator.simulate("technical", {})
        assert "total_score" in result
        assert "pass_probability" in result
        assert 0.0 <= result["pass_probability"] <= 1.0

    def test_all_review_types_return_consistent_format(self, simulator, complete_project):
        for review_type in ["technical", "investment", "product", "opensource"]:
            result = simulator.simulate(review_type, complete_project)
            assert "dimension_scores" in result
            assert "total_score" in result
            assert "pass_probability" in result
            assert "rejection_reasons" in result
            assert "suggestions" in result
            assert isinstance(result["rejection_reasons"], list)
            assert isinstance(result["suggestions"], list)
            assert 0 <= result["total_score"] <= 10

    def test_probability_range(self, simulator):
        project = {"tech_stack": "", "architecture": "", "test_coverage": 0, "security_review": False}
        result = simulator.simulate("technical", project)
        assert 0.0 <= result["pass_probability"] <= 1.0


class TestAntiSycophancy:
    """Tests for the anti-sycophancy mechanism."""

    def test_total_score_field(self, simulator, complete_project):
        """All results must include total_score on a 0-10 scale."""
        for review_type in ["technical", "investment", "product", "opensource"]:
            result = simulator.simulate(review_type, complete_project)
            assert "total_score" in result
            assert 0 <= result["total_score"] <= 10

    def test_multi_defect_compound_penalty(self, simulator, minimal_project):
        """Projects with many defects get compounded penalty."""
        result = simulator.simulate("technical", minimal_project)
        # Check for any anti-sycophancy marker (new format uses [非线性惩罚] or [抗讨好])
        assert any("[非线性惩罚]" in s or "[抗讨好]" in s or "[得分上限]" in s for s in result["suggestions"])

    def test_score_ceiling_enforced(self, simulator, minimal_project):
        """Many defects enforce a score ceiling regardless of base score."""
        result = simulator.simulate("opensource", minimal_project)
        # minimal_project has 5 defects → cap at 6.0
        assert result["total_score"] <= 6.0

    def test_defects_generate_suggestions(self, simulator):
        """Projects with multiple defects generate [抗讨好] suggestions."""
        project = {
            "tech_stack": "Python 3.11, FastAPI, PostgreSQL, React",
            "architecture": "微服务架构，前后端分离，API Gateway + 微服务集群，采用事件驱动",
            "test_coverage": 85,
            "security_review": False,
            "dependencies": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                             "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u"],
        }
        result = simulator.simulate("technical", project)
        # Has ≥2 defects, anti-sycophancy should be applied
        assert result["total_score"] <= 8.5

    def test_perfect_project_no_warnings(self, simulator, complete_project):
        """A complete project should not trigger sycophancy warnings."""
        result = simulator.simulate("technical", complete_project)
        assert len(result.get("sycophancy_warnings", [])) == 0
        assert not any("[抗讨好]" in s or "[非线性惩罚]" in s for s in result["suggestions"])

    def test_score_consistency(self, simulator, complete_project):
        """Verify total_score is consistent with pass_probability."""
        for review_type in ["technical", "investment", "product", "opensource"]:
            result = simulator.simulate(review_type, complete_project)
            expected_prob = result["total_score"] / 10
            assert abs(result["pass_probability"] - expected_prob) < 0.01


class TestAdversarialReview:
    """Tests for adversarial review mode."""

    def test_adversarial_review_returns_hostile_questions(self, simulator):
        """Adversarial review must generate hostile questions."""
        project = {"security_review": False, "competitor_analysis": False, "architecture": ""}
        result = simulator.simulate("adversarial", project)
        assert len(result["hostile_questions"]) >= 5

    def test_adversarial_review_returns_weakness_chain(self, simulator):
        """Adversarial review must generate weakness chains."""
        project = {"security_review": False, "competitor_analysis": False}
        result = simulator.simulate("adversarial", project)
        assert len(result["weakness_chain"]) >= 1

    def test_adversarial_review_returns_kill_factors(self, simulator):
        """Adversarial review must generate kill factors."""
        project = {"security_review": False, "competitor_analysis": False, "architecture": ""}
        result = simulator.simulate("adversarial", project)
        assert len(result["kill_factors"]) >= 1

    def test_adversarial_score_capped_at_75(self, simulator):
        """Adversarial review score should not exceed 7.5/10 (75%)."""
        project = {
            "architecture": "架构图: 微服务架构，完整安全设计",
            "security_review": True,
            "competitor_analysis": True,
            "team_background": "核心团队10年经验",
            "cost_estimate": "500万",
            "exit_strategy": "灰度下线方案",
            "user_persona": "企业开发者",
            "success_metrics": ["DAU 10万"],
        }
        result = simulator.simulate("adversarial", project)
        assert result["total_score"] <= 7.5

    def test_adversarial_multiple_kill_factors_reduce_probability(self, simulator):
        """Multiple kill factors should reduce pass_probability."""
        project = {"architecture": "", "security_review": False, "competitor_analysis": False, "user_persona": ""}
        result = simulator.simulate("adversarial", project)
        if len(result["kill_factors"]) >= 2:
            assert result["pass_probability"] <= 0.20

    def test_adversarial_hostile_questions_count(self, simulator):
        """Hostile questions must be between 5 and 8."""
        project = {"security_review": False, "architecture": "", "competitor_analysis": False}
        result = simulator.simulate("adversarial", project)
        assert 5 <= len(result["hostile_questions"]) <= 8


class TestWeaknessChain:
    """Tests for the weakness amplification mechanism."""

    def test_weakness_chain_has_two_layers(self, simulator):
        """Each weakness chain should have original, layer1, and optionally layer2."""
        project = {"security_review": False, "architecture": ""}
        result = simulator.simulate("adversarial", project)
        for chain in result["weakness_chain"]:
            assert "original_defect" in chain
            assert "layer1_inferred" in chain
            assert "layer2_inferred" in chain

    def test_weakness_chain_from_security_defect(self, simulator):
        """No security design should produce a chain about data leak risk."""
        project = {"security_review": False}
        result = simulator.simulate("adversarial", project)
        chain_text = " ".join(str(c) for c in result["weakness_chain"])
        assert any(kw in chain_text for kw in ["安全", "数据", "泄露", "合规"])

    def test_weakness_chain_from_no_competitor_analysis(self, simulator):
        """No competitor analysis should produce a chain about market positioning."""
        project = {"competitor_analysis": False}
        result = simulator.simulate("adversarial", project)
        chain_text = " ".join(str(c) for c in result["weakness_chain"])
        assert any(kw in chain_text for kw in ["竞品", "市场", "定位", "差异化"])


class TestNonLinearPenalty:
    """Tests for the non-linear defect penalty formula."""

    def test_penalty_increases_with_defect_count(self, simulator):
        """More defects should result in progressively larger penalties."""
        project_2_defects = {
            "tech_stack": "Python",
            "architecture": "MVC",
            "test_coverage": 0,
            "security_review": False,
            "dependencies": [],
        }
        project_5_defects = {
            "tech_stack": "",
            "architecture": "",
            "test_coverage": 0,
            "security_review": False,
            "dependencies": [],
        }
        result_2 = simulator.simulate("technical", project_2_defects)
        result_5 = simulator.simulate("technical", project_5_defects)
        # More defects → lower score (non-linear)
        assert result_5["total_score"] < result_2["total_score"]

    def test_score_ceiling_enforced_with_many_defects(self, simulator):
        """Projects with ≥4 defects should have score capped at 6.0."""
        project = {
            "tech_stack": "",
            "architecture": "",
            "test_coverage": 0,
            "security_review": False,
            "dependencies": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                             "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u"],
        }
        result = simulator.simulate("technical", project)
        assert result["total_score"] <= 6.0


class TestAllReviewTypesConsistent:
    """Tests for consistency across all review types including adversarial."""

    def test_adversarial_in_valid_types(self, simulator):
        """Adversarial must be a valid review type."""
        assert "adversarial" in simulator.VALID_TYPES

    def test_all_review_types_return_same_fields(self, simulator):
        """All review types must return the same set of fields."""
        project = {"tech_stack": "Python", "architecture": "MVC", "test_coverage": 50}
        expected_keys = {
            "dimension_scores", "total_score", "pass_probability",
            "rejection_reasons", "suggestions", "sycophancy_warnings",
            "hostile_questions", "weakness_chain", "kill_factors",
        }
        for review_type in simulator.VALID_TYPES:
            result = simulator.simulate(review_type, project)
            assert expected_keys.issubset(set(result.keys())), f"Missing keys in {review_type}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
