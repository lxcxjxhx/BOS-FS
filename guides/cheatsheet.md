# BOS-FS 快速参考卡

## Skill 速查表

| # | Skill | 文件 | 用途 | 输入 | 输出 | 触发场景 |
|---|-------|------|------|------|------|----------|
| 1 | Goal Refiner | skills/01_goal_refiner.md | 提炼项目意图 | 项目描述 | {persona,problem,solution,outcome} | 描述项目时 |
| 2 | Reviewer Simulator | skills/02_reviewer_simulator.md | 模拟四类评审 | 项目信息 | 通过概率/拒绝理由/建议 | 预审时 |
| 3 | README Refactor | skills/03_readme_refactor.md | 重构项目文档 | 原始 README | What/Why/How/Result/Next | 优化文档时 |
| 4 | Outcome Mapper | skills/04_outcome_mapper.md | Feature→Value | 功能描述 | Capability→Outcome | 价值转换时 |
| 5 | Submission Builder | skills/05_submission_builder.md | 构建交付包 | 项目信息 | submission_bundle/ | 准备提交时 |
| 6 | Reject Analyzer | skills/06_reject_analyzer.md | 分析被拒原因 | 拒绝说明 | 真实问题/修复建议 | 项目被拒时 |
| 7 | Pipeline | skills/pipeline.md | 完整流水线编排 | 项目描述 | 端到端优化结果 | 完整优化时 |

## Pipeline 步骤速查

```
Repo/描述 → Understand → Map → Refactor → Review → Build → Submit
              ↓              ↓        ↓         ↓        ↓
          Goal Refiner   Outcome   README    Reviewer  Submission
                          Mapper   Refactor  Simulator Builder
                                        ↓
                                Reject Analyzer (按需)
```

| 快捷命令 | 执行步骤 |
|----------|----------|
| 完整优化 | Step 1-5 |
| 快速预览 | Step 1-2 |
| 仅文档 | Step 3 |
| 仅评审 | Step 4 |
| 拒绝分析 | Step 6 |

## 输出格式速查

### Goal Refiner
```json
{"persona":"string","problem":"string","solution":"string","outcome":"string"}
```

### Reviewer Simulator
```json
{"review_type":"type","pass_probability":0-100,"scores":{"维度":0-10,"trust":0-10},"weighted_score":0.0-10.0,"rejection_reasons":["string"],"suggestions":["string"]}
```

### Outcome Mapper
```json
{"feature":"string","capability":"string","outcome":"string"}
```

### Submission Builder
```json
{"bundle_path":"submission_bundle/","components":["README.md","demo_guide.md","introduction.md","screenshots_guide.md","FAQ.md","risk_disclosure.md","trust_statement.md","bundle_meta.json"],"status":"complete"}
```

## 评分标准速查

### Pipeline 综合评分
| 阶段 | 权重 | 评分标准 |
|------|------|----------|
| Goal Refinement | 14% | persona/problem/solution/outcome 完整度 |
| Outcome Mapping | 14% | Feature→Capability→Outcome 转换质量 |
| README Refactor | 24% | 五段式结构完整度、价值公式应用 |
| Review Simulation | 24% | 四类评审平均通过率 |
| Submission Build | 19% | 提交包组件完整性、一致性 |
| Trust 信任背书 | 5% | 权威引用/行业对标/透明度 |

### 等级判定
| 等级 | 分数 | 含义 |
|------|------|------|
| S | ≥ 9.0 | 可直接提交 |
| A | 8.0-8.9 | 建议微调 |
| B | 6.0-7.9 | 需要改进 |
| C | 4.0-5.9 | 大幅修改 |
| D | < 4.0 | 重新规划 |

### 评审评分
| 维度 | 权重 | 评审要点 |
|------|------|----------|
| 技术深度 | 0-10 | 架构精良，有深度论证 |
| 创新性 | 0-10 | 行业首创，有专利/论文 |
| 实用价值 | 0-10 | 痛点明确，已验证 |
| 文档质量 | 0-10 | 文档完备，支撑二次开发 |
| 信任度 | 0-10 | 权威引用充分，差异化有据 |

通过阈值: ≥ 30/50

## 信任背书引用速查

### 技术权威引用
| 引用 | 适用场景 | 可信度 |
|------|----------|--------|
| OWASP Top 10 | 安全设计评审 | 高 |
| 12-Factor App | 云原生架构评审 | 高 |
| Clean Architecture | 架构分层评审 | 高 |
| SOLID 原则 | 代码质量评审 | 高 |
| TDD | 测试策略评审 | 高 |

### 行业对标
| 引用 | 适用场景 | 可信度 |
|------|----------|--------|
| Gartner Hype Cycle | 市场定位 | 高 |
| Forrester Wave | 竞品分析 | 高 |
| CNCF Landscape | 技术分类 | 高 |

### 方法论背书
| 引用 | 适用场景 | 可信度 |
|------|----------|--------|
| DORA 指标 | 交付效能评估 | 高 |
| SPACE 框架 | 开发者生产力 | 高 |
| DevOps 成熟度模型 | 工程能力评估 | 高 |

### 权威评审框架
| 引用 | 适用场景 | 可信度 |
|------|----------|--------|
| ISO/IEC 25010 | 软件质量评审 | 高（国际标准） |
| NIST CSF | 安全框架评审 | 高（政府标准） |
| Y Combinator | 投资评审 | 高（顶级孵化器） |
| a16z | 投资评审 | 高（顶级风投） |
| CHAOSS | 开源社区评审 | 高（Linux基金会） |
| CII Best Practices | 开源质量评审 | 高（Linux基金会） |

> 所有引用必须真实可查证，不可虚构。详见 [knowledge/governance/trust_framework.md](../knowledge/governance/trust_framework.md)。
