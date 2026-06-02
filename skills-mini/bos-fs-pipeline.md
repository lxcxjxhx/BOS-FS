---
name: bos-fs-pipeline
description: BOS-FS 流水线编排器，串联七大 Skill 完成完整项目优化流程（Understand → Map → Review → Refactor → Build → Analyze）。
---

# BOS-FS Pipeline Orchestrator
**version**: 0.2.11
> Context: [base_context](../../knowledge/base_context.md)
> Full version: skills/bos-fs-pipeline/SKILL.md

## Role
串联七大 Skill 完成完整项目优化。

## Pipeline Flow
```
Repo/描述 → Understand → Map → Review → Refactor → Build → Analyze(可选)
              ↓              ↓        ↓         ↓          ↓        ↓
          Goal Refiner   Outcome  Reviewer  README    Submission  Reject
                          Mapper  Simulator Refactor  Builder     Analyzer
```

## Steps
| Step | Stage | Skill | 可跳过 | 输入 | 输出 |
|------|-------|-------|--------|------|------|
| 1 | Understand | Goal Refiner | ❌ | 项目描述 | {persona,problem,solution,outcome} |
| 2 | Map | Outcome Mapper | ✅ | 特性列表 | Feature→Capability→Outcome |
| 3 | Review | Reviewer Simulator | ✅ | 项目信息 | 通过概率/拒绝理由/建议 |
| 4 | Refactor | README Refactor | ✅ | 原始README | What/Why/How/Result/Next |
| 5 | Build | Submission Builder | ❌ | 项目信息 | 完整提交包 |
| 6(可选) | Analyze | Reject Analyzer | ✅ | 拒绝原因 | 真实问题/修复建议 |

## Shortcut
| 命令 | 步骤 |
|------|------|
| 完整优化 | 1-5 | 快速预览 | 1-2 | 仅评审 | 3 | 仅文档 | 4 | 拒绝分析 | 6(可选) |

## Input/Output
**必需**: 项目描述(≥项目名+核心功能) | **可选**: README/技术栈/目标用户/竞品
**空输入**→终止 status=error | **仅项目名**→降级标注"（信息不足）" | **敏感信息**→脱敏+meta标 `"sanitized":true`
**Output**: 单行JSON含 `pipeline_result`(step1_goal/step2_outcomes/step3_review/step4_readme/step5_bundle/step6_reject) + `status`(complete|partial|needs_revision|error)

## Error Handling
| 场景 | 处理 |
|------|------|
| 单步失败 | 记录错误，已完成保留，status=partial |
| Step 1 失败 | 终止→status=error |
| 数据传递失败 | 缺失字段=null，后续跳过/降级 |
| 部分恢复 | 保存中间态到 `pipeline_state.json`，断点续传 |
| 超时(>10分钟) | 保存进度，status=partial |
| 非关键步重试 | Step 2/4/6 最多重试2次，失败跳过 |

## Dependency Matrix
| 步骤 | 前置 | 可跳过 |
|------|------|--------|
| 1 | 无 | ❌ | 2 | Step 1 | ✅ |
| 3 | Step 1,2 | ✅ | 4 | Step 1 | ✅ |
| 5 | Step 1,3,4 | ❌(complete必须) | 6(可选) | Step 3 | ✅ |

**规则**: Step 5须等1/3/4完成 | Step 6仅Step 3不通过时触发 | Step 6→Step 1反馈≤2次 | 每步输出含 `step_number`+`timestamp` 审计

## Anti-Patterns
| 反模式 | 后果 |
|--------|------|
| 跳过Step 1 | 后续 persona/problem/solution/outcome 为空 |
| Step 3未通过仍执行Step 5 | 提交包基于缺陷信息 |
| 循环执行同一Step | 死循环浪费资源 |
| 无视依赖乱序 | 如Step 6在Step 3前，无输入 |
| 完整与快捷混用 | 同会话可能输出覆盖 |

## Edge Cases
| 场景 | 处理 |
|------|------|
| Step 1输出为空 | 终止→status=error |
| Step 3概率<30 | 自动插Step 6，提示重执行1-5 |
| Step 5失败 | status=needs_revision，输出已成功的 |
| 执行超时(>10分钟) | 保存中间态，断点续传 |
| 自定义跳过Step 2/4 | 对应字段标"skipped" |

## Quality Gates
- [ ] 所有依赖步骤按正确顺序执行？（Step N输入依赖N-1输出？）
- [ ] pipeline_result 每step字段均有值或明确标注 skipped/error？
- [ ] Step 3未通过(pass_probability<60)是否触发Step 6或标注needs_revision？
- [ ] 最终status与实际一致？（complete=全部，partial=部分，needs_revision=需修改）
- [ ] 避免死循环？（同Step执行≤3次）

## 方法论来源
| 启发来源 | 核心贡献 |
|----------|----------|
| [Accelerate](Nicole Forsgren 等) | 交付效能 Pipeline |
| [Project to Product](Mik Kersten) | Flow Framework / 价值流 |
| [Team Topologies](Skelton & Pais) | 团队认知负荷与流 |
