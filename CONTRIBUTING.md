# CONTRIBUTING.md — 贡献指南

## 如何贡献

BOS-FS 是 Submission Engineering（提交工程）项目，欢迎通过以下方式参与贡献：

### 1. 提交 Skills

新增 Skill 需遵循以下规范：

1. 在 `skills/<skill-name>/` 目录下创建 `SKILL.md`
2. 遵循 kebab-case 命名（如 `doc-generator/`）
3. 必须包含 YAML frontmatter：
   ```yaml
   ---
   name: skill-name
   description: 一句话描述
   ---
   ```
4. 必须包含的章节：
   - Role / Purpose
   - Input Format
   - Output Schema
   - Anti-Patterns
   - Edge Cases
   - Quality Gates
5. 在 `skills/manifest.json` 和 `skills-mini/manifest.json` 中注册
6. 在 `BOS-FS.json` 的 skills 数组中添加条目
7. 在 `project_manifest.json` 的 files 数组中添加文件条目

### 2. 贡献知识文件

知识文件按五层架构组织：

| 层级 | 目录 | 内容 |
|------|------|------|
| Intent | `knowledge/intent/` | 持续发现框架、产品价值框架 |
| Runtime | `knowledge/runtime/` | 架构模式 |
| Execution | `knowledge/execution/templates/` | README/Pitch/Demo/Checklist 模板 |
| Governance | `knowledge/governance/` | 评分标准、信任框架、评审规则 |
| Adoption | `knowledge/adoption/` | 差异化、团队拓扑、流指标 |

知识文件要求：
- 每章提炼 ≤30 行核心要点
- 冗余检测：与现有内容相似度 >80% 需合并
- 标注来源书籍/框架

### 3. 报告问题

通过以下方式报告问题：

- **Bug 报告**：描述复现步骤、预期行为、实际行为
- **功能建议**：说明使用场景和期望效果
- **文档问题**：指出错误路径、过时内容、格式问题

### 4. 编码标准

#### Python 引擎
- 遵循 PEP 8 风格
- 所有引擎模块必须有对应测试
- 测试覆盖率要求：新增代码 ≥90%
- 运行测试：`cd engine && python -m pytest tests/ -v`

#### Markdown 文档
- 使用语义化标题（# → ## → ###）
- 代码块标注语言类型
- 路径引用使用相对路径
- 版本标签统一格式：`v0.x.x`

#### Skill 文件
- 目录名：kebab-case（如 `goal-refiner/`）
- 文件名：固定为 `SKILL.md`
- YAML frontmatter 的 `name` 字段：kebab-case
- 约束分级：MUST（必须）/ SHOULD（应该）/ MAY（可以）

### 5. 版本规范

- 语义化版本：MAJOR.MINOR.PATCH
- 每次变更同步更新：
  - `BOS-FS.json` version
  - `skills/manifest.json` version
  - `skills-mini/manifest.json` version
  - `project_manifest.json` version
  - `.cursorrules` version
  - `.trae/skills/bos-fs/SKILL.md` version
  - `README.md` badge
- 在 CHANGELOG.md 中添加新版本记录

### 6. Pull Request 流程

1. 创建特性分支（`feat/skill-name` 或 `fix/path-error`）
2. 遵循上述编码标准
3. 更新所有相关 manifest 和版本文件
4. 运行测试确保通过
5. 提交 PR，说明变更内容和影响范围
