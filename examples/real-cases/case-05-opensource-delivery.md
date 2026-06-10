# BOS-FS 开源项目交付案例

## 场景描述

一位开发者完成了一个 Python CLI 数据清洗工具的核心功能，代码已经推送到 GitHub，但项目缺乏标准化的开源交付物。README 仅有三行说明，无贡献指南、无安全策略、无许可证建议、无 CI/CD 配置。使用 BOS-FS 流水线将半成品项目转化为符合开源社区标准的专业项目。

## 输入数据

**原始项目状态（片段）**：

```
my-data-cleaner/
├── src/
│   └── cleaner.py          # 核心逻辑，500 行
├── tests/
│   └── test_cleaner.py     # 15 个单元测试
├── requirements.txt        # 依赖列表
└── README.md               # 仅 3 行："这是一个数据清洗工具，pip install 后用。"
```

| 维度 | 说明 |
|------|------|
| 项目名称 | my-data-cleaner |
| 项目描述 | Python CLI 工具，用于自动化数据清洗和格式转换 |
| 技术栈 | Python 3.8+, Click, Pandas, Pydantic |
| 核心功能 | CSV/JSON 数据清洗、格式转换、数据验证、批量处理 |
| 依赖列表 | click>=8.0, pandas>=1.4, pydantic>=1.10 |
| 当前状态 | 功能完成，无开源交付物 |

## 处理流程

### BOS-FS 流水线执行

```
项目状态 → Goal Refiner → Reviewer Simulator (开源评审) → README Refactor → Submission Builder → 完整开源交付包
```

| 阶段 | 技能 | 输入 | 输出 |
|------|------|------|------|
| Understand | **Goal Refiner** | 代码仓库 + 3 行 README | 结构化项目画像：{功能清单, 依赖树, 测试覆盖, 代码质量} |
| Review | **Reviewer Simulator (开源评审)** | 项目画像 + 社区标准 | 开源合规审查报告：对比 GitHub 高星项目，发现 12 项缺失 |
| Refactor | **README Refactor** | 原始项目 + 审查结果 | 标准 README：徽章、简介、安装、用法、API、贡献、许可证 |
| Build | **Submission Builder** | 各阶段输出 | 完整开源交付包：README/CONTRIBUTING/CODE_OF_CONDUCT/SECURITY/LICENSE/CI |

### 关键处理细节

**Goal Refiner 项目画像**：

| 维度 | 原始状态 | 结构化输出 |
|------|----------|------------|
| 功能清单 | 无文档 | `["csv_clean","json_transform","data_validate","batch_process","format_convert"]` |
| 测试覆盖 | 15 个测试 | `{"total":15,"passed":15,"coverage":"68%","missing":["edge_cases","error_handling"]}` |
| 代码质量 | 无分析 | `{"loc":500,"complexity":"medium","type_hints":"partial","docstrings":"missing"}` |
| 依赖管理 | requirements.txt | `{"runtime":["click","pandas","pydantic"],"dev":["pytest","black","mypy"]}` |

**Reviewer Simulator (开源评审) 发现**：

| # | 审查维度 | 开源社区标准 | 当前状态 | 差距 |
|---|----------|--------------|----------|------|
| 1 | README | 项目徽章、简介、安装、用法、API、贡献指南 | 仅 3 行 | 缺失 6 个标准章节 |
| 2 | 许可证 | 明确开源许可证（MIT/Apache/GPL） | 无 | 缺失，用户无法合法使用 |
| 3 | 贡献指南 | CONTRIBUTING.md 定义 PR 流程、代码规范 | 无 | 缺失，外部贡献者无指引 |
| 4 | 行为准则 | CODE_OF_CONDUCT.md | 无 | 缺失，不符合开源社区规范 |
| 5 | 安全策略 | SECURITY.md 定义漏洞报告流程 | 无 | 缺失，安全风险无法上报 |
| 6 | Issue 模板 | .github/ISSUE_TEMPLATE/ | 无 | 缺失，用户提 issue 格式混乱 |
| 7 | PR 模板 | .github/pull_request_template.md | 无 | 缺失，PR 描述不规范 |
| 8 | CI/CD | GitHub Actions 自动测试/构建 | 无 | 缺失，无法保证代码质量 |
| 9 | 版本管理 | CHANGELOG.md, 语义化版本 | 无 | 缺失，用户无法追踪变更 |
| 10 | 信任声明 | OpenSSF Scorecard / 供应链安全 | 无 | 缺失，企业用户无法评估风险 |
| 11 | 代码质量 | pre-commit, lint, type check | 无 | 缺失，代码风格不统一 |
| 12 | 文档站点 | MkDocs / Sphinx 文档站 | 无 | 建议项，可后续添加 |

