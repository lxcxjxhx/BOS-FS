"""成果映射引擎 — 将技术特性转换为业务能力与业务成果。"""

from __future__ import annotations


# ────────────────────── 转换规则库 ──────────────────────

FEATURE_RULES: dict[str, str] = {
    "ai workflow": "AI Workflow",
    "模型调度": "模型调度",
    "多模型支持": "多模型支持",
    "automated pipeline": "自动化流水线",
    "ci/cd": "CI/CD 集成",
    "code review": "代码审查",
    "test generation": "测试用例生成",
    "智能路由": "智能路由",
    "缓存优化": "缓存优化",
    "灰度发布": "灰度发布",
    "a/b test": "A/B 测试",
    "数据分析": "数据分析平台",
    "自动化部署": "自动化部署",
    "监控告警": "监控告警",
    "日志聚合": "日志聚合",
}

CAPABILITY_RULES: dict[str, str] = {
    "AI Workflow": "交付自动化平台",
    "模型调度": "降低交付成本",
    "多模型支持": "减少重复配置与上下文切换",
    "自动化流水线": "端到端交付加速",
    "CI/CD 集成": "发布频率提升",
    "代码审查": "代码质量保障",
    "测试用例生成": "测试覆盖率提升",
    "智能路由": "流量调度优化",
    "缓存优化": "响应延迟降低",
    "灰度发布": "风险控制能力",
    "A/B 测试": "数据驱动决策",
    "数据分析平台": "业务洞察自动化",
    "自动化部署": "运维成本降低",
    "监控告警": "故障响应速度提升",
    "日志聚合": "问题定位效率提升",
}

OUTCOME_RULES: dict[str, str] = {
    "交付自动化平台": "交付周期缩短 60%，人工干预减少 80%",
    "降低交付成本": "单次交付成本下降 40%",
    "减少重复配置与上下文切换": "开发者效率提升 30%",
    "端到端交付加速": "从代码提交到上线时间缩短 50%",
    "发布频率提升": "每日可发布次数提升 3x",
    "代码质量保障": "线上缺陷率降低 35%",
    "测试覆盖率提升": "回归测试时间减少 70%",
    "流量调度优化": "系统吞吐量提升 25%",
    "响应延迟降低": "P99 延迟下降 50%",
    "风险控制能力": "故障影响范围缩小 80%",
    "数据驱动决策": "实验迭代周期缩短 60%",
    "业务洞察自动化": "决策响应时间从天级降至分钟级",
    "运维成本降低": "运维人力投入减少 50%",
    "故障响应速度提升": "MTTR 降低 65%",
    "问题定位效率提升": "排查时间从小时级降至分钟级",
}


class OutcomeMapper:
    """Feature → Capability → Outcome 转换器。

    将底层技术特性翻译为业务方能理解的成果描述。
    """

    def map_feature_to_outcome(self, feature: str) -> dict[str, str]:
        """将技术特性映射到能力与成果。

        Args:
            feature: 技术特性描述，如 "AI Workflow"、"模型调度" 等。

        Returns:
            {"feature": str, "capability": str, "outcome": str}
        """
        normalized = feature.strip()
        capability = self._lookup_capability(normalized)
        outcome = self._lookup_outcome(capability)

        return {
            "feature": normalized,
            "capability": capability,
            "outcome": outcome,
        }

    @staticmethod
    def _lookup_capability(feature: str) -> str:
        """查找能力层描述。"""
        # 精确匹配
        if feature in CAPABILITY_RULES:
            return CAPABILITY_RULES[feature]
        # 通过 feature 别名匹配
        for alias, canonical in FEATURE_RULES.items():
            if alias in feature.lower():
                return CAPABILITY_RULES.get(canonical, feature)
        # 兜底
        return feature

    @staticmethod
    def _lookup_outcome(capability: str) -> str:
        """查找成果描述。"""
        if capability in OUTCOME_RULES:
            return OUTCOME_RULES[capability]
        # 模糊匹配
        for key, value in OUTCOME_RULES.items():
            if key in capability:
                return value
        return "效率与质量双提升"


if __name__ == "__main__":
    mapper = OutcomeMapper()

    test_cases = [
        "AI Workflow",
        "模型调度",
        "多模型支持",
        "ci/cd",
        "缓存优化",
        "unknown_feature",
    ]

    print(f"{'技术特性':<20} {'业务能力':<25} {'业务成果'}")
    print("-" * 80)
    for feat in test_cases:
        result = mapper.map_feature_to_outcome(feat)
        print(f"{result['feature']:<20} {result['capability']:<25} {result['outcome']}")
