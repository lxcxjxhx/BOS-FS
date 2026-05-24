# 架构模式框架（Architecture Patterns）

> 来源: Fundamentals of Software Architecture (Mark Richards & Neal Ford) / Software Architecture Metrics (Ciceri, Farley, Ford)  
> 映射: BOS-FS 五层架构 → Runtime Layer + Execution Layer  
> 用途: 指导 BOS-FS 架构设计与演进，提供模块化、事件驱动、演化式架构的实战模式与权衡分析方法。

---

## 一、架构设计核心原则

### 1.1 第一定律：万物皆可权衡（Everything in Architecture is a Trade-off）

Richards & Ford 的核心论断: 架构决策没有对错，只有权衡。

| 维度 | 内容 |
|------|------|
| **核心命题** | 每个架构决策都有利弊，不存在"最佳方案" |
| **关键问题** | "这个方案相对于替代方案的权衡是什么？" |
| **BOS-FS 应用** | Pipeline Stage 设计、Skill 粒度、知识组织方式的选择都是权衡结果 |

**BOS-FS 中的典型权衡**:

| 决策 | 选择 | 收益 | 代价 | 权衡理由 |
|------|------|------|------|---------|
| Stage 粒度 | 6个中等粒度 Stage | 可独立替换/升级 | Stage 间数据传递成本 | 平衡灵活性与复杂度 |
| 通信方式 | JSON 数据总线 | 语言无关/易调试 | 缺乏类型安全 | 支持多 AI Agent 集成 |
| 知识组织 | Markdown 文件 | 人类可读/易编辑 | 缺乏结构化查询 | 适合 AI 阅读理解 |
| 状态持久化 | 文件系统 | 零依赖/易调试 | 并发控制复杂 | 当前规模足够 |

### 1.2 架构特性（Architectural Characteristics）

系统需要满足的非功能性需求，BOS-FS 关注以下特性:

| 特性 | 优先级 | 定义 | BOS-FS 实现 |
|------|--------|------|------------|
| **可插拔性** | 🔴 高 | 组件可独立替换 | Skill 接口协议 + Stage Registry |
| **可维护性** | 🔴 高 | 代码易理解和修改 | 清晰的 Stage 边界 + 知识文件组织 |
| **可扩展性** | 🟡 中 | 支持新增功能 | Custom Stage + Plugin Interface |
| **可靠性** | 🟡 中 | 运行稳定 | 异常隔离 + 重试机制 + 缓存 |
| **性能** | 🟢 低 | 响应速度 | 当前阶段非瓶颈（AI 处理占主导） |
| **安全性** | 🟢 低 | 数据保护 | 本地运行，无网络传输 |

### 1.3 架构适度原则（The "It Depends" Principle）

| 情境 | 推荐做法 | 理由 |
|------|---------|------|
| 快速原型 | 单文件 + 简单流水线 | 验证可行性优先 |
| 生产使用 | 分层架构 + 接口契约 | 可维护性和可替换性 |
| 大规模部署 | 微服务 + 消息队列 | 扩展性和隔离性 |
| 当前 BOS-FS | 模块化单进程 + Stage 协议 | 平衡复杂度与可维护性 |

---

## 二、模块化架构模式

### 2.1 BOS-FS 模块化设计