**README Refactor 输出（摘要）**：

```markdown
# my-data-cleaner

[![PyPI version](https://badge.fury.io/py/my-data-cleaner.svg)](https://badge.fury.io/py/my-data-cleaner)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/user/my-data-cleaner/workflows/Tests/badge.svg)](https://github.com/user/my-data-cleaner/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

自动化数据清洗和格式转换的 Python CLI 工具。

## 特性
- CSV/JSON 数据清洗：去重、填充缺失值、类型转换
- 格式转换：CSV ↔ JSON ↔ Parquet
- 数据验证：基于 Pydantic 的 schema 校验
- 批量处理：支持目录级批量操作

## 快速开始
$ pip install my-data-cleaner
$ data-cleaner validate --input data.csv --schema schema.json
```

## 输出交付物

```
my-data-cleaner/
├── README.md                     # 完整项目主页（徽章、简介、安装、用法、贡献）
├── CONTRIBUTING.md               # 贡献指南（PR 流程、代码规范、开发环境）
├── CODE_OF_CONDUCT.md            # 贡献者行为准则
├── SECURITY.md                   # 安全策略与漏洞报告流程
├── LICENSE                       # MIT 许可证
├── CHANGELOG.md                  # 版本变更日志（语义化版本）
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md         # Bug 报告模板
│   │   └── feature_request.md    # 功能请求模板
│   ├── PULL_REQUEST_TEMPLATE.md  # PR 描述模板
│   └── workflows/
│       ├── test.yml              # CI 测试工作流
│       ├── lint.yml              # 代码规范检查
│       └── release.yml           # 发布工作流
├── .pre-commit-config.yaml       # pre-commit 钩子配置
├── pyproject.toml                # 现代 Python 项目配置
├── docs/
│   ├── getting_started.md        # 快速开始
│   └── api_reference.md          # API 参考文档
└── trust/
    └── sbom.json                 # 软件物料清单（供应链安全）
```

## 提效数据

| 指标 | 传统方式 | BOS-FS | 提升 |
|------|----------|--------|------|
| 总耗时 | 1-2 周 | 半天（4 小时） | **75% 时间缩减** |
| README 撰写 | 1 天 | 0.5 小时 | 94% 缩减 |
| 贡献文档 | 2 天 | 0.5 小时 | 94% 缩减 |
| CI/CD 配置 | 1 天 | 0.5 小时 | 94% 缩减 |
| 模板文件 | 0.5 天 | 0.25 小时 | 92% 缩减 |
| 许可证选择 | 0.5 天调研 | 0.1 小时推荐 | 96% 缩减 |
| 审查与修正 | 1 天 | 0.5 小时 | 94% 缩减 |
| 交付物完整性 | 约 30% | 100% | 提升 70% |

## 质量对比

| 维度 | BOS-FS 使用前 | BOS-FS 使用后 |
|------|---------------|---------------|
| 交付物完整性 | 30%（仅 README + 代码） | 100%（12 个标准开源组件） |
| 社区信任度 | 低（无徽章、无许可证、无 CI） | 高（完整徽章、CI 通过、许可证明确） |
| 可贡献性 | 无指引，外部贡献者无从下手 | CONTRIBUTING.md + Issue/PR 模板 |
| 安全合规 | 无安全策略 | SECURITY.md + 漏洞报告流程 |
| 代码质量保障 | 无自动化检查 | pre-commit + CI 自动测试 + lint |
| 版本管理 | 无变更日志 | CHANGELOG.md + 语义化版本 |
| 供应链安全 | 无透明度 | SBOM 清单，企业用户可审计 |
| 开源社区标准 | 不符合 | 完全符合 OpenSSF / GitHub 最佳实践 |

## 使用技能

| 技能 | 版本 | 应用场景 |
|------|------|----------|
| `goal-refiner` | v1.2 | 分析代码仓库，生成结构化项目画像 |
| `reviewer-simulator` | v1.3 | 开源社区标准评审（对比高星项目） |
| `readme-refactor` | v1.0 | 将 3 行 README 转化为标准项目主页 |
| `submission-builder` | v1.2 | 生成完整开源交付包 + CI/CD 配置 |

## 客户反馈

> "我的工具功能已经很好用了，但一直没人愿意贡献代码，后来发现是因为项目缺乏基本的开源规范。BOS-FS 半天时间就帮我补齐了所有缺失的交付物，PR 数量在接下来一个月增长了 3 倍。"
> — 某开源数据工具维护者
