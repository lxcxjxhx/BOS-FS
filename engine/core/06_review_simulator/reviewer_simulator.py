"""Reviewer Simulator - Simulate different review perspectives for project evaluation."""

from typing import Dict, List, Tuple


class ReviewerSimulator:
    """Simulates technical, investment, product, open-source, and adversarial reviews.

    Each review returns per-dimension scores on a 0-10 scale,
    plus anti-sycophancy corrections and actionable suggestions.
    """

    VALID_TYPES = {"technical", "investment", "product", "opensource", "adversarial"}

    # Layer-4 state placeholder for consecutive high-score tracking
    _consecutive_high_scores: Dict[str, int] = {}

    def simulate(self, review_type: str, project_info: dict) -> dict:
        """Simulate a specific review type against project info.

        Args:
            review_type: One of VALID_TYPES.
            project_info: Dict containing project details for evaluation.

        Returns:
            Dict with dimension_scores, total_score, pass_probability,
            rejection_reasons, suggestions, sycophancy_warnings,
            hostile_questions, weakness_chain, kill_factors,
            _original_score, _defect_count.
        """
        if review_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid review_type: {review_type}. Must be one of {self.VALID_TYPES}")

        handler = getattr(self, f"_review_{review_type}")
        result = handler(project_info)

        # Apply anti-sycophancy layers after scoring
        self._apply_anti_sycophancy(result, project_info, review_type)

        if review_type == "adversarial":
            return self._finalize_adversarial(result, project_info)
        else:
            return self._finalize(result, review_type)

    # ─── Anti-Sycophancy 4 Layers ───

    def _apply_anti_sycophancy(self, result: dict, project_info: dict, review_type: str) -> None:
        """Apply 4-layer anti-sycophancy checks in-place."""

        # Layer 1 (lexical): Detect empty praise words without evidence
        EMPTY_PRAISE_WORDS = {"优秀", "完美", "出色", "一流", "极佳", "卓越"}
        input_text = " ".join(str(v) for v in project_info.values() if isinstance(v, str))
        for word in EMPTY_PRAISE_WORDS:
            if word in input_text:
                # Check if there is supporting evidence (concrete numbers, data)
                has_evidence = any(ch.isdigit() for ch in input_text)
                if not has_evidence:
                    result["_trust_penalty"] = result.get("_trust_penalty", 0) + 2
                    result["sycophancy_warnings"].append(
                        f"[反讨好-L1] 检测到空泛赞美词「{word}」但无具体证据支撑，信任度-2"
                    )

        # Layer 2 (structural): If rejection_reasons is empty but input contains "未明确"/"推断"
        if not result["rejection_reasons"]:
            if "未明确" in input_text or "推断" in input_text:
                result["rejection_reasons"].append("项目信息存在未明确或推断部分，需进一步验证")
                result["suggestions"].append("[反讨好-L2] 信息中存在推断内容，已自动标记为风险项")

        # Layer 3 (score): High-score dimension with low check coverage & low variance
        dim_scores = result["dimension_scores"]
        scores = [d["score"] for d in dim_scores.values()]
        # Check for high-score dimensions (9-10) with insufficient coverage
        for name, data in dim_scores.items():
            if data["score"] >= 9:
                # <50% "check coverage" heuristic: no concrete evidence for this dimension
                if name not in input_text or len(input_text) < 20:
                    data["score"] = 6.0
                    result["suggestions"].append(
                        f"[反讨好-L3] 维度「{name}」高分但证据覆盖不足，已降至 6.0"
                    )
        # Low variance check
        if len(scores) >= 2:
            mean_score = sum(scores) / len(scores)
            variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
            if variance < 0.5:
                result["sycophancy_warnings"].append(
                    f"[反讨好-L3] 所有维度评分方差过低({variance:.2f}<0.5)，可能未充分评估差异，建议重新评审"
                )

        # Layer 4 (pattern): Security score >=7 but no security design in input
        # Track consecutive high scores (state management placeholder)
        # self._consecutive_high_scores[review_type] = ...
        security_data = dim_scores.get("安全性", dim_scores.get("合规法律", {}))
        if isinstance(security_data, dict) and security_data.get("score", 0) >= 7:
            has_security_design = bool(project_info.get("security_design", "")) or bool(project_info.get("security_review", False))
            if not has_security_design:
                if "安全性" in dim_scores:
                    dim_scores["安全性"]["score"] = 4.0
                elif "合规法律" in dim_scores:
                    dim_scores["合规法律"]["score"] = 4.0
                result["sycophancy_warnings"].append(
                    "[反讨好-L4] 安全评分≥7但未提供安全设计，已强制降至 4.0"
                )
                result["suggestions"].append("[反讨好-L4] 请补充安全设计文档以支撑安全评分")

    # ─── _finalize ───

    @staticmethod
    def _finalize(result: dict, review_type: str) -> dict:
        """Apply non-linear defect penalty and score ceilings to review result.

        Args:
            result: Partial result dict from review method.
            review_type: The review type string.
        """
        # Recalculate weighted score from dimensions
        dim_scores = result["dimension_scores"]
        total_weight = sum(d["weight"] for d in dim_scores.values())
        weighted_sum = sum(d["score"] * d["weight"] for d in dim_scores.values())
        total_score = weighted_sum / total_weight if total_weight > 0 else 0.0

        defect_count = result.get("_defect_count", 0)
        original_score = total_score

        # Non-linear defect penalty:
        # 第 1-2 个缺陷: severity = 1.0
        # 第 3 个缺陷: severity = 1.3
        # 第 4 个缺陷: severity = 1.7
        # 第 5+ 个缺陷: severity = 2.0 + (n-5) * 0.5
        penalty = 0.0
        for i in range(1, defect_count + 1):
            if i <= 2:
                penalty += 1.0
            elif i == 3:
                penalty += 1.3
            elif i == 4:
                penalty += 1.7
            else:
                penalty += 2.0 + (i - 5) * 0.5

        # Apply penalty (scale: each severity point = 0.5 score deduction)
        score_after_penalty = total_score - penalty * 0.5
        if penalty > 0:
            result["suggestions"].append(
                f"[非线性惩罚] {defect_count}项缺陷，累计惩罚值 {penalty:.1f}，"
                f"原始 {original_score:.1f}/10 → 校正后 {max(0, score_after_penalty):.1f}/10"
            )
        total_score = max(0.0, score_after_penalty)

        # Score ceiling via defect count
        if defect_count >= 4:
            cap = 6.0
        elif defect_count >= 3:
            cap = 7.0
        elif defect_count >= 2:
            cap = 8.5
        else:
            cap = 10.0

        if total_score > cap:
            total_score = cap
            result["suggestions"].append(f"[得分上限] 缺陷数{defect_count}，得分上限 {cap:.1f}/10")

        # Generate sycophancy warnings when original_score >= 8.0 and defect_count >= 2
        sycophancy_warnings = result.get("sycophancy_warnings", [])
        if original_score >= 8.0 and defect_count >= 2:
            sycophancy_warnings.append(
                f"原始分 {original_score:.1f}/10 但存在 {defect_count} 项缺陷，"
                f"经非线性惩罚后校正至 {total_score:.1f}/10"
            )
        if original_score >= 9.0 and len(result["rejection_reasons"]) >= 1:
            sycophancy_warnings.append(
                f"高分({original_score:.1f}/10)但有硬性拒绝原因，已降档"
            )

        total_score = round(total_score, 1)
        pass_probability = round(max(0.0, min(1.0, total_score / 10)), 2)

        # Round dimension scores
        for d in dim_scores.values():
            d["score"] = round(d["score"], 1)

        return {
            "dimension_scores": dim_scores,
            "total_score": total_score,
            "pass_probability": pass_probability,
            "rejection_reasons": result["rejection_reasons"],
            "suggestions": result["suggestions"],
            "sycophancy_warnings": sycophancy_warnings,
            "hostile_questions": [],
            "weakness_chain": [],
            "kill_factors": [],
            "_original_score": round(original_score, 1),
            "_defect_count": defect_count,
        }

    # ─── _finalize_adversarial ───

    @staticmethod
    def _finalize_adversarial(result: dict, project_info: dict) -> dict:
        """Finalize adversarial review with special logic.

        Applies kill-factor rules: if ≥2 kill factors, pass_probability ≤ 0.20.
        """
        dim_scores = result["dimension_scores"]
        total_weight = sum(d["weight"] for d in dim_scores.values())
        weighted_sum = sum(d["score"] * d["weight"] for d in dim_scores.values())
        total_score = weighted_sum / total_weight if total_weight > 0 else 0.0

        kill_factors = result.get("kill_factors", [])
        if len(kill_factors) >= 2:
            # Force pass_probability ≤ 0.20
            pass_probability = min(0.20, max(0.0, total_score / 10))
        else:
            pass_probability = max(0.0, min(1.0, total_score / 10))

        total_score = round(total_score, 1)
        pass_probability = round(pass_probability, 2)

        for d in dim_scores.values():
            d["score"] = round(d["score"], 1)

        return {
            "dimension_scores": dim_scores,
            "total_score": total_score,
            "pass_probability": pass_probability,
            "rejection_reasons": result["rejection_reasons"],
            "suggestions": result["suggestions"],
            "sycophancy_warnings": result.get("sycophancy_warnings", []),
            "hostile_questions": result.get("hostile_questions", []),
            "weakness_chain": result.get("weakness_chain", []),
            "kill_factors": kill_factors,
            "_original_score": round(total_score, 1),
            "_defect_count": result.get("_defect_count", 0),
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

        dimensions = {
            "架构设计": {"score": arch_score, "weight": 25, "max": 10},
            "技术栈": {"score": stack_score, "weight": 20, "max": 10},
            "代码质量": {"score": quality_score, "weight": 25, "max": 10},
            "安全性": {"score": security_score, "weight": 15, "max": 10},
            "依赖管理": {"score": dep_score, "weight": 15, "max": 10},
        }

        return {
            "dimension_scores": dimensions,
            "total_score": 0.0,
            "pass_probability": 0.0,
            "rejection_reasons": rejection_reasons,
            "suggestions": suggestions,
            "sycophancy_warnings": [],
            "hostile_questions": [],
            "weakness_chain": [],
            "kill_factors": [],
            "_defect_count": defect_count,
        }

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

        dimensions = {
            "市场规模": {"score": market_score, "weight": 25, "max": 10},
            "ROI估算": {"score": roi_score, "weight": 25, "max": 10},
            "竞品分析": {"score": comp_score, "weight": 20, "max": 10},
            "预算规划": {"score": budget_score, "weight": 15, "max": 10},
            "时间线": {"score": timeline_score, "weight": 15, "max": 10},
        }

        return {
            "dimension_scores": dimensions,
            "total_score": 0.0,
            "pass_probability": 0.0,
            "rejection_reasons": rejection_reasons,
            "suggestions": suggestions,
            "sycophancy_warnings": [],
            "hostile_questions": [],
            "weakness_chain": [],
            "kill_factors": [],
            "_defect_count": defect_count,
        }

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

        dimensions = {
            "用户画像": {"score": persona_score, "weight": 25, "max": 10},
            "价值主张": {"score": vp_score, "weight": 25, "max": 10},
            "MVP范围": {"score": mvp_score, "weight": 15, "max": 10},
            "成功指标": {"score": metrics_score, "weight": 20, "max": 10},
            "反馈机制": {"score": feedback_score, "weight": 15, "max": 10},
        }

        return {
            "dimension_scores": dimensions,
            "total_score": 0.0,
            "pass_probability": 0.0,
            "rejection_reasons": rejection_reasons,
            "suggestions": suggestions,
            "sycophancy_warnings": [],
            "hostile_questions": [],
            "weakness_chain": [],
            "kill_factors": [],
            "_defect_count": defect_count,
        }

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

        dimensions = {
            "开源许可证": {"score": license_score, "weight": 30, "max": 10},
            "文档完整度": {"score": doc_score, "weight": 25, "max": 10},
            "贡献指引": {"score": contrib_score, "weight": 15, "max": 10},
            "行为准则": {"score": coc_score, "weight": 10, "max": 10},
            "第三方合规": {"score": tp_score, "weight": 20, "max": 10},
        }

        return {
            "dimension_scores": dimensions,
            "total_score": 0.0,
            "pass_probability": 0.0,
            "rejection_reasons": rejection_reasons,
            "suggestions": suggestions,
            "sycophancy_warnings": [],
            "hostile_questions": [],
            "weakness_chain": [],
            "kill_factors": [],
            "_defect_count": defect_count,
        }

    # ─── Adversarial Review ───

    WEAKNESS_CHAIN_MAP = {
        "无安全设计": {
            "layer1": "可能存在数据泄露风险",
            "layer2": "合规审计不通过，面临罚款",
        },
        "无竞品分析": {
            "layer1": "市场定位不清晰",
            "layer2": "商业化可行性存疑",
        },
        "架构文档缺失": {
            "layer1": "技术债可能严重",
            "layer2": "维护成本不可控",
        },
        "无测试覆盖": {
            "layer1": "代码质量不可验证",
            "layer2": "生产故障率高",
        },
        "无用户验证": {
            "layer1": "需求可能不存在",
            "layer2": "产品无人使用",
        },
        "团队背景不明": {
            "layer1": "执行能力存疑",
            "layer2": "交付延期",
        },
        "无成本估算": {
            "layer1": "商业模式不可行",
            "layer2": "资金链断裂风险",
        },
        "无退出策略": {
            "layer1": "沉没成本风险",
            "layer2": "无法安全下线",
        },
    }

    def _review_adversarial(self, info: dict) -> dict:
        """Adversarial review with hostile questions, weakness chains, and kill factors."""
        rejection_reasons: List[str] = []
        suggestions: List[str] = []
        defect_count = 0
        identified_weaknesses: List[str] = []

        # Dimensions: 技术脆弱性(20%), 商业风险(20%), 执行能力(20%), 合规法律(20%), 致命缺陷(20%)
        tech_fragility = 5.0
        biz_risk = 5.0
        exec_capability = 5.0
        compliance = 5.0
        fatal_flaw = 5.0

        score = 35  # Base score
        ceiling = 75
        floor_val = 5

        input_text = " ".join(str(v) for v in info.values() if isinstance(v, str))

        # ── Special deduction rules ──

        # "未明确" field: -20 each
        for field_name in ["architecture", "tech_stack", "security_design",
                           "competitor_analysis", "cost_estimate", "exit_strategy"]:
            val = info.get(field_name, "")
            if isinstance(val, str) and "未明确" in val:
                score -= 20
                defect_count += 1
                identified_weaknesses.append(f"{field_name}未明确")
                rejection_reasons.append(f"{field_name}信息未明确")

        # "推断" field: -10 each
        for field_name in ["architecture", "tech_stack", "security_design",
                           "competitor_analysis", "cost_estimate", "user_validation"]:
            val = info.get(field_name, "")
            if isinstance(val, str) and "推断" in val:
                score -= 10
                defect_count += 1
                identified_weaknesses.append(f"{field_name}为推断")
                suggestions.append(f"{field_name}基于推断，需实际验证")

        # No architecture diagram: -25
        architecture = info.get("architecture", "")
        has_arch_diagram = bool(info.get("architecture_diagram", "")) or (
            isinstance(architecture, str) and any(kw in architecture for kw in ["架构图", "架构图示", "diagram", "架构图纸"])
        )
        if not architecture or not has_arch_diagram:
            score -= 25
            defect_count += 1
            identified_weaknesses.append("架构文档缺失")
            rejection_reasons.append("缺乏架构设计文档")
            suggestions.append("补充系统架构图及技术设计文档")
            tech_fragility = max(1, tech_fragility - 2)

        # No competitor analysis: -20
        competitor_analysis = info.get("competitor_analysis", False)
        if not competitor_analysis and not info.get("competitor_analysis_text", ""):
            score -= 20
            defect_count += 1
            identified_weaknesses.append("无竞品分析")
            rejection_reasons.append("未提供竞品分析")
            suggestions.append("补充竞品对比和差异化定位")
            biz_risk = max(1, biz_risk - 2)

        # No security design: -20
        security_design = info.get("security_design", "")
        security_review = info.get("security_review", False)
        if not security_design and not security_review:
            score -= 20
            defect_count += 1
            identified_weaknesses.append("无安全设计")
            rejection_reasons.append("缺乏安全设计")
            suggestions.append("补充安全架构设计和威胁建模")
            compliance = max(1, compliance - 2)

        # No user validation: -15
        user_validation = info.get("user_validation", False)
        user_persona = info.get("user_persona", "")
        if not user_validation and not user_persona:
            score -= 15
            defect_count += 1
            identified_weaknesses.append("无用户验证")
            suggestions.append("进行用户调研和需求验证")
            biz_risk = max(1, biz_risk - 1)

        # No tech selection rationale: -15
        tech_stack = info.get("tech_stack", "")
        has_rationale = bool(info.get("tech_rationale", "")) or (
            isinstance(tech_stack, str) and any(kw in tech_stack for kw in ["选型", "rationale", "理由", "原因"])
        )
        if not tech_stack or not has_rationale:
            score -= 15
            defect_count += 1
            identified_weaknesses.append("无技术选型依据")
            suggestions.append("说明技术选型的权衡和依据")
            tech_fragility = max(1, tech_fragility - 1)

        # Missing quantified metrics: -10 each
        quantified_fields = ["roi_estimate", "budget", "market_size", "success_metrics", "timeline"]
        missing_metrics = 0
        for field in quantified_fields:
            val = info.get(field, "")
            if field == "success_metrics":
                if not isinstance(val, list) or len(val) == 0:
                    missing_metrics += 1
            elif field in ("budget",):
                if not val or (isinstance(val, (int, float)) and val <= 0):
                    missing_metrics += 1
            elif not val or (isinstance(val, str) and not any(ch.isdigit() for ch in val)):
                missing_metrics += 1

        if missing_metrics > 0:
            score -= missing_metrics * 10
            defect_count += missing_metrics
            identified_weaknesses.extend([f"缺少量化指标: {f}" for f in quantified_fields if f in info and not info[f]]
                                         if missing_metrics > 0 else [])
            suggestions.append(f"补充{missing_metrics}项量化指标")

        # No cost estimate
        cost_estimate = info.get("cost_estimate", "")
        if not cost_estimate:
            defect_count += 1
            identified_weaknesses.append("无成本估算")
            rejection_reasons.append("缺乏成本估算")
            suggestions.append("提供详细的项目成本估算")
            biz_risk = max(1, biz_risk - 1)

        # No exit strategy
        exit_strategy = info.get("exit_strategy", "")
        if not exit_strategy:
            defect_count += 1
            identified_weaknesses.append("无退出策略")
            suggestions.append("制定项目退出策略和降级方案")
            biz_risk = max(1, biz_risk - 1)

        # No team background
        team = info.get("team_background", "")
        if not team:
            defect_count += 1
            identified_weaknesses.append("团队背景不明")
            suggestions.append("补充团队技术背景和历史项目经验")
            exec_capability = max(1, exec_capability - 2)

        # No test coverage
        test_coverage = info.get("test_coverage", 0)
        if not test_coverage or (isinstance(test_coverage, (int, float)) and test_coverage < 30):
            defect_count += 1
            identified_weaknesses.append("无测试覆盖")
            suggestions.append("补充测试策略和覆盖率目标")
            tech_fragility = max(1, tech_fragility - 2)

        # ── Calculate dimension scores ──
        tech_fragility = max(0, min(10, tech_fragility))
        biz_risk = max(0, min(10, biz_risk))
        exec_capability = max(0, min(10, exec_capability))
        compliance = max(0, min(10, compliance))
        fatal_flaw = max(0, min(10, fatal_flaw))

        # Map score (5-75) to dimension scores
        normalized = max(0, min(1, (score - floor_val) / (ceiling - floor_val)))
        dim_base = normalized * 10

        tech_fragility = max(0, min(10, dim_base + (tech_fragility - 5)))
        biz_risk = max(0, min(10, dim_base + (biz_risk - 5)))
        exec_capability = max(0, min(10, dim_base + (exec_capability - 5)))
        compliance = max(0, min(10, dim_base + (compliance - 5)))
        fatal_flaw = max(0, min(10, dim_base + (fatal_flaw - 5)))

        dimensions = {
            "技术脆弱性": {"score": round(tech_fragility, 1), "weight": 20, "max": 10},
            "商业风险": {"score": round(biz_risk, 1), "weight": 20, "max": 10},
            "执行能力": {"score": round(exec_capability, 1), "weight": 20, "max": 10},
            "合规法律": {"score": round(compliance, 1), "weight": 20, "max": 10},
            "致命缺陷": {"score": round(fatal_flaw, 1), "weight": 20, "max": 10},
        }

        # ── Generate hostile_questions (5-8 sharp questions) ──
        hostile_questions = self._generate_hostile_questions(identified_weaknesses, info)

        # ── Generate weakness_chain ──
        weakness_chain = self._generate_weakness_chain(identified_weaknesses)

        # ── Generate kill_factors ──
        kill_factors = self._generate_kill_factors(weakness_chain, identified_weaknesses)

        return {
            "dimension_scores": dimensions,
            "total_score": 0.0,
            "pass_probability": 0.0,
            "rejection_reasons": rejection_reasons,
            "suggestions": suggestions,
            "sycophancy_warnings": [],
            "hostile_questions": hostile_questions,
            "weakness_chain": weakness_chain,
            "kill_factors": kill_factors,
            "_defect_count": defect_count,
        }

    def _generate_hostile_questions(self, weaknesses: List[str], info: dict) -> List[str]:
        """Generate 5-8 sharp questions based on project weaknesses."""
        questions: List[str] = []

        question_bank = {
            "架构文档缺失": [
                "没有架构图，你如何保证团队对系统理解一致？",
                "架构文档缺失是否意味着系统设计是临时拼凑的？",
            ],
            "无竞品分析": [
                "不做竞品分析，你如何证明你的产品有市场差异化？",
                "如果已有巨头进入这个赛道，你的护城河是什么？",
            ],
            "无安全设计": [
                "没有安全设计，用户数据泄露后谁承担责任？",
                "你的系统如何应对SQL注入、XSS等常见攻击？",
            ],
            "无测试覆盖": [
                "没有测试覆盖，你如何保证代码质量？",
                "生产环境出现P0故障时，你的应急响应机制是什么？",
            ],
            "无用户验证": [
                "没有用户验证，你如何确认需求是真实存在的而非臆想？",
                "如果上线后DAU为零，你的应对方案是什么？",
            ],
            "团队背景不明": [
                "团队没有相关领域经验，凭什么能交付这个项目？",
                "核心成员如果离职，项目能否继续？",
            ],
            "无成本估算": [
                "没有成本估算，你如何向投资人证明商业可行性？",
                "如果预算超支200%，项目还能继续吗？",
            ],
            "无退出策略": [
                "如果项目失败，如何安全下线而不影响现有用户？",
                "沉没成本达到多少时你会决定终止项目？",
            ],
            "无技术选型依据": [
                "为什么选这个技术栈而不是更成熟的替代方案？",
                "技术选型的权衡分析在哪里？",
            ],
        }

        for weakness in weaknesses:
            matched = [q for key, qs in question_bank.items() if key in weakness for q in qs]
            if matched:
                questions.extend(matched)

        # Ensure at least 5 questions, at most 8
        if len(questions) < 5:
            questions.extend([
                "这个项目的核心假设是什么？如果假设不成立怎么办？",
                "你的项目在哪些环节存在单点故障？",
                "如果主要竞争对手降价50%，你的应对策略是什么？",
            ])

        return questions[:8] if len(questions) > 8 else questions

    def _generate_weakness_chain(self, weaknesses: List[str]) -> List[dict]:
        """Generate weakness chains: original defect → layer1 → layer2."""
        chains: List[dict] = []
        for weakness in weaknesses:
            for key, chain_data in self.WEAKNESS_CHAIN_MAP.items():
                if key in weakness:
                    chains.append({
                        "original_defect": key,
                        "layer1_inferred": chain_data["layer1"],
                        "layer2_inferred": chain_data["layer2"],
                    })
                    break
        return chains

    def _generate_kill_factors(self, weakness_chain: List[dict], weaknesses: List[str]) -> List[str]:
        """Generate kill factors based on most severe weakness chains."""
        kill_factors: List[str] = []

        # At least 1 kill factor if there are weakness chains
        if weakness_chain:
            # Most severe chains (those involving compliance or fatal issues)
            severity_keywords = ["数据泄露", "合规审计", "罚款", "资金链断裂", "无人使用"]
            for chain in weakness_chain:
                for kw in severity_keywords:
                    if kw in chain["layer2_inferred"] or kw in chain["layer1_inferred"]:
                        kill_factors.append(
                            f"【致命】{chain['original_defect']} → {chain['layer1_inferred']} → {chain['layer2_inferred']}"
                        )
                        break

            # If no severity keywords matched, take the first chain
            if not kill_factors and weakness_chain:
                chain = weakness_chain[0]
                kill_factors.append(
                    f"【严重】{chain['original_defect']} → {chain['layer1_inferred']} → {chain['layer2_inferred']}"
                )

        return kill_factors


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

    for review_type in ["technical", "investment", "product", "opensource", "adversarial"]:
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
        if result.get("hostile_questions"):
            print("Hostile Questions:")
            for q in result["hostile_questions"]:
                print(f"  ❓ {q}")
        if result.get("weakness_chain"):
            print("Weakness Chains:")
            for c in result["weakness_chain"]:
                print(f"  {c['original_defect']} → {c['layer1_inferred']} → {c['layer2_inferred']}")
        if result.get("kill_factors"):
            print("Kill Factors:")
            for k in result["kill_factors"]:
                print(f"  💀 {k}")
