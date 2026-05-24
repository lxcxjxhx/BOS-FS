---
name: goal-refiner
description: 描述项目时提炼项目意图为 persona、problem、solution、outcome 四个核心字段，为后续技能提供结构化输入。
---

# Goal Refiner
> Context: [base_context](../knowledge/base_context.md)

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
    "outcome": { "type": "string", "minLength": 1, "description": "预期目标/量化收益" }
  },
  "required": ["persona", "problem", "solution", "outcome"],
  "additionalProperties": false
}
```

### 字段类型说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| persona | string | ✅ | 目标用户群体，可为推断值（标注"（推断）"） |
| problem | string | ✅ | 解决的痛点，可为推断值（标注"（推断）"） |
| solution | string | ✅ | 方案描述，仅提取明确能力 |
| outcome | string | ✅ | 量化目标优先，否则"未明确" |

### 验证规则
- **格式约束**: 输出必须为单行纯JSON，不得包含换行符、代码块标记（```）或额外文本
- **必填字段**: `persona`, `problem`, `solution`, `outcome` 四个字段缺一不可
- **非空校验**: 所有字段值不得为空字符串 `""`，最小长度为1
- **禁止额外字段**: 不允许出现schema定义之外的字段
- **推断标注**: 推断值必须包含"（推断）"后缀，便于下游识别

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
```

## Anti-Patterns
- **将全部描述塞进一个字段**：如把方案和outcome合并到problem，下游skill无法独立消费。
- **过度推断未提及信息**：输入仅提技术栈却编造用户画像，导致persona失真。
- **矛盾字段未取舍**：persona说"企业"、problem却说"个人开发者"，输出前后矛盾。
- **outcome写空泛口号**：如"变得更好"缺乏量化或可验证维度，下游无法评估。

## Edge Cases
- **纯技术术语无业务描述**（如"K8s+Prometheus+Grafana"）→ persona/solution标注"（推断）"，problem/outcome写"未明确"。
- **一句话包含互斥目标**（"既要极简又要企业级功能"）→ 取最新出现的或标注"多目标冲突，取最主要"。
- **多语言混合描述**→ 统一翻译为中文输出，保留关键术语原文。
- **超长输入（>500字）**→ 先提取关键词再映射四字段，避免信息丢失。

## Quality Gates
- [ ] 四字段是否都存在且非空？
- [ ] persona与problem是否存在逻辑矛盾？（如企业级工具却针对个人用户）
- [ ] 推断值是否都标注了"（推断）"？
- [ ] outcome是否可量化或可验证？（非"更好/更快"等空泛描述）
- [ ] 输出是否为单行纯JSON，无代码块标记和额外文本？
