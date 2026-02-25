---
name: monday
description: "您可以直接通过 Monday.com 的 GraphQL API 读取和查询 Monday.com 上的看板（boards）、项目（items）、工作区（workspaces）以及用户（users）的相关信息。当您需要项目/任务数据、看板内容或团队信息时，可以使用该 API。该 API 直接调用 `api.monday.com`，无需通过任何第三方代理。"
metadata:
  openclaw:
    requires:
      env:
        - MONDAY_API_TOKEN
      bins:
        - python3
    primaryEnv: MONDAY_API_TOKEN
    files:
      - "scripts/*"
---
# Monday.com

您可以通过 `api.monday.com`（使用 GraphQL）直接查看看板（boards）、项目（items）和工作区（workspaces）的相关信息。

## 设置（只需一次）

1. 在 Monday.com 网站上，点击右上角的 **个人头像**。
2. 选择 **开发者**（Developers），这将打开开发者中心。
3. 点击 **API 令牌 → 显示**（API Token → Show）。
4. 复制您的个人 API 令牌。
5. 设置环境变量：
   ```
   MONDAY_API_TOKEN=your_token_here
   ```

## 命令

### 获取您的账户信息
```bash
python3 /mnt/skills/user/monday/scripts/monday.py me
```

### 列出所有看板
```bash
python3 /mnt/skills/user/monday/scripts/monday.py list-boards
python3 /mnt/skills/user/monday/scripts/monday.py list-boards --limit 50
```

### 获取看板详情（包括列和分组）
```bash
python3 /mnt/skills/user/monday/scripts/monday.py get-board <board_id>
```

### 列出看板上的项目
```bash
python3 /mnt/skills/user/monday/scripts/monday.py list-items <board_id>
python3 /mnt/skills/user/monday/scripts/monday.py list-items <board_id> --limit 50
```

### 列出所有工作区
```bash
python3 /mnt/skills/user/monday/scripts/monday.py list-workspaces
```

### 列出所有用户
```bash
python3 /mnt/skills/user/monday/scripts/monday.py list-users
```

## 注意事项

- 免费计划：提供 2 个用户账户和无限数量的看板；免费用户也可以使用 API 功能。
- 看板的 ID 是数字形式的，您可以在看板的 URL 中找到它，或者通过 `list-boards` 命令获取。
- Monday.com 仅使用 GraphQL 进行数据交互（没有 REST API）。
- 当前使用的 API 版本为 `2024-04`。