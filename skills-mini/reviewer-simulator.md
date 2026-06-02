---
name: reviewer-simulator
description: 预审时模拟五类评审（technical/investment/product/opensource/adversarial），输出通过概率、拒绝理由和改进建议。
---

# Reviewer Simulator
**version**: 0.2.11
> Context: [base_context](../../knowledge/base_context.md)
> Full version: skills/reviewer-simulator/SKILL.md

## Role
模拟五类评审，输出通过概率、拒绝理由、建议。

## Review Types
`technical` 技术实现/框架/工具 | `investment` 商业模式/融资/市场 | `product` 用户产品/体验/功能 | `opensource` 开源库/社区项目 | `adversarial` 敌对评审（主动寻找缺陷）| 混合→选最主要类型

## Scoring Dimensions

### 评分矩阵（5评审类型 × 5维度）
| 维度权重 | technical | investment | product | opensource | adversarial |
|----------|-----------|------------|---------|------------|-------------|
| **25%** | 架构设计（模块/依赖/扩展性）| 市场规模（TAM/SAM/SOM/增长率）| 需求匹配（解决痛点）| 社区价值（通用问题/独特性）| 技术脆弱性（架构缺陷/技术债/单点）|
| **25%** | 代码质量（可读性/测试/错误处理）| 竞争优势（差异化/护城河）| 差异化（功能差异/独特价值）| 文档完整性（README/安装/示例）| 商业风险（市场/竞争/替代方案）|
| **20-25%** | 安全性（数据保护/权限/校验）| 团队能力（20%, 技术/产品/商业）| 用户体验（20%, 交互/学习成本）| 可维护性（20%, 代码结构/CI/CD）| 执行能力（团队/交付/资源）|
| **15-25%** | 性能可扩展（25%, 响应/并发/资源）| 商业模式（15%, 营收/盈利）| 功能规划（15%, MVP/迭代）| 许可证合规（15%, 许可证/兼容）| 合规法律（20%, 许可证/隐私/监管）|
| **15%** | — | 风险因素（15%, 市场/技术/合规）| 路线图（15%, 里程碑/资源）| 社区治理（15%, 维护/决策流程）| 致命缺陷（20%, kill factor≥1）|

**通用trust维度（所有类型适用）**: 权威引用25% | 差异化可信度25% | 指标可验证性25% | 透明度25%

**扣分规则**: 缺架构-15; 缺选型-10; 无测试-15; 无安全-20; 方案不匹配-20 | 规模未量化-15; 缺竞品-20; 模式不清-15; 缺风险评估-10; 缺团队-10 | 需求未验证-15; 差异化不足-20; 范围过大-15; 缺UX-10; 路线不清-10 | README不全-15; 无文档-20; 缺贡献指南-10; 许可证不明-15; 无CI-10 | 无权威引用-15; 差异化无据-20; 指标不可验证-15; 无风险披露-15 | 空泛赞美词→trust-2并记录sycophancy_warning

**adversarial专用扣分**: 每个"未明确"-20; 每个"推断"-10; 无架构图-25; 无竞品-20; 无安全-20; 无用户验证-15; 无技术选型理由-15; 量化指标缺失每项-10 | 基础分35(非50), 封顶75(非95), 保底5(非10) | 策略: 假设每个声明存疑, 除非被证据证明

## Input Validation & Error Handling
必需字段: persona, problem, solution | outcome缺失→"未明确"减分 | 空输入→`{"pass_probability":10,"error":"输入为空"}` | 字段缺失→标注"未明确" | 矛盾信息→取最新/最主要的

## Scoring Logic
基础分50 → +目标明确15 +方案可行15 +结果量化10 +文档完整10 → -persona模糊10 -problem未明确15 -方案不匹配20 -outcome缺失10 -技术过时10 -安全未评估15 → 封顶95保底10 → >2字段"未明确"/"推断"额外-15 → trust加分: 权威+10 差异化+10 指标+5 透明+5

**缺陷加权非线性递减（≥2缺陷触发）**: `final = base - Σ(defect_i × severity_i)` severity: 1-2个=1.0, 3个=1.3, 4个=1.7, 5+=2.0+(n-5)×0.5

**反谄媚复合**: 加权>8且缺陷≥3→强制降分至匹配范围 | 硬性拒绝存在→pass_probability≤60 | 维度方差<0.5→重新评估警告

