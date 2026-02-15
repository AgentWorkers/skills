---
name: Colors
description: 构建具有适当对比度和语义标记的可访问色彩调色板。
metadata: {"clawdbot":{"emoji":"🎨","requires":{},"os":["linux","darwin","win32"]}}
---

## 对比度比率（WCAG）

| 等级 | 普通文本 | 大字号文本（≥18pt 或 ≥14pt 粗体） | 用户界面组件 |
|-------|-------------|----------------------------------|---------------|
| AA（最低要求）| ≥ 4.5:1 | ≥ 3:1 | ≥ 3:1 |
| AAA（高级要求）| ≥ 7:1 | ≥ 4.5:1 | — |

在白色背景下的关键阈值：
- `#767676` → 4.54:1 ✅ 刚好通过 |
- `#777777` → 4.47:1 ❌ 未通过（无法向上取整） |
- `#757575` → 4.6:1 ✅ 安全的最低灰色对比度 |

在白色背景下的纯色：
- 红色 `#FF0000` → 4:1 ❌ 未通过（不适合普通文本） |
- 绿色 `#00FF00` → 1.4:1 ❌ 绝对不适合用于文本 |
- 蓝色 `#0000FF` → 8.6:1 ✅ 通过 AAA 等级要求 |

## 仅依赖颜色的信息传递方式

切勿仅依靠颜色来传达信息。8% 的男性存在色觉缺陷。

```html
<!-- ❌ Bad: only color differentiates states -->
<span class="text-green-500">Active</span>
<span class="text-red-500">Inactive</span>

<!-- ✅ Good: icon + text + color -->
<span class="text-green-500">✓ Active</span>
<span class="text-red-500">✗ Inactive</span>
```

使用灰度模式测试设计，以确保信息仍然可区分。

## 语义颜色标记

采用三层架构来管理颜色调色板，以便于维护：

```css
/* Layer 1: Primitives (raw values) */
--blue-500: #3B82F6;
--gray-900: #111827;

/* Layer 2: Semantic (roles) */
--color-primary: var(--blue-500);
--color-text: var(--gray-900);
--color-error: var(--red-500);

/* Layer 3: Component (specific use) */
--btn-primary-bg: var(--color-primary);
--input-border-error: var(--color-error);
```

根据功能而非外观来命名颜色：例如使用 `text-primary` 而不是 `text-blue`。

## 深色模式

通过调整亮度来营造层次感，而非使用阴影效果：

```css
/* Light mode uses shadows for depth */
/* Dark mode uses surface brightness */
--surface-0: hsl(220 15% 8%);   /* page background */
--surface-1: hsl(220 15% 12%);  /* card */
--surface-2: hsl(220 15% 16%);  /* elevated element */
--surface-3: hsl(220 15% 20%);  /* modal */
```

避免使用纯黑色 `#000` 和纯白色 `#FFF` 作为背景色。使用 `#0a0a0a` 和 `#fafafa` 可以减少眼睛疲劳。

## 中性灰色

在灰色中加入主色的微妙色调，以增强整体协调性：

```css
/* Instead of pure gray */
--gray-100: hsl(220 10% 96%);  /* slight blue tint */
--gray-500: hsl(220 10% 46%);
--gray-900: hsl(220 10% 10%);
```

这样可以创建更加精致、有意图的色彩调色板。

## 使用 HSL 色彩模型进行颜色生成

HSL 色彩模型使得生成一致的色彩方案变得非常简单：

```css
--primary-100: hsl(220 90% 95%);
--primary-300: hsl(220 90% 75%);
--primary-500: hsl(220 90% 55%);
--primary-700: hsl(220 90% 35%);
--primary-900: hsl(220 90% 15%);
```

保持相同的色调和饱和度，仅调整明度。

## 颜色分布规则

遵循 60-30-10 的比例：
- 60% 用于主导色（背景、容器） |
- 30% 用于次要色（卡片、章节） |
- 10% 用于强调色（点击按钮、高亮部分） |

将调色板限制在 3-5 种颜色加上中性色。过多的颜色会导致视觉混乱。

## 常见错误：
- 在白色背景下使用 `text-gray-400` 或更浅的灰色通常会导致对比度不足 |
- 将主色或强调色用于正文会导致眼睛疲劳——仅应用于标题和点击按钮 |
- 仅通过改变不透明度来显示悬停状态可能会导致对比度问题——应调整色调或明度 |
- 紫色到蓝色的渐变是常见的设计套路——应选择更有设计感的组合 |
- 仅测试浅色模式——深色模式往往能揭示对比度问题 |
- 仅使用红色和绿色作为区分元素——应配合图标或文字标签使用 |

## 安全的色彩组合

| 行业 | 主色 | 次要色 | 原因 |
|--------|---------|-----------|-----|
| 金融科技 | 海军蓝 #00246B | 浅蓝色 #CADCFC | 传达信任感和清晰度 |
| 医疗保健 | 浅蓝色 #89ABE3 | 白色 | 传递平静和干净的感觉 |
| 电子商务 | 红色 #F96167 | 黄色 #F9E795 | 强调紧迫感和乐观情绪 |

避免使用：红色 + 绿色（可能导致色盲问题）、相邻的色调（如蓝色 + 紫色）、黄色 + 白色（对比度差）。