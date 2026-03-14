---
name: qweather
version: 1.0.0
description: >
  天气查询 — 提供实时天气信息、天气预报、生活指数以及城市搜索功能。数据来源为和风天气（QWeather）。  
  触发词：天气、气温、下雨、预报、天气、天气情况、穿什么衣服、洗车、紫外线指数（UV）、空气质量、今天的天气、明天的天气、北京的天气，或任何以“[城市] 天气”格式输入的查询。
metadata:
  openclaw:
    requires:
      env:
        - QWEATHER_API_KEY
        - QWEATHER_API_HOST
---
# qweather — 天气查询技能

通过 QWeather API 查询实时天气、天气预报以及生活指数。

## 快速入门
1. 确保已设置 `QWEATHER_API_KEY` 和 `QWEATHER_API_HOST`（这两个信息可以在 https://console.qweather.com 获取）。
2. 在该技能目录中运行 `bun scripts/weather.ts --help` 命令。
3. 从 `references/command-map.md` 文件中选择相应的命令。

## 工作流程
1. 如果用户提供了城市名称（例如 “北京” 或 “上海”），首先运行 `lookup` 命令以获取 LocationID。
2. 使用获取到的 LocationID 调用 `now`、`forecast` 或 `indices` 命令。
3. 以自然语言的形式返回查询结果。

## 常见城市映射
当用户提供城市名称时，使用 `lookup` 命令将其转换为 LocationID。常见城市对应关系如下：
- 北京 → 101010100
- 上海 → 101020100
- 广州 → 101280101
- 深圳 → 101280601

对于不熟悉的城市名称，务必使用 `lookup` 命令来获取正确的 LocationID。

## 注意事项
- 该技能基于脚本实现，不依赖于 MCP 服务器。
- 需要 `QWEATHER_API_KEY` 和 `QWEATHER_API_HOST` 环境变量。
- API 主机地址因开发者而异，请在 https://console.qweather.com/setting 获取您的主机地址。
- 实时天气数据每 10-20 分钟更新一次。