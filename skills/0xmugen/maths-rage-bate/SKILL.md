---
name: math-slop
description: 生成一些具有讽刺意味的“数学公式”，这些公式将著名的常数（φ、π、e、i）通过看似简单但实际上蕴含深刻意义的方程联系起来。输出结果应为 LaTeX 格式。这些公式可以用于数学相关的梗图，或者当有人要求提供“数学内容”时使用。
---

# 数学公式生成器

该工具能够生成单行公式，这些公式通过巧妙组合著名的数学常量，呈现出看似深奥实则简单的结果。

## 快速生成

```bash
node scripts/generate-slop.js

# Multiple formulas
node scripts/generate-slop.js --count 5
```

## 示例输出：

- `\varphi^{\ln e} = \varphi^{i^4}` → φ¹ = φ¹
- `e^{i\pi} + 1 + \gamma = 0 + \gamma` → 两边都等于 0（即欧拉公式）
- `\tau - 2\pi = e^{i\pi} + 1` → 0 = 0
- `\sqrt{2}^{\,2} = 2^{\sin^2 x + \cos^2 x}` → 2 = 2¹

## 输出格式

该脚本生成的公式为 LaTeX 格式。若需将公式转换为图像，可以使用以下工具进行渲染：
- 在线工具：latex.codecogs.com, quicklatex.com
- 本地工具：pdflatex, mathjax, katex

## 公式类型：

- **添加零**：`(φ-φ)`、`ln(1)`、`e^{iπ}+1`、`sin(0)`
- **乘以 1**：`e^0`、`i⁴`、`sin²θ+cos²θ`
- **对两边进行相同的操作**：在等式的两边同时加上或乘以相同的常数
- **欧拉公式的变体**：`e^{iπ}+1=0` 的各种变形
- **黄金分割**：`φ² = φ+1` 的各种变形