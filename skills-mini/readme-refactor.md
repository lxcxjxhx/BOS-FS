---
name: readme-refactor
description: 优化文档时将原始项目描述重构为专业五段式 README（What/Why/How/Result/Next）。
---

# README Refactor
**version**: 0.2.11
> Context: [base_context](../../knowledge/base_context.md)
> Full version: skills/readme-refactor/SKILL.md

## Role
将项目描述重构为专业 README（What/Why/How/Result/Next）。

## Input/Output/Boundary
- **最小输入**: README ≥ 20 字；空输入→输出错误提示
- **输入不足**: 标注"（内容不足，仅重构现有信息）"
- **输出**: 完整 Markdown 文档，**不使用**代码包裹，直接输出原始文本

## Structure Template
```markdown
# [项目名称]
## What — 一句话价值
[技术 × 用户 × 收益 = 产品描述]
## Why — 为什么存在
### 痛点 - [用户问题]
### 现有方案不足 - [对比]
## How — 如何实现
### 架构
[ASCII图-含数据流]
### 特性 - [特性]: [价值]
### 快速开始
```bash
[可执行命令]
```
## Result — 效果
### 指标 - [量化收益]
### 场景 - [≥2典型场景]
## Next — 路线图
- [ ] 近期[1-3月] - [ ] 中期[3-6月] - [ ] 远期[6-12月]
```

## Transformation Table
| 原始 | 转换后 |
|------|--------|
| AI Workflow Engine | 帮助开发者自动转换需求为可交付资产 |
| 支持多模型 | 减少重复配置与上下文切换 |
| 模型调度 | 降低交付成本 |
| 自动测试 | 质量保障自动化 |
| CI/CD | 交付流水线 |
| 代码生成 | 开发效率提升 |

## Validation Rules
| 规则 | 约束 |
|------|------|
| 五段式完整性 | What/Why/How/Result/Next 缺一不可 |
| What非技术可理解 | 非技术人员可理解 |
| 架构图含数据流 | How段必须含ASCII架构图+数据流向 |
| 快速开始可执行 | 含可复制运行的bash命令 |
| 指标可量化 | Result段含具体数值/百分比，≥2场景 |
| 三段路线图 | 近期(1-3月)/中期(3-6月)/远期(6-12月) |

## Anti-Patterns
| 反模式 | 后果 |
|--------|------|
| What段写技术架构 | 非技术人员无法理解 |
| How段缺失架构图或命令不可执行 | 读者无法5分钟跑起来 |
| Next段路线图空泛 | "持续优化"失去规划意义 |
| 虚构量化指标 | 输入无数据却编造"提升80%"，不可信 |

## Edge Cases
| 场景 | 处理 |
|------|------|
| 输入仅一句话 | 标注"（内容不足，仅重构现有信息）"，基于有限信息补全五段式 |
| 输入已是完整README | 不重写有效内容，仅精炼模糊段落 |
| 纯技术文档（无用户/场景） | 强制补充Why段痛点和Result段场景，否则标注"（推断）" |
| 多项目混合输入 | 仅重构主项目，其余作为Next段关联项 |

## Quality Gates
- [ ] What/Why/How/Result/Next 五段是否齐全？
- [ ] What段是否非技术人员可理解？
- [ ] How段ASCII架构图是否包含数据流向？
- [ ] How段快速开始命令是否可复制执行？
- [ ] Result段指标是否包含具体数值，且至少有2个场景？

## 方法论来源
| 启发来源 | 核心贡献 |
|----------|----------|
| [Product Management in Practice](Matt LeMay) | 产品文档结构 |
| [Continuous Discovery Habits](Teresa Torres) | 价值主张表达 |
