"""Tests for Configurable Submission Builder.

Tests SubmissionBuilder with default config (backward compatible),
custom component registration, add/remove/enable/disable components,
HTML/JSON output formats, and custom screenshot resolution.
"""

import sys
import os
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def _load_submission_builder():
    base = os.path.join(os.path.dirname(__file__), "..", "core", "04_delivery_builder", "submission_builder.py")
    import importlib.util
    spec = importlib.util.spec_from_file_location("submission_builder", base)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SubmissionBuilder


@pytest.fixture
def SubmissionBuilder():
    return _load_submission_builder()


@pytest.fixture
def default_builder(SubmissionBuilder, tmp_path):
    output_dir = str(tmp_path / "default_bundle")
    return SubmissionBuilder(output_dir=output_dir)


@pytest.fixture
def sample_project():
    return {
        "name": "TestProject",
        "version": "1.0.0",
        "tagline": "Test project tagline",
        "description": "A test project for submission builder testing.",
        "features": ["Feature A", "Feature B"],
        "target_users": "Test users",
        "tech_stack": ["Python 3.9", "FastAPI"],
        "value_proposition": "提升效率50%",
    }


class TestDefaultConfigBackwardCompatible:
    """Test SubmissionBuilder with default config (backward compatible)."""

    def test_default_init_no_config_path(self, default_builder):
        assert default_builder.output_dir is not None
        assert len(default_builder._components_config) == 8

    def test_default_build_creates_eight_components(self, default_builder, sample_project):
        result = default_builder.build(sample_project)
        assert result["status"] == "complete"
        assert len(result["components"]) == 8

    def test_default_build_creates_bundle_directory(self, default_builder, sample_project):
        result = default_builder.build(sample_project)
        assert os.path.isdir(result["bundle_path"])

    def test_default_build_all_expected_files(self, default_builder, sample_project):
        result = default_builder.build(sample_project)
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
            filepath = os.path.join(result["bundle_path"], filename)
            assert os.path.exists(filepath), f"{filename} was not created"

    def test_default_readme_content_not_empty(self, default_builder, sample_project):
        result = default_builder.build(sample_project)
        readme_path = os.path.join(result["bundle_path"], "README.md")
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert len(content) > 100

    def test_default_build_empty_project_uses_defaults(self, SubmissionBuilder, tmp_path):
        output_dir = str(tmp_path / "empty_bundle")
        builder = SubmissionBuilder(output_dir=output_dir)
        result = builder.build({})
        assert result["status"] in ("complete", "partial")
        assert "bundle_path" in result


