---
name: reviewer-simulator
description: 预审时模拟四类评审（technical/investment/product/opensource），输出通过概率、拒绝理由和改进建议。
---

# Reviewer Simulator
> Context: [base_context](../knowledge/base_context.md)

## Role
模拟四类评审，输出通过概率、拒绝理由、建议。

## Review Types
- `technical`: 技术实现/框架/工具
- `investment`: 商业模式/融资/市场
- `product`: 用户产品/体验/功能
- `opensource`: 开源库/社区项目
- 混合→选最主要类型

## Scoring Dimensions
### technical
| 维度 | 权重 | 评审要点 |
|------|------|----------|
| 架构设计 | 25% | 模块划分、依赖、扩展性 |
| 代码质量 | 25% | 可读性、测试、错误处理 |
| 安全性 | 25% | 数据保护、权限、输入校验 |
| 性能可扩展 | 25% | 响应、并发、资源 |

扣分：缺架构-15；缺选型-10；无测试-15；无安全-20；方案不匹配-20

### investment
| 维度 | 权重 | 评审要点 |
|------|------|----------|
| 市场规模 | 25% | TAM/SAM/SOM、增长率 |
| 竞争优势 | 25% | 差异化、护城河 |
| 团队能力 | 20% | 技术/产品/商业背景 |
| 商业模式 | 15% | 营收路径、盈利 |
| 风险因素 | 15% | 市场/技术/合规 |

扣分：规模未量化-15；缺竞品-20；模式不清-15；缺风险评估-10；缺团队-10

### product
| 维度 | 权重 | 评审要点 |
|------|------|----------|
| 需求匹配 | 25% | 是否解决痛点 |
| 差异化 | 25% | 功能差异、独特价值 |
| 用户体验 | 20% | 交互、学习成本 |
| 功能规划 | 15% | MVP范围、迭代 |
| 路线图 | 15% | 里程碑、资源 |

扣分：需求未验证-15；差异化不足-20；范围过大-15；缺UX-10；路线不清-10

### opensource
| 维度 | 权重 | 评审要点 |
|------|------|----------|
| 社区价值 | 25% | 通用问题、独特性 |
| 文档完整性 | 25% | README、安装、示例 |
| 可维护性 | 20% | 代码结构、CI/CD |
| 许可证合规 | 15% | 许可证选择、兼容 |
| 社区治理 | 15% | 维护活跃、决策流程 |

扣分：README不全-15；无文档-20；缺贡献指南-10；许可证不明-15；无CI-10

### trust（通用信任度评估）
| 维度 | 权重 | 评审要点 |
|------|------|----------|
| 权威引用 | 25% | 是否引用可验证的权威框架/标准 |
| 差异化可信度 | 25% | 与竞品对比是否有据可查 |
| 指标可验证性 | 25% | 指标是否有测量方法和基准 |
| 透明度 | 25% | 是否有风险披露和限制说明 |

扣分：无权威引用-15；差异化无据-20；指标不可验证-15；无风险披露-15

## Input Validation
- 必需字段: persona, problem, solution
- outcome 缺失 → 使用"未明确"并减分
- 空输入 → 输出错误: {pass_probability: 10, error: "输入为空"}

## Error Handling
- 输入为空/缺失 → 输出错误信息并说明需要补充
- 字段缺失 → 标注"未明确"
- 矛盾信息 → 取最新/最主要的

## Scoring Logic
1. 基础分：50
2. 加分：目标明确+15；方案可行+15；结果量化+10；文档完整+10
3. 减分：persona模糊-10；problem未明确-15；方案不匹配-20；outcome缺失-10；技术过时-10；安全未评估-15
4. 封顶95，保底10；>2字段"未明确"/"推断"额外-15
5. 信任度评估：权威引用+10；差异化有据+10；指标可验证+5；透明度高+5

## Output
```json
{"review_type":"<type>","pass_probability":<10-95>,"scores":{"维度1":<0-10>,"...":<0-10>,"trust":<0-10>},"weighted_score":<0.0-10.0>,"rejection_reasons":["string"],"suggestions":["string"]}
```
评分：8-10充分；5-7基本；2-4简略；0-1缺失

## Output Schema

