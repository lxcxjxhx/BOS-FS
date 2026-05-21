"""Goal Refiner - Extract structured project intent from descriptions."""

import re
from typing import Dict


class GoalRefiner:
    """Extracts persona, problem, solution, outcome from project descriptions."""

    PERSONA_PATTERNS = [
        r'作为(.*?)(?:我|需要|希望|想要|旨在|计划|团队|角色)',
        r'(?:角色|身份|用户群体|目标用户)[：:]\s*(.+?)(?:\n|。|$)',
        r'(?:针对|面向|服务)(.*?)(?:提供|开发|构建|设计|实现)',
    ]

    PROBLEM_PATTERNS = [
        r'(?:痛点|问题|挑战|困境|难题)[：:]\s*(.+?)(?:\n|。|$)',
        r'(?:存在|面临|遇到|缺少|缺乏)(.*?)(?:问题|困难|不足|瓶颈|限制)',
        r'(?:目前|当前|现有|传统|旧)(.*?)(?:效率低|成本高|体验差|性能差|不足|困难)',
    ]

    SOLUTION_PATTERNS = [
        r'(?:方案|解决|计划|目标|策略|方法)[：:]\s*(.+?)(?:\n|。|$)',
        r'(?:开发|构建|创建|实现|设计|提供|搭建)(.*?)(?:系统|平台|工具|模块|服务|产品|方案)',
        r'通过(.*?)(?:实现|解决|提升|优化|降低|提高|完成)',
    ]

    OUTCOME_PATTERNS = [
        r'(?:目标|预期|期望|成果|收益|价值|效果)[：:]\s*(.+?)(?:\n|。|$)',
        r'(?:实现|达到|提升|降低|提高|减少|改善|优化)(.*?)(?:效果|目标|指标|率|度|水平)',
        r'(?:以便|从而|进而|以期|最终|旨在)(.*?)(?:\n|。|$)',
    ]

    def refine(self, project_description: str) -> Dict[str, str]:
        """Extract structured intent from project description.
        
        Args:
            project_description: Raw project description text.
            
        Returns:
            Dict with keys: persona, problem, solution, outcome.
        """
        text = project_description.strip()
        
        return {
            "persona": self._extract(text, self.PERSONA_PATTERNS),
            "problem": self._extract(text, self.PROBLEM_PATTERNS),
            "solution": self._extract(text, self.SOLUTION_PATTERNS),
            "outcome": self._extract(text, self.OUTCOME_PATTERNS),
        }

    def _extract(self, text: str, patterns: list) -> str:
        """Extract first match from pattern list."""
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        # Fallback: return first sentence if patterns fail
        first_sentence = re.split(r'[。.\n]', text)[0].strip()
        return first_sentence if first_sentence else ""


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
