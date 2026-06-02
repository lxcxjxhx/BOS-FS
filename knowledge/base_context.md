# BOS-FS Base Context
> 引用: `../knowledge/base_context.md`

## Output Conventions
- JSON 输出：必须可被 `JSON.parse()` 直接解析，无额外文本
- Markdown 输出：What/Why/How/Result/Next 五段式
- 语言：与输入保持一致，不主动翻译
- 数值/指标必须可验证，不可虚构

## 交叉引用

### Intent Layer
- [discovery_framework.md](intent/discovery_framework.md) — 发现框架（持续发现/机会树/假设测试/持续访谈/提交前检查清单）
- [product_value_framework.md](intent/product_value_framework.md) — 产品价值框架（运营模式/价值流映射/Feature→Capability→Outcome转换）

### Adoption Layer
- [team_topology.md](adoption/team_topology.md) — 团队拓扑（四种团队类型/三种交互模式/RACI矩阵/认知负荷管理）
- [flow_metrics.md](adoption/flow_metrics.md) — Flow效能度量（Flow Velocity/Efficiency/Time/Load/仪表盘模板）

### Runtime Layer
- [architecture_patterns.md](runtime/architecture_patterns.md) — 架构模式（模块化/事件驱动/演化式架构/权衡分析/适配度函数）

### Execution Layer
- [templates/](execution/templates/) — 模板库（README/演示指南/Pitch/提交检查清单）

### Governance Layer
- [trust_framework.md](governance/trust_framework.md) — 信任框架（技术权威引用/行业对标/开源评估/方法论背书/透明度要求/验证方法/引用规范/使用指引）
- [rubrics.md](governance/rubrics.md) — 评分标准（流水线/README/五类评审评分细则）
- [metrics_framework.md](governance/metrics_framework.md) — 交付效能指标（DORA/Flow/Architecture/Review/Trust/DEI综合指数）
- [ai_delivery_framework.md](governance/ai_delivery_framework.md) — AI交付框架（Prompt工程/上下文管理/质量评估/Agent编排/观测监控）
- [review_rules/](governance/review_rules/) — 评审规则库（技术/投资/产品/开源）

### Core
- [differentiation.md](adoption/differentiation.md) — 核心差异化