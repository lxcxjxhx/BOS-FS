# Cursor Rules 集成指南

## 方式一：直接引用
将 skills/ 目录下的 .md 文件通过 @file 引用：
```
@skills/01_goal_refiner.md
```

## 方式二：合并到 .cursorrules
将 Skill 内容复制到项目根目录的 `.cursorrules` 文件。

## 方式三：Rules 目录
将 Skill 文件放入 `.cursor/rules/` 目录，Cursor 自动加载。

## 使用示例
```
使用 BOS-FS 的 Goal Refiner Skill 分析我的项目：
[项目描述]
```

## Pipeline 调用
```
1. @skills/01_goal_refiner.md → 提取意图
2. @skills/04_outcome_mapper.md → 价值转换
3. @skills/03_readme_refactor.md → 重构 README
4. @skills/02_reviewer_simulator.md → 预审
5. @skills/05_submission_builder.md → 构建提交包
```
