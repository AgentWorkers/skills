---
name: pick-your
description: "生成多主题的食物拼贴画（汉堡、披萨、寿司、沙拉、甜点），使用圆形遮罩效果处理图片。适用于用户请求特定类别的食物拼贴画、需要圆形遮罩效果的布局，或者希望从精选列表中选择食材的情况。"
---
# 选择您的主题

该技能可以根据预定义的主题生成高质量的食物拼贴画。

## 使用方法

使用 `make_wings_collage.py` 脚本来生成拼贴画。

```bash
python3 /root/.openclaw/workspace/skills/pick-your/scripts/make_wings_collage.py
```

## 特点

- **拼贴布局**：生成一个 3x3 的圆形遮罩图像网格。
- **动态标题**：自动生成 “PICK [X] [THEME]” 标题。
- **可定制**：支持汉堡、披萨、寿司、沙拉和甜点等主题。

## 主题选项

- Gourmet_Burgers（高级汉堡）
- Artisan_Pizzas（手工披萨）
- Sushi_Rolls（寿司卷）
- Healthy_Salads（健康沙拉）
- Dessert_Delights（甜点精选）