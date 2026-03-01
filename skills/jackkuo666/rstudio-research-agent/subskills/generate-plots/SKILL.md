---
name: generate-publication-plots
description: 使用 ggplot2 及其他 R 可视化库创建符合出版标准的图表，支持多种导出格式，并遵循特定期刊的格式要求。
---
# 生成适合发表的图表

这是一个专门用于在 R 语言中创建专业、符合期刊标准的图表（适合发表）的子技能，遵循科学可视化的最佳实践。

## 概述

该子技能使用 `ggplot2` 及其他 R 可视化库生成高质量图表，支持多种导出格式（PDF、PNG、SVG、TIFF），并遵循常见的期刊格式规范，包括分辨率、色彩空间和字体要求。

当用户需要以下操作时，可以使用此子技能：
- 从数据中创建适合发表的图表
- 以特定期刊格式导出图表
- 生成多面板复合图表
- 应用特定期刊的格式规范
- 在多篇论文中保持一致的图表样式

---

## 该子技能的功能

调用该子技能后，它会执行以下步骤：
1. **分析数据和需求**：
   - 检查数据结构和变量
   - 确定合适的图表类型
   - 识别期刊的格式要求
   - 区分分类变量和连续变量
2. **创建 ggplot2 可视化图表**：
   - 应用主题自定义
   - 使用对色盲友好的颜色调色板
   - 设置合适的图表尺寸
   - 添加适当的注释和标签
3. **导出为适合发表的格式**：
   - PDF（适用于期刊的矢量格式）
   - PNG（300-600 DPI 的光栅格式）
   - SVG（可缩放的矢量图形）
   - TIFF（高质量的光栅格式）
4. **遵循期刊格式规范**：
   - Nature（单列宽度：89mm 或 183mm）
   - Science（特定尺寸）
   - PLOS ONE（300+ DPI 的 TIFF/PNG）
   - IEEE（优先使用矢量格式）

---

## 支持的图表类型

| 图表类型 | 描述 | 使用场景 |
|-----------|-------------|----------|
| **散点图** | 带有回归线的点云 | 相关性分析 |
| **条形图** | 分组条形图、堆叠条形图或误差条 | 组间比较 |
| **箱线图/小提琴图** | 分布可视化 | 统计摘要 |
| **折线图** | 时间序列、趋势 | 纵向数据 |
| **热图** | 用颜色编码的矩阵 | 表达式数据 |
| **火山图** | -log10(p) 与倍数变化 | 差异表达分析 |
| **主成分分析图** | 主成分分析 | 降维 |
| **森林图** | 效应大小 | 元分析 |
| **生存曲线** | Kaplan-Meier 曲线 | 时间至事件数据 |
| **多面板图表** | 综合图表 | 复杂结果 |

---

## 用户示例请求

- “创建一个带有回归线的适合发表的散点图”
- “为我的差异表达结果生成一个火山图”
- “制作一个符合 Nature 期刊格式的带有误差条的条形图”
- “将此图表导出为 600 DPI 的 PNG 和矢量 PDF”
- “创建一个结合 PCA 和热图的多面板图表”

---

## 期刊格式规范

### Nature
- 单列宽度：89mm
- 双列宽度：183mm
- 优先格式：PDF、EPS、SVG（矢量格式）
- 光栅格式最低要求：600 DPI
- 字体：Arial、Helvetica 或 Symbol

### Science
- 宽度：5.5cm（单列）或 11.4cm（双列）
- 高度：最大 22.5cm
- 优先格式：TIFF、EPS
- 分辨率：300-600 DPI
- 字体：Helvetica 或 Arial

### PLOS ONE
- 宽度：每英寸 150-300 像素
- 优先格式：TIFF、PNG、PDF
- 分辨率：最低要求 300 DPI
- 颜色：支持 RGB 或 CMYK

### IEEE
- 单列宽度：3.5 英寸
- 页面宽度：7.5 英寸（双列）
- 优先格式：PDF、EPS
- 字体：Times New Roman、Helvetica、Arial

---

## 颜色调色板

### 对色盲友好的调色板
```r
# Okabe-Ito palette (8 colors)
c("#E69F00", "#56B4E9", "#009E73", "#F0E442",
  "#0072B2", "#D55E00", "#CC79A7", "#999999")

# Viridis (perceptually uniform)
viridis::viridis(8)

# ColorBrewer palettes
RColorBrewer::brewer.pal(8, "Set2")
```

### 发散型调色板
- 红-蓝（用于热图、火山图）
- RdYlBu、RdBu、BrBG

### 顺序型调色板
- 蓝色、绿色、PuBuGn

---

## 模板函数

