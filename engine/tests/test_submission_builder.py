"""Tests for Submission Builder engine."""

import sys
import os
import json
import pytest
import importlib.util

# Add engine directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load_submission_builder():
    """Load SubmissionBuilder module from file path."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base, "core", "04_delivery_builder", "submission_builder.py")
    spec = importlib.util.spec_from_file_location("submission_builder", file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SubmissionBuilder


SAMPLE_PROJECT = {
    "name": "TestProject",
    "version": "1.0.0",
    "tagline": "Test project tagline",
    "description": "A test project for submission builder testing.",
    "features": ["Feature A", "Feature B"],
    "target_users": "Test users",
    "tech_stack": ["Python 3.9", "FastAPI"],
    "value_proposition": "提升效率50%",
}


@pytest.fixture
def builder(tmp_path):
    SB = _load_submission_builder()
    output_dir = str(tmp_path / "submission_bundle")
    return SB(output_dir=output_dir)


class TestEightComponentGeneration:
    """Test 8-component generation."""

    def test_all_eight_files_created(self, builder):
        result = builder.build(SAMPLE_PROJECT)
        bundle_path = result["bundle_path"]
        expected = [
            "README.md",
            "demo_guide.md",
            "introduction.md",
            "screenshots_guide.md",
            "FAQ.md",
            "risk_disclosure.md",
            "trust_statement.md",
            "bundle_meta.json",
        ]
        for filename in expected:
            filepath = os.path.join(bundle_path, filename)
            assert os.path.exists(filepath), f"{filename} was not created"

    def test_readme_content_not_empty(self, builder):
        result = builder.build(SAMPLE_PROJECT)
        readme_path = os.path.join(result["bundle_path"], "README.md")
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert len(content) > 100

    def test_faq_has_ten_questions(self, builder):
        result = builder.build(SAMPLE_PROJECT)
        faq_path = os.path.join(result["bundle_path"], "FAQ.md")
        with open(faq_path, "r", encoding="utf-8") as f:
            content = f.read()
        for i in range(1, 11):
            assert f"Q{i}:" in content

    def test_meta_json_is_valid(self, builder):
        result = builder.build(SAMPLE_PROJECT)
        meta_path = os.path.join(result["bundle_path"], "bundle_meta.json")
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        assert meta["project_name"] == SAMPLE_PROJECT["name"]
        assert meta["version"] == SAMPLE_PROJECT["version"]


class TestConsistencyCheck:
    """Test consistency check passes."""

    def test_consistent_project_passes(self, builder):
        result = builder.build(SAMPLE_PROJECT)
        assert result["status"] == "complete"

    def test_missing_name_warns(self, builder, tmp_path):
        project = {**SAMPLE_PROJECT}
        del project["name"]
        output_dir = str(tmp_path / "no_name_bundle")
        SB = _load_submission_builder()
        b = SB(output_dir=output_dir)
        result = b.build(project)
        assert result["status"] == "complete_with_warnings"

    def test_missing_version_warns(self, builder, tmp_path):
        project = {**SAMPLE_PROJECT}
        del project["version"]
        output_dir = str(tmp_path / "no_ver_bundle")
        SB = _load_submission_builder()
        b = SB(output_dir=output_dir)
        result = b.build(project)
        assert result["status"] == "complete_with_warnings"

    def test_consistency_report_created(self, builder):
        result = builder.build(SAMPLE_PROJECT)
        report_path = os.path.join(result["bundle_path"], "consistency_report.md")
        assert os.path.exists(report_path)


class TestTrustStatement:
    """Test trust statement includes authority references."""

    def test_owasp_reference(self, builder):
        content = builder.generate_trust_statement(SAMPLE_PROJECT)
        assert "OWASP" in content

    def test_clean_architecture_reference(self, builder):
        content = builder.generate_trust_statement(SAMPLE_PROJECT)
        assert "Clean Architecture" in content

    def test_iso25010_reference(self, builder):
        content = builder.generate_trust_statement(SAMPLE_PROJECT)
        assert "ISO" in content and "25010" in content

    def test_solid_reference(self, builder):
        content = builder.generate_trust_statement(SAMPLE_PROJECT)
        assert "SOLID" in content


class TestMissingRequiredField:
    """Test missing required field handling."""

    def test_empty_project_uses_defaults(self, builder, tmp_path):
        SB = _load_submission_builder()
        output_dir = str(tmp_path / "default_bundle")
        b = SB(output_dir=output_dir)
        result = b.build({})
        assert result["status"] == "complete_with_warnings"

    def test_missing_description_uses_empty(self, builder):
        project = {**SAMPLE_PROJECT, "description": ""}
        content = builder.generate_readme(project)
        # Empty description renders as empty line in overview section
        assert "## 1. 概述" in content

    def test_missing_features_uses_placeholder(self, builder):
        project = {**SAMPLE_PROJECT, "features": []}
        content = builder.generate_readme(project)
        assert "待补充" in content


class TestOutputFormat:
    """Test output format (bundle_path, components, status)."""

    def test_return_keys(self, builder):
        result = builder.build(SAMPLE_PROJECT)
        assert "bundle_path" in result
        assert "components" in result
        assert "status" in result

    def test_bundle_path_is_directory(self, builder):
        result = builder.build(SAMPLE_PROJECT)
        assert os.path.isdir(result["bundle_path"])

    def test_components_is_list_of_eight(self, builder):
        result = builder.build(SAMPLE_PROJECT)
        assert isinstance(result["components"], list)
        assert len(result["components"]) == 8

    def test_status_values(self, builder, tmp_path):
        r1 = builder.build(SAMPLE_PROJECT)
        assert r1["status"] in ("complete", "complete_with_warnings")

        SB = _load_submission_builder()
        output_dir = str(tmp_path / "warn_bundle")
        b2 = SB(output_dir=output_dir)
        r2 = b2.build({})
        assert r2["status"] == "complete_with_warnings"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
