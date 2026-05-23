# BOS-FS Pipeline Runtime — State Machine Specification

> Python 引擎层运行状态机。与 `skills/pipeline.md`（AI Skill 编排）正交，本文件描述 Python runtime orchestrator 的内部状态模型。

---

## 1. State Machine

### States & Transitions

```
┌──────┐
│ Idle │ ── start(pipeline_cfg) ──▶ ┌────────────┐
└──────┘                            │ Processing │
                                    └─────┬──────┘
                ┌─────────────────────────┼──────────────────────────┐
                │                         │                          │
        next_stage()                  need_input()             stage_error()
                ▼                         ▼                          ▼
        ┌─────────────┐          ┌──────────┐               ┌─────────────┐
        │  Processing │          │ Waiting  │               │ ErrorState  │
        │  (next)     │          └────┬─────┘               └─────────────┘
        └──────┬──────┘               │                          ▲
               │                      │ user_input(data)         │
               ▼                      ▼                          │
        ┌─────────────┐          ┌────────────┐                  │
        │ Processing  │──────────▶ Processing │──────────────────┘
        └──────┬──────┘           (resume)     retry() [max=3]
               │
         all_complete()
               ▼
        ┌─────────┐
        │Complete │
        └─────────┘
```

### Transition Table

| From          | Trigger              | Condition                          | To          |
|---------------|----------------------|------------------------------------|-------------|
| `Idle`        | `start(cfg)`         | cfg.stages is non-empty            | `Processing` |
| `Idle`        | `start(cfg)`         | cfg.stages is empty                | `Complete`   |
| `Processing`  | `stage.run()`        | return == `ok`                     | `Processing` |
| `Processing`  | `stage.run()`        | return == `needs_input`            | `Waiting`    |
| `Processing`  | `stage.run()`        | return == `error`                  | `ErrorState` |
| `Waiting`     | `user_input(data)`   | data passes `input_schema`         | `Processing` |
| `Waiting`     | `timeout()`          | elapsed > `cfg.timeout`            | `ErrorState` |
| `ErrorState`  | `retry()`            | attempt < `cfg.max_retries`        | `Processing` |
| `ErrorState`  | `retry()`            | attempt >= `cfg.max_retries`       | `ErrorState` |
| `Processing`  | `all_complete()`     | stage_index >= len(stages)         | `Complete`   |

---

## 2. Stage Execution Model

### Stage Interface

```python
class Stage(Protocol):
    """所有引擎 Stage 必须实现的协议。"""

    @property
    def name(self) -> str: ...
    @property
    def input_schema(self) -> dict: ...   # JSON Schema
    @property
    def output_schema(self) -> dict: ...  # JSON Schema

    def validate_input(self, data: dict) -> tuple[bool, str]:
        """返回 (valid, error_message)。"""
        ...

    def execute(self, ctx: PipelineContext) -> StageResult: ...

class StageResult(NamedTuple):
    status: Literal["ok", "needs_input", "error"]
    data: dict                      # 输出数据
    cache_key: str                  # 用于缓存/回放
    metadata: dict = field(default_factory=dict)
```

### Stage Registry

Pipeline 内置 Stage 在启动时注册：

| Stage ID | Class                | Source Module                            |
|----------|----------------------|------------------------------------------|
| `understand` | `GoalRefiner`      | `engine/core/01_intent_parser/goal_refiner.py` |
| `map`        | `OutcomeMapper`    | `engine/core/02_value_mapper/outcome_mapper.py` |
| `refactor`   | `ReadmeRefactor`   | `engine/core/03_submission_optimizer/readme_refactor.py` |
| `build`      | `SubmissionBuilder`| `engine/core/04_delivery_builder/submission_builder.py` |
| `analyze`    | `RejectAnalyzer`   | `engine/core/05_artifact_generator/reject_analyzer.py` |
| `review`     | `ReviewerSimulator`| `engine/core/06_review_simulator/reviewer_simulator.py` |

### Isolation Guarantee

- 每个 Stage 在独立 try/except 块中执行，异常不会传播到其他 Stage
- Stage 间的唯一通信通道是 `PipelineContext.shared_data`
- Stage 失败时写入 `PipelineContext.stage_results[stage_id] = {"status": "error", ...}` 后继续下一个 Stage

### Cache / Replay

- 输出按 `cache_key = hash(stage_id + input_snapshot)` 存储到 `.bosfs/cache/`
- 相同输入命中缓存时跳过 `execute()`，直接返回缓存结果
- 环境变量 `BOSFS_NO_CACHE=1` 可禁用缓存

---

## 3. Data Flow

### Inter-Stage Communication

所有 Stage 通过统一的 JSON envelope 交换数据：

```json
{
  "pipeline_run_id": "uuid",
  "stage_id": "understand",
  "timestamp": "2025-08-15T10:30:00Z",
  "input": { ... },
  "output": { ... },
  "metadata": {
    "duration_ms": 42,
    "cache_hit": false,
    "attempt": 1
  }
}
```

