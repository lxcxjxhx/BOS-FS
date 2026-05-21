# BOS-FS Pipeline

## Flow
```
Repo → Understand → Optimize → Review → Package → Submit
```

## Step Detail
1. **Understand**: 读取项目描述/仓库，Goal Refiner 提取意图
2. **Optimize**: Outcome Mapper 转换价值表达，README Refactor 重构文档
3. **Review**: Reviewer Simulator 模拟四类评审，输出通过率与建议
4. **Package**: Submission Builder 构建完整提交包
5. **Submit**: 生成最终交付物

## Input/Output Contract
- Input: 项目描述（自然语言）+ 原始 README（可选）
- Output: submission_bundle/ + pipeline_report.json

## Error Handling
- 信息不足 → 标记 "未明确"，继续后续 Stage
- 评审不通过 → 输出建议，不阻断流程
- 构建失败 → 输出部分结果，标记失败组件
