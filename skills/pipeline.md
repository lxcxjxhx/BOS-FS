# BOS-FS Pipeline Orchestrator
> Context: [base_context](../knowledge/base_context.md)

## Role
串联六大 Skill 完成完整项目优化。

## Pipeline
```
Repo/描述 → Understand → Map → Review → Refactor → Build → Analyze
              ↓              ↓        ↓         ↓          ↓        ↓
          Goal Refiner   Outcome  Reviewer  README    Submission  Reject
                          Mapper  Simulator Refactor  Builder     Analyzer
```

## Steps
| Step | Stage | Skill | 输入 | 输出 |
|------|-------|-------|------|------|
| 1 | Understand | Goal Refiner | 项目描述 | {persona,problem,solution,outcome} |
| 2 | Map | Outcome Mapper | 特性列表 | Feature→Capability→Outcome |
| 3 | Review | Reviewer Simulator | 项目信息 | 通过概率/拒绝理由/建议 |
| 4 | Refactor | README Refactor | 原始README | What/Why/How/Result/Next |
| 5 | Build | Submission Builder | 项目信息 | 完整提交包 |
| 6 | Analyze | Reject Analyzer | 拒绝原因 | 真实问题/修复建议(按需) |

## Shortcut
| 命令 | 步骤 |
|------|------|
| 完整优化 | Step 1-5 |
| 快速预览 | Step 1-2 |
| 仅评审 | Step 3 |
| 仅文档 | Step 4 |
| 拒绝分析 | Step 6 |

## Output
```json
{"pipeline_result":{"step1_goal":{"persona":"","problem":"","solution":"","outcome":""},"step2_outcomes":[{"feature":"","capability":"","outcome":""}],"step3_review":{"review_type":"","pass_probability":0,"scores":{},"rejection_reasons":[],"suggestions":[]},"step4_readme":"","step5_bundle":{"bundle_path":"","components":[],"status":""},"step6_reject":{"real_issue":"","fixable_items":[],"resubmit_suggestion":""},"status":"complete|needs_revision"}}
```