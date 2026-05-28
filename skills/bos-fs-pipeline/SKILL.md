---
name: bos-fs-pipeline
description: BOS-FS 流水线编排器，串联七大 Skill 完成完整项目优化流程（Understand → Map → Review → Refactor → Build → Analyze）。
---

# BOS-FS Pipeline Orchestrator
**version**: 0.2.7
> Context: [base_context](../knowledge/base_context.md)

## Role
串联七大 Skill 完成完整项目优化。

## Pipeline
```
Repo/描述 → Understand → Map → Review → Refactor → Build → Analyze(可选)
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
| 6 (可选) | Analyze | Reject Analyzer | 拒绝原因 | 真实问题/修复建议(按需) |

## Shortcut
| 命令 | 步骤 |
|------|------|
| 完整优化 | Step 1-5 |
| 快速预览 | Step 1-2 |
| 仅评审 | Step 3 |
| 仅文档 | Step 4 |
| 拒绝分析 | Step 6 (可选) |

## Input Validation
- **必需输入**: 项目描述或仓库信息（至少包含项目名和核心功能描述）
- **可选输入**: README 内容、技术栈、目标用户、竞品列表
- **错误条件**:
  - 输入为空 → 终止流水线，status="error"，提示提供项目描述
  - 输入仅含项目名无功能描述 → 可执行但输出质量降级，标注"（信息不足）"
  - 输入包含敏感信息 → 自动脱敏并在 bundle_meta.json 中标注 `"sanitized": true`

## Output
```json
{"pipeline_result":{"step1_goal":{"persona":"","problem":"","solution":"","outcome":""},"step2_outcomes":[{"feature":"","capability":"","outcome":""}],"step3_review":{"review_type":"","pass_probability":0,"scores":{},"rejection_reasons":[],"suggestions":[]},"step4_readme":"","step5_bundle":{"bundle_path":"","components":[],"status":""},"step6_reject":{"real_issue":"","fixable_items":[],"resubmit_suggestion":""}},"status":"complete|partial|needs_revision|error"}
```

> **部分执行说明**: 当跳过可选步骤或某步骤失败时，对应字段返回 `null`。例如跳过 Step 6 时 `step6_reject` 为 `null`；status 为 `partial` 时表示部分步骤未完成。

## Output Schema
```json
{"type":"object","properties":{
  "pipeline_result":{"type":"object","properties":{
    "step1_goal":{"type":"object","properties":{"persona":{"type":"string"},"problem":{"type":"string"},"solution":{"type":"string"},"outcome":{"type":"string"}}},
    "step2_outcomes":{"type":"array","items":{"type":"object","properties":{"feature":{"type":"string"},"capability":{"type":"string"},"outcome":{"type":"string"}}}},
    "step3_review":{"type":"object","properties":{"review_type":{"type":"string"},"pass_probability":{"type":"integer"}}},
    "step4_readme":{"type":"string","description":"重构后的README内容"},
    "step5_bundle":{"type":"object","properties":{"status":{"type":"string"},"components":{"type":"array","items":{"type":"string"}}}},
    "step6_reject":{"type":"object","properties":{"real_issue":{"type":"string"},"fixable_items":{"type":"array"}}}
  }},
  "status":{"type":"string","enum":["complete","partial","needs_revision","error"]},
  "errors":{"type":"array","items":{"type":"string"},"description":"错误信息列表"}
},"required":["pipeline_result","status"],"additionalProperties":false}
```

验证规则:
- `status` 必须与实际执行结果一致
- `complete`: 全部步骤成功
- `partial`: 部分步骤失败
- `needs_revision`: Step 3 不通过
- `error`: Step 1 失败或输入无效

## Anti-Patterns
| 反模式 | 后果 |
|--------|------|
| 跳过Step 1直接执行后续步骤 | 缺少goal_refiner输出，后续步骤的persona/problem/solution/outcome均为空 |
| 在Step 3评审未通过时仍执行Step 5 Build | 构建的提交包基于有缺陷的项目信息，评审通过概率持续偏低 |
| 循环执行同一Step多次 | 流水线进入死循环，浪费资源且无法推进 |
| 无视Step依赖关系乱序执行 | 如Step 6（拒绝分析）在Step 3（评审）前执行，无输入数据 |
| 完整优化与快捷命令混用 | 同一会话中混合执行可能导致输出覆盖或状态不一致 |

## Edge Cases
| 边界场景 | 处理方式 |
|----------|----------|
| Step 1输出为空（输入描述无法理解） | 终止流水线，status="error"，提示补充项目描述 |
| Step 3评审通过概率<30 | 自动插入Step 6拒绝分析，生成修复建议后提示重新执行Step 1-5 |
| Step 5提交包生成失败 | status标记为"needs_revision"，输出已成功的步骤结果 |
| 流水线执行超时（>10分钟） | 保存中间状态到`pipeline_state.json`，支持断点续传 |
| 用户自定义跳过Step 2/4 | 允许跳过非核心步骤，但output中对应字段标注为"skipped" |

## Quality Gates
输出前自检：
1. 所有依赖步骤是否已按正确顺序执行？（Step N的输入是否依赖Step N-1的输出？）
2. pipeline_result中每个step字段是否均有值或明确标注"skipped"/"error"？
3. 若Step 3评审未通过（pass_probability<60），是否已触发Step 6或标注needs_revision？
4. 最终status字段是否与实际完成情况一致？（complete=全部成功，needs_revision=需修改）
5. 是否避免了流水线死循环？（同一Step执行次数≤3次）

## Error Handling
- **单个步骤失败**: 记录失败步骤编号和错误信息，已完成的步骤结果保留，`status` 标记为 `partial`
- **Step 1 失败**: 终止整条流水线（所有后续步骤依赖 Step 1 输出），`status` 标记为 `error`
- **步骤间数据传递失败**: 标注缺失字段为 `null`，后续步骤跳过或降级执行
- **部分执行恢复**: 保存中间状态到 `pipeline_state.json`，支持从失败步骤重新开始
- **超时处理**: 执行超过 10 分钟时保存当前进度，输出已完成的步骤结果，`status` 标记为 `partial`
- **步骤重试**: 单个非关键步骤（Step 2/4/6）最多重试 2 次，仍失败则跳过并标注

## Pipeline Stage Dependency Validation Rules
### 依赖关系矩阵
| 步骤 | 前置依赖 | 输出依赖 | 可跳过 |
|------|----------|----------|--------|
| Step 1 Understand | 无 | Step 2, 3, 4, 5 | ❌ |
| Step 2 Map | Step 1 | Step 3, 6 | ✅ |
| Step 3 Review | Step 1, 2 | Step 5, 6 | ✅ |
| Step 4 Refactor | Step 1 | Step 5 | ✅ |
| Step 5 Build | Step 1, 3, 4 | 最终输出 | ❌（若status=complete） |
| Step 6 Analyze | Step 3 | Step 1（反馈循环） | ✅ |

### 验证规则
- **硬依赖**: Step 5必须在Step 1/3/4完成后执行
- **条件依赖**: Step 6仅在Step 3评审不通过时触发
- **循环限制**: Step 6→Step 1的反馈循环最多执行2次
- **状态一致性**: 流水线最终status必须反映所有步骤的综合状态
- **输出追溯**: 每个步骤的输出必须包含`step_number`和`timestamp`用于审计

## 方法论来源与学术诚信

本 Skill 的方法论来源于**作者亲自阅读以下书籍并提炼核心要点**，非 AI 自动处理或简单摘要。

| 启发来源 | 核心贡献 |
|----------|----------|
| [Accelerate](Nicole Forsgren 等) | 交付效能 Pipeline |
| [Project to Product](Mik Kersten) | Flow Framework / 价值流 |
| [Team Topologies](Skelton & Pais) | 团队认知负荷与流 |

> **声明**: 本 Skill 中的方法论启发自上述书籍（见表格），所有代码实现、示例和知识重构均为作者原创。建议读者支持正版，购买原书以获得更完整的论述和案例。
