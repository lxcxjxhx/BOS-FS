---
name: submission-builder
description: 准备提交时构建项目提交包，包含 README、演示指南、FAQ、风险披露等标准化组件。
---

# Submission Builder
**version**: 0.3.0
> Context: [base_context](../knowledge/base_context.md)
> Flexibility: [flexibility_principles](../knowledge/flexibility_principles.md)

## Role
构建项目提交包。

## 组件分层 (TIERED)

### 核心组件 (MUST) — 不可省略
| 文件 | 内容 |
|------|------|
| README.md | What/Why/How/Result/Next |
| bundle_meta.json | 项目元数据+goal+状态 |

### 推荐组件 (SHOULD) — 建议保留
| 文件 | 内容 |
|------|------|
| demo_guide.md | 安装→配置→运行→验证 |
| introduction.md | 一句话价值+问题+方案+差异化+指标 |
| FAQ.md | 10个典型问答 |

### 可选组件 (MAY) — 按需选择
| 文件 | 内容 |
|------|------|
| screenshots_guide.md | 截图规范+关键界面 |
| risk_disclosure.md | 技术/市场/合规风险 |
| trust_statement.md | 技术/商业/工程可信度声明（权威引用） |

## 模式选择 (Mode Selection)

| 模式 | 组件 | 适用场景 |
|------|------|----------|
| **精简模式 (Lite)** | 2个核心组件 | 个人项目/MVP/快速原型 |
| **标准模式 (Standard)** | 2核心 + 3推荐 = 5个组件 | 常规项目 |
| **完整模式 (Full)** (默认) | 全部8个组件 | 商业发布/客户交付 |
| **自定义模式 (Custom)** | 用户指定组件列表 | 特殊需求 |

> **默认模式**: 完整模式 (Full) — 向后兼容

## Input/Output
输入: `{persona, problem, solution, outcome, readme, mode?}`
输出: 根据所选模式生成对应的组件文件列表

## Input Validation
- 必需: name, version, description
- 可选: readme, outcome, persona, problem, mode
- 缺失必需字段 → 输出错误: {status: "error", message: "缺少必需字段"}
- 无 readme → 生成简化版
- 无 mode → 使用默认模式(完整模式)

## Error Handling
- 输入为空/缺失 → 输出错误信息并说明需要补充
- 字段缺失 → 标注"未明确"
- 矛盾信息 → 取最新/最主要的

## Component Templates

### demo_guide.md
```markdown
# 演示指南
## 前置条件 - [环境/依赖]
## 安装 - [步骤]
## 配置 - [配置示例含注释]
## 运行 - [启动命令]
## 验证 - [功能→预期结果]
```

### introduction.md
```markdown
# 项目Pitch
## 一句话 [15字内价值]
## 问题 [谁+什么问题+多大影响]
## 方案 [关键创新]
## 差异化 [与竞品2-3点区别]
## 指标 [量化收益]
## 路线图 [近期/中期/远期]
```

### FAQ.md — 覆盖：问题定义、竞品差异、使用方法、技术基础、扩展性、数据存储、安全性、性能、二次开发、规划。每答2-4句。

### risk_disclosure.md — 三张表：技术/市场/合规，格式：风险名 | 描述 | 影响(高/中/低) | 缓解措施。

### trust_statement.md
```markdown
# 信任声明

## 技术可信度
- [ ] 基于 [权威框架名] 设计，参见 [来源链接]
- [ ] 采用 [标准/规范]，符合 [具体条款]

## 商业可信度
- [ ] 对标 [成功模式/行业标准]
- [ ] 市场验证：[数据/引用]

## 工程可信度
- [ ] 遵循 [工程实践标准]（如 Clean Code / SOLID / TDD）
- [ ] 代码质量：[测试覆盖率/静态分析结果]

## 引用清单
| 引用来源 | 版本 | 关联内容 | 验证方式 |
|----------|------|----------|----------|
| [权威引用1] | [版本] | [与项目的关联] | [如何验证] |
```

