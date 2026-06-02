"""README Refactor Engine — 将任意 README 重构为 What/Why/How/Result/Next 标准结构。"""

import re
from typing import Dict, List, Optional


class ReadmeRefactor:
    """将原始 README 重构为 5 段式标准文档（What/Why/How/Result/Next）。"""

    # 技术语言 → 价值语言 转换规则
    TRANSFORM_RULES = {
        "AI Workflow Engine": "帮助开发者自动转换需求为可交付资产",
        "支持多模型": "减少重复配置与上下文切换",
        "模型调度": "降低交付成本",
        "自动测试": "质量保障自动化",
        "CI/CD": "交付流水线",
        "代码生成": "开发效率提升",
    }

    # What — 价值提取模式
    WHAT_PATTERNS = [
        r"(?:简介|概述|介绍|关于)[：:]\s*(.+?)(?:\n\n|##|$)",
        r"一个(.*?)的(?:智能|高效|专业|强大|简单|轻量|开源)?(?:工具|系统|平台|引擎|框架|方案|库|服务)",
    ]

    # Why — 痛点提取模式
    WHY_PATTERNS = [
        r"(?:痛点|问题|挑战|困境|难题|背景)[：:\s]*(.+?)(?:\n\n|##|$)",
        r"(?:存在|面临|遇到|缺少|缺乏)(.*?)(?:问题|困难|不足|瓶颈|限制)",
        r"(?:目前|当前|现有|传统)(.*?)(?:效率低|成本高|体验差|复杂|繁琐|不足)",
    ]

    # How — 架构与特性提取模式
    HOW_PATTERNS = [
        r"(?:架构|设计|结构|实现)[：:\s]*(.+?)(?:\n\n|##|$)",
        r"(?:特性|功能|Features?|能力)[：:\s]*(.+?)(?:\n\n|##|$)",
        r"(?:采用|基于|使用|通过)(.*?)(?:实现|构建|开发|提供|支持)",
    ]

    # Result — 指标与场景提取模式
    RESULT_PATTERNS = [
        r"(?:指标|收益|效果|成果|性能|Metrics)[：:\s]*(.+?)(?:\n\n|##|$)",
        r"(?:场景|用例|应用场景|典型场景|使用场景)[：:\s]*(.+?)(?:\n\n|##|$)",
        r"(?:提升|提高|降低|减少|改善|优化)(.*?)(?:率|度|效果|目标|成本|时间)",
    ]

    # Next — 路线图提取模式
    NEXT_PATTERNS = [
        r"(?:路线图|Roadmap|计划|规划|TODO|未来)[：:\s]*(.+?)(?:\n\n|##|$)",
        r"(?:即将|下一步|未来|后续)(.*?)(?:实现|支持|添加|发布|推出)",
        r"(?:Phase|阶段|里程碑)[：:\s]*(.+?)(?:\n\n|##|$)",
    ]

    def refactor(self, raw_readme: str, goal_info: Optional[Dict] = None) -> str:
        """将原始 README 重构为标准 5 段式文档。

        Args:
            raw_readme: 原始 README 文本。
            goal_info: 可选的目标信息字典，可包含 persona/problem/solution/outcome 等键。

        Returns:
            重构后的 Markdown 格式 README 字符串。

        Raises:
            ValueError: 当输入为空或内容不足时抛出。
        """
        text = raw_readme.strip()

        if not text:
            raise ValueError("输入为空，请提供有效的 README 内容。")

        if len(text) < 20:
            note = "（内容不足，仅重构现有信息）"
        else:
            note = ""

        what = self._extract_what(text, goal_info)
        why = self._extract_why(text, goal_info)
        how = self._extract_how(text, goal_info)
        result = self._extract_result(text, goal_info)
        next_steps = self._extract_next(text, goal_info)

        title = self._extract_title(text)

        output = f"""# {title}
{note}

## What — 一句话价值
{what}

## Why — 为什么存在

### 痛点
{why}

### 现有方案不足
{self._generate_existing_solution_shortcomings(text)}

## How — 如何实现

### 架构
{self._generate_ascii_architecture(self._extract_features(text))}

### 快速开始
{self._generate_quick_start(text)}

### 特性
{how}

## Result — 效果

### 指标
{result}

## Next — 路线图
{next_steps}
"""
        return output

    # ────────────────────────── 提取方法 ──────────────────────────

    def _extract_what(self, raw_readme: str, goal_info: Optional[Dict] = None) -> str:
        """提取一句话价值主张（技术 × 用户 × 收益 = 产品描述）。

        Args:
            raw_readme: 原始 README 文本。
            goal_info: 可选目标信息。

        Returns:
            一句话价值描述。
        """
        text = raw_readme.strip()

        # 优先从 goal_info 获取
        if goal_info and goal_info.get("solution"):
            return self._transform_to_value(goal_info["solution"])

        # 从 README 提取
        for pattern in self.WHAT_PATTERNS:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                result = match.group(1).strip()
                result = self._transform_to_value(result)
                return result

        # 兜底：标题后的第一段（非空非标题行）
        lines = []
        skip_header = True
        for line in text.splitlines():
            stripped = line.strip()
            if skip_header:
                if stripped.startswith("#"):
                    continue
                if stripped:
                    skip_header = False
                    lines.append(stripped)
                    continue
                continue
            if stripped and not stripped.startswith("#") and not stripped.startswith("-"):
                lines.append(stripped)
            elif stripped and lines:
                break
        if lines:
            return self._transform_to_value(lines[0].strip())

        return "待补充：本项目帮助用户解决什么核心问题？"

    def _extract_why(self, raw_readme: str, goal_info: Optional[Dict] = None) -> str:
        """提取痛点与现有方案不足。

        Args:
            raw_readme: 原始 README 文本。
            goal_info: 可选目标信息。

        Returns:
            痛点描述（Markdown 列表格式）。
        """
        text = raw_readme.strip()

        # 优先从 goal_info 获取
        if goal_info and goal_info.get("problem"):
            return f"- {self._transform_to_value(goal_info['problem'])}"

        # 从 README 提取
        for pattern in self.WHY_PATTERNS:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                content = match.group(1).strip()
                # 转换为列表格式
                if not content.startswith("- "):
                    content = f"- {content}"
                return self._transform_to_value(content)

        # 提取所有 bullet points 作为候选
        bullets = re.findall(r"^[-*]\s+(.+)$", text, re.MULTILINE)
        if bullets:
            pain_points = [b for b in bullets if any(kw in b for kw in ("问题", "痛", "难", "不足", "低", "高", "差"))]
            if pain_points:
                return "\n".join(f"- {self._transform_to_value(p)}" for p in pain_points[:3])

        return "- 未明确：请补充当前用户面临的核心痛点。"

    def _extract_how(self, raw_readme: str, goal_info: Optional[Dict] = None) -> str:
        """提取架构设计与核心特性。

        Args:
            raw_readme: 原始 README 文本。
            goal_info: 可选目标信息。

        Returns:
            特性列表（Markdown 格式）。
        """
        text = raw_readme.strip()

        # 优先提取 Features 标题下的内容
        feature_section = re.search(r"##\s*(?:Features?|特性|功能)\s*\n([\s\S]*?)(?=##|$)", text, re.IGNORECASE)
        if feature_section:
            content = feature_section.group(1).strip()
            if content:
                return self._transform_to_value(content)

        # 从 README 提取特性描述（避免匹配到标题或段落中的零散文本）
        for pattern in self.HOW_PATTERNS:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                content = match.group(1).strip()
                # 过滤过短或无意义匹配
                if len(content) > 8 and not content.endswith("。") and not content.endswith("."):
                    return self._transform_to_value(content)

        # 提取 bullet points（排除 TODO 项）
        bullets = re.findall(r"^[-*]\s+(.+)$", text, re.MULTILINE)
        bullets = [b for b in bullets if not b.startswith("[")]
        if bullets:
            return "\n".join(f"- {self._transform_to_value(b)}" for b in bullets[:6])

        return "- 未明确：请补充核心功能与实现方式。"

    def _extract_result(self, raw_readme: str, goal_info: Optional[Dict] = None) -> str:
        """提取量化指标与典型场景。

        Args:
            raw_readme: 原始 README 文本。
            goal_info: 可选目标信息。

        Returns:
            指标与场景描述（Markdown 格式）。
        """
        text = raw_readme.strip()

        # 优先从 goal_info 获取
        if goal_info and goal_info.get("outcome"):
            return self._transform_to_value(goal_info["outcome"])

        # 提取 Metrics/指标 标题下的内容
        metrics_section = re.search(r"##\s*(?:指标|收益|效果|成果|性能|Metrics|Benchmark)\s*\n([\s\S]*?)(?=##|$)", text, re.IGNORECASE)
        if metrics_section:
            content = metrics_section.group(1).strip()
            if content:
                return self._transform_to_value(content)

        # 提取场景标题下的内容
        scenarios_section = re.search(r"##\s*(?:场景|用例|应用场景|典型场景|使用场景)\s*\n([\s\S]*?)(?=##|$)", text, re.IGNORECASE)
        if scenarios_section:
            content = scenarios_section.group(1).strip()
            if content:
                return self._transform_to_value(content)

        # 从模式提取
        for pattern in self.RESULT_PATTERNS:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                content = match.group(1).strip()
                # 过滤无意义匹配
                if len(content) > 8 and not content.endswith("。") and not content.endswith("."):
                    return self._transform_to_value(content)

        return "- 未明确：请补充可量化的效果指标。"

    def _extract_next(self, raw_readme: str, goal_info: Optional[Dict] = None) -> str:
        """提取路线图与未来计划。

        Args:
            raw_readme: 原始 README 文本。
            goal_info: 可选目标信息。

        Returns:
            路线图（Markdown 任务列表格式）。
        """
        text = raw_readme.strip()

        # 提取 Roadmap 标题下的内容
        roadmap_section = re.search(r"##\s*(?:路线图|Roadmap|计划|规划|TODO)\s*\n([\s\S]*?)(?=##|$)", text, re.IGNORECASE)
        if roadmap_section:
            content = roadmap_section.group(1).strip()
            if content:
                return content

        # 从模式提取
        for pattern in self.NEXT_PATTERNS:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return self._transform_to_value(match.group(1).strip())

        # 提取所有 TODO/checkbox items
        todos = re.findall(r"(- \[[ x]\]\s+.+)$", text, re.MULTILINE)
        if todos:
            return "\n".join(todos[:6])

        # 默认模板
        return "- [ ] 近期（1-3月）：待补充\n- [ ] 中期（3-6月）：待补充\n- [ ] 远期（6-12月）：待补充"

    # ────────────────────────── 辅助方法 ──────────────────────────

    def _transform_to_value(self, text: str) -> str:
        """将技术语言转换为价值语言。

        Args:
            text: 原始技术描述文本。

        Returns:
            转换后的价值描述文本。
        """
        result = text
        for tech_term, value_term in self.TRANSFORM_RULES.items():
            result = result.replace(tech_term, value_term)
        return result

    def _generate_ascii_architecture(self, features: List[str]) -> str:
        """生成简易 ASCII 架构图。

        Args:
            features: 特性/组件列表。

        Returns:
            ASCII 架构图字符串。
        """
        if not features:
            return (
                "┌──────────┐    ┌──────────┐    ┌──────────┐\n"
                "│  Client  │───▶│   Core   │───▶│  Output  │\n"
                "└──────────┘    └──────────┘    └──────────┘"
            )

        # 取前 5 个特性构建架构
        components = features[:5]
        boxes = []
        for comp in components:
            name = re.sub(r"^[-*]\s*", "", comp).strip()
            name = re.sub(r"^#+\s*", "", name).strip()
            name = name[:12]
            boxes.append(name)

        # 构建水平流程图
        top_lines = []
        mid_lines = []
        bot_lines = []
        arrow_lines = []

        for i, box in enumerate(boxes):
            width = max(len(box) + 4, 14)
            top_lines.append("┌" + "─" * width + "┐")
            mid_lines.append("│" + box.center(width) + "│")
            bot_lines.append("└" + "─" * width + "┘")
            if i < len(boxes) - 1:
                arrow_lines.append(" " * width + "───▶")

        result_lines = []
        result_lines.append("    ".join(top_lines))
        result_lines.append("    ".join(mid_lines))
        result_lines.append("    ".join(bot_lines))

        return "\n".join(result_lines)

    def _extract_features(self, text: str) -> List[str]:
        """从文本中提取特性列表。

        Args:
            text: 原始文本。

        Returns:
            特性字符串列表。
        """
        # 尝试提取 Features 章节
        feature_section = re.search(
            r"##\s*(?:Features?|特性|功能|架构)\s*\n([\s\S]*?)(?=##|$)", text, re.IGNORECASE
        )
        if feature_section:
            content = feature_section.group(1)
            bullets = re.findall(r"^[-*]\s+(.+)$", content, re.MULTILINE)
            if bullets:
                return bullets

        # 兜底：收集所有 bullet points
        bullets = re.findall(r"^[-*]\s+(.+)$", text, re.MULTILINE)
        return bullets[:6]

    def _generate_existing_solution_shortcomings(self, text: str) -> str:
        """分析现有方案为何无法解决问题。

        Args:
            text: 原始文本。

        Returns:
            现有方案不足分析（Markdown 列表格式）。
        """
        # 尝试从文本中提取与现有方案相关的关键词
        existing_patterns = [
            r"(?:现有|传统|当前|目前|旧|手动|人工)(.*?)(?:方案|方式|流程|方法|工具|系统)",
            r"(?:缺乏|缺少|没有|无法|难以|不便|繁琐|复杂)(.*?)(?:支持|解决|满足|实现|提供)",
        ]
        for pattern in existing_patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                content = match.group(0).strip()
                if len(content) > 4:
                    return self._transform_to_value(
                        f"- 现有方案{content}，无法从根本上解决问题，需要更系统化的方案。"
                    )

        # 提取 Install/Installation 相关内容判断是否有安装方式
        install_section = re.search(
            r"##\s*(?:Install|Installation|安装|QuickStart|快速开始|Getting\s*Started)\s*\n([\s\S]*?)(?=##|$)",
            text, re.IGNORECASE,
        )

        # 检查是否有代码块或命令示例
        has_code_block = bool(re.search(r"```(?:bash|sh|shell|cmd)?\s*\n", text))
        has_pip = "pip" in text.lower() or "npm" in text.lower() or "yarn" in text.lower()

        if has_code_block or has_pip or install_section:
            return (
                "- 现有工具多为独立解决方案，缺乏统一的集成框架，"
                "导致配置繁琐、学习成本高且难以维护。"
            )

        return (
            "- 当前缺乏标准化、系统化的解决方案，"
            "现有方法往往只能解决局部问题，无法形成完整的价值闭环。"
        )

    def _generate_quick_start(self, text: str) -> str:
        """生成快速开始的 bash 命令示例。

        Args:
            text: 原始文本。

        Returns:
            快速开始命令（Markdown 代码块格式）。
        """
        # 尝试从原始文本中提取已有的安装/快速开始部分
        install_section = re.search(
            r"##\s*(?:Install|Installation|安装|QuickStart|快速开始|Getting\s*Started)\s*\n([\s\S]*?)(?=##|$)",
            text, re.IGNORECASE,
        )
        if install_section:
            content = install_section.group(1).strip()
            # 提取已有的 bash 代码块
            code_blocks = re.findall(r"```(?:bash|sh|shell)?\s*\n([\s\S]*?)```", content)
            if code_blocks:
                commands = "\n".join(b.strip() for b in code_blocks if b.strip())
                if commands:
                    return f"```bash\n{commands}\n```"
            # 如果没有代码块但有内容，尝试提取命令
            commands = re.findall(r"^\$\s*(.+)$", content, re.MULTILINE)
            if commands:
                return f"```bash\n{' && \\\n'.join(c.strip() for c in commands)}\n```"

        # 检测包管理器类型
        if "npm" in text.lower() or "package.json" in text.lower():
            return "```bash\nnpm install <package-name>\nnpm start\n```"
        if "pip" in text.lower() or "setup.py" in text.lower() or "pyproject.toml" in text.lower():
            return "```bash\npip install <package-name>\npython -m <module>\n```"
        if "go mod" in text.lower() or "go.sum" in text.lower():
            return "```bash\ngo get <module-path>\ngo run main.go\n```"
        if "cargo.toml" in text.lower() or "cargo" in text.lower():
            return "```bash\ncargo add <crate-name>\ncargo run\n```"

        # 默认通用模板
        return "```bash\ngit clone <repository-url>\ncd <project-directory>\n# 参考项目文档完成环境配置与依赖安装\n```"

    @staticmethod
    def _extract_title(text: str) -> str:
        """提取项目标题。

        Args:
            text: 原始文本。

        Returns:
            项目标题字符串。
        """
        match = re.search(r"^#\s+(.+)", text, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return "Project"


if __name__ == "__main__":
    import json

    refactor = ReadmeRefactor()

    # ── 示例 1: 基本 README 重构 ──
    sample_readme = """\
# BOS-FS Value Mapper

一个智能化的价值映射引擎，自动将技术特性翻译为业务成果。

## Features

- AI 驱动的特性识别
- 多语言支持
- 实时映射

## Install

```bash
pip install bos-fs-value-mapper
```

## Roadmap

- [x] 核心映射引擎
- [ ] 多模型支持
- [ ] 自定义规则配置
"""

    print("=" * 60)
    print("示例 1: 基本 README 重构")
    print("=" * 60)
    result = refactor.refactor(sample_readme)
    print(result)

    # ── 示例 2: 结合 goal_info ──
    goal_info = {
        "persona": "企业内部研发团队",
        "problem": "现有流程缺乏标准化，沟通成本高，交付质量不稳定",
        "solution": "开发一套自动化项目交付管理系统",
        "outcome": "提升交付效率50%，降低人工成本30%",
    }

    short_readme = "# AI Workflow Engine\n支持多模型，自动测试，CI/CD集成。"

    print("=" * 60)
    print("示例 2: 结合 goal_info 重构（含技术→价值转换）")
    print("=" * 60)
    result2 = refactor.refactor(short_readme, goal_info)
    print(result2)

    # ── 示例 3: 转换规则演示 ──
    print("=" * 60)
    print("示例 3: 技术→价值转换规则")
    print("=" * 60)
    for tech, value in refactor.TRANSFORM_RULES.items():
        print(f"  {tech:20s} → {value}")
    print()

    # ── 示例 4: 错误处理 ──
    print("=" * 60)
    print("示例 4: 错误处理")
    print("=" * 60)
    try:
        refactor.refactor("")
    except ValueError as e:
        print(f"  ✓ 捕获预期错误: {e}")

    try:
        refactor.refactor("ab")
    except ValueError as e:
        print(f"  ✓ 捕获预期错误: {e}")
