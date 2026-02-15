---
name: ui-designer
description: 使用 Material You、极简主义（Minimalism）、玻璃形态学（Glassmorphism）、新野兽主义（Neo-Brutalism）和黏土形态学（Claymorphism）来设计美观的界面。精通 Tailwind CSS、色彩搭配、组件主题设计以及无障碍设计（WCAG）规范。
---

# UI设计师技能

提供专业的设计指导，以创建美观且以用户为中心的界面。该技能侧重于在实现之前和实施过程中的视觉和结构设计。

## 核心能力

### 1. 颜色调色板生成
根据项目风格生成协调统一的颜色调色板。
- 交付成果：十六进制颜色代码、Tailwind配置扩展以及CSS变量。
- 可选调色板风格：高端淡色调、深色调奢华风格或Material You主题的色调调色板。

### 2. 组件主题化
通过一致的设计元素（如背景色、文字色、强调色和边框色）来建立强大的主题系统。
- 定义`--bg`、`--text`、`--accent`和`--border`等变量。
- 确保所有UI元素在悬停、聚焦和激活状态下的外观保持一致。

### 3. 可访问性审计
评估并优化界面，以实现最大程度的包容性和合规性。
- 关注点：WCAG AA/AAA对比度比、语义化的HTML以及直观的导航体验。
- 提供指导：使用ARIA属性、焦点环管理以及提升屏幕阅读器的可用性。

## 核心设计语言

### 1. Material You (M3)
- **主要特点：** 大圆角、色调丰富的颜色调色板、富有表现力的字体设计。
- **参考文档：** [material-you.md](references/material-you.md)

### 2. 极简主义
- **主要特点：** 丰富的内边距、以字体为核心的层次结构、中性色调的调色板。
- **参考文档：** [minimalism.md](references/minimalism.md)

### 3. Glassmorphism
- **主要特点：** 背景模糊效果、细边框、鲜艳的背景渐变。
- **参考文档：** [glassmorphism.md](references/glassmorphism.md)

### 4. Neo-Brutalism
- **主要特点：** 厚实的黑色边框、强烈的阴影效果、对比鲜明的鲜艳色彩、粗体的字体设计。
- **参考文档：** [neo-brutalism.md](references/neo-brutalism.md)

### 5. Claymorphism
- **主要特点：** 温和的3D形状、双重内阴影效果、较大的边框半径、有趣的淡色调。
- **参考文档：** [claymorphism.md](references/claymorphism.md)

### 6. M3 Pastel Glass（混合风格）
- **主要特点：** 淡蓝色/深蓝色搭配、28像素的圆角、渐变的悬停效果。
- **参考文档：** [m3-pastel-glass.md](references/m3-pastel-glass.md)

### 7. Neo-M3 Hybrid（Wired/Verge风格）
- **主要特点：** 受Wired/Verge风格启发的高对比度设计、3像素的实线黑色边框、强烈的阴影效果（6像素以上）、24像素的圆角、色调丰富的淡色调强调元素。
- **参考文档：** [neo-m3-hybrid.md](references/neo-m3-hybrid.md)

## 自动化：光标样式集成

该技能可以自动更新项目的`.cursorrules`文件，以确保光标样式与设计目标保持一致。

### `apply_ui_rules.py`
运行此脚本，将设计规则添加到当前目录下的`.cursorrules`文件中。

```bash
python ~/.gemini/skills/ui-designer/scripts/apply_ui_rules.py --style [material|minimal|glass|neo-brutalism|claymorphism|m3-pastel|neo-m3] --palette [pastel|dark|vibrant]
```

## 工作流程

### 1. 设计构思
在开始新功能时，需要明确以下内容：
- 选择的主要设计语言（Material You、Minimalism、Glassmorphism、Neo-Brutalism、Claymorphism、M3 Pastel Glass、Neo-M3 Hybrid）
- 颜色风格（淡色调、深色调、高对比度）

### 2. 组件架构
使用Tailwind类规划HTML/React的结构，重点关注网格布局（Grid）和弹性布局（Flex布局），同时确保界面的响应式设计。

## 最佳实践
- **一致性：** 每个项目应使用统一的设计语言。
- **可访问性：** 确保文本具有足够的对比度。
- **Azzar的法则：** “只需足够的工程量就能把事情做好。”（Wong edan mah ajaib）