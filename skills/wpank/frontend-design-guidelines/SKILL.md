---
name: frontend-design
model: reasoning
version: 1.1.0
description: >
  Create distinctive, production-grade frontend interfaces that avoid generic "AI slop"
  aesthetics. Focuses on creative direction and memorable design choices.
tags: [frontend, design, ui, web, aesthetics, creative]
related: [ui-design, web-design, theme-factory]
---

# 前端设计

通过大胆的创意选择，打造出令人难忘的前端界面，使其在众多普通的人工智能生成的设计中脱颖而出。

> **另请参阅：** `ui-design`（了解基础设计原则，如排版、色彩、间距），`web-design`（学习CSS布局技巧）。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install frontend-design
```

## 本技能的作用

本技能通过以下方式指导您创建视觉上独特的前端界面：
- 在编码之前明确设计方向
- 有意识地选择字体、色彩和布局元素
- 实现令人愉悦的动态效果和微交互
- 避免使用那些常见于人工智能生成界面的、缺乏个性的设计模式

## 适用场景

- 创建新的组件、页面或Web应用程序
- 设计登录页面、营销网站或产品用户界面
- 重新设计界面以提高其记忆点
- 任何需要注重视觉效果的前端开发工作

## 关键词

前端设计（frontend design）、Web用户界面（Web UI）、用户界面设计（UI design）、登录页面（landing page）、创意用户界面（creative UI）、Web美学（Web aesthetics）、排版（typography）、视觉设计（visual design）、动态设计（motion design）、独特界面（distinctive interface）

## 设计思维流程

在开始编写代码之前，先确定设计方向：

### 1. 理解设计背景
- **目标**：该界面要解决什么问题？
- **目标用户**：谁会使用这个界面？他们的需求是什么？
- **限制因素**：所使用的框架、性能要求、可访问性要求

### 2. 选择鲜明的设计方向

选择一个极端的审美风格——平庸的设计很容易被遗忘：
| 设计方向 | 特点 |
|-----------|-----------------|
| **极简主义**（Brutal Minimalism） | 极简、纯粹，不添加任何多余元素 |
| **极繁主义**（Maximalist Chaos） | 密集的元素、多层次的布局，刻意营造视觉冲击 |
| **复古未来主义**（Retro-Futuristic） | 结合复古美学与现代科技 |
| **自然主义**（Organic/Natural） | 温和、流畅的视觉效果，灵感来源于自然 |
| **豪华/精致**（Luxury/Refined） | 使用高品质材料，展现细腻的优雅 |
| **趣味性/玩具风格**（Playful/Toy-like） | 轻松有趣、易于使用 |
| **编辑风格/杂志风格**（Editorial/Magazine） | 以文字为中心的布局，采用网格结构 |
| **原始主义**（Brutalism/Raw） | 展现界面的原始结构，反对过度装饰 |
| **艺术装饰风格**（Art Deco/Geometric） | 明显的几何形状、对称性、丰富的装饰元素 |
| **工业风格/实用主义**（Industrial/Utilitarian） | 以功能性为导向，设计简洁而实用 |

### 3. 确定最能让人记住的设计元素

这个界面中，有什么元素最能让人留下深刻印象？专注于这一点进行设计。

## 设计指导原则

### 排版

**绝不要**使用通用的字体：
- Arial、Helvetica、system-ui
- Inter、Roboto（除非有特殊的设计意图）

**应该**选择具有特色的字体：
- 将一种富有表现力的显示字体与一种简洁的正文字体搭配使用
- 可以尝试的字体示例：Space Grotesk、Clash Display、Cabinet Grotesk、Satoshi、General Sans、Instrument Serif、Fraunces、Newsreader

```css
/* Example pairing */
--font-display: 'Clash Display', sans-serif;
--font-body: 'Satoshi', sans-serif;
```

### 色彩与主题

- **确定一个统一的色彩方案**——不要选择保守、安全的颜色组合
- **使用主导色和强调色**比均匀分布的颜色更有效
- **利用CSS变量**来保持设计的一致性
- **避免**在白色背景上使用紫色渐变（这是人工智能设计中常见的颜色搭配）

```css
:root {
  --color-bg: #0a0a0a;
  --color-surface: #141414;
  --color-text: #fafafa;
  --color-accent: #ff4d00;
  --color-muted: #666666;
}
```

### 布局与空间设计

打破常规的布局规则：
- **不对称**而非完美的对称性
- 有意地让元素相互重叠
- 使用非传统的布局方式（如对角线布局）
- 保持足够的负空间（空白区域），避免过度拥挤
- 使用打破常规的元素来吸引用户的注意力

### 动态效果与交互设计

关注那些能产生强烈视觉冲击的瞬间：
- **页面加载时**：使用`animation-delay`实现渐进式的元素显示效果
- **滚动时**：触发令人意外的动画效果
- **鼠标悬停时**：设计出有特色的交互效果
- 对于HTML元素，优先使用CSS动画；对于React项目，可以使用专门的动画库

```css
/* Staggered entrance */
.card { animation: fadeUp 0.6s ease-out backwards; }
.card:nth-child(1) { animation-delay: 0.1s; }
.card:nth-child(2) { animation-delay: 0.2s; }
.card:nth-child(3) { animation-delay: 0.3s; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### 背景与氛围营造

创造深度和氛围：
- 使用渐变效果和多级渐变
- 添加噪声纹理或颗粒感
- 使用几何图案或微妙的网格结构
- 利用多层次的透明度效果
- 设计鲜明的阴影效果或完全平坦的背景
- 为交互式元素定制鼠标指针

## 实现原则

### 根据设计愿景调整代码复杂度

- **极繁主义设计**：使用复杂的代码和丰富的动画效果
- **极简主义设计**：保持简洁，注重细节，确保布局精确
- 美学价值在于将设计愿景完美地呈现出来，而非简单地增加元素

### 不同设计风格之间的变化

避免使用重复的设计模式：
- 不要一直使用相同的明暗色调
- 每次设计都使用不同的字体系列
- 不断尝试不同的设计方向
- 每个设计都应该具有独特的风格

## 绝对不要做的事情

1. **绝不要**使用通用的字体系列（如Inter、Roboto、Arial、系统字体）
2. **绝不要**在白色背景上使用紫色渐变
3. **绝不要**使用千篇一律的布局
4. **绝不要**跳过设计思考阶段——在开始开发之前先充分理解设计需求
5. **绝不要**选择保守、中庸的设计风格——要坚定地坚持自己的设计方向
6. **绝不要**忘记：独特的设计需要相应的代码实现
7. **绝不要**在不同设计版本中重复使用相同的元素——要有意识地做出变化
8. **绝不要**无目的地增加复杂性——极简主义和极繁主义都需要有明确的设计目的