```
┌─────────────────────────────────────────────────────────┐
│                    BOS-FS Architecture                    │
│                                                          │
│  ┌───────────────────────────────────────────────────┐   │
│  │                Skill Layer (技能层)                │   │
│  │  01_goal_refiner  02_reviewer_simulator           │   │
│  │  03_readme_refactor 04_outcome_mapper             │   │
│  │  05_submission_builder 06_reject_analyzer         │   │
│  │  07_book_knowledge_ingestor                       │   │
│  └─────────────────────────┬─────────────────────────┘   │
│                            │ Skill Manifest               │
│  ┌─────────────────────────▼─────────────────────────┐   │
│  │              Engine Layer (引擎层)                  │   │
│  │                                                    │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │   │
│  │  │Intent   │ │Value    │ │Submission│ │Review   │  │   │
│  │  │Parser   │ │Mapper   │ │Optimizer │ │Simulator │  │   │
│  │  │(Goal)   │ │(Outcome)│ │(Readme)  │ │(Review)  │  │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │   │
│  │  ┌─────────┐ ┌─────────┐                          │   │
│  │  │Artifact │ │Knowledge│                          │   │
│  │  │Generator│ │Ingestor │                          │   │
│  │  │(Reject) │ │(Book)   │                          │   │
│  │  └─────────┘ └─────────┘                          │   │
│  └─────────────────────────┬─────────────────────────┘   │
│                            │ PipelineContext              │
│  ┌─────────────────────────▼─────────────────────────┐   │
│  │             Runtime Layer (运行时层)                │   │
│  │  • State Machine  • Cache/Replay                   │   │
│  │  • Error Handling  • CLI Integration               │   │
│  └─────────────────────────┬─────────────────────────┘   │
│                            │                              │
│  ┌─────────────────────────▼─────────────────────────┐   │
│  │           Knowledge Layer (知识层)                  │   │
│  │  • intent/  • adoption/  • runtime/               │   │
│  │  • execution/  • governance/                      │   │
│  └───────────────────────────────────────────────────┘   │
│                                                          │
│  ┌───────────────────────────────────────────────────┐   │
│  │           Governance Layer (治理层)                 │   │
│  │  • metrics_framework  • rubrics                   │   │
│  │  • trust_framework  • review_rules/               │   │
│  └───────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 2.2 模块边界设计原则

| 原则 | 内容 | BOS-FS 中的应用 |
|------|------|----------------|
| **高内聚** | 模块内部功能高度相关 | 每个 Stage 只做一件事（单一职责） |
| **低耦合** | 模块间依赖最小化 | Stage 间仅通过 JSON 数据总线通信 |
| **明确契约** | 接口定义清晰 | `input_schema` / `output_schema` |
| **可替换性** | 实现可独立替换 | Custom Stage 注册机制 |
| **异常隔离** | 一个模块失败不影响其他 | try/except 包裹每个 Stage |

### 2.3 模块耦合度量化

| 耦合类型 | 定义 | BOS-FS 状态 | 目标 |
|---------|------|------------|------|
| **数据耦合** | 通过参数传递数据 | ✅ 仅通过 PipelineContext.shared_data | 保持 |
| **控制耦合** | 通过标志位控制行为 | ⚠️ Stage 执行顺序固定 | 未来支持 DAG |
| **内容耦合** | 直接访问模块内部数据 | ✅ 无 | 保持 |
| **公共耦合** | 通过全局变量共享数据 | ⚠️ PipelineContext 是共享上下文 | 限制为只追加 |

---

## 三、事件驱动模式

### 3.1 BOS-FS 中的事件驱动

虽然 BOS-FS 当前是顺序 Pipeline，但内部遵循事件驱动思想:

```
事件流:
  [项目描述输入] ──▶ Event: InputReceived
       │
       ▼
  [Goal Refined] ──▶ Event: GoalRefined
       │
       ▼
  [Outcomes Mapped] ──▶ Event: OutcomesMapped
       │
       ▼
  [README Refactored] ──▶ Event: ReadmeRefactored
       │
       ▼
  [Submission Built] ──▶ Event: SubmissionBuilt
       │
       ▼
  [Review Complete] ──▶ Event: ReviewComplete
       │
       ▼
  [Pipeline Complete] ──▶ Event: PipelineComplete
```

### 3.2 事件驱动的优势

| 优势 | BOS-FS 中的应用 |
|------|----------------|
| **解耦** | Stage 不需要知道上游/下游的具体实现 |
| **可追溯** | 每个事件携带完整的上下文（run_id, timestamp） |
| **可扩展** | 可添加新 Stage 监听现有事件 |
| **可回放** | 事件日志支持断点恢复（resume 命令） |

### 3.3 事件数据结构

```json
{
  "event_type": "stage_complete",
  "pipeline_run_id": "uuid",
  "stage_id": "understand",
  "timestamp": "2025-08-15T10:30:00Z",
  "input": { "description": "..." },
  "output": { "persona": "...", "problem": "...", "solution": "...", "outcome": "..." },
  "metadata": {
    "duration_ms": 42,
    "cache_hit": false,
    "attempt": 1
  }
}
```

### 3.4 向完全事件驱动演进的路线图

```
Phase 1 (当前): 顺序 Pipeline + 事件日志
  └─ 优点: 简单、易调试
  └─ 局限: Stage 执行顺序固定

Phase 2: DAG-based Pipeline
  └─ Stage 可声明依赖关系
  └─ Pipeline 自动拓扑排序
  └─ 支持并行执行无依赖的 Stage

Phase 3: 完全事件驱动
  └─ Stage 通过事件总线通信
  └─ 支持动态 Stage 注册/注销
  └─ 支持多 Pipeline 实例并发
