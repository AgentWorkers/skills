---
name: happy-hues
description: 从 Happy Hues 获取精选的色彩调色板，用于设计项目。当用户请求色彩方案、调色板推荐、设计用色，或提到“配色”、“色彩调色板”、“Happy Hues”等词汇时，可以使用这些调色板。该工具支持按情绪（暖色调、深色调、鲜明色调、极简风格等）进行筛选，并提供适用于不同角色的颜色（背景色、标题色、按钮色、高亮色等）。
---

# Happy Hues — 精选配色方案

来自 [happyhues.co](https://www.happyhues.co) 的 17 个精选配色方案，每个方案都包含适用于实际设计的颜色组合。

## 数据

请加载 `references/palettes.json` 文件，其中包含 17 个配色方案的详细信息，每个方案的字段如下：

| 字段 | 描述 |
|-------|-------------|
| `id` | 配色方案编号（1-17） |
| `name` | 简称（例如：“Dark Mode”（暗黑模式），“Clean Blue”（纯净蓝） |
| `mood` | 用于筛选的色调标签（以逗号分隔） |
| `background` | 页面/部分的背景颜色 |
| `headline` | 标题文本的颜色 |
| `paragraph` | 正文文本的颜色 |
| `button` | 主按钮/呼叫行动（CTA）的背景颜色 |
| `buttonText` | 按钮文本的颜色 |
| `stroke` | 边框/描边的颜色 |
| `main` | 卡片/容器的背景颜色 |
| `highlight` | 强调色/高亮颜色 |
| `secondary` | 次要强调色 |
| `tertiary` | 第三级强调色 |

## 使用方法

1. 阅读 `references/palettes.json` 文件。
2. 根据用户的情绪或氛围选择与配色方案中的 `mood` 标签相匹配的方案。
3. 获取该配色方案中的所有颜色及其在设计中的用途。
4. 点击 `https://www.happyhues.co/palettes/{id}` 进行实时预览。

## 色调快速参考

- **明亮/纯净**：3（Clean Blue）、6（Minimal Purple）、8（Teal Minimal）、14（Sunny Blue）
- **暗黑**：4（Dark Mode）、10（Forest Green）、12（Deep Purple）、13（Fire Dark）、16（Dark Peach）
- **温暖/舒适**：1（Default）、5（Earthy Green）、9（Orange Pop）、15（Warm Rose）、17（Vintage Pink）
- **鲜明/活力**：2（Bold Pop）、9（Orange Pop）、13（Fire Dark）
- **柔和/女性化**：7（Soft Pink）、15（Warm Rose）、12（Deep Purple）
- **专业**：3（Clean Blue）、8（Teal Minimal）、11（Luxury Dark）