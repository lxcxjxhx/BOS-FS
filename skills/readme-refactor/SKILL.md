---
name: readme-refactor
description: 优化文档时将原始项目描述重构为专业 README（支持灵活裁剪结构）。
---

# README Refactor
**version**: 0.3.0
> Context: [base_context](../knowledge/base_context.md)

## Role
将项目描述重构为专业 README。默认推荐五段式（What/Why/How/Result/Next），但可根据项目类型、所处阶段灵活裁剪。

## 约束等级定义

| 等级 | 含义 | 执行要求 |
|------|------|----------|
| **MUST** | 必须包含 | 不可省略，否则视为不完整 |
| **SHOULD** | 应该包含 | 建议保留，除非有充分理由省略 |
| **MAY** | 可选包含 | 根据项目阶段与类型自行决定 |

## 五段式段落等级

| 段落 | 等级 | 说明 |
|------|------|------|
| What | **MUST** | 一句话价值描述，不可省略 |
| Why | SHOULD | 存在理由、痛点分析 |
| How | SHOULD | 架构、特性、快速开始 |
| Result | MAY | 量化效果、典型场景 |
| Next | MAY | 路线图、下一步行动 |

> 详细裁剪原则参见 [flexibility_principles.md](../knowledge/flexibility_principles.md)

## 场景适配指南

根据项目类型选择最适合的结构：

| 项目类型 | 推荐段落 | 段数 | 说明 |
|----------|----------|------|------|
| **工具类项目** | What + How + Next | 3 | 强调实用性与快速上手 |
| **商业项目** | What + Why + How + Result + Next | 5 | 完整五段式，面向客户/投资人 |
| **开源项目** | What + How + Contribution + (Next) | 3-4 | 强调贡献指南，Result 可省略 |
| **安全交付项目** | What + Result + Next | 3 | 强调风险修复与合规结果 |

## 按需裁剪原则

当信息不足或项目处于早期阶段时，允许以下裁剪方式：

1. **信息不足时**: 仅保留 What（MUST），其余标注"待补充"
2. **早期项目（0→1）**: What + How 即可，Result 无数据可留空
3. **维护期项目**: What + Result + Next，Why/How 可从历史文档引用
4. **内部工具**: What + How + Next 三段足够
5. **对外发布**: 五段式完整输出

## 推荐结构

以下为五段式推荐结构（非强制，可按需裁剪）：

```markdown
# [项目名称]
## What — 一句话价值
[技术 × 用户 × 收益 = 产品描述]
## Why — 为什么存在
### 痛点 - [用户问题]
### 现有方案不足 - [对比]
## How — 如何实现
### 架构
```
[ASCII图]
```
### 特性 - [特性]: [价值]
### 快速开始
```bash
[命令]
```
## Result — 效果
### 指标 - [量化收益]
### 场景 - [典型场景]
## Next — 路线图
- [ ] 近期：[1-3月]
- [ ] 中期：[3-6月]
- [ ] 远期：[6-12月]
```

## Output
Output is a complete Markdown document. Do NOT wrap in code fences. Output raw markdown text directly.

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
- [ ] **MUST**: 一句话价值清晰（非技术人员可理解）
- [ ] **SHOULD**: 包含 Why 或 How 至少一个
- [ ] **MAY**: 指标可量化（如有数据）
- [ ] **MAY**: Next 路线图（如项目处于活跃开发期）

## Example
```
Input: "# My Project\nAI workflow engine, multi-model, auto-test"
Output: "# 交付自动化平台\n## What\n帮助开发者将AI工作流从手动配置转为自动化，减少60%重复操作。\n## Why\n### 痛点\n- 多模型切换需重复配置\n- 测试与开发流程割裂\n### 现有方案不足\n- 传统CI/CD不理解AI工作流\n## How\n### 架构\n[Client]→[API Gateway]→[Workflow Engine]→[Model Router]→[Test Runner]\n### 特性\n- **智能调度**: 自动选择最优模型\n- **自动化测试**: 内置AI工作流测试\n- **一键交付**: 开发到发布全流程\n### 快速开始\n```bash\npip install bos-fs && bos-fs init && bos-fs run\n```\n## Result\n### 指标\n- 配置时间减少60%，测试覆盖率提升40%\n### 场景\n- 个人开发者：5分钟完成发布\n## Next\n- [ ] 近期：更多模型供应商\n- [ ] 中期：团队协作\n- [ ] 远期：企业级安全合规"
```

