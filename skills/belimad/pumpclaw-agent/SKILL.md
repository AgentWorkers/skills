---
name: pumpclaw-agent
description: 生成适用于客户的 Telegram 轮询机器人，以及基于 Express 框架的 Web 服务器。这些工具能够集成 @pump-fun/agent-payments-sdk，实现 Pump.fun 的代币化代理支付功能（包括生成发票、接收支付以及在 Solana 上验证发票）。当需要实现 Pump.fun 或 Pumpfun 代理的集成、代币化代理支付流程、发票验证功能，或构建 Telegram 与 Web 的集成框架时，可使用这些工具。
---
# PumpClaw Agent — Pump.fun 的令牌化代理服务 + Telegram + Web 服务器

该技能模板用于创建可重用的项目，并根据客户需求进行定制。

**模板路径：** `assets/template/`

**参考文档：** `references/PUMP_TOKENIZED_AGENTS.md`

## 开始前的准备——所需信息**

在编写代码之前，请获取以下信息：

1. **代理令牌铸造地址**（用于铸造 Pump.fun 的令牌化代理）
2. **支付货币**（USDC 或 wSOL）——这将决定 `CURRENCY_MINT` 的值
3. **价格**（最小单位：USDC 保留 6 位小数，SOL 保留 9 位小数）
4. **付款后应提供的内容**（机器人/服务器需要完成的功能）
5. **Solana RPC URL**（必须支持 `sendTransaction` 操作）
6. **Telegram 机器人应提供的命令**（以及提醒/消息的发送方式）

## 安全规则（必须遵守）

- 绝不要记录或输出私钥或敏感信息。
- 绝不要代表用户签署交易。
- 在提供服务之前，务必通过 `validateInvoicePayment` 在服务器端验证支付信息。
- 确保 `amount > 0`，并且 `endTime > startTime`。

## 工作流程

### 第 1 步 — 使用模板创建项目

将 `assets/template/` 复制到新的客户文件夹中（文件夹名称应为项目名称）。

### 第 2 步 — 配置环境变量

确保 `.env.example` 文件包含以下内容：

- `SOLANA_RPC_URL`
- `AGENT_TOKEN_MINT_ADDRESS`
- `CURRENCY_MINT`
- `TELEGRAM_BOT_TOKEN`
- `PORT`

**注意：** 不要创建或提交实际的 `.env` 文件。

### 第 3 步 — 实现 Pump Tokenized Agent 的支付流程

使用 `@pump-fun/agent-payments-sdk`：

- 使用 `buildAcceptPaymentInstructions` 构建支付指令。
- 在服务器端使用 `validateInvoicePayment` 进行验证。

如果需要前端钱包功能，请参考 Pump 的相关技能文档（见 `references/PUMP_TOKENIZED_AGENTS.md`）。

### 第 4 步 — 实现 Telegram 机器人（轮询请求）

实现用户请求的命令，并确保提供 `/help` 命令。

### 第 5 步 — Web 服务器端点

必须包含以下端点：

- `GET /health` → 返回 `{ ok: true }`

根据需求添加与支付相关的端点（例如：创建发票、验证发票等）。

### 第 6 步 — 交付成果

提供以下内容：

- 完整的项目文件夹
- 运行项目的说明文档
- 简易测试 checklist