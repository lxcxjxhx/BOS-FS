#!/usr/bin/env python3
"""BOS-FS 案例与文档完整性验证脚本。

检查内容：
  1. examples/real-cases/ 下 3 个案例文件是否存在
  2. 每个案例文件包含必需章节
  3. knowledge/adoption/delivery_scenarios.md 存在且包含 5 个场景
  4. knowledge/adoption/roi_framework.md 存在且包含必需章节
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CASE_DIR = PROJECT_ROOT / "examples" / "real-cases"
DELIVERY_SCENARIOS = PROJECT_ROOT / "knowledge" / "adoption" / "delivery_scenarios.md"
ROI_FRAMEWORK = PROJECT_ROOT / "knowledge" / "adoption" / "roi_framework.md"

REQUIRED_CASE_SECTIONS = [
    "场景描述",
    "输入数据",
    "处理流程",
    "输出交付物",
    "提效数据",
    "质量对比",
    "使用技能",
]

REQUIRED_ROI_SECTIONS = [
    "人工基线测量方法",
    "ROI 计算公式",
    "输出质量评估指标",
    "人员要求降低程度",
    "实际案例数据",
]


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def _pass(msg: str):
    print(f"  {Colors.GREEN}[PASS]{Colors.RESET}  {msg}")


def _fail(msg: str):
    print(f"  {Colors.RED}[FAIL]{Colors.RESET}  {msg}")


def _warn(msg: str):
    print(f"  {Colors.YELLOW}[WARN]{Colors.RESET}  {msg}")


def _header(msg: str):
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}  {msg}{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")


def check_case_files_exist() -> bool:
    _header("检查 1: 案例文件存在性")
    expected = ["case-01-penetration-test.md", "case-02-code-audit.md", "case-03-vulnerability-ledger.md"]
    all_ok = True
    if not CASE_DIR.is_dir():
        _fail(f"目录不存在: {CASE_DIR}")
        return False
    for fname in expected:
        fpath = CASE_DIR / fname
        if fpath.is_file():
            size = fpath.stat().st_size
            _pass(f"{fname} 存在 ({size} bytes)")
        else:
            _fail(f"{fname} 不存在")
            all_ok = False
    return all_ok


def check_case_sections() -> bool:
    _header("检查 2: 案例文件必需章节")
    all_ok = True
    for fpath in sorted(CASE_DIR.glob("case-*.md")):
        content = fpath.read_text(encoding="utf-8")
        missing = [s for s in REQUIRED_CASE_SECTIONS if s not in content]
        if missing:
            _fail(f"{fpath.name} 缺少章节: {', '.join(missing)}")
            all_ok = False
        else:
            found = [s for s in REQUIRED_CASE_SECTIONS if s in content]
            _pass(f"{fpath.name} 包含全部 {len(found)} 个必需章节")
    return all_ok


def check_delivery_scenarios() -> bool:
    _header("检查 3: delivery_scenarios.md")
    if not DELIVERY_SCENARIOS.is_file():
        _fail(f"文件不存在: {DELIVERY_SCENARIOS}")
        return False
    content = DELIVERY_SCENARIOS.read_text(encoding="utf-8")
    _pass(f"文件存在 ({DELIVERY_SCENARIOS.stat().st_size} bytes)")
    scenario_count = content.count("## 场景 ")
    if scenario_count >= 5:
        _pass(f"包含 {scenario_count} 个场景 (要求 >= 5)")
    else:
        _fail(f"仅包含 {scenario_count} 个场景 (要求 >= 5)")
        return False
    return True


def check_roi_framework() -> bool:
    _header("检查 4: roi_framework.md")
    if not ROI_FRAMEWORK.is_file():
        _fail(f"文件不存在: {ROI_FRAMEWORK}")
        return False
    content = ROI_FRAMEWORK.read_text(encoding="utf-8")
    _pass(f"文件存在 ({ROI_FRAMEWORK.stat().st_size} bytes)")
    missing = [s for s in REQUIRED_ROI_SECTIONS if s not in content]
    if missing:
        _fail(f"缺少章节: {', '.join(missing)}")
        return False
    _pass(f"包含全部 {len(REQUIRED_ROI_SECTIONS)} 个必需章节")
    return True


def main():
    print(f"{Colors.BOLD}BOS-FS 案例与文档完整性验证{Colors.RESET}")
    print(f"项目根目录: {PROJECT_ROOT}")

    results = {
        "案例文件存在性": check_case_files_exist(),
        "案例文件章节": check_case_sections(),
        "交付场景文档": check_delivery_scenarios(),
        "ROI 框架文档": check_roi_framework(),
    }

    _header("验证汇总")
    all_passed = True
    for name, ok in results.items():
        status = f"{Colors.GREEN}通过{Colors.RESET}" if ok else f"{Colors.RED}失败{Colors.RESET}"
        print(f"  {name}: {status}")
        if not ok:
            all_passed = False

    print()
    if all_passed:
        print(f"{Colors.BOLD}{Colors.GREEN}全部检查通过!{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.BOLD}{Colors.RED}部分检查未通过，请查看上方详情。{Colors.RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
