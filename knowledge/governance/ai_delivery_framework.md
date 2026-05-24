# AI 交付框架（AI Delivery Framework）

> 来源: AI Engineering (Chip Huyen)  
> 映射: BOS-FS 五层架构 → Intent Layer + Runtime Layer + Governance Layer  
> 用途: 指导用户在 AI 辅助的提交生成工作流中进行 Prompt 工程、上下文管理、质量评估、Agent 编排与观测监控。

---

## 一、Prompt 工程模式

### 1.1 Prompt 设计原则

Huyen 的核心观点: Prompt 工程不是"玄学"，而是可系统化设计的工程实践。

| 原则 | 内容 | BOS-FS 中的应用 |
|------|------|----------------|
| **明确性** | 清晰指定输入/输出格式 | 所有 Skill 定义 `Output Schema` |
| **上下文** | 提供足够的上下文信息 | `base_context.md` 作为基础上下文 |
| **约束** | 明确禁止的行为和格式要求 | Input Validation / Error Handling |
| **示例** | 提供 Few-shot 示例 | 每个 Skill 包含 Examples |
| **迭代** | 持续优化 Prompt | 基于评审反馈调整知识文件 |

### 1.2 BOS-FS 中的 Prompt 模式

#### 模式 1: 结构化提取（Structured Extraction）

```
Input: 自然语言项目描述
Prompt: "从以下描述中提取 {persona, problem, solution, outcome} 四个字段..."
Output: 严格格式的 JSON

应用: Goal Refiner (`skills/goal-refiner/SKILL.md`)
```

#### 模式 2: 转换映射（Transformation Mapping）

```
Input: 技术特性列表
Prompt: "将以下技术特性转换为 Feature → Capability → Outcome 格式..."
Output: 标准化的价值映射 JSON

应用: Outcome Mapper (`skills/outcome-mapper/SKILL.md`)
```

#### 模式 3: 模板填充（Template Filling）

```
Input: 结构化数据 + 模板
Prompt: "根据以下数据和模板生成完整的 README..."
Output: 符合五段式结构的 Markdown

应用: Readme Refactor (`skills/readme-refactor/SKILL.md`)
```

#### 模式 4: 评审模拟（Review Simulation）

```
Input: 提交包内容 + 评审规则
Prompt: "作为[技术/投资/产品/开源]评审人，根据以下规则评估..."
Output: 结构化评审报告

应用: Reviewer Simulator (`skills/reviewer-simulator/SKILL.md`)
```

#### 模式 5: 拒绝分析（Rejection Analysis）

```
Input: 评审拒绝反馈
Prompt: "分析以下评审反馈，识别核心问题并给出改进建议..."
Output: 分类的改进清单

应用: Reject Analyzer (`skills/reject-analyzer/SKILL.md`)
```

### 1.3 Prompt 模板库

#### 通用提取模板

```markdown
# [角色定义]
你是一个[角色名]，擅长[核心能力]。

# [任务]
从以下输入中提取/转换/生成[目标]。

# [输入]
{{input}}

# [规则]
1. [规则1]
2. [规则2]
3. [规则3]

# [输出格式]
```json
{{schema}}
```

# [示例]
Input: {{example_input}}
Output: {{example_output}}
```

#### BOS-FS Skill 模板映射

| Skill | Prompt 模式 | 核心模板 |
|-------|------------|---------|
| Goal Refiner | 结构化提取 | `{"persona":"...","problem":"...","solution":"...","outcome":"..."}` |
| Outcome Mapper | 转换映射 | `{"feature":"...","capability":"...","outcome":"..."}` |
| Readme Refactor | 模板填充 | What/Why/How/Result/Next 五段式 |
| Submission Builder | 模板填充 | 8组件提交包模板 |
| Reviewer Simulator | 评审模拟 | 四类评审规则 + 加权评分 |
| Reject Analyzer | 拒绝分析 | 分类码 + 改进建议 |

---

## 二、上下文管理

### 2.1 上下文层次

BOS-FS 的上下文管理采用分层结构:

```
┌─────────────────────────────────────────┐
│  L0: 系统级上下文                         │
│  • BOS-FS 架构定义                       │
│  • 输出规范 (base_context.md)            │
├─────────────────────────────────────────┤
│  L1: Skill 级上下文                      │
│  • Skill 角色定义                        │
│  • 输入/输出格式                         │
│  • 规则约束                              │
├─────────────────────────────────────────┤
│  L2: 领域级上下文                        │
│  • 知识文件 (knowledge/)                 │
│  • 评审规则 (review_rules/)              │
│  • 模板库 (templates/)                   │
├─────────────────────────────────────────┤
│  L3: 运行级上下文                        │
│  • 项目描述 (当前输入)                   │
│  • Pipeline 中间状态                     │
│  • 缓存结果                              │
└─────────────────────────────────────────┘
```

### 2.2 上下文加载策略

| 策略 | 触发条件 | 加载内容 | Token 预算 |
|------|---------|---------|-----------|
| **全量加载** | 首次运行 | L0 + L1 + 相关 L2 | ~8K tokens |
| **按需加载** | Stage 切换 | 当前 Stage 的 L2 知识 | ~2-4K tokens |
| **缓存加载** | 命中缓存 | 仅 L3 上下文 | ~1K tokens |
| **最小加载** | 简单查询 | 仅 L0 核心规则 | ~500 tokens |

### 2.3 上下文优化技术

| 技术 | 描述 | BOS-FS 中的应用 |
|------|------|----------------|
| **知识分层** | 将知识按层级组织，按需加载 | knowledge/ 目录的五层结构 |
| **规则精炼** | 将冗长规则压缩为要点 | 评审规则的精简版 |
| **示例精选** | 只保留最有代表性的示例 | 每个 Skill 3-4 个核心示例 |
| **上下文窗口管理** | 控制输入长度在窗口内 | 长输入分段处理 |
| **引用替代全文** | 用引用替代嵌入完整内容 | 交叉引用而非全文复制 |

### 2.4 上下文一致性保障

