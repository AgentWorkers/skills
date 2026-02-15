---
name: videogames
slug: videogames
display_name: Video Games
description: 一种用于查询电子游戏信息并比较多个商店价格的技能。
author: ivanheral
version: 1.0.0
license: MIT
---

# 视频游戏技能 🎮

此技能允许 OpenClaw 搜索游戏、查看 Steam 上的游戏详情，并通过 CheapShark 找到最优惠的价格。

## 工具

### `scripts/game_tool.py`

这是一个 Python 脚本，用于与 Steam 和 CheapShark 进行交互。

**使用方法：**

1. **搜索优惠（CheapShark）：**
    ```bash
    python3 scripts/game_tool.py deals "Game Name"
    ```
    *示例：* `python3 scripts/game_tool.py deals "Batman"`

2. **在 Steam 上搜索：**
    ```bash
    python3 scripts/game_tool.py search "Game Name"
    ```
    *示例：* `python3 scripts/game_tool.py search "Elden Ring"`

3. **查看游戏详情（Steam）：**
    ```bash
    python3 scripts/game_tool.py details <APPID>
    ```
    *示例：* `python3 scripts/game_tool.py details 1245620`

## 注意事项：
- 该脚本需要 Python 3 环境。
- 不需要安装任何外部库（使用标准的 `urllib` 库）。

---
*由 Cachitos 为 Ivan 热情制作。*