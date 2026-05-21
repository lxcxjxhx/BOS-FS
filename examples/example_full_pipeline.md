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
输出完整 README（What/Why/How/Result/Next 结构）

## Step 4: Review → Reviewer Simulator
```json
{
  "technical": {"pass_probability": 72},
  "investment": {"pass_probability": 45},
  "product": {"pass_probability": 68},
  "opensource": {"pass_probability": 55}
}
```

## Step 5: Build → Submission Builder
生成 submission_bundle/ 包含 README/Demo/Pitch/FAQ/风险说明

## 最终输出
完整的项目提交包，可直接用于开源发布、投资路演或内部评审。