| 风险 | 症状 | 预防措施 |
|------|------|---------|
| **上下文污染** | 上一次运行的状态影响当前运行 | PipelineContext 每次运行创建新的实例 |
| **上下文丢失** | 关键信息在传递中丢失 | PipelineContext.shared_data 只追加 |
| **上下文冲突** | 不同知识文件中的规则矛盾 | 定期一致性检查 |
| **上下文膨胀** | 上下文过大导致 Token 浪费 | 按需加载策略 |

---

## 三、AI 生成质量评估

### 3.1 评估维度

Huyen 提出的 AI 输出评估框架，映射到 BOS-FS:

| 维度 | 定义 | BOS-FS 评估方式 |
|------|------|----------------|
| **正确性** | 输出是否准确反映了输入 | Input Validation + Schema 校验 |
| **完整性** | 是否覆盖了所有要求的内容 | 检查清单 (Checklist) |
| **一致性** | 输出各部分是否一致 | 一致性报告 (consistency_report.md) |
| **可读性** | 人类是否容易理解 | README 评分 |
| **可信度** | 输出是否可被信任 | Trust Metrics |

### 3.2 自动化评估流程

```
AI 生成输出
    │
    ▼
┌───────────────────────┐
│  Step 1: 格式验证      │
│  JSON.parse() / Schema │
│  ✓ / ✗                 │
└───────────┬───────────┘
            │ ✓
            ▼
┌───────────────────────┐
│  Step 2: 内容检查      │
│  必填字段/非空/格式    │
│  ✓ / ✗                 │
└───────────┬───────────┘
            │ ✓
            ▼
┌───────────────────────┐
│  Step 3: 语义验证      │
│  逻辑一致性/完整性     │
│  ✓ / ✗                 │
└───────────┬───────────┘
            │ ✓
            ▼
┌───────────────────────┐
│  Step 4: 评审模拟      │
│  四类评审打分          │
│  Score: X.X/10         │
└───────────────────────┘
```

### 3.3 评估指标矩阵

| 评估类型 | 指标 | 采集方式 | 阈值 |
|---------|------|---------|------|
| 格式验证 | Schema 验证通过率 | JSON Schema 校验 | 100% |
| 内容检查 | 必填字段覆盖率 | 字段存在性检查 | 100% |
| 语义验证 | 逻辑一致性得分 | 规则引擎检查 | ≥ 8.0 |
| 评审模拟 | 综合评审通过率 | Reviewer Simulator | ≥ 70% |
| 用户反馈 | 实际评审通过率 | 用户报告 | 趋势分析 |

### 3.4 幻觉检测与防护

| 幻觉类型 | 症状 | 检测方法 | 防护措施 |
|---------|------|---------|---------|
| **事实幻觉** | 编造不存在的标准/数据 | 引用验证 | 知识文件中预定义引用清单 |
| **逻辑幻觉** | 推理过程不符合逻辑 | 规则检查 | 明确的转换规则和边界条件 |
| **格式幻觉** | 输出格式不符合要求 | Schema 校验 | 严格的 Output Schema |
| **范围幻觉** | 超出任务范围的内容 | 关键词检查 | 明确的 Boundary 定义 |

**BOS-FS 幻觉防护清单**:

| 防护点 | 措施 | 对应文件 |
|--------|------|---------|
| 数字不可虚构 | "数值/指标必须可验证，不可虚构" | `base_context.md` |
| 推断必须标注 | 推断值标注"（推断）" | `skills/goal-refiner/SKILL.md` |
| 输出格式约束 | 单行纯JSON，无额外文本 | 所有 Skill 的 Output Schema |
| 引用规范 | 必须标注来源和版本 | `trust_framework.md` |
| 风险不可省略 | 风险说明不可省略或淡化 | `trust_framework.md` |

---

## 四、Agent 编排模式

### 4.1 BOS-FS 的 Agent 架构

BOS-FS 本身不是 Agent 系统，但可以被嵌入到 Agent 工作流中:

```
┌─────────────────────────────────────────────────────┐
│                  AI Agent (外部)                      │
│  (Cursor / Trae / Claude Code / OpenHands)           │
│                                                      │
│  ┌───────────────────────────────────────────────┐   │
│  │            BOS-FS Skill Runtime                │   │
│  │                                                │   │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐    │   │
│  │  │Goal │ │Map  │ │Re-  │ │Build│ │Re-  │    │   │
│  │  │Ref. │ │per  │ │fact.│ │er   │ │view │    │   │
│  │  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘    │   │
│  │     │        │        │        │        │     │   │
│  │     └────────┴────────┴────────┴────────┘     │   │
│  │                    │                          │   │
│  │              PipelineContext                  │   │
│  └───────────────────────────────────────────────┘   │
│                                                      │
│  外部 Agent 通过以下方式调用 BOS-FS:                  │
│  1. 读取 Skill 定义 → 理解每个 Stage 做什么          │
│  2. 执行 Pipeline → 生成提交包                       │
│  3. 读取评审结果 → 指导后续修改                       │
└─────────────────────────────────────────────────────┘
```

### 4.2 Agent 协作模式

| 模式 | 描述 | 适用场景 |
|------|------|---------|
| **单 Agent + BOS-FS** | 一个 Agent 使用 BOS-FS Pipeline 完成端到端交付 | 个人开发者 |
| **多 Agent 协作** | 不同 Agent 负责不同 Stage，BOS-FS 协调 | 复杂项目 |
| **Agent 链** | 前一个 Agent 的输出作为后一个的输入 | 流水线式工作流 |
| **Human-in-the-Loop** | 人工在关键节点审核 AI 输出 | 高质量要求场景 |

### 4.3 BOS-FS 作为 Agent 工具

BOS-FS 可以被注册为 Agent 的工具:

