# BOS-FS 灵活性原则

> **定位**: 定义 BOS-FS Skill 在不同项目场景下的灵活裁剪原则。在坚持质量底线的前提下，允许按需调整 Skill 组件的使用范围与深度。
>
> 核心思想: **灵活性服务于适配，而非降低交付标准。**
>
> 受众: 所有使用 BOS-FS 的团队负责人、项目经理、工程师。

---

## 1. 约束级别定义 (Constraint Levels)

BOS-FS 中的所有规范与规则按三个约束级别分级，便于按需裁剪：

| 级别 | 中文 | 含义 | 裁剪原则 | 违反后果 |
|------|------|------|---------|---------|
| **MUST** | 必须 | 缺少则交付不合格，任何场景不可省略 | **不可裁剪** | 交付质量不达标，评审不通过 |
| **SHOULD** | 推荐 | 缺少会降低质量但仍可接受，建议保留 | 可在精简模式下裁剪 | 质量评分下降，但交付可用 |
| **MAY** | 可选 | 根据项目类型和阶段选择，按需启用 | 按需决定是否启用 | 无影响，仅减少功能覆盖 |

### 1.1 约束级别在 BOS-FS 中的具体映射

| BOS-FS 元素 | 约束级别 | 说明 |
|-------------|---------|------|
| 目标清晰 (What/Why/Who) | MUST | 任何交付物必须清晰表达核心目标 |
| 价值声明 (Outcome) | MUST | 必须有可衡量的产出/价值描述 |
| README 基础结构 | MUST | 标题 + 项目简介 + 快速开始 |
| 五段式 README 完整结构 | SHOULD | Why → What → How → Result → Next |
| 提交组件完整性 (8个) | SHOULD | 完整包含 8 个组件，可裁剪 |
| 评审模拟五维度 | SHOULD | 完整评审含 5 类视角 |
| 安全策略文件 | SHOULD (安全交付: MUST) | 安全交付场景升级为 MUST |
| 开源贡献指南 | MAY (开源: SHOULD) | 仅开源项目需要 |
| 信任声明 / CII 对齐 | MAY | 商业交付通常不需要 |

---

## 2. 场景化适配规则 (Scenario-based Adaptation)

不同类型的项目对交付物的侧重不同。BOS-FS 应根据项目类型调整五段式 README 和各组件的权重。

### 2.1 适配矩阵

| 项目类型 | README 核心段 | 强调维度 | 可裁剪组件 | 评审侧重 |
|---------|-------------|---------|-----------|---------|
| **工具类项目** (CLI/库/SDK) | What + How | 用法示例、API 清晰、安装便捷 | 价值映射、用户画像 | 技术评审 + 开发者体验 |
| **商业项目** (SaaS/平台/服务) | 五段完整 | Why (商业价值) + Result (可度量产出) | 无 | 业务评审 + 产品评审 + 管理层视角 |
| **开源项目** | How + Contribution | 贡献流程、行为准则、社区规范 | 商业价值映射 | 社区评审 + 安全评审 + 可维护性 |
| **安全交付项目** | Result + Next | 风险发现、修复方案、整改计划 | 贡献指南 | 安全评审 + 合规评审 + 管理层视角 |

### 2.2 工具类项目适配

工具类项目的核心诉求是"拿来就能用"，交付文档应聚焦于功能说明和使用指南。

**README 建议结构 (3段)**:

| 段落 | 内容 | 约束级别 |
|------|------|---------|
| What | 工具是什么，解决什么问题 | MUST |
| How | 安装步骤、使用示例、参数说明 | MUST |
| Next | 未来计划 / 已知问题 / 反馈渠道 | SHOULD |

**提交组件建议**:

| 组件 | 是否需要 | 说明 |
|------|---------|------|
| README | MUST | 核心交付物 |
| 项目元信息 (meta) | MUST | 版本、依赖、许可证 |
| 技术栈说明 | SHOULD | 帮助开发者理解内部实现 |
| API/CLI 参考 | SHOULD | 工具类项目的核心文档 |
| 变更日志 (CHANGELOG) | SHOULD | 版本管理必需 |
| 其他组件 | MAY | 按需添加 |

