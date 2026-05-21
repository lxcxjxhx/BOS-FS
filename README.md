<p align="center">
  
  # BOS-FS
</p>
<p align="center">

  <img src="https://img.shields.io/badge/version-v0.0.5-blue" alt="Version" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License" />
  <img src="https://img.shields.io/badge/status-Production Ready-brightgreen" alt="Status" />
</p>

<p align="center">
  <strong>Submission Engineering Runtime</strong> · Build · Optimize · Submit
</p>

---

## 概述

BOS-FS 是可集成到任意 AI Agent（Cursor / Trae / OpenHands / Claude Code）的 **Submission Engineering Runtime**，把项目的"能力"转化为"**可被理解、评估、接受的交付物**"。

## Pipeline 工作流

| Step | Stage | Skill | 输入 | 输出 |
|------|-------|-------|------|------|
| 1 | Understand | Goal Refiner | 项目描述 | {persona,problem,solution,outcome} |
| 2 | Map | Outcome Mapper | 特性列表 | Feature→Capability→Outcome |
| 3 | Refactor | README Refactor | 原始 README | What/Why/How/Result/Next |
| 4 | Review | Reviewer Simulator | 项目信息 | 通过概率/拒绝理由/建议 |
| 5 | Build | Submission Builder | 项目信息 | 完整提交包 |
| 6 | Analyze | Reject Analyzer | 拒绝原因 | 真实问题/修复建议(按需) |

## 核心 Skills

| Skill | 用途 | 输入 | 输出 |
|-------|------|------|------|
| [Goal Refiner](skills/01_goal_refiner.md) | 提炼项目意图 | 自然语言描述 | persona/problem/solution/outcome |
| [Reviewer Simulator](skills/02_reviewer_simulator.md) | 模拟四类评审 | 项目信息 | 通过概率/拒绝理由/建议 |
| [README Refactor](skills/03_readme_refactor.md) | 重构项目文档 | 原始 README | What/Why/How/Result/Next |
| [Outcome Mapper](skills/04_outcome_mapper.md) | Feature→Value | 功能描述 | Capability→Outcome |
| [Submission Builder](skills/05_submission_builder.md) | 构建交付包 | 项目信息 | 完整 submission_bundle/ |
| [Reject Analyzer](skills/06_reject_analyzer.md) | 分析被拒原因 | 拒绝说明 | 真实问题/修复建议 |
| [Pipeline](skills/pipeline.md) | 完整流水线编排 | 项目描述 | 端到端优化结果 |

## 快速命令

| 场景 | 命令 |
|------|------|
| 完整优化 | 加载 `skills/pipeline.md` |
| 仅提炼意图 | 加载 `skills/01_goal_refiner.md` |
| 仅价值转换 | 加载 `skills/04_outcome_mapper.md` |
| 仅重构 README | 加载 `skills/03_readme_refactor.md` |
| 仅预审 | 加载 `skills/02_reviewer_simulator.md` |
| Cursor | `@skills/pipeline.md` |
| Trae | `/skill bos-fs/pipeline` |

## 核心差异化

| 竞品 | 定位 | BOS-FS 优势 |
|------|------|-------------|
| README.so | README 生成器 | 理解意图后生成 |
| Mintlify | 代码→文档 | 内置四类评审 |
| SonarQube | 代码质量 | 文档重构引擎 |
| OpenHands | 自动开发 | 完整提交包 |

> 唯一把 **"生成→表达→审核→交付"** 串联成统一 Skill Runtime 的系统。

## 价值转换公式

```
技术 × 用户 × 收益 = 产品描述
```

| 原始表达 | 转换后 |
|---------|--------|
| "AI Workflow Engine" | "帮助开发者将需求自动转换为可交付软件资产的平台" |
| "支持多模型" | "减少重复配置与上下文切换" |
| "模型调度" | "降低交付成本" |

## 项目结构

```
BOS-FS/
├── README.md · LICENSE · BOS-FS.json · .cursorrules
├── skills/ — 六大 Skill + pipeline 编排器
├── .trae/skills/bos-fs/ — Trae Skill 引用
├── knowledge/ — base_context · 竞品分析 · 评审规则 · 模板 · 评分
├── guides/ — 多平台集成指南
├── examples/ — 使用示例
├── engine/ — Python 可选引擎
├── input/ — 输入目录 (repo/docs/screenshots/notes)
└── output/ — 输出目录
```

## 常见问题

**Q: 和普通 README 生成器有什么区别？**  
A: README 生成器只关注格式，BOS-FS 先理解价值→重构表达→模拟评审→确保通过率。

**Q: `engine/` 目录是必须的吗？**  
A: 不是。`engine/` 是可选的 Python 后端引擎，仅在需要批量处理时使用。

**Q: 如何集成？**  
A: 参见 [guides/integration.md](guides/integration.md)。

## 核心原则

| ❌ 不做 | ✅ 做 |
|---------|-------|
| 伪造成果/用户/数据 | 明确目标/补齐交付 |
| 夸大能力/规避规则 | 重构描述/对齐评审 |

## 项目起源

- **定位**: Submission Engineering（提交工程）
- **HOS 生态**: HOS-LS / HOS-M2F 负责"生成"，BOS-FS 负责"让成果被接受"

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **v0.0.5** | 2026-05-21 | Skill文件压缩、Knowledge库合并(竞品分析+差异化)、评分标准统一、模板精简 |
| **v0.0.4** | 2026-05-21 | README高密度化、集成指南合并、元数据精简 |
| **v0.0.3** | 2026-05-21 | Skill Token优化(~55%压缩)、.trae/目录去重、公共上下文提取 |
| v0.0.2 | 2026-05-21 | 生产级Skill、pipeline编排器、多平台集成、评分标准 |
| v0.0.1 | 2026-05-21 | 初始版本：六大Skill+基础Runtime+知识库 |

---

<p align="center">
  <sub>Built with ❤️ by <a href="https://github.com/HOS">HOS (安全风信子)</a></sub>
</p>
