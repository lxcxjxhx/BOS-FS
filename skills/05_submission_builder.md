# Submission Builder Skill

## Purpose
构建完整的项目提交包。

## Activation
当需要准备提交材料、发布项目时激活。

## Input
项目信息：{persona, problem, solution, outcome, readme}

## Output Structure
```
submission_bundle/
├── README.md          # 重构后的项目说明
├── demo_guide.md      # 演示指南
├── introduction.md    # 项目介绍（Pitch）
├── screenshots_guide.md # 截图说明
├── FAQ.md            # 常见问题
├── risk_disclosure.md # 风险说明
└── bundle_meta.json  # 提交包元数据
```

## Component Templates

### README.md
使用 README Refactor 的输出，严格遵循以下结构：
```markdown
# 项目名称

## What
一句话描述项目做什么。

## Why
为什么需要这个项目？解决什么痛点？

## How
核心架构或技术方案概述（不超过 3 段）。

## Result
已实现的功能与可量化指标。

## Next
下一步规划（近期/中期/远期）。
```

### demo_guide.md
```markdown
# 演示指南

## 前置条件
- [运行环境要求，如 Node.js >= 18, Python >= 3.10]
- [依赖项，如数据库、外部 API]
- [硬件/网络要求（如适用）]

## 安装
```bash
[安装步骤，按顺序列出]
```

## 配置
```yaml
# 配置示例（含关键参数注释）
[配置内容]
```

## 运行
```bash
[启动命令，含后台/前台模式说明]
```

## 验证
- [ ] 功能 1：[描述] → 预期结果
- [ ] 功能 2：[描述] → 预期结果
- [ ] 功能 3：[描述] → 预期结果
```

### introduction.md (Pitch)
```markdown
# 项目 Pitch

## 一句话
[一句话价值主张，15 字以内]

## 问题
[3 句话描述痛点：谁、什么问题、多大影响]

## 方案
[我们如何解决，突出关键创新点]

## 差异化
[与现有方案的具体区别，2-3 点]

## 指标
[可量化收益：效率提升 X%、成本降低 Y% 等]

## 路线图
- **近期**（1-3 月）：[可交付项]
- **中期**（3-6 月）：[可交付项]
- **远期**（6-12 月）：[可交付项]
```

### screenshots_guide.md
```markdown
# 截图说明

## 截图规范
- 分辨率：1920x1080 或 1280x720
- 格式：PNG
- 命名：screen_01_[模块名].png

## 关键界面清单
| 编号 | 界面 | 标注要点 |
|------|------|---------|
| 01 | [主界面] | [核心功能区域标注] |
| 02 | [配置页] | [关键参数标注] |
| 03 | [结果页] | [输出效果标注] |

## 标注要求
- 使用红色箭头/方框标注重点
- 每个截图附 1-2 句说明文字
```

### FAQ.md
覆盖以下典型问题（根据项目实际调整）：
1. 这个项目解决什么问题？
2. 与 [竞品/替代方案] 有什么区别？
3. 如何开始使用？
4. 需要哪些技术基础？
5. 是否支持 [常见需求]？
6. 数据如何存储/处理？
7. 安全性如何保障？
8. 性能表现如何？
9. 是否支持扩展/二次开发？
10. 未来规划是什么？

每个问题回答结构：
- **Q**: 问题
- **A**: 回答（2-4 句，含示例或链接）

### risk_disclosure.md
```markdown
# 风险说明

## 技术风险
| 风险 | 描述 | 影响等级 | 缓解措施 |
|------|------|---------|---------|
| [风险1] | [描述] | 高/中/低 | [具体措施] |

## 市场风险
| 风险 | 描述 | 影响等级 | 缓解措施 |
|------|------|---------|---------|
| [风险1] | [描述] | 高/中/低 | [具体措施] |

## 合规风险
| 风险 | 描述 | 影响等级 | 缓解措施 |
|------|------|---------|---------|
| [风险1] | [描述] | 高/中/低 | [具体措施] |

## 声明
本项目已进行风险评估，上述措施已纳入开发计划。
```

### bundle_meta.json
```json
{
  "project_name": "",
  "version": "1.0.0",
  "build_date": "",
  "components": [],
  "goal": {
    "persona": "",
    "problem": "",
    "solution": "",
    "outcome": ""
  },
  "status": "complete"
}
```

## Consistency Rules
- 所有组件中的项目名称、版本号必须一致
- 价值主张在所有文件中保持统一表述
- 数据/指标必须真实可验证，不可虚构
- 风险说明不可省略，必须覆盖技术/市场/合规三类
- 每个组件必须独立可读，不依赖其他文件上下文

## Output Format
```json
{
  "bundle_path": "submission_bundle/",
  "components": ["README.md", "demo_guide.md", "introduction.md", "screenshots_guide.md", "FAQ.md", "risk_disclosure.md", "bundle_meta.json"],
  "status": "complete"
}
```

## Rules
- 每个组件必须独立可读
- 信息保持一致性
- 风险说明不可省略
- 自动生成 bundle_meta.json 中的 build_date（ISO 8601 格式）
- 所有 markdown 文件使用统一的标题层级（# → ## → ###）