```json
{
  "name": "bos_fs_pipeline",
  "description": "执行 BOS-FS 提交工程 Pipeline，将项目描述转换为完整提交包",
  "input_schema": {
    "type": "object",
    "properties": {
      "project_description": { "type": "string" },
      "stages": { "type": "array", "items": { "type": "string" } },
      "output_dir": { "type": "string" }
    },
    "required": ["project_description"]
  },
  "output_schema": {
    "type": "object",
    "properties": {
      "status": { "type": "string", "enum": ["complete", "partial", "error"] },
      "bundle_path": { "type": "string" },
      "review_scores": { "type": "object" }
    }
  }
}
```

### 4.4 Agent 编排最佳实践

| 实践 | 描述 | BOS-FS 支持 |
|------|------|------------|
| **明确角色边界** | 每个 Agent 有清晰的职责 | Skill 定义明确 Role |
| **标准通信格式** | Agent 间通过 JSON 交换数据 | PipelineContext.shared_data |
| **错误处理** | Agent 失败时有恢复机制 | Stage 重试 + 错误隔离 |
| **可追溯性** | 每一步的执行可追溯 | Pipeline 日志 + 状态持久化 |
| **人工审核点** | 关键节点设置人工审核 | Pipeline Waiting 状态 |

---

## 五、观测与监控

### 5.1 观测层次

```
┌─────────────────────────────────────────┐
│  L1: 业务观测                            │
│  • Pipeline 运行成功率                    │
│  • 评审通过率趋势                        │
│  • 交付效能指数 (DEI)                    │
├─────────────────────────────────────────┤
│  L2: 系统观测                            │
│  • Pipeline Stage 耗时                   │
│  • 缓存命中率                            │
│  • 错误类型分布                          │
├─────────────────────────────────────────┤
│  L3: AI 观测                             │
│  • Token 消耗量                          │
│  • Prompt 质量指标                       │
│  • 生成输出质量评分                      │
├─────────────────────────────────────────┤
│  L4: 基础设施观测                        │
│  • CPU/内存使用                          │
│  • 磁盘 I/O                             │
│  • 网络延迟                              │
└─────────────────────────────────────────┘
```

### 5.2 AI 特定观测指标

| 指标 | 定义 | 采集方式 | 预警阈值 |
|------|------|---------|---------|
| **Token 消耗** | 每次 Pipeline 运行的总 Token 数 | AI 提供商 API | 异常突增 > 50% |
| **Prompt 效率** | 输出质量 / Token 消耗 | 评分 / Token 数 | 持续下降 |
| **幻觉率** | 输出中被标记为幻觉的比例 | 人工审计/规则检测 | > 5% |
| **格式合规率** | 输出符合 Schema 的比例 | Schema 校验 | < 95% |
| **重试率** | 需要重试的 Pipeline 运行比例 | Pipeline 日志 | > 10% |

### 5.3 监控仪表盘模板

```
┌──────────────────────────────────────────────────────────┐
│  BOS-FS AI 交付监控仪表盘 — [日期]                        │
├──────────────────────────────────────────────────────────┤
│  Pipeline 状态                                            │
│  ✅ 完成: X 次    ⏳ 进行中: X 次    ❌ 失败: X 次         │
│  成功率: XX%                                             │
├──────────────────────────────────────────────────────────┤
│  AI 生成质量                                              │
│  • 格式合规率: XX%      (阈值: ≥95%)                      │
│  • 幻觉率: X.X%         (阈值: ≤5%)                       │
│  • 平均评审得分: X.X/10  (阈值: ≥7.0)                     │
│  • Token 消耗: X.XK/run  (趋势: ↑/↓/→)                    │
├──────────────────────────────────────────────────────────┤
│  交付效能                                                 │
│  • Flow Velocity: X 次/周   (等级: Elite/High/Medium/Low) │
│  • Flow Efficiency: XX%                                   │
│  • Flow Time P50: Xh                                      │
│  • DEI 综合指数: X.X                                      │
├──────────────────────────────────────────────────────────┤
│  告警                                                     │
│  [无告警 / 告警列表]                                      │
└──────────────────────────────────────────────────────────┘
```

### 5.4 异常检测规则

| 异常类型 | 触发条件 | 响应动作 |
|---------|---------|---------|
| **成功率下降** | 连续 3 次运行失败 | 检查输入格式，通知用户 |
| **幻觉率上升** | 单周幻觉率 > 10% | 检查知识文件一致性 |
| **Token 突增** | 单次消耗 > 3 倍均值 | 检查输入长度，可能需分段 |
| **评审分数异常** | 某类评审分数骤降 > 20% | 检查评审规则是否变更 |
| **Flow Time 延长** | P50 超过阈值 2 倍 | 检查 Pipeline 瓶颈 Stage |

---

## 六、AI 交付链的持续改进

### 6.1 改进循环

```
运行 Pipeline
    │
    ▼
收集数据 (指标/日志/评审结果)
    │
    ▼
分析问题 (瓶颈/幻觉/低质量输出)
    │
    ▼
制定改进方案
    ├── 优化 Prompt (修改 Skill 定义)
    ├── 更新知识 (完善 knowledge/ 文件)
    ├── 调整规则 (修改 review_rules/)
    └── 增强模板 (更新 templates/)
    │
    ▼
验证改进 (对比前后指标)
    │
    ▼
固化改进 (更新 Skill/知识文件)
    │
    ▼
    └──▶ 循环
```

### 6.2 改进度量

| 改进类型 | 度量方式 | 目标 |
|---------|---------|------|
| Prompt 优化 | 输出质量评分提升 | +10% |
| 知识更新 | 幻觉率下降 | -20% |
| 规则调整 | 评审通过率提升 | +15% |
| 模板增强 | 一致性得分提升 | +10% |

### 6.3 版本管理

| 组件 | 版本策略 | 变更记录 |
|------|---------|---------|
| Skill 定义 | 语义化版本 (MAJOR.MINOR.PATCH) | `skills/manifest.json` |
| 知识文件 | 按变更类型标记 | 文件头部注释 |
| 评审规则 | 按评审类型独立版本 | `review_rules/` 目录 |
| Pipeline | 与 BOS-FS 版本同步 | `pipeline_result.json` |

---

## 七、与其他知识文件的关联

