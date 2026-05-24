---
name: book-knowledge-ingestor
description: 需要摄入产品管理类书籍时，将书籍解析、提取并映射到 BOS-FS 知识体系五层架构。
---

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

## Anti-Patterns
| 反模式 | 后果 |
|--------|------|
| 单章节提取超过30行 | 触发密度控制规则：自动截断至30行，保留高优先级条目 |
| 跨章节概念未去重 | 知识库膨胀，降低检索准确性 |
| 跳过Phase 1直接做Phase 2 | 章节边界丢失，来源标注不准确 |
| 将书籍原文直接复制为知识条目 | 未做提取和映射，违反知识结构化原则 |
| 同一概念映射到多个BOS-FS层 | 导致知识体系混乱，应选最匹配的单一层 |

## Edge Cases
| 边界场景 | 处理方式 |
|----------|----------|
| 书籍无章节标记且<1000字符 | 整体视为单条知识，归入`knowledge/runtime/<book>_single.md` |
| 单章节内容>50000字符 | 按子主题二次拆分后分别提取映射 |
| 同一概念在不同章节相似度>80% | 触发冗余检测：仅保留首次出现最完整的版本，后续标注`"see: <首次出现路径>"` |
| 书籍包含代码示例/公式 | 代码块保留原始格式，公式转为Markdown兼容格式或标注`[公式]` |
| 书籍语言非中文/英文 | 标注`"language":"<语言>"`，知识映射质量可能降级 |

## Quality Gates
输出前自检：
1. 每个章节提取的总行数是否≤30行（不含标题和分隔线）？
2. 是否存在相似度>80%的冗余条目？如有是否已合并或交叉引用？
3. 每个知识条目是否包含正确的来源标注`[<book_name>: Chapter <N>]`？
4. BOS-FS五层映射是否每层最多3个主题文件（避免单层过载）？
5. 所有输出文件是否均可通过Markdown语法正确渲染（无断链/空表）？

## 知识提取密度控制规则
- **单章节上限**: 提取内容≤30行（含Core Concepts/Methodology/Actionable Steps/Key Metrics）
- **优先级排序**: core_concepts > methodologies > actionable_steps > key_metrics（行数不足时优先保留高优先级维度）
- **冗余检测**: 跨章节条目计算余弦相似度，>80%视为冗余，仅保留信息量最大的版本
- **去重策略**: 同名概念以首次出现为准，后续出现仅补充差异化内容

## 实时知识摄取管道

### 管道概述
book_knowledge_ingestor 提供完整的实时知识摄取能力，使 BOS-FS 能够快速纳入新发布的产品/工程书籍。

```
新书(.txt)
  ↓
Phase 1: 章节划分（自动识别目录/章节标记）
  ↓
Phase 2: 逐章提取（核心概念/方法论/行动项/指标，≤30行/章）
  ↓
Phase 3: 五层映射（intent/runtime/execution/governance/adoption）
  ↓
Phase 4: 增量更新（检测已有文件，仅更新变化部分）
  ↓
Phase 5: 版本标记（记录书籍版本和摄取时间）
  ↓
knowledge/<layer>/<topic>.md
```

### CLI 命令
| 命令 | 用途 | 示例 |
|------|------|------|
| `ingest` | 单本书摄取 | `python -m engine.core.07_knowledge_ingestor.book_ingestor ingest "book.txt"` |
| `batch` | 批量摄取+去重+报告 | `python -m engine.core.07_knowledge_ingestor.book_ingestor batch "book1.txt" "book2.txt" -s summary.md` |
| `ingest --incremental` | 增量更新（仅更新变化章节） | `python -m engine.core.07_knowledge_ingestor.book_ingestor ingest "book.txt" --incremental` |

### 实时跟进流程
1. **获取新书**：将 txt 格式书籍放入 `NEED-PACK/<n>/` 目录
2. **运行摄取**：执行 `ingest` 或 `batch` 命令
3. **审查报告**：检查生成的摄取摘要，确认知识文件已正确生成
4. **知识合并**：如已有同名知识文件，增量更新模式会保留原有内容并追加新章节提炼
5. **提交更新**：将新的/更新的知识文件提交到 `knowledge/` 目录

## 增量更新机制

### 检测逻辑
- 对每个输出路径 `knowledge/<layer>/<topic>.md`，检查文件是否已存在
- 如存在，读取文件末尾的 `> Ingested: <timestamp>` 元数据
- 比较书籍文件的修改时间与上次摄取时间
- 仅当书籍有更新时，才重新提取并追加内容

### 追加策略
- 增量更新在知识文件末尾追加 `## 新增章节提炼（摄取时间: <timestamp>）` 区块
- 不覆盖已有内容，确保历史知识不丢失
- 如新旧内容相似度 >80%，跳过该章节（避免重复）

### 回滚机制
- 每次增量更新前自动备份原文件至 `knowledge/.backup/<topic>.md.bak`
- 如更新后文件异常（语法错误/空文件），自动恢复备份

## 版本管理

### 摄取元数据
每个知识文件末尾包含摄取元数据：
```markdown
---
> Ingested: 2026-05-24T10:30:00
> Source Book: Continuous Discovery Habits (Teresa Torres)
> Source Path: NEED-PACK/3/01 - Continuous Discovery Habits.txt
> Book Version: 1st Edition
> Chapters Processed: 12
> Knowledge Files Generated: 5
> Ingestor Version: BOS-FS v0.2.0
---
```

### 版本兼容性
- 摄取元数据格式向后兼容，旧格式文件可正常读取
- 新版本摄取引擎可读取旧版本生成的知识文件
- 批次摄取报告包含每本书的摄取状态（success/error/skipped）

### 知识版本追踪
- `knowledge/` 目录下可运行 `python -m engine.core.07_knowledge_ingestor.book_ingestor status` 查看所有知识文件的摄取状态
- 输出包含：最后摄取时间、来源书籍、处理章节数

## 方法论来源与学术诚信

本 Skill 的方法论来源于**作者亲自阅读以下书籍并提炼核心要点**，非 AI 自动处理或简单摘要。

| 启发来源 | 核心贡献 |
|----------|----------|
| NEED-PACK 全部 10 本书籍 | 知识提取与映射体系的基础 |

> **声明**: 本 Skill 中的方法论启发自上述书籍（见表格），所有代码实现、示例和知识重构均为作者原创。建议读者支持正版，购买原书以获得更完整的论述和案例。
