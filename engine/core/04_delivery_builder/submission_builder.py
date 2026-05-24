"""Submission Builder - Generate 8-component submission documentation bundles."""

import os
import json
from datetime import datetime
from typing import Dict, List


class SubmissionBuilder:
    """构建项目提交流程所需的 8 组件文档包。"""

    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or os.path.join(
            os.getcwd(), "submission_bundle"
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(self, project_info: dict) -> dict:
        """生成完整的提交文档包并写入磁盘。

        Args:
            project_info: 项目元信息，建议包含 name, version, description,
                features, target_users, tech_stack, tagline 等。

        Returns:
            {"bundle_path": str, "components": list[str], "status": "complete"}
        """
        os.makedirs(self.output_dir, exist_ok=True)

        # 1) 全局一致性检查
        issues = self._check_consistency(project_info)

        # 2) 生成 8 个组件
        generators = [
            ("README.md", self.generate_readme),
            ("demo_guide.md", self.generate_demo_guide),
            ("introduction.md", self.generate_introduction),
            ("screenshots_guide.md", self.generate_screenshots_guide),
            ("FAQ.md", self.generate_faq),
            ("risk_disclosure.md", self.generate_risk_disclosure),
            ("trust_statement.md", self.generate_trust_statement),
            ("bundle_meta.json", self.generate_meta),
        ]

        components: List[str] = []
        content_cache: Dict[str, str] = {}

        for filename, generator in generators:
            content = generator(project_info)
            content_cache[filename] = content
            path = os.path.join(self.output_dir, filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            components.append(filename)

        # 3) 一致性报告（附加写入）
        if issues:
            report = f"# 一致性检查报告\n\n发现 {len(issues)} 个问题:\n\n"
            for idx, issue in enumerate(issues, 1):
                report += f"{idx}. {issue}\n"
        else:
            report = "# 一致性检查报告\n\n所有组件一致性通过。"

        report_path = os.path.join(self.output_dir, "consistency_report.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)

        status = "complete" if not issues else "complete_with_warnings"

        return {
            "bundle_path": self.output_dir,
            "components": components,
            "status": status,
        }

    # ------------------------------------------------------------------
    # 8 component generators
    # ------------------------------------------------------------------

    def generate_readme(self, project_info: dict) -> str:
        """生成 5 段式 README.md（概述 / 特性 / 快速开始 / 架构 / 许可）。"""
        name = project_info.get("name", "BOS-FS-Project")
        version = project_info.get("version", "0.1.0")
        tagline = project_info.get("tagline", "")
        desc = project_info.get("description", "待补充项目描述。")
        features = project_info.get("features", [])
        tech_stack = project_info.get("tech_stack", [])
        target_users = project_info.get("target_users", "待定义")

        features_md = "".join(f"- {f}\n" for f in features) if features else "- 待补充\n"
        tech_md = "".join(f"- {t}\n" for t in tech_stack) if tech_stack else "- 待补充\n"

        return f"""# {name}

{tagline}

> **Version**: {version}

## 1. 概述

{desc}

**目标用户**: {target_users}

## 2. 功能特性

{features_md}
## 3. 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动项目
python main.py
```

详细演示步骤请参阅 `demo_guide.md`。

## 4. 技术架构

{tech_md}
## 5. 许可证

内部项目，未经授权请勿外传。
"""

    def generate_demo_guide(self, project_info: dict) -> str:
        """生成演示 / 安装指南。"""
        name = project_info.get("name", "项目")
        version = project_info.get("version", "0.1.0")
        tagline = project_info.get("tagline", "")
        features = project_info.get("features", [])
        tech_stack = project_info.get("tech_stack", [])

        feature_steps = ""
        for idx, feat in enumerate(features[:5], 1):
            feature_steps += f"### Step {idx}: {feat}\n\n按照业务场景完成该功能操作并验证结果。\n\n"

        env_reqs = "\n".join(f"- {t}" for t in tech_stack) if tech_stack else "- 参考项目要求"

        tagline_line = f"\n> {tagline}\n" if tagline else ""

        return f"""# {name} v{version} — 演示与安装指南
{tagline_line}
## 环境准备

1. Python 3.9+ 运行环境
2. 满足以下技术栈要求：
{env_reqs}

## 安装步骤

```bash
# 1. 克隆项目
git clone <repository_url>
cd {name}

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量（如需要）
cp .env.example .env
```

## 演示流程

{feature_steps}
## 验证与排查

| 检查项 | 预期结果 |
|--------|----------|
| 服务启动 | 控制台无报错，服务正常监听 |
| 核心接口 | 返回 200 状态码 |
| 数据持久化 | 数据库记录正确写入 |

如遇问题，请查看 `FAQ.md` 获取帮助。
"""

    def generate_introduction(self, project_info: dict) -> str:
        """生成项目推介 / 介绍文档。"""
        name = project_info.get("name", "项目")
        version = project_info.get("version", "0.1.0")
        tagline = project_info.get("tagline", "")
        desc = project_info.get("description", "待补充")
        value = project_info.get("value_proposition", "提升效率、降低门槛、标准化交付")
        target_users = project_info.get("target_users", "待定义")

        return f"""# {name} 项目介绍

> {tagline}

**版本**: {version}

## 项目概述

{desc}

## 核心价值主张

{value}

## 目标用户

{target_users}

## 架构亮点

- **模块化设计**: 各组件独立可替换，支持按需扩展
- **标准化流程**: 减少人为错误，确保交付一致性
- **开箱即用**: 最小配置即可启动完整工作流
- **可审计性**: 全流程留痕，便于追溯与复盘

## 适用场景

- 项目交付标准化与自动化
- 跨团队协作文档统一管理
- 自动化提交包与评审材料生成
- 内部知识库沉淀与复用
"""

    def generate_screenshots_guide(self, project_info: dict) -> str:
        """生成截图规范与指南。"""
        name = project_info.get("name", "项目")
        version = project_info.get("version", "0.1.0")
        tagline = project_info.get("tagline", "")
        features = project_info.get("features", [])

        checklist_items = ""
        default_items = [
            "项目首页 / Dashboard",
            "核心功能操作界面",
            "配置 / 设置页面",
            "输出结果展示",
            "异常处理 / 错误提示示例",
        ]
        all_items = (default_items + features) if features else default_items
        for idx, item in enumerate(all_items, 1):
            checklist_items += f"{idx}. {item}\n"

        tagline_line = f"\n> {tagline}\n" if tagline else ""

        return f"""# {name} v{version} — 截图指南
{tagline_line}
## 截图规范

| 场景 | 要求 | 推荐格式 |
|------|------|----------|
| 主界面 | 完整窗口，含导航栏 | PNG 1920×1080 |
| 核心流程 | 关键步骤逐帧截图 | PNG 或 GIF 动图 |
| 异常处理 | 错误提示 + 解决路径 | PNG |
| 数据展示 | 含真实/模拟数据 | PNG |

## 建议截图清单

{checklist_items}
## 存放路径

将截图统一存放于 `{name}/assets/screenshots/` 目录下，命名规则：

```
<模块名>_<序号>_<简短描述>.png
```

示例: `dashboard_01_overview.png`

## 注意事项

- 截图中不得包含敏感数据（密钥、个人信息等）
- 建议使用演示环境或脱敏后的数据进行截图
- 保持截图风格一致（主题、分辨率、语言）
"""

    def generate_faq(self, project_info: dict) -> str:
        """生成 10 条 FAQ 问答。"""
        name = project_info.get("name", "项目")
        version = project_info.get("version", "0.1.0")
        tagline = project_info.get("tagline", "")

        tagline_line = f"\n> {tagline}\n" if tagline else ""

        return f"""# {name} v{version} — 常见问题 (FAQ)
{tagline_line}
## Q1: {name} 的运行环境要求是什么？

**A**: 需要 Python 3.9+ 运行环境。具体依赖请参阅项目根目录的 `requirements.txt`。推荐使用虚拟环境（venv / conda）隔离依赖。

## Q2: 如何快速上手使用 {name}？

**A**: 请按照 `demo_guide.md` 中的安装步骤操作，3 步即可完成环境搭建并运行首个演示流程。

## Q3: 是否支持自定义文档模板？

**A**: 支持。本项目采用模块化架构，您可以继承对应 Builder 类并覆盖生成方法，或通过配置文件自定义模板参数。

## Q4: 提交后审核不通过如何处理？

**A**: 请参考项目中的审核分析模块，查看具体拒绝原因。常见问题包括：描述不完整、缺少截图、风险披露不充分等。针对性修改后重新提交即可。

## Q5: {name} 是否支持批量生成提交文档？

**A**: 支持。可传入多个 `project_info` 字典，循环调用 `build()` 方法实现批量生成。

## Q6: 生成的文档支持哪些输出格式？

**A**: 当前默认输出 Markdown 格式（.md），JSON 元数据格式（.json）。如需 PDF 或 HTML 格式，可使用第三方 Markdown 转换工具进行后处理。

## Q7: 项目中的数据和隐私如何保障？

**A**: {name} 采用本地运行模式，所有数据保留在您的环境中，不上传任何外部服务器。演示数据与生产数据严格隔离。

## Q8: 如何进行版本升级？

**A**: 关注项目发布的 Release 说明，按照升级指南执行 `pip install --upgrade` 或手动替换最新版本文件。升级前建议备份现有配置。

## Q9: 是否提供 API 或 SDK 供其他系统集成？

**A**: 当前版本主要面向命令行和脚本调用。后续版本计划提供 RESTful API 和 Python SDK，便于与其他系统（CI/CD、项目管理平台等）集成。

## Q10: 如何报告 Bug 或提交功能建议？

**A**: 请通过项目 Issues 页面提交问题描述（包含复现步骤、环境信息、预期与实际行为）。功能建议请标注 `[Feature Request]` 标签。
"""

    def generate_risk_disclosure(self, project_info: dict) -> str:
        """生成风险披露（技术 / 市场 / 合规）。"""
        name = project_info.get("name", "项目")
        version = project_info.get("version", "0.1.0")
        tagline = project_info.get("tagline", "")

        tagline_line = f"\n> {tagline}\n" if tagline else ""

        return f"""# {name} v{version} — 风险披露声明
{tagline_line}
## 一、技术风险

### 1.1 已知限制

- 当前版本为预发布版本，部分功能仍在持续迭代中
- 大规模数据场景下的性能表现需进一步验证和优化
- 暂未覆盖所有边界情况的异常处理

### 1.2 兼容性风险

- 建议在 Python 3.9+ 环境下运行
- 未在其他 Python 版本或操作系统上充分测试
- 第三方依赖库的版本冲突可能导致运行异常

### 1.3 安全风险

- 请确保运行环境的防火墙和安全策略已正确配置
- 建议定期更新依赖库以修复已知安全漏洞
- 生产环境部署前请进行完整的安全审计

## 二、市场风险

### 2.1 竞争环境

- 同类解决方案可能已存在市场竞品
- 技术演进速度可能影响产品的长期竞争力
- 用户需求变化可能导致功能方向的调整

### 2.2 采用门槛

- 用户需要一定的技术背景才能充分利用全部功能
- 从现有流程迁移可能需要额外的学习和适配成本

## 三、合规风险

### 3.1 数据合规

- 请确保使用本项目时遵守适用的数据保护法规（如《个人信息保护法》、GDPR 等）
- 处理敏感数据时请采取额外的加密和脱敏措施

### 3.2 许可证合规

- 本项目使用的第三方依赖库均遵循各自的开源许可证
- 使用前请确认各依赖许可证与您项目的兼容性

## 四、免责声明

本项目按"现状"（AS IS）提供，作者及贡献者不对因使用本项目产生的任何直接、间接、附带或后果性损失承担责任。使用者应自行评估风险并采取适当的防护措施。
"""

    def generate_trust_statement(self, project_info: dict) -> str:
        """生成信任声明，引用 OWASP、Clean Architecture、ISO 25010 等权威框架。"""
        name = project_info.get("name", "项目")
        version = project_info.get("version", "0.1.0")
        tagline = project_info.get("tagline", "")

        return f"""# {name} v{version} — 信任声明

> {tagline}

## 安全承诺

本项目在设计与开发过程中严格遵循以下安全原则与最佳实践：

- **OWASP Top 10** (2021): 针对十大 Web 应用安全风险（注入、认证失效、敏感数据泄露等）进行了防护设计
- **OWASP ASVS**: 参照应用安全验证标准 4.0 进行安全控制分级
- **最小权限原则**: 所有操作默认采用最小权限模型，避免过度授权

## 架构原则

项目架构遵循业界公认的软件工程标准：

- **Clean Architecture** (Robert C. Martin): 采用依赖倒置和分层架构，确保核心业务逻辑与外部框架解耦，提升可测试性和可维护性
- **SOLID 原则**: 单一职责、开闭原则、里氏替换、接口隔离、依赖倒置——贯穿代码设计全过程
- **十二要素应用** (12-Factor App): 在配置管理、依赖声明、日志处理等方面遵循云原生最佳实践

## 质量保障

软件质量维度参考国际标准 **ISO/IEC 25010** 进行评估：

| 质量特性 | 保障措施 |
|----------|----------|
| 功能适用性 | 需求可追溯，覆盖核心业务场景 |
| 性能效率 | 关键路径性能监控，资源使用优化 |
| 兼容性 | 标准化接口设计，版本向后兼容 |
| 可靠性 | 异常处理全覆盖，故障恢复机制 |
| 安全性 | 输入校验、权限控制、数据加密 |
| 可维护性 | 模块化设计、代码规范、自动化测试 |
| 可移植性 | 无硬编码环境依赖，容器化部署支持 |

## 透明度

- 项目代码可审计，关键模块附有设计文档
- 变更日志（CHANGELOG）记录所有重要修改
- 第三方依赖清单（SBOM）公开可查

## 持续改进

我们承诺：

1. 定期审查并更新安全策略以应对新兴威胁
2. 积极响应用户报告的安全问题和功能缺陷
3. 持续跟踪业界标准更新并及时适配

---

*本声明基于项目发布时的已知信息，将随项目演进而持续更新。*
"""

    def generate_meta(self, project_info: dict) -> str:
        """生成 bundle_meta.json 元数据。"""
        name = project_info.get("name", "BOS-FS-Project")
        version = project_info.get("version", "0.1.0")
        tagline = project_info.get("tagline", "")
        desc = project_info.get("description", "")
        target_users = project_info.get("target_users", "")
        tech_stack = project_info.get("tech_stack", [])
        features = project_info.get("features", [])

        meta = {
            "project_name": name,
            "version": version,
            "tagline": tagline,
            "description": desc,
            "target_users": target_users,
            "tech_stack": tech_stack,
            "features": features,
            "components": [
                "README.md",
                "demo_guide.md",
                "introduction.md",
                "screenshots_guide.md",
                "FAQ.md",
                "risk_disclosure.md",
                "trust_statement.md",
                "bundle_meta.json",
            ],
            "generated_at": datetime.now().isoformat(),
            "builder_version": "1.0.0",
        }

        return json.dumps(meta, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _check_consistency(self, project_info: dict) -> list:
        """全局一致性检查：验证 name / version / tagline 在所有组件中一致。

        Returns:
            不一致问题列表，空列表表示全部通过。
        """
        issues: List[str] = []
        name = project_info.get("name", "")
        version = project_info.get("version", "")
        tagline = project_info.get("tagline", "")

        if not name:
            issues.append("project_info 缺少必填字段: name")
        if not version:
            issues.append("project_info 缺少必填字段: version")

        # 生成所有组件内容后交叉校验
        generators = {
            "README.md": self.generate_readme,
            "demo_guide.md": self.generate_demo_guide,
            "introduction.md": self.generate_introduction,
            "screenshots_guide.md": self.generate_screenshots_guide,
            "FAQ.md": self.generate_faq,
            "risk_disclosure.md": self.generate_risk_disclosure,
            "trust_statement.md": self.generate_trust_statement,
            "bundle_meta.json": self.generate_meta,
        }

        content_cache = {}
        for fname, gen in generators.items():
            content_cache[fname] = gen(project_info)

        # 校验 name 一致性
        if name:
            for fname, content in content_cache.items():
                if fname.endswith(".json"):
                    meta = json.loads(content)
                    if meta.get("project_name") != name:
                        issues.append(f"{fname} 中 project_name 不一致")
                else:
                    if name not in content:
                        issues.append(f"{fname} 中未包含项目名称: {name}")

        # 校验 version 一致性
        if version:
            for fname, content in content_cache.items():
                if fname.endswith(".json"):
                    meta = json.loads(content)
                    if meta.get("version") != version:
                        issues.append(f"{fname} 中 version 不一致")
                else:
                    if version not in content:
                        issues.append(f"{fname} 中未包含版本号: {version}")

        # 校验 tagline 一致性（仅在提供时检查）
        if tagline:
            for fname, content in content_cache.items():
                if fname.endswith(".json"):
                    meta = json.loads(content)
                    if meta.get("tagline") != tagline:
                        issues.append(f"{fname} 中 tagline 不一致")
                else:
                    if tagline not in content:
                        issues.append(f"{fname} 中未包含标语: {tagline}")

        return issues


if __name__ == "__main__":
    sample_info = {
        "name": "BOS-FS",
        "version": "1.0.0",
        "tagline": "标准化项目交付与提交文档自动化平台",
        "description": "BOS-FS 是一套面向企业级项目的自动化交付文档生成系统，整合需求分析、代码审查、质量评估、提交包构建等全链路环节。",
        "features": [
            "一键生成 8 组件标准化提交文档包",
            "审核拒绝原因自动分析与修复建议",
            "模块化可扩展架构，支持自定义模板",
            "全局一致性自动校验",
            "开箱即用的演示与安装指南",
        ],
        "target_users": "项目经理、交付工程师、研发团队、QA 人员",
        "tech_stack": ["Python 3.9+", "Markdown", "JSON", "Git"],
        "value_proposition": "将手动整理提交文档的时间从小时级压缩到分钟级，实现标准化、可审计、可复用的项目交付流程。",
    }

    builder = SubmissionBuilder()
    result = builder.build(sample_info)
    print(json.dumps(result, ensure_ascii=False, indent=2))
