---
name: reject-analyzer
description: 项目被拒时分析拒绝原因，提取真实问题并给出具体可操作的修复建议。
---

# Reject Analyzer
**version**: 0.2.11
> Context: [base_context](../../knowledge/base_context.md)
> Full version: skills/reject-analyzer/SKILL.md

## Role
分析被拒原因，提取真实问题，给出修复建议。

## Reject Patterns (20种)
| # | 模式 | 关键词 | 修复方向 |
|---|------|--------|----------|
| 1 | 表达太底层 | 看不出用户价值 | Feature→Capability→Outcome |
| 2 | 目标不明确 | 不清楚解决什么问题 | 补充persona/problem/solution |
| 3 | 差异化不足 | 又一个XX工具 | 竞品对比+差异点 |
| 4 | 文档不完整 | 缺少安装说明 | 补齐README+Demo Guide |
| 5 | 安全风险 | 未说明数据安全 | 补充安全评估 |
| 6 | 价值模糊 | 看不出优势 | 竞品对比+量化指标 |
| 7 | 场景缺失 | 不知道什么时候用 | 补充2-3真实场景 |
| 8 | 路线图不清 | 规划不清晰 | 近期/中期/远期规划 |
| 9 | 技术可行性 | 方案与问题不匹配 | 简化架构+PoC |
| 10 | 合规问题 | 许可证不明确 | 补充许可证+数据声明 |
| 11 | 数据隐私缺失 | 用户数据如何处理 | 隐私政策+处理说明 |
| 12 | 可扩展性陷阱 | 无法支撑大规模 | 扩展策略+瓶颈分析 |
| 13 | 技术债务隐瞒 | 未发现已知限制 | 诚实披露+修复计划 |
| 14 | 用户验证空白 | 无真实用户反馈 | 用户调研/MVP测试 |
| 15 | 依赖风险 | 核心依赖不稳定 | 依赖评估+替代方案 |
| 16 | 运维盲区 | 无监控告警方案 | 运维设计+应急预案 |
| 17 | 国际化缺失 | 仅支持单一语言 | i18n方案+本地化策略 |
| 18 | 无障碍合规 | 不符合无障碍标准 | WCAG合规评估 |
| 19 | 成本控制缺失 | 云成本未优化 | 成本估算+优化策略 |
| 20 | 退出策略缺失 | 无服务下线预案 | 数据导出+迁移方案 |

## Analysis Logic
1. 匹配模式（精确优先，模糊兜底）
2. 根因分析：表层→一级→二级→修复路径
3. 提取真实问题（区分表层与根因）
4. 生成修复项（具体可操作可验证）
5. 附加通用检查
6. 输出 root_cause_tree

## Root Cause Tree Rules
```
表层拒绝: "[评审原文]"
  → 一级根因: "[直接原因]"
    → 二级根因: "[设计决策/流程缺失]"
      → 修复路径: "[具体可执行行动项]"
```
- 二级根因必须追溯到**设计决策**或**流程缺失**，非表面现象
- 修复路径必须具体到**可执行行动项**，非空泛建议
- 修复路径关联 BOS-FS Skill/知识文件（如适用）

## Input/Output
- **最小输入**: 拒绝说明文本；空输入→错误提示；模糊→基于常见模式推断