## Output Schema

### Markdown 灵活结构定义
输出应以 **What** 为核心（MUST），其余段落根据项目类型按需组合（SHOULD/MAY）：

| 段落 | 标题 | 约束等级 | 必含内容 |
|------|------|----------|----------|
| What | `## What — 一句话价值` | **MUST** | 技术 × 用户 × 收益 公式描述 |
| Why | `## Why — 为什么存在` | SHOULD | 痛点列表 + 现有方案不足 |
| How | `## How — 如何实现` | SHOULD | ASCII架构图 + 特性列表 + 快速开始命令 |
| Result | `## Result — 效果` | MAY | 量化指标 + 典型场景 |
| Next | `## Next — 路线图` | MAY | 近期/中期/远期规划 |

### 验证规则
- **What 段落必须存在**: 无论何种裁剪，What 段不可省略
- **What 非技术可理解**: 一句话价值必须让非技术人员能理解
- **架构图含数据流（如含 How 段）**: How 段若存在，应包含 ASCII 架构图，展示主要组件和数据流向
- **快速开始可执行（如含 How 段）**: How 段若存在，应包含可复制运行的命令（bash 代码块）
- **指标可量化（如含 Result 段且有数据）**: Result 段指标若存在数据，应包含数值或百分比
- **场景数量（如含 Result 段）**: Result 段建议包含至少2个典型使用场景
- **路线图三段（如含 Next 段）**: Next 段若存在，建议包含近期（1-3月）、中期（3-6月）、远期（6-12月）

## Anti-Patterns
- **What段写技术架构而非价值**：如"基于React+FastAPI的全栈应用"，非技术人员无法理解。
- **How段缺失架构图或命令不可执行**：读者无法5分钟内跑起来，README失去实用价值。
- **Next段路线图空泛**：写"持续优化"而非具体里程碑，失去路线规划意义。
- **虚构量化指标**：输入未提供任何数据却编造"提升80%"，导致文档不可信。

## Edge Cases
- **输入仅一句话（如"做了个聊天机器人"）**→ 标注"（内容不足，仅重构现有信息）"，基于有限信息补全结构，但至少保留 What。
- **输入已是完整README**→ 不重写已有有效内容，仅对模糊段落做精炼转换。
- **纯技术文档（无用户/场景描述）**→ 建议补充 Why 段痛点和 Result 段场景，否则标注"（推断）"。
- **多项目混合输入**→ 识别边界，仅重构主项目，其余作为 Next 段关联项。

## Quality Gates
- [ ] **MUST**: What 段落是否存在且非技术人员可理解？
- [ ] **SHOULD**: 是否包含 Why 或 How 至少一个段落？
- [ ] **MAY**: 如有 Result 段，指标是否包含具体数值？
- [ ] **MAY**: 如有 How 段，快速开始命令是否可复制执行？

## 方法论来源与学术诚信

本 Skill 的方法论来源于**作者亲自阅读以下书籍并提炼核心要点**，非 AI 自动处理或简单摘要。

| 启发来源 | 核心贡献 |
|----------|----------|
| [Product Management in Practice](Matt LeMay) | 产品文档结构 |
| [Continuous Discovery Habits](Teresa Torres) | 价值主张表达 |

> **声明**: 本 Skill 中的方法论启发自上述书籍（见表格），所有代码实现、示例和知识重构均为作者原创。建议读者支持正版，购买原书以获得更完整的论述和案例。