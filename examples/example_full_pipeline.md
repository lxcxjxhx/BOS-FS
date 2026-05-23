# BOS-FS 完整流水线示例

## 输入
```
做了一个 AI 工作流系统，支持多模型调度，可以自动测试和发布。目前主要是团队内部使用。
```

## Step 1: Understand → Goal Refiner
```json
{
  "persona": "研发团队/内部技术团队",
  "problem": "工作流配置繁琐，多模型切换效率低，测试发布流程割裂",
  "solution": "AI 工作流系统，支持多模型调度、自动测试与发布",
  "outcome": "提升团队协作效率，降低配置与测试成本"
}
```

## Step 2: Map → Outcome Mapper
```json
{
  "features": [
    {"feature": "AI 工作流", "capability": "交付自动化平台", "outcome": "交付周期缩短 60%"},
    {"feature": "多模型调度", "capability": "智能资源分配", "outcome": "减少上下文切换"},
    {"feature": "自动测试", "capability": "质量保障自动化", "outcome": "回归成本降低 60%"},
    {"feature": "自动发布", "capability": "交付流水线", "outcome": "部署风险降低 70%"}
  ]
}
```

## Step 3: Refactor → README Refactor
**输入**: 原始 README（项目功能列表）
```markdown
# AI Workflow Engine
- Multi-model support
- Auto testing
- CI/CD integration
```
**输出**: 完整 README（What/Why/How/Result/Next 结构）
**转换逻辑**: 技术功能列表 → 五段式价值文档。What 提炼核心价值，Why 说明痛点，How 展示架构，Result 量化收益，Next 规划路线。

## Step 4: Review → Reviewer Simulator
**输入**: Step 1 输出的 {persona, problem, solution, outcome}
```json
{
  "technical": {"pass_probability": 72},
  "investment": {"pass_probability": 45},
  "product": {"pass_probability": 68},
  "opensource": {"pass_probability": 55}
}
```

## Step 5: Build → Submission Builder
**输入**: Goal Refiner 输出 + README Refactor 输出 + Outcome Mapper 输出
**输出**: submission_bundle/ 包含 8 个组件（README/Demo/Pitch/FAQ/风险说明/信任声明/截图指南/元数据）
**转换逻辑**: 将各 Stage 输出整合为统一提交包，确保全局一致性。

## 最终输出
完整的项目提交包，可直接用于开源发布、投资路演或内部评审。

## 输入输出对照总结
| Stage | 输入 | 输出格式 | 输出内容 |
|-------|------|----------|----------|
| Understand | 自然语言描述 | JSON | {persona, problem, solution, outcome} |
| Map | 特性列表 | JSON | {features: [{feature, capability, outcome}]} |
| Refactor | 原始 README | Markdown | What/Why/How/Result/Next |
| Review | Stage 1 输出 | JSON | {review_type, pass_probability, scores, suggestions} |
| Build | Stage 1-4 输出 | 文件系统 | submission_bundle/ (8 组件) |
