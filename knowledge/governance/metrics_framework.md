# BOS-FS 交付效能指标体系 (Delivery Metrics Framework)

> 来源: 综合 (Accelerate DORA + Engineering MLOps)
> 映射: BOS-FS 五层架构 → Governance Layer + Runtime Layer
> 用途: 量化评估从项目意图到完整提交包的全流程效率、质量与可信度，提供 DORA 指标映射与效能度量模型。

本文件定义 BOS-FS（Submission Engineering Runtime）交付效能指标体系，用于量化评估从项目意图到完整提交包的全流程效率、质量与可信度。

---

## 一、DORA 四指标映射

将 DORA 四大指标映射到 BOS-FS 运行时上下文。

| DORA 指标 | BOS-FS 定义 | 采集方式 | 单位 |
|-----------|-------------|----------|------|
| **Lead Time for Changes** | 从项目描述输入到完整提交包生成的端到端时间 | `submission_build_timestamp - project_description_timestamp` | 小时 (h) |
| **Deployment Frequency** | 单位时间内提交包的更新/迭代频率 | 按自然周统计提交包版本号变更次数 | 次/周 |
| **Mean Time to Recovery (MTTR)** | 提交被拒后，从收到评审意见到修复并重新提交的时间 | `resubmission_timestamp - rejection_feedback_timestamp` | 小时 (h) |
| **Change Failure Rate** | 提交包被评审拒绝的比例 | `rejected_submissions / total_submissions × 100%` | 百分比 (%) |

### Elite / High / Medium / Low 分级基准

| 等级 | Lead Time | Deployment Frequency | MTTR | Change Failure Rate |
|------|-----------|---------------------|------|---------------------|
| **Elite** | < 1h | 按需（日均 ≥ 1） | < 1h | 0-5% |
| **High** | 1h - 24h | 每周 1-6 次 | 1h - 24h | 6-15% |
| **Medium** | 1d - 7d | 每月 1-3 次 | 1d - 7d | 16-30% |
| **Low** | > 7d | 少于每月 1 次 | > 7d | > 30% |

---

## 二、Flow Metrics

基于 Flow Framework 的效能指标，衡量 BOS-FS 内部处理流水线的流动效率。

### 2.1 Flow Velocity（流动速率）

单位时间内 BOS-FS 处理的提交包数量。

| 维度 | 说明 |
|------|------|
| **定义** | 单位时间（周/月）内完成 Submission Build 阶段的提交包总数 |
| **公式** | `completed_submissions / time_period` |
| **用途** | 评估团队/流水线的吞吐能力 |

### 2.2 Flow Efficiency（流动效率）

有效工作时间占总处理时间的比例。

| 维度 | 说明 |
|------|------|
| **定义** | 流水线主动处理时间（非等待状态）占总端到端时间的比例 |
| **公式** | `active_processing_time / total_end_to_end_time × 100%` |
| **用途** | 识别流程瓶颈（等待评审、等待反馈等非增值环节） |

### 2.3 Flow Time（流动时间）

提交包从进入流水线到完成构建的端到端耗时。

| 维度 | 说明 |
|------|------|
| **定义** | 单个提交包从 Goal Refinement 到 Submission Build 完成的总时长 |
| **公式** | `submission_complete_timestamp - goal_refinement_start_timestamp` |
| **用途** | 追踪单次交付周期的可预测性 |

### 2.4 Flow Load（流动负载）

流水线并行处理的提交包/任务数量。

| 维度 | 说明 |
|------|------|
| **定义** | 任一时刻处于活跃处理状态的提交包数量 |
| **公式** | `count(submissions where status ∈ [processing, reviewing, building])` |
| **用途** | 评估并发容量与过载风险 |

### Flow Metrics 基准

| 指标 | Elite | High | Medium | Low |
|------|-------|------|--------|-----|
| **Flow Velocity** | ≥ 10 次/周 | 5-9 次/周 | 2-4 次/周 | < 2 次/周 |
| **Flow Efficiency** | ≥ 70% | 50-69% | 30-49% | < 30% |
| **Flow Time (P50)** | < 2h | 2h - 8h | 8h - 2d | > 2d |
| **Flow Load** | 稳定 ≤ 3 | 3-5 | 5-8 | > 8（过载风险） |

---

## 三、Architecture Metrics

衡量 BOS-FS Skill 架构的设计质量，确保可插拔、可维护、可演进。

### 3.1 Coupling（耦合度）

Skill 间依赖程度。