| 关联文件 | 关联点 | 使用场景 |
|---------|--------|---------|
| [discovery_framework.md](../intent/discovery_framework.md) | AI 辅助发现 | AI 如何辅助用户访谈和假设验证 |
| [product_value_framework.md](../intent/product_value_framework.md) | AI 价值转换 | Outcome Mapper 的 Prompt 设计 |
| [architecture_patterns.md](../runtime/architecture_patterns.md) | AI 运行时架构 | Pipeline 如何支撑 AI 驱动的 Stage |
| [flow_metrics.md](../adoption/flow_metrics.md) | AI 交付效能度量 | AI 生成效率纳入 Flow Metrics |
| [metrics_framework.md](../governance/metrics_framework.md) | 综合效能度量 | DEI 中纳入 AI 质量指标 |
| [trust_framework.md](../governance/trust_framework.md) | AI 生成内容的可信度 | 如何验证 AI 引用的权威性 |
| [base_context.md](../base_context.md) | 输出规范 | AI 输出格式的一致性保障 |

---

> 完整框架参见: Chip Huyen, *AI Engineering: Building Applications with Foundation Models* (2024)  
> BOS-FS 实现: Skill 系统 + Pipeline Runtime + Knowledge Layer 共同构成 AI 辅助交付链

---

## 附录 A: 大模型选择框架

### A.1 模型选择维度

选择大模型时需在四个维度之间权衡:

| 维度 | 关注点 | 测量方式 | BOS-FS 权重 |
|------|--------|---------|------------|
| **能力** | 推理/编码/理解/生成质量 | 基准测试 + 任务特定评估 | 35% |
| **成本** | 每千 Token 价格 / 上下文窗口价格 | API 定价 × 预估用量 | 25% |
| **延迟** | 首 Token 时间 / 端到端时间 | API 延迟测量 | 20% |
| **隐私** | 数据是否离开本地 / 训练风险 | 部署模式 + 合规认证 | 20% |

### A.2 模型能力对比矩阵

| 能力维度 | 评估方法 | BOS-FS 相关场景 |
|---------|---------|----------------|
| **指令跟随** | 是否严格按格式输出 | 所有 Skill 的 JSON 输出 |
| **长上下文理解** | 能否处理 10K+ token 输入 | 知识文件加载 + 项目描述 |
| **代码理解** | 能否理解代码结构和逻辑 | Pipeline 引擎分析 |
| **结构化提取** | 从非结构化文本提取 JSON | Goal Refiner, Outcome Mapper |
| **推理能力** | 复杂逻辑推理 | Reviewer Simulator 综合评审 |
| **多语言** | 中英文混合处理 | 知识文件（中文）+ 代码（英文） |
| **一致性** | 相同输入产生相同输出 | 缓存命中验证 |

### A.3 模型选择决策树

```
是否需要数据不出本地?
  ├─ 是 → 本地部署模型 (Ollama/vLLM)
  │        └─ 选择: Llama 3 / Qwen / DeepSeek
  │           └─ 评估: 本地推理能力 vs 硬件限制
  └─ 否 → 是否需要最低成本?
           ├─ 是 → 选择: Claude Haiku / GPT-4o-mini
           │        └─ 适合: 简单格式化任务
           └─ 否 → 是否需要最强推理能力?
                    ├─ 是 → 选择: Claude Sonnet-4 / GPT-4o
                    │        └─ 适合: 评审模拟 / 拒绝分析
                    └─ 否 → 选择: Claude Haiku / Gemini Flash
                             └─ 适合: 性价比平衡
```

### A.4 BOS-FS 模型配置建议

| Skill | 推荐模型 | 理由 | 成本/次 |
|-------|---------|------|---------|
| Goal Refiner | Claude Haiku | 简单结构化提取，速度快成本低 | ~$0.01 |
| Outcome Mapper | Claude Haiku | 固定格式的转换映射 | ~$0.01 |
| Readme Refactor | Claude Sonnet | 需要理解和生成自然语言 | ~$0.05 |
| Reviewer Simulator | Claude Sonnet-4 | 复杂推理和多规则综合评估 | ~$0.10 |
| Reject Analyzer | Claude Sonnet | 需要理解拒绝原因并给出建议 | ~$0.05 |
| Book Ingestor | Claude Sonnet | 长上下文理解 + 知识提取 | ~$0.08 |

**总成本估算**: 完整 Pipeline 运行 ~$0.30/次

### A.5 模型降级策略

```
主模型 (Sonnet) 不可用时:
  ├─ 降级 1: 同厂商次级模型 (Haiku)
  │        └─ 能力下降 ~20%，成本下降 ~70%
  ├─ 降级 2: 跨厂商同级模型 (GPT-4o)
  │        └─ 需要调整 Prompt 格式
  └─ 降级 3: 本地模型 (Llama 3 70B)
           └─ 能力下降 ~30%，延迟增加，隐私最优
```

---

## 附录 B: 提示工程模式库

### B.1 高级模式完整定义

#### Chain-of-Thought (CoT) — 链式思考

```
模式: 要求模型逐步推理后再给出结论

Prompt 模板:
  "请按照以下步骤分析问题:
   1. 理解输入的核心要素
   2. 分析每个要素之间的关系
   3. 评估可能的解释/方案
   4. 得出最终结论
   
   输入: {{input}}
   输出: 最终结论（JSON 格式）"

适用场景: Reviewer Simulator 的综合评审
效果: 复杂推理任务准确率提升 20-40%
注意: CoT 会增加 Token 消耗（推理过程也是输出）
```

#### ReAct — 推理+行动

```
模式: 模型交替进行推理（Thought）和行动（Action）

工作流:
  Thought: 我需要先了解项目的目标用户
  Action:  从输入中提取 persona 信息
  Observation: persona = "独立开发者"
  Thought: 独立开发者最关注上手难度和文档质量
  Action:  检查 README 的快速开始部分
  Observation: 快速开始部分存在但不够详细
  Thought: 这是评审中的文档质量扣分点
  ...

适用场景: 知识摄取引擎（需要多步骤信息检索）
实现: BOS-FS 可通过 Stage 链模拟 ReAct 模式
```

