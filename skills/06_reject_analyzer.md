# Reject Analyzer
> Context: [base_context](../knowledge/base_context.md)

## Purpose
分析被拒原因，提取真实问题，给出修复建议。

## Reject Patterns
| # | 模式 | 典型拒绝 | 真实问题 | 修复方向 |
|---|------|----------|----------|----------|
| 1 | 表达太底层 | "看不出用户价值" | 技术语言替代价值 | Feature→Capability→Outcome |
| 2 | 目标不明确 | "不清楚解决什么问题" | 缺少场景定位 | 补充persona/problem/solution |
| 3 | 差异化不足 | "又一个XX工具" | 未突出独特价值 | 竞品对比+差异点 |
| 4 | 文档不完整 | "缺少安装说明" | 交付物不全 | 补齐README+Demo Guide |
| 5 | 安全风险 | "未说明数据安全" | 缺少安全设计 | 补充安全评估 |
| 6 | 价值模糊 | "看不出优势" | 未做竞品对比 | 竞品对比+量化指标 |
| 7 | 场景缺失 | "不知道什么时候用" | 缺少用户故事 | 补充2-3真实场景 |
| 8 | 路线图不清 | "规划不清晰" | 缺少执行路径 | 近期/中期/远期规划 |
| 9 | 技术可行性 | "方案与问题不匹配" | 方案复杂度过高 | 简化架构+提供PoC |
| 10 | 合规问题 | "许可证不明确" | 缺少合规声明 | 补充许可证+数据声明 |

## Analysis Logic
1. 匹配拒绝模式（精确优先，模糊兜底）
2. 提取真实问题（表层 vs 根本原因）
3. 生成修复项（具体、可操作、可验证）
4. 附加通用检查

## General Checklist
- [ ] README清晰(What/Why/How/Result/Next)
- [ ] 典型场景(2-3个)
- [ ] 可量化指标
- [ ] 风险说明(技术/市场/合规)
- [ ] 竞品对比(差异化)
- [ ] 文档完整(安装/配置/运行/验证)
- [ ] 许可证合规

## Output
```json
{"real_issue":"<string>","fixable_items":["<string>"],"resubmit_suggestion":"<string>","matched_pattern":"<string>","confidence":0.0-1.0,"checklist_results":{"readme_clear":true/false,"has_scenarios":true/false,"has_metrics":true/false,"has_risk_disclosure":true/false,"has_competitor_comparison":true/false,"docs_complete":true/false,"compliance_clear":true/false}}
```

## Examples
```
Input: "技术实现描述太底层，看不出用户价值"
Output: {"real_issue":"表达太底层，用户价值弱","fixable_items":["技术描述转用户价值","增加场景描述","补充量化指标"],"resubmit_suggestion":"从'交付工具'重新定位为'交付平台'，强调自动化和效率提升","matched_pattern":"表达太底层","confidence":0.85}

Input: "又一个AI Agent工具"
Output: {"real_issue":"未突出独特价值主张","fixable_items":["明确与竞品差异","突出核心定位","补充竞品对比表"],"resubmit_suggestion":"强调'让成果被接受'而非'成果生成'，定位为Acceptance Engineering","matched_pattern":"差异化不足","confidence":0.9}
```

## Rules
- 分析根本原因，不止表层
- 修复项具体可操作
- 始终附加通用检查
- confidence<0.5标注"低置信度，建议人工复核"
- 多模式匹配按置信度排序输出最高项