### 2.3 商业项目适配

商业项目的核心诉求是"证明价值"，交付文档需要完整传达为什么做、做了什么、产生了什么价值。

**README 建议结构 (5段完整)**:

| 段落 | 内容 | 约束级别 |
|------|------|---------|
| Why | 业务背景、痛点、为什么做 | MUST |
| What | 解决方案、核心功能 | MUST |
| How | 技术实现、部署方式 | SHOULD |
| Result | 可度量的产出、商业价值 | MUST |
| Next | 路线图、后续计划 | SHOULD |

**提交组件建议**: 全部 8 个组件，不可裁剪。

### 2.4 开源项目适配

开源项目的核心诉求是"降低参与门槛"，交付文档需要让贡献者快速理解项目并参与进来。

**README 建议结构 (4段)**:

| 段落 | 内容 | 约束级别 |
|------|------|---------|
| Why | 项目动机，简要说明 | SHOULD |
| What | 项目功能与定位 | MUST |
| How | 安装、使用、贡献指南 | MUST |
| Contribution | 如何参与、行为准则、PR 流程 | MUST |

**额外交付物**:

| 文件 | 约束级别 |
|------|---------|
| CONTRIBUTING.md | MUST |
| CODE_OF_CONDUCT.md | SHOULD |
| SECURITY.md | SHOULD |
| LICENSE | MUST |

### 2.5 安全交付项目适配

安全交付的核心诉求是"清晰传达风险与修复"，交付文档需要让管理层理解风险、让技术团队知道如何修复。

**README 建议结构 (4段)**:

| 段落 | 内容 | 约束级别 |
|------|------|---------|
| What | 服务范围、测试目标 | MUST |
| Result | 风险发现、风险等级分布、关键发现 | MUST |
| How | 测试方法、工具链、测试范围 | SHOULD |
| Next | 修复建议、整改计划、复测安排 | MUST |

**额外交付物**:

| 文件 | 约束级别 |
|------|---------|
| 执行摘要 | MUST |
| 技术发现详情 | MUST |
| 风险评估矩阵 | MUST |
| 修复优先级列表 | MUST |

---

## 3. 精简模式 vs 完整模式 (Lite vs Full Mode)

BOS-FS 支持两种运行模式，以适应不同交付要求的项目。

### 3.1 模式对比总览

| 维度 | 精简模式 (Lite) | 完整模式 (Full) |
|------|----------------|----------------|
| 适用场景 | 个人项目 / MVP / 内部工具 / 快速原型 | 商业发布 / 开源发布 / 客户交付 / 融资材料 |
| README 段落 | 3 段 (What / How / Next) | 5 段完整 (Why → What → How → Result → Next) |
| 提交组件 | 2 个核心 (README + meta) | 全部 8 个组件 |
| 评审模式 | 轻量模式 (核心维度) | 完整模式 (所有维度) |
| Pipeline 阶段 | 可选子集 | 完整 Pipeline |
| 生成时间 | ~5-15 分钟 | ~30-60 分钟 |
| 输出文件大小 | ~5-20 KB | ~50-200 KB |

### 3.2 精简模式详解

**适用条件** (满足任一即可):

- 个人项目或小型团队内部使用
- MVP / 概念验证阶段
- 内部工具，无外部交付要求
- 快速原型，需要快速验证思路
- 时间紧迫 (< 1 天交付周期)

**精简模式配置**:

```yaml
mode: lite
readme:
  sections:
    - what          # MUST
    - how           # MUST
    - next          # SHOULD
  excluded:
    - why           # MAY: 精简模式下可省略
    - result        # MAY: 精简模式下可省略

submission:
  required_components:
    - readme        # MUST
    - meta          # MUST
  optional_components:
    - tech_stack
    - value_proposition
    - user_persona
    - outcome_mapping
    - architecture
    - changelog

review:
  mode: lite
  dimensions:
    - completeness  # 完整性检查
    - clarity       # 清晰度检查
  optional_dimensions:
    - feasibility   # MAY: 精简模式下可选
    - business      # MAY: 精简模式下可选
    - security      # MAY: 精简模式下可选
```

