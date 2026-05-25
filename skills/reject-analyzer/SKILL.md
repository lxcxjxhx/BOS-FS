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
| 11 | 数据隐私缺失 | "用户数据如何处理" | 涉及用户数据无隐私声明 | 补充隐私政策+数据处理说明 |
| 12 | 可扩展性陷阱 | "无法支撑大规模" | 架构不支持水平扩展 | 补充扩展策略+瓶颈分析 |
| 13 | 技术债务隐瞒 | "未发现已知限制" | 未提及已知限制/技术债 | 诚实披露已知问题+修复计划 |
| 14 | 用户验证空白 | "无真实用户反馈" | 无真实用户验证/测试 | 补充用户调研数据或MVP测试 |
| 15 | 依赖风险 | "核心依赖不稳定" | 核心依赖不稳定/许可证冲突 | 依赖风险评估+替代方案 |
| 16 | 运维盲区 | "无监控告警方案" | 无监控/告警/回滚方案 | 补充运维设计+应急预案 |
| 17 | 国际化缺失 | "仅支持单一语言" | 目标全球化但无i18n | 补充i18n方案+本地化策略 |
| 18 | 无障碍合规 | "不符合无障碍标准" | 面向公众产品无a11y考虑 | 补充WCAG合规评估 |
| 19 | 成本控制缺失 | "云成本未优化" | 云架构无成本优化策略 | 补充成本估算+优化策略 |
| 20 | 退出策略缺失 | "无服务下线预案" | 无数据迁移/服务下线预案 | 补充数据导出+迁移方案 |

## Input Validation
- 最小输入: 拒绝说明文本
- 空输入 → 输出错误提示
- 模糊拒绝理由 → 基于常见模式推断

## Error Handling
- 输入为空/缺失 → 输出错误信息并说明需要补充
- 字段缺失 → 标注"未明确"
- 矛盾信息 → 取最新/最主要的

## Analysis Logic
1. 匹配拒绝模式（精确优先，模糊兜底，支持20种模式）
2. **根因分析（3层深度）**: 表层拒绝 → 一级根因 → 二级根因 → 修复路径
3. 提取真实问题（区分表层描述与根本原因）
4. 生成修复项（具体、可操作、可验证）
5. 附加通用检查
6. 输出root_cause_tree（每层分析必须完整）

## 根因分析树

对每个拒绝模式进行 3 层深度分析，从表层拒绝追溯到根本原因，并给出可操作的修复路径。

### 分析结构
```
表层拒绝: "[评审原文]"
  → 一级根因: "[直接原因——为什么会出现这个拒绝]"
    → 二级根因: "[根本原因——什么设计决策导致了这个问题]"
      → 修复路径: "[具体可操作的修复步骤]"
```

### 根因分析示例

#### 模式1: 表达太底层
```
表层拒绝: "看不出用户价值"
  → 一级根因: "技术描述替代了价值主张，评审无法理解谁受益、受益多少"
    → 二级根因: "Feature→Capability→Outcome 转换链断裂，停留在技术实现层"
      → 修复路径: "对每个功能追问'让用户做什么？'和'带来什么收益？'，将技术特性翻译为用户能力"
```

#### 模式3: 差异化不足
```
表层拒绝: "又一个XX工具"
  → 一级根因: "未展示与现有方案的实质性差异，评审视为同质化产品"
    → 二级根因: "缺乏竞品分析，或差异化定位停留在功能列表而非价值主张"
      → 修复路径: "选择2-3个直接竞品，从'解决什么问题不同'和'为谁解决'两个维度建立差异化矩阵"
```

#### 模式5: 安全风险
```
表层拒绝: "未说明数据安全"
  → 一级根因: "涉及数据处理但无安全设计说明，评审视为风险敞口"
    → 二级根因: "开发优先级排序中安全被置于功能之后，或团队缺乏安全设计意识"
      → 修复路径: "按OWASP Top 10逐项检查，补充数据加密、访问控制、输入校验等安全设计说明"
```

