---
name: submission-builder
description: 准备提交时构建完整的项目提交包，包含 README、演示指南、FAQ、风险披露等标准化组件。
---

# Submission Builder
**version**: 0.2.11
> Context: [base_context](../../knowledge/base_context.md)
> Full version: skills/submission-builder/SKILL.md

## Role
构建完整项目提交包。

## Input/Output
**输入**: `{persona, problem, solution, outcome, readme}`
**必需**: name, version, description（缺失→`{status:"error", message:"缺少必需字段"}`）

| 组件 | 内容 |
|------|------|
| README.md | What/Why/How/Result/Next |
| demo_guide.md | 安装→配置→运行→验证 |
| introduction.md | 一句话价值+问题+方案+差异化+指标 |
| screenshots_guide.md | 截图规范+关键界面 |
| FAQ.md | 10个典型问答（每答2-4句） |
| risk_disclosure.md | 技术/市场/合规风险三张表 |
| trust_statement.md | 技术/商业/工程可信度声明 |
| bundle_meta.json | 项目元数据+goal+状态 |

**Output JSON**:
```json
{"bundle_path":"submission_bundle/","components":["README.md","demo_guide.md","introduction.md","screenshots_guide.md","FAQ.md","risk_disclosure.md","trust_statement.md","bundle_meta.json"],"status":"complete|partial|error"}
```

### Output Schema
| 字段 | 类型 | 必填 | 取值 | 说明 |
|------|------|------|------|------|
| bundle_path | string | ✅ | 非空路径 | 提交包根目录 |
| components | array | ✅ | 8个预定义名 | 生成组件列表，不重复 |
| status | string | ✅ | complete/partial/error | 构建状态 |

### 验证规则
| 规则 | 约束 |
|------|------|
| 格式 | 单行纯JSON，无代码块/额外文本 |
| components枚举 | 必须是预定义的8个文件名之一 |
| components唯一性 | 不可重复 |
| status枚举 | 仅 complete/partial/error |

## Component Templates (Compact)
| 组件 | 结构 |
|------|------|
| demo_guide.md | 前置条件→安装→配置(含注释)→运行→验证(功能→预期结果) |
| introduction.md | 一句话(≤15字)→问题(谁+什么+多大)→方案(创新)→差异化(2-3点)→指标→路线图 |
| FAQ.md | 10问答覆盖：定义/竞品/使用/技术/扩展/数据/安全/性能/二次开发/规划，每答2-4句 |
| risk_disclosure.md | 三张表(技术/市场/合规)：风险名|描述|影响(高/中/低)|缓解措施 |
| trust_statement.md | 技术可信度(框架/规范)→商业可信度(模式/验证)→工程可信度(实践/质量)→引用清单 |
| bundle_meta.json | `{"project_name":"","version":"1.0.0","build_date":"","components":[],"goal":{"persona":"","problem":"","solution":"","outcome":""},"status":""}` |

## Consistency
项目名/版本号全局一致 | 价值主张统一 | 指标真实可验证 | 风险说明不可省略

## Self-Check Rules
| 完成项 | status | 动作 |
|--------|--------|------|
| ≥6/8 | complete | 正常输出 |
| 3-5/8 | partial | 标注缺失项 |
| <3/8 | error | 输出错误 |

## Anti-Patterns
| 反模式 | 后果 |
|--------|------|
| 缺少 risk_disclosure.md | 评审信任度降低 |
| 项目名/版本号不一致 | 工程不规范评分下降 |
| FAQ 回答>5句/答 | 评审认为掩盖问题 |
| trust_statement 引用不可验证 | 触发反谄媚降级 |
| bundle_meta components 与实际不匹配 | status 必须标记 partial |

## Edge Cases
| 场景 | 处理 |
|------|------|
| 仅有 name/version | 最小提交包，标注"待补充"，status=partial |
| README>50000字符 | 精简提取核心五段式 |
| 无可识别风险 | 仍生成 risk_disclosure，填"暂无已知重大风险"+假设条件 |
| 含敏感信息 | 替换为 `<REDACTED>`，meta 标注 `"sanitized":true` |
| 多语言项目 | 英文为主+中文辅助，meta 标注 `"languages":["en","zh"]` |

## Quality Gates
- [ ] README.md — What/Why/How/Result/Next 五要素？
- [ ] demo_guide.md — 安装→配置→运行→验证完整流程？
- [ ] introduction.md — 一句话≤15字？
- [ ] screenshots_guide.md — ≥3个关键界面截图说明？
- [ ] FAQ.md — ≥10个问答，每答2-4句？
- [ ] risk_disclosure.md — 技术/市场/合规各≥1条？
- [ ] trust_statement.md — 权威引用且可验证？
- [ ] bundle_meta.json — components 列表与实际生成数量一致（8项）？

## 方法论来源
| 启发来源 | 核心贡献 |
|----------|----------|
| [Engineering MLOps](Emmanuel Raj) | 交付流水线标准化 |
| [Fundamentals of Software Architecture](Richards & Ford) | 架构文档规范 |