### 3.3 完整模式详解

**适用条件** (满足任一即可):

- 商业产品正式发布
- 开源项目首次发布或重大版本
- 面向客户的正式交付
- 融资 / 路演材料准备
- 合规 / 审计要求
- 合同明确交付标准

**完整模式配置**:

```yaml
mode: full
readme:
  sections:
    - why             # MUST
    - what            # MUST
    - how             # SHOULD
    - result          # MUST (商业/安全交付)
    - next            # SHOULD

submission:
  required_components:
    - readme           # MUST
    - meta             # MUST
    - tech_stack       # MUST
    - value_proposition # MUST
    - user_persona     # MUST
    - outcome_mapping  # MUST
    - architecture     # SHOULD
    - changelog        # SHOULD

review:
  mode: full
  dimensions:
    - completeness    # MUST
    - feasibility     # MUST
    - business        # MUST (商业项目)
    - security        # MUST (安全交付)
    - innovation      # SHOULD
```

---

## 4. 按需执行原则 (On-Demand Execution)

BOS-FS Pipeline 包含多个阶段，但**不必执行所有阶段**。应根据项目当前阶段和交付目标，选择最合适的 Skill 组合。

### 4.1 Pipeline 阶段总览

BOS-FS Pipeline 按执行顺序包含以下阶段：

| 阶段 | Skill | 输入 | 输出 | 约束级别 |
|------|-------|------|------|---------|
| 1 | Goal Refiner | 项目描述 | 结构化的目标定义 (persona/problem/solution/outcome) | MUST |
| 2 | README Refactor | 目标定义 | 标准化 README | MUST |
| 3 | Outcome Mapper | 功能列表 | 价值映射 (Feature → Capability → Outcome) | SHOULD |
| 4 | Submission Builder | 所有组件 | 完整交付包 | SHOULD |
| 5 | Reviewer Simulator | 交付包 | 评审报告 + 改进建议 | SHOULD |

### 4.2 场景 → Skill 组合映射

| 场景 | 推荐 Skill 组合 | 模式 | 说明 |
|------|---------------|------|------|
| **快速原型** | Goal Refiner → README Refactor | Lite | 快速产出可用文档，验证思路 |
| **内部工具** | README Refactor | Lite | 已有清晰目标，直接生成文档 |
| **客户交付** | 完整 Pipeline (全部 5 阶段) | Full | 面向客户的正式交付，不可裁剪 |
| **开源发布** | 完整 Pipeline + 开源评审 | Full | 需额外验证 CONTRIBUTING / CODE_OF_CONDUCT |
| **融资材料** | Goal Refiner → Outcome Mapper → 投资评审 | Full | 强化价值表达，侧重商业评审 |
| **安全交付** | 完整 Pipeline (安全模式) | Full | Result 阶段强化风险/修复表达 |
| **迭代更新** | README Refactor + Submission Builder | Lite | 已有基础，仅更新文档和交付包 |
| **合规审查** | Reviewer Simulator (安全+合规维度) | Full | 已有交付物，需要审查 |

### 4.3 典型场景执行路径

#### 场景 A: 快速原型 (15 分钟)

```
[输入] 一段项目描述
   ↓
Goal Refiner (提炼目标)
   ↓
README Refactor (生成 3 段式 README)
   ↓
[输出] 可用 README.md
```

#### 场景 B: 客户交付 (60 分钟)

```
[输入] 项目描述 + 功能列表 + 技术架构
   ↓
Goal Refiner (目标定义)
   ↓
README Refactor (5 段式 README)
   ↓
Outcome Mapper (价值映射)
   ↓
Submission Builder (构建完整交付包)
   ↓
Reviewer Simulator (模拟评审 → 修正)
   ↓
[输出] 完整交付包 (8 个组件 + 评审报告)
```

