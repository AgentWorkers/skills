---
name: ui-designer
description: 使用16种以上的设计系统（包括Material You、Fluent Design、Apple HIG、Ant Design、Carbon Design、Shopify Polaris、Minimalism、Glassmorphism、Neo-Brutalism、Neumorphism、Skeuomorphism、Claymorphism、Swiss Design和Atlassian Design）来设计美观的界面。精通Tailwind CSS、色彩搭配、组件主题设计以及无障碍设计（WCAG标准）。
---
# UI设计师技能

提供专业的设计指导，帮助您创建美观且以用户为中心的界面，支持多种设计语言。该技能侧重于在实现之前和实现过程中的视觉与结构设计。

## 核心能力

### 1. 颜色调色板生成
根据项目风格生成协调统一的颜色调色板。
- 交付成果：十六进制颜色代码、Tailwind配置扩展以及CSS变量。
- 可选调色板风格：高端淡色调、深色调奢华风格或Material You主题风格。

### 2. 组件主题化
通过一致的设计元素（如背景色、文字色、强调色和边框色）建立强大的主题系统。
- 定义`--bg`、`--text`、`--accent`和`--border`等变量。
- 确保所有UI元素在悬停、聚焦和激活状态下的样式保持一致。

### 3. 可访问性审计
评估并优化界面，以实现最大程度的包容性和合规性。
- 关注点：WCAG AA/AAA对比度比、语义化HTML以及直观的导航体验。
- 提供指导：使用ARIA属性、焦点提示功能以及优化屏幕阅读器的兼容性。

## 设计系统库（共16个）

| 类别 | 系统 | 关键特性 | 适用场景 | 参考文档 |
|----------|--------|------------|----------|-----------|
| **企业级** | Fluent Design | 亚克力材质效果、5大设计原则 | Windows应用程序、Microsoft 365企业版 | [fluent-design.md](references/fluent-design.md) |
| **企业级** | Ant Design | 自然风格、8像素网格布局、12列布局 | 管理面板、B2B应用程序、数据密集型应用 | [ant-design.md](references/ant-design.md) |
| **企业级** | Carbon Design | 16列网格布局、IBM Plex设计语言 | 企业级软件、数据可视化应用 | [carbon-design.md](references/carbon-design.md) |
| **企业级** | Atlassian Design | 强烈的视觉效果、注重协作性、8像素网格布局 | 项目管理工具、团队协作工具 | [atlassian-design.md](references/atlassian-design.md) |
| **平台级** | Apple HIG | SF Pro字体、鲜艳的色彩搭配、模糊背景效果 | iOS、macOS原生应用程序 | [apple-hig.md](references/apple-hig.md) |
| **平台级** | Shopify Polaris | 以商家为中心的设计风格、清新的蓝色调 | 电子商务平台、商家工具 | [shopify-polaris.md](references/shopify-polaris.md) |
| **现代风格** | Material You | 动态颜色效果、大圆角设计、渐变背景 | Android应用程序、现代网页应用 | [material-you.md](references/material-you.md) |
| **现代风格** | Glassmorphism | 背景模糊效果、鲜艳的渐变色 | 仪表盘、首页设计 | [glassmorphism.md](references/glassmorphism.md) |
| **现代风格** | Neumorphism | 软质3D效果、双重阴影效果、单色设计 | 创意项目、极简主义UI | [neumorphism.md](references/neumorphism.md) |
| **现代风格** | Neo-Brutalism | 厚边框、强烈阴影效果、鲜明色彩 | 创意机构、艺术品牌 | [neo-brutalism.md](references/neo-brutalism.md) |
| **现代风格** | Claymorphism | 软质3D效果、双重内阴影、趣味性设计元素 | 休闲类应用程序、消费品设计 | [claymorphism.md](references/claymorphism.md) |
| **经典风格** | 极简主义 | 以 typography 为核心的设计语言、充足的间距设计 | 内容网站、作品集展示 | [minimalism.md](references/minimalism.md) |
| **经典风格** | Swiss Design | 12列网格布局、无阴影效果、非对称设计元素 | 专业服务网站、字体设计 | [swiss-design.md](references/swiss-design.md) |
| **经典风格** | Skeuomorphism | 真实材质模拟效果、仿生设计 | 奢侈品网站、复古风格设计 | [skeuomorphism.md](references/skeuomorphism.md) |
| **混合风格** | M3 Pastel Glass | Material You风格与Glass设计元素的结合、28像素圆角设计 | 现代SaaS平台、创意工具 | [m3-pastel-glass.md](references/m3-pastel-glass.md) |
| **混合风格** | Neo-M3 Hybrid | Brutalism风格与M3风格的结合、3像素边框、强烈阴影效果 | 科技媒体网站、新闻类网站 | [neo-m3-hybrid.md](references/neo-m3-hybrid.md) |

## 自动化：光标样式集成

该技能可自动更新您项目中的`.cursorrules`文件，确保光标样式与设计目标保持一致。

### `apply_ui_rules.py`
运行此脚本，将设计规则添加到当前目录下的`.cursorrules`文件中。

```bash
python3 $WORKSPACE/skills/ui-designer-skill/scripts/apply_ui_rules.py --style [fluent|ant|carbon|atlassian|apple-hig|polaris|material|minimal|glass|neumorphism|neo-brutalism|claymorphism|skeuomorphism|swiss|m3-pastel|neo-m3] --palette [pastel|dark|vibrant|mono]
```

## 工作流程

### 1. 设计构思
在开始新功能时，需要考虑以下问题：
- 主要使用哪种设计语言？（从16种设计系统中选择：Fluent Design、Ant Design、Carbon Design、Atlassian Design、Apple HIG、Polaris、Material You、Glassmorphism、Neumorphism、Neo-Brutalism、Claymorphism、Minimalism、Swiss Design、Skeuomorphism或混合风格）
- 颜色风格是什么？（淡色调、深色调、高对比度、单色或品牌专属风格）
- 目标平台是什么？（Web、iOS、Android、桌面应用或跨平台应用）

### 2. 组件架构设计
使用Tailwind框架规划HTML/React组件的结构，重点关注网格布局和响应式设计。

## 最佳实践
- **一致性：**每个项目应坚持使用统一的设计语言。
- **可访问性：**确保文本具有足够的对比度。
- **Azzar法则：**“只需足够的工程量就能做好设计。”（Wong edan mah ajaib）