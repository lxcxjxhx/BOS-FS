# Changelog

All notable changes to BOS-FS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.0.7] - 2026-05-22
### Added
- 信任背书体系（knowledge/trust_signals.md）
- 权威引用库（knowledge/authority_references.md）
- Submission Builder 新增 trust_statement.md 组件
- 评审模拟器新增"信任度"维度

### Changed
- 评分标准新增 Trust 信任背书维度（权重 5%）
- Pitch 模板新增信任背书章节
- README.md 新增信任背书展示区段

## [0.0.6] - 2026-05-21
### Changed
- 集成指南合并（guides/integration.md + runtime/integration.md）
- 评分文件清理
- Skill 目录精简（.trae/skills/bos-fs/ 仅保留 SKILL.md）
- 模板格式增强

## [0.0.5] - 2026-05-21
### Changed
- Skill 文件压缩
- Knowledge 库合并（竞品分析+差异化）
- 评分标准统一
- 模板精简

## [0.0.4] - 2026-05-21
### Changed
- README 高密度化
- 集成指南合并
- 元数据精简

## [0.0.3] - 2026-05-21
### Changed
- Skill Token 优化（~55% 压缩）
- .trae/ 目录去重
- 公共上下文提取

## [0.0.2] - 2026-05-21
### Added
- 生产级 Skill
- Pipeline 编排器
- 多平台集成
- 评分标准

## [0.0.1] - 2026-05-21
### Added
- 初始版本：六大 Skill + 基础 Runtime + 知识库

[Unreleased]: https://github.com/HOS/BOS-FS/compare/v0.0.7...HEAD
[0.0.7]: https://github.com/HOS/BOS-FS/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/HOS/BOS-FS/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/HOS/BOS-FS/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/HOS/BOS-FS/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/HOS/BOS-FS/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/HOS/BOS-FS/compare/v0.0.1...v0.0.2
