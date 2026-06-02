# BOS-FS 自定义配置指南 (v0.3.1+)

本指南涵盖 BOS-FS 配置系统的全部自定义能力，包括评审规则、提交组件、场景配置模板和高级自定义场景。

---

## 配置系统概览

### 设计理念

v0.3.1 版本将引擎中所有硬编码参数提取为可配置项，实现：
- **零代码定制**：通过 JSON 配置文件即可调整评审规则、组件、输出格式
- **场景化模板**：预定义 3 个行业场景配置，开箱即用
- **三级覆盖**：硬编码默认值 < JSON 默认值 < 用户配置 < 场景配置

### 目录结构

```
engine/config/
├── defaults/                          # 默认配置（JSON 文件）
│   ├── reviewer_rules.json            # 评审维度权重/阈值/缺陷惩罚/通过率
│   ├── anti_sycophancy.json           # 反谄媚检测规则（词汇/方差/阈值/惩罚）
│   ├── adversarial_rules.json         # 敌对评审规则（基础分/上限/下限）
│   ├── submission_components.json     # 提交组件定义（8 组件/输出格式）
│   ├── goal_refiner.json              # 意图解析配置
│   ├── outcome_mapper.json            # 成果映射配置
│   └── reject_analyzer.json           # 拒绝分析配置
├── scenarios/                         # 场景配置模板
│   ├── pen-test.json                  # 渗透测试场景（安全优先）
│   ├── code-audit.json                # 代码审计场景（质量优先）
│   └── vulnerability-ledger.json      # 漏洞台账场景（跟踪优先）
└── loader.py                          # 配置加载器（递归合并 + 点号访问）
```

### 配置加载器 API

```python
from engine.config.loader import ConfigLoader

# 初始化
loader = ConfigLoader()                          # 使用默认配置目录
loader = ConfigLoader(config_dir="/my/config")   # 使用自定义目录

# 加载单个配置文件
reviewer_rules = loader.load("reviewer_rules.json")

# 点号路径访问任意配置值
weight = loader.get("reviewer_rules.review_types.technical.dimensions.安全性.weight")
threshold = loader.get("reviewer_rules.thresholds.test_coverage.excellent")  # → 80

# 加载场景配置（自动三级合并）
scenario_config = loader.load_scenario("pen-test")

# 重新加载（清除缓存）
loader.reload()
```

---

## 自定义评审规则

### 维度权重调整

评审维度权重决定各维度在总分中的占比。默认配置位于 `defaults/reviewer_rules.json`。

**默认技术评审维度：**

```json
{
  "review_types": {
    "technical": {
      "dimensions": {
        "架构设计": {"weight": 25, "max": 10},
        "技术栈":   {"weight": 20, "max": 10},
        "代码质量": {"weight": 25, "max": 10},
        "安全性":   {"weight": 15, "max": 10},
        "依赖管理": {"weight": 15, "max": 10}
      }
    }
  }
}
```

**自定义示例（安全项目提升安全性权重）：**

```json
{
  "review_types": {
    "technical": {
      "dimensions": {
        "架构设计": {"weight": 20, "max": 10},
        "技术栈":   {"weight": 10, "max": 10},
        "代码质量": {"weight": 20, "max": 10},
        "安全性":   {"weight": 35, "max": 10},
        "依赖管理": {"weight": 15, "max": 10}
      }
    }
  }
}
```

**支持的评审类型：**
- `technical` — 技术评审
- `investment` — 投资评审
- `product` — 产品评审
- `opensource` — 开源评审

### 阈值配置

阈值用于评估各项指标的质量等级：

```json
{
  "thresholds": {
    "test_coverage": {
      "excellent": 80,
      "good": 60,
      "poor": 30
    },
    "text_length": {
      "detailed": 50,
      "moderate": 30,
      "brief": 20
    },
    "dependency_count": {
      "optimal": 10,
      "max_acceptable": 20
    }
  }
}
```

**自定义示例（提高测试覆盖率要求）：**

```json
{
  "thresholds": {
    "test_coverage": {
      "excellent": 90,
      "good": 75,
      "poor": 50
    }
  }
}
```

### 缺陷惩罚规则

缺陷惩罚采用非线性递减曲线，缺陷数量越多惩罚越重：

