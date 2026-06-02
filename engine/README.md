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

## 配置系统 (v0.3.1+)

v0.3.1 引入了全面的配置化系统，所有硬编码参数均提取为可配置项，支持自定义评审规则、提交组件和输出格式。

### 配置目录结构

```
engine/config/
├── defaults/                          # 默认配置（JSON）
│   ├── reviewer_rules.json            # 评审维度权重/阈值/缺陷惩罚
│   ├── anti_sycophancy.json           # 反谄媚检测规则
│   ├── adversarial_rules.json         # 敌对评审规则
│   ├── submission_components.json     # 提交组件定义
│   ├── goal_refiner.json              # 意图解析配置
│   ├── outcome_mapper.json            # 成果映射配置
│   └── reject_analyzer.json           # 拒绝分析配置
├── scenarios/                         # 场景配置模板
│   ├── pen-test.json                  # 渗透测试场景
│   ├── code-audit.json                # 代码审计场景
│   └── vulnerability-ledger.json      # 漏洞台账场景
└── loader.py                          # 配置加载器（三级合并）
```

### 配置加载优先级

```
硬编码默认值 < JSON 默认值 < 用户自定义配置 < 场景配置
```

```python
from config.loader import ConfigLoader

# 1. 加载默认配置（JSON defaults 覆盖硬编码默认值）
loader = ConfigLoader()
reviewer_rules = loader.load("reviewer_rules.json")

# 2. 加载场景配置（场景配置覆盖默认配置）
scenario_config = loader.load_scenario("pen-test")

# 3. 使用点号访问配置值
security_weight = loader.get("reviewer_rules.review_types.technical.dimensions.安全性.weight")
# → 35（pen-test 场景覆盖后的值）
```

### 自定义评审规则

创建自定义规则 JSON 文件，覆盖默认维度权重和阈值：

```json
{
  "reviewer_rules": {
    "review_types": {
      "technical": {
        "dimensions": {
          "架构设计": {"weight": 30, "max": 10},
          "代码质量": {"weight": 30, "max": 10},
          "安全性": {"weight": 25, "max": 10},
          "技术栈": {"weight": 10, "max": 10},
          "依赖管理": {"weight": 5, "max": 10}
        }
      }
    },
    "thresholds": {
      "test_coverage": {"excellent": 85, "good": 70, "poor": 40}
    }
  }
}
```

```python
# 使用自定义配置
custom_loader = ConfigLoader(config_dir="/path/to/custom/config")
config = custom_loader.load_all_defaults()
```

### 自定义提交组件

在 `submission_components.json` 中定义组件：

```json
{
  "components": [
    {
      "id": "custom_report",
      "filename": "custom_report.md",
      "description": "自定义报告文档",
      "generator_method": "generate_custom_report",
      "required_fields": ["name", "version"],
      "optional_fields": ["author", "date"],
      "output_extension": ".md",
      "priority": 9
    }
  ],
  "output_formats": ["markdown", "json", "html"],
  "default_format": "markdown"
}
```

### 使用场景配置

```python
# 加载预定义场景
loader = ConfigLoader()

# 渗透测试场景：安全性维度权重提升至 35%
pen_test_config = loader.load_scenario("pen-test")

# 代码审计场景：代码质量维度权重提升至 35%
code_audit_config = loader.load_scenario("code-audit")

# 漏洞台账场景：文档完整性权重 30%、可追溯性 25%
ledger_config = loader.load_scenario("vulnerability-ledger")
```

### 预定义场景对比

| 维度 | 默认 | pen-test | code-audit | vulnerability-ledger |
|------|------|----------|------------|---------------------|
| 安全性权重 | 15% | **35%** | 20% | 15% |
| 代码质量权重 | 25% | 20% | **35%** | 20% |
| 专属组件数 | 8 | 10 (8+2) | 10 (8+2) | 11 (8+3) |
| 测试覆盖率(excellent) | 80% | **90%** | 85% | 80% |
