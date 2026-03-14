---
name: flatastic
description: 通过 Flatastic 管理家庭共享的杂务、购物清单和开支。当用户询问有关杂务、团队任务、购物清单、开支或 Flatastic 的信息时，请使用该工具。
metadata:
  clawdbot:
    emoji: "🏠"
    requires:
      bins: ["flatastic"]
---
# Flatastic CLI

这是一个用于管理Flatastic（WG-App）中共享家务事务的命令行工具（CLI）。

## 安装

```bash
cd ~/Projects/flatastic-cli
npm install
npm run build
npm link
```

安装完成后，`flatastic`命令将在系统中全局可用。

## 设置

```bash
flatastic auth             # Login with email/password
flatastic refresh          # Refresh WG data from server
```

用户的Token信息以及WG（共享家庭）的相关信息会被保存在`~/.config/flatastic/config.json`文件中。

## 命令

### 家务事务

```bash
flatastic chores           # List all chores with assignee, points, due dates
flatastic done <search>    # Mark chore as done (partial name match)
flatastic remind <search>  # Send reminder notification for a chore
flatastic stats            # Show chore statistics & leaderboard
flatastic history          # Show chore completion history
flatastic history -l 50    # Show last 50 entries
```

### 购物清单

```bash
flatastic shop             # Show pending items (shortcut)
flatastic shop -a          # Show all items (including bought)

flatastic shopping list    # Show pending items
flatastic shopping add "Milch"  # Add item to list
flatastic shopping done milch   # Mark item as bought
flatastic shopping delete milch # Remove item from list
flatastic shopping clear        # Clear all bought items
```

### 开支/财务

```bash
flatastic expenses         # Show recent expenses
flatastic expenses -l 20   # Show last 20 expenses
flatastic balances         # Show who owes whom
flatastic expense "Pizza" 24.50           # Add expense, split with all
flatastic expense "Taxi" 15 -s "David"    # Split only with David
```

### WG（共享家庭）信息

```bash
flatastic wg               # Show WG info and flatmates with points
```

### 通知/公告板

```bash
flatastic shouts           # Show recent shouts
flatastic shout "Pizza ist da!"  # Post a new shout
```

## 使用示例

**“今天有什么任务？”**
```bash
flatastic chores
```

**“请安排吸尘器打扫”**
```bash
flatastic done staubsaugen
```

**“提醒一下垃圾处理的事”**
```bash
flatastic remind müll
```

**“谁的积分最多？”**
```bash
flatastic stats
```

**“我还需要买些什么？”**
```bash
flatastic shop
```

**“把牛奶加到购物清单里”**
```bash
flatastic shopping add "Milch"
```

**“我已经买好了”**
```bash
flatastic shopping done milch
```

**“谁欠谁钱？”**
```bash
flatastic balances
```

**“我花了24欧元买披萨”**
```bash
flatastic expense "Pizza" 24
```

## 发现的API端点

### 家务事务
- `GET /chores` — 列出所有家务任务
- `GET /chores/next?id=&userId=&completedBy=` — 将任务标记为已完成
- `GET /chores/remind?id=` — 发送提醒
- `GET /chores/statistics` — 获取任务完成统计信息
- `GET /chores/history` — 查看任务完成历史
- `POST /chores` — 创建新的家务任务
- `POST /chores/update` — 更新家务任务
- `DELETE /chores/id/:id` — 删除家务任务

### 购物
- `GET /shoppinglist` — 列出所有购物清单项目
- `POST /shoppinglist` — 添加购物项目（格式：`{name: "..."}`
- `GET /shoppinglist/toggle_item?id=` — 切换项目的购买状态（已购买/未购买）
- `DELETE /shoppinglist/item/:id` — 删除购物项目
- `POST /shoppinglist/delete_bought_items` — 清除已购买的物品

### 开支（现金流）
- `GET /cashflow?offset=&limit=` — 列出所有开支记录
- `GET /cashflow/settlement` — 查看谁欠谁钱
- `GET /cashflow/statistics` — 获取开支统计信息
- `POST /cashflow` — 添加新的开支记录
- `DELETE /cashflow/id/:id` — 删除开支记录

### 通知
- `GET /shouts` — 查看所有通知
- `POST /shouts` — 发布新的通知（格式：`{shout: "..."}`
- `DELETE /shouts/id/:id` — 删除通知

### 共享家庭（WG）
- `GET /wg` — 查看共享家庭的相关信息

## 配置文件

配置文件位于`~/.config/flatastic/config.json`：

```json
{
  "token": "...",
  "user": { "id": "...", "firstName": "...", "chorePoints": "..." },
  "wg": {
    "name": "...",
    "flatmates": [{ "id": "...", "firstName": "..." }, ...]
  }
}
```

## 注意事项

- 所有命令都支持部分名称匹配（不区分大小写）
- 开支金额以欧元为单位（例如：`24.50`或`24,50`）
- 通知会发送给指定的接收者。