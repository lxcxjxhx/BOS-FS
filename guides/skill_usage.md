# Skill 独立使用指南

> 每个 Skill 均可独立加载使用，无需运行完整 Pipeline。

## 通用规则

- 输入不足时，Skill 会标注"（推断）"或输出"未明确"
- 所有输出遵循单一职责原则，不依赖其他 Skill 的状态
- 可直接在对话中粘贴 Skill 内容，或读取对应 `.md` 文件

---

## 1. Goal Refiner

**文件**: `skills/01_goal_refiner.md`

**用途**: 将自然语言项目描述提炼为结构化目标

**最小输入**: 5 字以上的项目描述

**输入示例**:
```
"做了个AI工作流系统"
```

**输出格式**: JSON
```json
{"persona":"开发者（推断）","problem":"工作流配置繁琐（推断）","solution":"AI工作流系统","outcome":"未明确"}
```

**独立使用场景**: 快速理解任何项目描述的核心意图

---

## 2. Reviewer Simulator

**文件**: `skills/02_reviewer_simulator.md`

**用途**: 模拟四类评审（technical/investment/product/opensource），输出通过概率和改进建议

**最小输入**: persona, problem, solution 三个字段

**输入示例**:
```json
{"persona":"开发者","problem":"多模型切换成本高","solution":"AI工作流系统","outcome":"提升效率"}
```

**输出格式**: JSON
```json
{"review_type":"technical","pass_probability":65,"scores":{"架构设计":5,"代码质量":5,"安全性":4,"性能":5},"weighted_score":4.8,"rejection_reasons":["缺少架构文档"],"suggestions":["补充架构设计"]}
```

**独立使用场景**: 提交前预审、评审模拟、寻找改进方向

---

## 3. README Refactor

**文件**: `skills/03_readme_refactor.md`

**用途**: 将技术化 README 重构为五段式专业文档（What/Why/How/Result/Next）

**最小输入**: 20 字以上的原始 README 内容

**输入示例**:
```markdown
# My Project
AI workflow engine, multi-model, auto-test
```

**输出格式**: Markdown

**独立使用场景**: 优化任何项目文档、提升可读性

---

## 4. Outcome Mapper

**文件**: `skills/04_outcome_mapper.md`

**用途**: 将技术特性转换为用户价值（Feature → Capability → Outcome）

**最小输入**: 至少 1 个功能描述

**输入示例**:
```
"多模型调度"
```

**输出格式**: JSON
```json
{"feature":"多模型调度","capability":"智能资源分配","outcome":"减少重复配置与上下文切换"}
```

**独立使用场景**: 准备 pitch、文档优化、价值提炼

---

## 5. Submission Builder

**文件**: `skills/05_submission_builder.md`

**用途**: 构建完整提交包（8 个组件）

**必需输入**: name, version, description

**可选输入**: readme, outcome, persona, problem

**输出**: 提交包组件清单
```json
{"bundle_path":"submission_bundle/","components":["README.md","demo_guide.md","introduction.md","screenshots_guide.md","FAQ.md","risk_disclosure.md","trust_statement.md","bundle_meta.json"],"status":"complete"}
```

**独立使用场景**: 准备最终提交、生成完整项目材料

---

## 6. Reject Analyzer

**文件**: `skills/06_reject_analyzer.md`

**用途**: 分析被拒原因，提取真实问题，给出可操作的修复建议

**最小输入**: 拒绝说明文本（即使模糊也可处理）

**输入示例**:
```
"技术实现描述太底层，看不出用户价值"
```

**输出格式**: JSON
```json
{"real_issue":"表达太底层，用户价值弱","fixable_items":["技术描述转用户价值","增加场景描述","补充量化指标"],"resubmit_suggestion":"从'交付工具'重新定位为'交付平台'","matched_pattern":"表达太底层","confidence":0.85}
```

**独立使用场景**: 项目被拒后分析原因、针对性改进

---

## 推荐工作流

| 目标 | 推荐 Skill 顺序 |
|------|----------------|
| 快速优化描述 | Goal Refiner → Outcome Mapper |
| 准备提交 | Goal Refiner → README Refactor → Submission Builder |
| 预审改进 | Goal Refiner → Reviewer Simulator |
| 分析被拒 | Reject Analyzer → 针对性使用其他 Skill |
| 完整流程 | 使用 `skills/pipeline.md` 编排器 |
