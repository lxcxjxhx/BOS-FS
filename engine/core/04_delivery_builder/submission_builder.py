"""Submission Builder - Generate configurable component submission documentation bundles."""

import os
import json
from datetime import datetime
from typing import Dict, List, Callable, Optional, Any

try:
    from engine.config import ConfigLoader
except ImportError:
    ConfigLoader = None


class SubmissionBuilder:
    """构建项目提交流程所需的可配置组件文档包。"""

    DEFAULT_COMPONENTS = [
        {"filename": "README.md", "generator_method": "generate_readme", "enabled": True},
        {"filename": "demo_guide.md", "generator_method": "generate_demo_guide", "enabled": True},
        {"filename": "introduction.md", "generator_method": "generate_introduction", "enabled": True},
        {"filename": "screenshots_guide.md", "generator_method": "generate_screenshots_guide", "enabled": True},
        {"filename": "FAQ.md", "generator_method": "generate_faq", "enabled": True},
        {"filename": "risk_disclosure.md", "generator_method": "generate_risk_disclosure", "enabled": True},
        {"filename": "trust_statement.md", "generator_method": "generate_trust_statement", "enabled": True},
        {"filename": "bundle_meta.json", "generator_method": "generate_meta", "enabled": True},
    ]

    HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.6; color: #333; }}
        h1 {{ border-bottom: 2px solid #eaecef; padding-bottom: 0.3em; }}
        h2 {{ border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
        pre {{ background: #f6f8fa; padding: 16px; border-radius: 6px; overflow-x: auto; }}
        code {{ background: #f6f8fa; padding: 0.2em 0.4em; border-radius: 3px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #dfe2e5; padding: 8px; text-align: left; }}
        th {{ background: #f6f8fa; }}
        blockquote {{ border-left: 4px solid #dfe2e5; margin: 0; padding: 0 1em; color: #6a737d; }}
    </style>
</head>
<body>
{body}
</body>
</html>"""

    def __init__(
        self,
        output_dir: str = None,
        config_path: str = None,
    ):
        self.output_dir = output_dir or os.path.join(os.getcwd(), "submission_bundle")
        self.config_path = config_path
        self._component_registry: Dict[str, Callable] = {}
        self._components_config: List[dict] = list(self.DEFAULT_COMPONENTS)
        self._screenshot_resolution = (1920, 1080)
        self._default_placeholders: Dict[str, Any] = {
            "name": "BOS-FS-Project",
            "version": "0.1.0",
            "tagline": "",
            "description": "待补充项目描述。",
            "features": [],
            "tech_stack": [],
            "target_users": "待定义",
            "value_proposition": "提升效率、降低门槛、标准化交付",
        }

        self._load_config()

    def _load_config(self) -> None:
        """加载配置文件，覆盖默认组件列表和设置。"""
        if self.config_path and os.path.isfile(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except (json.JSONDecodeError, OSError):
                return

            if "components" in config and isinstance(config["components"], list):
                self._components_config = config["components"]

            if "screenshot_resolution" in config:
                res = config["screenshot_resolution"]
                if isinstance(res, (list, tuple)) and len(res) == 2:
                    self._screenshot_resolution = (int(res[0]), int(res[1]))

            if "default_placeholders" in config and isinstance(config["default_placeholders"], dict):
                self._default_placeholders.update(config["default_placeholders"])

        else:
            bundled_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "config",
                "submission_components.json",
            )
            if os.path.isfile(bundled_path):
                try:
                    with open(bundled_path, "r", encoding="utf-8") as f:
                        config = json.load(f)
                    if "components" in config and isinstance(config["components"], list):
                        self._components_config = config["components"]
                    if "screenshot_resolution" in config:
                        res = config["screenshot_resolution"]
                        if isinstance(res, (list, tuple)) and len(res) == 2:
                            self._screenshot_resolution = (int(res[0]), int(res[1]))
                    if "default_placeholders" in config and isinstance(config["default_placeholders"], dict):
                        self._default_placeholders.update(config["default_placeholders"])
                except (json.JSONDecodeError, OSError):
                    pass

    def register_component(self, name: str, generator_func: Callable[[dict], str]) -> None:
        """注册自定义组件生成器。

        Args:
            name: 组件文件名（如 my_component.md）
            generator_func: 接受 project_info dict，返回内容字符串的函数
        """
        self._component_registry[name] = generator_func

    def add_component(self, filename: str, generator_method: str, enabled: bool = True) -> None:
        """动态添加组件到配置列表。"""
        self._components_config.append({
            "filename": filename,
            "generator_method": generator_method,
            "enabled": enabled,
        })

    def remove_component(self, filename: str) -> bool:
        """动态移除组件。"""
        original_len = len(self._components_config)
        self._components_config = [
            c for c in self._components_config if c.get("filename") != filename
        ]
        return len(self._components_config) < original_len

    def enable_component(self, filename: str) -> bool:
        for comp in self._components_config:
            if comp.get("filename") == filename:
                comp["enabled"] = True
                return True
        return False

    def disable_component(self, filename: str) -> bool:
        for comp in self._components_config:
            if comp.get("filename") == filename:
                comp["enabled"] = False
                return True
        return False

    def build(self, project_info: dict, output_format: str = "markdown") -> dict:
        """生成完整的提交文档包并写入磁盘。

        Args:
            project_info: 项目元信息，建议包含 name, version, description,
                features, target_users, tech_stack, tagline 等。
            output_format: 输出格式，支持 "markdown"（默认）、"json"、"html"。

        Returns:
            markdown/json: {"bundle_path": str, "components": list[str], "status": "complete"}
            html: 同上，但文件扩展名为 .html
        """
        os.makedirs(self.output_dir, exist_ok=True)

        issues = self._check_consistency(project_info)

        active_components = [c for c in self._components_config if c.get("enabled", True)]

        components: List[str] = []
        content_cache: Dict[str, str] = {}

        for comp_config in active_components:
            filename = comp_config.get("filename", "")
            method_name = comp_config.get("generator_method", "")
            if not filename or not method_name:
                continue

            content = self._resolve_generator(method_name)(project_info)
            content_cache[filename] = content

            output_filename = self._adapt_filename(filename, output_format)
            path = os.path.join(self.output_dir, output_filename)

            adapted_content = self._adapt_content(content, filename, output_format)

            with open(path, "w", encoding="utf-8") as f:
                f.write(adapted_content)
            components.append(output_filename)

        if issues:
            report = f"# 一致性检查报告\n\n发现 {len(issues)} 个问题:\n\n"
            for idx, issue in enumerate(issues, 1):
                report += f"{idx}. {issue}\n"
        else:
            report = "# 一致性检查报告\n\n所有组件一致性通过。"

        report_filename = self._adapt_filename("consistency_report.md", output_format)
        report_path = os.path.join(self.output_dir, report_filename)
        report_content = self._adapt_content(report, "consistency_report.md", output_format)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        issue_count = len(issues)
        expected_count = len(self.DEFAULT_COMPONENTS)
        if issue_count == 0 and len(components) == expected_count:
            status = "complete"
        elif issue_count <= 3:
            status = "partial"
        else:
            status = "error"

        if output_format == "json":
            return self._build_json_output(project_info, content_cache, issues, status)

        return {
            "bundle_path": self.output_dir,
            "components": components,
            "status": status,
        }

    def _resolve_generator(self, method_name: str) -> Callable:
        """解析生成器方法名到实际可调用对象。"""
        if hasattr(self, method_name):
            return getattr(self, method_name)
        if method_name in self._component_registry:
            return self._component_registry[method_name]
        return lambda _: f"<!-- 未找到生成器: {method_name} -->"

    def _adapt_filename(self, filename: str, output_format: str) -> str:
        """根据输出格式调整文件扩展名。"""
        if output_format == "html" and filename.endswith(".md"):
            return filename[:-3] + ".html"
        return filename

    def _adapt_content(self, content: str, filename: str, output_format: str) -> str:
        """根据输出格式适配内容。"""
        if output_format == "html" and filename.endswith(".md"):
            return self._markdown_to_html(content)
        if output_format == "json" and filename.endswith(".md"):
            return content
        return content

    def _markdown_to_html(self, markdown_content: str) -> str:
        """将 Markdown 内容转换为基本 HTML。"""
        lines = markdown_content.split("\n")
        html_lines = []
        in_code_block = False
        in_list = False
        in_table = False

        for line in lines:
            if line.strip().startswith("```"):
                if in_code_block:
                    html_lines.append("</code></pre>")
                    in_code_block = False
                else:
                    if in_list:
                        html_lines.append("</ul>")
                        in_list = False
                    if in_table:
                        html_lines.append("</table>")
                        in_table = False
                    lang = line.strip()[3:].strip()
                    html_lines.append(f'<pre><code class="language-{lang}">')
                    in_code_block = True
                continue

            if in_code_block:
                html_lines.append(self._escape_html(line))
                continue

            if line.startswith("|") and line.strip().endswith("|"):
                if not in_table:
                    html_lines.append("<table>")
                    in_table = True
                cells = [c.strip() for c in line.split("|")[1:-1]]
                if all(c.startswith("-") or c == "---" for c in cells):
                    continue
                tag = "th" if not any(l.startswith("|") and not l.startswith("|---") for l in lines) else "td"
                row_cells = "".join(f"<{tag}>{self._escape_html(c)}</{tag}>" for c in cells)
                if not html_lines or not html_lines[-1].startswith("<table>"):
                    prev = html_lines[-1] if html_lines else ""
                    if prev.startswith("<tr>"):
                        tag = "td"
                html_lines.append(f"<tr>{row_cells}</tr>")
                continue
            elif in_table:
                html_lines.append("</table>")
                in_table = False

            if line.startswith("# "):
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<h1>{self._escape_html(line[2:])}</h1>")
            elif line.startswith("## "):
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<h2>{self._escape_html(line[3:])}</h2>")
            elif line.startswith("### "):
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<h3>{self._escape_html(line[4:])}</h3>")
            elif line.startswith("#### "):
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<h4>{self._escape_html(line[5:])}</h4>")
            elif line.startswith("> "):
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<blockquote>{self._escape_html(line[2:])}</blockquote>")
            elif line.startswith("- "):
                if not in_list:
                    html_lines.append("<ul>")
                    in_list = True
                html_lines.append(f"<li>{self._inline_markdown_to_html(self._escape_html(line[2:]))}</li>")
            elif line.strip() == "":
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
            else:
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                if line.strip():
                    html_lines.append(f"<p>{self._inline_markdown_to_html(self._escape_html(line))}</p>")

        if in_code_block:
            html_lines.append("</code></pre>")
        if in_list:
            html_lines.append("</ul>")
        if in_table:
            html_lines.append("</table>")

        title = "Submission Document"
        for l in lines:
            if l.startswith("# "):
                title = l[2:].strip()
                break

        body = "\n".join(html_lines)
        return self.HTML_TEMPLATE.format(title=self._escape_html(title), body=body)

    def _escape_html(self, text: str) -> str:
        """转义 HTML 特殊字符。"""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    def _inline_markdown_to_html(self, text: str) -> str:
        """转换行内 Markdown 语法（粗体、斜体、行内代码）为 HTML。"""
        import re
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
        return text

    def _build_json_output(
        self,
        project_info: dict,
        content_cache: Dict[str, str],
        issues: List[str],
        status: str,
    ) -> dict:
        """构建 JSON 格式的结构化输出。"""
        return {
            "bundle_path": self.output_dir,
            "components": {
                filename: content
                for filename, content in content_cache.items()
            },
            "consistency_issues": issues,
            "metadata": {
                "project_name": project_info.get("name", ""),
                "version": project_info.get("version", ""),
                "generated_at": datetime.now().isoformat(),
                "screenshot_resolution": f"{self._screenshot_resolution[0]}x{self._screenshot_resolution[1]}",
                "component_count": len(content_cache),
            },
            "status": status,
        }

    def _get_with_default(self, project_info: dict, key: str) -> Any:
        """获取项目信息，缺失时使用配置中的默认值。"""
        value = project_info.get(key)
        if value is not None:
            return value
        return self._default_placeholders.get(key)

    # ------------------------------------------------------------------
    # 8 component generators
    # ------------------------------------------------------------------

    def generate_readme(self, project_info: dict) -> str:
        """生成 5 段式 README.md（概述 / 特性 / 快速开始 / 架构 / 许可）。"""
        name = self._get_with_default(project_info, "name")
        version = self._get_with_default(project_info, "version")
        tagline = self._get_with_default(project_info, "tagline")
        desc = self._get_with_default(project_info, "description")
        features = self._get_with_default(project_info, "features")
        tech_stack = self._get_with_default(project_info, "tech_stack")
        target_users = self._get_with_default(project_info, "target_users")

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
        name = self._get_with_default(project_info, "name")
        version = self._get_with_default(project_info, "version")
        tagline = self._get_with_default(project_info, "tagline")
        features = self._get_with_default(project_info, "features")
        tech_stack = self._get_with_default(project_info, "tech_stack")

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
        name = self._get_with_default(project_info, "name")
        version = self._get_with_default(project_info, "version")
        tagline = self._get_with_default(project_info, "tagline")
        desc = self._get_with_default(project_info, "description")
        value = self._get_with_default(project_info, "value_proposition")
        target_users = self._get_with_default(project_info, "target_users")

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
        name = self._get_with_default(project_info, "name")
        version = self._get_with_default(project_info, "version")
        tagline = self._get_with_default(project_info, "tagline")
        features = self._get_with_default(project_info, "features")
        res_w, res_h = self._screenshot_resolution

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
| 主界面 | 完整窗口，含导航栏 | PNG {res_w}x{res_h} |
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
        name = self._get_with_default(project_info, "name")
        version = self._get_with_default(project_info, "version")
        tagline = self._get_with_default(project_info, "tagline")

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
        name = self._get_with_default(project_info, "name")
        version = self._get_with_default(project_info, "version")
        tagline = self._get_with_default(project_info, "tagline")

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
        name = self._get_with_default(project_info, "name")
        version = self._get_with_default(project_info, "version")
        tagline = self._get_with_default(project_info, "tagline")

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
        name = self._get_with_default(project_info, "name")
        version = self._get_with_default(project_info, "version")
        tagline = self._get_with_default(project_info, "tagline")
        desc = self._get_with_default(project_info, "description")
        target_users = self._get_with_default(project_info, "target_users")
        tech_stack = self._get_with_default(project_info, "tech_stack")
        features = self._get_with_default(project_info, "features")

        generated_at = datetime.now().isoformat()
        res_w, res_h = self._screenshot_resolution

        meta = {
            "project_name": name,
            "version": version,
            "tagline": tagline,
            "description": desc,
            "target_users": target_users,
            "tech_stack": tech_stack,
            "features": features,
            "goal": project_info.get("goal", {}),
            "components": [
                c["filename"]
                for c in self._components_config
                if c.get("enabled", True)
            ],
            "generated_at": generated_at,
            "build_date": generated_at,
            "builder_version": "1.0.0",
            "screenshot_resolution": f"{res_w}x{res_h}",
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
        name = self._get_with_default(project_info, "name")
        version = self._get_with_default(project_info, "version")
        tagline = self._get_with_default(project_info, "tagline")

        if not name or name == self._default_placeholders.get("name"):
            issues.append("project_info 缺少有效值: name")
        if not version or version == self._default_placeholders.get("version"):
            issues.append("project_info 缺少有效值: version")

        active_components = [c for c in self._components_config if c.get("enabled", True)]

        generators = {}
        for comp in active_components:
            method_name = comp.get("generator_method", "")
            filename = comp.get("filename", "")
            if method_name and filename:
                generators[filename] = self._resolve_generator(method_name)

        content_cache = {}
        for fname, gen in generators.items():
            content_cache[fname] = gen(project_info)

        if name and name != self._default_placeholders.get("name"):
            for fname, content in content_cache.items():
                if fname.endswith(".json"):
                    try:
                        meta = json.loads(content)
                        if meta.get("project_name") != name:
                            issues.append(f"{fname} 中 project_name 不一致")
                    except json.JSONDecodeError:
                        pass
                else:
                    if name not in content:
                        issues.append(f"{fname} 中未包含项目名称: {name}")

        if version and version != self._default_placeholders.get("version"):
            for fname, content in content_cache.items():
                if fname.endswith(".json"):
                    try:
                        meta = json.loads(content)
                        if meta.get("version") != version:
                            issues.append(f"{fname} 中 version 不一致")
                    except json.JSONDecodeError:
                        pass
                else:
                    if version not in content:
                        issues.append(f"{fname} 中未包含版本号: {version}")

        if tagline:
            for fname, content in content_cache.items():
                if fname.endswith(".json"):
                    try:
                        meta = json.loads(content)
                        if meta.get("tagline") != tagline:
                            issues.append(f"{fname} 中 tagline 不一致")
                    except json.JSONDecodeError:
                        pass
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

    print("\n--- HTML Output Demo ---")
    builder_html = SubmissionBuilder(output_dir="submission_bundle_html")
    result_html = builder_html.build(sample_info, output_format="html")
    print(json.dumps(result_html, ensure_ascii=False, indent=2))

    print("\n--- JSON Output Demo ---")
    builder_json = SubmissionBuilder(output_dir="submission_bundle_json")
    result_json = builder_json.build(sample_info, output_format="json")
    print(f"Status: {result_json['status']}, Components: {len(result_json['components'])}")

    print("\n--- Custom Component Demo ---")
    def my_changelog_generator(info: dict) -> str:
        return f"# Changelog for {info.get('name', 'Project')}\n\n## v{info.get('version', '0.1.0')}\n\n- Initial release"

    builder_custom = SubmissionBuilder()
    builder_custom.register_component("changelog.md", my_changelog_generator)
    builder_custom.add_component("changelog.md", "my_changelog_generator")
    result_custom = builder_custom.build(sample_info)
    print(json.dumps(result_custom, ensure_ascii=False, indent=2))
