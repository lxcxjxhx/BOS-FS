"""Tests for Readme Refactor engine."""

import sys
import os
import pytest
import importlib.util

# Add engine directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load_readme_refactor():
    """Load ReadmeRefactor module from file path."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base, "core", "03_submission_optimizer", "readme_refactor.py")
    spec = importlib.util.spec_from_file_location("readme_refactor", file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ReadmeRefactor


@pytest.fixture
def refactor():
    return _load_readme_refactor()()


SAMPLE_README = """# BOS-FS 智能交付引擎

一个智能化的价值映射引擎，自动将技术特性翻译为业务成果。

## 简介

帮助企业自动化项目交付全流程。

## 特性

- AI 驱动的特性识别
- 自动测试
- CI/CD 集成

## Roadmap

- [x] 核心映射引擎
- [ ] 多模型支持
"""

GOAL_INFO = {
    "persona": "企业内部研发团队",
    "problem": "现有流程缺乏标准化，沟通成本高，交付质量不稳定",
    "solution": "开发一套自动化项目交付管理系统",
    "outcome": "提升交付效率50%，降低人工成本30%",
}


class TestFiveSectionCompleteness:
    """Test 5-section completeness (What/Why/How/Result/Next)."""

    def test_all_sections_present(self, refactor):
        result = refactor.refactor(SAMPLE_README)
        assert "## What" in result
        assert "## Why" in result
        assert "## How" in result
        assert "## Result" in result
        assert "## Next" in result

    def test_what_section_not_empty(self, refactor):
        result = refactor.refactor(SAMPLE_README)
        what_start = result.index("## What")
        why_start = result.index("## Why")
        what_content = result[what_start:why_start].strip()
        assert len(what_content) > len("## What — 一句话价值")

    def test_why_section_has_pain_points(self, refactor):
        result = refactor.refactor(SAMPLE_README)
        why_start = result.index("## Why")
        how_start = result.index("## How")
        why_content = result[why_start:how_start]
        assert "### 痛点" in why_content

    def test_how_section_has_architecture(self, refactor):
        result = refactor.refactor(SAMPLE_README)
        assert "### 架构" in result
        assert "### 特性" in result

    def test_next_section_has_roadmap(self, refactor):
        result = refactor.refactor(SAMPLE_README)
        next_start = result.index("## Next")
        assert len(result[next_start:]) > len("## Next — 路线图")


class TestTechToValueTransformation:
    """Test tech-to-value transformation rules."""

    def test_ai_workflow_transformed(self, refactor):
        text = "AI Workflow Engine 帮助团队提升效率"
        result = refactor.refactor(text)
        assert "帮助开发者自动转换需求为可交付资产" in result

    def test_cicd_transformed(self, refactor):
        text = "CI/CD 集成方案"
        result = refactor.refactor(text)
        assert "交付流水线" in result

    def test_code_generation_transformed(self, refactor):
        text = "代码生成模块"
        result = refactor.refactor(text)
        assert "开发效率提升" in result

    def test_multiple_terms_transformed(self, refactor):
        text = "支持多模型，自动测试，CI/CD集成"
        result = refactor.refactor(text)
        assert "减少重复配置与上下文切换" in result
        assert "质量保障自动化" in result


class TestWithGoalInfo:
    """Test with goal_info parameter."""

    def test_goal_info_solution_used(self, refactor):
        result = refactor.refactor("# Project", GOAL_INFO)
        assert "开发一套自动化项目交付管理系统" in result

    def test_goal_info_problem_used(self, refactor):
        result = refactor.refactor("# Project", GOAL_INFO)
        why_start = result.index("## Why")
        how_start = result.index("## How")
        why_section = result[why_start:how_start]
        assert "现有流程缺乏标准化" in why_section

    def test_goal_info_outcome_used(self, refactor):
        result = refactor.refactor("# Project", GOAL_INFO)
        assert "提升交付效率50%" in result

    def test_goal_info_overrides_readme(self, refactor):
        result = refactor.refactor(SAMPLE_README, GOAL_INFO)
        assert "开发一套自动化项目交付管理系统" in result


class TestErrorHandling:
    """Test empty input and short input error handling."""

    def test_empty_input_raises(self, refactor):
        with pytest.raises(ValueError, match="输入为空"):
            refactor.refactor("")

    def test_whitespace_only_raises(self, refactor):
        with pytest.raises(ValueError, match="输入为空"):
            refactor.refactor("   ")

    def test_short_input_note(self, refactor):
        result = refactor.refactor("ab")
        assert "内容不足" in result

    def test_valid_short_input_no_note(self, refactor):
        result = refactor.refactor("# Project\n" + "x" * 30)
        assert "内容不足" not in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
