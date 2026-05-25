# BOS-FS 拒绝分析示例

## 对应 Skill
[skills/06_reject_analyzer.md](../skills/06_reject_analyzer.md)

## Input（拒绝原因）
```
拒绝原因：技术实现描述过于底层，看不出用户价值，与现有方案差异不明显。
```

## Output（Reject Analyzer 分析结果）
```json
{
  "real_issue": "表达太底层，用技术语言替代了价值描述，差异化不足",
  "fixable_items": [
    "将技术描述转换为用户价值（Feature → Outcome）",
    "明确与竞品的具体差异点",
    "补充典型使用场景",
    "增加可量化指标"
  ],
  "resubmit_suggestion": "从'技术工具'重新定位为'交付平台'，强调自动化和效率提升，补充竞品对比表",
  "matched_pattern": "表达太底层 + 差异化不足",
  "confidence": 0.85
}
```

## 处理说明
1. **模式匹配**: 精确匹配"表达太底层"模式（技术语言替代价值描述），模糊匹配"差异化不足"模式
2. **根本原因提取**: 表层问题是"看不出用户价值"，根本原因是"用技术语言替代了价值描述"
3. **修复建议生成**: 具体可操作（转换语言/明确差异/补充场景/增加指标）
4. **置信度**: 0.85（高），基于两类拒绝模式的组合判断

## 修复后
使用 Outcome Mapper 转换所有技术描述为价值主张，使用 README Refactor 重构文档，使用 Reviewer Simulator 预审通过率提升至 70%+。
