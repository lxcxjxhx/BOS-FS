---
name: outcome-mapper
description: 价值转换时将技术特性翻译为用户能力与业务价值（Feature → Capability → Outcome）。
---

# Outcome Mapper
**version**: 0.2.7
> Context: [base_context](../knowledge/base_context.md)

## Role
技术特性→用户价值: Feature → Capability → Outcome。

## Input
Accepted formats:
- **string** — single feature description (e.g., `"多模型调度"`)
- **array of strings** — multiple feature descriptions (e.g., `["AI Workflow","自动测试","CI/CD"]`)

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

## Input Validation
- 最小输入: ≥ 1 个功能描述
- 纯技术描述 → 推断用户价值
- 空输入 → 输出错误提示

## Error Handling
- 输入为空/缺失 → 输出错误信息并说明需要补充
- 字段缺失 → 标注"未明确"
- 矛盾信息 → 取最新/最主要的

## Output
Unified format — always wraps results in `features` array:
```json
{"features":[{"feature":"<string>","capability":"<string>","outcome":"<string>"}]}
```
- **Single feature input** → `{"features":[{...}]}` (array with 1 element)
- **Multiple feature input** → `{"features":[{...},{...},...]}` (array with N elements)

## Output Schema

### 统一 JSON Schema（支持单特性/多特性）
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "features": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "feature": { "type": "string", "minLength": 1, "description": "技术特性" },
          "capability": { "type": "string", "minLength": 1, "description": "用户能力" },
          "outcome": { "type": "string", "minLength": 1, "description": "用户价值/收益" }
        },
        "required": ["feature", "capability", "outcome"],
        "additionalProperties": false
      },
      "minItems": 1
    }
  },
  "required": ["features"],
  "additionalProperties": false
}
```

> **变体说明**:
> - **单特性输入**: `{"features":[{"feature":"多模型调度","capability":"智能资源分配","outcome":"减少重复配置"}]}`
> - **多特性输入**: `{"features":[{"feature":"AI Workflow",...},{"feature":"自动测试",...},{"feature":"CI/CD",...}]}`

### 字段类型说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| feature | string | ✅ | 技术特性描述，源自输入 |
| capability | string | ✅ | 翻译为用户能力："让用户做什么？" |
| outcome | string | ✅ | 翻译为用户价值/收益："带来什么收益？" |

### 验证规则
- **格式约束**: 统一输出为 `{"features":[...]}` 结构，须为单行纯JSON
- **必填字段**: 每个特性对象中 `feature`, `capability`, `outcome` 三个字段缺一不可
- **非空校验**: 所有字段值不得为空字符串 `""`，最小长度为1
- **features 数组**: 至少包含1个元素（`minItems: 1`）
- **禁止额外字段**: 特性对象和根对象均不允许出现schema定义之外的字段

## Examples
```
Input: "多模型调度"
Output: {"features":[{"feature":"多模型调度","capability":"智能资源分配","outcome":"减少重复配置与上下文切换"}]}

Input: "实时数据同步"
Output: {"features":[{"feature":"实时数据同步","capability":"数据一致性保障","outcome":"消除信息延迟，决策基于最新数据"}]}

Input: ["AI Workflow","自动测试","CI/CD"]
Output: {"features":[{"feature":"AI Workflow","capability":"交付自动化平台","outcome":"交付周期缩短60%"},{"feature":"自动测试","capability":"质量保障自动化","outcome":"回归成本降低60%"},{"feature":"CI/CD","capability":"交付流水线","outcome":"部署风险降低70%"}]}
```

## Anti-Patterns
- **Capability只是Feature的同义词替换**：如"多模型调度"→"多模型路由"，未真正翻译为用户能力。
- **Outcome写技术收益而非业务收益**：如"API响应<100ms"应转译为"用户无需等待加载"。
- **对未提及的功能编造outcome**：输入只提了1个功能却输出3个outcome，超出输入范围。
- **多个特性合并为一个对象**：统一使用features数组，即使是单特性也包裹在数组中。
- **Capability为空或"未明确"**：每个feature必须有明确capability，"未明确"表示映射失败。
- **循环特性引用**：如"A依赖B，B依赖A"→ 检测并标记"循环依赖，取最主要链路"。
- **Outcome过于模糊**（如"提升体验"/"改善效率"）→ 必须包含量化指标或可验证维度。

## Edge Cases
- **输入为嵌套技术描述**（如"基于OAuth2+JWT的RBAC鉴权"）→ 拆解为独立feature逐项映射。
- **输入仅含业务描述无技术特性**（如"让用户快速发布内容"）→ 反推可能的feature并标注"（推断）"。
- **输入feature间存在依赖关系**（"先认证再授权"）→ 保持features数组顺序，在outcome中体现依赖价值。
- **输入包含完全不在规则库的技术**→ 走Generic Logic链路，逐问"让用户做什么？""带来什么收益？"。

## Quality Gates
- [ ] 每个feature是否都映射了capability和outcome？
- [ ] capability是否回答了"让用户做什么"而非技术同义词？
- [ ] outcome是否体现业务/用户价值而非技术指标？
- [ ] 输出是否使用了统一的`{"features":[...]}`格式？
- [ ] 输出是否为合法单行纯JSON？

## 方法论来源与学术诚信

本 Skill 的方法论来源于**作者亲自阅读以下书籍并提炼核心要点**，非 AI 自动处理或简单摘要。

| 启发来源 | 核心贡献 |
|----------|----------|
| [Product Management in Practice](Matt LeMay) | Feature→Capability→Outcome 转换链 |
| [Accelerate](Nicole Forsgren 等) | 效能指标量化方法 |

> **声明**: 本 Skill 中的方法论启发自上述书籍（见表格），所有代码实现、示例和知识重构均为作者原创。建议读者支持正版，购买原书以获得更完整的论述和案例。