```json
{
  "defect_penalty": {
    "severity_curve": {
      "1": 1.0,
      "2": 1.0,
      "3": 1.3,
      "4": 1.7,
      "5+": "2.0 + (n-5) * 0.5"
    },
    "score_deduction_per_severity": 0.5,
    "score_ceiling_by_defects": {
      "0-1": 10.0,
      "2": 8.5,
      "3": 7.0,
      "4+": 6.0
    }
  }
}
```

### 反谄媚机制

反谄媚检测防止 AI 给出过度正面评价：

```json
{
  "anti_sycophancy": {
    "empty_praise_words": ["优秀", "完美", "出色", "一流", "极佳", "卓越"],
    "variance_threshold": 0.5,
    "high_score_threshold": 9,
    "security_score_threshold": 7,
    "trust_penalty": 2
  }
}
```

**四层防护：**
1. **词汇级**：检测空泛赞美词汇
2. **结构级**：检测各维度评分方差过低
3. **分数级**：检测高分但无实质理由
4. **模式级**：检测模板化评价模式

### 敌对评审规则

模拟竞争对手/敌对者的严格评审：

```json
{
  "adversarial_rules": {
    "base_score": 35,
    "ceiling": 75,
    "floor": 5,
    "pass_probability_cap_with_kill_factors": 0.20
  }
}
```

---

## 自定义提交组件

### 组件定义结构

每个提交组件在 `submission_components.json` 中定义：

```json
{
  "components": [
    {
      "id": "component_id",
      "filename": "filename.md",
      "description": "组件描述",
      "generator_method": "generate_method_name",
      "required_fields": ["name", "version"],
      "optional_fields": ["author", "date"],
      "output_extension": ".md",
      "priority": 1
    }
  ]
}
```

**字段说明：**

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 组件唯一标识符 |
| `filename` | 是 | 输出文件名 |
| `description` | 是 | 组件用途描述 |
| `generator_method` | 是 | 生成器方法名 |
| `required_fields` | 是 | 必填字段列表 |
| `optional_fields` | 否 | 可选字段列表 |
| `output_extension` | 是 | 输出文件扩展名 |
| `priority` | 是 | 生成优先级（数字越小越先） |

### 默认 8 组件

| 优先级 | ID | 文件名 | 说明 |
|--------|-----|--------|------|
| 1 | `readme` | README.md | 五段式项目说明 |
| 2 | `demo_guide` | demo_guide.md | 演示与安装指南 |
| 3 | `introduction` | introduction.md | 项目推介文档 |
| 4 | `screenshots_guide` | screenshots_guide.md | 截图规范指南 |
| 5 | `faq` | FAQ.md | 常见问题解答 |
| 6 | `risk_disclosure` | risk_disclosure.md | 风险披露声明 |
| 7 | `trust_statement` | trust_statement.md | 信任声明 |
| 8 | `bundle_meta` | bundle_meta.json | 提交包元数据 |

### 新增组件

在 `submission_components.json` 的 `components` 数组中添加：

```json
{
  "components": [
    // ... 原有 8 个组件 ...
    {
      "id": "api_documentation",
      "filename": "api_docs.md",
      "description": "API 接口文档（端点列表 / 请求响应示例 / 错误码）",
      "generator_method": "generate_api_docs",
      "required_fields": ["name", "version"],
      "optional_fields": ["base_url", "auth_type", "endpoints"],
      "output_extension": ".md",
      "priority": 9
    }
  ]
}
```

### 删除组件

从 `components` 数组中移除对应组件定义即可。建议在场景配置中通过 `default_components` 列表控制启用的组件：

```json
{
  "submission_components": {
    "default_components": [
      "readme",
      "demo_guide",
      "introduction",
      "faq",
      "trust_statement",
      "bundle_meta"
    ]
  }
}
```

### 修改组件

直接修改对应组件的字段值：

```json
{
  "components": [
    {
      "id": "readme",
      "required_fields": ["name", "version", "description", "author"],
      "optional_fields": ["tagline", "features", "tech_stack", "target_users", "license"]
    }
  ]
}
```

### 输出格式配置

```json
{
  "output_formats": ["markdown", "json", "html"],
  "default_format": "markdown",
  "output_directory": "submission_bundle"
}
```

