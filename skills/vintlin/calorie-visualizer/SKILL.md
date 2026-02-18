---
name: calorie-visualizer
description: 本地卡路里记录与可视化报告功能（每次记录后自动更新，并生成报告图像）
metadata:
  openclaw:
    emoji: "📊"
    os:
      - darwin
      - linux
    requires:
      bins:
        - python3
---
# 卡路里可视化工具

这是一个用于记录饮食信息并进行营养分析的本地工具。

## 核心流程

1. 用户上传饮食相关的文本或图片；上游模块会提取卡路里和蛋白质含量数据，或调用食物数据库进行查询。
2. `add`（或 `add-food`）函数将数据写入 `calorie_data.db` 文件。
3. 数据写入完成后，`visualrenderer.py` 会生成一份新的报告图像。
4. 命令行界面（CLI）会输出 `REPORT_IMAGE:<path>`，以便将图像发送到相应的聊天平台。

## 每日目标设置

1. 用户可以通过 `config.daily_goal` 功能手动设置每日目标。
2. 每日总热量消耗（TDEE）数据来源于 `USER.md` 文件。
3. 如果用户明确拒绝提供个人健康数据，系统将仅记录饮食信息，不再重复提示用户输入数据。
4. 如果用户未设置目标，渲染器将使用默认值：2000 卡路里。

## 命令行界面（CLI）命令

```bash
# Add a meal with explicit nutrition values
python3 scripts/calorie_visualizer.py add "food name" 500 25 [--photo /path/to/image.jpg]

# Add from local food database (local-first, online fallback optional)
python3 scripts/calorie_visualizer.py add-food "Subway chicken sandwich" --multiplier 1.0
python3 scripts/calorie_visualizer.py add-food "rice" --offline

# Daily summary
python3 scripts/calorie_visualizer.py summary

# Regenerate report image
python3 scripts/calorie_visualizer.py report

# Config
python3 scripts/calorie_visualizer.py config daily_goal 2000
python3 scripts/calorie_visualizer.py config user_refused_profile True
```

## 所需依赖库/服务

```bash
cd skills/calorie-visualizer
python3 -m pip install -r requirements.txt
```

- Python 库：`html2image`、`Pillow`
- 可选的外部服务：美国农业部（USDA）API（需要 `USDA_API_KEY`）
- 数据库：SQLite（Python 自带）
- 图像渲染：需要系统安装 Chromium/Chrome 浏览器（由 `html2image` 库使用）

## 数据存储

- 数据存储在本地 SQLite 文件 `calorie_data.db` 中
- 不支持自动与外部系统同步数据