#### Few-Shot — 少样本学习

```
模式: 在 Prompt 中提供 2-5 个输入输出示例

BOS-FS 中的 Few-Shot 示例:

Goal Refiner Few-Shot:
  示例 1:
    Input: "这是一个帮助用户管理待办事项的工具"
    Output: {"persona":"忙碌的专业人士","problem":"任务管理混乱","solution":"智能待办管理工具","outcome":"每天节省30分钟任务规划时间"}
  
  示例 2:
    Input: "这个 API 网关可以自动限流和认证"
    Output: {"persona":"后端架构师","problem":"API 安全和性能难以保障","solution":"智能 API 网关","outcome":"减少 80% 的安全事件和 50% 的 API 延迟"}

关键原则:
  1. 示例覆盖边界情况（简单输入 + 复杂输入）
  2. 示例格式与期望输出完全一致
  3. 示例数量 2-5 个（太多浪费 Token，太少效果不佳）
  4. 定期更新示例以匹配最新模式
```

#### Self-Consistency — 自洽性验证

```
模式: 同一问题多次采样，选择最一致的答案

实现步骤:
  1. 用相同 Prompt 运行 N 次（N=3-5）
  2. 收集 N 个输出
  3. 投票/聚类选择最一致的输出
  4. 如果不一致度 > 阈值，标记为"不确定"

BOS-FS 应用:
  - Reviewer Simulator: 对关键评审项运行 3 次，取一致结论
  - Reject Analyzer: 多次分析确保改进建议的一致性
  - 成本增加: N 倍 Token 消耗
  - 效果: 关键决策准确率提升 15-25%
```

### B.2 BOS-FS 提示工程清单

| 检查项 | 是/否 | 说明 |
|--------|-------|------|
| Prompt 是否有明确的角色定义？ | ✓ | "你是一个资深技术评审专家..." |
| 输入输出格式是否明确？ | ✓ | JSON Schema 定义 |
| 是否提供了 Few-Shot 示例？ | ✓ | 每个 Skill 包含 2-3 个示例 |
| 是否使用了 CoT 处理复杂推理？ | ✓ | Reviewer Simulator 使用 |
| 是否有边界条件定义？ | ✓ | "如果输入缺少 X 字段，则..." |
| 是否限制了输出长度？ | ✓ | "输出不超过 500 字" |
| 是否防止了幻觉？ | ✓ | "不要编造数据，缺失则标注" |
| 是否定义了失败处理？ | ✓ | "如果无法确定，返回错误码" |

---

## 附录 C: 上下文工程（Context Engineering）

### C.1 RAG 架构在知识摄取中的应用

```
┌─────────────────────────────────────────────────────┐
│              BOS-FS RAG 知识引擎                      │
│                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────────┐   │
│  │ 书籍/文档 │───▶│ 分块处理  │───▶│ 向量嵌入     │   │
│  │ 源文件    │    │ (Chunking)│    │ (Embedding)  │   │
│  └──────────┘    └──────────┘    └──────┬───────┘   │
│                                         │            │
│  ┌──────────┐    ┌──────────┐    ┌──────▼───────┐   │
│  │ 增强输出 │◀───│ 上下文组装 │◀───│ 向量检索     │   │
│  │ (Prompt) │    │ (Context) │    │ (Retrieval)  │   │
│  └──────────┘    └──────────┘    └──────┬───────┘   │
│                                         │            │
│                                  ┌──────▼───────┐   │
│                                  │ 向量数据库    │   │
│                                  │ (Chroma/FAISS)│   │
│                                  └──────────────┘   │
└─────────────────────────────────────────────────────┘
```

### C.2 分块策略（Chunking Strategies）

| 策略 | 适用场景 | 块大小 | 重叠 | 效果 |
|------|---------|--------|------|------|
| **固定大小** | 通用场景 | 500-1000 tokens | 10-15% | 简单高效 |
| **语义分块** | 技术文档 | 按段落/章节 | 5% | 保持上下文完整 |
| **结构分块** | 代码+文档 | 按代码块/函数 | 0% | 保留代码结构 |
| **递归分块** | 混合内容 | 从大到小递归 | 10% | 最优但复杂 |

**BOS-FS 推荐**: 知识文件使用语义分块（按章节），代码使用结构分块（按函数/类）。

### C.3 检索优化技术

| 技术 | 描述 | 效果 | 复杂度 |
|------|------|------|--------|
| **混合检索** | 向量相似度 + BM25 关键词 | 召回率 +15-25% | 中 |
| **重排序 (Rerank)** | 检索后用交叉编码器排序 | 准确率 +10-20% | 中 |
| **查询扩展** | 用户查询 → 多查询检索 | 召回率 +10% | 低 |
| **上下文压缩** | 检索后提取相关段落 | Token 消耗 -30% | 中 |
| **元数据过滤** | 按来源/类型/时间过滤 | 精度 +20% | 低 |

### C.4 BOS-FS 知识摄取引擎优化路径

```
Phase 1 (当前): 静态 Markdown 文件
  └─ 优点: 简单、人类可读
  └─ 局限: 无法按语义检索，上下文加载全量

Phase 2: 向量化知识检索
  └─ 知识文件分块 + 向量化
  └─ 按需检索相关段落
  └─ Token 消耗降低 40-60%

Phase 3: 混合 RAG 引擎
  └─ 向量检索 + 关键词检索 + 元数据过滤
  └─ 知识摄取引擎自动选择最佳上下文
  └─ 检索准确率 ≥ 85%

Phase 4: 自适应上下文
  └─ 根据 Stage 类型自动调整上下文策略
  └─ 根据历史表现优化检索参数
  └─ 实现 Self-RAG 模式
```

---

## 附录 D: AI 评估框架

### D.1 评估维度全景

