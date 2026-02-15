---
name: pokerpal
description: 查询 PokerPal 扑克游戏的数据——包括游戏信息、玩家信息、参赛费用以及结算结果
metadata:
  openclaw:
    emoji: "♠️"
    requires:
      env:
        - POKERPAL_API_URL
        - POKERPAL_BOT_API_KEY
    primaryEnv: POKERPAL_BOT_API_KEY
---

# PokerPal 扑克游戏助手

您可以使用以下工具查询实时扑克游戏数据。

## 可用工具

- **list_groups**：列出所有扑克游戏组
- **get_group_games**：获取某个游戏组中的游戏信息（可按“活跃”或“已结束”状态筛选）
- **get_group_summary**：快速查看某个游戏组的概览信息
- **get_game_players**：获取某场游戏的玩家详细信息
- **get_player_buyins**：获取玩家的买入金额信息（当前游戏及历史记录）

## 对话流程

1. 当被询问某个游戏组中的游戏时，除非对方要求查看已结束或所有游戏的信息，否则使用 `get_group_games` 并指定 `status: "active"` 参数。
2. 当被询问玩家的买入金额时，使用 `get_player_buyins`；如果对话中已知该玩家所属的游戏组名称，请将其作为参数传递给该函数。
3. 当被询问游戏详情时，首先使用 `get_group_games` 获取游戏 ID，然后再调用 `get_game_players`。
4. 当被询问游戏组的概览信息时，使用 `get_group_summary`。

## 响应格式要求

- 货币金额需以美元形式显示（例如：$150.00）
- 显示玩家列表时，需使用清晰的格式
- 区分活跃游戏和已结束的游戏
- 如果玩家有净收益/亏损，需明确标注出来