#### 模式11: 数据隐私缺失
```
表层拒绝: "用户数据如何处理"
  → 一级根因: "收集/存储用户数据但未说明隐私保护措施"
    → 二级根因: "产品需求阶段未纳入隐私by design原则，或团队不了解GDPR/等保要求"
      → 修复路径: "补充隐私政策（数据收集范围/存储位置/处理方式/用户权利），声明合规框架（GDPR/CCPA/等保）"
```

#### 模式13: 技术债务隐瞒
```
表层拒绝: "未发现已知限制"
  → 一级根因: "文档仅展示正面信息，评审认为缺乏诚实披露"
    → 二级根因: "团队误以为披露限制会降低评审通过率，实际相反——坦诚增加信任度"
      → 修复路径: "在risk_disclosure.md中诚实列出已知限制、技术债务和计划修复时间线"
```

#### 模式16: 运维盲区
```
表层拒绝: "无监控告警方案"
  → 一级根因: "系统上线后无法感知故障和性能退化"
    → 二级根因: "开发团队将运维视为独立职责，未在设计阶段考虑可观测性"
      → 修复路径: "补充三支柱可观测性设计（日志/指标/追踪），定义关键告警阈值和升级流程"
```

### 通用根因分析规则
- 所有拒绝模式的二级根因必须追溯到**设计决策**或**流程缺失**，而非表面现象
- 修复路径必须具体到**可执行的行动项**，而非"改进XX"等空泛建议
- 每个修复路径需关联到 BOS-FS 的具体 Skill 或知识文件（如适用）

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
{"real_issue":"<string>","fixable_items":["<string>"],"resubmit_suggestion":"<string>","matched_pattern":"<string>","confidence":0.0-1.0,"checklist_results":{"readme_clear":true/false,"has_scenarios":true/false,"has_metrics":true/false,"has_risk_disclosure":true/false,"has_competitor_comparison":true/false,"docs_complete":true/false,"compliance_clear":true/false},"root_cause_tree":{"surface":"<string>","primary":"<string>","secondary":"<string>","fix_path":"<string>"}}
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
    },
    "root_cause_tree": {
      "type": "object",
      "properties": {
        "surface": { "type": "string", "minLength": 1, "description": "表层拒绝（评审原文）" },
        "primary": { "type": "string", "minLength": 1, "description": "一级根因（直接原因）" },
        "secondary": { "type": "string", "minLength": 1, "description": "二级根因（根本原因）" },
        "fix_path": { "type": "string", "minLength": 1, "description": "修复路径（具体可操作）" }
      },
      "required": ["surface", "primary", "secondary", "fix_path"],
      "additionalProperties": false,
      "description": "3层根因分析树"
    }
  },
  "required": ["real_issue", "fixable_items", "resubmit_suggestion", "matched_pattern", "confidence", "checklist_results", "root_cause_tree"],
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
| root_cause_tree | object | ✅ | 见下方 | 3层根因分析（表层→一级→二级→修复路径） |

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
- **必填字段**: 顶层7个字段缺一不可
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
- **根因分析仅停留在表层**：如"看不出价值"仅转述为"价值描述不足"，未追溯到转换链断裂或用户画像缺失。
- **修复路径过于空泛**：如"改进文档"应具体到"在What段补充技术×用户×收益一句话，参考readme-refactor SKILL.md"。
- **20种模式识别不全**：新扩展的模式（11-20）必须与原有模式（1-10）同等对待，不可遗漏。

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
- [ ] **root_cause_tree的4个字段是否全部填写？**（surface/primary/secondary/fix_path）
- [ ] **二级根因是否追溯到设计决策或流程缺失，而非表面现象？**
- [ ] **修复路径是否关联到BOS-FS的具体Skill或知识文件（如适用）？**

## 方法论来源与学术诚信

本 Skill 的方法论来源于**作者亲自阅读以下书籍并提炼核心要点**，非 AI 自动处理或简单摘要。

| 启发来源 | 核心贡献 |
|----------|----------|
| [Accelerate](Nicole Forsgren 等) | 失败模式分析 |
| [Continuous Discovery Habits](Teresa Torres) | 假设检验与验证 |

> **声明**: 本 Skill 中的方法论启发自上述书籍（见表格），所有代码实现、示例和知识重构均为作者原创。建议读者支持正版，购买原书以获得更完整的论述和案例。
