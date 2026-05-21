# Reject Analyzer Skill

## Purpose
分析项目被拒绝的原因，提取真实问题，给出修复建议。

## Activation
当项目被拒、需要分析原因并重投时激活。

## Input
拒绝原因文本（评审反馈、审核意见等）。

## Reject Pattern Database

### Pattern 1: 表达太底层
**典型拒绝**: "技术实现描述过于底层，看不出用户价值"
**真实问题**: 用技术语言替代了价值描述，评审无法理解项目解决了什么实际问题
**修复方向**: Feature → Capability → Outcome 转换
**示例**:
- 旧: "基于 LangChain 的多 Agent 框架"
- 新: "帮助开发者将复杂 AI 任务简化为可配置工作流的平台"

### Pattern 2: 目标不明确
**典型拒绝**: "不清楚这个项目具体解决什么问题"
**真实问题**: 缺少场景描述和定位，评审不知道什么时候会用这个项目
**修复方向**: 增加 persona/problem/solution 三要素描述，补充 2-3 个典型使用场景

### Pattern 3: 差异化不足
**典型拒绝**: "又一个 Agent 套壳 / 又一个工作流工具"
**真实问题**: 未突出独特价值主张，与现有方案区别不明显
**修复方向**: 明确与竞品的具体差异点（功能/性能/体验/成本），增加竞品对比表

### Pattern 4: 文档不完整
**典型拒绝**: "缺少安装说明/演示/架构图"
**真实问题**: 交付物不全，评审无法快速了解和使用项目
**修复方向**: 补齐 README（What/Why/How/Result/Next）、Demo Guide、架构图

### Pattern 5: 安全风险
**典型拒绝**: "未说明数据安全/隐私保护"
**真实问题**: 缺少安全设计文档和风险评估
**修复方向**: 补充安全评估报告（数据流、权限控制、加密方案、合规声明）

### Pattern 6: 价值模糊
**典型拒绝**: "看不出相比现有方案的优势"
**真实问题**: 未做竞品对比和价值量化
**修复方向**: 增加竞品对比表（功能/性能/易用性/成本维度），补充可量化指标

### Pattern 7: 场景缺失
**典型拒绝**: "不知道什么时候会用到这个"
**真实问题**: 缺少典型使用场景和用户故事
**修复方向**: 补充 2-3 个真实场景（用户角色 → 痛点 → 解决方案 → 效果）

### Pattern 8: 路线图不合理
**典型拒绝**: "未来规划不清晰"
**真实问题**: 缺少可执行的项目路线图
**修复方向**: 补充近期（1-3 月）/中期（3-6 月）/远期（6-12 月）规划，每个阶段含可交付项

### Pattern 9: 技术可行性存疑
**典型拒绝**: "方案与问题不匹配" / "技术路线不合理"
**真实问题**: 解决方案复杂度过高或技术选型不当
**修复方向**: 重新审视解决方案的合理性，简化架构，提供技术验证（PoC）

### Pattern 10: 合规问题
**典型拒绝**: "许可证/数据使用合规性不明确"
**真实问题**: 缺少合规声明
**修复方向**: 补充许可证声明、数据使用说明、第三方依赖合规检查

## Analysis Logic
1. 匹配拒绝模式（精确匹配优先，模糊匹配兜底）
2. 提取真实问题（区分表层原因 vs 根本原因）
3. 生成修复项（具体、可操作、可验证）
4. 附加通用检查（始终执行，见下方 Checklist）

## General Checklist（始终附加）
无论匹配到什么模式，都检查以下项目：
- [ ] README 是否清晰（What/Why/How/Result/Next）
- [ ] 是否包含典型使用场景（2-3 个）
- [ ] 是否有可量化指标（效率/成本/质量提升）
- [ ] 是否有风险说明（技术/市场/合规）
- [ ] 是否有竞品对比（差异化价值）
- [ ] 文档是否完整（安装/配置/运行/验证）
- [ ] 许可证和合规声明是否齐全

## Output Format
```json
{
  "real_issue": "真实问题描述",
  "fixable_items": ["可修改项1", "可修改项2"],
  "resubmit_suggestion": "重新提交版本的具体建议",
  "matched_pattern": "匹配到的拒绝模式名称",
  "confidence": 0.0-1.0,
  "checklist_results": {
    "readme_clear": true/false,
    "has_scenarios": true/false,
    "has_metrics": true/false,
    "has_risk_disclosure": true/false,
    "has_competitor_comparison": true/false,
    "docs_complete": true/false,
    "compliance_clear": true/false
  }
}
```

## Examples

### Example 1: 表达太底层
**Input**: "解决项目交付问题"
**Output**:
```json
{
  "real_issue": "表达太底层，用户价值弱",
  "fixable_items": ["将技术描述转换为用户价值", "增加场景描述", "补充量化指标"],
  "resubmit_suggestion": "从'交付工具'重新定位为'交付平台'，强调自动化和效率提升",
  "matched_pattern": "表达太底层",
  "confidence": 0.85
}
```

### Example 2: 差异化不足
**Input**: "又一个 AI Agent 工具"
**Output**:
```json
{
  "real_issue": "未突出独特价值主张",
  "fixable_items": ["明确与竞品的具体差异", "突出核心定位", "补充竞品对比表"],
  "resubmit_suggestion": "强调'让成果被接受'而非'成果生成'，定位为 Acceptance Engineering",
  "matched_pattern": "差异化不足",
  "confidence": 0.9
}
```

## Rules
- 分析拒绝原因背后的真实问题（不只停留在表层）
- 给出具体可操作的修复项（不可模糊）
- 始终附加通用检查项（README/场景/指标/风险）
- confidence < 0.5 时标注"低置信度，建议人工复核"
- 多个模式匹配时，按置信度排序输出最高的一项
