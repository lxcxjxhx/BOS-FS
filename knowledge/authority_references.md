# 权威引用库

> 用于项目评审的权威参考框架集合，涵盖技术评审、商业评审、开源评估三大领域。

---

## 一、技术评审权威框架

### ISO/IEC 25010 软件质量模型

| 维度 | 说明 |
|------|------|
| **8大质量特性** | 功能适合性、性能效率、兼容性、可用性、可靠性、安全性、可维护性、可移植性 |
| **适用场景** | 技术评审、产品验收 |
| **引用方式** | 按8维度逐一评估，给出评分 |
| **可信度等级** | 高（国际标准） |

> 来源：ISO/IEC 25010:2023 — Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE)

### NIST 网络安全框架 (Cybersecurity Framework)

| 维度 | 说明 |
|------|------|
| **5大核心功能** | 识别 (Identify)、保护 (Protect)、检测 (Detect)、响应 (Respond)、恢复 (Recover) |
| **适用场景** | 安全评审、合规审查 |
| **引用方式** | 对照5大功能说明项目安全设计 |
| **可信度等级** | 高（美国政府标准） |

> 来源：NIST Cybersecurity Framework (CSF) 2.0 — National Institute of Standards and Technology

### CWE/SANS Top 25 最危险软件错误

| 维度 | 说明 |
|------|------|
| **内容** | 25类最常见的严重软件安全漏洞（CWE-79 XSS、CWE-89 SQL注入等） |
| **适用场景** | 代码安全评审 |
| **引用方式** | 说明项目已规避的 CWE 类别 |
| **可信度等级** | 高 |

> 来源：CWE Top 25 — Common Weakness Enumeration / SANS Institute

---

## 二、商业评审权威框架

### Y Combinator 评估标准

| 维度 | 说明 |
|------|------|
| **四维度** | 团队、市场、产品、增长 |
| **适用场景** | 投资路演、创业评审 |
| **引用方式** | 按YC四维度准备Pitch |
| **可信度等级** | 高（顶级孵化器标准） |

> 来源：Y Combinator — YC Startup School / Application Criteria

### a16z 投资框架

| 维度 | 说明 |
|------|------|
| **评估维度** | 市场规模、团队、产品差异化、增长飞轮 |
| **适用场景** | 融资评审 |
| **引用方式** | 对标a16z投资评估维度 |
| **可信度等级** | 高 |

> 来源：Andreessen Horowitz (a16z) — Investment Thesis & Framework

### Lean Canvas 商业模式画布

| 维度 | 说明 |
|------|------|
| **9个模块** | 问题、解决方案、价值主张、客户、渠道、收入、成本、指标、壁垒 |
| **适用场景** | 商业模式评审 |
| **引用方式** | 按9模块填写商业计划 |
| **可信度等级** | 高 |

> 来源：Ash Maurya — Running Lean / Lean Canvas

---

## 三、开源评估框架

### CHAOSS 开源社区健康指标

| 维度 | 说明 |
|------|------|
| **核心指标** | 社区参与度、多样性、响应性、包容性 |
| **适用场景** | 开源项目评审 |
| **引用方式** | 使用CHAOSS指标评估项目社区健康度 |
| **可信度等级** | 高（Linux基金会项目） |

> 来源：CHAOSS Project — Community Health Analytics Open Source Software (Linux Foundation)

### CII Best Practices Badge

| 维度 | 说明 |
|------|------|
| **认证等级** | 基础级 / 银级 / 金级（三级认证） |
| **覆盖范围** | 基础、变更管理、报告、质量、安全 |
| **适用场景** | 开源项目质量证明 |
| **引用方式** | 申请CII徽章作为质量背书 |
| **可信度等级** | 高（Linux基金会） |

> 来源：OpenSSF CII Best Practices Badge Program

### OpenSSF Scorecard

| 维度 | 说明 |
|------|------|
| **功能** | 自动化开源项目安全评分 |
| **适用场景** | 安全合规评审 |
| **引用方式** | 运行Scorecard获取评分并引用 |
| **可信度等级** | 高 |

> 来源：OpenSSF Scorecard — Open Source Security Foundation

---

## 四、引用指南

### 如何选择引用

| 评审类型 | 优先顺序 |
|----------|----------|
| 技术评审 | ISO 25010 > NIST CSF > CWE/SANS Top 25 |
| 商业评审 | YC > a16z > Lean Canvas |
| 开源评审 | CHAOSS > CII Best Practices > OpenSSF Scorecard |

### 引用规范

1. **必须标注来源和版本** — 每个引用需注明出处框架名称及版本/发布日期
2. **不可断章取义** — 必须完整引用框架原意，不得扭曲或片面截取
3. **必须说明与项目的关联** — 引用后需解释该框架维度如何映射到当前项目
4. **不可虚构引用结果** — 所有评分、评级、认证结果必须真实可验证
