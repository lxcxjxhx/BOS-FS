# 贡献指南

感谢你对 BOS-FS 的兴趣！欢迎通过以下方式贡献。

## 贡献流程

1. **Fork** 本仓库
2. **创建分支**: `git checkout -b feature/your-feature`
3. **提交更改**: `git commit -m 'feat: add your feature'`
4. **推送**: `git push origin feature/your-feature`
5. **提交 PR**: 在 GitHub 上创建 Pull Request

## 代码规范

### 通用规范
- 使用 2 空格缩进
- 文件使用 UTF-8 编码
- 行末换行符使用 LF（Unix 风格）

### Markdown 规范
- 使用 ATX 风格标题（`# Title`）
- 代码块指定语言标记
- 链接使用相对路径
- 标题使用 Sentence case

### Python 规范（engine/ 目录）
- 遵循 PEP 8
- 函数/类文档字符串使用 Google 风格
- 类型注解必须

## Skill 文件编写规范

每个 Skill 文件必须包含：

```markdown
# [Skill 名称]
> Context: [base_context 链接]

## Role / Purpose
[1-2 句话说明用途]

## Rules / Logic
[核心规则，使用表格或列表]

## Output
[输出格式，使用 JSON Schema 或示例]

## Examples
[1-3 个输入输出示例]
```

### 约束
- 每个 Skill 必须可独立执行
- 输出格式必须明确（JSON / Markdown）
- 边界条件必须说明
- 不可包含模糊指令

## 提交信息规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body]
```

### Type 说明
| Type | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 |
| `docs` | 文档变更 |
| `style` | 代码格式 |
| `refactor` | 重构 |
| `test` | 测试相关 |
| `chore` | 构建/工具链变更 |

### 示例
```
feat: add trust dimension to reviewer simulator
fix: remove duplicate tagline in README
docs: update project structure in README
refactor: merge integration guides
```

## 讨论

- 功能建议：创建 Issue 讨论
- Bug 报告：包含复现步骤和预期行为
- 问题咨询：直接在 Issue 中提问
