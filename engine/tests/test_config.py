"""Tests for the ConfigLoader module.

Verifies hierarchical configuration loading, deep merging,
dot notation access, and scenario-based configuration.
"""

import sys
import os
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.loader import ConfigLoader, HARDCODED_DEFAULTS


@pytest.fixture
def config_loader(tmp_path):
    return ConfigLoader(config_dir=str(tmp_path))


@pytest.fixture
def temp_config_dir(tmp_path):
    defaults_dir = tmp_path
    defaults_dir.mkdir(exist_ok=True)

    reviewer_rules = {
        "review_types": {
            "technical": {
                "dimensions": {
                    "架构设计": {"weight": 30, "max": 10},
                    "新维度": {"weight": 10, "max": 10},
                }
            },
            "new_type": {
                "dimensions": {
                    "custom_dim": {"weight": 50, "max": 10},
                }
            }
        },
        "thresholds": {
            "test_coverage": {
                "excellent": 90,
                "good": 70,
            }
        }
    }
    (defaults_dir / "reviewer_rules.json").write_text(
        json.dumps(reviewer_rules, ensure_ascii=False), encoding="utf-8"
    )

    anti_sycophancy = {
        "layer1_lexical": {
            "empty_praise_words": ["优秀", "完美", "出色"],
            "trust_penalty": 3,
        },
        "layer3_score": {
            "high_score_threshold": 8,
            "variance_threshold": 0.3,
        }
    }
    (defaults_dir / "anti_sycophancy.json").write_text(
        json.dumps(anti_sycophancy, ensure_ascii=False), encoding="utf-8"
    )

    return defaults_dir


@pytest.fixture
def scenario_dir(tmp_path):
    config_dir = tmp_path / "config_with_scenarios"
    config_dir.mkdir()
    scenarios_dir = config_dir / "scenarios"
    scenarios_dir.mkdir()

    defaults_data = {"reviewer_rules": {"thresholds": {"pass_threshold": 6.0}}}
    (config_dir / "reviewer_rules.json").write_text(
        json.dumps(defaults_data), encoding="utf-8"
    )

    strict_scenario = {
        "reviewer_rules": {
            "thresholds": {
                "pass_threshold": 8.0,
                "strict_mode": True,
            }
        }
    }
    (scenarios_dir / "strict_review.json").write_text(
        json.dumps(strict_scenario), encoding="utf-8"
    )

    return config_dir


class TestConfigLoaderInitialization:
    def test_init_with_default_dir(self):
        loader = ConfigLoader()
        assert loader.config_dir is not None
        assert loader._cache == {}
        assert loader._merged is None

    def test_init_with_custom_dir(self, tmp_path):
        loader = ConfigLoader(config_dir=str(tmp_path))
        assert loader.config_dir == tmp_path

    def test_init_does_not_load_automatically(self, tmp_path):
        loader = ConfigLoader(config_dir=str(tmp_path))
        assert loader._merged is None


class TestLoadMethod:
    def test_load_existing_file(self, temp_config_dir):
        loader = ConfigLoader(config_dir=str(temp_config_dir))
        data = loader.load("reviewer_rules.json")
        assert "review_types" in data
        assert "new_type" in data["review_types"]

    def test_load_missing_file_returns_hardcoded_default(self, tmp_path):
        loader = ConfigLoader(config_dir=str(tmp_path))
        data = loader.load("nonexistent.json")
        assert data == {}

    def test_load_caches_result(self, temp_config_dir):
        loader = ConfigLoader(config_dir=str(temp_config_dir))
        data1 = loader.load("reviewer_rules.json")
        data2 = loader.load("reviewer_rules.json")
        assert data1 is data2

    def test_load_valid_json_syntax(self, tmp_path):
        config_dir = tmp_path
        config_file = config_dir / "valid.json"
        config_file.write_text('{"key": "value", "nested": {"a": 1}}', encoding="utf-8")

        loader = ConfigLoader(config_dir=str(config_dir))
        data = loader.load("valid.json")
        assert data["key"] == "value"
        assert data["nested"]["a"] == 1


class TestMergeMethod:
    def test_simple_merge(self, config_loader):
        base = {"a": 1, "b": 2}
        override = {"b": 3, "c": 4}
        result = config_loader.merge(base, override)
        assert result == {"a": 1, "b": 3, "c": 4}

    def test_deep_merge_nested_dicts(self, config_loader):
        base = {"outer": {"inner1": 1, "inner2": 2}}
        override = {"outer": {"inner2": 20, "inner3": 3}}
        result = config_loader.merge(base, override)
        assert result["outer"]["inner1"] == 1
        assert result["outer"]["inner2"] == 20
        assert result["outer"]["inner3"] == 3

    def test_override_replaces_non_dict_values(self, config_loader):
        base = {"key": {"nested": True}}
        override = {"key": "simple_string"}
        result = config_loader.merge(base, override)
        assert result["key"] == "simple_string"

    def test_merge_preserves_base_when_no_override(self, config_loader):
        base = {"a": {"b": {"c": 1}}}
        override = {}
        result = config_loader.merge(base, override)
        assert result == base

    def test_deep_merge_three_levels(self, config_loader):
        base = {"level1": {"level2": {"level3": "base_value", "keep": True}}}
        override = {"level1": {"level2": {"level3": "override_value"}}}
        result = config_loader.merge(base, override)
        assert result["level1"]["level2"]["level3"] == "override_value"
        assert result["level1"]["level2"]["keep"] is True

    def test_merge_does_not_mutate_base(self, config_loader):
        base = {"a": {"b": 1}}
        override = {"a": {"c": 2}}
        config_loader.merge(base, override)
        assert "c" not in base["a"]


