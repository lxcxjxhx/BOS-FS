# 通用 LLM API 集成指南

## 最小集成
```python
import json

def load_skill(skill_name):
    with open(f"skills/{skill_name}.md") as f:
        return f.read()

# Step 1: Load Skill
system_prompt = load_skill("01_goal_refiner.md")

# Step 2: Call LLM
result = llm.chat(
    system_prompt=system_prompt,
    user_input="做了一个AI工作流系统 支持多模型调度"
)

# Step 3: Parse
parsed = json.loads(result)
```

## Pipeline 集成
```python
def bosfs_pipeline(project_description):
    # 1. Understand
    goal = call_llm(load_skill("01_goal_refiner.md"), project_description)
    
    # 2. Map
    outcomes = call_llm(load_skill("04_outcome_mapper.md"), goal)
    
    # 3. Refactor
    readme = call_llm(load_skill("03_readme_refactor.md"), original_readme)
    
    # 4. Review
    review = call_llm(load_skill("02_reviewer_simulator.md"), {**goal, **outcomes})
    
    # 5. Build
    bundle = call_llm(load_skill("05_submission_builder.md"), {**goal, "readme": readme})
    
    return {"goal": goal, "outcomes": outcomes, "readme": readme, "review": review, "bundle": bundle}
```

## 批量评审
```python
review_types = ["technical", "investment", "product", "opensource"]
results = {rt: call_llm(load_skill("02_reviewer_simulator.md"), project_info, review_type=rt) for rt in review_types}
```