```

---

## 四、演化式架构（Evolutionary Architecture）

### 4.1 演化式架构原则

Ford 定义的核心原则: 架构应该支持渐进式变更，而非一次性的大重构。

| 原则 | 内容 | BOS-FS 实践 |
|------|------|------------|
| **增量变更** | 小步修改而非大重构 | 每次版本只改动 1-2 个 Stage |
| **适配度函数** | 自动化验证架构约束 | 未来: 自动测试 Stage 接口契约 |
| **最后责任时刻** | 推迟不可逆决策 | Stage 接口保持灵活，不锁定实现 |
| **架构治理** | 持续监控架构健康度 | Architecture Metrics (coupling/cohesion/modularity) |

### 4.2 适配度函数设计

适配度函数（Fitness Functions）是自动化验证架构约束的机制:

| 适配度函数 | 验证内容 | 当前状态 | 实现方式 |
|-----------|---------|---------|---------|
| Stage 接口契约 | 每个 Stage 实现 input_schema/output_schema | ✅ 已实现 | Python Protocol |
| 异常隔离 | Stage 异常不传播 | ✅ 已实现 | try/except 包裹 |
| 数据契约 | Stage 间传递的数据格式一致 | ✅ 已实现 | JSON Schema |
| 缓存一致性 | 相同输入产生相同输出 | ✅ 已实现 | cache_key 哈希 |
| Stage 内聚度 | Stage 功能聚焦核心职责 | ⚠️ 未自动化 | 人工评审 |
| Stage 耦合度 | Stage 间依赖最小 | ⚠️ 未自动化 | 人工评审 |

### 4.3 架构演化路线图

```
v0.1-v0.5: 验证阶段
  └─ 核心 Pipeline 跑通
  └─ 基础 Stage 实现
  └─ 简单知识文件

v0.6-v0.10: 稳定阶段
  └─ Stage 接口契约完善
  └─ 异常处理/重试/缓存
  └─ 四类评审规则
  └─ 完整知识体系

v0.11-v0.15: 优化阶段 (当前)
  └─ Token 优化
  └─ 信任框架
  └─ 一致性保障
  └─ 知识文件从书籍提取

v1.0+: 演化阶段
  └─ DAG-based Pipeline
  └─ 插件生态系统
  └─ 多 Agent 集成
  └─ 分布式运行时
```

### 4.4 架构决策记录（ADR）模板

```markdown
# ADR-[编号]: [决策标题]

## 状态: [提议/接受/已弃置/已替代]
## 日期: [YYYY-MM-DD]

## 背景
[为什么需要做这个决策？]

## 决策
[我们决定做什么？]

## 权衡分析
### 选择的方案
- 优势: [...]
- 劣势: [...]

### 替代方案
- 方案 A: [...]
- 方案 B: [...]

## 后果
[这个决策会带来什么影响？]

## 相关决策
[与哪些 ADR 相关？]
```

---

## 五、权衡分析框架（Trade-off Analysis）

### 5.1 ATAM 方法（Architecture Tradeoff Analysis Method）

简化版 ATAM 适用于 BOS-FS 日常架构决策:

```
1. 描述架构决策
2. 列出架构特性需求（可插拔性/性能/可维护性...）
3. 分析决策对每个特性的影响（+ 改善 / - 损害 / = 不变）
4. 识别敏感点（哪些决策对某个特性影响最大？）
5. 识别权衡点（哪些决策对多个特性有相反影响？）
6. 做出决策并记录理由
```

### 5.2 BOS-FS 权衡分析示例

**决策**: 知识文件使用 Markdown 还是 JSON？

| 特性 | Markdown | JSON | 分析 |
|------|----------|------|------|
| 人类可读性 | ++ | -- | Markdown 更适合阅读和编辑 |
| AI 可理解性 | + | ++ | JSON 更结构化，但 Markdown 也能解析 |
| 编辑友好度 | ++ | - | Markdown 可增量编辑 |
| 查询能力 | -- | ++ | JSON 可程序化查询 |
| 版本控制友好 | ++ | + | Markdown diff 更清晰 |
| **结论** | ✅ 选择 Markdown | | 人工编辑和 AI 阅读是主要场景 |

### 5.3 架构特性优先级矩阵

在资源有限时，按优先级排序架构特性:

```
  重要性
    ▲
    │  🔴 核心特性
  高 │  (必须满足)
    │
    │  🟡 重要特性
    │  (应该满足)
    │
    │  🟢 期望特性
  低 │  (可以满足)
    │
    └────────────────────▶ 实现成本
        低        中        高
