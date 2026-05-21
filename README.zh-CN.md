


# BOS-FS

> **构建 → 定位 → 评审 → 提交**
>
> 将想法、仓库与原型转换为可理解、可评估、可交付的成果。

一次构建，清晰表达，高效交付。

---

## 项目简介

**BOS-FS（Build Outcome Submission – FS）** 是一个面向 AI Agent 的可移植 **Skill Runtime**。

目标不是重新开发 IDE。

而是将：

```text
原始项目
↓
目标提炼
↓
价值表达
↓
评审对齐
↓
交付封装
```

串联成统一流程。

BOS-FS 不伪造成果。

它帮助真实能力变得：

* 更容易理解
* 更容易评估
* 更容易交付
* 更容易被采用

支持：

* Cursor
* Trae
* Claude Code
* OpenHands
* 任意 LLM Runtime

---

## 为什么做 BOS-FS

很多项目失败：

不是能力不够。

而是：

* 不会表达
* README 太弱
* 用户看不懂价值
* 缺少提交材料
* 与评审视角不一致

BOS-FS 聚焦最后一公里：

> 能力 → 结果 → 被接受

---

## 核心能力

| 模块                 | 作用      |
| ------------------ | ------- |
| Goal Refiner       | 提炼项目目标  |
| README Refactor    | 重构项目表达  |
| Reviewer Simulator | 模拟评审    |
| Outcome Mapper     | 将功能转为结果 |
| Submission Builder | 构建提交包   |
| Reject Analyzer    | 将拒绝转为迭代 |

---

## 工作流

```text
项目
 ↓
理解
 ↓
定位
 ↓
重构
 ↓
评审
 ↓
封装
 ↓
提交
```

---

## 示例

### 输入

```text
项目做出来了。

用户看不懂。

README 很乱。

审核失败。
```

### 输出

```text
问题
↓

理解成本高

方案
↓

结构化表达

结果
↓

降低认知门槛

输出
↓

README
提交包
评审建议
```

---

## 快速接入

### Cursor

```text
skill/*.md
→ .cursorrules
```

### Trae

```text
.trae/skills/
```

### OpenHands

```text
mount skills/
```

### 通用 API

```text
system_prompt=skill.md
```

---

## 原则

### 做

✅ 明确目标
✅ 强化表达
✅ 结构化交付
✅ 对齐评审标准

### 不做

❌ 伪造成果
❌ 编造用户
❌ 夸大能力
❌ 绕过规则

---

## 愿景

帮助优秀项目，更容易被正确理解。
