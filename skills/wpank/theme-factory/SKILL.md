---
name: theme-factory
model: fast
description: 这是一套精心挑选的专业色彩与排版主题集合，适用于设计各种文档（如幻灯片、报告、登录页面等）。您可以在为演示文稿应用视觉主题、生成具有特定风格的文本内容，或创建自定义品牌调色板时使用这些主题。这些主题涵盖了主题设计、色彩搭配、字体选择、幻灯片样式以及品牌色彩等多个方面。
---

# 主题工厂（Theme Factory）

使用精心设计的主题和颜色搭配，为任何文档或界面应用一致、专业的样式。

---

## 使用场景

- 为幻灯片、报告或文档添加统一的视觉风格
- 为 HTML 页面或 landing 页面设置颜色方案和字体组合
- 选择预设主题以快速实现专业化的样式设计
- 当现有预设主题都不适用时，创建自定义主题

---

## 使用方法

### 第一步：展示可用主题

向用户展示 10 个可用主题及其描述：

| 编号 | 主题名称 | 风格 | 适用场景 |
|---|-------|------|----------|
| 1 | **Ocean Depths** | 专业、宁静的海洋风格 | 企业、金融、咨询领域 |
| 2 | **Sunset Boulevard** | 温暖、充满活力的风格 | 创意提案、市场营销、活动 |
| 3 | **Forest Canopy** | 自然、质朴的色调 | 环保、可持续性、健康主题 |
| 4 | **Modern Minimalist** | 简洁、现代的灰度风格 | 科技、建筑、设计展示 |
| 5 | **Golden Hour** | 丰富、温暖的秋日风格 | 酒店、生活方式、手工品牌 |
| 6 | **Arctic Frost** | 凉爽、清晰的风格 | 医疗保健、科技、清洁技术 |
| 7 | **Desert Rose** | 软柔和雅的色调 | 时尚、美容、室内设计 |
| 8 | **Tech Innovation** | 大胆、对比强烈的现代风格 | 初创企业、软件发布、人工智能/机器学习 |
| 9 | **Botanical Garden** | 清新、自然的风格 | 食品、园艺、天然产品 |
| 10 | **Midnight Galaxy** | 剧烈、宇宙般的风格 | 娱乐、游戏、奢侈品牌 |

### 第二步：获取用户选择

询问用户希望应用哪个主题，并在得到明确确认后再继续下一步。

### 第三步：应用主题

1. 从 `themes/` 目录中读取选定的主题文件
2. 在整个文档或界面中一致地应用所选主题的颜色和字体
3. 确保对比度和可读性符合要求
4. 保持所有页面/幻灯片上的视觉风格一致

---

## 主题文件结构

`themes/` 目录下的每个主题文件都遵循以下格式：

```markdown
# Theme Name

Description of the visual mood and inspiration.

## Color Palette
- **Primary Dark**: `#hex` — Usage description
- **Accent**: `#hex` — Usage description
- **Secondary**: `#hex` — Usage description
- **Light/Background**: `#hex` — Usage description

## Typography
- **Headers**: Font family
- **Body Text**: Font family

## Best Used For
Context and audience descriptions.
```

---

## 如何将主题应用于不同类型的文档/界面

### 幻灯片

- **背景**：使用主题中的主要深色作为标题幻灯片的背景，浅色作为内容幻灯片的背景
- **标题**：使用标题字体和主题中的强调色
- **正文**：在浅色背景上使用正文字体和主题中的主要深色
- **强调元素**：使用强调色或次要颜色来标注图表、重点内容等

### HTML / Landing 页面

---（具体应用方式在此处省略，可根据实际需求补充）

### 文档 / 报告

- **封面页**：使用主题中的主要深色背景和浅色文字
- **章节标题**：使用标题字体和强调色
- **正文**：在浅色背景上使用正文字体
- **图表/表格**：使用强调色和次要颜色来标注数据系列
- **提示框**：使用次要颜色作为背景，文字使用主要颜色

---

## 创建自定义主题

当现有预设主题都不适用时，可以按照以下步骤创建自定义主题：

1. **收集信息**：了解品牌、目标受众、主题氛围和适用场景
2. **选择颜色搭配**：选择 4 种能够形成统一风格的颜色：
   - 一种深色（用于背景和文字）
   - 一种主要强调色（用于重点内容、呼叫行动按钮）
   - 一种次要强调色（用于辅助元素）
   - 一种浅色或中性色（用于背景和空白区域）
3. **搭配字体**：选择相互搭配的标题字体和正文字体：
   - 标题字体：具有辨识度、能体现主题特色的字体
   - 正文字体：易于阅读、简洁的字体
4. **检查对比度**：确保文本在背景上的可读性符合 WCAG AA 标准
5. **命名主题**：为主题起一个能够体现其视觉风格的名称
6. **编写主题文件**：按照标准格式编写主题文件
7. **审核**：在应用之前展示主题文件以获得批准

### 颜色搭配规则

- **互补色**：色轮上相对的颜色（对比度较高）
- **类似色**：色轮上相邻的颜色（和谐统一）
- **三原色**：三种等间距的颜色（色彩丰富但平衡）
- **分裂互补色**：基础色加上其互补色（用途广泛）

---

## 对比度指南

应用任何主题时，请确保可读性：

| 颜色组合 | 最小对比度 | WCAG 级别 |
|-------------|--------------|------------|
| 正文在背景上 | 4.5:1 | AA |
| 大字号文本（18px 及以上）在背景上 | 3:1 | AA |
- **用户界面元素/边框** | 3:1 | AA |
- **提高可读性** | 7:1 | AAA |

在最终确定颜色之前，需要在浅色和深色背景下测试强调色。

---

## 可用主题列表

所有主题的详细信息都位于 `themes/` 目录中：

- [themes/ocean-depths.md](themes/ocean-depths.md)
- [themes/sunset-boulevard.md](themes/sunset-boulevard.md)
- [themes/forest-canopy.md](themes/forest-canopy.md)
- [themes/modern-minimalist.md](themes/modern-minimalist.md)
- [themes/golden-hour.md](themes/golden-hour.md)
- [themes/arctic-frost.md](themes/arctic-frost.md)
- [themes/desert-rose.md](themes/desert-rose.md)
- [themes/tech-innovation.md](themes/tech-innovation.md)
- [themes/botanical-garden.md](themes/botanical-garden.md)
- [themes/midnight-galaxy.md](themes/midnight-galaxy.md)

---

## 注意事项

- **未经确认切勿应用主题** — 必须得到用户的明确选择
- **不要混合不同主题的颜色** — 每个主题都是一个独立的、完整的风格单元
- **不要忽略对比度要求** — 可读性比美观更重要
- **不要将强调色用于大段文字** — 强调色仅用于突出重点
- **不要忽略字体搭配** — 标题字体和正文字体必须相互搭配
- **不要硬编码主题样式** — 使用 CSS 变量以便于灵活切换主题

---

## 相关技能

- [design-system-patterns](../design-system-patterns/) — 设计系统模式和主题设计基础
- [distinctive-design-systems](../distinctive-design-systems/) — 独特的设计系统和视觉识别度构建