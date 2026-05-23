"""
Reject Analyzer Module
Parse and analyze submission rejection reasons, extract actionable fix items.
"""

import json
import re
from typing import Optional


class RejectAnalyzer:
    """分析提交被拒绝的原因，输出可执行的修复建议。"""

    # 常见拒绝模式 → 真实问题映射
    PATTERNS = [
        {
            "keywords": ["底层", "low-level", "太细", "细节", "实现细节"],
            "real_issue": "表达过于底层，缺乏用户视角的价值描述",
            "fixable_items": [
                "将工具能力描述升级为交付成果描述",
                "补充业务场景和用户价值说明",
                "增加前后对比或效果指标",
            ],
            "suggestion": "从「工具」视角转换为「交付平台」视角，强调最终产出而非实现过程",
        },
        {
            "keywords": ["用户价值", "价值弱", "没有价值", "不清楚做什么", "意义不明"],
            "real_issue": "用户价值主张不够清晰，审核方无法快速理解项目意义",
            "fixable_items": [
                "在 README 首屏明确写出核心用户价值",
                "添加真实使用场景案例",
                "用数据或指标量化价值提升",
            ],
            "suggestion": "采用「谁 + 在什么场景 + 解决了什么问题 + 效果如何」的结构重写价值描述",
        },
        {
            "keywords": ["重复", "已有", "类似", "同质化"],
            "real_issue": "与现有项目差异化不足",
            "fixable_items": [
                "明确列出与同类项目的差异点",
                "突出独有的功能或技术优势",
                "提供竞品对比表格",
            ],
            "suggestion": "聚焦 1-2 个核心差异化卖点，避免功能列表式罗列",
        },
        {
            "keywords": ["不完整", "缺少", "文档", "demo", "示例"],
            "real_issue": "提交材料不完整，缺少关键文档或演示",
            "fixable_items": [
                "补充完整的 README 和 Demo Guide",
                "添加可运行的示例或截图",
                "提供部署和使用说明",
            ],
            "suggestion": "使用 SubmissionBuilder 生成标准化文档包后重新提交",
        },
        {
            "keywords": ["安全", "权限", "敏感", "泄露"],
            "real_issue": "存在安全隐患或敏感信息泄露风险",
            "fixable_items": [
                "移除硬编码的密钥、Token、密码",
                "检查依赖组件的已知漏洞",
                "补充安全测试报告",
            ],
            "suggestion": "完成安全自查并附上审计报告后重新提交",
        },
    ]

    # 通用修复项（任何拒绝都建议检查）
    GENERAL_ITEMS = [
        "检查 README 是否清晰描述了「是什么」和「为什么」",
        "确认提交版本号为最新且符合语义化版本规范",
        "确保所有链接和引用有效",
    ]

    def analyze(self, rejection_reason: str) -> dict:
        """
        解析拒绝原因，提取真实问题和可修复项。

        Args:
            rejection_reason: 审核方给出的拒绝原因文本。

        Returns:
            {"real_issue": str, "fixable_items": list[str], "resubmit_suggestion": str}
        """
        if not rejection_reason or not rejection_reason.strip():
            return {
                "real_issue": "未提供拒绝原因，请补充审核后重试",
                "fixable_items": self.GENERAL_ITEMS[:],
                "resubmit_suggestion": "获取明确拒绝原因后再进行分析",
            }

        matched = self._match_pattern(rejection_reason)
        if matched:
            fixable = matched["fixable_items"] + self.GENERAL_ITEMS
            return {
                "real_issue": matched["real_issue"],
                "fixable_items": fixable,
                "resubmit_suggestion": matched["suggestion"],
            }

        # 未匹配到已知模式，返回通用分析
        return self._fallback_analysis(rejection_reason)

    # -- internal -----------------------------------------------------------

    def _match_pattern(self, reason: str) -> Optional[dict]:
        reason_lower = reason.lower()
        for pattern in self.PATTERNS:
            if any(kw.lower() in reason_lower for kw in pattern["keywords"]):
                return pattern
        return None

    def _fallback_analysis(self, reason: str) -> dict:
        # 提取关键动词和名词做基础分析
        key_phrases = self._extract_key_phrases(reason)
        return {
            "real_issue": f"审核反馈: {reason.strip()}",
            "fixable_items": [
                f"针对反馈「{phrase}」进行专项优化" for phrase in key_phrases[:3]
            ]
            + self.GENERAL_ITEMS,
            "resubmit_suggestion": "建议与审核方沟通获取更具体的修改方向",
        }

    @staticmethod
    def _extract_key_phrases(text: str) -> list[str]:
        """从文本中提取可能的关键短语（中文分词简化版）。"""
        # 按常见分隔符切分
        parts = re.split(r"[，,、；;。\n]", text)
        return [p.strip() for p in parts if p.strip() and len(p.strip()) > 1]


if __name__ == "__main__":
    examples = [
        "表达太底层，看不出用户价值",
        "与现有项目重复，缺乏差异化",
        "文档不完整，缺少 Demo 和截图",
        "存在敏感信息泄露风险",
        "不知道这个项目解决了什么问题",
        "自定义的拒绝原因：流程太复杂，用户上手成本高",
    ]

    analyzer = RejectAnalyzer()
    for reason in examples:
        print(f"\n{'='*60}")
        print(f"拒绝原因: {reason}")
        print(f"{'='*60}")
        result = analyzer.analyze(reason)
        print(json.dumps(result, ensure_ascii=False, indent=2))
