---
name: anti-slop-design
description: 创建具有独特风格的前端界面，确保其达到专业级（production-grade）的质量标准，同时避免使用过于通用（generic）的人工智能设计元素（AI aesthetics）。这种设计理念适用于构建网页组件、游戏用户界面（game UIs）、登录页面（landing pages）、仪表板（dashboards）或任何类型的可视化网页界面（visual web interfaces）。通过采用这种设计方法，可以有效避免出现“紫色渐变背景、圆角以及不协调的字体组合”（purple-gradient-rounded-corner-Inter-font syndrome）这类常见设计缺陷。
metadata:
  author: misskim
  version: "1.0"
  origin: Concept inspired by Anthropic frontend-design skill, rewritten for our environment
---

# 防止平庸设计

在所有前端设计中，我们必须坚决避免那种“看起来像是人工智能制作的”、缺乏创意的设计。

## 人工智能设计的典型特征（绝对禁止）

- 仅使用系统默认字体（如 Inter/Roboto/Arial）
- 在白色背景上使用紫色渐变效果
- 所有元素都具有相同的圆角效果
- 布局仅采用居中排列方式
- 使用千篇一律的英雄栏（hero section）和三栏式功能布局
- 所有卡片都使用相同的阴影效果
- 使用缺乏情感表达的插图

## 设计流程

### 1. 理解设计背景
- **目标：** 这个界面旨在解决什么问题？
- **用户群体：** 是谁在使用这个界面？（玩家？开发者？普通用户？）
- **设计风格：** 从以下几种风格中选择一种：
  - 布鲁塔利兹姆（Brutalism）/极简主义（Minimalism）/复古未来主义（Retro-Futurism）/有机自然风格（Organic-Nature）
  - 豪华风格（Luxury）/玩具风格（Toy-like）/编辑风格（Editorial）/艺术装饰风格（Art-Deco）
  - 工业风格（Industrial）/柔和粉彩风格（Soft-Pastel）/80年代霓虹风格（80s Neon）/日本极简风格（Japanese Minimal）
- **独特卖点：** 用户能记住这个设计的哪个独特元素？

### 2. 核心设计原则

**字体设计：**
- 选择独特且美观的字体（建议从 Google Fonts 中寻找）
- 确保展示字体和正文字体之间的搭配协调一致
- 每次设计都使用不同的字体组合（避免重复使用相同的字体）

**色彩设计：**
- 通过 CSS 变量来保持色彩的一致性
- 使用主导色和强烈的色彩点缀（但要注意色彩分布的平衡）
- 每次设计都使用不同的色彩调色板

**动态效果：**
- 尽量使用纯 CSS 动画效果（适用于 HTML 单文件的项目）
- 页面加载时，采用错落有致的元素显示效果（staggered reveal）
- 利用 hover 或 scroll 事件来实现意想不到的交互效果

**空间布局：**
- 使用非对称布局、元素重叠以及 diagonal（对角线方向）的视觉流动
- 在布局中加入打破规则感的元素
- 适当设置合理的间距或故意营造密集感

**背景与细节处理：**
- 禁止使用纯色背景
- 使用渐变纹理、噪声纹理或几何图案
- 通过层次感、阴影和透明度来增强视觉深度

### 针对游戏界面的特殊设计原则

在开发游戏界面时，还需遵循以下原则：
- **沉浸感优先：** 界面设计应融入游戏的世界观
- **充分利用现有资源：** 可以使用 NAS 游戏资源库（如 161GB 的游戏素材库）、Gemini AI 生成的素材，或免费的素材网站
- **动画效果：** 使用 CSS 过渡效果（CSS transitions）并结合 requestAnimationFrame 实现动画
- **声音反馈：** 在用户点击或悬停时添加音效（如果可能的话）
- **响应式设计：** 考虑到 Telegram Mini App 的使用环境，确保界面在 WebView 中也能正常显示

## 设计质量检查清单

- [ ] 是否没有使用 Inter/Roboto/Arial 等系统默认字体？
- [ ] 是否没有使用紫色渐变效果？
- [ ] 所有元素的 border-radius 是否都相同？
- [ ] 布局中是否包含非对称元素？
- [ ] 字体和颜色是否与之前的设计有所不同？
- [ ] 设计是否足够独特，让人不会怀疑它是人工智能制作的？