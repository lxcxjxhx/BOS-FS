"""Goal Refiner - Extract structured project intent from descriptions."""

import json
import os
import re
from typing import Dict, Optional

try:
    from engine.config import ConfigLoader
    HAS_CONFIG_LOADER = True
except ImportError:
    HAS_CONFIG_LOADER = False


class GoalRefiner:
    """Extracts persona, problem, solution, outcome from project descriptions."""

    DEFAULT_CONFIG = {
        "example_templates": [
            "作为企业内部研发团队，我们希望解决当前项目交付效率低下的问题。",
            "痛点：现有流程缺乏标准化，沟通成本高，交付质量不稳定。",
            "方案：开发一套自动化项目交付管理系统，整合需求分析、代码生成、质量审查等环节。",
            "目标：提升交付效率50%，降低人工成本30%，实现标准化可复用的交付流程。",
        ],
        "min_description_length": 10,
        "output_fields": ["persona", "problem", "solution", "outcome"],
        "persona_patterns": [
            r'作为(.*?)(?:我|需要|希望|想要|旨在|计划|角色)',
            r'(?:角色|身份|用户群体|目标用户)[：:]\s*(.+?)(?:\n|。|$)',
            r'(?:针对|面向|服务)(.*?)(?:提供|开发|构建|设计|实现)',
        ],
        "problem_patterns": [
            r'(?:痛点|问题|挑战|困境|难题)[：:]\s*(.+?)(?:\n|。|$)',
            r'(?:存在|面临|遇到|缺少|缺乏)(.*?)(?:问题|困难|不足|瓶颈|限制)',
            r'(?:目前|当前|现有|传统|旧)(.*?)(?:效率低|成本高|体验差|性能差|不足|困难)',
        ],
        "solution_patterns": [
            r'(?:方案|解决|计划|目标|策略|方法)[：:]\s*(.+?)(?:\n|。|$)',
            r'(?:开发|构建|创建|实现|设计|提供|搭建)(.*?)(?:系统|平台|工具|模块|服务|产品|方案)',
            r'通过(.*?)(?:实现|解决|提升|优化|降低|提高|完成)',
        ],
        "outcome_patterns": [
            r'(?:目标|预期|期望|成果|收益|价值|效果)[：:]\s*(.+?)(?:\n|。|$)',
            r'(?:实现|达到|提升|降低|提高|减少|改善|优化)(.*?)(?:效果|目标|指标|率|度|水平)',
            r'(?:以便|从而|进而|以期|最终|旨在)(.*?)(?:\n|。|$)',
        ],
        "default_fallback": "未明确",
        "inference_annotation": "（推断）",
    }

    def __init__(self, config_path: Optional[str] = None):
        config = self._load_config(config_path)
        self.PERSONA_PATTERNS = config.get("persona_patterns", self.DEFAULT_CONFIG["persona_patterns"])
        self.PROBLEM_PATTERNS = config.get("problem_patterns", self.DEFAULT_CONFIG["problem_patterns"])
        self.SOLUTION_PATTERNS = config.get("solution_patterns", self.DEFAULT_CONFIG["solution_patterns"])
        self.OUTCOME_PATTERNS = config.get("outcome_patterns", self.DEFAULT_CONFIG["outcome_patterns"])
        self.MIN_DESCRIPTION_LENGTH = config.get("min_description_length", self.DEFAULT_CONFIG["min_description_length"])
        self.OUTPUT_FIELDS = config.get("output_fields", self.DEFAULT_CONFIG["output_fields"])
        self.DEFAULT_FALLBACK = config.get("default_fallback", self.DEFAULT_CONFIG["default_fallback"])
        self.INFERENCE_ANNOTATION = config.get("inference_annotation", self.DEFAULT_CONFIG["inference_annotation"])

    def _load_config(self, config_path: Optional[str] = None) -> Dict:
        try:
            if config_path and os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        try:
            if HAS_CONFIG_LOADER:
                loader = ConfigLoader()
                cfg = loader.get("goal_refiner")
                if cfg:
                    return cfg
        except Exception:
            pass
        return self.DEFAULT_CONFIG

    def refine(self, project_description: str) -> Dict[str, str]:
        """Extract structured intent from project description.
        
        Args:
            project_description: Raw project description text.
            
        Returns:
            Dict with keys: persona, problem, solution, outcome.
        """
        text = project_description.strip()
        
        if not text:
            return self._empty_result()
        if len(text) < self.MIN_DESCRIPTION_LENGTH:
            return self._empty_result()
        
        raw_persona = self._extract(text, self.PERSONA_PATTERNS)
        raw_problem = self._extract(text, self.PROBLEM_PATTERNS)
        raw_solution = self._extract(text, self.SOLUTION_PATTERNS)
        raw_outcome = self._extract(text, self.OUTCOME_PATTERNS)
        
        persona = self._annotate_inferred(raw_persona, text, "persona")
        problem = self._annotate_inferred(raw_problem, text, "problem")
        solution = self._annotate_inferred(raw_solution, text, "solution")
        outcome = self._annotate_inferred(raw_outcome, text, "outcome")
        
        return {
            "persona": persona,
            "problem": problem,
            "solution": solution,
            "outcome": outcome,
        }

    def _extract(self, text: str, patterns: list) -> str:
        """Extract first match from pattern list."""
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip().strip('，,。.')
        
        first_sentence = re.split(r'[。.\n]', text)[0].strip()
        return first_sentence if first_sentence else ""

    def _empty_result(self) -> Dict[str, str]:
        """Return empty result with default fallback values."""
        fallback = self.DEFAULT_FALLBACK
        return {
            "persona": fallback,
            "problem": fallback,
            "solution": fallback,
            "outcome": fallback,
        }

    def _annotate_inferred(self, value: str, full_text: str, field: str) -> str:
        """Annotate values that were inferred (fallback used) rather than explicitly extracted."""
        if not value:
            return self.DEFAULT_FALLBACK
        first_sentence = re.split(r'[。.\n]', full_text)[0].strip().strip('，,。.')
        if value == first_sentence:
            if len(value) < self.MIN_DESCRIPTION_LENGTH:
                return f"{value}{self.INFERENCE_ANNOTATION}"
        return value


if __name__ == "__main__":
    refiner = GoalRefiner()
    
    sample_desc = """
    作为企业内部研发团队，我们希望解决当前项目交付效率低下的问题。
    痛点：现有流程缺乏标准化，沟通成本高，交付质量不稳定。
    方案：开发一套自动化项目交付管理系统，整合需求分析、代码生成、质量审查等环节。
    目标：提升交付效率50%，降低人工成本30%，实现标准化可复用的交付流程。
    """
    
    result = refiner.refine(sample_desc)
    
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
