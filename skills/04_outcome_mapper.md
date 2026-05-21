# Outcome Mapper Skill

## Purpose
将 Feature 描述转换为 Capability 再转换为 Outcome（用户价值）。

## Activation
当需要将技术表达转换为用户价值时激活。

## Transformation Chain
```
Feature → Capability → Outcome
```

## Conversion Rules
| Feature | Capability | Outcome |
|---------|-----------|---------|
| AI Workflow | 交付自动化平台 | 交付周期缩短 60%，人工干预减少 80% |
| 多模型调度 | 降低交付成本 | 减少重复配置与上下文切换 |
| 自动测试 | 质量保障自动化 | 测试覆盖率提升，回归成本降低 |
| CI/CD | 交付流水线 | 发布频率提升，部署风险降低 |
| 代码生成 | 开发效率提升 | 编码时间减少，一致性提高 |
| 文档自动化 | 知识沉淀自动化 | 文档维护成本降低，知识传递效率提高 |

## Input
Feature 描述（如 "AI Workflow"、"多模型调度"）

## Output Format
```json
{
  "feature": "",
  "capability": "",
  "outcome": ""
}
```

## Rules
- 精确匹配转换规则库
- 未匹配时使用通用转换逻辑
- 始终输出三层结构
