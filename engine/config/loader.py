"""Configuration loader with hierarchical merging and dot notation access."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULTS_DIR = Path(__file__).parent / "defaults"

HARDCODED_DEFAULTS = {
    "reviewer_rules": {
        "review_types": {
            "technical": {
                "dimensions": {
                    "架构设计": {"weight": 25, "max": 10},
                    "技术栈": {"weight": 20, "max": 10},
                    "代码质量": {"weight": 25, "max": 10},
                    "安全性": {"weight": 15, "max": 10},
                    "依赖管理": {"weight": 15, "max": 10},
                }
            },
            "investment": {
                "dimensions": {
                    "市场规模": {"weight": 25, "max": 10},
                    "ROI估算": {"weight": 25, "max": 10},
                    "竞品分析": {"weight": 20, "max": 10},
                    "预算规划": {"weight": 15, "max": 10},
                    "时间线": {"weight": 15, "max": 10},
                }
            },
            "product": {
                "dimensions": {
                    "用户画像": {"weight": 25, "max": 10},
                    "价值主张": {"weight": 25, "max": 10},
                    "MVP范围": {"weight": 15, "max": 10},
                    "成功指标": {"weight": 20, "max": 10},
                    "反馈机制": {"weight": 15, "max": 10},
                }
            },
            "opensource": {
                "dimensions": {
                    "开源许可证": {"weight": 30, "max": 10},
                    "文档完整度": {"weight": 25, "max": 10},
                    "贡献指引": {"weight": 15, "max": 10},
                    "行为准则": {"weight": 10, "max": 10},
                    "第三方合规": {"weight": 20, "max": 10},
                }
            },
        },
        "thresholds": {
            "test_coverage": {"excellent": 80, "good": 60, "poor": 30},
            "text_length": {"detailed": 50, "moderate": 30, "brief": 20},
            "dependency_count": {"optimal": 10, "max_acceptable": 20},
        },
    },
    "anti_sycophancy": {
        "empty_praise_words": ["优秀", "完美", "出色", "一流", "极佳", "卓越"],
        "variance_threshold": 0.5,
        "high_score_threshold": 9,
        "security_score_threshold": 7,
        "trust_penalty": 2,
    },
    "adversarial_rules": {
        "base_score": 35,
        "ceiling": 75,
        "floor": 5,
        "pass_probability_cap_with_kill_factors": 0.20,
    },
    "submission_components": {
        "output_formats": ["markdown", "json", "html"],
    },
}


class ConfigLoader:
    """Hierarchical configuration loader with dot notation access.
    
    Supports three-tier merging: hardcoded defaults < JSON defaults < user overrides.
    """

    def __init__(self, config_dir: Optional[str] = None):
        """Initialize the configuration loader.
        
        Args:
            config_dir: Optional directory containing user JSON config files.
                        Defaults to the 'defaults' directory bundled with this module.
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = DEFAULTS_DIR

        self._cache: Dict[str, dict] = {}
        self._merged: Optional[dict] = None

    def load(self, filename: str) -> dict:
        """Load a single JSON configuration file.
        
        Falls back to hardcoded defaults if the file is missing.
        
        Args:
            filename: Name of the JSON config file (e.g., 'reviewer_rules.json').
            
        Returns:
            dict: Loaded configuration data.
        """
        if filename in self._cache:
            return self._cache[filename]

        key = Path(filename).stem
        file_path = self.config_dir / filename

        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = HARDCODED_DEFAULTS.get(key, {})

        self._cache[filename] = data
        return data

    def merge(self, base: dict, override: dict) -> dict:
        """Deep merge two configuration dictionaries.
        
        Values in 'override' take precedence over 'base'.
        Nested dictionaries are merged recursively.
        
        Args:
            base: Base configuration dictionary.
            override: Override configuration dictionary.
            
        Returns:
            dict: Merged configuration dictionary.
        """
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge(result[key], value)
            else:
                result[key] = value
        return result

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation.
        
        Example: get('reviewer_rules.thresholds.test_coverage.excellent') -> 80
        
        Args:
            key: Dot-separated path to the configuration value.
            default: Value to return if the key is not found.
            
        Returns:
            The configuration value at the specified path, or default if not found.
        """
        if self._merged is None:
            self._merged = self.load_all_defaults()

        parts = key.split(".")
        current = self._merged
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        return current

    def load_scenario(self, scenario_name: str) -> dict:
        """Load a scenario-specific configuration with full hierarchy merging.
        
        Looks for a scenario file in '<config_dir>/scenarios/<scenario_name>.json'.
        Merges: hardcoded defaults < JSON defaults < scenario overrides.
        
        Args:
            scenario_name: Name of the scenario (without .json extension).
            
        Returns:
            dict: Fully merged scenario configuration.
        """
        scenario_path = self.config_dir / "scenarios" / f"{scenario_name}.json"

        base = self.load_all_defaults()

        if scenario_path.exists():
            with open(scenario_path, "r", encoding="utf-8") as f:
                scenario_config = json.load(f)
            return self.merge(base, scenario_config)

        return base

    def load_all_defaults(self) -> dict:
        """Load and merge all default configuration files.
        
        Returns:
            dict: Fully merged default configuration.
        """
        result = HARDCODED_DEFAULTS.copy()

        if not self.config_dir.exists():
            return result

        for json_file in sorted(self.config_dir.glob("*.json")):
            key = json_file.stem
            file_data = self.load(json_file.name)
            if key in result:
                result[key] = self.merge(result[key], file_data)
            else:
                result[key] = file_data

        return result

    def reload(self) -> None:
        """Clear the cache and force reloading on next access."""
        self._cache.clear()
        self._merged = None