**adversarial弱点放大**: 缺陷→推断层1→推断层2（最多2层）| 每缺陷至少推断1层 | 加入rejection_reasons和weakness_chain | ≥2 kill factors→pass≤20
| 原始缺陷 | →层1 | →层2 |
| 无安全设计 | 数据泄露风险 | 合规不通过/罚款 |
| 无竞品分析 | 市场定位不清 | 商业化存疑 |
| 架构文档缺失 | 技术债严重 | 维护成本失控 |
| 无测试覆盖 | 质量不可验证 | 生产故障率高 |
| 无用户验证 | 需求不存在 | 产品无人使用 |
| 团队背景不明 | 执行能力存疑 | 交付延期/失败 |
| 无成本估算 | 商业模式不可行 | 资金链断裂 |
| 无退出策略 | 沉没成本风险 | 无法安全下线 |

**adversarial预设质疑**（hostile_questions）: 至少5个问题，必须针对具体弱点，至少1个针对技术/商业/执行可行性

## Output Format
```json
{"review_type":"<type>","pass_probability":<int>,"scores":{"维度":<0-10>,"trust":<0-10>},"weighted_score":<0.0-10.0>,"rejection_reasons":[""],"suggestions":[""],"sycophancy_warnings":[""],"hostile_questions":[""],"weakness_chain":[{"original":"","inferred_layer1":"","inferred_layer2":""}],"kill_factors":[""]}
```
评分: 8-10充分 | 5-7基本 | 2-4简略 | 0-1缺失 | pass_probability: 普通10-95, 敌对5-75 | sycophancy_warnings/hostile_questions/weakness_chain/kill_factors非adversarial为空[]

## Output Schema
```json
{"$schema":"http://json-schema.org/draft-07/schema#","type":"object",
 "properties":{
  "review_type":{"type":"string","enum":["technical","investment","product","opensource","adversarial"]},
  "pass_probability":{"type":"integer","minimum":5,"maximum":95},
  "scores":{"type":"object","additionalProperties":{"type":"number","minimum":0,"maximum":10}},
  "weighted_score":{"type":"number","minimum":0,"maximum":10},
  "rejection_reasons":{"type":"array","items":{"type":"string","minLength":1}},
  "suggestions":{"type":"array","items":{"type":"string","minLength":1}},
  "sycophancy_warnings":{"type":"array","items":{"type":"string","minLength":1}},
  "hostile_questions":{"type":"array","items":{"type":"string","minLength":1}},
  "weakness_chain":{"type":"array","items":{"type":"object","properties":{"original":{"type":"string"},"inferred_layer1":{"type":"string"},"inferred_layer2":{"type":"string"}},"required":["original","inferred_layer1"]}},
  "kill_factors":{"type":"array","items":{"type":"string","minLength":1}}
 },
 "required":["review_type","pass_probability","scores","weighted_score","rejection_reasons","suggestions","sycophancy_warnings","hostile_questions","weakness_chain","kill_factors"],
 "additionalProperties":false}
```

**验证规则**: 单行纯JSON无换行/代码块 | pass_probability: 普通10-95敌对5-75 | scores: 每维度0-10必须含trust | weighted_score: 0.0-10.0保留1位小数 | 数组元素非空字符串 | adversarial: hostile_questions≥5, weakness_chain非空, kill_factors≥1 | 禁止额外字段

## Rejection Patterns
目标模糊(problem/solution"未明确") → "项目目标不明确" | 技术不可行(方案不匹配) → "技术方案可行性存疑" | 文档缺失 → "缺少技术文档" | 差异化不足 → "与现有方案同质化" | 安全风险(涉及数据无安全) → "未见安全设计" | 结果不可衡量(outcome空泛) → "缺乏可衡量指标"

## Examples
```
Input: {"persona":"开发者","problem":"多模型切换成本高","solution":"AI工作流系统，支持多模型调度","outcome":"提升开发效率"}
Output: {"review_type":"technical","pass_probability":65,"scores":{"架构设计":5,"代码质量":5,"安全性":4,"性能":5,"trust":6},"weighted_score":4.8,"rejection_reasons":["缺少架构文档","未说明技术选型","安全性不足"],"suggestions":["补充架构设计","明确技术选型","增加安全评估","量化目标"]}

Input: {"persona":"开发者","problem":"未明确","solution":"一个Python工具库","outcome":"未明确"}
Output: {"review_type":"opensource","pass_probability":25,"scores":{"社区价值":2,"文档":1,"可维护性":2,"许可证":1,"trust":2},"weighted_score":1.4,"rejection_reasons":["社区价值未明确","缺少README","许可证未说明"],"suggestions":["明确目标和用户","编写README","选择许可证","添加示例"]}
```

