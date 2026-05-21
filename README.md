# BOS-FS

## Submission Engineering Runtime

> Build · Optimize · Submit
> 将"生成→表达→审核→交付"串联成统一 Skill Runtime。

## What is BOS-FS

BOS-FS 不是另一个 AI IDE，也不是独立的程序。它是一个可集成到任意 AI Agent（Cursor/Trae/OpenHands/Claude Code）的 **Submission Engineering Runtime** 层。

很多项目不是做不出来，而是能力强、表达弱、价值不清晰、审核失败。BOS-FS 解决的是：把项目的"能力"转化为"可被理解、评估、接受的交付物"。

## Core Skills

| Skill | Purpose | Input | Output |
|-------|---------|-------|--------|
| Goal Refiner | 提炼项目意图 | 自然语言描述 | persona/problem/solution/outcome |
| Reviewer Simulator | 模拟评审 | 项目信息 | 通过概率/拒绝理由/建议 |
| README Refactor | 重构文档 | 原始 README | What/Why/How/Result/Next 结构 |
| Outcome Mapper | 价值转换 | Feature 描述 | Capability → Outcome |
| Submission Builder | 构建提交包 | 项目信息 | 完整 submission_bundle |
| Reject Analyzer | 分析拒绝原因 | 拒绝说明 | 真实问题/修复建议/重投版本 |

## Differentiation

| 竞品 | 定位 | 缺失 |
|------|------|------|
| README.so | README 生成器 | 不理解项目价值 |
| Mintlify | 代码→文档 | 不做审核模拟 |
| SonarQube | 代码质量扫描 | 不改 README |
| Linear | 团队管理 | 不触及产品包装 |
| OpenHands | 自动开发执行 | 无交付包装层 |

**BOS-FS**: 唯一把"生成→表达→审核→交付"串联成统一 Skill Runtime 的系统。

## Quick Load

### Cursor
将 skills/ 目录下的 .md 文件添加到 .cursorrules 或直接引用。

### Trae
将 Skill 文件放入 .trae/skills/ 目录。

### OpenHands
通过 skills/ 目录加载对应 Skill 提示词。

### Generic LLM API
读取对应 Skill .md 文件作为 system prompt。

## Pipeline

```
Repo → Understand → Optimize → Review → Package → Submit
```

## Value Formula

```
技术 × 用户 × 收益 = 产品描述
```

## Core Principles

**不做**: 伪造成果、伪造用户、伪造数据、夸大能力、规避规则
**做**: 明确目标、补齐交付、重构描述、对齐评审语言
