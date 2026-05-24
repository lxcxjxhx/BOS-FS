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

## Input Validation
- 最小输入: README ≥ 20 字
- 输入不足 → 标注"（内容不足，仅重构现有信息）"
- 空输入 → 输出错误提示

## Error Handling
- 输入为空/缺失 → 输出错误信息并说明需要补充
- 字段缺失 → 标注"未明确"
- 矛盾信息 → 取最新/最主要的

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

## Output Schema

### Markdown 结构定义
输出必须包含以下五段式结构：

| 段落 | 标题 | 必含内容 |
|------|------|----------|
| What | `## What — 一句话价值` | 技术 × 用户 × 收益 公式描述 |
| Why | `## Why — 为什么存在` | 痛点列表 + 现有方案不足 |
| How | `## How — 如何实现` | ASCII架构图 + 特性列表 + 快速开始命令 |
| Result | `## Result — 效果` | 量化指标 + 典型场景 |
| Next | `## Next — 路线图` | 近期/中期/远期规划 |

### 验证规则
- **五段式完整性**: What/Why/How/Result/Next 五个段落缺一不可
- **What 非技术可理解**: 一句话价值必须让非技术人员能理解
- **架构图必须含数据流**: How 段必须包含 ASCII 架构图，展示主要组件和数据流向
- **快速开始可执行**: How 段必须包含可复制运行的命令（bash 代码块）
- **指标可量化**: Result 段指标必须包含数值或百分比，不可空泛描述
- **场景至少2个**: Result 段至少包含2个典型使用场景
- **三段路线图**: Next 段必须包含近期（1-3月）、中期（3-6月）、远期（6-12月）