**支持的格式：**
- `markdown` — Markdown 格式（`.md`）
- `json` — JSON 格式（`.json`）
- `html` — HTML 格式（`.html`）

---

## 使用场景配置模板

BOS-FS 预定义 3 个场景配置模板，覆盖常见安全服务交付场景。

### 场景 1：渗透测试 (pen-test)

**适用场景**：渗透测试服务交付

**核心特性：**
- 安全性维度权重 **35%**（默认 15%）
- 测试覆盖率要求提升（excellent: 90%）
- 安全缺陷加重惩罚（`security_vulnerability_multiplier: 1.5`）

**专属组件（8 默认 + 2 安全）：**

| 优先级 | 组件 | 说明 |
|--------|------|------|
| 9 | `security_report` | 渗透测试安全报告（测试范围/方法论/漏洞发现/风险评级/修复建议） |
| 10 | `remediation_guide` | 漏洞修复指南（按优先级排序的修复方案/代码示例/验证步骤） |

**安全检查项：**
- 10 种漏洞类型检测（SQL 注入/XSS/CSRF/认证绕过等）
- 最低安全评分要求：7/10
- 零日漏洞披露要求
- PoC 要求（可复现/非破坏性/含步骤/含证据）

**使用方式：**

```python
loader = ConfigLoader()
config = loader.load_scenario("pen-test")
security_weight = loader.get("reviewer_rules.review_types.technical.dimensions.安全性.weight")
# → 35
```

### 场景 2：代码审计 (code-audit)

**适用场景**：代码审计服务交付

**核心特性：**
- 代码质量维度权重 **35%**（默认 25%）
- 静态分析要求（SonarQube/ESLint/Bandit/SpotBugs）
- 代码复杂度限制（圈复杂度 ≤ 15）

**专属组件（8 默认 + 2 审计）：**

| 优先级 | 组件 | 说明 |
|--------|------|------|
| 9 | `audit_summary` | 代码审计总结报告（审计范围/方法论/问题统计/风险概览/总体评价） |
| 10 | `vulnerability_list` | 漏洞与问题清单（按严重程度排序/代码位置/修复建议） |

**代码质量检查：**
- 静态分析（最大允许问题数：blocker=0, critical=0, major=3）
- 圈复杂度 ≤ 15，认知复杂度 ≤ 20
- 函数长度 ≤ 50 行，类长度 ≤ 300 行
- 重复代码 ≤ 5%

**使用方式：**

```python
config = loader.load_scenario("code-audit")
code_quality_weight = loader.get("reviewer_rules.review_types.technical.dimensions.代码质量.weight")
# → 35
```

### 场景 3：漏洞台账 (vulnerability-ledger)

**适用场景**：漏洞台账管理

**核心特性：**
- 文档完整性权重 **30%**、可追溯性 **25%**
- 状态生命周期管理（9 种状态及转换规则）
- SLA 管理（P0: 4h, P1: 24h, P2: 72h, P3: 168h, P4: 720h）

**专属组件（8 默认 + 3 台账）：**

| 优先级 | 组件 | 说明 |
|--------|------|------|
| 9 | `ledger_report` | 漏洞台账总览报告（漏洞汇总/状态分布/SLA达成率/修复统计） |
| 10 | `trend_analysis` | 漏洞趋势分析（时间趋势/类型分布/模块分布/修复效率） |
| 11 | `status_tracker` | 漏洞状态跟踪器（当前状态清单/变更历史/超时预警/待办事项） |

**跟踪要求：**
- 12 个必填跟踪字段
- 状态转换规则验证
- 月度报告要求
- 数据质量要求（完整性 ≥ 95%，准确性 ≥ 98%）

**使用方式：**

```python
config = loader.load_scenario("vulnerability-ledger")
doc_weight = loader.get("reviewer_rules.review_types.technical.dimensions.文档完整性.weight")
# → 30
```

### 场景对比表

