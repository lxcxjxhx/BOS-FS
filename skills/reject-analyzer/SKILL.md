---
name: reject-analyzer
description: 项目被拒时分析拒绝原因，提取真实问题并给出具体可操作的修复建议。
---

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

## Input Validation
- 最小输入: 拒绝说明文本
- 空输入 → 输出错误提示
- 模糊拒绝理由 → 基于常见模式推断

## Error Handling
- 输入为空/缺失 → 输出错误信息并说明需要补充
- 字段缺失 → 标注"未明确"
- 矛盾信息 → 取最新/最主要的

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

## Output Schema

### JSON Schema Definition
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "real_issue": {
      "type": "string",
      "minLength": 1,
      "description": "根本原因（非表层描述）"
    },
    "fixable_items": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 },
      "minItems": 1,
      "description": "可操作的修复项列表"
    },
    "resubmit_suggestion": {
      "type": "string",
      "minLength": 1,
      "description": "重新提交建议"
    },
    "matched_pattern": {
      "type": "string",
      "minLength": 1,
      "description": "匹配的拒绝模式名称"
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "匹配置信度"
    },
    "checklist_results": {
      "type": "object",
      "properties": {
        "readme_clear": { "type": "boolean" },
        "has_scenarios": { "type": "boolean" },
        "has_metrics": { "type": "boolean" },
        "has_risk_disclosure": { "type": "boolean" },
        "has_competitor_comparison": { "type": "boolean" },
        "docs_complete": { "type": "boolean" },
        "compliance_clear": { "type": "boolean" }
      },
      "required": [
        "readme_clear",
        "has_scenarios",
        "has_metrics",
        "has_risk_disclosure",
        "has_competitor_comparison",
        "docs_complete",
        "compliance_clear"
      ],
      "additionalProperties": false,
      "description": "通用检查结果"
    }
  },
  "required": ["real_issue", "fixable_items", "resubmit_suggestion", "matched_pattern", "confidence", "checklist_results"],
  "additionalProperties": false
}
```

### 字段类型说明
| 字段 | 类型 | 必填 | 取值范围 | 说明 |
|------|------|------|----------|------|
| real_issue | string | ✅ | 非空 | 拒绝的根本原因，非表层描述 |
| fixable_items | array | ✅ | 非空字符串数组，至少1项 | 具体可操作的修复项 |
| resubmit_suggestion | string | ✅ | 非空 | 重新提交的策略建议 |
| matched_pattern | string | ✅ | 非空 | 匹配的拒绝模式（来自Reject Patterns表） |
| confidence | number | ✅ | 0.0–1.0 | 匹配置信度，<0.5需标注"低置信度，建议人工复核" |
| checklist_results | object | ✅ | 见下方 | 通用检查清单结果 |

### checklist_results 子字段
| 子字段 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| readme_clear | boolean | ✅ | README是否清晰 |
| has_scenarios | boolean | ✅ | 是否有典型场景 |
| has_metrics | boolean | ✅ | 是否有可量化指标 |
| has_risk_disclosure | boolean | ✅ | 是否有风险说明 |
| has_competitor_comparison | boolean | ✅ | 是否有竞品对比 |
| docs_complete | boolean | ✅ | 文档是否完整 |
| compliance_clear | boolean | ✅ | 许可证/合规是否明确 |

### 验证规则
- **格式约束**: 输出必须为单行纯JSON，不得包含换行符、代码块标记或额外文本
- **confidence 范围**: 必须在 0.0–1.0 之间（含边界），类型为 number
- **低置信度标注**: `confidence < 0.5` 时，须在输出中附加"低置信度，建议人工复核"
- **fixable_items 非空**: 至少包含1个修复项（`minItems: 1`）
- **checklist_results 完整性**: 7个子字段缺一不可，均为 boolean 类型
- **必填字段**: 顶层6个字段缺一不可
- **禁止额外字段**: 不允许出现schema定义之外的字段（checklist_results 同理）

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

## Anti-Patterns
- **仅复述拒绝理由不挖掘根因**：如拒绝说"看不出价值"，real_issue应定位到具体缺失（缺少场景/指标/竞品对比）。
- **fixable_items写空泛建议**：如"改进文档"应具体为"在What段补充技术×用户×收益一句话"。
- **confidence盲目给高分**：模糊拒绝理由（"不太合适"）却给0.9置信度，误导后续决策。
- **忽略多模式复合拒绝**：一条拒绝同时涉及"表达底层"和"差异化不足"，仅匹配单一模式。

## Edge Cases
- **拒绝理由极度模糊**（如"暂不通过"）→ 匹配最近似模式，confidence≤0.3，附加"低置信度，建议人工复核"。
- **多条拒绝意见矛盾**→ 取最新/最具体的拒绝，其余作为fixable_items补充。
- **拒绝理由含攻击性/非建设性语言**→ 过滤情绪化表述，仅提取可操作问题点。
- **拒绝涉及外部因素**（如"市场时机不对"）→ 归入real_issue但不生成fixable_items（超出项目可控范围）。

## Quality Gates
- [ ] real_issue是否指出根本原因而非复述表层拒绝？
- [ ] fixable_items每项是否具体、可操作、可验证？
- [ ] confidence值是否合理？（模糊拒绝应≤0.5并附低置信度标注）
- [ ] checklist_results的7个子字段是否全部填写？
- [ ] 输出是否为合法单行纯JSON，且无schema外字段？

## 方法论来源与学术诚信

本 Skill 的方法论来源于**作者亲自阅读以下书籍并提炼核心要点**，非 AI 自动处理或简单摘要。

| 启发来源 | 核心贡献 |
|----------|----------|
| [Accelerate](Nicole Forsgren 等) | 失败模式分析 |
| [Continuous Discovery Habits](Teresa Torres) | 假设检验与验证 |

> **声明**: 本 Skill 中的方法论启发自上述书籍（见表格），所有代码实现、示例和知识重构均为作者原创。建议读者支持正版，购买原书以获得更完整的论述和案例。
