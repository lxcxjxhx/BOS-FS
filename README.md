# BOS-FS

> **v0.0.2** · MIT License · Submission Engineering Runtime

## Build · Optimize · Submit

> 将"生成→表达→审核→交付"串联成统一 Skill Runtime。

## What is BOS-FS

BOS-FS 不是另一个 AI IDE，也不是独立的程序。它是一个可集成到任意 AI Agent（Cursor/Trae/OpenHands/Claude Code）的 **Submission Engineering Runtime** 层。

很多项目不是做不出来，而是能力强、表达弱、价值不清晰、审核失败。BOS-FS 解决的是：把项目的"能力"转化为"可被理解、评估、接受的交付物"。

## Quick Start

### Cursor
项目根目录已有 `.cursorrules` 文件，自动加载。或引用：
```
@skills/pipeline.md
```

### Trae
已配置 `.trae/skills/bos-fs/` 目录，使用：
```
/skill bos-fs/pipeline
```

### 通用 LLM
读取 `skills/pipeline.md` 作为 system prompt。

## Pipeline Walkthrough

### Step 1: 理解项目
```
Input: "做了一个AI工作流系统 支持多模型调度"
Output: {
  "persona": "开发者/技术团队",
  "problem": "工作流配置繁琐、多模型切换成本高",
  "solution": "AI工作流系统支持多模型调度与自动化",
  "outcome": "降低配置成本、提升交付效率"
}
```

### Step 2: 价值转换
```
Input: "多模型调度"
Output: {
  "feature": "多模型调度",
  "capability": "智能资源分配",
  "outcome": "减少重复配置与上下文切换"
}
```

### Step 3: README 重构
```
Input: 原始 README
Output: What/Why/How/Result/Next 结构的完整文档
```

### Step 4: 评审模拟
```
Input: 项目信息
Output: {
  "technical": {"pass_probability": 65, "suggestions": [...]},
  "investment": {"pass_probability": 45, "suggestions": [...]},
  "product": {"pass_probability": 70, "suggestions": [...]},
  "opensource": {"pass_probability": 55, "suggestions": [...]}
}
```

### Step 5: 构建提交包
```
Output: submission_bundle/
├── README.md
├── demo_guide.md
├── pitch.md
├── FAQ.md
└── risk_disclosure.md
```

## Core Skills

| Skill | 用途 | 输入 | 输出 |
|-------|------|------|------|
| [Goal Refiner](skills/01_goal_refiner.md) | 提炼项目意图 | 自然语言描述 | persona/problem/solution/outcome |
| [Reviewer Simulator](skills/02_reviewer_simulator.md) | 模拟评审 | 项目信息 | 通过概率/拒绝理由/建议 |
| [README Refactor](skills/03_readme_refactor.md) | 重构文档 | 原始 README | What/Why/How/Result/Next |
| [Outcome Mapper](skills/04_outcome_mapper.md) | 价值转换 | Feature 描述 | Capability → Outcome |
| [Submission Builder](skills/05_submission_builder.md) | 构建提交包 | 项目信息 | submission_bundle/ |
| [Reject Analyzer](skills/06_reject_analyzer.md) | 分析拒绝 | 拒绝说明 | 真实问题/修复建议 |
| [Pipeline](skills/pipeline.md) | 完整流水线 | 项目描述 | 完整优化结果 |

## Differentiation

| 竞品 | 定位 | 缺失 | BOS-FS 优势 |
|------|------|------|------------|
| README.so | README 生成器 | 不理解项目价值 | 理解意图后生成 |
| Mintlify | 代码→文档 | 不做审核模拟 | 内置四类评审 |
| SonarQube | 代码质量 | 不改 README | 文档重构引擎 |
| Linear | 团队管理 | 不触及产品包装 | 提交工程层 |
| OpenHands | 自动开发 | 无交付包装 | 完整提交包 |

**核心差异化**：唯一把"生成→表达→审核→交付"串联成统一 Skill Runtime 的系统。

## Value Formula

```
技术 × 用户 × 收益 = 产品描述
```

### Transformation Examples
| 原始表达 | 转换后 |
|---------|--------|
| "AI Workflow Engine" | "帮助开发者将需求自动转换为可交付软件资产的平台" |
| "支持多模型" | "减少重复配置与上下文切换" |
| "模型调度" | "降低交付成本" |

## FAQ

**Q: BOS-FS 和普通 README 生成器有什么区别？**
A: README 生成器只关注格式，BOS-FS 先理解项目价值，再重构表达，最后模拟评审确保通过率。

**Q: 需要写代码吗？**
A: 不需要。所有功能通过 Skill 提示词文件实现，可直接加载到 AI Agent 中使用。

**Q: engine/ 目录是必须的吗？**
A: 不是。`engine/` 是可选的 Python 后端引擎，仅在需要程序化批量处理时使用。

**Q: 如何集成到我的工作流？**
A: 见 [Cursor 集成指南](guides/cursor_integration.md)、[Trae 集成指南](guides/trae_integration.md)、[通用 LLM 集成指南](guides/generic_llm_integration.md)。

## Project Origin

- 需求文档: `NEED` — 核心价值定义与架构设计
- 竞品分析: `NEED2` — 市场分析与差异化定位
- 定位: Submission Engineering（提交工程）
- 与 HOS 生态关系: HOS-LS/HOS-M2F 负责"生成"，BOS-FS 负责"让成果被接受"

## Core Principles

**不做**: 伪造成果、伪造用户、伪造数据、夸大能力、规避规则
**做**: 明确目标、补齐交付、重构描述、对齐评审语言

## Quick Command Reference

| 场景 | 命令 |
|------|------|
| 完整优化 | 加载 `skills/pipeline.md`，提供项目描述 |
| 仅提炼意图 | 加载 `skills/01_goal_refiner.md` |
| 仅价值转换 | 加载 `skills/04_outcome_mapper.md` |
| 仅重构 README | 加载 `skills/03_readme_refactor.md` |
| 仅预审 | 加载 `skills/02_reviewer_simulator.md` |
| 分析拒绝 | 加载 `skills/06_reject_analyzer.md` |
| Cursor | `@skills/pipeline.md` |
| Trae | `/skill bos-fs/pipeline` |

## Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| v0.0.2 | 2026-05-21 | 生产级 Skill、pipeline 编排器、多平台集成、评分标准、发布就绪 |
| v0.0.1 | 2026-05-21 | 初始版本：六大 Skill + 基础 Runtime + 知识库 |

## Directory Structure

```
BOS-FS/
├── README.md              # 使用指南（本文件）
├── LICENSE                # MIT License
├── BOS-FS.json            # Skill 描述文件
├── .cursorrules           # Cursor 规则文件
├── skills/                # 六大 Skill 提示词 + 编排器
├── .trae/skills/bos-fs/   # Trae 可直接加载的 Skill 目录
├── runtime/               # 状态机与流水线定义
├── guides/                # 多平台集成指南
├── knowledge/             # 竞品分析 + 评审规则 + 模板 + 评分
├── examples/              # 使用示例
├── engine/                # Optional Backend（Python 可选引擎）
├── input/                 # 输入目录（repo/docs/screenshots/notes）
└── output/                # 输出目录
```
