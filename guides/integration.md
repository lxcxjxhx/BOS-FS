# BOS-FS 多平台集成指南

## 快速参考

| 平台 | 加载方式 | 文件 |
|------|----------|------|
| Cursor | `@skills/pipeline.md` | 根目录 `.cursorrules` 自动加载 |
| Trae | `/skill bos-fs/pipeline` | `.trae/skills/bos-fs/` 自动加载 |
| OpenHands | 引用 skills/ 目录 | 对应 Skill .md 文件 |
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

```python
import json

def load_skill(name):
    with open(f"skills/{name}.md") as f: return f.read()

# Pipeline 流程
def bosfs_pipeline(desc, readme=""):
    goal = call_llm(load_skill("01_goal_refiner.md"), desc)
    outcomes = call_llm(load_skill("04_outcome_mapper.md"), goal)
    new_readme = call_llm(load_skill("03_readme_refactor.md"), readme)
    review = call_llm(load_skill("02_reviewer_simulator.md"), {**goal, **outcomes})
    bundle = call_llm(load_skill("05_submission_builder.md"), {**goal, "readme": new_readme})
    return {"goal": goal, "outcomes": outcomes, "readme": new_readme, "review": review, "bundle": bundle}
```
