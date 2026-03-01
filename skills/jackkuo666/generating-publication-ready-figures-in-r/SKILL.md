---
name: generating-publication-ready-figures-in-r
description: 将标准的 ggplot2 图形转换为符合《自然》（Nature）、《科学》（Science）等顶级期刊要求的可视化效果，确保其主题、颜色、字体和导出设置均符合这些期刊的规范。
---
# 在 R 中生成适合发表的图表

本技能专注于将普通的 ggplot2 图表转换为符合《自然》（Nature）、《科学》（Science）、《细胞》（Cell）等顶级期刊严格要求的专业图表。

当用户需要以下操作时，可以使用此技能：
- 将 ggplot 图表转换为符合期刊风格的图表
- 为现有图表应用《自然》或《科学》期刊的样式
- 创建具有统一样式的多面板图表
- 以正确的 DPI、尺寸和格式导出图表
- 使图表符合特定期刊的提交规范
- 创建适合色盲人群的、高质量的配色方案

---

## 该技能的功能

激活此技能后，它将执行以下操作：
1. **分析现有的 ggplot 代码**：读取并理解当前图表的结构。
2. **应用期刊样式**：添加符合期刊要求的元素，包括：
   - 适当的字体大小和字体系列
   - 清晰的轴线和背景
   - 特定期刊的配色方案
   - 图例的位置和样式。
3. **优化图表以适应提交要求**：确保图表满足以下条件：
   - DPI 要求（通常为 300-600 DPI）
   - 宽度/高度规格（单栏/双栏）
   - 文件格式要求（TIFF、PDF、EPS）
   - 色彩空间要求（CMYK 或 RGB）。
4. **创建多面板图表**：使用以下方法组合图表：
   - `patchwork` 用于简单的布局
   - `cowplot` 用于复杂的构图
   - 自定义注释和标签。
5. **正确导出图表**：以正确的格式保存图表，包括：
   - 分辨率（DPI）
   - 尺寸（英寸/厘米）
   - 文件格式
   - 色彩配置文件。

---

## 可能触发此技能的用户请求示例：
- “将这个 ggplot 图表转换为《自然》期刊的风格”
- “让这个图表适合在《科学》期刊上发表”
- “创建一个符合《细胞》期刊格式的双栏图表”
- “以 600 DPI 的分辨率导出这些图表以供提交”
- “为我的图表应用适合色盲人群的配色方案”
- “将这四个图表合并成一个适合发表的图表”
- “为我的散点图调整格式以适应《美国国家科学院院刊》（PNAS）的提交要求”

---

## 期刊风格指南

### 《自然》期刊风格
- 字体：Arial 或 Helvetica
- 字体大小：轴标题 7-9 磅，轴标签 6-8 磅
- 单栏宽度：89 毫米（3.5 英寸）
- 双栏宽度：183 毫米（7.2 英寸）
- 最大高度：234 毫米（9.2 英寸）
- 分辨率：300-600 DPI
- 格式：TIFF、PDF、EPS（优先使用矢量格式）

### 《科学》期刊风格
- 字体：Arial
- 字体大小：标题 9 磅，标签 7 磅
- 单栏宽度：57 毫米（2.25 英寸）
- 双栏宽度：114 毫米（4.5 英寸）
- 分辨率：300-600 DPI
- 格式：TIFF、PDF、EPS

### 《细胞》期刊风格
- 字体：Arial 或 Helvetica
- 单栏宽度：85 毫米（3.3 英寸）
- 双栏宽度：178 毫米（7 英寸）
- 分辨率：至少 300 DPI
- 格式：TIFF、EPS、PDF

---

## 可用的主题模板

### `theme_nature()`
- 清晰、简约的主题，符合《自然》期刊的风格：
  - 无灰色背景
  - 最少的网格线
  - 使用 Arial 字体系列
  - 适当的轴尺寸设置

### `theme_science()`
- 适用于《科学》期刊提交的主题：
  - 紧凑的布局
  - 清晰的排版
  - 适合较窄页面宽度的设计

### `theme_cellpress()`
- 《细胞》期刊的主题：
  - 专业的外观
  - 灵活的图例位置设置
  - 符合发表要求的默认样式