| 维度 | 默认 | pen-test | code-audit | vulnerability-ledger |
|------|------|----------|------------|---------------------|
| 安全性权重 | 15% | **35%** | 20% | 15% |
| 代码质量权重 | 25% | 20% | **35%** | 20% |
| 架构设计权重 | 25% | 20% | 20% | — |
| 文档完整性权重 | — | — | — | **30%** |
| 可追溯性权重 | — | — | — | **25%** |
| 专属组件数 | 0 | 2 | 2 | 3 |
| 总组件数 | 8 | 10 | 10 | 11 |
| 测试覆盖率(excellent) | 80% | **90%** | 85% | 80% |
| 最低安全/质量分 | — | 7 | 6 | — |

---

## 高级：创建自定义场景配置

### 场景配置文件结构

在 `engine/config/scenarios/` 目录下创建新的 JSON 文件：

```
engine/config/scenarios/
├── pen-test.json
├── code-audit.json
├── vulnerability-ledger.json
└── my-custom-scenario.json   ← 自定义场景
```

### 完整场景配置模板

```json
{
  "_comment": "自定义场景配置模板",
  "description": "场景描述",
  "scenario_id": "my-custom-scenario",
  "version": "1.0.0",

  "reviewer_rules": {
    "review_types": {
      "technical": {
        "dimensions": {
          "架构设计": {"weight": 25, "max": 10},
          "代码质量": {"weight": 30, "max": 10},
          "安全性": {"weight": 25, "max": 10},
          "技术栈": {"weight": 10, "max": 10},
          "依赖管理": {"weight": 10, "max": 10}
        }
      }
    },
    "thresholds": {
      "test_coverage": {"excellent": 85, "good": 70, "poor": 40},
      "text_length": {"detailed": 60, "moderate": 35, "brief": 25}
    },
    "defect_penalty": {
      "severity_curve": {
        "1": 1.0,
        "2": 1.1,
        "3": 1.4,
        "4": 1.8,
        "5+": "2.2 + (n-5) * 0.6"
      }
    }
  },

  "submission_components": {
    "default_components": [
      "readme", "demo_guide", "introduction", "screenshots_guide",
      "faq", "risk_disclosure", "trust_statement", "bundle_meta"
    ],
    "custom_components": [
      {
        "id": "custom_report",
        "filename": "custom_report.md",
        "description": "自定义报告",
        "generator_method": "generate_custom_report",
        "required_fields": ["name", "version"],
        "optional_fields": ["author"],
        "output_extension": ".md",
        "priority": 9,
        "mandatory": true
      }
    ],
    "total_required_components": 9,
    "consistency_check": {
      "enabled": true
    }
  },

  "scenario_thresholds": {
    "min_quality_score": 7,
    "require_test_coverage": true,
    "pass_criteria": {
      "all_critical_fixed": true,
      "all_high_fixed_or_mitigated": true
    }
  }
}
```

### 使用自定义场景

```python
loader = ConfigLoader()
config = loader.load_scenario("my-custom-scenario")
```

### 配置合并规则

场景配置仅覆盖与默认配置不同的部分，未指定的字段保持默认值：

```python
# 假设场景配置仅覆盖安全性权重
scenario = {
  "reviewer_rules": {
    "review_types": {
      "technical": {
        "dimensions": {
          "安全性": {"weight": 40, "max": 10}
        }
      }
    }
  }
}

# 合并后结果
merged = {
  "reviewer_rules": {
    "review_types": {
      "technical": {
        "dimensions": {
          "架构设计": {"weight": 25, "max": 10},  # 保持默认
          "技术栈":   {"weight": 20, "max": 10},  # 保持默认
          "代码质量": {"weight": 25, "max": 10},  # 保持默认
          "安全性":   {"weight": 40, "max": 10},  # 场景覆盖
          "依赖管理": {"weight": 15, "max": 10}   # 保持默认
        }
      }
    }
  }
}
```

---

## 配置加载优先级和覆盖规则

### 四级优先级

```
Level 0: 硬编码默认值（loader.py 中的 HARDCODED_DEFAULTS）
    ↓ 被覆盖
Level 1: JSON 默认值（config/defaults/*.json）
    ↓ 被覆盖
Level 2: 用户自定义配置（ConfigLoader(config_dir="/custom/path")）
    ↓ 被覆盖
Level 3: 场景配置（config/scenarios/*.json）
```

### 合并算法

采用深度递归合并（`ConfigLoader.merge()`）：

