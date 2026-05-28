---
name: book-knowledge-ingestor
description: 需要摄入产品管理类书籍时，将书籍解析、提取并映射到 BOS-FS 知识体系五层架构。
---

# Book Knowledge Ingestor
**version**: 0.2.11
> Context: [base_context](../../knowledge/base_context.md)
> Full version: skills/book-knowledge-ingestor/SKILL.md

## Role
将产品管理类书籍(txt格式)解析、提取、映射至 BOS-FS 五层架构(intent/runtime/execution/governance/adoption)。

## Input/Validation
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| book_path | string | ✓ | txt绝对路径 |
| output_dir | string | ✗ | 默认 `knowledge/` |
**校验**: `.txt`格式 | ≤50MB | 含章节标记 | UTF-8/GBK

## 3-Phase Pipeline
### Phase 1: Chapter Splitting
| 优先级 | 模式 |
|--------|------|
| 1 | TABLE OF CONTENTS块 | 2 | Chapter N / Chapter N: Title | 3 | PART N: Title | 4 | 目录缩进行(连续3+行) |
**规则**: 最高优先级为边界；前言/致谢→`knowledge/runtime/<book>_preface.md`

### Phase 2: Chapter Extraction
| 维度 | 标识词 | 输出 |
|------|--------|------|
| core_concepts | key idea, principle, 核心概念 | bullets |
| methodologies | methodology, approach, 方法论 | numbered |
| actionable_steps | action item, 行动项 | checklist |
| key_metrics | metric, KPI, 关键指标 | table |
**规则**: 每章≤30行 | 每维度≤5条 | 来源标注 `[<book>: Ch<N>]` | 跨章去重(首次为准)

### Phase 3: Knowledge Mapping
| BOS-FS层 | 内容 | 路径 |
|----------|------|------|
| intent | 愿景/画像/问题 | `knowledge/intent/` |
| runtime | 工作流/节奏/习惯 | `knowledge/runtime/` |
| execution | 模板/SOP/清单 | `knowledge/execution/` |
| governance | 度量/规则/标准 | `knowledge/governance/` |
| adoption | 策略/差异化/推广 | `knowledge/adoption/` |
**决策**: 用户/价值→intent | 流程/习惯→runtime | 模板/SOP→execution | 度量/标准→governance | 推广→adoption

## Output Format
```markdown
# <Topic>
> Source: <book>: Ch<N> | Layer: <layer>
## Core Concepts / Methodology / Actionable Steps / Key Metrics
## BOS-FS Context — Related + Applies to
```

## Density Control
| 规则 | 约束 |
|------|------|
| 单章上限 | ≤30行 |
| 优先级 | core_concepts > methodologies > actionable_steps > key_metrics |
| 冗余检测 | 余弦相似度>80%仅保留最完整版 |
| 去重 | 首次为准，后续仅补差异化 |
| 每维度 | ≤5条 |

## Error Handling
| 错误 | 处理 |
|------|------|
| 文件不存在 | `FileNotFoundError: <path>` |
| 无章节标记 | 整书单章处理 |
| 空章节 | 跳过+日志 |
| 编码错误 | UTF-8→GBK→Latin-1 |
| 映射失败 | →`knowledge/runtime/unmapped.md` |

## Anti-Patterns
| 反模式 | 后果 |
|--------|------|
| 单章>30行 | 违反密度规则 |
| 跨章未去重 | 知识库膨胀 |
| 跳过Phase 1 | 边界丢失 |
| 原文直接复制 | 未结构化 |
| 同概念映射多层 | 体系混乱 |

## Edge Cases
| 场景 | 处理 |
|------|------|
| 无章节且<1000字符 | →`knowledge/runtime/<book>_single.md` |
| 单章>50000字符 | 子主题二次拆分 |
| 概念相似度>80% | 保留首次，后续标`"see: <路径>"` |
| 含代码/公式 | 代码保留，公式转MD或标`[公式]` |
| 非中/英文 | 标注语言，质量可能降级 |

## Quality Gates
- [ ] 每章提取≤30行？
- [ ] 相似度>80%冗余已合并/交叉引用？
- [ ] 每条目含正确来源标注 `[<book>: Ch<N>]`？
- [ ] 五层映射每层≤3主题文件？
- [ ] 所有输出可正确Markdown渲染？

## 方法论来源
| 启发来源 | 核心贡献 |
|----------|----------|
| NEED-PACK 全部10本书籍 | 知识提取与映射体系基础 |
