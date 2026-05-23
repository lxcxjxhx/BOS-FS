# BOS-FS Engine (Optional Backend)

> Python 模块作为可选后端引擎，非核心交付物。
> 核心功能通过 Skill 提示词文件（skills/）实现，无需代码。

## When to Use
- 需要程序化批量处理
- 需要集成到自动化流水线
- 需要结构化输出解析

## Quick Start
```bash
python main.py
python -m pytest tests/ -v
```

## Modules
- `core/01_intent_parser/goal_refiner.py` — 意图解析
- `core/02_value_mapper/outcome_mapper.py` — 成果映射
- `core/03_submission_optimizer/readme_refactor.py` — README 重构
- `core/04_delivery_builder/submission_builder.py` — 提交构建
- `core/05_artifact_generator/reject_analyzer.py` — 拒绝分析
- `core/06_review_simulator/reviewer_simulator.py` — 评审模拟

## Relationship with Skills
Engine 是 Skill 的 Python 实现版本。Skill 提示词文件（skills/）是核心交付物，可在任意 AI Agent 中直接使用，无需此引擎。
