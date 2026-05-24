# Book Knowledge Ingestor
> Context: [base_context](../knowledge/base_context.md)

## Role
将产品管理类书籍(txt格式)解析、提取、映射至 BOS-FS 知识体系五层架构(intent/runtime/execution/governance/adoption)。

## Input Schema
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| book_path | string | ✓ | 待导入书籍的txt文件绝对路径 |
| output_dir | string | ✗ | 知识输出目录，默认 `knowledge/` |

### Input Validation
- 文件必须为 `.txt` 格式
- 文件大小 ≤ 50MB
- 文件必须包含可识别的目录或章节标记
- 编码: UTF-8 或 GBK

## Phase 1: Chapter Splitting

### 识别模式(Priority Order)
| 优先级 | 模式 | 正则 |
|--------|------|------|
| 1 | TABLE OF CONTENTS 块 | `TABLE OF CONTENTS[\s\S]*?(?=\n\n[A-Z])` |
| 2 | Chapter N / Chapter N: Title | `Chapter\s+(?:One|Two|Three|\d+)[.:]?\s*.+` |
| 3 | PART N: Title | `PART\s+(?:One|Two|Three|\d+)[.:]?\s*.+` |
| 4 | 目录缩进行 | `^\s+\d+\.\s+.+$` (连续3+行) |

### 分割规则
- 以最高优先级匹配到的模式为章节边界
- 章节内容从当前章节标记开始，至下一章节标记前一行
- 前言/致谢等非章节内容归入 `knowledge/runtime/<book>_preface.md`

## Phase 2: Chapter Extraction

### 提取维度
| 维度 | 标识词 | 输出格式 |
|------|--------|----------|
| core_concepts | key idea, principle, framework, concept, 核心概念 | bullet list |
| methodologies | methodology, approach, process, step-by-step, 方法论 | numbered steps |
| actionable_steps | action item, do this, practice, 行动项 | checklist |
| key_metrics | metric, measure, KPI, indicator, 关键指标 | table: metric \| definition \| target |

### 提取规则
- 每个维度最多提取5条，避免信息过载
- 标注来源: `[<book_name>: Chapter <N>]`
- 去重: 跨章节相同概念仅保留首次出现

## Phase 3: Knowledge Mapping

### BOS-FS 五层映射
| BOS-FS 层 | 映射内容 | 输出路径 |
|-----------|----------|----------|
| **intent** | 产品愿景、用户画像、问题定义 | `knowledge/intent/<topic>.md` |
| **runtime** | 工作流、节奏、循环、习惯 | `knowledge/runtime/<topic>.md` |
| **execution** | 执行模板、SOP、检查清单 | `knowledge/execution/<topic>.md` |
| **governance** | 度量框架、评审规则、质量标准 | `knowledge/governance/<topic>.md` |
| **adoption** | 采纳策略、差异化定位、推广方法 | `knowledge/adoption/<topic>.md` |

### 映射决策树
```
content_type?
├── 用户/价值/目标 → intent
├── 流程/节奏/习惯 → runtime
├── 模板/SOP/步骤 → execution
├── 度量/规则/标准 → governance
└── 推广/差异化/采纳 → adoption
```

## Output Schema

### 输出格式: `knowledge/<layer>/<topic>.md`
```markdown
# <Topic Title>
> Source: <book_name>: Chapter <N>
> Layer: <intent|runtime|execution|governance|adoption>

## Core Concepts
- <concept_1>
- <concept_2>

## Methodology
1. <step_1>
2. <step_2>

## Actionable Steps
- [ ] <action_1>
- [ ] <action_2>

## Key Metrics
| Metric | Definition | Target |
|--------|------------|--------|
| <m1> | <d1> | <t1> |

## BOS-FS Context
- Related: [<related_topic>](./<related>.md)
- Applies to: <persona/scenario>
```

## Example Usage

### NEED-PACK/3 示例
```
python -m engine.core.07_knowledge_ingestor.book_ingestor ingest \
  "NEED-PACK/3/01 - Continuous Discovery Habits.txt" \
  --output-dir knowledge/
```

预期输出:
- `knowledge/intent/opportunity_solution_tree.md`
- `knowledge/runtime/discovery_habits.md`
- `knowledge/execution/interview_checklist.md`
- `knowledge/governance/assumptions_testing.md`
- `knowledge/adoption/product_discovery_adoption.md`

### NEED-PACK/4 示例
```
python -m engine.core.07_knowledge_ingestor.book_ingestor ingest \
  "NEED-PACK/4/01 - Team Topologies.txt" \
  --output-dir knowledge/
```

预期输出:
- `knowledge/intent/team_first_choice.md`
- `knowledge/runtime/cognitive_load_management.md`
- `knowledge/execution/team_interaction_modes.md`
- `knowledge/governance/conway_law_metrics.md`
- `knowledge/adoption/topology_transformation.md`

## Error Handling
| 错误场景 | 处理方式 |
|----------|----------|
| 文件不存在 | 报错: `FileNotFoundError: <path>` |
| 无章节标记 | 警告: 整书作为单章处理 |
| 空章节 | 跳过，记录到日志 |
| 编码错误 | 尝试 UTF-8 → GBK → Latin-1 降级 |
| 映射失败 | 归入 `knowledge/runtime/unmapped.md` |
