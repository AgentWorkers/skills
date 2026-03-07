---
name: pet-me-master
description: 通过 Bankr 批量处理 Aavegotchis 货币的借出操作，同时实现冷却时间检查、提醒自动化以及基于自然语言的路由功能。
homepage: https://github.com/aaigotchi/pet-me-master
metadata:
  openclaw:
    requires:
      bins:
        - cast
        - jq
        - curl
        - python3
      env:
        - BANKR_API_KEY
---
# **Pet Me Master**

这是一个专为 Aavegotchis 设计的批量宠物互动脚本：

- **功能说明：**
  - 识别出由用户代理钱包拥有的 Aavegotchis。
  - 将这些 Aavegotchis（包括被委托/借出的 Aavegotchis）添加到用户的钱包中。
  - 检查这些 Aavegotchis 在链上的“冷却时间”（`lastInteracted`字段）。
  - 对所有符合条件的 Aavegotchis 发送一个 `interact(uint256[])` 交易请求。
  - 如果用户没有响应，系统会自动发送提醒并执行默认的宠物互动操作。

## **配置文件（`~/.openclaw/workspace/skills/pet-me-master/config.json`）**

```json
{
  "walletResolutionOrder": [
    "PET_ME_WALLET_ADDRESS",
    "BANKR_WALLET_ADDRESS"
  ],
  "reminderChatResolutionOrder": [
    "PET_ME_TELEGRAMCHAT_ID",
    "TELEGRAMCHAT_ID",
    "config.reminderTelegramChatId"
  ]
}
```

## **Bankr 认证**

该脚本直接通过 Bankr API 提交交易请求。API 密钥的来源包括：
- 环境变量 `BANKR_API_KEY`。
- 通过 `systemctl --user` 导出的环境变量。
- 文件 `~/.openclaw/skills/bankr/config.json` 中的 `apiKey`。
- 文件 `~/.openclaw/workspace/skills/bankr/config.json` 中的 `apiKey`。

## **脚本说明：**

- `./scripts/check-cooldown.sh [gotchi-id]`：检查指定 Aavegotchis 的冷却时间。
- `./scripts/pet-all.sh [--dry-run]`：批量获取用户拥有的及被委托的 Aavegotchis，并对符合条件的 Aavegotchis 执行宠物互动操作。
- `./scripts/pet.sh [--dry-run]`：`pet-all.sh` 的简化版本，用于批量执行宠物互动操作。
- `./scripts/pet-status.sh`：显示用户拥有的及被委托的 Aavegotchis 的当前状态。
- `./scripts/check-status.sh`：`pet-status.sh` 的简化版本，用于检查 Aavegotchis 的状态。
- `./scripts/pet-command.sh [--dry-run] [--tx-dry-run] "<natural-language command>"`：将用户输入的自然语言命令转换为批量执行的形式。
- `./scripts/check-and-remind.sh`：检查 Aavegotchis 的状态并发送提醒。
- `./scripts/auto-pet-fallback.sh`：在用户未响应时自动执行宠物互动操作。
- `./scripts/schedule-dynamic-check.sh`：定期检查 Aavegotchis 的状态。

## **自然语言命令示例：**

（此处应提供具体的自然语言命令示例，但原文未提供。）

## **操作说明：**

- **冷却时间设置：** 冷却时间为 43260 秒（12 小时 + 1 分钟）。
- **提醒机制：** 当所有可互动的 Aavegotchis 都满足条件时，系统会发送提醒。
- **默认行为：** 如果用户没有响应，系统会在配置的延迟时间（默认为 1 小时）后自动执行宠物互动操作。
- **自动执行与手动执行：** 无论是自动执行还是手动执行宠物互动操作，都采用批量处理的方式。

## **故障排除：**

- **问题1：** 无法识别代理钱包地址。** 请确保设置了 `PET_ME_WALLET_ADDRESS` 或 `configwalletAddress`。
- **问题2：** 缺少 Bankr API 密钥。** 请确保导出了 `BANKR_API_KEY` 或在配置文件中设置了正确的 API 密钥。
- **问题3：** 缺少 Telegram 聊天 ID。** 请确保设置了 `PET_ME_TELEGRAMCHAT_ID` 或 `config.reminderTelegramChatId`。
- **问题4：** 冷却时间检查失败。** 请检查 `rpcUrl`、合约地址以及与 Base RPC 服务的连接是否正常。