# Reviewer Simulator Skill

## Purpose
模拟四种评审角色，评估项目通过率。

## Activation
当需要预审项目、评估审核通过率时激活。

## Review Types
- technical: 技术评审（代码质量、架构、性能、安全）
- investment: 投资评审（市场规模、竞争、团队、营收）
- product: 产品评审（用户需求、差异化、体验）
- opensource: 开源评审（社区价值、可维护性、文档）

## Input
项目信息：{persona, problem, solution, outcome}

## Output Format
```json
{
  "review_type": "",
  "pass_probability": 0.0-100.0,
  "rejection_reasons": [],
  "suggestions": []
}
```

## Scoring Logic
- 目标明确性（25%）
- 技术可行性（25%）
- 用户价值（25%）
- 文档完整性（25%）
- 每项缺失扣 10-15 分

## Example
Input: {"persona": "开发者", "problem": "工作流繁琐", "solution": "AI工作流系统", "outcome": "提升效率"}
Output (technical): {"pass_probability": 65, "rejection_reasons": ["缺少架构图", "未说明技术栈"], "suggestions": ["补充架构设计", "明确技术选型"]}
