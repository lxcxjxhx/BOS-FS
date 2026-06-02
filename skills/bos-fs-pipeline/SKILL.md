---
name: bos-fs-pipeline
description: BOS-FS 流水线编排器，串联七大 Skill 完成完整项目优化流程（支持按需执行/精简模式/完整模式）。
---

# BOS-FS Pipeline Orchestrator
**version**: 0.3.0
> Context: [base_context](../knowledge/base_context.md)
> Flexibility: [flexibility_principles.md](../knowledge/adoption/flexibility_principles.md)

## Role
串联 Skill 完成项目优化。**不必执行所有阶段**，根据项目需求选择流水线模式。

## 流水线模式 (Pipeline Modes)

| 模式 | 执行步骤 | 适用场景 | 预计耗时 |
|------|---------|---------|---------|
| 完整流水线 (Full) | Step 1-5 (完整) | 商业发布/客户交付/融资材料 | 15-20分钟 |
| 精简流水线 (Lite) | Step 1, 3, 4 | 个人项目/MVP/内部工具 | 5-8分钟 |
| 按需执行 (Custom) | 用户自选 | 根据项目阶段灵活组合 | 视选择而定 |

### 按需执行原则 (On-Demand Execution)

**MUST 执行**: Step 1 (Understand) — 所有后续步骤依赖其输出
**SHOULD 执行**: Step 3 (Review), Step 4 (Refactor) — 确保质量和文档
**MAY 执行**: Step 2 (Map), Step 5 (Build), Step 6 (Analyze) — 按需选择

### 典型执行路径

| 路径 | 步骤 | 场景 |
|------|------|------|
| 快速预览 | 1→2 | 仅提炼项目意图 |
| 质量预审 | 1→3 | 仅执行评审，不修改文档 |
| 文档优化 | 1→4 | 仅重构 README |
| 客户交付 | 1→2→3→4→5 | 完整流水线 |
| 迭代优化 | 1→3→6→(修复)→1 | 评审→分析→修复 |
| 安全交付 | 1→3(adversarial)→4→5 | 含安全评审的完整交付 |

## Pipeline

```
Repo/描述 → Understand → Map(可选) → Review → Refactor → Build(可选) → Analyze(可选)
              ↓              ↓         ↓         ↓          ↓         ↓
          Goal Refiner   Outcome  Reviewer  README    Submission  Reject
                          Mapper  Simulator Refactor  Builder     Analyzer
```

## Steps
| Step | Stage | Skill | 约束 | 输入 | 输出 |
|------|-------|-------|------|------|------|
| 1 | Understand | Goal Refiner | MUST | 项目描述 | {persona,problem,solution,outcome} |
| 2 | Map | Outcome Mapper | MAY | 特性列表 | Feature→Capability→Outcome |
| 3 | Review | Reviewer Simulator | SHOULD | 项目信息 | 通过概率/拒绝理由/建议 |
| 4 | Refactor | README Refactor | SHOULD | 原始README | 重构后README |
| 5 | Build | Submission Builder | MAY | 项目信息 | 提交包 |
| 6 (可选) | Analyze | Reject Analyzer | MAY | 拒绝原因 | 真实问题/修复建议 |

> **约束说明**:
> - MUST: 不可跳过，所有后续步骤依赖 Step 1
> - SHOULD: 建议执行，跳过会降低交付质量
> - MAY: 按需选择，根据项目阶段决定是否执行

## 快捷命令 (Shortcuts)
| 命令 | 执行步骤 | 模式 | 适用场景 |
|------|---------|------|---------|
| 完整优化 | 1→2→3→4→5 | Full | 客户交付/商业发布 |
| 精简优化 | 1→3→4 | Lite | 个人项目/MVP |
| 快速预览 | 1→2 | Lite | 仅提炼意图 |
| 仅评审 | 3 | Lite | 质量预审 |
| 仅文档 | 1→4 | Lite | 文档优化 |
| 拒绝分析 | 6 | Custom | 诊断评审失败原因 |
| 迭代优化 | 1→3→6→修复 | Custom | 评审→分析→修复循环 |

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