class TestGetMethod:
    def test_get_top_level_key(self, config_loader):
        config_loader._merged = {"key": "value"}
        assert config_loader.get("key") == "value"

    def test_get_nested_key_with_dot_notation(self, config_loader):
        config_loader._merged = {"a": {"b": {"c": "deep_value"}}}
        assert config_loader.get("a.b.c") == "deep_value"

    def test_get_returns_default_for_missing_key(self, config_loader):
        config_loader._merged = {"a": 1}
        assert config_loader.get("missing", "default_val") == "default_val"

    def test_get_returns_default_for_partial_path(self, config_loader):
        config_loader._merged = {"a": {"b": 1}}
        assert config_loader.get("a.b.c", 42) == 42

    def test_get_hardcoded_default_via_dot_notation(self):
        loader = ConfigLoader()
        result = loader.get("reviewer_rules.thresholds.test_coverage.excellent")
        assert result == 80

    def test_get_auto_loads_defaults_when_merged_is_none(self):
        loader = ConfigLoader()
        assert loader._merged is None
        result = loader.get("reviewer_rules")
        assert result is not None
        assert "thresholds" in result


class TestLoadScenario:
    def test_load_existing_scenario(self, scenario_dir):
        loader = ConfigLoader(config_dir=str(scenario_dir))
        result = loader.load_scenario("strict_review")
        assert result["reviewer_rules"]["thresholds"]["pass_threshold"] == 8.0
        assert result["reviewer_rules"]["thresholds"]["strict_mode"] is True

    def test_load_missing_scenario_returns_base(self, scenario_dir):
        loader = ConfigLoader(config_dir=str(scenario_dir))
        result = loader.load_scenario("nonexistent_scenario")
        assert "reviewer_rules" in result
        assert "thresholds" in result["reviewer_rules"]

    def test_scenario_deep_merges_with_defaults(self, scenario_dir):
        loader = ConfigLoader(config_dir=str(scenario_dir))
        result = loader.load_scenario("strict_review")
        assert "pass_threshold" in result["reviewer_rules"]["thresholds"]

    def test_scenario_adds_new_keys(self, scenario_dir):
        loader = ConfigLoader(config_dir=str(scenario_dir))
        result = loader.load_scenario("strict_review")
        assert result["reviewer_rules"]["thresholds"]["strict_mode"] is True


class TestLoadAllDefaults:
    def test_load_all_defaults_returns_merged_dict(self, temp_config_dir):
        loader = ConfigLoader(config_dir=str(temp_config_dir))
        result = loader.load_all_defaults()
        assert isinstance(result, dict)
        assert "reviewer_rules" in result
        assert "anti_sycophancy" in result

    def test_load_all_defaults_includes_hardcoded(self, tmp_path):
        loader = ConfigLoader(config_dir=str(tmp_path))
        result = loader.load_all_defaults()
        assert "reviewer_rules" in result
        assert "thresholds" in result["reviewer_rules"]

    def test_load_all_defaults_file_overrides_hardcoded(self, temp_config_dir):
        loader = ConfigLoader(config_dir=str(temp_config_dir))
        result = loader.load_all_defaults()
        thresholds = result["reviewer_rules"]["thresholds"]["test_coverage"]
        assert thresholds["excellent"] == 90
        assert thresholds["good"] == 70

    def test_load_all_defaults_handles_missing_config_dir(self, tmp_path):
        non_existent = tmp_path / "non_existent_dir"
        loader = ConfigLoader(config_dir=str(non_existent))
        result = loader.load_all_defaults()
        assert "reviewer_rules" in result


class TestReload:
    def test_reload_clears_cache(self, temp_config_dir):
        loader = ConfigLoader(config_dir=str(temp_config_dir))
        loader.load("reviewer_rules.json")
        assert "reviewer_rules.json" in loader._cache
        loader.reload()
        assert loader._cache == {}

    def test_reload_resets_merged(self, temp_config_dir):
        loader = ConfigLoader(config_dir=str(temp_config_dir))
        loader.get("reviewer_rules")
        assert loader._merged is not None
        loader.reload()
        assert loader._merged is None


class TestFallbackToHardcodedDefaults:
    def test_hardcoded_defaults_has_reviewer_rules(self):
        assert "reviewer_rules" in HARDCODED_DEFAULTS

    def test_hardcoded_defaults_has_thresholds(self):
        assert "thresholds" in HARDCODED_DEFAULTS["reviewer_rules"]

    def test_hardcoded_defaults_has_anti_sycophancy(self):
        assert "anti_sycophancy" in HARDCODED_DEFAULTS

    def test_hardcoded_defaults_has_adversarial_rules(self):
        assert "adversarial_rules" in HARDCODED_DEFAULTS

    def test_loader_falls_back_when_config_dir_empty(self, tmp_path):
        loader = ConfigLoader(config_dir=str(tmp_path))
        result = loader.load("some_nonexistent_file.json")
        assert isinstance(result, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
