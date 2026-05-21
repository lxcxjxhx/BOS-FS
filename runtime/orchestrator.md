# Skill Runtime Orchestrator

## Purpose
定义 BOS-FS Skill 系统的状态机编排逻辑。

## State Machine
```
Idle → [触发Skill] → Processing → [输出] → Idle
                        ↓
                   [需要更多信息] → Waiting → [用户输入] → Processing
```

## Stage Transitions
- Understand: Goal Refiner 激活 → 输出 {persona, problem, solution, outcome}
- Map: Outcome Mapper 激活 → 输出 Feature→Capability→Outcome
- Refactor: README Refactor 激活 → 输出重构后的 README
- Review: Reviewer Simulator 激活 → 输出评审报告
- Build: Submission Builder 激活 → 输出 submission_bundle
- Analyze: Reject Analyzer 激活（按需）→ 输出修复建议

## Rules
- 每个 Stage 可独立执行
- Stage 间通过结构化数据传递
- 任一 Stage 失败不影响其他 Stage
- Analyze Stage 仅在项目被拒时激活
