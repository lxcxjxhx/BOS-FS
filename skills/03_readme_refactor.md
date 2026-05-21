# README Refactor
> Context: [base_context](../knowledge/base_context.md)

## Role
将项目描述重构为专业 README（What/Why/How/Result/Next）。

## Structure
```markdown
# [项目名称]
## What — 一句话价值
[技术 × 用户 × 收益 = 产品描述]
## Why — 为什么存在
### 痛点 - [用户问题]
### 现有方案不足 - [对比]
## How — 如何实现
### 架构 ```[ASCII图]```
### 特性 - [特性]: [价值]
### 快速开始 ```bash[命令]```
## Result — 效果
### 指标 - [量化收益]
### 场景 - [典型场景]
## Next — 路线图
- [ ] 近期：[1-3月] - [ ] 中期：[3-6月] - [ ] 远期：[6-12月]
```

## Transformation
| 原始 | 转换后 |
|------|--------|
| AI Workflow Engine | 帮助开发者自动转换需求为可交付资产 |
| 支持多模型 | 减少重复配置与上下文切换 |
| 模型调度 | 降低交付成本 |
| 自动测试 | 质量保障自动化 |
| CI/CD | 交付流水线 |
| 代码生成 | 开发效率提升 |

## Checklist
- [ ] 一句话价值清晰（非技术可理解）
- [ ] 架构图含主要组件和数据流
- [ ] 快速开始5分钟完成
- [ ] 指标可量化

## Example
```
Input: "# My Project\nAI workflow engine, multi-model, auto-test"
Output: "# 交付自动化平台\n## What\n帮助开发者将AI工作流从手动配置转为自动化，减少60%重复操作。\n## Why\n### 痛点\n- 多模型切换需重复配置\n- 测试与开发流程割裂\n### 现有方案不足\n- 传统CI/CD不理解AI工作流\n## How\n### 架构\n[Client]→[API Gateway]→[Workflow Engine]→[Model Router]→[Test Runner]\n### 特性\n- **智能调度**: 自动选择最优模型\n- **自动化测试**: 内置AI工作流测试\n- **一键交付**: 开发到发布全流程\n### 快速开始\n```bash\npip install bos-fs && bos-fs init && bos-fs run\n```\n## Result\n### 指标\n- 配置时间减少60%，测试覆盖率提升40%\n### 场景\n- 个人开发者：5分钟完成发布\n## Next\n- [ ] 近期：更多模型供应商\n- [ ] 中期：团队协作\n- [ ] 远期：企业级安全合规"
```