| 评估维度 | 评估方法 | 工具 | BOS-FS 应用 |
|---------|---------|------|------------|
| **事实准确性** | 参考答案对比 / 人工审核 | LLM-as-a-Judge | Goal Refiner 输出验证 |
| **格式合规性** | Schema 校验 | JSON Schema | 所有 Skill 输出 |
| **一致性** | 多次运行对比 | Self-Consistency | Reviewer Simulator |
| **幻觉检测** | 引用验证 / 事实验证 | 自定义规则 | 知识摄取引擎 |
| **安全性** | 有害内容检测 | 安全分类器 | 所有用户输入 |
| **成本效率** | Token 消耗 / 输出质量比 | 自定义度量 | Pipeline 优化 |

### D.2 HELM 框架映射

HELM (Holistic Evaluation of Language Models) 定义了多维度评估:

| HELM 场景 | 定义 | BOS-FS 对应 |
|-----------|------|------------|
| 问答 | 给定上下文回答问题 | 知识摄取引擎的问答能力 |
| 摘要 | 生成长文本摘要 | 书籍知识提取 |
| 信息抽取 | 从文本提取结构化信息 | Goal Refiner, Outcome Mapper |
| 文本创作 | 生成连贯的长文本 | Readme Refactor, Submission Builder |
| 对话 | 多轮对话能力 | 未来: 交互式 Goal Refining |

### D.3 LLM-as-a-Judge 实现

```python
# LLM-as-a-Judge 模板用于 BOS-FS 评审

JUDGE_PROMPT = """
你是一个严格的评估专家。请评估以下 AI 生成的输出质量。

评估标准:
1. 准确性: 输出是否准确反映了输入信息？(1-5)
2. 完整性: 是否覆盖了所有要求的内容？(1-5)
3. 格式合规: 是否符合指定的输出格式？(1-5)
4. 逻辑一致: 输出各部分是否一致？(1-5)
5. 实用性: 输出对目标用户是否有用？(1-5)

输入: {input}
输出: {output}

请以 JSON 格式返回评分:
{{"accuracy": X, "completeness": X, "format": X, "consistency": X, "usefulness": X, "overall": X, "feedback": "..."}}
"""
```

### D.4 BOS-FS 评估仪表板

```
┌────────────────────────────────────────────────────────────┐
│  BOS-FS AI 质量评估仪表板                                    │
├────────────────────────────────────────────────────────────┤
│  技能级评估                                                  │
│  ┌────────────┬──────┬──────┬──────┬──────┬──────┬─────┐   │
│  │ Skill      │ 准确 │ 完整 │ 格式 │ 一致 │ 实用 │ 综合 │   │
│  ├────────────┼──────┼──────┼──────┼──────┼──────┼─────┤   │
│  │ Goal Ref.  │ 4.2  │ 4.5  │ 4.8  │ 4.0  │ 4.3  │ 4.4 │   │
│  │ Outcome M. │ 4.0  │ 4.3  │ 4.9  │ 3.8  │ 4.1  │ 4.2 │   │
│  │ Readme Ref.│ 4.1  │ 4.0  │ 4.5  │ 4.2  │ 4.4  │ 4.2 │   │
│  │ Review Sim.│ 3.8  │ 3.5  │ 4.6  │ 3.2  │ 3.9  │ 3.8 │   │
│  │ Reject An. │ 3.9  │ 3.7  │ 4.5  │ 3.5  │ 4.0  │ 3.9 │   │
│  └────────────┴──────┴──────┴──────┴──────┴──────┴─────┘   │
├────────────────────────────────────────────────────────────┤
│  幻觉检测                                                    │
│  事实幻觉: 2%  (阈值 ≤ 5%)  ✅                              │
│  逻辑幻觉: 3%  (阈值 ≤ 5%)  ✅                              │
│  格式幻觉: 1%  (阈值 ≤ 3%)  ✅                              │
├────────────────────────────────────────────────────────────┤
│  成本效率                                                    │
│  平均 Token/运行: 12,500                                    │
│  平均质量/Token: 0.34 (综合评分/千 Token)                     │
│  成本/运行: $0.30                                           │
└────────────────────────────────────────────────────────────┘
```

### D.5 人工评估流程

| 步骤 | 活动 | 参与者 | 产出 |
|------|------|--------|------|
| 1 | 抽样（每周随机抽取 10 次运行） | 质量工程师 | 样本集 |
| 2 | 盲审（不知道是哪个模型/版本） | 2-3 名评审员 | 独立评分 |
| 3 | 讨论分歧（评分差异 > 1 的项目） | 评审组 | 共识评分 |
| 4 | 反馈到 Prompt 优化 | 提示工程师 | 改进后的 Prompt |
| 5 | 验证改进（对比前后评分） | 质量工程师 | 改进报告 |

---

## 附录 E: AI Agent 编排模式

### E.1 编排模式对比

| 模式 | 结构 | 适用场景 | 复杂度 | BOS-FS 匹配度 |
|------|------|---------|--------|--------------|
| **Chain** | 线性 A→B→C | 确定性流程 | 低 | ✅ Pipeline 模式 |
| **Router** | 条件分支 | 多路径决策 | 中 | ⚠️ 未来 DAG |
| **Parallel** | 并发执行 | 独立子任务 | 中 | ⚠️ 未来并行 Stage |
| **Orchestrator** | 中心调度 | 动态任务分配 | 高 | 🔴 过度设计 |
| **Evaluator-Optimizer** | 生成→评估→优化 | 迭代改进 | 高 | ⚠️ 可用于评审迭代 |

### E.2 BOS-FS Chain 模式详解

```
当前: 硬编码 Chain
  Understand → Map → Review → Refactor → Build → Analyze
  
优势:
  ✓ 简单可预测
  ✓ 易于调试
  ✓ 每个 Stage 可独立测试
  
局限:
  ✗ 无法跳过不需要的 Stage
  ✗ 无法并行执行
  ✗ 新增 Stage 需要修改代码
  
未来: 可配置 Chain (v1.0)
  通过配置文件定义 Stage 顺序和依赖
  支持条件执行 (if condition)
  支持并行执行 (parallel block)
```

