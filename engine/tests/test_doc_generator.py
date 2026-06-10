"""
doc-generator 文档生成质量规则测试.

验证知识库文件的可信度标注、真实案例目录完整性、
以及 doc-generator SKILL 的核心原则覆盖。
"""

import pytest
from pathlib import Path

# 知识库根目录：engine/tests/../../../knowledge
KNOWLEDGE_DIR = Path(__file__).parent.parent.parent / "knowledge"
# skills 根目录：engine/tests/../../../skills
SKILLS_DIR = Path(__file__).parent.parent.parent / "skills"


class TestCredibilityRating:
    """验证所有知识库文件包含可信度标注。"""

    def test_content_quality_rules_exists(self):
        """content_quality_rules.md 文件存在"""
        path = KNOWLEDGE_DIR / "governance" / "content_quality_rules.md"
        assert path.exists(), f"文件不存在: {path}"

    def test_adoption_files_have_rating(self):
        """adoption/ 目录文件都有可信度标注"""
        adoption_dir = KNOWLEDGE_DIR / "adoption"
        for f in adoption_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            assert "可信度" in content, f"{f.name} 缺少可信度标注"

    def test_governance_files_have_rating(self):
        """governance/ 目录文件都有可信度标注"""
        gov_dir = KNOWLEDGE_DIR / "governance"
        for f in gov_dir.rglob("*.md"):
            if f.name == "content_quality_rules.md":
                continue  # 该文件自身定义评级规范
            content = f.read_text(encoding="utf-8")
            assert "可信度" in content, f"{f.name} 缺少可信度标注"

    def test_runtime_files_have_rating(self):
        """runtime/ 目录文件都有可信度标注"""
        runtime_dir = KNOWLEDGE_DIR / "runtime"
        for f in runtime_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            assert "可信度" in content, f"{f.name} 缺少可信度标注"

    def test_intent_files_have_rating(self):
        """intent/ 目录文件都有可信度标注"""
        intent_dir = KNOWLEDGE_DIR / "intent"
        for f in intent_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            assert "可信度" in content, f"{f.name} 缺少可信度标注"

    def test_template_files_have_rating(self):
        """execution/templates/ 目录文件都有可信度标注"""
        tpl_dir = KNOWLEDGE_DIR / "execution" / "templates"
        for f in tpl_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            assert "可信度" in content, f"{f.name} 缺少可信度标注"


class TestRealWorldDirectory:
    """验证真实案例目录完整性。"""

    def test_real_world_dir_exists(self):
        """real-world/ 目录存在"""
        path = KNOWLEDGE_DIR / "real-world"
        assert path.exists(), f"目录不存在: {path}"
        assert path.is_dir()

    def test_readme_exists(self):
        """real-world/README.md 存在"""
        path = KNOWLEDGE_DIR / "real-world" / "README.md"
        assert path.exists(), f"文件不存在: {path}"

    def test_template_exists(self):
        """real-world/template.md 存在"""
        path = KNOWLEDGE_DIR / "real-world" / "template.md"
        assert path.exists(), f"文件不存在: {path}"

    def test_example_case_exists(self):
        """real-world/ 至少有一个真实案例"""
        path = KNOWLEDGE_DIR / "real-world"
        cases = list(path.glob("*.md"))
        # 排除 README.md 和 template.md
        cases = [c for c in cases if c.name not in ("README.md", "template.md")]
        assert len(cases) >= 1, "real-world/ 应至少包含一个真实案例文件"

    def test_example_case_has_credibility(self):
        """真实案例文件包含可信度标注"""
        path = KNOWLEDGE_DIR / "real-world" / "pen-test-lessons.md"
        content = path.read_text(encoding="utf-8")
        assert "可信度" in content, "pen-test-lessons.md 缺少可信度标注"


class TestDocGeneratorSkill:
    """验证 doc-generator SKILL 的完整性。"""

    @pytest.fixture(scope="class")
    def skill_path(self):
        return SKILLS_DIR / "doc-generator" / "SKILL.md"

    def test_skill_exists(self, skill_path):
        """doc-generator/SKILL.md 存在"""
        assert skill_path.exists(), f"SKILL 文件不存在: {skill_path}"

    def test_skill_has_core_principles(self, skill_path):
        """SKILL 包含核心原则"""
        content = skill_path.read_text(encoding="utf-8")
        assert (
            "真实场景" in content or "真实" in content
        ), "SKILL 缺少'真实场景优先'原则"
        assert (
            "人工校对" in content or "校对" in content
        ), "SKILL 缺少'人工校对'相关要求"

    def test_skill_has_anti_patterns(self, skill_path):
        """SKILL 包含反模式定义"""
        content = skill_path.read_text(encoding="utf-8")
        assert (
            "反模式" in content or "Anti" in content
        ), "SKILL 缺少反模式定义"


class TestDocGenExample:
    """验证文档生成示例完整性。"""

    @pytest.fixture(scope="class")
    def example_path(self):
        return Path(__file__).parent.parent.parent / "examples" / "doc-gen-example.md"

    def test_example_exists(self, example_path):
        """doc-gen-example.md 存在"""
        assert example_path.exists(), f"示例文件不存在: {example_path}"

    def test_example_shows_workflow(self, example_path):
        """示例展示了完整工作流"""
        content = example_path.read_text(encoding="utf-8")
        assert (
            "收集" in content or "素材" in content
        ), "示例缺少素材收集环节"
        assert (
            "校对" in content or "验证" in content
        ), "示例缺少校对/验证环节"
