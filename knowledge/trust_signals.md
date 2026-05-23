# 信任背书体系（Trust Signals）

本文件为使用 BOS-FS 框架的项目提供权威引用框架，用于在技术评审、架构答辩、项目交付等场景中引用行业公认标准，增强项目的可信度与工程严谨性。

---

## 一、技术权威引用

### 1. OWASP Top 10

| 维度 | 内容 |
|------|------|
| **名称** | OWASP Top 10 Web Application Security Risks |
| **来源** | [OWASP Foundation](https://owasp.org/www-project-top-ten/) |
| **适用场景** | 安全架构评审、渗透测试报告、合规审计（等保/GDPR） |
| **如何引用** | 在安全设计文档中标注"本系统针对 OWASP Top 10（2021版）各项风险项设计了相应防护机制"，并逐项映射到具体控制措施（如输入校验、参数化查询、CSP策略等） |
| **可信度等级** | 🔴 高 |

### 2. 12-Factor App

| 维度 | 内容 |
|------|------|
| **名称** | The Twelve-Factor App |
| **来源** | [Heroku / 12factor.net](https://12factor.net/) |
| **适用场景** | 云原生架构评审、SaaS 应用设计评审、容器化部署方案评审 |
| **如何引用** | 在架构设计文档中声明"本系统遵循 12-Factor App 原则构建"，逐项说明代码库管理、依赖隔离、配置外部化、无状态进程、端口绑定、进程并发等要素的落地方式 |
| **可信度等级** | 🔴 高 |

### 3. Clean Architecture

| 维度 | 内容 |
|------|------|
| **名称** | Clean Architecture |
| **来源** | Robert C. Martin, [Blog Post](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) / 《架构整洁之道》 |
| **适用场景** | 架构分层评审、依赖管理评审、模块化设计评审 |
| **如何引用** | 在架构图中明确标注 Entities → Use Cases → Interface Adapters → Frameworks 四层结构，并在评审中说明"本架构采用 Clean Architecture 实现依赖倒置，确保业务逻辑独立于框架与外部服务" |
| **可信度等级** | 🔴 高 |

### 4. SOLID 原则

| 维度 | 内容 |
|------|------|
| **名称** | SOLID — 面向对象设计五原则 |
| **来源** | Robert C. Martin 整理命名，Michael Feathers 提出首字母缩写 |
| **适用场景** | 代码评审、设计模式评审、重构方案评审 |
| **如何引用** | 在代码评审报告中说明关键模块如何体现单一职责（SRP）、开闭原则（OCP）、里氏替换（LSP）、接口隔离（ISP）、依赖倒置（DIP），可配合 UML 类图展示 |
| **可信度等级** | 🟡 中 |

### 5. TDD 测试驱动开发

| 维度 | 内容 |
|------|------|
| **名称** | Test-Driven Development（TDD） |
| **来源** | Kent Beck, 《Test-Driven Development: By Example》 |
| **适用场景** | 质量体系评审、测试覆盖率评审、持续集成流程评审 |
| **如何引用** | 在质量报告中声明"核心模块采用 TDD 红-绿-重构循环开发"，附测试覆盖率数据、测试金字塔结构图、CI 流水线中自动化测试执行情况 |
| **可信度等级** | 🟡 中 |

---

## 二、行业对标

### 1. Gartner 技术成熟度曲线（Hype Cycle）

| 维度 | 内容 |
|------|------|
| **名称** | Gartner Hype Cycle |
| **来源** | [Gartner Research](https://www.gartner.com/en/research/methodologies/gartner-hype-cycle) |
| **适用场景** | 技术选型评审、创新技术引入评审、战略技术规划 |
| **如何引用** | 在技术选型报告中定位所采用技术处于 Hype Cycle 的阶段（技术触发期 → 期望膨胀期 → 泡沫破裂低谷期 → 稳步爬升复苏期 → 生产成熟期），说明选型决策的理性依据，避免盲目追新或保守滞后 |
| **可信度等级** | 🔴 高 |

### 2. Forrester Wave 评估框架

| 维度 | 内容 |
|------|------|
| **名称** | Forrester Wave |
| **来源** | [Forrester Research](https://www.forrester.com/research/methodology/) |
| **适用场景** | 供应商选型评审、工具链评估、平台能力对比 |
| **如何引用** | 引用 Forrester Wave 对相关品类（如 DevOps 平台、API 管理、低代码等）的评估报告，将项目所采用工具/平台与 Leader/Strong Performer/Contender 象限对应，辅助选型决策说明 |
| **可信度等级** | 🔴 高 |

### 3. CNCF Cloud Native Landscape

| 维度 | 内容 |
|------|------|
| **名称** | CNCF Cloud Native Landscape |
| **来源** | [CNCF Landscape](https://landscape.cncf.io/) |
| **适用场景** | 云原生技术栈评审、微服务架构评审、开源技术选型 |
| **如何引用** | 在架构文档中标注项目所采用的各层技术组件（编排、服务网格、可观测性、CI/CD 等）在 CNCF Landscape 中的分类位置，说明技术栈符合云原生基金会认可的技术图谱 |
| **可信度等级** | 🔴 高 |

### 4. 行业分类选型指南

| 维度 | 内容 |
|------|------|
| **名称** | 项目类型 × 行业对标映射指南 |
| **来源** | 综合 Gartner / Forrester / CNCF / IDC 分类体系 |
| **适用场景** | 项目立项评审、技术战略规划 |
| **如何引用** | 根据项目类型选择对应分类体系：<br>• **SaaS / 云应用** → 12-Factor App + CNCF Landscape + Gartner Cloud SaaS Hype Cycle<br>• **企业级平台** → Forrester Wave（对应品类）+ Clean Architecture<br>• **安全敏感系统** → OWASP Top 10 + NIST CSF<br>• **DevOps / 工具链** → CNCF Landscape + DORA 指标 + SPACE 框架 |
| **可信度等级** | 🟡 中 |

---

## 三、方法论背书

### 1. DORA 四大指标

| 维度 | 内容 |
|------|------|
| **名称** | DORA Metrics — 部署频率、Lead Time for Changes、MTTR、变更失败率 |
| **来源** | Google DevOps Research & Assessment (DORA), 《Accelerate: The Science of Lean Software and DevOps》 |
| **适用场景** | 工程效能评审、DevOps 成熟度评估、团队绩效衡量 |
| **如何引用** | 在工程效能报告中量化展示四项指标当前值与行业基准（Elite / High / Medium / Low）对比，说明持续交付能力。例如："本季度部署频率达日均 X 次（Elite 级别），Lead Time 中位数 X 小时，MTTR < X 分钟，变更失败率 X%" |
| **可信度等级** | 🔴 高 |

### 2. SPACE 框架

| 维度 | 内容 |
|------|------|
| **名称** | SPACE Framework — 开发者生产力五维度 |
| **来源** | Nicole Forsgren 等, ACM Queue 2021, [论文链接](https://queue.acm.org/detail.cfm?id=3454124) |
| **适用场景** | 研发效能评审、团队健康度评估、工程改进规划 |
| **如何引用** | 从五个维度（Satisfaction & Well-being、Performance、Activity、Communication & Collaboration、Efficiency & Flow）设计度量指标，避免单一指标（如代码行数）偏见。在评审中说明"采用 SPACE 框架多维度评估研发效能，各维度基线值与改进目标如下…" |
| **可信度等级** | 🟡 中 |

### 3. DevOps 成熟度模型

| 维度 | 内容 |
|------|------|
| **名称** | DevOps Maturity Model |
| **来源** | 综合 DORA / CMMI / 行业实践，分为五阶段：初始 → 可重复 → 已定义 → 已管理 → 优化 |
| **适用场景** | 组织级 DevOps 转型评审、工程能力评估、改进路线图规划 |
| **如何引用** | 在评估报告中定位项目/团队当前所处阶段，说明各阶段特征与目标阶段差距，并附改进路线图。例如："当前处于「已定义」阶段（标准化 CI/CD 流水线与自动化测试已建立），下一阶段目标为「已管理」阶段（引入量化度量与持续反馈闭环）" |
| **可信度等级** | 🟡 中 |

### 4. 工程严谨性证明指南

| 维度 | 内容 |
|------|------|
| **名称** | 方法论组合引用策略 |
| **来源** | 综合上述方法论的最佳实践 |
| **适用场景** | 技术评审、架构答辩、项目验收、晋升评审 |
| **如何引用** | 按场景组合引用以证明工程严谨性：<br><br>**架构评审场景：** Clean Architecture + SOLID + OWASP Top 10<br>**交付评审场景：** DORA 指标 + 12-Factor App + DevOps 成熟度<br>**效能评审场景：** SPACE 框架 + DORA 指标 + TDD 覆盖率<br>**技术选型场景：** Gartner Hype Cycle + Forrester Wave + CNCF Landscape<br><br>引用时需提供具体数据支撑（指标值、覆盖率、阶段定位），而非仅声明"遵循 XX 原则"。 |
| **可信度等级** | 🔴 高（组合引用时） |

---

## 使用指引

1. **按需引用**：不必在单次评审中引用全部内容，根据评审类型选择 2-3 个最相关的背书即可。
2. **数据支撑**：所有方法论引用必须附带可量化的数据或具体实践说明，空泛声明不具说服力。
3. **时效性**：关注各标准的最新版本（如 OWASP Top 10 2021、DORA 年度报告），引用时注明版本/年份。
4. **内部映射**：在项目文档中建立"本系统实践 ↔ 权威标准"的映射表，便于评审时快速定位证据。