```

**BOS-FS 特性优先级**:

| 特性 | 优先级 | 当前满足度 | 改进方向 |
|------|--------|-----------|---------|
| 可插拔性 | 🔴 | 80% | 完善 Plugin Interface |
| 可维护性 | 🔴 | 85% | 增加架构文档 |
| 可扩展性 | 🟡 | 70% | DAG Pipeline |
| 可靠性 | 🟡 | 75% | 增强错误恢复 |
| 性能 | 🟢 | 90% | 当前不是瓶颈 |
| 安全性 | 🟢 | 80% | 本地运行风险低 |

---

## 六、架构质量度量

### 6.1 模块化度量

| 度量 | 定义 | 计算公式 | 目标值 | 采集方式 |
|------|------|---------|--------|---------|
| **耦合度** | 跨模块依赖程度 | `(inter_stage_refs) / total_stages` | < 0.3 | 代码静态分析 |
| **内聚度** | 模块功能聚焦度 | `core_functions / total_functions` | ≥ 0.8 | 功能点分析 |
| **可插拔性** | 模块可替换程度 | 0-10 量表 | ≥ 8.0 | 热插拔测试 |
| **复杂度** | 模块理解难度 | 圈复杂度 / 认知复杂度 | < 15 | 静态分析工具 |

### 6.2 BOS-FS 架构健康度评分

```
Architecture Health Score =
  (Coupling_Inverse × 30%) +
  (Cohesion × 25%) +
  (Pluggability × 25%) +
  (Complexity_Inverse × 20%)
```

| 等级 | 分数 | 含义 |
|------|------|------|
| **健康** | ≥ 8.0 | 架构质量良好，可持续演进 |
| **亚健康** | 6.0-7.9 | 有技术债务，需要关注 |
| **不健康** | < 6.0 | 需要架构重构 |

### 6.3 架构债务追踪

| 债务类型 | 症状 | 影响 | 偿还优先级 |
|---------|------|------|-----------|
| **接口债务** | Stage 接口不一致 | 替换困难 | 🔴 高 |
| **知识债务** | 知识文件与代码不同步 | AI 理解偏差 | 🟡 中 |
| **测试债务** | 缺少架构约束测试 | 退化风险 | 🟡 中 |
| **文档债务** | 架构文档缺失 | 新人上手慢 | 🟢 低 |

---

## 七、BOS-FS Runtime 架构模式应用

### 7.1 State Machine 模式

BOS-FS 的 Pipeline 使用状态机模式管理 Stage 执行:

| 状态 | 触发条件 | 转换 |
|------|---------|------|
| `Idle` | `start(cfg)` | → `Processing` 或 → `Complete` |
| `Processing` | `stage.run()` 成功 | → `Processing` (next stage) |
| `Processing` | `stage.run()` 需要输入 | → `Waiting` |
| `Processing` | `stage.run()` 失败 | → `ErrorState` |
| `Waiting` | `user_input(data)` | → `Processing` |
| `ErrorState` | `retry()` (次数 < max) | → `Processing` |
| `Processing` | `all_complete()` | → `Complete` |

详见 `runtime/pipeline.md` 中的完整状态机规范。

### 7.2 Strategy 模式

不同 Stage 实现统一的 `Stage` 协议，支持运行时替换:

```python
class Stage(Protocol):
    name: str
    input_schema: dict
    output_schema: dict

    def validate_input(self, data: dict) -> tuple[bool, str]: ...
    def execute(self, ctx: PipelineContext) -> StageResult: ...
```

### 7.3 Chain of Responsibility 模式

Pipeline Stage 组成责任链，每个 Stage 处理一部分职责:

```
Input → Goal Refiner → Outcome Mapper → Readme Refactor → Submission Builder → Reviewer Simulator → Output
         (理解意图)     (转换价值)       (优化表达)        (构建提交包)       (模拟评审)
```

### 7.4 Observer 模式

Pipeline 运行状态变化触发事件通知:

```python
class PipelineObserver(Protocol):
    def on_stage_start(self, stage_id: str, ctx: PipelineContext): ...
    def on_stage_complete(self, stage_id: str, result: StageResult): ...
    def on_stage_error(self, stage_id: str, error: Exception): ...
    def on_pipeline_complete(self, ctx: PipelineContext): ...
