---
name: goal-refiner
description: 描述项目时提炼项目意图为 persona、problem、solution、outcome 四个核心字段，为后续技能提供结构化输入。
---

# Goal Refiner
**version**: 0.3.0
> Context: [base_context](../knowledge/base_context.md)
> Flexibility: [flexibility_principles](../../knowledge/adoption/flexibility_principles.md)

## Role
提炼项目意图: `{persona, problem, solution, outcome}`。

## Rules
| 字段 | 关键词 | 推断 |
|------|--------|------|
| persona | 作为/针对/面向 | 技术→开发者；商业→企业；工具→终端用户；AI→AI开发者 |
| problem | 痛点/效率低/成本高 | 从功能反推，标注"（推断）" |
| solution | 开发/构建/实现 | 仅提取明确能力 |
| outcome | 目标/提升/降低 | 优先量化，否则"未明确" |

## Boundary
描述<10字/纯技术→推断标注"（推断）"；字段缺失→"未明确"；多目标/矛盾→取最主要/最新

## Input Validation
- 最小输入: 项目描述 ≥ 5 字
- 描述 < 10 字 → 推断标注"（推断）"
- 空输入 → 输出 {"persona":"未明确","problem":"未明确","solution":"未明确","outcome":"未明确"}
- 多目标/矛盾 → 取最主要/最新

## Error Handling
- 输入为空/缺失 → 输出错误信息并说明需要补充
- 字段缺失 → 标注"未明确"
- 矛盾信息 → 取最新/最主要的

## Output
```json
{"persona":"<string>","problem":"<string>","solution":"<string>","outcome":"<string>"}
```
约束：四字段必存在；非空；无换行；纯JSON。

## 扩展输出

核心四字段 `persona`/`problem`/`solution`/`outcome` **MUST** 始终存在，保证向后兼容和下游 Skill 正常消费。

根据项目类型，**MAY** 添加以下扩展字段（不影响核心字段消费）：

| 项目类型 | 扩展字段 | 说明 |
|----------|----------|------|
| 工具类项目 | `tech_stack`, `install_command` | 技术栈、安装命令 |
| 商业项目 | `target_market`, `revenue_model`, `competitors` | 目标市场、盈利模式、竞品 |
| 开源项目 | `license`, `contribution_guide` | 开源协议、贡献指南 |
| 安全交付 | `risk_level`, `remediation_priority` | 风险等级、修复优先级 |

扩展字段使用规则：
- 扩展字段为 **MAY** 级别，可根据上下文判断是否添加
- 扩展字段**不得替代**核心四字段，核心字段仍为 MUST
- 下游 Skill 仅依赖核心四字段，扩展字段为附加信息
- 扩展字段值也应遵循非空、单行约束

## Output Schema

### JSON Schema Definition
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "persona": { "type": "string", "minLength": 1, "description": "目标用户/角色" },
    "problem": { "type": "string", "minLength": 1, "description": "解决的痛点/问题" },
    "solution": { "type": "string", "minLength": 1, "description": "解决方案/核心能力" },
    "outcome": { "type": "string", "minLength": 1, "description": "预期目标/量化收益" },
    "tech_stack": { "type": "string", "minLength": 1, "description": "技术栈（工具类项目可选）" },
    "install_command": { "type": "string", "minLength": 1, "description": "安装命令（工具类项目可选）" },
    "target_market": { "type": "string", "minLength": 1, "description": "目标市场（商业项目可选）" },
    "revenue_model": { "type": "string", "minLength": 1, "description": "盈利模式（商业项目可选）" },
    "competitors": { "type": "string", "minLength": 1, "description": "竞品（商业项目可选）" },
    "license": { "type": "string", "minLength": 1, "description": "开源协议（开源项目可选）" },
    "contribution_guide": { "type": "string", "minLength": 1, "description": "贡献指南（开源项目可选）" },
    "risk_level": { "type": "string", "minLength": 1, "description": "风险等级（安全交付可选）" },
    "remediation_priority": { "type": "string", "minLength": 1, "description": "修复优先级（安全交付可选）" }
  },
  "required": ["persona", "problem", "solution", "outcome"],
  "additionalProperties": true
}
```

### 字段类型说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| persona | string | ✅ MUST | 目标用户群体，可为推断值（标注"（推断）"） |
| problem | string | ✅ MUST | 解决的痛点，可为推断值（标注"（推断）"） |
| solution | string | ✅ MUST | 方案描述，仅提取明确能力 |
| outcome | string | ✅ MUST | 量化目标优先，否则"未明确" |
| tech_stack | string | ❌ MAY | 技术栈（工具类项目） |
| install_command | string | ❌ MAY | 安装命令（工具类项目） |
| target_market | string | ❌ MAY | 目标市场（商业项目） |
| revenue_model | string | ❌ MAY | 盈利模式（商业项目） |
| competitors | string | ❌ MAY | 竞品（商业项目） |
| license | string | ❌ MAY | 开源协议（开源项目） |
| contribution_guide | string | ❌ MAY | 贡献指南（开源项目） |
| risk_level | string | ❌ MAY | 风险等级（安全交付） |
| remediation_priority | string | ❌ MAY | 修复优先级（安全交付） |

### 验证规则
- **格式约束**: 输出必须为单行纯JSON，不得包含换行符、代码块标记（```）或额外文本
- **必填字段**: `persona`, `problem`, `solution`, `outcome` 四个字段 **MUST** 存在，缺一不可
- **非空校验**: 所有字段值不得为空字符串 `""`，最小长度为1
- **扩展字段**: 扩展字段 **MAY** 根据项目类型添加，但核心四字段 MUST 始终存在
- **推断标注**: 推断值必须包含"（推断）"后缀，便于下游识别
- **下游兼容**: 下游 Skill 仅消费核心四字段，扩展字段不应影响下游逻辑

