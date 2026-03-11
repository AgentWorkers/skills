---
name: design-pick
description: "生成多种主题的食物拼贴画（如病毒蛋糕、街头美食、冰沙碗、咖啡艺术、融合塔可）。当用户请求特定类型的食物拼贴画、使用圆形遮罩的图片布局，或者希望从精选列表中“挑选”食材时，可以使用该功能。"
---
# 设计精选（Design Pick）

该功能能够根据预定义的主题生成高质量的食物拼贴画。

## 使用方法

请使用 `generate_collage.py` 脚本来生成拼贴画。

```bash
python3 /root/.openclaw/workspace/skills/design-pick/scripts/generate_collage.py
```

## 主要特性

- **拼贴布局**：生成一个 3x3 的网格，其中包含带有圆形遮罩的图片。
- **动态标题**：根据所选主题，自动生成 “PICK 2...” 或 “PICK 3...” 等形式的标题。
- **可定制性**：支持多种主题，如 “病毒式蛋糕”（Viral Cakes）、“街头美食”（Street Food）、“冰沙碗”（Smoothie Bowls）、“咖啡艺术”（Coffee Art）以及 “融合塔可”（Fusion Tacos）等。

## 可用主题

- 病毒式蛋糕（Viral Cakes）
- 街头美食（Street Food）
- 冰沙碗（Smoothie Bowls）
- 咖啡艺术（Coffee Art）
- 融合塔可（Fusion Tacos）