```

---

## 八、与其他知识文件的关联

| 关联文件 | 关联点 | 使用场景 |
|---------|--------|---------|
| [flow_metrics.md](../adoption/flow_metrics.md) | 架构决策对效能的影响 | 架构权衡如何影响 Flow Efficiency |
| [metrics_framework.md](../governance/metrics_framework.md) | Architecture Metrics 定义 | 耦合度/内聚度/可插拔性度量 |
| [team_topology.md](../adoption/team_topology.md) | 架构与团队拓扑的对应 | 模块边界 ↔ 团队边界 |
| [ai_delivery_framework.md](../governance/ai_delivery_framework.md) | AI 架构模式 | Runtime 如何支撑 AI 驱动的交付 |
| [base_context.md](../base_context.md) | 输出规范 | 保持一致的文档结构 |

---

> 完整框架参见:  
> Mark Richards & Neal Ford, *Fundamentals of Software Architecture* (2020)  
> Ciceri, Farley, Ford et al., *Software Architecture Metrics* (2023)  
> BOS-FS 实现: `runtime/pipeline.md` + Stage 协议定义 + PipelineContext 数据流

---

## 附录 A: 架构特征定义与适配度函数

### A.1 架构特征（Architectural Characteristics）完整分类

Richards & Ford 将架构特征分为三类:

| 类别 | 定义 | 示例 | BOS-FS 关注 |
|------|------|------|------------|
| **运行时特征** | 系统运行时表现的特性 | 可用性、性能、弹性、安全性 | 低（当前不是重点） |
| **静态特征** | 系统在静止状态的特性 | 可维护性、可测试性、可部署性 | 🔴 高 |
| **跨切特征** | 影响多个维度的特性 | 可扩展性、适应性、合规性 | 🟡 中 |

### A.2 关键架构特征的适配度函数

适配度函数 = 自动化验证架构特征满足度的机制。

```
适配度函数三要素:
1. 度量什么 (What to measure)
2. 如何度量 (How to measure)
3. 什么算合格 (Pass/Fail criteria)
```

#### BOS-FS 适配度函数清单

```python
# 适配度函数: Stage 接口契约验证
def fitness_stage_contract():
    """验证所有 Stage 实现了 input_schema 和 output_schema"""
    for stage in registry.get_all_stages():
        assert hasattr(stage, 'input_schema'), f"{stage.name} 缺少 input_schema"
        assert hasattr(stage, 'output_schema'), f"{stage.name} 缺少 output_schema"
        assert validate_json_schema(stage.input_schema), f"{stage.name} 的 input_schema 无效"
        assert validate_json_schema(stage.output_schema), f"{stage.name} 的 output_schema 无效"

# 适配度函数: 知识文件引用完整性
def fitness_knowledge_references():
    """验证所有 knowledge/ 文件的交叉引用有效"""
    refs = extract_markdown_references("knowledge/")
    for ref in refs:
        assert os.path.exists(ref.target_path), f"引用断裂: {ref.source} → {ref.target_path}"

# 适配度函数: 异常隔离
def fitness_exception_isolation():
    """验证 Stage 异常不会传播到其他 Stage"""
    # 注入异常到每个 Stage，验证其他 Stage 不受影响
    for stage in registry.get_all_stages():
        result = run_with_injected_error(stage, ValueError("test"))
        assert result.status == "error"
        assert result.error_isolated, f"{stage.name} 的异常未隔离"

# 适配度函数: 圈复杂度上限
def fitness_cyclomatic_complexity():
    """验证所有函数的圈复杂度不超过阈值"""
    for func in analyze_python_complexity("engine/"):
        assert func.cc <= 25, f"{func.name} 的圈复杂度 {func.cc} 超过阈值 25"
