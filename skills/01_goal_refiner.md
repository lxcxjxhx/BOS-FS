# Goal Refiner Skill

## Purpose
从用户的项目描述中提取结构化意图。

## Activation
当用户描述项目、需要明确目标时自动激活。

## Input
用户的项目描述（自然语言）。

## Output Format
```json
{
  "persona": "目标用户是谁",
  "problem": "解决什么问题",
  "solution": "如何解决",
  "outcome": "预期结果"
}
```

## Rules
- 从描述中识别目标用户群体
- 提取核心痛点/问题
- 归纳解决方案
- 明确预期结果
- 如信息不足，标记为 "未明确"

## Example
Input: "做了一个AI工作流系统 支持多模型调度 可以自动测试和发布"
Output: {"persona": "开发者/技术团队", "problem": "工作流配置繁琐、多模型切换成本高", "solution": "AI工作流系统支持多模型调度与自动化", "outcome": "降低配置成本、提升交付效率"}