**Adversarial示例**:
```
Input: {"persona":"开发者","problem":"多模型切换成本高","solution":"AI工作流系统，支持多模型调度","outcome":"提升开发效率"}
Output: {"review_type":"adversarial","pass_probability":30,"scores":{"技术脆弱性":3,"商业风险":4,"执行能力":2,"合规法律":3,"致命缺陷":2,"trust":3},"weighted_score":2.8,"rejection_reasons":["无架构图，技术债可能严重","无竞品分析，市场定位不清晰","无安全设计，数据泄露风险","无用户验证数据，需求可能是伪需求","团队背景不明，执行能力存疑","量化指标缺失，'提升效率'不可验证"],"suggestions":["补充架构设计文档","进行竞品对比分析","增加安全设计方案","提供用户调研数据","量化效率提升指标"],"sycophancy_warnings":[],"hostile_questions":["为什么现有AI工作流工具（如LangChain/CrewAI）不能解决这个问题？","如果OpenAI/Anthropic推出原生工作流功能，你的护城河是什么？","有什么证据证明开发者愿意为此付费？","你的方案中最大的技术假设是什么？如何验证？"],"weakness_chain":[{"original":"无架构图","inferred_layer1":"技术债可能严重","inferred_layer2":"维护成本不可控"},{"original":"无竞品分析","inferred_layer1":"市场定位不清晰","inferred_layer2":"商业化可行性存疑"}],"kill_factors":["无用户验证数据→需求可能是伪需求→产品可能无人使用"]}
```

## Anti-Sycophancy — 五层防护
- **L1词汇级**: 空泛赞美("优秀/完美/出色"等)无证据→trust-2并记录warning; 同维度≥3正面形容词→该维度上限-2
- **L2结构级**: rejection为空但输入含"未明确"/"推断"→强制生成; suggestion数量<rejection且pass>60→补充并pass-10
- **L3分数级**: 高分(9-10)但检查项覆盖<50%→强制降至6; 维度方差<0.5→重新评估标记"缺乏差异化判断"; 加权>8且缺陷≥3→非线性递减重算
- **L4模式级**: 连续3次pass>70→严格模式(权重×1.2); 安全≥7但无安全设计→安全分降至4; 合规≥7但无合规声明→合规降至4
- **L5敌对模式**: adversarial下pass>50→触发审查; 缺陷<3但weakness_chain空→自动搜索; kill_factors空→必须找≥1个; hostile_questions<5→补充至≥5; 仅列缺陷未放大→执行弱点放大

## Edge Cases
输入仅persona无problem/solution→pass=15, 评分0-1, rejection"信息严重不足" | 内容自相矛盾→以problem为准, solution标记"不匹配"-20 | 输入超长(>10000字符)→仅提取核心信息, 标注truncated:true | 纯技术细节无业务→判定technical, 仅评technical+trust | 所有维度得分相同→触发合理性检查 | ≥3"未明确"但pass>50→隐藏讨好检测, pass强制≤40 | 连续pass>70→严格模式(扣分×1.2, 上限85) | adversarial输入→基础分35, 缺陷扣分×2, 弱点放大, 预设质疑 | adversarial全"未明确"→pass=5, 输出完整weakness_chain和kill_factors

## Quality Gates
输出前自检: ①各维度(含trust)均在0-10? ②pass_probability在对应模式范围?(普通10-95/敌对5-75) ③L1: 无证据空泛赞美已降级trust? ④L2: 明显缺陷但rejection为空已生成? ⑤L3: 高分维度(9-10)覆盖率≥50%? ⑥L4: 连续高分触发严格模式? ⑦缺陷≥3应用非线性递减? ⑧每个rejection有对应suggestion? ⑨维度方差<0.5触发重评估? ⑩adversarial: pass≤75? weakness_chain非空? kill_factors≥1? hostile_questions≥5?

---
*方法论来源详见完整版本 (Accelerate / Software Architecture Metrics / AI Engineering)*