| 维度 | 说明 |
|------|------|
| **定义** | 跨 Skill 调用与共享状态的数量和深度 |
| **采集方式** | 统计 Skill 间 import/reference 次数、共享配置文件数量 |
| **公式** | `coupling_score = (inter_skill_calls + shared_state_refs) / total_skills` |
| **目标** | 越低越好；理想值 < 0.3（平均每个 Skill 依赖少于 1 个其他 Skill） |

### 3.2 Cohesion（内聚度）

单一 Skill 内部职责的聚焦程度。

| 维度 | 说明 |
|------|------|
| **定义** | Skill 内部功能与其核心职责的相关度 |
| **采集方式** | 评审 Skill 描述与实际功能的匹配度；检查是否存在职责外溢 |
| **公式** | `cohesion_score = core_functions / total_functions` |
| **目标** | 越高越好；理想值 ≥ 0.8（80% 以上功能直接服务于核心职责） |

### 3.3 Modularity（可插拔性）

Skill 作为独立模块的可替换程度。

| 维度 | 说明 |
|------|------|
| **定义** | Skill 在不影响其他组件的前提下被替换/升级/移除的能力 |
| **采集方式** | 验证 Skill 接口契约完整性、热插拔测试结果、替换影响范围 |
| **评分** | 0-10 量表：10 = 完全热插拔无需修改其他代码；0 = 替换导致全局重构 |

### Architecture Metrics 基准

| 指标 | Elite | High | Medium | Low |
|------|-------|------|--------|-----|
| **Coupling Score** | < 0.2 | 0.2-0.35 | 0.35-0.5 | > 0.5 |
| **Cohesion Score** | ≥ 0.9 | 0.8-0.89 | 0.6-0.79 | < 0.6 |
| **Modularity Score** | ≥ 9.0 | 7.5-8.9 | 5.0-7.4 | < 5.0 |

---

## 四、Review Simulation Metrics

基于四类评审模拟（technical / investment / product / opensource）的效能指标。

### 4.1 四类评审通过率

| 评审类型 | 定义 | 通过阈值 | 采集方式 |
|----------|------|----------|----------|
| **技术评审** | 架构设计、代码质量、安全性、性能综合评分 | 加权分 ≥ 7.0/10 | `review_simulator` 输出 |
| **投资评审** | 市场规模、ROI 估算、竞品分析、预算合理性综合评分 | 加权分 ≥ 7.0/10 | `review_simulator` 输出 |
| **产品评审** | 需求匹配、用户体验、功能规划、路线图综合评分 | 加权分 ≥ 7.0/10 | `review_simulator` 输出 |
| **开源评审** | 社区价值、文档、可维护性、许可证综合评分 | 加权分 ≥ 7.0/10 | `review_simulator` 输出 |

### 4.2 加权综合评分

```
comprehensive_review_score = Σ(review_type_score × weight)
```

| 评审类型 | 权重 |
|----------|------|
| 技术评审 | 35% |
| 投资评审 | 20% |
| 产品评审 | 25% |
| 开源评审 | 20% |

### 4.3 拒绝原因分类

| 分类代码 | 拒绝原因 | 典型表现 |
|----------|----------|----------|
| **R-TECH** | 技术不可行 | 架构缺陷、安全风险、性能不达标 |
| **R-BIZ** | 商业价值不足 | 市场过小、ROI 为负、无差异化 |
| **R-PROD** | 产品设计缺陷 | 伪需求、体验差、范围蔓延 |
| **R-OS** | 开源合规问题 | 许可证冲突、文档缺失、社区价值低 |
| **R-TRUST** | 信任背书不足 | 无权威引用、无行业对标、透明度低 |

### Review Simulation Metrics 基准

| 指标 | Elite | High | Medium | Low |
|------|-------|------|--------|-----|
| **综合评审通过率** | ≥ 90% | 70-89% | 50-69% | < 50% |
| **技术评审通过率** | ≥ 95% | 80-94% | 60-79% | < 60% |
| **综合加权评分** | ≥ 8.5 | 7.5-8.4 | 6.0-7.4 | < 6.0 |
| **拒绝原因集中度** | 均匀分布 | 单一原因 < 50% | 单一原因 50-70% | 单一原因 > 70%（系统性问题） |

---

## 五、Trust Metrics

衡量项目信任背书的完整度与可信度。

### 5.1 权威引用覆盖率 (Authority Citation Coverage)

