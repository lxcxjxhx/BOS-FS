"""Reviewer Simulator - Simulate different review perspectives for project evaluation."""

from typing import Dict, List, Tuple


class ReviewerSimulator:
    """Simulates technical, investment, product, and open-source reviews.

    Each review returns per-dimension scores on a 0-10 scale,
    plus anti-sycophancy corrections and actionable suggestions.
    """

    VALID_TYPES = {"technical", "investment", "product", "opensource"}

    def simulate(self, review_type: str, project_info: dict) -> dict:
        """Simulate a specific review type against project info.

        Args:
            review_type: One of "technical", "investment", "product", "opensource".
            project_info: Dict containing project details for evaluation.

        Returns:
            Dict with dimension_scores (0-10 per dimension), total_score,
            pass_probability, rejection_reasons, suggestions,
            sycophancy_warnings.
        """
        if review_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid review_type: {review_type}. Must be one of {self.VALID_TYPES}")

        handler = getattr(self, f"_review_{review_type}")
        return handler(project_info)

    @staticmethod
    def _finalize(dimensions: List[Tuple[str, float, float]],
                   rejection_reasons: List[str],
                   suggestions: List[str],
                   defect_count: int) -> dict:
        """Convert raw dimension scores to final review result.

        Args:
            dimensions: List of (name, score_0_10, weight).
            rejection_reasons: Hard rejection items.
            suggestions: Improvement suggestions.
            defect_count: Number of defects found.
        """
        total_weight = sum(w for _, _, w in dimensions)
        weighted_sum = sum(s * w for _, s, w in dimensions)
        total_score = weighted_sum / total_weight if total_weight > 0 else 0.0

        # Anti-sycophancy: compound penalty for multiple defects
        original_score = total_score
        if defect_count >= 4:
            penalty = defect_count * 0.3
            total_score = max(0.0, total_score - penalty)
            suggestions.append(
                f"[抗讨好] {defect_count}项缺陷，叠加扣分 {penalty:.1f}，"
                f"原始 {original_score:.1f}/10 → 校正后 {total_score:.1f}/10"
            )
        elif defect_count >= 3:
            penalty = defect_count * 0.2
            total_score = max(0.0, total_score - penalty)
            suggestions.append(
                f"[抗讨好] {defect_count}项缺陷，叠加扣分 {penalty:.1f}，"
                f"原始 {original_score:.1f}/10 → 校正后 {total_score:.1f}/10"
            )

        # Grade ceiling via score cap
        if defect_count >= 4:
            cap = 6.0
            if total_score > cap:
                total_score = cap
                suggestions.append(f"[抗讨好] 多项缺陷，得分上限 6.0/10")
        elif defect_count >= 3:
            cap = 7.0
            if total_score > cap:
                total_score = cap
                suggestions.append(f"[抗讨好] 多项缺陷，得分上限 7.0/10")
        elif defect_count >= 2:
            cap = 8.5
            if total_score > cap:
                total_score = cap
                suggestions.append(f"[抗讨好] 存在缺陷，得分上限 8.5/10")

        # Sycophancy warnings
        sycophancy_warnings: List[str] = []
        if original_score >= 8.0 and defect_count >= 2:
            sycophancy_warnings.append(
                f"原始分 {original_score:.1f}/10 但存在 {defect_count} 项缺陷，"
                f"已校正至 {total_score:.1f}/10"
            )
        if original_score >= 9.0 and len(rejection_reasons) >= 1:
            sycophancy_warnings.append(
                f"高分({original_score:.1f}/10)但有硬性拒绝原因，已降档"
            )

        # Build dimension output
        dimension_scores = {}
        for name, score, weight in dimensions:
            dimension_scores[name] = {
                "score": round(score, 1),
                "weight": weight,
                "max": 10,
            }

        pass_probability = max(0.0, min(1.0, total_score / 10))

        return {
            "dimension_scores": dimension_scores,
            "total_score": round(total_score, 1),
            "pass_probability": pass_probability,
            "rejection_reasons": rejection_reasons,
            "suggestions": suggestions,
            "sycophancy_warnings": sycophancy_warnings,
            "_original_score": round(original_score, 1),
        }

    # ─── Technical Review ───

    def _review_technical(self, info: dict) -> dict:
        rejection_reasons: List[str] = []
        suggestions: List[str] = []
        defect_count = 0

        # Architecture design (25%)
        arch_score = 10.0
        architecture = info.get("architecture", "")
        if not architecture:
            arch_score = 0.0
            defect_count += 1
            rejection_reasons.append("架构设计未说明")
            suggestions.append("补充系统架构图和模块划分说明")
        elif len(architecture) < 20:
            arch_score = 4.0
            defect_count += 1
            suggestions.append("架构描述过于简略，建议补充详细设计")
        elif len(architecture) < 50:
            arch_score = 7.0
        else:
            arch_score = 9.0

        # Tech stack (20%)
        stack_score = 10.0
        tech_stack = info.get("tech_stack", "")
        if not tech_stack:
            stack_score = 0.0
            defect_count += 1
            rejection_reasons.append("技术栈信息缺失")
            suggestions.append("明确列出使用的技术栈及版本")
        elif len(tech_stack) < 10:
            stack_score = 3.0
            defect_count += 1
            rejection_reasons.append("技术栈描述过于简略")
            suggestions.append("技术栈描述需包含具体框架和版本")
        elif len(tech_stack) < 30:
            stack_score = 6.0
        else:
            stack_score = 9.0

        # Code quality / test coverage (25%)
        tests = info.get("test_coverage", 0)
        if tests >= 80:
            quality_score = 9.0
        elif tests >= 60:
            quality_score = 7.0
        elif tests >= 30:
            quality_score = 4.0
        else:
            quality_score = 1.0
            defect_count += 1
        if tests < 60:
            suggestions.append(f"测试覆盖率当前{tests}%，建议提升至80%以上")

        # Security (15%)
        security = info.get("security_review", False)
        if security:
            security_score = 9.0
        else:
            security_score = 3.0
            defect_count += 1
            suggestions.append("建议补充安全审计环节")

        # Dependency management (15%)
        dependencies = info.get("dependencies", [])
        if len(dependencies) == 0:
            dep_score = 5.0
            suggestions.append("未声明项目依赖")
        elif len(dependencies) <= 10:
            dep_score = 9.0
        elif len(dependencies) <= 20:
            dep_score = 7.0
        else:
            dep_score = 4.0
            defect_count += 1
            suggestions.append("依赖过多，建议精简核心依赖")

        dimensions = [
            ("架构设计", arch_score, 25),
            ("技术栈", stack_score, 20),
            ("代码质量", quality_score, 25),
            ("安全性", security_score, 15),
            ("依赖管理", dep_score, 15),
        ]

        return self._finalize(dimensions, rejection_reasons, suggestions, defect_count)

    # ─── Investment Review ───

    def _review_investment(self, info: dict) -> dict:
        rejection_reasons: List[str] = []
        suggestions: List[str] = []
        defect_count = 0

        # Market size (25%)
        market_score = 10.0
        market_size = info.get("market_size", "")
        if not market_size:
            market_score = 0.0
            defect_count += 1
            rejection_reasons.append("市场规模数据缺失")
            suggestions.append("补充目标市场规模和增长预测数据")
        elif len(market_size) < 5:
            market_score = 3.0
            defect_count += 1
            suggestions.append("市场规模描述过于模糊，需要具体数据支撑")
        elif len(market_size) < 20:
            market_score = 6.0
        else:
            market_score = 8.0

        # ROI estimate (25%)
        roi_score = 10.0
        roi = info.get("roi_estimate", "")
        if not roi:
            roi_score = 0.0
            defect_count += 1
            rejection_reasons.append("ROI估算未提供")
            suggestions.append("提供详细的投资回报分析")
        elif len(roi) < 10:
            roi_score = 4.0
            defect_count += 1
            suggestions.append("ROI估算过于简略，需要详细分析")
        else:
            roi_score = 8.0

        # Competitor analysis (20%)
        competitors = info.get("competitor_analysis", False)
        if competitors:
            comp_score = 8.0
        else:
            comp_score = 2.0
            defect_count += 1
            rejection_reasons.append("缺少竞品分析")
            suggestions.append("补充竞品对比和差异化定位")

        # Budget (15%)
        budget = info.get("budget", 0)
        if budget > 100000:
            budget_score = 8.0
        elif budget > 0:
            budget_score = 5.0
        else:
            budget_score = 1.0
            defect_count += 1
            suggestions.append("明确项目预算和资金规划")

        # Timeline (15%)
        timeline_score = 10.0
        timeline = info.get("timeline", "")
        if not timeline:
            timeline_score = 2.0
            defect_count += 1
            suggestions.append("提供清晰的项目里程碑和时间线")
        elif len(timeline) < 10:
            timeline_score = 5.0
        else:
            timeline_score = 8.0

        dimensions = [
            ("市场规模", market_score, 25),
            ("ROI估算", roi_score, 25),
            ("竞品分析", comp_score, 20),
            ("预算规划", budget_score, 15),
            ("时间线", timeline_score, 15),
        ]

        return self._finalize(dimensions, rejection_reasons, suggestions, defect_count)

    # ─── Product Review ───

    def _review_product(self, info: dict) -> dict:
        rejection_reasons: List[str] = []
        suggestions: List[str] = []
        defect_count = 0

        # User persona (25%)
        persona_score = 10.0
        user_persona = info.get("user_persona", "")
        if not user_persona:
            persona_score = 0.0
            defect_count += 1
            rejection_reasons.append("目标用户画像不清晰")
            suggestions.append("明确定义目标用户群体和使用场景")
        elif len(user_persona) < 10:
            persona_score = 4.0
            defect_count += 1
            suggestions.append("用户画像过于简略，需要详细描述")
        elif len(user_persona) < 30:
            persona_score = 7.0
        else:
            persona_score = 9.0

        # Value proposition (25%)
        vp_score = 10.0
        value_proposition = info.get("value_proposition", "")
        if not value_proposition:
            vp_score = 0.0
            defect_count += 1
            rejection_reasons.append("核心价值主张缺失")
            suggestions.append("清晰表述产品为用户解决的核心问题")
        elif len(value_proposition) < 10:
            vp_score = 3.0
            defect_count += 1
            suggestions.append("价值主张过于简短，需要更详细的表述")
        elif len(value_proposition) < 30:
            vp_score = 6.0
        else:
            vp_score = 9.0

        # MVP scope (15%)
        mvp_score = 10.0
        mvp_scope = info.get("mvp_scope", "")
        if not mvp_scope:
            mvp_score = 2.0
            defect_count += 1
            suggestions.append("定义最小可行产品(MVP)范围")
        elif len(mvp_scope) < 10:
            mvp_score = 5.0
        else:
            mvp_score = 8.0

        # Success metrics (20%)
        metrics = info.get("success_metrics", [])
        if len(metrics) >= 3:
            metrics_score = 9.0
        elif len(metrics) >= 1:
            metrics_score = 6.0
        else:
            metrics_score = 1.0
            defect_count += 1
            rejection_reasons.append("缺少成功指标定义")
            suggestions.append("设定可量化的产品成功指标")

        # Feedback mechanism (15%)
        feedback = info.get("feedback_mechanism", False)
        if feedback:
            feedback_score = 8.0
        else:
            feedback_score = 2.0
            defect_count += 1
            suggestions.append("建立用户反馈收集和迭代机制")

        dimensions = [
            ("用户画像", persona_score, 25),
            ("价值主张", vp_score, 25),
            ("MVP范围", mvp_score, 15),
            ("成功指标", metrics_score, 20),
            ("反馈机制", feedback_score, 15),
        ]

        return self._finalize(dimensions, rejection_reasons, suggestions, defect_count)

    # ─── Open Source Review ───

    def _review_opensource(self, info: dict) -> dict:
        rejection_reasons: List[str] = []
        suggestions: List[str] = []
        defect_count = 0

        # License (30%)
        license_score = 10.0
        license_type = info.get("license", "")
        if not license_type:
            license_score = 0.0
            defect_count += 1
            rejection_reasons.append("未声明开源许可证")
            suggestions.append("选择合适的开源许可证(如MIT/Apache-2.0/GPL)")
        elif license_type.upper() in ("MIT", "APACHE-2.0", "BSD-2-CLAUSE", "BSD-3-CLAUSE", "ISC"):
            license_score = 10.0
        elif license_type.upper() in ("GPL-2.0", "GPL-3.0", "LGPL", "MPL-2.0"):
            license_score = 8.0
        else:
            license_score = 5.0
            suggestions.append(f"许可证 '{license_type}' 不常见，建议确认合规性")

        # Documentation (25%)
        documentation = info.get("documentation", False)
        if documentation:
            doc_score = 8.0
        else:
            doc_score = 1.0
            defect_count += 1
            rejection_reasons.append("文档不完整")
            suggestions.append("补充README、安装指南和API文档")

        # Contributing guide (15%)
        contrib = info.get("contributing_guide", False)
        if contrib:
            contrib_score = 9.0
        else:
            contrib_score = 2.0
            defect_count += 1
            suggestions.append("添加CONTRIBUTING.md指引贡献者")

        # Code of conduct (10%)
        coc = info.get("code_of_conduct", False)
        if coc:
            coc_score = 9.0
        else:
            coc_score = 2.0
            defect_count += 1
            suggestions.append("添加行为准则(CODE_OF_CONDUCT.md)")

        # Third-party licenses (20%)
        third_party = info.get("third_party_licenses", [])
        if len(third_party) >= 3:
            tp_score = 9.0
        elif len(third_party) >= 1:
            tp_score = 6.0
        else:
            tp_score = 1.0
            defect_count += 1
            suggestions.append("声明第三方依赖及其许可证兼容性")

        dimensions = [
            ("开源许可证", license_score, 30),
            ("文档完整度", doc_score, 25),
            ("贡献指引", contrib_score, 15),
            ("行为准则", coc_score, 10),
            ("第三方合规", tp_score, 20),
        ]

        return self._finalize(dimensions, rejection_reasons, suggestions, defect_count)


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

    for review_type in ["technical", "investment", "product", "opensource"]:
        result = simulator.simulate(review_type, sample_project)
        print(f"\n{'='*50}")
        print(f"Review Type: {review_type.upper()}")
        print(f"Total Score: {result['total_score']:.1f}/10")
        print(f"Pass Probability: {result['pass_probability']:.0%}")
        print("Dimension Scores:")
        for dim_name, dim_data in result["dimension_scores"].items():
            print(f"  {dim_name}: {dim_data['score']}/{dim_data['max']} (weight: {dim_data['weight']}%)")
        if result["rejection_reasons"]:
            print(f"Rejection: {', '.join(result['rejection_reasons'])}")
        if result["suggestions"]:
            print("Suggestions:")
            for s in result["suggestions"]:
                print(f"  - {s}")
        if result["sycophancy_warnings"]:
            print("Anti-Sycophancy Warnings:")
            for w in result["sycophancy_warnings"]:
                print(f"  ⚠ {w}")
