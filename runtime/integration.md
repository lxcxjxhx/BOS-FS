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

## Claude Code Integration

### Method 1: Skill Reference
Place Skill files in a project directory and reference via `@`:
```
@skills/pipeline.md
```

### Method 2: Claude Desktop Config
Add BOS-FS skills to Claude Desktop's custom instructions:
1. Read each Skill .md file
2. Add content to Claude Desktop settings → Custom Instructions
3. Use the pipeline prompt for full workflow

### Method 3: API Integration
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

## OpenDevin Integration

### Setup
Copy BOS-FS `skills/` directory to OpenDevin's skills path.

### Usage
In OpenDevin agent configuration:
```json
{
  "skills": [
    {"name": "bos-fs", "path": "skills/", "pipeline": "pipeline.md"}
  ]
}
```

### Execution Flow
OpenDevin will use BOS-FS Skills during:
- Repository analysis phase → Goal Refiner
- Documentation generation → README Refactor
- Pre-submission check → Reviewer Simulator

## GitHub Copilot Integration

### Method 1: Copilot Chat
Reference Skill files in Copilot Chat:
```
#file:skills/pipeline.md
Optimize my project: [project description]
```

### Method 2: Copilot Custom Instructions
Add BOS-FS principles to GitHub Copilot custom instructions:
```
When helping with project documentation:
1. Use BOS-FS What/Why/How/Result/Next structure
2. Apply value formula: technology × user × benefit
3. Simulate reviewer feedback before finalizing
```

### Method 3: VS Code Extension
Create `.github/copilot-instructions.md` in project root:
```markdown
Use BOS-FS Skill system for project optimization:
- Load skills/pipeline.md for full workflow
- Use individual skills for specific tasks
- Follow Submission Engineering principles
```
