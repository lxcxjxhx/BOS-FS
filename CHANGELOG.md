# Changelog

All notable changes to BOS-FS will be documented in this file.

## [v0.3.4] - 2026-06-01

- 文档生成Skill(解决纯AI生成内容缺乏人感/无法落地/不能保证正确性问题)
- 新增doc-generator SKILL
- 三级可信度评级系统
- real-world真实案例沉淀目录
- 现有27个知识文件全部标注可信度
- 文档生成工作流示例
- 16新增质量规则测试
- 完整文档生成使用指南

## [v0.3.3] - 2026-06-01

- 灵活性增强(所有Skill引入MUST/SHOULD/MAY约束分级)
- README Refactor五段式改为推荐结构
- Submission Builder支持精简/自定义模式
- Reviewer Simulator增加轻量评审模式
- Pipeline支持按需执行
- flexibility_principles.md知识文件
- 修复2个配置化测试失败
- 318测试全通过

## [v0.3.2] - 2026-06-01

- 扩展适用场景(从5类安全交付→8类通用交付)
- 强调产品交付辅助定位
- 新增软件产品/技术文档/开源项目/咨询报告交付案例
- delivery_scenarios.md全面重写为通用场景
- README适用场景/提效数据章节
- 6个真实案例库
- 全局版本号升级

## [v0.3.1] - 2026-06-01

- 全面配置化(所有硬编码提取为可配置项)
- 支持自定义评审规则/提交组件/输出格式
- 3个预定义场景配置模板
- 96新增配置测试

## [v0.3.0] - 2026-06-01

- 真实落地增强(新增5类交付场景定义)
- ROI提效验证框架
- 3个完整真实案例库
- README适用场景/提效数据章节
- guides/delivery_usage.md使用指南
- 全局版本号升级

## [v0.2.11] - 2026-05-26

- SKILL结构完整性与引擎演示修复
- reject-analyzer Purpose→Role
- bos-fs-pipeline新增Output Schema章节
- engine/main.py修正reviewer_simulator调用签名
- outcome_mapper使用map_features批量方法
- pytest 171 passed
- 全局版本号升级

## [v0.2.10] - 2026-05-26

- SKILL目录结构与路径一致性优化
- README.md全部skill链接从扁平路径→子目录路径
- submission-builder Edge Cases增强
- outcome-mapper Anti-Patterns增强
- 全局版本号升级

## [v0.2.9] - 2026-05-26

- SKILL细节优化
- skills-mini/版本标签修正
- Context路径修正
- Full version格式统一
- 新增压缩版README使用入口
- reviewer-simulator/reject-analyzer压缩版Schema紧凑多行化
- 全局版本号升级

## [v0.2.8] - 2026-05-26

- 高压缩Token-Saver版本
- skills-mini/独立目录8个压缩SKILL.md
- 合并重复节/表格化/删除boilerplate
- token减少30-60%
- 保留100%核心规则/约束/输出格式

## [v0.2.7] - 2026-05-25

- SKILL文档质量优化
- reviewer_simulator规范统一pass_probability/五层标题/缺陷阈值
- book-knowledge-ingestor精简CLI文档
- reject-analyzer示例补全
- readme-refactor Output章节
- outcome-mapper Input格式
- submission-builder FAQ数量统一
- pipeline InputValidation+ErrorHandling
- 全局version标签

## [v0.2.6] - 2026-05-25

- 引擎剩余差距补齐
- reject_analyzer 20模式+root_cause_tree
- readme_refactor Quick Start+现有方案不足
- submission_builder status枚举对齐+meta补充
- outcome_mapper空输入提示
- engine/main adversarial演示
- manifest engine_status标注

## [v0.2.5] - 2026-05-25

- 引擎与SKILL对齐
- 新增adversarial评审引擎
- 反谄媚4层检测引擎化
- 非线性递减公式实现
- 弱点放大/kill_factors引擎输出
- goal_refiner输入验证补充
- 测试用例从24→37

## [v0.2.4] - 2026-05-25

- 一致性优化与结构对齐
- 四类→五类评审全项目修正
- 六大→七大Skill修正
- BOS-FS.json路径对齐
- adversarial评审规则文件新增
- 版本号全局升级

## [v0.2.3] - 2026-05-24

- 敌对评审模式(竞争对手/敌对者视角)
- 弱点放大机制(缺陷→关联缺陷推断链)
- 预设质疑清单(8个尖锐问题)
- kill_factors致命缺陷检测
- adversarial评分逻辑(基础分35/封顶75/保底5)

## [v0.2.2] - 2026-05-24

- 反讨好机制深度增强(四层防护:词汇级/结构级/分数级/模式级)
- 缺陷加权非线性递减
- 拒绝模式扩展(20种含数据隐私/可扩展性/技术债务等)
- 根因分析树(3层深度)
- 排查深度矩阵(4评审×7层)
- 交叉验证规则
- 基准对比规则

