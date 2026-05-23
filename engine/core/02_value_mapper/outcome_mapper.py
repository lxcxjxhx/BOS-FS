"""Outcome Mapper - Convert technical Features to user Capabilities and Outcomes."""

import re
from typing import Dict, List, Optional


class OutcomeMapper:
    """Converts technical features to user-facing capabilities and measurable outcomes."""

    CONVERSION_RULES = [
        # AI 类别
        {"category": "AI", "feature": "AI Workflow", "capability": "交付自动化平台", "outcome": "交付周期缩短60%"},
        {"category": "AI", "feature": "多模型调度", "capability": "智能资源分配", "outcome": "减少重复配置"},
        {"category": "AI", "feature": "RAG", "capability": "知识增强", "outcome": "回答准确率提升40%"},
        {"category": "AI", "feature": "Agent协作", "capability": "多智能体编排", "outcome": "复杂任务并行执行"},
        {"category": "AI", "feature": "Function Calling", "capability": "工具调用自动化", "outcome": "减少手动API集成"},

        # DevOps 类别
        {"category": "DevOps", "feature": "CI/CD", "capability": "交付流水线", "outcome": "发布频率提升3倍"},
        {"category": "DevOps", "feature": "自动测试", "capability": "质量保障自动化", "outcome": "回归成本降低60%"},
        {"category": "DevOps", "feature": "代码生成", "capability": "开发加速", "outcome": "编码时间减少40%"},
        {"category": "DevOps", "feature": "容器化", "capability": "环境标准化", "outcome": "部署一致性100%"},

        # Product 类别
        {"category": "Product", "feature": "文档自动化", "capability": "知识沉淀", "outcome": "文档维护成本降低70%"},
        {"category": "Product", "feature": "权限管理", "capability": "访问控制", "outcome": "安全合规100%"},
        {"category": "Product", "feature": "数据可视化", "capability": "洞察呈现", "outcome": "决策效率提升50%"},
    ]

    def map_feature(self, feature: str) -> Dict[str, str]:
        """Convert a single technical feature to capability and outcome.

        Args:
            feature: Technical feature description.

        Returns:
            Dict with keys: feature, capability, outcome.
        """
        text = feature.strip()

        if not text:
            return {
                "feature": "",
                "capability": "未明确",
                "outcome": "未明确",
            }

        match = self._find_match(text)
        if match:
            return {
                "feature": text,
                "capability": match["capability"],
                "outcome": match["outcome"],
            }

        return self._generic_conversion(text)

    def map_features(self, features: List[str]) -> Dict[str, List[Dict[str, str]]]:
        """Convert multiple technical features to capabilities and outcomes.

        Args:
            features: List of technical feature descriptions.

        Returns:
            Dict with key 'features' containing a list of mapped results.
        """
        if not features:
            return {"features": []}

        mapped = [self.map_feature(f) for f in features]
        return {"features": mapped}

    def _find_match(self, feature: str) -> Optional[Dict[str, str]]:
        """Find the best matching rule from the conversion rules database."""
        # Exact match
        for rule in self.CONVERSION_RULES:
            if rule["feature"].lower() == feature.lower():
                return rule

        # Fuzzy match using regex
        for rule in self.CONVERSION_RULES:
            pattern = re.compile(re.escape(rule["feature"]), re.IGNORECASE)
            if pattern.search(feature):
                return rule

        return None

    def _generic_conversion(self, feature: str) -> Dict[str, str]:
        """Fallback generic conversion when no rule matches.

        Args:
            feature: Technical feature that has no matching rule.

        Returns:
            Dict with generic capability and outcome based on the feature.
        """
        return {
            "feature": feature,
            "capability": f"让用户{feature}",
            "outcome": f"提升{feature}相关效率",
        }


if __name__ == "__main__":
    mapper = OutcomeMapper()

    # Single feature conversion
    print("=== Single Feature Conversion ===")
    result = mapper.map_feature("多模型调度")
    print(f"Input: 多模型调度")
    print(f"Output: {result}")
    print()

    # Multiple features conversion
    print("=== Multiple Features Conversion ===")
    sample_features = ["AI Workflow", "自动测试", "CI/CD"]
    result = mapper.map_features(sample_features)

    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()

    # Generic conversion (no rule match)
    print("=== Generic Conversion (Fallback) ===")
    result = mapper.map_feature("实时数据同步")
    print(f"Input: 实时数据同步")
    print(f"Output: {result}")
