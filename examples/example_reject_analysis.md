# BOS-FS 拒绝分析示例

## 输入
```
拒绝原因：技术实现描述过于底层，看不出用户价值，与现有方案差异不明显。
```

## 分析 → Reject Analyzer
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

## 修复后
使用 Outcome Mapper 转换所有技术描述为价值主张，使用 README Refactor 重构文档，使用 Reviewer Simulator 预审通过率提升至 70%+。