## [v0.2.1] - 2026-05-24

- 书籍背书展示(10本NEED-PACK完整书单/贡献映射/BOS-FS能力对应)
- 学术诚信声明(用户亲自阅读并提炼要点)
- 各Skill文档方法论来源标注
- 知识文件来源追溯
- README方法论背书章节

## [v0.2.0] - 2026-05-24

- book_knowledge_ingestor增强(实时摄取管道/增量更新/版本管理)
- 10本NEED-PACK书籍逐章深度提取
- 知识提取密度控制(≤30行/章)与冗余检测(>80%相似度)
- reviewer_simulator反谄媚机制(10分制/缺陷计数/复合惩罚)
- Agent Skills开放标准格式(YAML frontmatter/kebab-case目录)
- SKILL文件增强(Anti-Patterns/Edge Cases/Quality Gates)
- reviewer-simulator与submission-builder新增references/目录

## [v0.1.9] - 2026-05-24

- 8个SKILL文件增强(Anti-Patterns/Edge Cases/Quality Gates章节)
- reviewer-simulator与submission-builder新增references/目录
- 知识文件引用格式更新(01_xxx.md→skill-name/SKILL.md)
- book_ingestor.py增强(密度控制≤30行/章、冗余检测)
- Agent Skills开放标准格式(YAML frontmatter)

## [v0.1.8] - 2026-05-24

- Anti-Sycophancy 机制(reviewer_simulator 缺陷计数/复合惩罚/等级上限/谄媚警告)
- rubrics.md 新增反谄媚规则
- 10 本 NEED-PACK 书籍逐章深度提取完成

## [v0.1.7] - 2026-05-24

- NEED-PACK 综合提炼整合
- 4 新增知识文件(accelerate_dora/mlops_delivery/data_intensive_patterns/architecture_quality_metrics)
- 6 增强知识文件
- 151 tests/0 failed

## [v0.1.6] - 2026-05-24

- 知识摄取引擎增强(batch/summary)
- NEED-PACK/3 完整摄取(5本书→238文件)
- NEED-PACK/4 完整摄取(5本书→371文件)
- 测试修复(151 passed/0 failed)
- _slugify Windows 兼容性修复

## [v0.1.5] - 2026-05-24

- 知识体系五层重构
- Pipeline 阶段重排序(Review→Refactor)
- 信任框架合并
- 交付指标框架
- SKILL.md 五层架构
- runtime 知识来源标注
- 书籍知识摄取引擎
- NEED-PACK/3+4 知识提炼(6文件)

## [v0.1.4] - 2026-05-23

- 工程收尾与一致性修复
- 新增5个测试(4引擎+1集成)
- manifest同步
- 引擎演示完整
- rubrics对齐
- 删除orchestrator

## [v0.1.3] - 2026-05-23

- Python引擎补齐(4个)
- README Refactor输出Schema
- Reviewer示例修复
- submission_checklist一致性
- 评审模拟测试

## [v0.1.2] - 2026-05-23

- 评审体系完整化
- 新增产品/开源评审规则
- Pipeline职责分离
- Skill输出Schema统一
- 示例输入输出对照

## [v0.1.1] - 2026-05-23

- SKILL系统增强
- 新增Skill清单
- InputValidation/ErrorHandling
- 重写SKILL.md

## [v0.1.0] - 2026-05-23

- Python引擎修复
- 引擎模块文件重对齐
- 新增engine基础项目结构
- 新增project_manifest

## [v0.0.9] - 2026-05-23

- 文档与可用性增强
- 新增快速上手指南和速查表
- 更新cursorrules
- 知识库交叉引用

## [v0.0.8] - 2026-05-23

- 文档与结构一致性优化
- 新增CHANGELOG/SECURITY/CONTRIBUTING
- 修复README重复tagline

## [v0.0.7] - 2026-05-22

- 信任背书增强
- 权威引用库
- Submission新增trust_statement
- 评审新增信任度维度

## [v0.0.6] - 2026-05-21

- 集成指南合并
- 评分文件清理
- Skill目录精简
- 模板格式增强

## [v0.0.5] - 2026-05-21

- Skill文件压缩
- Knowledge库合并(竞品分析+差异化)
- 评分标准统一
- 模板精简

## [v0.0.4] - 2026-05-21

- README高密度化
- 集成指南合并
- 元数据精简

## [v0.0.3] - 2026-05-21

- Skill Token优化(~55%压缩)
- .trae/目录去重
- 公共上下文提取

## [v0.0.2] - 2026-05-21

- 生产级Skill
- pipeline编排器
- 多平台集成
- 评分标准

## [v0.0.1] - 2026-05-21

- 初始版本
- 七大Skill
- 基础Runtime
- 知识库
