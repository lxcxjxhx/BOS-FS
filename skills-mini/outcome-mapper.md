---
name: outcome-mapper
description: 价值转换时将技术特性翻译为用户能力与业务价值（Feature → Capability → Outcome）。
---

# Outcome Mapper
**version**: 0.2.11
> Context: [base_context](../../knowledge/base_context.md)
> Full version: skills/outcome-mapper/SKILL.md

## Role
技术特性→用户价值: Feature → Capability → Outcome。

## Input
- **string** — 单特性 | **array** — 多特性
- 最小≥1功能 | 空→错误 | 纯技术→推断用户价值

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
**Generic**: 不在规则库→逐问"让用户做什么？""带来什么收益？"

## Output Schema
统一JSON: `{"features":[{"feature":"<string>","capability":"<string>","outcome":"<string>"}]}`
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| feature | string | ✅ | 源自输入 |
| capability | string | ✅ | "让用户做什么？" |
| outcome | string | ✅ | "带来什么收益？" |

**验证**: 单行纯JSON | feature/capability/outcome缺一不可 | 非空minLength≥1 | minItems≥1 | 无额外字段

## Examples
```
Input: "多模型调度"
Output: {"features":[{"feature":"多模型调度","capability":"智能资源分配","outcome":"减少重复配置与上下文切换"}]}
Input: ["AI Workflow","自动测试","CI/CD"]
Output: {"features":[{"feature":"AI Workflow","capability":"交付自动化平台","outcome":"交付周期缩短60%"},{"feature":"自动测试","capability":"质量保障自动化","outcome":"回归成本降低60%"},{"feature":"CI/CD","capability":"交付流水线","outcome":"部署风险降低70%"}]}
```

## Anti-Patterns
| 反模式 | 后果 |
|--------|------|
| Capability仅是Feature同义词 | 未翻译为用户能力 |
| Outcome写技术收益 | 应转译用户视角 |
| 编造未提及功能outcome | 超出输入范围 |
| 多特性合并为一个对象 | 须用features数组 |

## Edge Cases
| 场景 | 处理 |
|------|------|
| 嵌套技术描述 | 拆解独立feature逐项映射 |
| 仅业务描述无技术 | 反推feature标注"（推断）" |
| feature间存在依赖 | 保持数组顺序，outcome体现依赖 |
| 完全不在规则库 | 走Generic Logic链路 |

## Quality Gates
- [ ] 每个feature映射了capability和outcome？
- [ ] capability回答"让用户做什么"而非技术同义词？
- [ ] outcome体现业务/用户价值而非技术指标？
- [ ] 输出使用统一`{"features":[...]}`格式？
- [ ] 输出为合法单行纯JSON？

## 方法论来源
| 启发来源 | 核心贡献 |
|----------|----------|
| [Product Management in Practice](Matt LeMay) | Feature→Capability→Outcome 转换链 |
| [Accelerate](Nicole Forsgren 等) | 效能指标量化方法 |
