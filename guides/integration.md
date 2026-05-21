# BOS-FS 多平台集成指南

## 快速参考

| 平台 | 加载方式 | 文件 |
|------|----------|------|
| Cursor | `@skills/pipeline.md` | 根目录 `.cursorrules` 自动加载 |
| Trae | `/skill bos-fs/pipeline` | `.trae/skills/bos-fs/` 自动加载 |
| OpenHands | 引用 skills/ 目录 | 对应 Skill .md 文件 |
| Claude Code | `@skills/pipeline.md` | Skill .md 文件或 Custom Instructions |
| OpenDevin | 配置 skills 路径 | skills/pipeline.md |
| Copilot | `#file:skills/pipeline.md` | 自定义指令或 .github/copilot-instructions.md |
| 通用 LLM | 读取 .md 作为 system prompt | skills/pipeline.md |

## Cursor 集成

```
# 方式一：直接引用
@skills/pipeline.md

# 方式二：合并到 .cursorrules
将 Skill 内容复制到项目根目录 .cursorrules
```

## Trae 集成

```
# 完整流水线
/spec 使用 BOS-FS 分析并优化：[项目描述]

# 单个 Skill
/skill bos-fs/01_goal_refiner
```

## 通用 LLM 集成

### 方式一：最小集成示例

```python
# Step 1: 读取 Skill 提示词
system_prompt = read_file("skills/01_goal_refiner.md")

# Step 2: 调用 LLM
result = llm.chat(system_prompt=system_prompt, user_input=project_description)

# Step 3: 解析输出
parsed = json.loads(result)
```

### 方式二：Pipeline 流程

```python
import json

def load_skill(name):
    with open(f"skills/{name}.md") as f: return f.read()

def bosfs_pipeline(desc, readme=""):
    goal = call_llm(load_skill("01_goal_refiner.md"), desc)
    outcomes = call_llm(load_skill("04_outcome_mapper.md"), goal)
    new_readme = call_llm(load_skill("03_readme_refactor.md"), readme)
    review = call_llm(load_skill("02_reviewer_simulator.md"), {**goal, **outcomes})
    bundle = call_llm(load_skill("05_submission_builder.md"), {**goal, "readme": new_readme})
    return {"goal": goal, "outcomes": outcomes, "readme": new_readme, "review": review, "bundle": bundle}
```

### 方式三：API 集成步骤
1. 读取 BOS-FS.json 获取 Skill 列表
2. 读取对应 .md 文件作为 system prompt
3. 按 pipeline 顺序依次调用
4. 通过结构化输出解析结果

## OpenHands 集成

1. 将 skills/ 目录复制到 OpenHands 的 skills 目录
2. 在 agent 配置中注册 BOS-FS Skills
3. 通过 Skill ID 调用对应功能

## Claude Code 集成

### 方式一：Skill 引用
将 Skill 文件放在项目目录中，通过 `@` 引用：
```
@skills/pipeline.md
```

### 方式二：Claude Desktop 配置
将 BOS-FS Skills 添加到 Claude Desktop 的自定义指令：
1. 读取每个 Skill .md 文件
2. 将内容添加到 Claude Desktop 设置 → Custom Instructions
3. 使用 pipeline 提示词进行完整工作流

### 方式三：API 集成
```python
import anthropic

def bosfs_pipeline(project_description):
    with open("skills/pipeline.md") as f:
        system_prompt = f.read()
    
    client = anthropic.Anthropic()
    result = client.messages.create(
        model="claude-sonnet-4-20250514",
        system=system_prompt,
        messages=[{"role": "user", "content": project_description}],
        max_tokens=8192
    )
    return result.content[0].text
```

## OpenDevin 集成

### 配置
将 BOS-FS `skills/` 目录复制到 OpenDevin 的 skills 路径。

### 使用方法
在 OpenDevin agent 配置中：
```json
{
  "skills": [
    {"name": "bos-fs", "path": "skills/", "pipeline": "pipeline.md"}
  ]
}
```

### 执行流程
OpenDevin 将在以下阶段使用 BOS-FS Skills：
- 仓库分析阶段 → Goal Refiner
- 文档生成阶段 → README Refactor
- 提交前检查 → Reviewer Simulator

## GitHub Copilot 集成

### 方式一：Copilot Chat
在 Copilot Chat 中引用 Skill 文件：
```
#file:skills/pipeline.md
Optimize my project: [project description]
```

### 方式二：Copilot 自定义指令
将 BOS-FS 原则添加到 GitHub Copilot 自定义指令：
```
When helping with project documentation:
1. Use BOS-FS What/Why/How/Result/Next structure
2. Apply value formula: technology × user × benefit
3. Simulate reviewer feedback before finalizing
```

### 方式三：VS Code 扩展
在项目根目录创建 `.github/copilot-instructions.md`：
```markdown
Use BOS-FS Skill system for project optimization:
- Load skills/pipeline.md for full workflow
- Use individual skills for specific tasks
- Follow Submission Engineering principles
```