## Examples
```
Input: "企业研发团队，交付效率低，缺标准化。方案：自动化交付系统。目标：提升50%。"
Output: {"persona":"企业研发团队","problem":"交付效率低，缺标准化","solution":"自动化交付系统","outcome":"效率提升50%"}

Input: "做了个AI工作流系统"
Output: {"persona":"开发者（推断）","problem":"工作流配置繁琐（推断）","solution":"AI工作流系统","outcome":"未明确"}

Input: "中小商家，智能库存管理，减少盘点时间，节省30%人力"
Output: {"persona":"中小商家","problem":"人工盘点耗时","solution":"智能库存管理系统","outcome":"节省30%人力"}

Input: "基于LangChain的多Agent框架，支持RAG和Function Calling"
Output: {"persona":"AI开发者","problem":"多Agent协作复杂、需统一框架","solution":"基于LangChain的多Agent框架，支持RAG和Function Calling","outcome":"降低多Agent开发门槛（推断）"}

Input: "Python CLI工具，用Click+Rich构建，pip install mytool，面向开发者，解决依赖管理混乱问题，目标是简化安装流程"
Output: {"persona":"开发者","problem":"依赖管理混乱","solution":"Python CLI工具，基于Click+Rich","outcome":"简化安装流程","tech_stack":"Python+Click+Rich","install_command":"pip install mytool"}

Input: "SaaS CRM系统，面向中小企业销售团队，月费199起，竞品Salesforce，目标获取1000家客户"
Output: {"persona":"中小企业销售团队","problem":"客户管理效率低、缺少轻量CRM（推断）","solution":"SaaS CRM系统","outcome":"获取1000家付费客户","target_market":"中小企业","revenue_model":"月费199起SaaS订阅","competitors":"Salesforce"}
```

## Anti-Patterns
- **将全部描述塞进一个字段**：如把方案和outcome合并到problem，下游skill无法独立消费。
- **过度推断未提及信息**：输入仅提技术栈却编造用户画像，导致persona失真。
- **矛盾字段未取舍**：persona说"企业"、problem却说"个人开发者"，输出前后矛盾。
- **outcome写空泛口号**：如"变得更好"缺乏量化或可验证维度，下游无法评估。
- **扩展字段替代核心字段**：只写了tech_stack却缺少persona/problem/solution/outcome，下游无法消费。
- **扩展字段与核心字段矛盾**：如persona写"个人开发者"但target_market写"大型企业"。

## Edge Cases
- **纯技术术语无业务描述**（如"K8s+Prometheus+Grafana"）→ persona/solution标注"（推断）"，problem/outcome写"未明确"。
- **一句话包含互斥目标**（"既要极简又要企业级功能"）→ 取最新出现的或标注"多目标冲突，取最主要"。
- **多语言混合描述**→ 统一翻译为中文输出，保留关键术语原文。
- **超长输入（>500字）**→ 先提取关键词再映射四字段，避免信息丢失。
- **项目类型不明确**→ 仅输出核心四字段，不添加扩展字段。
- **部分扩展信息缺失**→ 只添加可确认的扩展字段，不强行推断。

## Quality Gates
- [ ] 四字段是否都存在且非空？（MUST）
- [ ] persona与problem是否存在逻辑矛盾？（如企业级工具却针对个人用户）
- [ ] 推断值是否都标注了"（推断）"？
- [ ] outcome是否可量化或可验证？（非"更好/更快"等空泛描述）
- [ ] 输出是否为单行纯JSON，无代码块标记和额外文本？
- [ ] 扩展字段（如有）是否与核心字段逻辑一致？
- [ ] 扩展字段是否仅在有明确依据时添加？（不强行推断）

## 方法论来源与学术诚信

本 Skill 的方法论来源于**作者亲自阅读以下书籍并提炼核心要点**，非 AI 自动处理或简单摘要。

| 启发来源 | 核心贡献 |
|----------|----------|
| [Continuous Discovery Habits](Teresa Torres) | persona/problem 提取方法论 |
| [Product Management in Practice](Matt LeMay) | 用户价值定义 |

> **声明**: 本 Skill 中的方法论启发自上述书籍（见表格），所有代码实现、示例和知识重构均为作者原创。建议读者支持正版，购买原书以获得更完整的论述和案例。