### PipelineContext

```python
@dataclass
class PipelineContext:
    run_id: str                       # 每次运行唯一 ID
    config: PipelineConfig
    shared_data: dict                 # Stage 间共享数据（只追加）
    stage_results: dict[str, dict]    # 已完成 Stage 的结果
    errors: list[StageError]          # 收集的错误（非致命）
    output_dir: Path                  # 输出根目录
    persist_path: Path                # .bosfs/state/<run_id>.json
```

### State Persistence

- 每次状态转换后将 `PipelineContext` 序列化到 `.bosfs/state/<run_id>.json`
- 支持断点恢复：`engine/main.py --resume <run_id>` 读取最新状态并继续
- 持久化格式与 inter-stage envelope 兼容

---

## 4. Error Handling

### Input Validation

```
Input → validate_input() → valid? → execute()
                          → invalid? → return StageResult(error)
```

- 每个 Stage 的 `input_schema` 在 `execute()` 前校验
- 校验失败返回 `StageResult(status="error")`，不抛异常

### Partial Failure Recovery

| 场景                    | 策略                        |
|------------------------|-----------------------------|
| 单个 Stage 失败         | 记录错误，继续后续 Stage     |
| 连续 Stage 失败 (>50%)  | 终止 Pipeline，返回 `ErrorState` |
| 最终产物缺失关键组件     | 标记 `status: "incomplete"`，输出已有部分 |

### Retry Logic

```python
MAX_RETRIES = 3
BACKOFF_BASE = 1.0  # seconds

def execute_with_retry(stage, ctx):
    for attempt in range(1, MAX_RETRIES + 1):
        result = stage.execute(ctx)
        if result.status != "error":
            return result
        time.sleep(BACKOFF_BASE * (2 ** (attempt - 1)))
    return StageResult(status="error", data={}, ...)
```

---

## 5. CLI Integration

### Entry Point

```bash
python engine/main.py [command] [options]
```

### Commands

| Command    | Description                    | Example                           |
|------------|--------------------------------|-----------------------------------|
| `run`      | 执行完整 Pipeline              | `python engine/main.py run --input desc.md` |
| `run-stage`| 执行单个 Stage                 | `python engine/main.py run-stage understand --input desc.md` |
| `status`   | 查看运行状态                   | `python engine/main.py status --run-id <id>` |
| `resume`   | 从断点恢复                     | `python engine/main.py resume --run-id <id>` |
| `cache`    | 管理缓存                       | `python engine/main.py cache clear` |

### Flags

| Flag              | Default     | Description                   |
|-------------------|-------------|-------------------------------|
| `--input <file>`  | (stdin)     | 输入描述文件                  |
| `--output <dir>`  | `output/`   | 输出目录                      |
| `--stages <list>` | all         | 逗号分隔的 Stage 列表         |
| `--no-cache`      | false       | 禁用缓存                      |
| `--json`          | false       | 输出 JSON 而非人类可读格式    |
| `--verbose`       | false       | 显示详细日志                  |

### Output Format

```
# 默认人类可读格式
=== Pipeline Run: <run_id> ===
[1/6] understand  ✓ (42ms)
[2/6] map         ✓ (38ms)
[3/6] refactor    ✓ (120ms)
[4/6] build       ✓ (95ms)
[5/6] review      ✓ (55ms)
[6/6] analyze     ⊘ (skipped)

Status: complete
Output: output/<run_id>/
```

```json
# --json 模式
{"run_id": "uuid", "status": "complete", "stages": [...], "artifacts": {...}}
```

---

## 6. Extensibility

### Custom Stage

实现 `Stage` 协议并注册：

```python
from bosfs.engine import Pipeline, Stage, PipelineContext, StageResult

class MyCustomStage(Stage):
    name = "my_stage"
    input_schema = {"type": "object", "properties": {"text": {"type": "string"}}}
    output_schema = {"type": "object", "properties": {"result": {"type": "string"}}}

    def execute(self, ctx: PipelineContext) -> StageResult:
        text = ctx.shared_data.get("text", "")
        return StageResult(
            status="ok",
            data={"result": text.upper()},
            cache_key=f"my_{hash(text)}",
        )

# 注册
pipeline = Pipeline()
pipeline.register_stage(MyCustomStage())
pipeline.run()
```

### Plugin Interface

Plugin 通过 entry point 自动发现：

```toml
# pyproject.toml
[project.entry-points."bosfs.plugins"]
my_plugin = "my_package:MyCustomStage"
```

Pipeline 启动时扫描 `bosfs.plugins` entry point，自动调用 `register_stage()`。

### Stage Dependency Graph

支持声明 Stage 间的依赖关系：

```python
class StageDef:
    id: str
    depends_on: list[str] = []   # 前置 Stage

# 示例：analyze 依赖 review 的结果
StageDef(id="analyze", depends_on=["review"])
```

Pipeline 根据依赖图进行拓扑排序，自动确定执行顺序。未声明依赖的 Stage 按默认顺序执行。
