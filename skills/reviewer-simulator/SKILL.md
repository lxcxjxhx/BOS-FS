---
name: reviewer-simulator
description: 预审时模拟五类评审（technical/investment/product/opensource/adversarial），输出通过概率、拒绝理由和改进建议。
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
- `adversarial`: 敌对评审（竞争对手/敌对者视角，主动寻找缺陷）
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

**词汇级检测**: 若评审输出中出现空泛赞美词（优秀/完美/出色/一流/极佳/卓越）但无具体证据支撑，强制降级 trust 分 2 分，并记录到 sycophancy_warnings。

### adversarial（敌对评审）
> 模拟竞争对手、敌对投资者、恶意收购方的评审视角。目标：像憎恶项目一样尽可能找到缺陷。

| 维度 | 权重 | 评审要点 | 敌对策略 |
|------|------|----------|----------|
| 技术脆弱性 | 20% | 架构缺陷/技术债/单点故障 | 从架构文档缺失推断技术债严重性 |
| 商业风险 | 20% | 市场规模/竞争护城河/替代方案 | 假设每个市场声明都不可信 |
| 执行能力 | 20% | 团队背景/交付历史/资源充足性 | 假设团队无法兑现承诺 |
| 合规法律 | 20% | 许可证/数据隐私/监管风险 | 假设所有合规声明需要第三方审计 |
| 致命缺陷 | 20% | 可导致项目彻底失败的因素 | 寻找≥1个kill factor |

**敌对评审专用扣分规则**:
- 每个"未明确"字段：-20（普通模式仅-10/-15）
- 每个"推断"字段：-10（视为信息不足的证据）
- 无架构图：-25
- 无竞品分析：-20
- 无安全设计：-20
- 无用户验证数据：-15
- 无技术选型理由：-15
- 量化指标缺失：每项-10

**评分范围**: 基础分35（而非50），封顶75（而非95），保底5（而非10）
**原理**: 敌对评审假设项目存在重大问题，除非被证据证明否则所有声明都存疑。

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

### 缺陷加权非线性递减
当缺陷数 ≥ 3 时，pass_probability 按公式计算：
`final_score = base_score - Σ(defect_penalty_i × severity_i)`
其中 severity_i 随缺陷数递增：
- 第 1-2 个缺陷：severity = 1.0（线性）
- 第 3 个缺陷：severity = 1.3
- 第 4 个缺陷：severity = 1.7
- 第 5+ 个缺陷：severity = 2.0 + (n-5) × 0.5

**原理**: 模拟真实评审中问题越多越严厉的非线性趋势。3个缺陷比2个缺陷严重得多，而非简单+1。

### 反谄媚复合规则
- 加权分>8且缺陷数≥3：强制降分至与缺陷数匹配范围，标记`"warning":"评分与缺陷不匹配"`
- 硬性拒绝原因存在时：即使原始分≥9.0，pass_probability ≤ 60
- 所有维度得分完全相同（方差<0.5）：触发重新评估警告

### 弱点放大机制（仅 adversarial 模式）

当发现缺陷时，自动推断关联缺陷，形成弱点链：

| 原始缺陷 | → 推断缺陷（第1层） | → 推断缺陷（第2层） |
|----------|---------------------|---------------------|
| 无安全设计 | 可能存在数据泄露风险 | 合规审计不通过，面临罚款 |
| 无竞品分析 | 市场定位不清晰 | 商业化可行性存疑，投资者不信任 |
| 架构文档缺失 | 技术债可能严重 | 维护成本不可控，扩展性受限 |
| 无测试覆盖 | 代码质量不可验证 | 生产故障率高，用户流失 |
| 无用户验证 | 需求可能不存在 | 产品无人使用，投资浪费 |
| 团队背景不明 | 执行能力存疑 | 交付延期，产品失败 |
| 无成本估算 | 商业模式不可行 | 资金链断裂风险 |
| 无退出策略 | 沉没成本风险 | 无法安全下线，数据损失 |

**弱点放大规则**:
- 每个原始缺陷至少推断 1 层关联缺陷
- 最多推断 2 层（避免过度推测）
- 推断结果加入 rejection_reasons 和 weakness_chain
- 若发现 ≥2 个 kill factors，pass_probability 降至 ≤20

