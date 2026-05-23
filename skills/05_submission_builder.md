# Submission Builder
> Context: [base_context](../knowledge/base_context.md)

## Purpose
构建完整项目提交包。

## Input/Output
输入: `{persona, problem, solution, outcome, readme}`
输出:
| 文件 | 内容 |
|------|------|
| README.md | What/Why/How/Result/Next |
| demo_guide.md | 安装→配置→运行→验证 |
| introduction.md | 一句话价值+问题+方案+差异化+指标 |
| screenshots_guide.md | 截图规范+关键界面 |
| FAQ.md | 10个典型问答 |
| risk_disclosure.md | 技术/市场/合规风险 |
| trust_statement.md | 技术/商业/工程可信度声明（权威引用） |
| bundle_meta.json | 项目元数据+goal+状态 |

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
- 风险说明不可省略

## Output
```json
{"bundle_path":"submission_bundle/","components":["README.md","demo_guide.md","introduction.md","screenshots_guide.md","FAQ.md","risk_disclosure.md","trust_statement.md","bundle_meta.json"],"status":"complete"}
```