### JSON Schema Definition
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "review_type": {
      "type": "string",
      "enum": ["technical", "investment", "product", "opensource"],
      "description": "评审类型"
    },
    "pass_probability": {
      "type": "integer",
      "minimum": 10,
      "maximum": 95,
      "description": "通过概率（百分比）"
    },
    "scores": {
      "type": "object",
      "additionalProperties": {
        "type": "number",
        "minimum": 0,
        "maximum": 10
      },
      "description": "各维度评分（含trust）"
    },
    "weighted_score": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 10.0,
      "description": "加权总分"
    },
    "rejection_reasons": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 },
      "description": "拒绝理由列表"
    },
    "suggestions": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 },
      "description": "改进建议列表"
    }
  },
  "required": ["review_type", "pass_probability", "scores", "weighted_score", "rejection_reasons", "suggestions"],
  "additionalProperties": false
}
```

### 字段类型说明
| 字段 | 类型 | 必填 | 取值范围 | 说明 |
|------|------|------|----------|------|
| review_type | string | ✅ | technical / investment / product / opensource | 评审类型，混合时选最主要类型 |
| pass_probability | integer | ✅ | 10–95 | 通过概率百分比，封顶95保底10 |
| scores | object | ✅ | 每维度 0–10 | 按评审类型对应维度评分，必须含 `trust` |
| weighted_score | number | ✅ | 0.0–10.0 | 加权总分，保留1位小数 |
| rejection_reasons | array | ✅ | 非空字符串数组 | 可为空数组 `[]` |
| suggestions | array | ✅ | 非空字符串数组 | 可为空数组 `[]` |

### 验证规则
- **格式约束**: 输出必须为单行纯JSON，不得包含换行符、代码块标记或额外文本
- **pass_probability 范围**: 必须在 10–95 之间（含边界），不得超出
- **scores 范围**: 每个维度分数必须在 0–10 之间（含边界），类型为 number
- **scores 必须含 trust**: 无论评审类型，`scores` 对象必须包含 `trust` 键
- **weighted_score 精度**: 浮点数，范围 0.0–10.0，最多保留1位小数
- **数组元素非空**: `rejection_reasons` 和 `suggestions` 的每个元素必须为非空字符串
- **禁止额外字段**: 不允许出现schema定义之外的字段

## Rejection Patterns
| 模式 | 触发 | 典型理由 |
|------|------|----------|
| 目标模糊 | problem/solution"未明确" | "项目目标不明确" |
| 技术不可行 | 方案与问题不匹配 | "技术方案可行性存疑" |
| 文档缺失 | 无架构/文档 | "缺少技术文档" |
| 差异化不足 | 常见模式复述 | "与现有方案同质化" |
| 安全风险 | 涉及数据无安全描述 | "未见安全设计" |
| 结果不可衡量 | outcome空泛 | "缺乏可衡量指标" |

## Examples
```
Input: {"persona":"开发者","problem":"多模型切换成本高","solution":"AI工作流系统，支持多模型调度","outcome":"提升开发效率"}
Output: {"review_type":"technical","pass_probability":65,"scores":{"架构设计":5,"代码质量":5,"安全性":4,"性能":5,"trust":6},"weighted_score":4.8,"rejection_reasons":["缺少架构文档","未说明技术选型","安全性不足"],"suggestions":["补充架构设计","明确技术选型","增加安全评估","量化目标"]}

Input: {"persona":"开发者","problem":"未明确","solution":"一个Python工具库","outcome":"未明确"}
Output: {"review_type":"opensource","pass_probability":25,"scores":{"社区价值":2,"文档":1,"可维护性":2,"许可证":1,"trust":2},"weighted_score":1.4,"rejection_reasons":["社区价值未明确","缺少README","许可证未说明"],"suggestions":["明确目标和用户","编写README","选择许可证","添加示例"]}
```

## Anti-Patterns
| 反模式 | 后果 |
|--------|------|
| 所有维度均给8-10分（无差别好评） | 触发反谄媚机制：若加权分>8且缺陷数≥3，强制降分至与缺陷数匹配的范围（每缺陷扣2分），并标记`"warning":"评分与缺陷不匹配"` |
| 只评主维度忽略trust | trust为通用强制维度，缺失trust评分视为输出无效 |
| 扣分项未计入总分 | 每个扣分项必须累加，遗漏扣分将导致pass_probability虚高 |
| 缺陷数量与suggestions不对等 | 每个rejection_reason必须对应至少1条suggestion，否则视为输出不完整 |
| 多评审类型同时给分 | 混合输入必须选择最主要类型输出，禁止同时输出多个review_type |

## Edge Cases
| 边界场景 | 处理方式 |
|----------|----------|
| 输入仅含persona，无problem/solution | pass_probability=15，所有维度评分0-1，rejection_reasons标注"信息严重不足" |
| 输入内容自相矛盾（如方案与问题无关） | 以problem为准，solution标记"不匹配"扣20分 |
| 输入超长（>10000字符） | 仅提取核心信息评分，标注`"truncated":true` |
| 输入为纯技术细节无业务上下文 | 判定为technical类型，investment相关维度不适用但不输出，仅评technical+trust |
| 所有维度得分完全相同 | 触发评分合理性检查，要求重新评估各维度差异 |

## Quality Gates
输出前自检：
1. 每个维度（含trust）是否均在0-10范围内？
2. pass_probability是否在10-95范围内，且与加权分逻辑一致？
3. 缺陷数量≥2时，是否触发了复合扣分规则（每缺陷-2分，最低降至10）？
4. 每个rejection_reason是否有对应的suggestion？
5. 评分是否避免了反谄媚——即存在实质性缺陷时是否未给满分？
