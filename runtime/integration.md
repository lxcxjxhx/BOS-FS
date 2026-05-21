# Multi-Platform Integration Guide

## Cursor Rules Integration
1. 将 skills/ 目录下的 .md 文件内容复制到项目 `.cursorrules` 文件
2. 或在 Cursor 中通过 @file 引用对应 Skill 文件
3. 推荐加载顺序：BOS-FS.json → 对应 Skill .md

## Trae Skills Integration
1. 将 Skill 文件放入项目 `.trae/skills/` 目录
2. 使用 /skill 命令激活对应 Skill
3. 支持通过 BOS-FS.json 自动发现所有可用 Skills

## OpenHands Skills Integration
1. 将 skills/ 目录复制到 OpenHands 的 skills 目录
2. 在 agent 配置中注册 BOS-FS Skills
3. 通过 Skill ID 调用对应功能

## Generic LLM API Integration
1. 读取 BOS-FS.json 获取 Skill 列表
2. 读取对应 .md 文件作为 system prompt
3. 按 pipeline 顺序依次调用
4. 通过结构化输出解析结果

## Minimal Integration Example
```
# Step 1: Load Skill prompt
system_prompt = read_file("skills/01_goal_refiner.md")

# Step 2: Call LLM
result = llm.chat(system_prompt=system_prompt, user_input=project_description)

# Step 3: Parse output
parsed = json.loads(result)
```
