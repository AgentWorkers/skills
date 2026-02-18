---
name: videogames
slug: videogames
display_name: Video Games
description: 一种用于查询电子游戏信息（如价格、兼容性以及游戏时长）的技能。
author: ivanheral
version: 1.0.1
license: MIT
---
# 视频游戏技能 🎮

此技能使 OpenClaw 能够搜索游戏、查看 Steam 上的游戏详情、检查与 ProtonDB 的兼容性、使用 HowLongToBeat 估算游戏时长，以及通过 CheapShark 找到最优惠的价格。

## 工具

### `scripts/game_tool.py`

这个 Python 脚本可以与多个游戏 API（Steam、CheapShark、ProtonDB）进行交互。

**使用方法：**

1. **搜索优惠信息（CheapShark）：**
    ```bash
    python3 scripts/game_tool.py deals "Game Name"
    ```

2. **检查兼容性（ProtonDB）：**
    ```bash
    python3 scripts/game_tool.py compatibility <APPID>
    ```

3. **获取游戏时长（HowLongToBeat）：**
    ```bash
    python3 scripts/game_tool.py duration "Game Name"
    ```

4. **查看游戏详情与规格（Steam）：**
    ```bash
    python3 scripts/game_tool.py details <APPID>
    ```

## 注意事项：
- 该脚本需要 Python 3 环境。
- 不需要安装任何外部库。