```

### A.3 适配度函数执行时机

| 时机 | 执行方式 | 覆盖范围 | 反馈速度 |
|------|---------|---------|---------|
| 代码提交 | Git Hook / CI | 变更的代码 | 秒级 |
| 合并请求 | CI Pipeline | 全部代码 | 分钟级 |
| 定时检查 | Cron Job | 全部代码+文档 | 小时级 |
| 架构评审 | 手动触发 | 特定特征 | 即时 |

---

## 附录 B: 架构风格矩阵

### B.1 常见架构风格对比

| 风格 | 耦合度 | 复杂度 | 可测试性 | 部署难度 | 适用场景 | BOS-FS 使用 |
|------|--------|--------|---------|---------|---------|------------|
| **微内核** | 低 | 中 | 高 | 低 | 插件化系统 | ✅ 当前 |
| **分层架构** | 低 | 低 | 高 | 低 | 企业应用 | ⚠️ 隐含在知识分层中 |
| **事件驱动** | 低 | 高 | 中 | 中 | 异步处理、实时系统 | ⚠️ 未来 Phase 3 |
| **微服务** | 极低 | 极高 | 中 | 高 | 大规模分布式系统 | 🔴 不适用 |
| **空间架构** | 极低 | 极高 | 低 | 高 | 极高并发场景 | 🔴 不适用 |
| **编排架构** | 中 | 中 | 高 | 低 | 业务流程 | ⚠️ Pipeline 类似 |

### B.2 BOS-FS 当前架构风格: 微内核

```
┌─────────────────────────────────────────────┐
│              微内核架构                        │
│                                              │
│  ┌─────────────────────────────────────┐     │
│  │            核心系统 (Core)            │     │
│  │  • Pipeline 状态机                    │     │
│  │  • Stage 注册表                       │     │
│  │  • PipelineContext (数据总线)         │     │
│  │  • 异常处理框架                       │     │
│  └──────────────────┬──────────────────┘     │
│                     │                         │
│     ┌───────────────┼───────────────┐         │
│     │               │               │         │
│  ┌──▼──┐  ┌────────▼─┐  ┌────────▼─┐        │
│  │Stage│  │Stage     │  │Stage     │        │
│  │插件  │  │插件      │  │插件      │  ...   │
│  │#1   │  │#2        │  │#3        │        │
│  └─────┘  └──────────┘  └──────────┘        │
│                                              │
│  核心不变，插件可变                            │
└─────────────────────────────────────────────┘
```

| 维度 | 当前实现 | 评估 |
|------|---------|------|
| 核心职责 | 状态机、注册表、数据流管理 | ✅ 精简 |
| 插件机制 | Stage 协议（Python Protocol） | ✅ 清晰 |
| 插件通信 | PipelineContext.shared_data (JSON) | ✅ 松耦合 |
| 核心可扩展性 | Stage 注册表支持动态注册 | ⚠️ 当前为静态注册 |
| 插件独立性 | Stage 异常隔离，不互相影响 | ✅ 良好 |

### B.3 架构风格选择决策树

```
系统需要独立部署的组件？
  ├─ 是 → 是否需要跨网络通信？
  │        ├─ 是 → 需要高并发？
  │        │        ├─ 是 → 空间架构 (如 Redis Cluster 场景)
  │        │        └─ 否 → 微服务架构
  │        └─ 否 → 分层架构 / 模块化单体
  └─ 否 → 是否需要插件化扩展？
           ├─ 是 → 微内核架构 ← BOS-FS 当前选择
           └─ 否 → 是否需要异步处理？
                    ├─ 是 → 事件驱动架构
                    └─ 否 → 管道-过滤器架构 / 分层架构
```

---

## 附录 C: 演化架构模式详解

### C.1 演化架构的三大支柱

Ford 定义的演化架构基于三大支柱:

| 支柱 | 定义 | BOS-FS 实现 | 成熟度 |
|------|------|------------|--------|
| **增量变更** | 架构可以渐进式修改 | Stage 可独立替换 | ✅ 成熟 |
| **适配度函数** | 自动化验证架构约束 | 见 A.2 清单 | ⚠️ 部分实现 |
| **架构治理** | 持续监控架构健康 | 架构质量指标 (见 architecture_quality_metrics.md) | ⚠️ 部分实现 |

### C.2 演化策略

| 策略 | 描述 | 适用场景 | BOS-FS 应用 |
|------|------|---------|------------|
| **绞杀者模式** | 新功能用新架构，旧功能逐步迁移 | 大系统重构 | 不适用（系统较小） |
| **分支抽象** | 在旧接口上构建抽象层，新实现通过抽象 | 接口变更 | 未来: Stage 接口升级 |
| **并行实现** | 新旧实现并行运行，逐步切换流量 | 关键路径变更 | 未来: 模型切换 |
| **扩展点** | 预留扩展接口，按需实现 | 已知但不确定的需求 | Custom Stage 机制 |

### C.3 BOS-FS 架构演化记录

```
v0.1-v0.5: 原型验证 (单体)
  └─ 架构: 单文件脚本
  └─ 变更: 不可演化

v0.6-v0.10: 模块化 (当前已实现)
  └─ 架构: 微内核 + Stage 插件
  └─ 变更: Stage 可独立替换
  └─ 适配度: 接口契约验证

v0.11-v0.15: 增强模块化 (当前)
  └─ 架构: 微内核 + 知识分层
  └─ 变更: 知识文件可独立更新
  └─ 适配度: + 引用完整性验证

