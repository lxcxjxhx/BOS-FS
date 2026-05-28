# BOS-FS Skills Mini (Token-Saver)

高压缩版 SKILL 文档，token 消耗降低 30-70%，核心规则/约束/输出格式 100% 保留。

## 与主版本差异

| 对比项 | skills/ (主版本) | skills-mini/ (压缩版) |
|--------|-----------------|---------------------|
| Token 消耗 | 100% | 30-70% |
| 示例详细度 | 完整示例 | 精简/外部引用 |
| 学术声明 | 完整内容 | 引用主版本 |
| Schema 格式 | 多行/详细 | 紧凑多行 |
| 适用场景 | 首次学习/审计 | 日常加载/低 token 环境 |

## 加载方式

### Cursor
```
@skills-mini/goal-refiner.md
@skills-mini/reviewer-simulator.md
@skills-mini/readme-refactor.md
@skills-mini/outcome-mapper.md
@skills-mini/submission-builder.md
@skills-mini/reject-analyzer.md
@skills-mini/book-knowledge-ingestor.md
@skills-mini/bos-fs-pipeline.md
```

### Trae
```
/skill bos-fs-mini/pipeline
```

### 通用
直接加载对应 `.md` 文件，路径为 `skills-mini/<skill-name>.md`。

## 文件清单

| 文件 | 压缩率 | 核心功能 |
|------|--------|---------|
| goal-refiner.md | ~40% | 四字段意图提炼 |
| reviewer-simulator.md | ~30% | 五类评审+反谄媚+敌对模式 |
| readme-refactor.md | ~57% | README 重构 |
| outcome-mapper.md | ~54% | 价值转换 |
| submission-builder.md | ~54% | 提交包构建 |
| reject-analyzer.md | ~43% | 20模式拒绝分析 |
| book-knowledge-ingestor.md | ~51% | 书籍知识摄取 |
| bos-fs-pipeline.md | ~62% | 流水线编排 |

## 版本
- **当前版本**: 0.2.11
- **主版本**: skills/manifest.json
- **完整文档**: 见 `skills/` 目录

> 压缩版适用于日常开发加载。如需完整示例/学术声明/详细评分说明，请参考主版本 `skills/` 目录。
