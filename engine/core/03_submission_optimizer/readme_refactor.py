"""README 重构引擎 — 将任意 README 转为 What/Why/How/Result/Next 标准结构。"""

import re


class ReadmeRefactor:
    """基于 一句话价值 / 架构图 / 安装 / 场景 / 指标 / 路线图 六段式模板重构 README。"""

    TEMPLATE = """\
# {title}

## 一句话价值
{one_liner}

## 架构图
{ascii_arch}

## 安装
{installation}

## 场景
{scenarios}

## 指标
{metrics}

## 路线图
{roadmap}
"""

    def refactor(self, original_readme: str) -> str:
        """读取原始 README，提取关键信息并按模板输出。"""
        info = self._extract(original_readme)
        return self.TEMPLATE.format(**info)

    # ────────────────────────── 内部提取逻辑 ──────────────────────────

    def _extract(self, text: str) -> dict:
        return {
            "title": self._extract_title(text),
            "one_liner": self._extract_one_liner(text),
            "ascii_arch": self._extract_ascii_arch(text),
            "installation": self._extract_installation(text),
            "scenarios": self._extract_scenarios(text),
            "metrics": self._extract_metrics(text),
            "roadmap": self._extract_roadmap(text),
        }

    @staticmethod
    def _extract_title(text: str) -> str:
        m = re.search(r"^#\s+(.+)", text, re.MULTILINE)
        return m.group(1).strip() if m else "Project"

    @staticmethod
    def _extract_one_liner(text: str) -> str:
        """从首段或简介段提取一句话价值。"""
        lines = text.strip().splitlines()
        # 跳过标题行，取第一个非空段落
        skip_title = False
        for line in lines:
            if line.startswith("#"):
                skip_title = True
                continue
            if skip_title and line.strip():
                return line.strip().rstrip(".")
        return "待补充：一句话说明本项目的核心价值。"

    @staticmethod
    def _extract_ascii_arch(text: str) -> str:
        """尝试提取已有 ASCII 架构图；否则生成默认骨架。"""
        # 匹配 code block 中包含 ─ │ └ ├ 等字符的块
        blocks = re.findall(r"```(?:\w*)\n(.*?)```", text, re.DOTALL)
        for block in blocks:
            if any(ch in block for ch in ("──", "│", "├", "└", "→")):
                return block.strip()
        return (
            "┌──────────┐    ┌──────────┐    ┌──────────┐\n"
            "│  Client   │───▶│  Core    │───▶│  Output   │\n"
            "└──────────┘    └──────────┘    └──────────┘\n"
            "                 (待补充细节)"
        )

    @staticmethod
    def _extract_installation(text: str) -> str:
        """提取安装/快速开始部分。"""
        patterns = [
            r"(##\s*安装[\s\S]*?)(?=##|$)",
            r"(##\s*Install[\s\S]*?)(?=##|$)",
            r"(##\s*QuickStart[\s\S]*?)(?=##|$)",
            r"(##\s*快速开始[\s\S]*?)(?=##|$)",
        ]
        for p in patterns:
            m = re.search(p, text, re.IGNORECASE)
            if m:
                # 移除首行的 ## 标题，保留内容
                content = m.group(1).strip()
                lines = content.splitlines()
                if lines and lines[0].strip().startswith("##"):
                    return "\n".join(lines[1:]).strip()
                return content
        return "```bash\npip install <package>\n```"

    @staticmethod
    def _extract_scenarios(text: str) -> str:
        """提取使用场景 / 特性列表。"""
        patterns = [
            r"(##\s*场景[\s\S]*?)(?=##|$)",
            r"(##\s*(?:Features?|特性|使用场景|用例)[\s\S]*?)(?=##|$)",
        ]
        for p in patterns:
            m = re.search(p, text, re.IGNORECASE)
            if m:
                # 移除首行的 ## 标题，保留内容
                content = m.group(1).strip()
                lines = content.splitlines()
                if lines and lines[0].strip().startswith("##"):
                    return "\n".join(lines[1:]).strip()
                return content
        # 兜底：收集所有 bullet points
        bullets = re.findall(r"^[-*]\s+(.+)$", text, re.MULTILINE)
        if bullets:
            return "- " + "\n- ".join(bullets[:6])
        return "待补充：列出 3-5 个典型使用场景。"

    @staticmethod
    def _extract_metrics(text: str) -> str:
        """提取性能指标 / 数据。"""
        patterns = [
            r"(##\s*(?:指标|Metrics|性能|Benchmark)[\s\S]*?)(?=##|$)",
        ]
        for p in patterns:
            m = re.search(p, text, re.IGNORECASE)
            if m:
                # 移除首行的 ## 标题，保留内容
                content = m.group(1).strip()
                lines = content.splitlines()
                if lines and lines[0].strip().startswith("##"):
                    return "\n".join(lines[1:]).strip()
                return content
        return "| 指标 | 目标 | 当前 |\n|------|------|------|\n| 待补充 | - | - |"

    @staticmethod
    def _extract_roadmap(text: str) -> str:
        """提取路线图 / TODO / 计划。"""
        patterns = [
            r"(##\s*(?:路线图|Roadmap|TODO|计划|Planned)[\s\S]*?)(?=##|$)",
        ]
        for p in patterns:
            m = re.search(p, text, re.IGNORECASE)
            if m:
                # 移除首行的 ## 标题，保留内容
                content = m.group(1).strip()
                lines = content.splitlines()
                if lines and lines[0].strip().startswith("##"):
                    return "\n".join(lines[1:]).strip()
                return content
        return "- [ ] 待补充：下一阶段计划"


if __name__ == "__main__":
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

## QuickStart

```python
from bos_fs import ValueMapper
mapper = ValueMapper()
result = mapper.map("AI Workflow")
print(result)
```

## Metrics

- 映射准确率: 95%+
- 响应延迟: <50ms

## Roadmap

- [x] 核心映射引擎
- [ ] 多模型支持
- [ ] 自定义规则配置
"""

    refactored = ReadmeRefactor().refactor(sample_readme)
    print(refactored)