v1.0+: 可配置 Pipeline
  └─ 架构: 微内核 + DAG 编排
  └─ 变更: Pipeline 结构可配置
  └─ 适配度: + DAG 正确性验证

v2.0+: 事件驱动
  └─ 架构: 事件驱动 + 微内核
  └─ 变更: Stage 可动态注册/注销
  └─ 适配度: + 事件流完整性验证
```

---

## 附录 D: ATAM 权衡分析方法

### D.1 ATAM 完整流程

Architecture Tradeoff Analysis Method (ATAM) 是 SEI 提出的架构评估方法:

```
步骤 1: 呈现 ATAM 流程
步骤 2: 呈现业务驱动因素
步骤 3: 呈现架构设计
步骤 4: 识别架构方法
步骤 5: 生成质量属性效用树
步骤 6: 分析架构方法
步骤 7: 头脑风暴和优先级排序场景
步骤 8: 分析架构方法 (第二轮)
步骤 9: 呈现结果
```

### D.2 简化版 ATAM（适用于日常架构决策）

```markdown
# ATAM 简化模板

## 决策描述
[什么架构决策需要评估？]

## 业务驱动因素
- [业务目标 1]
- [业务目标 2]

## 质量属性效用树

| 属性 | 场景 | 重要性 (H/M/L) | 难度 (H/M/L) |
|------|------|---------------|-------------|
| 可插拔性 | 新增 Stage 无需修改核心代码 | H | M |
| 可维护性 | 新人 1 周内理解代码结构 | H | M |
| 可扩展性 | 支持 10+ Stage 并行执行 | M | H |
| 可靠性 | Pipeline 失败可恢复 | H | L |

## 敏感点
- [哪个决策对哪个属性影响最大？]

## 权衡点
- [哪个决策对多个属性有相反影响？]

## 风险决策
- [哪些决策可能在未来成为问题？]

## 非风险决策
- [哪些决策确认是安全的？]
```

### D.3 BOS-FS ATAM 分析示例

**决策**: 使用 JSON 数据总线 vs 类型安全对象

| 质量属性 | JSON 数据总线 | 类型安全对象 | 分析 |
|---------|-------------|-------------|------|
| 可插拔性 | ++ 语言无关 | -- 锁定 Python | JSON 更适合多语言 |
| 类型安全 | -- 运行时才能发现 | ++ 编译时检查 | JSON 需要额外验证 |
| 开发速度 | ++ 快速迭代 | -- 需要先定义类型 | JSON 适合原型 |
| 维护性 | -- 缺少文档化 | ++ 类型即文档 | 类型安全更利于长期维护 |
| AI 友好度 | ++ LLM 擅长 JSON | ⚠️ LLM 也能生成类 | JSON 略优 |

**结论**: 当前选择 JSON 数据总线，但需要在 v1.0 引入 JSON Schema 验证弥补类型安全。

### D.4 ATAM 输出 — 风险清单

| 风险 | 影响属性 | 严重度 | 缓解措施 |
|------|---------|--------|---------|
| JSON 数据总线缺少类型安全 | 可靠性、可维护性 | 中 | 引入 JSON Schema 验证 |
| Pipeline 顺序固定 | 可扩展性、性能 | 中 | 规划 DAG Pipeline |
| 知识文件无版本控制 | 可追溯性 | 低 | 利用 Git 版本控制 |
| 无架构测试 | 退化风险 | 中 | 编写适配度函数测试 |

---

## 附录 E: 架构 Kata 练习

### E.1 什么是架构 Kata

架构 Kata 是团队练习架构思维的短练习（1-2 小时），通过解决简化的架构问题来提升团队的架构决策能力。

### E.2 BOS-FS 团队适用的架构 Kata

#### Kata 1: Stage 粒度设计

```
场景: 你需要为一个 "代码质量分析" 功能设计 Pipeline Stage。
功能包括:
  - 代码静态分析
  - 测试覆盖率计算
  - 安全漏洞扫描
  - 性能分析
  - 生成质量报告

问题:
  1. 这是一个 Stage 还是多个 Stage？
  2. 如果是多个，如何划分边界？
  3. Stage 间传递什么数据？
  4. 每个 Stage 的 input_schema / output_schema 是什么？

时间: 30 分钟
产出: Stage 设计图 + 接口定义
评审标准: 内聚度 (TCC) + 耦合度 (Ce)
```

#### Kata 2: 知识文件组织

```
场景: 你有以下知识内容需要组织到 knowledge/ 目录:
  - 10 本软件工程书籍的摘要
  - 20 个架构模式
  - 50 个评审规则
  - 30 个 Prompt 模板
  - 10 个团队运营模型

