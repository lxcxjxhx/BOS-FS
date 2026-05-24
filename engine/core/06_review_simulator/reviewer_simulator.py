"""Reviewer Simulator - Simulate different review perspectives for project evaluation."""

from typing import Dict, List


class ReviewerSimulator:
    """Simulates technical, investment, product, and open-source reviews."""

    VALID_TYPES = {"technical", "investment", "product", "opensource"}

    def simulate(self, review_type: str, project_info: dict) -> dict:
        """Simulate a specific review type against project info.
        
        Args:
            review_type: One of "technical", "investment", "product", "opensource".
            project_info: Dict containing project details for evaluation.
            
        Returns:
            Dict with pass_probability, rejection_reasons, suggestions.
        """
        if review_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid review_type: {review_type}. Must be one of {self.VALID_TYPES}")
        
        handler = getattr(self, f"_review_{review_type}")
        return handler(project_info)

    def _review_technical(self, info: dict) -> dict:
        rejection_reasons: List[str] = []
        suggestions: List[str] = []
        score = 100.0

        tech_stack = info.get("tech_stack", "")
        if not tech_stack:
            score -= 20
            rejection_reasons.append("技术栈信息缺失")
            suggestions.append("明确列出使用的技术栈及版本")

        architecture = info.get("architecture", "")
        if not architecture:
            score -= 15
            rejection_reasons.append("架构设计未说明")
            suggestions.append("补充系统架构图和模块划分说明")

        tests = info.get("test_coverage", 0)
        if tests < 60:
            score -= (60 - tests) * 0.5
            suggestions.append(f"测试覆盖率当前{tests}%，建议提升至80%以上")

        dependencies = info.get("dependencies", [])
        if len(dependencies) > 20:
            score -= 10
            suggestions.append("依赖过多，建议精简核心依赖")

        security = info.get("security_review", False)
        if not security:
            score -= 10
            suggestions.append("建议补充安全审计环节")

        return {
            "pass_probability": max(0.0, min(1.0, score / 100)),
            "rejection_reasons": rejection_reasons,
            "suggestions": suggestions,
        }

    def _review_investment(self, info: dict) -> dict:
        rejection_reasons: List[str] = []
        suggestions: List[str] = []
        score = 100.0

        market_size = info.get("market_size", "")
        if not market_size:
            score -= 20
            rejection_reasons.append("市场规模数据缺失")
            suggestions.append("补充目标市场规模和增长预测数据")

        roi = info.get("roi_estimate", "")
        if not roi:
            score -= 20
            rejection_reasons.append("ROI估算未提供")
            suggestions.append("提供详细的投资回报分析")

        competitors = info.get("competitor_analysis", False)
        if not competitors:
            score -= 15
            rejection_reasons.append("缺少竞品分析")
            suggestions.append("补充竞品对比和差异化定位")

        budget = info.get("budget", 0)
        if budget <= 0:
            score -= 15
            suggestions.append("明确项目预算和资金规划")

        timeline = info.get("timeline", "")
        if not timeline:
            score -= 10
            suggestions.append("提供清晰的项目里程碑和时间线")

        return {
            "pass_probability": max(0.0, min(1.0, score / 100)),
            "rejection_reasons": rejection_reasons,
            "suggestions": suggestions,
        }

    def _review_product(self, info: dict) -> dict:
        rejection_reasons: List[str] = []
        suggestions: List[str] = []
        score = 100.0

        user_persona = info.get("user_persona", "")
        if not user_persona:
            score -= 20
            rejection_reasons.append("目标用户画像不清晰")
            suggestions.append("明确定义目标用户群体和使用场景")

        value_proposition = info.get("value_proposition", "")
        if not value_proposition:
            score -= 20
            rejection_reasons.append("核心价值主张缺失")
            suggestions.append("清晰表述产品为用户解决的核心问题")

        mvp_scope = info.get("mvp_scope", "")
        if not mvp_scope:
            score -= 15
            suggestions.append("定义最小可行产品(MVP)范围")

        metrics = info.get("success_metrics", [])
        if not metrics:
            score -= 15
            rejection_reasons.append("缺少成功指标定义")
            suggestions.append("设定可量化的产品成功指标")

        feedback_loop = info.get("feedback_mechanism", False)
        if not feedback_loop:
            score -= 10
            suggestions.append("建立用户反馈收集和迭代机制")

        return {
            "pass_probability": max(0.0, min(1.0, score / 100)),
            "rejection_reasons": rejection_reasons,
            "suggestions": suggestions,
        }

    def _review_opensource(self, info: dict) -> dict:
        rejection_reasons: List[str] = []
        suggestions: List[str] = []
        score = 100.0

        license_type = info.get("license", "")
        if not license_type:
            score -= 25
            rejection_reasons.append("未声明开源许可证")
            suggestions.append("选择合适的开源许可证(如MIT/Apache-2.0/GPL)")

        documentation = info.get("documentation", False)
        if not documentation:
            score -= 15
            rejection_reasons.append("文档不完整")
            suggestions.append("补充README、安装指南和API文档")

        contributing_guide = info.get("contributing_guide", False)
        if not contributing_guide:
            score -= 10
            suggestions.append("添加CONTRIBUTING.md指引贡献者")

        code_of_conduct = info.get("code_of_conduct", False)
        if not code_of_conduct:
            score -= 10
            suggestions.append("添加行为准则(CODE_OF_CONDUCT.md)")

        third_party_deps = info.get("third_party_licenses", [])
        if not third_party_deps:
            score -= 10
            suggestions.append("声明第三方依赖及其许可证兼容性")

        return {
            "pass_probability": max(0.0, min(1.0, score / 100)),
            "rejection_reasons": rejection_reasons,
            "suggestions": suggestions,
        }


if __name__ == "__main__":
    simulator = ReviewerSimulator()
    
    sample_project = {
        "tech_stack": "Python 3.11, FastAPI, PostgreSQL, React",
        "architecture": "微服务架构，前后端分离",
        "test_coverage": 45,
        "dependencies": ["fastapi", "sqlalchemy", "pytest", "react"],
        "security_review": False,
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
        "contributing_guide": False,
        "code_of_conduct": False,
        "third_party_licenses": [],
    }
    
    import json
    
    for review_type in ["technical", "investment", "product", "opensource"]:
        result = simulator.simulate(review_type, sample_project)
        print(f"\n{'='*50}")
        print(f"Review Type: {review_type.upper()}")
        print(f"Pass Probability: {result['pass_probability']:.0%}")
        if result['rejection_reasons']:
            print(f"Rejection Reasons: {', '.join(result['rejection_reasons'])}")
        if result['suggestions']:
            print("Suggestions:")
            for s in result['suggestions']:
                print(f"  - {s}")