class TestCustomComponentRegistration:
    """Test custom component registration."""

    def test_register_custom_component(self, default_builder):
        def my_generator(project_info):
            return f"Custom content for {project_info.get('name', 'unknown')}"

        default_builder.register_component("custom.md", my_generator)
        assert "custom.md" in default_builder._component_registry

    def test_registered_component_generates_content(self, default_builder, sample_project):
        def my_generator(project_info):
            return f"Project: {project_info['name']}"

        default_builder.register_component("custom.md", my_generator)
        content = default_builder._resolve_generator("custom.md")(sample_project)
        assert "TestProject" in content

    def test_registered_component_can_be_used_in_build(self, SubmissionBuilder, tmp_path, sample_project):
        output_dir = str(tmp_path / "custom_reg_bundle")
        builder = SubmissionBuilder(output_dir=output_dir)

        builder.add_component("api_doc.md", "custom_api_gen")

        def api_doc_generator(project_info):
            return f"# API Documentation\n\nProject: {project_info['name']}"

        builder.register_component("custom_api_gen", api_doc_generator)
        result = builder.build(sample_project)

        api_path = os.path.join(result["bundle_path"], "api_doc.md")
        assert os.path.exists(api_path)
        with open(api_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "TestProject" in content

    def test_unregister_or_overwrite_component(self, default_builder):
        def gen_v1(_):
            return "version 1"

        def gen_v2(_):
            return "version 2"

        default_builder.register_component("test.md", gen_v1)
        assert default_builder._component_registry["test.md"]({}) == "version 1"

        default_builder.register_component("test.md", gen_v2)
        assert default_builder._component_registry["test.md"]({}) == "version 2"


class TestAddRemoveEnableDisableComponents:
    """Test add/remove/enable/disable components."""

    def test_add_component(self, default_builder):
        default_builder.add_component("extra.md", "generate_extra")
        comp_list = default_builder._components_config
        assert any(c["filename"] == "extra.md" for c in comp_list)

    def test_add_component_default_enabled(self, default_builder):
        default_builder.add_component("extra.md", "generate_extra")
        comp_list = default_builder._components_config
        extra = [c for c in comp_list if c["filename"] == "extra.md"][0]
        assert extra["enabled"] is True

    def test_add_component_disabled(self, default_builder):
        default_builder.add_component("extra.md", "generate_extra", enabled=False)
        comp_list = default_builder._components_config
        extra = [c for c in comp_list if c["filename"] == "extra.md"][0]
        assert extra["enabled"] is False

    def test_remove_component(self, default_builder):
        original_count = len(default_builder._components_config)
        removed = default_builder.remove_component("README.md")
        assert removed is True
        assert len(default_builder._components_config) == original_count - 1

    def test_remove_nonexistent_component(self, default_builder):
        removed = default_builder.remove_component("nonexistent.md")
        assert removed is False

    def test_disable_component(self, default_builder):
        disabled = default_builder.disable_component("FAQ.md")
        assert disabled is True
        faq_comp = [c for c in default_builder._components_config if c["filename"] == "FAQ.md"][0]
        assert faq_comp["enabled"] is False

    def test_disable_nonexistent_component(self, default_builder):
        disabled = default_builder.disable_component("nonexistent.md")
        assert disabled is False

    def test_enable_component(self, default_builder):
        default_builder.disable_component("FAQ.md")
        enabled = default_builder.enable_component("FAQ.md")
        assert enabled is True
        faq_comp = [c for c in default_builder._components_config if c["filename"] == "FAQ.md"][0]
        assert faq_comp["enabled"] is True

    def test_disabled_component_not_in_build(self, SubmissionBuilder, tmp_path, sample_project):
        output_dir = str(tmp_path / "disabled_bundle")
        builder = SubmissionBuilder(output_dir=output_dir)
        builder.disable_component("FAQ.md")
        builder.disable_component("risk_disclosure.md")
        result = builder.build(sample_project)
        assert "FAQ.md" not in result["components"]
        assert "risk_disclosure.md" not in result["components"]

    def test_removed_component_not_in_build(self, SubmissionBuilder, tmp_path, sample_project):
        output_dir = str(tmp_path / "removed_bundle")
        builder = SubmissionBuilder(output_dir=output_dir)
        builder.remove_component("demo_guide.md")
        result = builder.build(sample_project)
        assert "demo_guide.md" not in result["components"]


class TestHTMLOutputFormat:
    """Test HTML output format."""

    def test_html_output_creates_html_files(self, SubmissionBuilder, tmp_path, sample_project):
        output_dir = str(tmp_path / "html_bundle")
        builder = SubmissionBuilder(output_dir=output_dir)
        result = builder.build(sample_project, output_format="html")
        md_files = [c for c in result["components"] if c.endswith(".md") or c.endswith(".html")]
        for comp in md_files:
            if not comp.endswith(".json"):
                assert comp.endswith(".html"), f"Expected .html extension, got {comp}"

    def test_html_output_contains_doctype(self, SubmissionBuilder, tmp_path, sample_project):
        output_dir = str(tmp_path / "html_bundle2")
        builder = SubmissionBuilder(output_dir=output_dir)
        result = builder.build(sample_project, output_format="html")
        readme_html = os.path.join(result["bundle_path"], "README.html")
        with open(readme_html, "r", encoding="utf-8") as f:
            content = f.read()
        assert "<!DOCTYPE html>" in content

    def test_html_output_contains_html_tags(self, SubmissionBuilder, tmp_path, sample_project):
        output_dir = str(tmp_path / "html_bundle3")
        builder = SubmissionBuilder(output_dir=output_dir)
        result = builder.build(sample_project, output_format="html")
        intro_html = os.path.join(result["bundle_path"], "introduction.html")
        with open(intro_html, "r", encoding="utf-8") as f:
            content = f.read()
        assert "<html" in content
        assert "</html>" in content

    def test_html_output_preserves_project_info(self, SubmissionBuilder, tmp_path, sample_project):
        output_dir = str(tmp_path / "html_bundle4")
        builder = SubmissionBuilder(output_dir=output_dir)
        result = builder.build(sample_project, output_format="html")
        readme_html = os.path.join(result["bundle_path"], "README.html")
        with open(readme_html, "r", encoding="utf-8") as f:
            content = f.read()
        assert "TestProject" in content


class TestJSONOutputFormat:
    """Test JSON output format."""

    def test_json_output_returns_dict(self, default_builder, sample_project):
        result = default_builder.build(sample_project, output_format="json")
        assert isinstance(result, dict)

    def test_json_output_has_components_dict(self, default_builder, sample_project):
        result = default_builder.build(sample_project, output_format="json")
        assert "components" in result
        assert isinstance(result["components"], dict)

    def test_json_output_has_metadata(self, default_builder, sample_project):
        result = default_builder.build(sample_project, output_format="json")
        assert "metadata" in result
        assert result["metadata"]["project_name"] == "TestProject"
        assert result["metadata"]["version"] == "1.0.0"

    def test_json_output_has_status(self, default_builder, sample_project):
        result = default_builder.build(sample_project, output_format="json")
        assert "status" in result
        assert result["status"] in ("complete", "partial", "error")

    def test_json_output_is_serializable(self, default_builder, sample_project):
        result = default_builder.build(sample_project, output_format="json")
        serialized = json.dumps(result, ensure_ascii=False)
        deserialized = json.loads(serialized)
        assert deserialized["status"] == result["status"]


class TestCustomScreenshotResolution:
    """Test custom screenshot resolution."""

    def test_default_screenshot_resolution(self, default_builder):
        assert default_builder._screenshot_resolution == (1920, 1080)

    def test_custom_screenshot_resolution_via_config(self, SubmissionBuilder, tmp_path):
        config_dir = tmp_path / "config_with_res"
        config_dir.mkdir()

        config_file = config_dir / "submission_config.json"
        config_data = {
            "screenshot_resolution": [2560, 1440],
            "components": [],
        }
        config_file.write_text(json.dumps(config_data), encoding="utf-8")

        output_dir = str(tmp_path / "res_bundle")
        builder = SubmissionBuilder(output_dir=output_dir, config_path=str(config_file))
        assert builder._screenshot_resolution == (2560, 1440)

    def test_custom_screenshot_resolution_in_json_metadata(self, SubmissionBuilder, tmp_path, sample_project):
        config_dir = tmp_path / "config_with_res2"
        config_dir.mkdir()

        config_file = config_dir / "submission_config.json"
        config_data = {
            "screenshot_resolution": [3840, 2160],
            "components": [],
        }
        config_file.write_text(json.dumps(config_data), encoding="utf-8")

        output_dir = str(tmp_path / "res_bundle2")
        builder = SubmissionBuilder(output_dir=output_dir, config_path=str(config_file))
        result = builder.build(sample_project, output_format="json")
        assert result["metadata"]["screenshot_resolution"] == "3840x2160"

    def test_screenshot_resolution_tuple_conversion(self, SubmissionBuilder, tmp_path):
        config_dir = tmp_path / "config_with_res3"
        config_dir.mkdir()

        config_file = config_dir / "submission_config.json"
        config_data = {
            "screenshot_resolution": [1280, 720],
        }
        config_file.write_text(json.dumps(config_data), encoding="utf-8")

        output_dir = str(tmp_path / "res_bundle3")
        builder = SubmissionBuilder(output_dir=output_dir, config_path=str(config_file))
        assert isinstance(builder._screenshot_resolution, tuple)
        assert builder._screenshot_resolution[0] == 1280
        assert builder._screenshot_resolution[1] == 720


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
