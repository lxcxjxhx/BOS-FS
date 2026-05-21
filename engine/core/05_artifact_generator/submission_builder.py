"""
Submission Builder Module
Generate submission-ready documentation bundles for BOS-FS projects.
"""

import os
import json
from datetime import datetime
from typing import Optional


class SubmissionBuilder:
    """构建项目提交流程所需的全套文档包。"""

    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = output_dir or os.path.join(
            os.getcwd(), "output", "submission_bundle"
        )

    def build_submission(self, project_info: dict) -> dict:
        """
        根据项目信息生成提交文档包。

        Args:
            project_info: 项目元信息，建议包含 name, version, description, features, target_users 等。

        Returns:
            {"bundle_path": str, "components": list[str], "status": str}
        """
        os.makedirs(self.output_dir, exist_ok=True)

        name = project_info.get("name", "BOS-FS-Project")
        components = []

        for builder in [
            self._build_readme,
            self._build_demo_guide,
            self._build_introduction,
            self._build_screenshots_guide,
            self._build_faq,
            self._build_risk_disclosure,
        ]:
            result = builder(project_info)
            if result:
                components.append(result["filename"])

        meta = {
            "project_name": name,
            "generated_at": datetime.now().isoformat(),
            "components": components,
        }
        meta_path = os.path.join(self.output_dir, "bundle_meta.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        components.append("bundle_meta.json")

        return {
            "bundle_path": self.output_dir,
            "components": components,
            "status": "success",
        }

    # -- internal builders --------------------------------------------------

    def _build_readme(self, info: dict) -> Optional[dict]:
        name = info.get("name", "BOS-FS-Project")
        version = info.get("version", "0.1.0")
        desc = info.get("description", "待补充项目描述。")
        features = info.get("features", [])
        users = info.get("target_users", "待定义")

        features_md = "".join(f"- {f}\n" for f in features) if features else "- 待补充\n"

        content = f"""# {name}

**Version**: {version}

{desc}

## 功能特性

{features_md}
## 目标用户

{users}

## 快速开始

请参考 `demo_guide.md` 了解使用方式。

## 许可证

内部项目，未经授权请勿外传。
"""
        return self._write("README.md", content)

    def _build_demo_guide(self, info: dict) -> Optional[dict]:
        name = info.get("name", "项目")
        content = f"""# {name} — 演示指南

## 环境准备

1. 确保运行环境满足最低要求
2. 安装必要依赖

## 演示步骤

### Step 1: 初始化
启动项目并确认主界面正常加载。

### Step 2: 核心流程
按照业务场景完成端到端操作。

### Step 3: 结果验证
确认输出符合预期。

## 注意事项

- 演示环境数据已隔离，不会影响生产数据
- 如遇问题请查看 FAQ
"""
        return self._write("demo_guide.md", content)

    def _build_introduction(self, info: dict) -> Optional[dict]:
        name = info.get("name", "项目")
        desc = info.get("description", "待补充")
        value = info.get("value_proposition", "提升效率、降低门槛、标准化交付")
        content = f"""# {name} 项目介绍

## 概述

{desc}

## 核心价值

{value}

## 架构亮点

- 模块化设计，支持灵活扩展
- 标准化流程，减少人为错误
- 开箱即用的提交物生成能力

## 适用场景

- 项目交付标准化
- 跨团队协作文档管理
- 自动化提交包生成
"""
        return self._write("introduction.md", content)

    def _build_screenshots_guide(self, info: dict) -> Optional[dict]:
        name = info.get("name", "项目")
        content = f"""# {name} — 截图指南

## 截图规范

| 场景 | 要求 | 格式 |
|------|------|------|
| 主界面 | 完整窗口，含导航 | PNG 1920×1080 |
| 核心流程 | 关键步骤逐帧 | PNG / GIF |
| 异常处理 | 错误提示 + 解决路径 | PNG |

## 建议截图清单

1. 项目首页 / Dashboard
2. 核心功能操作界面
3. 配置 / 设置页面
4. 输出结果展示
5. 异常处理示例

## 存放路径

将截图存放于 `{name}/assets/screenshots/` 目录。
"""
        return self._write("screenshots_guide.md", content)

    def _build_faq(self, info: dict) -> Optional[dict]:
        name = info.get("name", "项目")
        content = f"""# {name} — 常见问题

## Q: 项目运行环境要求？

**A**: 请参考 README 中的环境准备部分。

## Q: 如何自定义提交文档模板？

**A**: 修改对应 builder 的配置参数或继承 SubmissionBuilder 覆盖私有方法。

## Q: 提交后审核不通过怎么办？

**A**: 参考 reject_analyzer 模块分析拒绝原因，针对性修改后重新提交。

## Q: 是否支持批量生成？

**A**: 支持。可传入多个 project_info 字典循环调用 build_submission。
"""
        return self._write("FAQ.md", content)

    def _build_risk_disclosure(self, info: dict) -> Optional[dict]:
        name = info.get("name", "项目")
        content = f"""# {name} — 风险披露

## 已知限制

1. 当前版本为内部预发布，部分功能仍在迭代中
2. 大规模数据场景下性能需进一步验证

## 数据安全

- 演示数据与生产数据严格隔离
- 不收集任何用户敏感信息

## 兼容性

- 建议运行环境: Python 3.9+
- 未在其他版本上充分测试

## 免责声明

本项目按"现状"提供，作者不对因使用本项目产生的任何直接/间接损失负责。
"""
        return self._write("risk_disclosure.md", content)

    # -- helpers ------------------------------------------------------------

    def _write(self, filename: str, content: str) -> Optional[dict]:
        path = os.path.join(self.output_dir, filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"filename": filename, "path": path}
        except Exception as e:
            print(f"[SubmissionBuilder] Failed to write {filename}: {e}")
            return None


if __name__ == "__main__":
    example_info = {
        "name": "BOS-FS",
        "version": "1.0.0",
        "description": "标准化项目交付与提交文档自动生成平台",
        "features": [
            "一键生成提交文档包",
            "审核拒绝原因自动分析",
            "模块化可扩展架构",
        ],
        "target_users": "项目经理、交付工程师、研发团队",
        "value_proposition": "将手动整理提交文档的时间从小时级压缩到分钟级",
    }

    builder = SubmissionBuilder()
    result = builder.build_submission(example_info)
    print(json.dumps(result, ensure_ascii=False, indent=2))
