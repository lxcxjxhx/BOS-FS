# 快速上手指南

## 前置条件

- **AI Agent 环境**：Cursor / Trae / Claude Code / OpenHands 等
- **项目代码或描述**：待优化的项目源码或项目说明

---

## 3 步快速开始

### Step 1: 加载 Skill

````
# Cursor
@skills/pipeline.md

# Trae
/skill bos-fs/pipeline

# 通用 LLM
读取 skills/pipeline.md 作为 system prompt
````

### Step 2: 输入项目描述

```
优化我的项目：[项目描述或粘贴 README]
```

### Step 3: 获取输出

| 阶段 | 输出内容 |
|------|----------|
| **Goal Refiner** | `{persona, problem, solution, outcome}` |
| **README Refactor** | What / Why / How / Result / Next 结构 |
| **Submission Builder** | 完整提交包 |

---

## Skill 独立使用示例

### Goal Refiner

```
加载: skills/01_goal_refiner.md
输入: "做了个AI工作流系统"
输出: {"persona":"开发者","problem":"工作流配置繁琐","solution":"AI工作流系统","outcome":"未明确"}
```

### Reviewer Simulator

```
加载: skills/02_reviewer_simulator.md
输入: {persona, problem, solution, outcome}
输出: {pass_probability, rejection_reasons, suggestions}
```

### README Refactor

```
加载: skills/03_readme_refactor.md
输入: 原始 README
输出: What/Why/How/Result/Next 结构
```

### Outcome Mapper

```
加载: skills/04_outcome_mapper.md
输入: "多模型调度"
输出: {"feature":"多模型调度","capability":"智能资源分配","outcome":"减少重复配置"}
```

### Submission Builder

```
加载: skills/05_submission_builder.md
输入: {persona, problem, solution, outcome, readme}
输出: 完整 submission_bundle/
```

### Reject Analyzer

```
加载: skills/06_reject_analyzer.md
输入: "技术实现描述太底层，看不出用户价值"
输出: {real_issue, fixable_items, resubmit_suggestion}
```

---

## 完整 Pipeline 使用示例

```
输入: "做了一个 AI 工作流系统，支持多模型调度，可以自动测试和发布"

Step 1 → Understand: 提炼 persona / problem / solution / outcome
Step 2 → Map:       Feature → Capability → Outcome 转换
Step 3 → Refactor:  README 重构为五段式
Step 4 → Review:    四类评审模拟，获取通过概率和建议
Step 5 → Build:     生成完整提交包（README / Demo / Pitch / FAQ / 风险声明 / 信任声明）
```

---

## 常见问题

**Q: 输出是 JSON 格式还是 Markdown？**
A: Goal Refiner / Outcome Mapper / Reviewer Simulator 输出 JSON；README Refactor / Submission Builder 输出 Markdown。

**Q: 如何单独使用某个 Skill？**
A: 直接加载对应的 `skills/0X_xxx.md` 文件，按文件中的输入格式提供数据。

**Q: 评审通过率多少算合格？**
A: 技术评审 > 70% 为合格，50–70% 需要改进，< 50% 需要大幅修改。

**Q: 信任声明是什么？**
A: 基于权威框架（OWASP / ISO 25010 / DORA 等）的技术可信度声明，详见 [knowledge/trust_signals.md](../knowledge/trust_signals.md)。
