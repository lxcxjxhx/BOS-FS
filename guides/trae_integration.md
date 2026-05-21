# Trae Skills 集成指南

## 安装
将 BOS-FS/skills/ 目录复制到项目 `.trae/skills/` 目录。

## 激活
```
/skill goal_refiner
/skill reviewer_simulator
/skill readme_refactor
/skill outcome_mapper
/skill submission_builder
/skill reject_analyzer
```

## 完整流水线
```
/spec 使用 BOS-FS Skill 系统分析并优化我的项目：
[项目描述]
```

## 配置
在 .trae/rules/project_rules.md 中添加：
```markdown
当涉及项目优化时，使用 BOS-FS Skill 系统：
1. 先用 Goal Refiner 明确意图
2. 再用 Outcome Mapper 转换价值
3. 再用 README Refactor 重构文档
4. 最后用 Reviewer Simulator 预审
```