### 基础发表主题
```r
theme_publication <- function(base_size = 12, base_family = "Arial") {
  theme_bw(base_size = base_size, base_family = base_family) +
  theme(
    legend.position = "top",
    panel.border = element_rect(size = 0.5),
    panel.grid.major = element_line(color = "grey90"),
    panel.grid.minor = element_blank(),
    axis.text = element_text(size = rel(0.8)),
    legend.key = element_rect(color = "grey90"),
    legend.key.size = unit(0.4, "cm"),
    legend.margin = margin(0, 0, 0, 0, "cm")
  )
}
```

### 导出函数
```r
save_publication_figure <- function(plot, filename,
                                    width = 89, height = 89,
                                    dpi = 600, units = "mm") {
  ggsave(filename, plot = plot,
         width = width, height = height,
         dpi = dpi, units = units,
         device = "pdf")
}
```

---

## 参数

| 参数 | 描述 | 默认值 |
|-----------|-------------|---------|
| `plot_type` | 要创建的图表类型 | 必需 |
| `data` | 用于绘图的数据框 | 必需 |
| `x_var` | x 轴的变量 | 必需 |
| `y_var` | y 轴的变量 | 必需 |
| `journal` | 目标期刊格式 | `generic` |
| `output_format` | 导出格式（pdf、png、svg、tiff） | `pdf` |
| `width` | 图表宽度（毫米） | `89` |
| `height` | 图表高度（毫米） | `89` |
| `dpi` | 光栅格式的分辨率 | `600` |
| `color_palette` | 颜色方案 | `Okabe-Ito` |

---

## 示例工作流程

### 简单散点图
```r
# Input data: df with columns x, y, group
# Output: scatter_with_regression.pdf

p <- ggplot(df, aes(x = x, y = y, color = group)) +
  geom_point(size = 3, alpha = 0.7) +
  geom_smooth(method = "lm", se = TRUE) +
  scale_color_okabe_ito() +
  theme_publication() +
  labs(x = "X Variable", y = "Y Variable")

save_publication_figure(p, "scatter_with_regression.pdf",
                       width = 89, height = 89, dpi = 600)
```

### 火山图
```r
# Input data: de_results with log2FC, pvalue
# Output: volcano.pdf

p <- ggplot(de_results, aes(x = log2FC, y = -log10(pvalue))) +
  geom_point(aes(color = significant), alpha = 0.6) +
  scale_color_manual(values = c("grey", "#D55E00", "#0072B2")) +
  theme_publication() +
  geom_vline(xintercept = c(-1, 1), linetype = "dashed") +
  geom_hline(yintercept = -log10(0.05), linetype = "dashed") +
  labs(x = expression(log[2]~Fold~Change),
       y = expression(-log[10]~p~value))

save_publication_figure(p, "volcano.pdf")
```

### 多面板图表
```r
# Combine multiple plots using patchwork
library(patchwork)

combined <- (p1 | p2) / (p3 | p4)

ggsave("multipanel.pdf", combined,
       width = 183, height = 183,
       dpi = 600)
```

---

## 输出规范

### PDF（矢量格式）
- 适用于期刊
- 可缩放且不失真
- 文件扩展名：`.pdf`

### PNG（光栅格式）
- 300-600 DPI
- 适合网页/PPT 使用
- 文件扩展名：`.png`

### SVG（矢量格式）
- 适合网页使用的矢量图形
- 可在 Inkscape/Illustrator 中编辑
- 文件扩展名：`.svg`

### TIFF（光栅格式）
- 适合发表的高质量图像
- 无损压缩
- 文件扩展名：`.tiff`

---

## 字体选项

| 字体 | 用途 | 可用性 |
|------|-------|--------------|
| Arial | 最常用的字体 | 系统字体 |
| Helvetica | 经典字体 | 系统字体 |
| Times New Roman | 传统字体 | 系统字体 |
| CM Roman | LaTeX 风格的字体 | 需通过 Extrafont 包安装 |
| Latin Modern | LaTeX 风格的字体 | 需通过 Extrafont 包安装 |

## 最佳实践

1. **尽可能使用矢量格式** - 出版物优先使用 PDF 格式
2. **检查对色盲的影响** - 使用对色盲友好的颜色调色板
3. **保持纵横比** - 避免图表变形
4. **清晰标注** - 使用易于理解的轴标签和图例
5. **保持简洁** - 删除多余的图表元素和装饰
6. **保持一致性** - 在整篇论文中使用统一的图表风格
7. **以正确的 DPI 导出** - 大多数期刊推荐 600 DPI

---

## 注意事项

- 默认使用对色盲友好的调色板
- 字体可以根据期刊要求进行自定义
- 多面板图表使用 `patchwork` 包进行制作
- 所有图表默认使用适合发表的主题
- 分辨率和尺寸符合常见期刊标准

---

## 相关子技能

- **create-project**：在创建图表之前设置项目
- **run-analysis**：生成用于绘图的分析结果