### bundle_meta.json
```json
{"project_name":"","version":"1.0.0","build_date":"","components":[],"goal":{"persona":"","problem":"","solution":"","outcome":""},"status":"complete"}
```

## Consistency
- 项目名/版本号全局一致
- 价值主张统一
- 指标真实可验证
- 风险说明（如启用）不可省略

## Output
本 Skill 生成指定组件的**实际文件内容**（非仅路径）：

| 文件 | 内容 | 分层 |
|------|------|------|
| README.md | What/Why/How/Result/Next 五段式文档 | MUST |
| demo_guide.md | 安装→配置→运行→验证 演示指南 | SHOULD |
| introduction.md | 一句话价值+问题+方案+差异化+指标 | SHOULD |
| screenshots_guide.md | 截图规范+关键界面说明 | MAY |
| FAQ.md | 10个典型问答（每答2-4句） | SHOULD |
| risk_disclosure.md | 技术/市场/合规风险三张表 | MAY |
| trust_statement.md | 技术/商业/工程可信度声明 | MAY |
| bundle_meta.json | 项目元数据+goal+状态 | MUST |

```json
{"bundle_path":"submission_bundle/","components":["README.md","demo_guide.md","introduction.md","screenshots_guide.md","FAQ.md","risk_disclosure.md","trust_statement.md","bundle_meta.json"],"mode":"full","status":"complete"}
```

## Output Schema

