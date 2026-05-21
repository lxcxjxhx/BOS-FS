# Outcome Mapper
> Context: [base_context](../knowledge/base_context.md)

## Role
技术特性→用户价值: Feature → Capability → Outcome。

## Conversion Rules
| 类别 | Feature | Capability | Outcome |
|------|---------|-----------|---------|
| AI | AI Workflow | 交付自动化平台 | 交付周期缩短60% |
| AI | 多模型调度 | 智能资源分配 | 减少重复配置 |
| AI | RAG | 知识增强 | 回答准确率提升40% |
| AI | Agent协作 | 多智能体编排 | 复杂任务并行执行 |
| AI | Function Calling | 工具调用自动化 | 减少手动API集成 |
| DevOps | CI/CD | 交付流水线 | 发布频率提升3倍 |
| DevOps | 自动测试 | 质量保障自动化 | 回归成本降低60% |
| DevOps | 代码生成 | 开发加速 | 编码时间减少40% |
| DevOps | 容器化 | 环境标准化 | 部署一致性100% |
| Product | 文档自动化 | 知识沉淀 | 文档维护成本降低70% |
| Product | 权限管理 | 访问控制 | 安全合规100% |
| Product | 数据可视化 | 洞察呈现 | 决策效率提升50% |

## Generic Logic
不在规则库: Feature→"让用户做什么？"→Capability→"带来什么收益？"→Outcome

## Output
```json
{"feature":"<string>","capability":"<string>","outcome":"<string>"}
```
多个: `{"features":[{"feature":"<string>","capability":"<string>","outcome":"<string>"}]}`

## Examples
```
Input: "多模型调度"
Output: {"feature":"多模型调度","capability":"智能资源分配","outcome":"减少重复配置与上下文切换"}

Input: "实时数据同步"
Output: {"feature":"实时数据同步","capability":"数据一致性保障","outcome":"消除信息延迟，决策基于最新数据"}

Input: ["AI Workflow","自动测试","CI/CD"]
Output: {"features":[{"feature":"AI Workflow","capability":"交付自动化平台","outcome":"交付周期缩短60%"},{"feature":"自动测试","capability":"质量保障自动化","outcome":"回归成本降低60%"},{"feature":"CI/CD","capability":"交付流水线","outcome":"部署风险降低70%"}]}
```