### Output Schema (Complete)
```json
{"type":"object",
 "properties":{
  "real_issue":{"type":"string","minLength":1,"description":"根本原因"},
  "fixable_items":{"type":"array","items":{"type":"string","minLength":1},"minItems":1},
  "resubmit_suggestion":{"type":"string","minLength":1},
  "matched_pattern":{"type":"string","minLength":1},
  "confidence":{"type":"number","minimum":0.0,"maximum":1.0},
  "checklist_results":{"type":"object","properties":{"clear_problem":{"type":"boolean"},"value_proposition":{"type":"boolean"},"differentiation":{"type":"boolean"},"documentation":{"type":"boolean"},"security_privacy":{"type":"boolean"},"compliance":{"type":"boolean"},"roadmap":{"type":"boolean"}},"required":["clear_problem","value_proposition","differentiation","documentation","security_privacy","compliance","roadmap"]},
  "root_cause_tree":{"type":"object","properties":{"surface":{"type":"string"},"primary":{"type":"string"},"secondary":{"type":"string"},"fix_path":{"type":"string"}},"required":["surface","primary","secondary","fix_path"]},
  "multi_patterns":{"type":"array","items":{"type":"object","properties":{"pattern_name":{"type":"string"},"confidence":{"type":"number","minimum":0.0,"maximum":1.0}},"required":["pattern_name","confidence"]}}
 },
 "required":["real_issue","fixable_items","resubmit_suggestion","matched_pattern","confidence","checklist_results","root_cause_tree"],
 "additionalProperties":false}
```
**必填**: real_issue, fixable_items, resubmit_suggestion, matched_pattern, confidence, checklist_results, root_cause_tree
**confidence<0.5**: 标注"低置信度，建议人工复核"
**格式**: 单行纯JSON，无额外字段

### Field Summary
| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| real_issue | ✅ | string | 根本原因 |
| fixable_items | ✅ | array≥1 | 可操作修复项 |
| resubmit_suggestion | ✅ | string | 重提策略 |
| matched_pattern | ✅ | string | 匹配模式名 |
| confidence | ✅ | number 0-1 | 置信度 |
| checklist_results | ✅ | object(7个boolean) | 通用检查 |
| root_cause_tree | ✅ | object(4个string) | 3层根因 |
| multi_patterns | ❌ | array | 多模式结果 |

## Rules
| 规则 | 约束 |
|------|------|
| 分析根本原因 | 不止表层描述 |
| 修复项具体可操作 | 非空泛建议 |
| 始终附加通用检查 | 7项全部填写 |
| confidence<0.5 | 标注低置信度 |
| 多模式 | 按置信度排序输出最高 |

## Anti-Patterns
| 反模式 | 后果 |
|--------|------|
| 仅复述不挖掘根因 | real_issue应定位具体缺失 |
| fixable_items空泛 | 应具体到行动项 |
| confidence盲目高分 | 误导后续决策 |
| 忽略多模式复合 | 应同时匹配多模式 |
| 根因停留表层 | 需追溯转换链断裂/画像缺失 |
| 修复路径空泛 | 关联到具体Skill |
| 20种模式识别不全 | 模式11-20同等对待 |

## Edge Cases
| 场景 | 处理 |
|------|------|
| 拒绝极度模糊（"暂不通过"） | 匹配最近似模式，confidence≤0.3，附低置信度标注 |
| 多条拒绝矛盾 | 取最新/最具体，其余作fixable_items补充 |
| 含攻击性/非建设性语言 | 过滤情绪化，提取可操作问题 |
| 涉及外部因素 | 归入real_issue但不生成fixable_items |

## Quality Gates
- [ ] real_issue是否指出根本原因而非复述表层？
- [ ] fixable_items每项是否具体可操作可验证？
- [ ] confidence值是否合理？（模糊≤0.5附低置信度标注）
- [ ] checklist_results的7个子字段是否全部填写？
- [ ] 输出是否为合法单行纯JSON，无schema外字段？
- [ ] root_cause_tree的4个字段（surface/primary/secondary/fix_path）是否全部填写？
- [ ] 二级根因是否追溯到设计决策/流程缺失？
- [ ] 修复路径是否关联到BOS-FS具体Skill/知识文件（如适用）？

## 方法论来源
| 启发来源 | 核心贡献 |
|----------|----------|
| [Accelerate](Nicole Forsgren 等) | 失败模式分析 |
| [Continuous Discovery Habits](Teresa Torres) | 假设检验与验证 |
