"""Tests for Reviewer Simulator engine."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.review_simulator.reviewer_simulator import ReviewerSimulator


@pytest.fixture
def simulator():
    return ReviewerSimulator()


@pytest.fixture
def complete_project():
    return {
        "tech_stack": "Python 3.11, FastAPI, PostgreSQL, React",
        "architecture": "微服务架构，前后端分离",
        "test_coverage": 85,
        "dependencies": ["fastapi", "sqlalchemy", "pytest"],
        "security_review": True,
        "market_size": "约500亿元",
        "roi_estimate": "预计18个月回本",
        "competitor_analysis": True,
        "budget": 2000000,
        "timeline": "6个月完成MVP",
        "user_persona": "企业内部项目经理和开发人员",
        "value_proposition": "提升项目交付效率50%",
        "mvp_scope": "需求管理+代码生成+质量审查",
        "success_metrics": ["交付周期缩短50%", "Bug率降低30%"],
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
        assert result["pass_probability"] >= 0.8
        assert len(result["suggestions"]) <= 1

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
        assert result["pass_probability"] < 0.8

    def test_security_review_bonus(self, simulator):
        project_a = {"tech_stack": "Python", "architecture": "MVC", "test_coverage": 80, "security_review": True}
        project_b = {"tech_stack": "Python", "architecture": "MVC", "test_coverage": 80, "security_review": False}
        result_a = simulator.simulate("technical", project_a)
        result_b = simulator.simulate("technical", project_b)
        assert result_a["pass_probability"] > result_b["pass_probability"]


class TestInvestmentReview:
    """Investment review tests."""

    def test_high_score_complete_project(self, simulator, complete_project):
        result = simulator.simulate("investment", complete_project)
        assert result["pass_probability"] >= 0.8

    def test_low_score_minimal_project(self, simulator, minimal_project):
        result = simulator.simulate("investment", minimal_project)
        assert result["pass_probability"] < 0.5
        assert any("市场" in r for r in result["rejection_reasons"])

    def test_competitor_analysis_required(self, simulator):
        project = {"market_size": "100亿", "roi_estimate": "24个月", "competitor_analysis": False, "budget": 1000000, "timeline": "12个月"}
        result = simulator.simulate("investment", project)
        assert any("竞品" in r for r in result["rejection_reasons"])


class TestProductReview:
    """Product review tests."""

    def test_high_score_complete_project(self, simulator, complete_project):
        result = simulator.simulate("product", complete_project)
        assert result["pass_probability"] >= 0.8

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
        assert result["pass_probability"] >= 0.8

    def test_no_license_penalty(self, simulator):
        project = {"license": "", "documentation": True, "contributing_guide": True, "code_of_conduct": True, "third_party_licenses": ["MIT"]}
        result = simulator.simulate("opensource", project)
        assert result["pass_probability"] < 0.8
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
        assert "pass_probability" in result
        assert 0.0 <= result["pass_probability"] <= 1.0

    def test_all_review_types_return_consistent_format(self, simulator, complete_project):
        for review_type in ["technical", "investment", "product", "opensource"]:
            result = simulator.simulate(review_type, complete_project)
            assert "pass_probability" in result
            assert "rejection_reasons" in result
            assert "suggestions" in result
            assert isinstance(result["rejection_reasons"], list)
            assert isinstance(result["suggestions"], list)

    def test_probability_range(self, simulator):
        project = {"tech_stack": "", "architecture": "", "test_coverage": 0, "security_review": False}
        result = simulator.simulate("technical", project)
        assert 0.0 <= result["pass_probability"] <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