### E.3 Agent 编排安全考量

| 安全风险 | 描述 | 防护措施 |
|---------|------|---------|
| **Prompt 注入** | 用户输入包含恶意指令 | 输入清洗 + 系统 Prompt 隔离 |
| **过度执行** | Agent 执行了超出预期的操作 | 操作白名单 + 输出验证 |
| **信息泄漏** | Agent 输出包含敏感信息 | 输出过滤 + 脱敏 |
| **无限循环** | Agent 陷入自我调用循环 | 最大迭代次数限制 |
| **资源耗尽** | Agent 消耗过多 Token | Token 预算 + 超时控制 |

---

## 附录 F: AI 系统可观测性和调试

### F.1 可观测性三层

| 层次 | 内容 | 工具 |
|------|------|------|
| **Logging** | 记录发生了什么 | 结构化日志 (JSON) |
| **Tracing** | 记录请求的完整路径 | OpenTelemetry / 自定义 Trace ID |
| **Metrics** | 记录聚合的统计信息 | Prometheus / 自定义计数器 |

### F.2 AI 特定可观测性

| 观测维度 | 指标 | 采集方式 | 告警阈值 |
|---------|------|---------|---------|
| **Token 使用** | 输入/输出 Token 数 | API 响应元数据 | 突增 > 50% |
| **模型选择** | 使用的模型和版本 | 配置记录 | 模型变更通知 |
| **Prompt 版本** | 使用的 Prompt 模板版本 | 模板 ID | 版本回退检测 |
| **响应质量** | 输出评分 (人工/自动) | LLM-as-a-Judge | 评分 < 3.5 |
| **错误模式** | 错误类型分布 | 错误日志分类 | 新错误类型 |
| **延迟分布** | P50/P90/P99 延迟 | 时间戳记录 | P99 > 30s |

### F.3 调试工具箱

| 工具 | 用途 | 使用方法 |
|------|------|---------|
| **Prompt 调试器** | 逐步执行 Prompt | 记录每一步的输入输出 |
| **Trace 查看器** | 查看完整请求链路 | 通过 run_id 追踪 |
| **Diff 工具** | 对比不同版本 Prompt 的输出 | A/B 测试 |
| **Token 分析器** | 分析 Token 消耗分布 | 识别浪费 |
| **幻觉检测器** | 自动检测幻觉输出 | 引用验证 + 逻辑检查 |

### F.4 BOS-FS 调试日志规范

```json
{
  "trace_id": "uuid",
  "run_id": "uuid",
  "stage_id": "understand",
  "timestamp": "2025-08-15T10:30:00Z",
  "model": "claude-sonnet-4-20250514",
  "prompt_version": "v1.2.0",
  "input_tokens": 1250,
  "output_tokens": 85,
  "latency_ms": 1200,
  "cost_usd": 0.012,
  "status": "success",
  "cache_hit": false,
  "retry_count": 0,
  "output_quality_score": 4.2,
  "error": null
}
```

### F.5 BOS-FS 知识摄取引擎观测方案

```
知识摄取引擎观测:
  1. 摄取指标
     - 书籍页数/章节数
     - 分块数量
     - 向量嵌入数量
     - 摄取耗时
     
  2. 检索指标
     - 检索命中率
     - Top-K 相关度
     - 检索延迟
     - 上下文利用率
     
  3. 质量指标
     - 提取准确性
     - 幻觉率
     - 覆盖率 (有多少知识被成功提取)
     
  4. 成本指标
     - Token 消耗/书籍
     - 存储成本
     - 检索成本
```

---

## 附录 G: 与其他知识文件的关联扩展

| 关联文件 | 关联点 | 使用场景 |
|---------|--------|---------|
| [architecture_quality_metrics.md](architecture_quality_metrics.md) | AI 生成代码的质量监控 | 用架构指标监控 AI 生成代码的结构质量 |
| [flow_metrics.md](../adoption/flow_metrics.md) | AI 生成效率纳入 Flow 度量 | AI 处理时间占 Flow Time 的比例 |
| [architecture_patterns.md](../runtime/architecture_patterns.md) | AI 驱动的运行时模式 | Pipeline 如何支撑 AI 生成 |
| [trust_framework.md](trust_framework.md) | AI 生成内容的可信度保障 | 引用验证 + 幻觉检测 |
| [discovery_framework.md](../intent/discovery_framework.md) | AI 辅助发现 | 用 AI 加速用户访谈分析 |
| [mlops_delivery.md](mlops_delivery.md) | AI 模型的 MLOps 交付 | 模型版本管理和部署 |

---

## 逐章深度提炼 v0.2.0（基于原文逐章读取，NEED4 重新校准）

### Chapter 1: Introduction to Building AI Applications with Foundation Models
**核心论点**: AI Engineering 是在基础模型之上构建应用的新工程学科。与 ML Engineering 不同，AI Engineering 利用现有强大模型而非从头训练。三个因素（通用AI能力/低API使用成本/低入门门槛）共同推动了AI Engineering的爆发式增长。
**关键概念**: Foundation Model（LLM/LMM）、Self-supervision、AI Engineering vs ML Engineering、三大驱动因素、提示工程/RAG/微调三大适配技术
**实践方法**: 选择适配技术（提示工程快速验证→RAG接入知识库→微调提升质量）；评估自建 vs 调用API；理解 token/参数/多模态基础概念
**BOS-FS 映射**: BOS-FS Pipeline 可作为 AI 应用的"质量门"——代码审查检测 prompt injection/数据泄露风险。技术评审 Stage 可检查 AI 依赖的安全性和合规性。四类评审保障 AI 交付的可控性和可追溯性。

