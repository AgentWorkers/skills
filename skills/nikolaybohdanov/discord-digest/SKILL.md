---
name: discord-digest
description: >
  **使用用户令牌从 Discord 服务器生成格式化的摘要**  
  该工具能够从指定的频道/帖子中读取消息，并生成包含链接的简洁摘要。适用于生成 Discord 服务器摘要、监控频道动态或创建活动报告。支持多服务器配置、交互式频道选择、令牌验证（包含过期通知功能），以及自定义时间范围设置。
---
# Discord Digest

该工具可以从 Discord 服务器中生成格式化的摘要信息。用户无需使用任何机器人，只需提供自己的 Discord 用户令牌即可。

## 设置

### 1. 获取 Discord 用户令牌

在浏览器中获取令牌：进入 Discord（网页版）→ 按 F12 → 打开“网络”选项卡 → 找到任意 API 请求 → 查看“请求头”中的 `Authorization` 值。

```bash
python3 scripts/config_manager.py set-token "YOUR_TOKEN"
```

### 2. 扫描并选择服务器

列出用户所属的所有服务器：

```bash
python3 scripts/discord_api.py "TOKEN" guilds
```

### 3. 扫描并选择频道

列出特定服务器中的所有频道：

```bash
python3 scripts/discord_api.py "TOKEN" channels SERVER_ID
```

### 4. 将服务器添加到配置文件中

将选定的服务器信息添加到配置文件中：

```bash
python3 scripts/config_manager.py add-server '{"id":"SERVER_ID","name":"Server Name","channels":[{"id":"CH_ID","name":"channel-name","type":"text"}]}'
```

## 使用方法

### 生成摘要信息

使用 `run_digest.py` 脚本生成摘要信息：

```bash
python3 scripts/run_digest.py [--hours 24] [--server SERVER_ID]
```

### 验证令牌

在每次运行工具之前，会通过 `GET /users/@me` 请求来验证令牌的有效性。如果返回 401 错误，将执行以下操作：
1. 通知用户：“⚠️ Discord 令牌已过期，请重新获取新令牌。”
2. 等待用户获取新的令牌。
3. 更新配置文件：`python3 scripts/config_manager.py set-token "NEW_TOKEN"`
4. 重新运行工具以生成摘要信息。

## 输出格式

生成的摘要信息将按照预设的格式显示。

## 配置文件

配置文件位于 `~/.openclaw/workspace/config/discord-digest.json`：

```json
{
  "discord_token": "...",
  "servers": [
    {
      "id": "829331298878750771",
      "name": "DOUBLETOP SQUAD",
      "channels": [
        {"id": "1238663837515911198", "name": "drops-alerts", "type": "text"}
      ]
    }
  ],
  "digest_period_hours": 24
}
```

## 脚本说明

- `discord_api.py`：用于与 Discord API 进行通信的客户端脚本（需要用户令牌进行身份验证）。
- `digest_formatter.py`：负责将获取到的消息格式化为摘要格式。
- `config_manager.py`：用于管理用户令牌、服务器信息以及频道配置。
- `run_digest.py`：程序的主入口脚本，负责执行令牌验证、数据读取和摘要生成等操作。

## 速率限制

Discord API 的请求速率限制为每秒约 1 次请求；如果遇到 429 错误（请求速率超过限制），系统会自动尝试重试。该工具集包含了内置的速率限制处理机制（采用指数级退避策略）。

## 重要提示：

- 使用用户令牌可能违反 Discord 的服务条款，请仅限于个人用途。
- 令牌可能会过期，该工具提供了令牌验证和失效通知功能。
- 该工具完全依赖 Python 3 的标准库（`urllib`、`json`）进行开发，无需任何外部依赖。