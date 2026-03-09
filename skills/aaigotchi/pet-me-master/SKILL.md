---
name: pet-me-master
description: 通过 Bankr 批量处理 Aavegotchis 的交易，包括冷却时间检查、提醒自动化以及自然语言路由功能。
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
  - 自动发现用户代理钱包中拥有的 Aavegotchis。
  - 从 Base 核心子图中将用户代理钱包中委托（出借）的 Aavegotchis 添加到用户的钱包中。
  - 检查这些 Aavegotchis 在链上的冷却时间（`lastInteracted` 字段）。
  - 对所有符合条件的 Aavegotchis 发送一个 `interact(uint256[])` 交易请求。
  - 如果用户没有响应，系统会发送提醒信息并自动执行宠物互动操作。

## **配置文件：**
  创建 `~/.openclaw/workspace/skills/pet-me-master/config.json` 文件：

### 钱包地址解析顺序：
1. `PET_ME_WALLET_ADDRESS` / `BANKR_WALLET_ADDRESS`
2. `configwalletAddress` / `configwallet`
3. Bankr 提示信息：`What is my Base wallet address?`（用于获取 Base 钱包地址）

### 提醒信息发送顺序：
1. `PET_ME_TELEGRAMCHAT_ID`
2. `TELEGRAMCHAT_ID`
3. `config.reminderTelegramChatId`（或 `configTelegramChatId`）

## **Bankr 认证：**
  该脚本直接通过 Bankr API 提交交易请求。API 密钥的来源包括：
  - 环境变量 `BANKR_API_KEY`
  - 通过 `systemctl --user` 导出的环境变量
  - 文件 `~/.openclaw/skills/bankr/config.json` 中的 `apiKey`
  - 文件 `~/.openclaw/workspace/skills/bankr/config.json` 中的 `apiKey`

## **脚本说明：**
- `./scripts/check-cooldown.sh [gotchi-id]`：检查指定 Aavegotchis 的冷却时间。
- `./scripts/pet-all.sh [--dry-run]`：发现用户拥有的及被委托的 Aavegotchis，并对符合条件的 Aavegotchis 执行批量宠物互动操作。
- `./scripts/pet.sh [--dry-run]`：`pet-all.sh` 的简化版本。
- `./scripts/pet-status.sh`：显示已发现的用户拥有的及被委托的 Aavegotchis 的状态。
- `./scripts/check-status.sh`：`pet-status.sh` 的简化版本。
- `./scripts/pet-command.sh [--dry-run] [--tx-dry-run] "<自然语言命令>"`：将用户输入的自然语言命令转换为批量操作。
- `./scripts/check-and-remind.sh`：检查 Aavegotchis 的状态并发送提醒信息。
- `./scripts/auto-pet-fallback.sh`：等待所有符合条件的 Aavegotchis 都准备好后，自动执行宠物互动操作，并通过 Telegram 发送总数和被互动的 Aavegotchis 的 ID。
- `./scripts/auto-pet-at-cooldown.sh`：循环检查所有符合条件的 Aavegotchis 的状态，直到它们都准备好后，执行批量宠物互动操作并发送通知。

## **自然语言命令处理：**
（示例命令未在提供的代码块中列出，但通常会包含类似 “pet my-gotchi” 的命令。）

### **操作说明：**
- 冷却时间阈值设置为 43260 秒（12 小时 + 1 分钟）。
- 当所有符合条件的 Aavegotchis 都准备好后，系统会触发提醒信息。
- 如果用户没有采取任何操作，系统会在配置的延迟时间后自动执行宠物互动操作（默认为 1 小时）。
- 自动执行宠物互动操作和手动执行宠物互动操作都使用批量处理流程。

## **故障排除：**
- **问题1：无法解析代理钱包地址**：请设置 `PET_ME_WALLET_ADDRESS` 或 `configwalletAddress`。
- **问题2：缺少 Bankr API 密钥**：请导出 `BANKR_API_KEY` 或配置 Bankr 技能的 API 密钥。
- **问题3：缺少 Telegram 聊天 ID**：请设置 `PET_ME_TELEGRAMCHAT_ID` 或 `config.reminderTelegramChatId`。
- **问题4：冷却时间检查失败**：请检查 `rpcUrl`、合约地址以及与 Base RPC 服务的连接是否正常。