#### 场景 C: 融资材料 (45 分钟)

```
[输入] 项目描述 + 商业数据
   ↓
Goal Refiner (强化 problem / outcome 表达)
   ↓
Outcome Mapper (Feature → 商业价值映射)
   ↓
Reviewer Simulator (商业/投资人视角评审)
   ↓
[输出] 价值说明文档 + 评审报告
```

---

## 5. 质量底线 (Quality Floor)

灵活性不等于降低质量。无论选择精简模式还是完整模式，都必须满足最小交付标准。

### 5.1 最小交付标准 (Minimum Viable Delivery)

任何交付物必须满足以下条件：

| 维度 | 最低要求 | 约束级别 |
|------|---------|---------|
| 目标表达 | 读者能在 30 秒内理解项目是什么 | MUST |
| 功能描述 | 核心功能无歧义描述 | MUST |
| 使用说明 | 读者能按步骤完成安装/使用 | MUST |
| 技术诚实 | 不夸大能力，不隐瞒已知问题 | MUST |
| 版本信息 | 明确的版本号或时间戳 | MUST |
| 联系方式 | 至少一个反馈/联系渠道 | MUST |

### 5.2 质量底线检查清单

在执行任何精简操作前，确认以下底线未被破坏：

- [ ] 目标表达是否清晰？(What + 目标用户)
- [ ] 核心价值是否传达？(解决什么问题)
- [ ] 基本使用路径是否可执行？(安装 → 使用)
- [ ] 技术栈/依赖是否明确？
- [ ] 是否存在虚假或夸大的声明？
- [ ] 是否包含版本或时间标识？

### 5.3 不可违反的 MUST 规则

以下规则在任何场景下都不可违反：

| # | 规则 | 说明 |
|---|------|------|
| 1 | 目标必须清晰 | 不能出现"这是一个工具"这类模糊描述，必须说明是什么工具、为谁、解决什么问题 |
| 2 | 价值必须可理解 | 技术语言必须配套商业/用户语言的翻译 |
| 3 | 使用路径必须可执行 | 安装和使用说明必须可实际操作，不能是占位符 |
| 4 | 不可隐瞒风险 | 已知问题、限制、风险必须披露 |
| 5 | 评审必须覆盖核心维度 | 精简模式下至少检查完整性和清晰度 |
| 6 | 输出必须可审计 | 所有交付物必须包含版本/时间/作者信息 |

---

## 6. 快速决策指南

根据以下条件快速决定使用哪种模式：

```
你的项目是？
│
├─ 个人项目 / 学习笔记 / 实验代码
│  └→ 精简模式 | 仅 README Refactor
│
├─ 内部工具 / 团队脚本
│  └→ 精简模式 | Goal Refiner → README Refactor
│
├─ MVP / 概念验证 / 快速原型
│  └→ 精简模式 | Goal Refiner → README Refactor
│
├─ 即将迭代的已有项目
│  └→ 精简模式 | README Refactor + Submission Builder
│
├─ 商业产品正式发布
│  └→ 完整模式 | 完整 Pipeline
│
├─ 开源项目首次发布
│  └→ 完整模式 | 完整 Pipeline + 开源评审
│
├─ 面向客户的正式交付
│  └→ 完整模式 | 完整 Pipeline (不可裁剪)
│
├─ 融资 / 路演材料
│  └→ 完整模式 | Goal Refiner → Outcome Mapper → 投资评审
│
└─ 安全服务交付
   └→ 完整模式 | 完整 Pipeline (安全模式)
```

---

## 7. 相关文档

- [适用场景](./delivery_scenarios.md) — BOS-FS 的 8 大适用场景详解
- [团队拓扑](./team_topology.md) — 如何按团队角色配置 BOS-FS
- [ROI 评估](./roi_framework.md) — BOS-FS 的投资回报分析
- [差异化定位](./differentiation.md) — 与同类工具的对比
- [Flow 指标](./flow_metrics.md) — 如何衡量 BOS-FS 对交付流的影响
