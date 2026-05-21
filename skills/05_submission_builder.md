# Submission Builder Skill

## Purpose
构建完整的项目提交包。

## Activation
当需要准备提交材料、发布项目时激活。

## Input
项目信息：{persona, problem, solution, outcome, readme}

## Output Structure
```
submission_bundle/
├── README.md          # 重构后的项目说明
├── demo_guide.md      # 演示指南
├── introduction.md    # 项目介绍（Pitch）
├── screenshots_guide.md # 截图说明
├── FAQ.md            # 常见问题
├── risk_disclosure.md # 风险说明
└── bundle_meta.json  # 提交包元数据
```

## Component Templates
- README: What/Why/How/Result/Next 结构
- Demo: 安装→配置→运行→验证 流程
- Pitch: 一句话价值 → 问题 → 方案 → 指标 → 路线图
- FAQ: 覆盖 5-10 个典型问题
- Risk: 技术风险、市场风险、合规风险

## Rules
- 每个组件必须独立可读
- 信息保持一致性
- 风险说明不可省略
