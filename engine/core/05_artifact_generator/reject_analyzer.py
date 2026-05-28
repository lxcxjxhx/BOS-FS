"""Reject Analyzer - Analyze rejection reasons and generate fixable suggestions."""

import re
from typing import Dict, List


class RejectAnalyzer:
    """Analyzes rejection text, matches rejection patterns, and generates actionable fixes."""

    REJECTION_PATTERNS = [
        {
            "name": "表达太底层",
            "keywords": ["底层", "技术", "实现", "看不出", "用户价值", "feature", "功能", "工具", "技术语言"],
            "real_issue": "技术语言替代了价值表达",
            "fixable_items": [
                "将技术描述转为用户价值描述（Feature→Capability→Outcome）",
                "补充用户使用场景描述",
                "增加可量化效果指标",
            ],
            "suggestion": "从'交付工具'重新定位为'交付平台'，强调自动化和效率提升",
        },
        {
            "name": "目标不明确",
            "keywords": ["不清楚", "解决什么", "问题", "目标", "不明确", "缺少场景", "定位", "用途", "干什么"],
            "real_issue": "缺少场景定位",
            "fixable_items": [
                "补充目标用户（persona）描述",
                "明确要解决的核心问题（problem）",
                "给出具体解决方案（solution）",
            ],
            "suggestion": "补充persona/problem/solution三要素，明确场景定位",
        },
        {
            "name": "差异化不足",
            "keywords": ["又一个", "同类", "类似", "差异", "独特", "竞品", "区别", "不同", "特色", "优势", "特别"],
            "real_issue": "未突出独特价值主张",
            "fixable_items": [
                "明确与竞品的核心差异点",
                "突出项目的独特定位",
                "补充竞品对比分析表",
            ],
            "suggestion": "强调差异化定位，补充竞品对比和独特价值主张",
        },
        {
            "name": "文档不完整",
            "keywords": ["缺少", "文档", "安装", "说明", "README", "Demo", "指南", "交付物", "不全", "使用"],
            "real_issue": "交付物不全",
            "fixable_items": [
                "补齐README（What/Why/How/Result/Next）",
                "补充Demo Guide和快速开始指南",
                "完善安装、配置、运行说明",
            ],
            "suggestion": "补齐完整文档体系，确保交付物齐全可验证",
        },
        {
            "name": "安全风险",
            "keywords": ["安全", "数据", "隐私", "泄露", "权限", "漏洞", "加密", "保护", "风险评估"],
            "real_issue": "缺少安全设计",
            "fixable_items": [
                "补充安全评估报告",
                "说明数据存储和传输加密方案",
                "明确权限控制策略",
            ],
            "suggestion": "补充安全设计文档，涵盖数据安全、隐私保护和权限控制",
        },
        {
            "name": "价值模糊",
            "keywords": ["看不出", "优势", "价值", "模糊", "量化", "指标", "收益", "效果", "回报", "ROI"],
            "real_issue": "未做竞品对比和量化分析",
            "fixable_items": [
                "补充竞品对比分析",
                "增加可量化价值指标",
                "明确投入产出比（ROI）",
            ],
            "suggestion": "补充竞品对比+量化指标，明确项目价值主张",
        },
        {
            "name": "场景缺失",
            "keywords": ["场景", "用户故事", "什么时候", "什么时候用", "用例", "使用场景", "实际应用", "真实"],
            "real_issue": "缺少用户故事和真实场景",
            "fixable_items": [
                "补充2-3个真实用户使用场景",
                "编写用户故事（User Story）",
                "说明典型使用流程和触发条件",
            ],
            "suggestion": "补充2-3个真实场景，让评审者理解项目适用边界",
        },
        {
            "name": "路线图不清",
            "keywords": ["规划", "路线图", "清晰", "路径", "执行", "里程碑", "阶段", "近期", "中期", "远期", "未来"],
            "real_issue": "缺少执行路径和里程碑",
            "fixable_items": [
                "制定近期/中期/远期规划",
                "明确各阶段里程碑和交付物",
                "说明资源需求和优先级",
            ],
            "suggestion": "制定清晰的近期/中期/远期路线图，包含可验证的里程碑",
        },
        {
            "name": "技术可行性",
            "keywords": ["可行", "复杂", "架构", "PoC", "验证", "方案", "不匹配", "过度", "过度设计", "技术风险"],
            "real_issue": "方案复杂度过高或缺乏验证",
            "fixable_items": [
                "简化架构设计，降低复杂度",
                "提供概念验证（PoC）演示",
                "补充技术可行性分析",
            ],
            "suggestion": "简化架构，提供PoC验证技术可行性，降低评审风险",
        },
        {
            "name": "合规问题",
            "keywords": ["许可证", "合规", "license", "声明", "数据", "开源", "版权", "授权", "法律", "协议"],
            "real_issue": "缺少合规声明和许可证信息",
            "fixable_items": [
                "补充明确的许可证声明",
                "说明数据来源和使用合规性",
                "补充第三方依赖许可证检查",
            ],
            "suggestion": "补充许可证声明和数据合规说明，确保法律合规",
        },
        {
            "name": "数据隐私缺失",
            "keywords": ["数据隐私", "隐私保护", "个人信息", "合规", "GDPR", "数据安全"],
            "real_issue": "缺少数据隐私保护设计",
            "fixable_items": [
                "补充数据收集和使用声明",
                "说明个人信息加密和匿名化方案",
                "明确数据保留和删除策略",
            ],
            "suggestion": "补充数据隐私保护方案，确保符合GDPR等法规要求",
        },
        {
            "name": "可扩展性陷阱",
            "keywords": ["扩展性", "并发", "性能瓶颈", "扩展", "scale", "并发量"],
            "real_issue": "架构设计未考虑可扩展性",
            "fixable_items": [
                "补充性能基准测试数据",
                "说明水平/垂直扩展策略",
                "识别潜在性能瓶颈及优化方案",
            ],
            "suggestion": "补充扩展性分析和性能规划，确保系统可应对增长",
        },
        {
            "name": "技术债务隐瞒",
            "keywords": ["技术债", "重构", "历史包袱", "技术债务", "legacy", "维护成本"],
            "real_issue": "未识别和规划技术债务",
            "fixable_items": [
                "列出已知技术债务清单",
                "制定技术债务偿还计划",
                "评估维护成本和重构优先级",
            ],
            "suggestion": "透明化技术债务，制定偿还计划降低长期风险",
        },
        {
            "name": "用户验证空白",
            "keywords": ["用户验证", "需求验证", "用户调研", "市场验证", "validation", "PMF"],
            "real_issue": "缺乏用户验证和市场反馈",
            "fixable_items": [
                "补充用户调研数据和反馈",
                "提供MVP验证结果",
                "说明产品市场匹配度（PMF）评估",
            ],
            "suggestion": "补充用户验证数据，证明需求真实存在",
        },
        {
            "name": "依赖风险",
            "keywords": ["依赖", "第三方", "供应链", "dependency", "supply chain"],
            "real_issue": "未评估第三方依赖风险",
            "fixable_items": [
                "列出核心第三方依赖清单",
                "评估依赖项目的活跃度和稳定性",
                "制定替代方案和降级策略",
            ],
            "suggestion": "评估供应链风险，确保关键依赖可控",
        },
        {
            "name": "运维盲区",
            "keywords": ["运维", "监控", "告警", "SRE", "on-call", "可用性"],
            "real_issue": "缺少运维和监控设计",
            "fixable_items": [
                "补充监控和告警策略",
                "说明日志记录和故障排查方案",
                "定义SLA/SLO指标",
            ],
            "suggestion": "补充运维方案，确保系统可观测和可维护",
        },
        {
            "name": "国际化缺失",
            "keywords": ["国际化", "i18n", "多语言", "本地化", "l10n", "全球化"],
            "real_issue": "未考虑国际化和本地化",
            "fixable_items": [
                "评估多语言支持需求",
                "说明i18n/l10n技术方案",
                "识别区域化差异和合规要求",
            ],
            "suggestion": "评估国际化需求，规划多语言支持方案",
        },
        {
            "name": "无障碍合规",
            "keywords": ["无障碍", "a11y", "accessibility", "WCAG", "残障", "辅助功能"],
            "real_issue": "未考虑无障碍设计",
            "fixable_items": [
                "评估WCAG合规级别",
                "补充无障碍功能清单",
                "说明辅助技术支持方案",
            ],
            "suggestion": "补充无障碍设计，确保产品对残障用户友好",
        },
        {
            "name": "成本控制缺失",
            "keywords": ["成本", "预算", "ROI", "盈利", "成本效益", "cost"],
            "real_issue": "未进行成本效益分析",
            "fixable_items": [
                "补充成本估算和预算规划",
                "明确盈利模式和ROI计算",
                "分析不同规模下的成本变化",
            ],
            "suggestion": "补充成本效益分析，确保项目经济可行",
        },
        {
            "name": "退出策略缺失",
            "keywords": ["退出", "下线", "迁移", "退出策略", "rollback", "deprecation"],
            "real_issue": "缺少项目退出和迁移方案",
            "fixable_items": [
                "制定项目下线/迁移预案",
                "说明数据备份和迁移策略",
                "定义弃用(deprecation)流程",
            ],
            "suggestion": "补充退出策略，确保项目生命周期完整可控",
        },
    ]

    CHECKLIST_ITEMS = {
        "readme_clear": ["README", "说明", "文档", "What", "Why", "How"],
        "has_scenarios": ["场景", "用例", "故事", "用户", "实际"],
        "has_metrics": ["指标", "量化", "提升", "降低", "%", "率", "效率", "成本"],
        "has_risk_disclosure": ["风险", "安全", "合规", "限制", "注意"],
        "has_competitor_comparison": ["竞品", "对比", "差异", "优势", "同类"],
        "docs_complete": ["安装", "配置", "运行", "验证", "Demo", "示例"],
        "compliance_clear": ["许可证", "license", "合规", "声明", "开源", "版权"],
    }

    KEYWORD_MAP = {
        "表达太底层": ["底层", "技术", "实现", "看不出", "用户价值", "feature", "功能", "工具", "技术语言"],
        "目标不明确": ["不清楚", "解决什么", "问题", "目标", "不明确", "缺少场景", "定位", "用途", "干什么"],
        "差异化不足": ["又一个", "同类", "类似", "差异", "独特", "竞品", "区别", "不同", "特色", "优势", "特别"],
        "文档不完整": ["缺少", "文档", "安装", "说明", "README", "Demo", "指南", "交付物", "不全", "使用"],
        "安全风险": ["安全", "数据", "隐私", "泄露", "权限", "漏洞", "加密", "保护", "风险评估"],
        "价值模糊": ["看不出", "优势", "价值", "模糊", "量化", "指标", "收益", "效果", "回报", "ROI"],
        "场景缺失": ["场景", "用户故事", "什么时候", "什么时候用", "用例", "使用场景", "实际应用", "真实"],
        "路线图不清": ["规划", "路线图", "清晰", "路径", "执行", "里程碑", "阶段", "近期", "中期", "远期", "未来"],
        "技术可行性": ["可行", "复杂", "架构", "PoC", "验证", "方案", "不匹配", "过度", "过度设计", "技术风险"],
        "合规问题": ["许可证", "合规", "license", "声明", "数据", "开源", "版权", "授权", "法律", "协议"],
        "数据隐私缺失": ["数据隐私", "隐私保护", "个人信息", "合规", "GDPR", "数据安全"],
        "可扩展性陷阱": ["扩展性", "并发", "性能瓶颈", "扩展", "scale", "并发量"],
        "技术债务隐瞒": ["技术债", "重构", "历史包袱", "技术债务", "legacy", "维护成本"],
        "用户验证空白": ["用户验证", "需求验证", "用户调研", "市场验证", "validation", "PMF"],
        "依赖风险": ["依赖", "第三方", "供应链", "dependency", "supply chain"],
        "运维盲区": ["运维", "监控", "告警", "SRE", "on-call", "可用性"],
        "国际化缺失": ["国际化", "i18n", "多语言", "本地化", "l10n", "全球化"],
        "无障碍合规": ["无障碍", "a11y", "accessibility", "WCAG", "残障", "辅助功能"],
        "成本控制缺失": ["成本", "预算", "ROI", "盈利", "成本效益", "cost"],
        "退出策略缺失": ["退出", "下线", "迁移", "退出策略", "rollback", "deprecation"],
    }

    def analyze(self, rejection_text: str) -> Dict:
        """Analyze rejection text and return structured analysis result.

        Args:
            rejection_text: Raw rejection reason text.

        Returns:
            Dict with keys: real_issue, fixable_items, resubmit_suggestion,
            matched_pattern, confidence, checklist_results, root_cause_tree.
        """
        text = rejection_text.strip()

        if not text:
            return self._empty_result()

        matched = self._match_pattern(text)
        real_issue = self._extract_real_issue(matched, text)
        fixable_items = self._generate_fixable_items(matched)
        suggestion = self._generate_suggestion(matched)
        confidence = self._calculate_confidence(text, matched)
        checklist = self._run_checklist(text)
        root_cause_tree = self._build_root_cause_tree(matched["name"], real_issue)

        result = {
            "real_issue": real_issue,
            "fixable_items": fixable_items,
            "resubmit_suggestion": suggestion,
            "matched_pattern": matched["name"],
            "confidence": round(confidence, 2),
            "checklist_results": checklist,
            "root_cause_tree": root_cause_tree,
        }

        if confidence < 0.5:
            result["resubmit_suggestion"] += "（低置信度，建议人工复核）"

        return result

    def _match_pattern(self, text: str) -> Dict:
        """Match rejection text to the best-fitting rejection pattern.

        Args:
            text: Cleaned rejection text.

        Returns:
            The best-matching pattern dict.
        """
        best_pattern = None
        best_score = 0.0

        for pattern in self.REJECTION_PATTERNS:
            score = self._calculate_confidence(text, pattern)
            if score > best_score:
                best_score = score
                best_pattern = pattern

        # Fallback to first pattern if no match found
        if best_pattern is None or best_score == 0.0:
            best_pattern = self.REJECTION_PATTERNS[0]

        return best_pattern

    def _extract_real_issue(self, matched_pattern: Dict, text: str) -> str:
        """Extract root cause from matched pattern and rejection text.

        Args:
            matched_pattern: The matched rejection pattern dict.
            text: Original rejection text.

        Returns:
            Root cause description string.
        """
        base_issue = matched_pattern["real_issue"]

        # Enrich with context from rejection text if available
        text_lower = text.lower()
        if any(kw in text_lower for kw in ["价值", "优势", "意义"]):
            return f"{base_issue}，未充分体现项目对用户/业务的实际价值"
        if any(kw in text_lower for kw in ["说明", "文档", "信息"]):
            return f"{base_issue}，关键信息表达不充分"

        return base_issue

    def _generate_fixable_items(self, matched_pattern: Dict) -> List[str]:
        """Generate actionable fix items from matched pattern.

        Args:
            matched_pattern: The matched rejection pattern dict.

        Returns:
            List of actionable fix strings.
        """
        return list(matched_pattern["fixable_items"])

    def _generate_suggestion(self, matched_pattern: Dict) -> str:
        """Generate resubmit strategy suggestion from matched pattern.

        Args:
            matched_pattern: The matched rejection pattern dict.

        Returns:
            Resubmit suggestion string.
        """
        return matched_pattern["suggestion"]

    def _calculate_confidence(self, text: str, pattern: Dict) -> float:
        """Calculate match confidence based on keyword overlap.

        Args:
            text: Rejection text to evaluate.
            pattern: Pattern dict with keywords list.

        Returns:
            Confidence score between 0.0 and 1.0.
        """
        text_lower = text.lower()
        keywords = pattern.get("keywords", [])

        if not keywords:
            return 0.0

        matched_count = sum(1 for kw in keywords if kw.lower() in text_lower)
        overlap_ratio = matched_count / len(keywords)

        # Scale: at least 1 keyword match gives baseline confidence
        if matched_count == 0:
            return 0.0

        # Non-linear scaling: more matches → diminishing returns
        confidence = min(0.3 + 0.7 * (matched_count / max(len(keywords), 1)), 1.0)

        # Bonus if pattern name appears in text
        if pattern["name"] in text:
            confidence = min(confidence + 0.15, 1.0)

        return confidence

    def _run_checklist(self, text: str) -> Dict:
        """Run general checklist against rejection text.

        Args:
            text: Rejection text to evaluate.

        Returns:
            Dict with checklist_results boolean values.
        """
        text_lower = text.lower()
        results = {}

        for item_name, keywords in self.CHECKLIST_ITEMS.items():
            found = any(kw.lower() in text_lower for kw in keywords)
            results[item_name] = found

        return results

    def _build_root_cause_tree(self, pattern_name: str, description: str) -> Dict[str, str]:
        """Build a 3-layer root cause analysis tree.

        Args:
            pattern_name: The matched rejection pattern name.
            description: The real issue description.

        Returns:
            Dict with keys: surface, primary, secondary, fix_path.
        """
        surface = description[:50] if len(description) > 50 else description

        root_cause_mapping = {
            "表达太底层": {
                "primary": "交付文档未聚焦用户价值",
                "secondary": "缺乏以用户为中心的设计思维",
                "fix_path": "从用户场景出发重写问题定义，用业务价值替代技术描述",
            },
            "目标不明确": {
                "primary": "交付文档未明确场景定位",
                "secondary": "缺乏问题定义和范围界定能力",
                "fix_path": "补充persona/problem/solution三要素，明确项目边界",
            },
            "差异化不足": {
                "primary": "交付文档未突出独特价值主张",
                "secondary": "缺乏竞品分析和市场定位意识",
                "fix_path": "补充竞品对比分析，明确差异化定位和核心优势",
            },
            "文档不完整": {
                "primary": "交付物体系不完整",
                "secondary": "缺乏工程化和标准化交付意识",
                "fix_path": "建立标准文档模板（What/Why/How/Result/Next），逐项补齐",
            },
            "安全风险": {
                "primary": "交付文档缺少安全设计说明",
                "secondary": "安全左移意识不足，未在设计阶段考虑安全",
                "fix_path": "补充安全评估报告，涵盖数据安全、隐私保护和权限控制",
            },
            "价值模糊": {
                "primary": "交付文档未做竞品对比和量化分析",
                "secondary": "缺乏数据驱动的价值验证方法",
                "fix_path": "补充竞品对比+量化指标，明确项目价值主张和ROI",
            },
            "场景缺失": {
                "primary": "交付文档缺少用户故事和真实场景",
                "secondary": "脱离实际用户需求，缺乏场景化思考",
                "fix_path": "补充2-3个真实场景，让评审者理解项目适用边界",
            },
            "路线图不清": {
                "primary": "交付文档缺少执行路径和里程碑",
                "secondary": "缺乏项目管理和阶段性规划能力",
                "fix_path": "制定清晰的近期/中期/远期路线图，包含可验证的里程碑",
            },
            "技术可行性": {
                "primary": "交付方案复杂度过高或缺乏验证",
                "secondary": "技术方案脱离实际需求，过度设计",
                "fix_path": "简化架构，提供PoC验证技术可行性，降低评审风险",
            },
            "合规问题": {
                "primary": "交付文档缺少合规声明和许可证信息",
                "secondary": "法律合规意识不足，忽视开源协议约束",
                "fix_path": "补充许可证声明和数据合规说明，确保法律合规",
            },
            "数据隐私缺失": {
                "primary": "交付文档未体现数据隐私保护设计",
                "secondary": "隐私合规意识不足，未将数据保护纳入架构设计",
                "fix_path": "补充数据隐私保护方案，明确数据收集/使用/删除策略，确保符合GDPR等法规",
            },
            "可扩展性陷阱": {
                "primary": "架构设计未考虑系统可扩展性",
                "secondary": "缺乏容量规划和性能工程思维",
                "fix_path": "补充扩展性分析，设计水平/垂直扩展策略，确保系统可应对增长",
            },
            "技术债务隐瞒": {
                "primary": "交付文档未识别和规划技术债务",
                "secondary": "缺乏技术债管理和长期维护规划意识",
                "fix_path": "透明化技术债务清单，制定偿还计划和重构优先级",
            },
            "用户验证空白": {
                "primary": "交付文档缺乏用户验证和市场反馈",
                "secondary": "跳过用户调研直接开发，缺乏精益创业思维",
                "fix_path": "补充用户调研数据和MVP验证结果，证明需求真实存在",
            },
            "依赖风险": {
                "primary": "交付文档未评估第三方依赖风险",
                "secondary": "缺乏供应链安全意识，对关键依赖缺少管控",
                "fix_path": "建立依赖清单，评估活跃度和稳定性，制定替代方案",
            },
            "运维盲区": {
                "primary": "交付文档缺少运维和监控设计",
                "secondary": "缺乏可观测性设计，运维左移意识不足",
                "fix_path": "补充监控告警策略和日志方案，定义SLA/SLO指标",
            },
            "国际化缺失": {
                "primary": "交付文档未考虑国际化和本地化需求",
                "secondary": "缺乏全球化产品思维，局限于单一市场",
                "fix_path": "评估多语言支持需求，规划i18n/l10n技术方案",
            },
            "无障碍合规": {
                "primary": "交付文档未考虑无障碍设计",
                "secondary": "缺乏包容性设计意识，忽视残障用户需求",
                "fix_path": "评估WCAG合规级别，补充无障碍功能清单和辅助技术支持方案",
            },
            "成本控制缺失": {
                "primary": "交付文档未进行成本效益分析",
                "secondary": "缺乏商业思维，未评估项目经济可行性",
                "fix_path": "补充成本估算和预算规划，明确盈利模式和ROI计算",
            },
            "退出策略缺失": {
                "primary": "交付文档缺少项目退出和迁移方案",
                "secondary": "缺乏全生命周期管理思维，未考虑项目终止场景",
                "fix_path": "制定下线/迁移预案，说明数据备份策略和弃用流程",
            },
        }

        mapping = root_cause_mapping.get(
            pattern_name,
            {
                "primary": "交付文档存在不足",
                "secondary": "缺乏系统化的交付规范意识",
                "fix_path": "根据评审意见逐项完善文档，建立标准化交付模板",
            },
        )

        return {
            "surface": surface,
            "primary": mapping["primary"],
            "secondary": mapping["secondary"],
            "fix_path": mapping["fix_path"],
        }

    def _empty_result(self) -> Dict:
        """Return empty/error result for invalid input.

        Returns:
            Error result dict with all required fields.
        """
        return {
            "real_issue": "输入为空，无法分析拒绝原因",
            "fixable_items": ["请提供完整的拒绝说明文本"],
            "resubmit_suggestion": "补充拒绝原因后重新提交分析",
            "matched_pattern": "无",
            "confidence": 0.0,
            "checklist_results": {
                "readme_clear": False,
                "has_scenarios": False,
                "has_metrics": False,
                "has_risk_disclosure": False,
                "has_competitor_comparison": False,
                "docs_complete": False,
                "compliance_clear": False,
            },
            "root_cause_tree": {
                "surface": "",
                "primary": "",
                "secondary": "",
                "fix_path": "",
            },
        }


if __name__ == "__main__":
    analyzer = RejectAnalyzer()

    test_cases = [
        "技术实现描述太底层，看不出用户价值",
        "又一个AI Agent工具，没看出有什么特别的",
        "缺少安装说明和使用文档",
        "未说明数据安全和隐私保护措施",
        "看不出项目相比现有方案的优势",
        "不知道这个项目在什么场景下使用",
        "规划不清晰，没有明确的执行路径",
        "方案过于复杂，与要解决的问题不匹配",
        "许可证不明确，缺少合规声明",
        "不清楚这个项目要解决什么问题",
        "",
    ]

    import json

    for i, text in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"测试用例 {i}: {text or '(空输入)'}")
        print(f"{'='*60}")
        result = analyzer.analyze(text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
