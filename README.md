<div align="center">
  
  # BOS-FS
  <img width=30% height=30% alt="42e644be-c1b3-422b-b246-2d8418d56e4f" src="https://github.com/user-attachments/assets/c2f58bb0-f4fa-4ab5-ae94-887b468eb11f" />

</div>
<p align="center">

  <img src="https://img.shields.io/badge/version-v0.1.2-blue" alt="Version" />
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

## 信任背书

### 技术理念
- 基于 **DORA 指标体系** 设计交付效能评估
- 遵循 **SOLID 原则** 与 **Clean Architecture** 架构分层
- 安全设计对齐 **OWASP Top 10** 基准

### 工程标准
- 评审体系参考 **ISO/IEC 25010** 软件质量模型
- 提交包规范对标 **CII Best Practices** 开源质量标准
- 信任声明遵循 **OpenSSF Scorecard** 透明度原则

### 生态定位
- **HOS 生态**: HOS-LS / HOS-M2F 负责"生成"，BOS-FS 负责"让成果被接受"
- **行业分类**: AI Agent 技能系统 / Submission Engineering / 开发者工具

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
├── CHANGELOG.md · SECURITY.md · CONTRIBUTING.md
├── skills/ — 六大 Skill + pipeline 编排器
├── .trae/skills/bos-fs/SKILL.md — Trae Skill 引用（仅入口）
├── knowledge/ — base_context · differentiation · review_rules · templates · rubrics · trust_signals · authority_references
├── guides/ — 多平台集成指南 · 快速上手 · 速查表
├── examples/ — 使用示例（含 trust_statement 示例）
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

- **定位**: Submission Engineering（提交工程）— 让成果被接受，而非仅被生成
- **哲学**: 技术需要被权威框架验证，信任需要可查证。BOS-FS 不只优化表达，更建立可验证的信任体系
- **HOS 生态**: HOS-LS / HOS-M2F 负责"生成"，BOS-FS 负责"让成果被接受"
- **信任体系**: 内置权威引用库，支持 OWASP / ISO 25010 / CII Best Practices 等权威标准引用

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **v0.1.2** | 2026-05-23 | 评审体系完整化、新增产品/开源评审规则、Pipeline职责分离、Skill输出Schema统一、示例输入输出对照 |
| **v0.1.1** | 2026-05-23 | SKILL系统增强、新增Skill清单、InputValidation/ErrorHandling、重写SKILL.md |
| **v0.1.0** | 2026-05-23 | Python引擎修复、引擎模块文件重对齐、新增engine基础项目结构、新增project_manifest |
| **v0.0.9** | 2026-05-23 | 文档与可用性增强、新增快速上手指南和速查表、更新cursorrules、知识库交叉引用 |
| **v0.0.8** | 2026-05-23 | 文档与结构一致性优化、新增CHANGELOG/SECURITY/CONTRIBUTING、修复README重复tagline |
| **v0.0.7** | 2026-05-22 | 信任背书增强、权威引用库、Submission新增trust_statement、评审新增信任度维度 |
| **v0.0.6** | 2026-05-21 | 集成指南合并、评分文件清理、Skill目录精简、模板格式增强 |
| **v0.0.5** | 2026-05-21 | Skill文件压缩、Knowledge库合并(竞品分析+差异化)、评分标准统一、模板精简 |
| **v0.0.4** | 2026-05-21 | README高密度化、集成指南合并、元数据精简 |
| **v0.0.3** | 2026-05-21 | Skill Token优化(~55%压缩)、.trae/目录去重、公共上下文提取 |
| v0.0.2 | 2026-05-21 | 生产级Skill、pipeline编排器、多平台集成、评分标准 |
| v0.0.1 | 2026-05-21 | 初始版本：六大Skill+基础Runtime+知识库 |

---

<p align="center">
  <sub>Built with ❤️ by <a href="https://github.com/HOS">HOS (安全风信子)</a></sub>
</p>