| 维度 | 说明 |
|------|------|
| **定义** | 项目文档中引用的权威标准占适用权威标准总数的比例 |
| **公式** | `cited_standards / applicable_standards × 100%` |
| **适用标准池** | OWASP Top 10、ISO 25010、NIST CSF、12-Factor App、Clean Architecture、DORA 指标、SPACE 框架等 |

### 5.2 行业对标完整度 (Industry Benchmark Completeness)

| 维度 | 说明 |
|------|------|
| **定义** | 项目对标分析覆盖的行业维度数量 |
| **公式** | `covered_benchmark_dimensions / total_relevant_dimensions × 100%` |
| **维度池** | Gartner Hype Cycle、Forrester Wave、CNCF Landscape、YC 评估标准、a16z 投资框架、Lean Canvas |

### 5.3 透明度指数 (Transparency Index)

| 维度 | 说明 |
|------|------|
| **定义** | 项目文档中风险披露、限制说明、透明度声明的完整度 |
| **评分项** | 风险披露完整度、已知限制说明、OpenSSF Scorecard 公开度、方法论数据支撑完整度 |
| **公式** | `transparency_score = (risk_disclosure + limitation_statement + scorecard_disclosure + data_backing) / 4 × 100%` |

### Trust Metrics 基准

| 指标 | Elite | High | Medium | Low |
|------|-------|------|--------|-----|
| **权威引用覆盖率** | ≥ 80% | 60-79% | 40-59% | < 40% |
| **行业对标完整度** | ≥ 75% | 55-74% | 35-54% | < 35% |
| **透明度指数** | ≥ 90% | 75-89% | 50-74% | < 50% |

---

## 六、测量方法与数据采集

### 6.1 数据源矩阵

| 指标类别 | 主要数据源 | 辅助验证 |
|----------|-----------|----------|
| DORA 指标 | 流水线时间戳、提交包版本记录 | 人工抽样审计 |
| Flow Metrics | 流水线各阶段状态日志 | 周期性的流程审计 |
| Architecture Metrics | 代码静态分析、Skill 依赖图谱 | 架构评审记录 |
| Review Metrics | `review_simulator` 输出日志 | 人工评审对比 |
| Trust Metrics | 文档内容分析、引用提取 | 第三方权威数据库交叉验证 |

### 6.2 采集频率

| 指标 | 采集频率 | 报告周期 |
|------|----------|----------|
| DORA Lead Time / MTTR | 实时 | 周报 + 月度趋势 |
| Deployment Frequency | 按事件触发 | 周报 |
| Change Failure Rate | 按事件触发 | 周报 |
| Flow Velocity / Efficiency / Time / Load | 实时 | 周报 + 看板 |
| Coupling / Cohesion | 每次代码变更 | 变更报告 |
| Modularity | 每月/季度 | 季度架构评审 |
| Review Pass Rate | 每次评审 | 评审报告 |
| Trust Metrics | 项目关键里程碑 | 里程碑报告 |

### 6.3 综合效能指数 (Delivery Effectiveness Index)

```
DEI = (DORA_Score × 30%) + (Flow_Score × 25%) + (Architecture_Score × 15%) + (Review_Score × 20%) + (Trust_Score × 10%)
```

| 维度分数 | 计算方法 |
|----------|----------|
| DORA_Score | 四项指标分别归一化后取平均 |
| Flow_Score | 四项指标分别归一化后取平均 |
| Architecture_Score | 耦合度取反 + 内聚度 + 可插拔性，归一化 |
| Review_Score | 综合评审通过率 × 加权评分归一化 |
| Trust_Score | 权威引用覆盖率 + 行业对标完整度 + 透明度指数，归一化 |

### DEI 等级

| 等级 | DEI 分值 | 含义 |
|------|----------|------|
| **Elite** | ≥ 9.0 | 交付效能卓越，可直接作为行业标杆 |
| **High** | 8.0 - 8.9 | 交付效能优秀，建议持续优化 |
| **Medium** | 6.0 - 7.9 | 交付效能合格，有改进空间 |
| **Low** | 4.0 - 5.9 | 交付效能不足，需要系统性改进 |
| **Critical** | < 4.0 | 交付效能严重不足，需要重新评估流程 |

---

## 交叉引用

- [rubrics.md](rubrics.md) — 评分标准（流水线评分 / README 评分 / 评审评分细则）
- [trust_framework.md](trust_framework.md) — 信任框架（权威引用 / 行业对标 / 透明度）
- [review_rules/](review_rules/) — 四类评审规则（技术 / 投资 / 产品 / 开源）
- [base_context.md](../base_context.md) — 基础上下文