```python
def merge(base, override):
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge(result[key], value)  # 递归合并
        else:
            result[key] = value  # 直接覆盖
    return result
```

### 覆盖示例

**硬编码默认值：**
```json
{"reviewer_rules": {"thresholds": {"test_coverage": {"excellent": 80}}}}
```

**JSON 默认值覆盖：**
```json
{"reviewer_rules": {"thresholds": {"test_coverage": {"excellent": 85}}}}
```

**场景配置覆盖：**
```json
{"reviewer_rules": {"thresholds": {"test_coverage": {"excellent": 90}}}}
```

**最终结果：**
```json
{"reviewer_rules": {"thresholds": {"test_coverage": {"excellent": 90}}}}
```

### 加载流程

```
ConfigLoader.__init__()
    ↓
ConfigLoader.load_scenario("pen-test")
    ↓
1. load_all_defaults()
   ├── 复制 HARDCODED_DEFAULTS
   ├── 遍历 defaults/*.json
   └── merge(硬编码, JSON 默认) → base_config
    ↓
2. 读取 scenarios/pen-test.json
    ↓
3. merge(base_config, scenario_config) → 最终配置
    ↓
返回最终配置
```

---

## 常见问题排查

### Q1: 配置未生效

**问题**：修改了 JSON 配置文件，但运行结果未变化。

**排查步骤：**
1. 确认修改的文件路径正确（`config/defaults/` vs `config/scenarios/`）
2. 确认 JSON 语法正确（无多余逗号、引号匹配）
3. 调用 `loader.reload()` 清除缓存后重新加载
4. 使用 `loader.get("key.path")` 验证配置值是否正确加载

```python
loader.reload()
value = loader.get("reviewer_rules.thresholds.test_coverage.excellent")
print(f"Current value: {value}")  # 应显示新值
```

### Q2: 场景配置覆盖不生效

**问题**：加载场景配置后，部分维度权重未变化。

**原因**：场景配置仅覆盖显式指定的字段。

**解决方案**：确保场景配置中指定了完整的维度路径：

```json
{
  "reviewer_rules": {
    "review_types": {
      "technical": {
        "dimensions": {
          "安全性": {"weight": 35, "max": 10}
        }
      }
    }
  }
}
```

### Q3: 自定义组件未生成

**问题**：在 `submission_components.json` 中添加了新组件，但未生成对应文件。

**排查步骤：**
1. 确认组件定义包含所有必填字段（`id`, `filename`, `description`, `generator_method`, `required_fields`, `output_extension`, `priority`）
2. 确认 `generator_method` 方法在代码中已实现
3. 确认组件在场景的 `default_components` 列表中（如使用场景配置）

### Q4: JSON 解析错误

**问题**：运行时报 `json.decoder.JSONDecodeError`。

**常见原因：**
- JSON 文件中存在尾随逗号（`,`）
- 使用了单引号而非双引号
- 注释未使用 `_comment` 字段

**解决方案**：使用 JSON 校验工具验证文件语法：

```bash
python -m json.tool config/defaults/reviewer_rules.json
```

### Q5: 配置冲突检测

**问题**：多个配置项之间存在冲突。

**示例**：维度权重总和不等于 100%。

**建议**：添加配置校验脚本：

```python
def validate_reviewer_rules(config):
    dimensions = config.get("reviewer_rules.review_types.technical.dimensions", {})
    total_weight = sum(d.get("weight", 0) for d in dimensions.values())
    if total_weight != 100:
        print(f"警告: 维度权重总和为 {total_weight}%，应为 100%")
    return total_weight == 100
```

### Q6: 如何查看所有已加载的配置

```python
# 加载并打印全部配置
loader = ConfigLoader()
config = loader.load_all_defaults()
import json
print(json.dumps(config, indent=2, ensure_ascii=False))
```

### Q7: 如何在不同环境使用不同配置

```python
import os

env = os.getenv("BOS_FS_ENV", "development")
config_dir = f"config/envs/{env}"
loader = ConfigLoader(config_dir=config_dir)
```

目录结构：
```
config/
├── defaults/          # 通用默认配置
├── envs/
│   ├── development/   # 开发环境配置
│   ├── staging/       # 预发环境配置
│   └── production/    # 生产环境配置
└── scenarios/         # 场景配置
```