### 预设质疑清单（仅 adversarial 模式）

敌对评审 SHALL 主动提出至少 5 个尖锐质疑问题，从 hostile_questions 数组输出：

1. "为什么现有方案不能解决这个问题？你的方案比现有方案好在哪里？"
2. "如果你的方案失败了，最可能的原因是什么？"
3. "有什么证据证明用户真的需要这个？有调研数据还是假设？"
4. "如果竞争对手（如[行业巨头]）复制你的方案，你的护城河是什么？"
5. "你的方案中最大的技术/商业假设是什么？如何验证或证伪？"
6. "你如何证明你的团队有能力执行这个方案？"
7. "你的成本结构和盈利路径是什么？多久能盈亏平衡？"
8. "如果监管机构改变规则（如数据安全法/反垄断），你的方案如何应对？"

**规则**:
- 至少输出 5 个问题，最多 8 个
- 问题必须针对当前项目的具体弱点（非通用问题）
- 至少 1 个问题针对技术可行性
- 至少 1 个问题针对商业可行性
- 至少 1 个问题针对执行能力

## Output
```json
{"review_type":"<type>","pass_probability":<5-95>,"scores":{"维度1":<0-10>,"...":<0-10>,"trust":<0-10>},"weighted_score":<0.0-10.0>,"rejection_reasons":["string"],"suggestions":["string"],"sycophancy_warnings":["string"],"hostile_questions":["string"],"weakness_chain":[{"original":"<string>","inferred_layer1":"<string>","inferred_layer2":"<string>"}],"kill_factors":["string"]}
```
评分：8-10充分；5-7基本；2-4简略；0-1缺失
sycophancy_warnings: 反讨好机制触发的警告列表，无警告时为空数组[]
hostile_questions: 敌对评审的尖锐质疑问题（仅 adversarial 模式非空）
weakness_chain: 弱点放大链（原始缺陷→推断缺陷），仅 adversarial 模式非空
kill_factors: 致命缺陷列表（可导致项目彻底失败），仅 adversarial 模式非空

## Output Schema

