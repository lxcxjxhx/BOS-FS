# BOS-FS Pipeline Orchestrator
> Context: [base_context](../knowledge/base_context.md)

## Role
串联六大 Skill 完成完整项目优化。

## Pipeline
```
Repo/描述 → Understand → Map → Refactor → Review → Build → Submit
              ↓              ↓        ↓         ↓        ↓
          Goal Refiner   Outcome   README    Reviewer  Submission
                          Mapper   Refactor  Simulator Builder
```

## Steps
| Step | Stage | Skill | 输入 | 输出 |
|------|-------|-------|------|------|
| 1 | Understand | Goal Refiner | 项目描述 | {persona,problem,solution,outcome} |
| 2 | Map | Outcome Mapper | 特性列表 | Feature→Capability→Outcome |
| 3 | Refactor | README Refactor | 原始README | What/Why/How/Result/Next |
| 4 | Review | Reviewer Simulator | 项目信息 | 通过概率/拒绝理由/建议 |
| 5 | Build | Submission Builder | 项目信息 | 完整提交包 |
| 6 | Analyze | Reject Analyzer | 拒绝原因 | 真实问题/修复建议(按需) |

## Shortcut
| 命令 | 步骤 |
|------|------|
| 完整优化 | Step 1-5 |
| 快速预览 | Step 1-2 |
| 仅文档 | Step 3 |
| 仅评审 | Step 4 |
| 拒绝分析 | Step 6 |

## Output
```json
{"pipeline_result":{"goal":{},"outcomes":[],"readme":"","reviews":{},"bundle":{},"status":"complete|needs_revision"}}
```