问题:
  1. 如何分类？
  2. 目录结构如何设计？
  3. 文件间如何建立关联？
  4. 如何保证引用完整性？

时间: 30 分钟
产出: 目录结构树 + 交叉引用策略
评审标准: 导航效率 + 引用完整性
```

#### Kata 3: 架构演进设计

```
场景: 当前 BOS-FS 有 6 个顺序执行的 Stage。现在需要支持:
  - 某些项目不需要所有 Stage
  - 某些 Stage 可以并行执行
  - 用户可以自定义 Stage 顺序

问题:
  1. 如何设计 DAG 数据结构？
  2. 如何定义 Stage 依赖？
  3. 如何验证 DAG 正确性（无环）？
  4. 向后兼容性如何保证？

时间: 45 分钟
产出: DAG 设计 + 迁移方案
评审标准: 正确性 + 渐进性 + 兼容性
```

### E.3 架构 Kata 运行指南

| 角色 | 职责 |
|------|------|
| 主持人 | 控制时间、引导讨论、确保所有人参与 |
| 设计者 | 提出设计方案、解释理由 |
| 挑战者 | 提出质疑、指出风险 |
| 记录者 | 记录决策、权衡、风险 |

**运行流程**:
1. 主持人宣读场景（2 分钟）
2. 个人独立思考（5 分钟）
3. 分组讨论方案（15 分钟）
4. 各组展示方案（每组 5 分钟）
5. 集体评审和讨论（10 分钟）
6. 总结关键教训（3 分钟）

---

## 附录 F: BOS-FS 运行时引擎架构指南

### F.1 引擎设计原则

| 原则 | 内容 | 实践 |
|------|------|------|
| **Stage 自治** | 每个 Stage 是独立的执行单元 | 异常隔离、独立验证 |
| **数据流透明** | Stage 间数据传递完全可见 | PipelineContext 共享数据 |
| **可追溯性** | 每次运行的完整链路可追溯 | run_id + 时间戳 + 状态日志 |
| **渐进增强** | 新能力通过扩展而非修改 | Custom Stage + Plugin Interface |
| **失败安全** | 部分失败不影响整体系统 | 状态持久化 + 断点恢复 |

### F.2 运行时扩展点

| 扩展点 | 接口 | 扩展方式 | 示例 |
|--------|------|---------|------|
| Stage 注册 | `Stage` Protocol | 实现 Protocol + 注册 | Custom Stage |
| 事件监听 | `PipelineObserver` Protocol | 实现观察者 | 日志记录、指标采集 |
| 缓存策略 | `CacheBackend` 接口 | 替换实现 | Redis 缓存替代文件缓存 |
| 配置加载 | `ConfigLoader` 接口 | 替换实现 | YAML/Env 配置 |
| 错误处理 | `ErrorHandler` 接口 | 自定义策略 | 指数退避重试 |

### F.3 引擎质量保障

| 保障机制 | 方法 | 执行频率 |
|---------|------|---------|
| 接口契约验证 | JSON Schema 校验 | 每次 Stage 执行 |
| 异常隔离 | try/except 包裹 | 每次 Stage 执行 |
| 状态一致性 | 持久化到文件 | 每次状态变更 |
| 缓存一致性 | 输入哈希作为 key | 每次缓存查找 |
| 架构适配度 | 适配度函数测试 | 每次代码变更 |

---

## 附录 G: 与其他知识文件的关联扩展

| 关联文件 | 关联点 | 使用场景 |
|---------|--------|---------|
| [architecture_quality_metrics.md](../governance/architecture_quality_metrics.md) | 架构特征的质量度量 | 用指标验证架构特征是否满足 |
| [flow_metrics.md](../adoption/flow_metrics.md) | 架构决策对 Flow 的影响 | DAG Pipeline 如何影响 Flow Velocity |
| [ai_delivery_framework.md](../governance/ai_delivery_framework.md) | AI 驱动的架构模式 | 运行时如何支撑 AI 生成和验证 |
| [team_topology.md](../adoption/team_topology.md) | 架构与团队边界的对齐 | 微内核的插件边界 ↔ 团队 API |
| [mlops_delivery.md](../governance/mlops_delivery.md) | 模型交付的架构考量 | 运行时如何集成 ML 模型 |
| [data_intensive_patterns.md](data_intensive_patterns.md) | 数据密集型架构模式 | Pipeline 处理大量数据时的模式 |