### `theme_colorblind()`
- 适合色盲人群的配色方案：
  - 使用 Viridis/Colorbrewer 配色方案
  - 高对比度
  - 适合打印的颜色

---

## 配色方案

### 《自然》期刊认可的配色方案
```r
# Primary colors
nature_colors <- c(
  blue = "#3B4992",
  red = "#EE0000",
  green = "#008B45",
  purple = "#631879"
)
```

### 适合色盲人群的配色方案
- `scale_fill_viridis()`
- `scale_color_okabe_ito()`（Okabe-Ito 配色方案）
- `scale_color_viridis()`

---

## 示例工作流程

**用户：** 这是我的 ggplot 代码，请将其转换为《自然》期刊的风格。
```r
# Original plot
p <- ggplot(mtcars, aes(x = wt, y = mpg, color = factor(cyl))) +
  geom_point(size = 3)
```

**技能转换后的结果：**
```r
# Publication-ready version
p <- ggplot(mtcars, aes(x = "Weight (tons)", y = "Fuel Efficiency (mpg)",
                        color = "Cylinders")) +
  geom_point(size = 2.5, shape = 16, alpha = 0.8) +
  scale_color_nature() +
  theme_nature(base_size = 8) +
  labs(title = NULL)

# Export at correct size
ggsave("figure1.pdf", p, width = 3.5, height = 3, dpi = 300,
       device = "pdf")
```

---

## 多面板图表

```r
# Combine plots with patchwork
library(patchwork)

figure1 <- (panel_a | panel_b) / (panel_c | panel_d)

# Add panel labels
figure1 <- figure1 +
  plot_annotation(tag_levels = "A",
                  tag_suffix = ")")

# Export
ggsave("figure1.pdf", figure1, width = 7, height = 6, dpi = 300)
```

---

## 常用的工具和包

| 功能 | R 包                          |
|--------|-------------------------------|
| 基础绘图 | ggplot2                          |
| 主题设置 | ggplot2, cowplot, hrbrthemes                |
| 配色方案 | viridis, RColorBrewer, scales, ggsci           |
| 多面板图表 | patchwork, cowplot, ggpubr                   |
| 导出功能 | ggplot2, ragg                        |
| 字体设置 | extrafont, showtext                     |
| 注释功能 | ggrepel, ggpp                       |

---

## 常见期刊的格式要求

| 期刊        | 单栏宽度 | 双栏宽度 | 最大高度 | 最小 DPI       |
|------------|---------|---------|---------|------------|
| 《自然》      | 89 mm    | 183 mm    | 234 mm    | 300         |
| 《科学》      | 57 mm    | 114 mm    | 229 mm    | 300         |
| 《细胞》      | 85 mm    | 178 mm    | 229 mm    | 300         |
| 《美国国家科学院院刊》（PNAS）| 87 mm    | 178 mm    | 227 mm    | 300         |
| 《PLOS ONE》    | 170 mm    |         | 230 mm    | 300         |
| 《eLife》     | 183 mm    |         | 244 mm    | 300         |

---

## 快速参考

### 应用主题
```r
p + theme_nature()           # Nature style
p + theme_science()          # Science style
p + theme_cellpress()        # Cell Press style
p + theme_colorblind()       # Colorblind-safe
```

### 导出格式
```r
# Vector (preferred)
ggsave("figure.pdf", ... device = "pdf")
ggsave("figure.eps", ... device = "eps")

# Raster (high DPI)
ggsave("figure.tiff", ... device = "tiff", dpi = 600)
ggsave("figure.png", ... device = "png", dpi = 300)
```

### 常见问题及解决方法
- **文本太小**：在主题设置中增加 `base_size` 的值。
- **图例重叠**：使用 `theme(legend.position = "bottom")`。
- **颜色不清晰**：使用 `scale_fill_viridis()`。
- **字体无法显示**：使用 `extrafont::font_import()`。

---

## 注意事项
- 提交前请务必查看具体期刊的格式要求。
- 建议使用矢量格式（PDF/EPS）而非光栅格式。
- 确保论文中的所有图表保持一致的样式。
- 使用 `colorblindr` 包测试图表的色盲友好性。
- 保持轴标签清晰简洁。
- 避免多余的图表元素（如背景、网格线）。