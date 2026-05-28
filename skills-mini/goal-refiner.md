---
name: goal-refiner
description: 描述项目时提炼项目意图为 persona、problem、solution、outcome 四个核心字段，为后续技能提供结构化输入。
---

# Goal Refiner
**version**: 0.2.11
> Context: [base_context](../../knowledge/base_context.md)

## Role
提炼项目意图: `{persona, problem, solution, outcome}`。

## Input
| 字段 | 关键词 | 推断规则 |
|------|--------|----------|
| persona | 作为/针对/面向 | 技术→开发者；商业→企业；工具→终端用户；AI→AI开发者 |
| problem | 痛点/效率低/成本高 | 从功能反推，标注"（推断）" |
| solution | 开发/构建/实现 | 仅提取明确能力 |
| outcome | 目标/提升/降低 | 优先量化，否则"未明确" |

**验证与边界**: 最小输入≥5字；<10字/纯技术→推断标"（推断）"；空输入→全"未明确"；多目标/矛盾→取最主要/最新；字段缺失→"未明确"。

## Output
```json
{"persona":"<string>","problem":"<string>","solution":"<string>","outcome":"<string>"}
```
约束：四字段必存在、非空、无换行、纯JSON。

## Output Schema
```json
{"type":"object","required":["persona","problem","solution","outcome"],"additionalProperties":false,
 "properties":{
  "persona":{"type":"string","minLength":1,"description":"目标用户/角色"},
  "problem":{"type":"string","minLength":1,"description":"解决的痛点/问题"},
  "solution":{"type":"string","minLength":1,"description":"解决方案/核心能力"},
  "outcome":{"type":"string","minLength":1,"description":"预期目标/量化收益"}
 }}
```
- **格式**: 单行纯JSON，无代码块标记
- **必填**: 四字段缺一不可，不得为空串
- **推断**: 推断值必须含"（推断）"后缀

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
- **塞入单字段**：方案+outcome合并到problem，下游无法消费。
- **过度推断**：仅提技术栈却编造用户画像，persona失真。
- **矛盾未取舍**：persona说"企业"、problem说"个人开发者"。
- **outcome空泛**："变得更好"缺乏量化维度，下游无法评估。

## Edge Cases
- **纯技术术语**（如"K8s+Prometheus"）→ persona/solution标"（推断）"，problem/outcome写"未明确"。
- **互斥目标**（"既要极简又要企业级"）→ 取最新或标"多目标冲突，取最主要"。
- **多语言混合**→ 统一翻译为中文，保留关键术语原文。
- **超长输入（>500字）**→ 先提取关键词再映射四字段。

## Quality Gates
- [ ] 四字段都存在且非空？
- [ ] persona与problem无逻辑矛盾？
- [ ] 推断值是否标注"（推断）"？
- [ ] outcome可量化或可验证？
- [ ] 输出为单行纯JSON，无代码块和额外文本？

> Full version: skills/goal-refiner/SKILL.md