### JSON Schema Definition
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "review_type": {
      "type": "string",
      "enum": ["technical", "investment", "product", "opensource", "adversarial"],
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
    },
    "sycophancy_warnings": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 },
      "description": "反讨好机制触发的警告列表"
    },
    "hostile_questions": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 },
      "minItems": 0,
      "maxItems": 8,
      "description": "敌对评审的尖锐质疑问题"
    },
    "weakness_chain": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "original": { "type": "string", "minLength": 1, "description": "原始缺陷" },
          "inferred_layer1": { "type": "string", "minLength": 1, "description": "第1层推断缺陷" },
          "inferred_layer2": { "type": "string", "minLength": 0, "description": "第2层推断缺陷（可选）" }
        },
        "required": ["original", "inferred_layer1"],
        "additionalProperties": false
      },
      "minItems": 0,
      "description": "弱点放大链"
    },
    "kill_factors": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 },
      "minItems": 0,
      "description": "致命缺陷列表"
    }
  },
  "required": ["review_type", "pass_probability", "scores", "weighted_score", "rejection_reasons", "suggestions", "sycophancy_warnings", "hostile_questions", "weakness_chain", "kill_factors"],
  "additionalProperties": false
}
```

### 字段类型说明
| 字段 | 类型 | 必填 | 取值范围 | 说明 |
|------|------|------|----------|------|
| review_type | string | ✅ | technical / investment / product / opensource / adversarial | 评审类型，混合时选最主要类型 |
| pass_probability | integer | ✅ | 5–95 | 通过概率百分比，普通模式10-95，敌对模式5-75 |
| scores | object | ✅ | 每维度 0–10 | 按评审类型对应维度评分，必须含 `trust` |
| weighted_score | number | ✅ | 0.0–10.0 | 加权总分，保留1位小数 |
| rejection_reasons | array | ✅ | 非空字符串数组 | 可为空数组 `[]` |
| suggestions | array | ✅ | 非空字符串数组 | 可为空数组 `[]` |
| sycophancy_warnings | array | ✅ | 非空字符串数组 | 反讨好机制触发的警告列表，无警告时可为空数组 `[]` |
| hostile_questions | array | ✅ | 0-8个 | 敌对评审的尖锐质疑问题，非 adversarial 模式为空数组 `[]` |
| weakness_chain | array | ✅ | 非空对象数组 | 弱点放大链（原始缺陷→推断缺陷），非 adversarial 模式为空数组 `[]` |
| kill_factors | array | ✅ | 非空字符串数组 | 致命缺陷列表，非 adversarial 模式为空数组 `[]` |

### 验证规则
- **格式约束**: 输出必须为单行纯JSON，不得包含换行符、代码块标记或额外文本
- **pass_probability 范围**: 普通模式 10–95，敌对模式 5–75
- **scores 范围**: 每个维度分数必须在 0–10 之间（含边界），类型为 number
- **scores 必须含 trust**: 无论评审类型，`scores` 对象必须包含 `trust` 键
- **weighted_score 精度**: 浮点数，范围 0.0–10.0，最多保留1位小数
- **数组元素非空**: `rejection_reasons` 和 `suggestions` 的每个元素必须为非空字符串
- **敌对模式验证**: adversarial 模式下 `hostile_questions` 必须 ≥5 个，`weakness_chain` 非空，`kill_factors` ≥1 个
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

### Adversarial 模式示例
```
Input: {"persona":"开发者","problem":"多模型切换成本高","solution":"AI工作流系统，支持多模型调度","outcome":"提升开发效率"}
Output: {"review_type":"adversarial","pass_probability":30,"scores":{"技术脆弱性":3,"商业风险":4,"执行能力":2,"合规法律":3,"致命缺陷":2,"trust":3},"weighted_score":2.8,"rejection_reasons":["无架构图，技术债可能严重","无竞品分析，市场定位不清晰","无安全设计，数据泄露风险","无用户验证数据，需求可能是伪需求","团队背景不明，执行能力存疑","量化指标缺失，'提升效率'不可验证"],"suggestions":["补充架构设计文档","进行竞品对比分析","增加安全设计方案","提供用户调研数据","量化效率提升指标"],"sycophancy_warnings":[],"hostile_questions":["为什么现有AI工作流工具（如LangChain/CrewAI）不能解决这个问题？","如果OpenAnthropic推出原生工作流功能，你的护城河是什么？","有什么证据证明开发者愿意为此付费？","你的方案中最大的技术假设是什么？如何验证？"],"weakness_chain":[{"original":"无架构图","inferred_layer1":"技术债可能严重","inferred_layer2":"维护成本不可控"},{"original":"无竞品分析","inferred_layer1":"市场定位不清晰","inferred_layer2":"商业化可行性存疑"}],"kill_factors":["无用户验证数据→需求可能是伪需求→产品可能无人使用"]}
```

## Anti-Patterns — 四层反讨好防护

### Layer 1: 词汇级检测
| 反模式 | 触发条件 | 后果 |
|--------|----------|------|
| 空泛赞美 | 出现"优秀/完美/出色/一流/极佳/卓越"但无具体证据 | trust分-2，记录sycophancy_warning |
| 过度修饰 | 同一维度描述中≥3个正面形容词 | 该维度分数上限-2 |

### Layer 2: 结构级检测
| 反模式 | 触发条件 | 后果 |
|--------|----------|------|
| 缺陷遗漏 | rejection_reasons为空但输入含"未明确"/"推断" | 强制生成rejection_reasons，标记sycophancy_warning |
| 建议缺失 | suggestion数量<rejection_reason数量且pass_probability>60 | 补充suggestion，pass_probability-10 |

### Layer 3: 分数级检测
| 反模式 | 触发条件 | 后果 |
|--------|----------|------|
| 高分低覆盖 | 维度给9-10分但该维度对应检查项<50%覆盖 | 强制降至6分 |
| 分数均匀化 | 所有维度得分方差<0.5 | 触发重新评估，标记"缺乏差异化判断" |
| 缺陷不匹配 | 加权分>8且缺陷数≥3 | 按非线性递减公式重算 |

### Layer 4: 模式级检测
| 反模式 | 触发条件 | 后果 |
|--------|----------|------|
| 连续高分 | 连续3次评审pass_probability>70 | 进入严格模式（所有权重×1.2） |
| 安全回避 | 安全问题给分≥7但输入无安全设计 | 强制安全分降至4，标记sycophancy_warning |
| 合规回避 | 合规问题给分≥7但输入无合规声明 | 强制合规相关分降至4 |

### Layer 5: 敌对评审模式检测
| 反模式 | 触发条件 | 后果 |
|--------|----------|------|
| 敌对模式给高分 | adversarial 模式下 pass_probability >50 | 触发审查，疑似未执行敌对策略 |
| 弱点链不足 | 发现的缺陷数 <3 但 weakness_chain 为空 | 自动搜索更多缺陷并推断 |
| 无kill_factors | adversarial 模式 kill_factors 为空 | 必须至少找出 1 个潜在致命缺陷 |
| 质疑问题过少 | hostile_questions 数量 <5 | 补充尖锐问题至≥5个 |
| 敌对模式无推断 | 仅列出缺陷未做弱点放大 | 执行弱点放大机制 |

## Edge Cases
| 边界场景 | 处理方式 |
|----------|----------|
| 输入仅含persona，无problem/solution | pass_probability=15，所有维度评分0-1，rejection_reasons标注"信息严重不足" |
| 输入内容自相矛盾（如方案与问题无关） | 以problem为准，solution标记"不匹配"扣20分 |
| 输入超长（>10000字符） | 仅提取核心信息评分，标注`"truncated":true` |
| 输入为纯技术细节无业务上下文 | 判定为technical类型，investment相关维度不适用但不输出，仅评technical+trust |
| 所有维度得分完全相同 | 触发评分合理性检查，要求重新评估各维度差异 |
| 输入含≥3个"未明确"/"推断"但pass_probability>50 | 触发隐藏讨好模式检测，强制降级pass_probability至≤40 |
| 连续评审pass_probability持续>70 | 进入严格模式：所有扣分项权重×1.2，上限分降至85 |
| adversarial 模式输入 | 应用敌对评审逻辑：基础分35，缺陷扣分×2，弱点放大，预设质疑 |
| adversarial 模式下所有字段"未明确" | pass_probability=5，输出完整weakness_chain和kill_factors |

## Quality Gates
输出前自检：
1. 每个维度（含trust）是否均在0-10范围内？
2. pass_probability是否在对应模式的范围内？（普通：10-95，敌对：5-75）
3. **Layer 1**: 是否存在无证据支撑的空泛赞美词？如有是否已降级trust分？
4. **Layer 2**: 是否存在明显缺陷但rejection_reasons为空？如有是否已生成？
5. **Layer 3**: 高分维度（9-10分）的检查项覆盖率是否≥50%？
6. **Layer 4**: 是否存在连续高分模式？是否触发严格模式？
7. 缺陷数量≥3时，是否应用了非线性递减公式？
8. 每个rejection_reason是否有对应的suggestion？
9. 是否所有维度得分完全相同（方差<0.5）？如是是否触发重新评估？
10. **敌对模式**: pass_probability是否≤75？如>75是否触发审查？
11. **敌对模式**: weakness_chain是否非空？至少包含1条弱点链？
12. **敌对模式**: kill_factors是否至少包含1个致命缺陷？
13. **敌对模式**: hostile_questions数量是否≥5？

## 方法论来源与学术诚信

本 Skill 的方法论来源于**作者亲自阅读以下书籍并提炼核心要点**，非 AI 自动处理或简单摘要。

| 启发来源 | 核心贡献 |
|----------|----------|
| [Accelerate](Nicole Forsgren 等) | DORA 指标、变革能力评估 |
| [Software Architecture Metrics](Ciceri, Farley, Ford) | 架构质量度量 |
| [AI Engineering](Chip Huyen) | AI 系统评估维度 |

> **声明**: 本 Skill 中的方法论启发自上述书籍（见表格），所有代码实现、示例和知识重构均为作者原创。建议读者支持正版，购买原书以获得更完整的论述和案例。