### Chapter 2: Understanding Foundation Models
**核心论点**: 基础模型的能力、局限性和内部机制决定了 AI 应用的设计边界。理解预训练、上下文窗口、幻觉、概率生成是构建可靠 AI 应用的前提。
**关键概念**: 预训练与后训练、上下文窗口限制、幻觉（hallucination）、概率生成本质、温度参数、top-k/top-p 采样
**实践方法**: 根据任务选择模型大小；控制温度参数平衡创造性vs确定性；设计 prompt 减少幻觉；建立评估基准
**BOS-FS 映射**: Pipeline 技术评审应检查 AI 应用的"幻觉缓解策略"和"确定性保障"。投资评审评估 API 调用成本 vs 自建模型 ROI。Pipeline 确保 AI 组件纳入质量保障体系。

### Chapter 3: Evaluating AI Applications
**核心论点**: AI 应用评估与传统软件测试根本不同——输出是概率性的、开放式的。需要建立多维度评估体系：准确性、安全性、鲁棒性、延迟、成本。
**关键概念**: 评估基准（benchmark）、LLM-as-a-Judge、人工评估、自动评估、红队测试、对抗性评估
**实践方法**: 建立任务特定的评估数据集；组合自动+人工评估；持续监控生产环境性能；红队测试检测安全漏洞
**BOS-FS 映射**: Pipeline 可集成 AI 评估工具作为 Custom Stage。技术评审检查评估覆盖率，产品评审验证用户体验指标。Pipeline 确保评估在部署前完成。

### Chapter 4: Prompt Engineering
**核心论点**: 提示工程是与基础模型交互的核心技能。好的 prompt 设计可以显著提升输出质量，是最轻量的模型适配方法。
**关键概念**: Zero-shot/Few-shot、Chain-of-Thought、ReAct 框架、结构化 prompt、prompt 模板、prompt 版本管理
**实践方法**: 使用 few-shot 提供示例；结构化 prompt（角色/任务/格式/约束）；迭代优化 prompt；建立 prompt 测试集
**BOS-FS 映射**: Pipeline 可审查 prompt 安全性（injection检测）。技术评审检查 prompt 是否有版本管理和测试覆盖。Pipeline 确保 prompt 变更纳入代码审查流程。

### Chapter 5: Building AI Pipelines (RAG & Agents)
**核心论点**: RAG（检索增强生成）和 Agent 模式是 AI 应用的两大核心架构模式。RAG 解决知识更新问题，Agent 解决复杂任务编排问题。
**关键概念**: RAG 架构（检索器/向量数据库/生成器）、Agent 模式（规划/工具使用/记忆）、多 Agent 协作、工具调用
**实践方法**: RAG：构建知识库→向量化→检索策略→生成整合；Agent：定义工具→规划策略→记忆管理→错误恢复
**BOS-FS 映射**: BOS-FS Pipeline 本身即是一种"Agent Workflow"——Stage 是工具，执行顺序是规划，报告是记忆。Pipeline 的 Stage 设计模式可借鉴 Agent 架构。

### Chapter 6: Fine-Tuning Foundation Models
**核心论点**: 微调是在特定任务上提升模型性能的技术手段，适用于 RAG 和提示工程无法满足的场景。需要平衡数据质量、计算成本和性能收益。
**关键概念**: 全量微调 vs PEFT（LoRA/QLoRA）、指令微调、RLHF、数据准备、过拟合检测
**实践方法**: 评估是否真正需要微调；准备高质量指令数据；选择 PEFT 降低计算成本；建立微调评估基准
**BOS-FS 映射**: 技术评审检查微调项目的数据隐私和合规性。投资评审评估微调成本 vs API 调用成本。Pipeline 确保微调过程可追溯。

### Chapter 7: Building Reliable AI Applications
**核心论点**: AI 应用的可靠性挑战远超传统软件——概率输出、非确定性、幻觉、prompt injection 等都需要专门的保障机制。
**关键概念**: 确定性保障、输出验证、Guardrails、回退策略、监控告警、可观测性
**实践方法**: 为关键输出建立验证层；设置 guardrails 防止不安全输出；设计确定性回退路径；建立 AI 专项监控
**BOS-FS 映射**: Pipeline 四类评审是 AI 应用"可靠性保障"的关键环节。技术评审检查 guardrails 实现，开源评审检测模型供应链风险。Pipeline 确保可靠性在部署前验证。

### Chapter 8: AI Application Architecture
**核心论点**: AI 应用架构需要专门的模式和方法论。与传统架构不同，AI 架构需要处理概率组件、外部模型依赖、数据隐私和成本优化。
**关键概念**: AI 架构模式（API 调用/自托管/混合）、模型路由、缓存策略、多模型编排、成本优化
**实践方法**: 选择部署模式（API vs 自托管）；设计模型路由策略；实现响应缓存降低成本；多模型组合提升质量
**BOS-FS 映射**: Pipeline 可审查 AI 架构决策的合规性和安全性。投资评审评估架构成本效益。Pipeline 确保 AI 架构决策被记录和追溯。

### Chapter 9: AI Infrastructure and Operations
**核心论点**: AI 基础设施和运营（AI Ops）需要专门的工具链和流程。GPU 资源管理、模型版本控制、数据管线、监控告警都与传统运维不同。
**关键概念**: GPU 资源调度、模型注册表、数据版本控制、推理服务、自动扩缩容、成本监控
**实践方法**: 建立模型注册表管理版本；实现推理服务自动化；监控 GPU 利用率；建立 AI 成本仪表盘
**BOS-FS 映射**: BOS-FS Pipeline 可扩展支持 AI 组件的 CI/CD——模型版本管理、数据管线审查、推理服务健康检查。Pipeline 成为 AI Ops 的一部分。

### Chapter 10: The Future of AI Engineering
**核心论点**: AI Engineering 正在快速演进。多 Agent 系统、具身智能、AI 原生应用等新范式将重塑软件开发。工程师需要持续学习和适应。
**关键概念**: 多 Agent 系统、具身智能、AI 原生设计、AI 辅助编程、模型开源趋势
**实践方法**: 持续跟踪模型和技术发展；建立实验文化；关注开源社区；培养跨领域能力
**BOS-FS 映射**: Pipeline 需要持续演进以适配 AI 工程新需求。Custom Stage 机制支持灵活扩展。Pipeline 应成为"AI 工程实践"的质量保障基础设施。