### JSON Schema Definition
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "bundle_path": {
      "type": "string",
      "minLength": 1,
      "description": "提交包根目录路径"
    },
    "components": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "README.md",
          "demo_guide.md",
          "introduction.md",
          "screenshots_guide.md",
          "FAQ.md",
          "risk_disclosure.md",
          "trust_statement.md",
          "bundle_meta.json"
        ]
      },
      "minItems": 1,
      "uniqueItems": true,
      "description": "生成的组件文件列表"
    },
    "mode": {
      "type": "string",
      "enum": ["lite", "standard", "full", "custom"],
      "description": "构建模式：精简/标准/完整/自定义"
    },
    "status": {
      "type": "string",
      "enum": ["complete", "partial", "error"],
      "description": "构建状态"
    }
  },
  "required": ["bundle_path", "components", "status"],
  "additionalProperties": false
}
```

### 字段类型说明
| 字段 | 类型 | 必填 | 取值范围 | 说明 |
|------|------|------|----------|------|
| bundle_path | string | ✅ | 非空路径字符串 | 提交包根目录路径 |
| components | array | ✅ | 预定义文件名集合 | 实际生成的组件文件列表，不可重复 |
| mode | string | ❌ | lite / standard / full / custom | 构建模式，默认full |
| status | string | ✅ | complete / partial / error | `complete`=全部生成；`partial`=部分生成；`error`=构建失败 |

### 验证规则
- **格式约束**: 输出必须为单行纯JSON，不得包含换行符、代码块标记或额外文本
- **components 枚举约束**: 数组中每个元素必须是预定义的8个文件名之一
- **components 唯一性**: 数组元素不可重复（`uniqueItems: true`）
- **components 非空**: 至少包含1个组件（`minItems: 1`）
- **mode 与 components 一致性**: lite模式必须包含2个核心组件；standard模式必须包含5个核心+推荐组件；full模式必须包含全部8个组件；custom模式可由用户指定（但核心组件始终必须包含）
- **status 枚举约束**: 仅允许 `"complete"`, `"partial"`, `"error"` 三种状态值
- **必填字段**: `bundle_path`, `components`, `status` 缺一不可
- **禁止额外字段**: 不允许出现schema定义之外的字段

## Anti-Patterns
| 反模式 | 后果 |
|--------|------|
| 缺少risk_disclosure.md（完整模式下） | 评审信任度降低，investment类评审直接扣分 |
| 各文档项目名称/版本号不一致 | 评审视为工程不规范，trust评分下降 |
| FAQ回答过于笼统（>5句/答） | 降低可读性，评审认为掩盖问题 |
| trust_statement.md引用不可验证来源 | 触发反谄媚检查，信任度评估降级 |
| bundle_meta.json中components列表与实际生成文件不匹配 | 提交包验证失败，status必须标记为partial |
| 核心组件（README.md/bundle_meta.json）缺失 | 提交包不完整，status=error |

## Edge Cases
| 边界场景 | 处理方式 |
|----------|----------|
| 输入仅有name/version，无problem/solution | 生成最小提交包，缺失内容标注"待补充"，status=partial |
| 输入README内容>50000字符 | 精简提取核心章节，保留What/Why/How/Result/Next |
| 输入无readme内容 | 使用README模板生成简化版README |
| 输入描述超长（>500字符） | 截断核心信息并标注"truncated"，保留完整原文于bundle_meta |
| persona与outcome矛盾（如"个人工具"vs"企业级SLA"） | 以problem为准，矛盾标注于bundle_meta.json的"warnings"字段 |
| 风险披露无可识别风险 | 仍生成risk_disclosure.md，填写"暂无已知重大风险"并说明假设条件 |
| 输入含敏感信息（密钥/内部地址） | 自动替换为`<REDACTED>`并在bundle_meta.json中标注`"sanitized":true` |
| 多语言项目输入 | 以英文为主生成，中文为辅助语言，在bundle_meta.json中标注`"languages":["en","zh"]` |

## Quality Gates — 提交包完整性自检清单

### 精简模式 (Lite) — 检查2项
1. ✅ README.md — 包含What/Why/How/Result/Next五要素？
2. ✅ bundle_meta.json — 元数据完整且components列表一致？

### 标准模式 (Standard) — 检查5项
1. ✅ README.md — 包含What/Why/How/Result/Next五要素？
2. ✅ bundle_meta.json — 元数据完整且components列表一致？
3. ✅ demo_guide.md — 包含安装→配置→运行→验证完整流程？
4. ✅ introduction.md — 一句话价值主张≤15字？
5. ✅ FAQ.md — 包含≥10个典型问答，每答2-4句？

### 完整模式 (Full) — 检查8项
1. ✅ README.md — 包含What/Why/How/Result/Next五要素？
2. ✅ bundle_meta.json — 元数据完整且components列表一致？
3. ✅ demo_guide.md — 包含安装→配置→运行→验证完整流程？
4. ✅ introduction.md — 一句话价值主张≤15字？
5. ✅ screenshots_guide.md — 列出≥3个关键界面截图说明？
6. ✅ FAQ.md — 包含≥10个典型问答，每答2-4句？
7. ✅ risk_disclosure.md — 技术/市场/合规三类风险各≥1条？
8. ✅ trust_statement.md — 含权威引用且引用可验证？

### 自定义模式 (Custom) — 按用户指定组件检查

## 自检规则
- 精简模式: 2项全部完成 → status=complete；1项完成 → status=partial；0项 → status=error
- 标准模式: 5项中≥4项完成 → status=complete；5项中2-3项完成 → status=partial；5项中<2项完成 → status=error
- 完整模式: 8项中≥6项完成 → status=complete；8项中3-5项完成 → status=partial；8项中<3项完成 → status=error
- 自定义模式: 按指定组件数量比例计算（≥80%完成=complete，40-79%=partial，<40%=error）

## 方法论来源与学术诚信

本 Skill 的方法论来源于**作者亲自阅读以下书籍并提炼核心要点**，非 AI 自动处理或简单摘要。

| 启发来源 | 核心贡献 |
|----------|----------|
| [Engineering MLOps](Emmanuel Raj) | 交付流水线标准化 |
| [Fundamentals of Software Architecture](Richards & Ford) | 架构文档规范 |

> **声明**: 本 Skill 中的方法论启发自上述书籍（见表格），所有代码实现、示例和知识重构均为作者原创。建议读者支持正版，购买原书以获得更完整的论述和案例。
