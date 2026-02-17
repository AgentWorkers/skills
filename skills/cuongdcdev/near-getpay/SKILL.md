---
name: near-getpay
description: 通过集成 PingPay 或 HOT PAY 的美观支付页面，接受加密货币支付（NEAR、USDC、USDT）。
---
# NEAR 支付技能

通过集成 PingPay 或 HOT PAY 的美观支付页面，接受加密货币支付（NEAR、USDC、USDT）。

## 🎯 功能介绍

我们提供了一个托管的支付页面，用户只需点击几下即可使用加密货币支付给您：

1. **美观的用户界面**：适用于移动设备的支付页面，支持预设金额。
2. **支持多种加密货币**：接受 NEAR、USDC 或 USDT。
3. **双支付提供商支持**：同时支持 PingPay 和 HOT PAY（或两者均可）。
4. **公开 URL**：通过 `localhost.run` 隧道生成并公开访问。
5. **新手友好**：设置向导可指导新用户完成配置。
6. **智能的代币选择**：选择一种代币后，其他代币会自动隐藏，避免混淆（尤其适用于 HOT PAY，因为每种代币都有唯一的支付链接）。

## 🎨 用户使用流程

### PingPay 流程（默认，最佳流程）
1. 用户选择代币（NEAR、USDC 或 USDT）。
2. 用户输入金额或选择预设金额。
3. 点击“立即支付”。
4. 重定向至 PingPay 的支付页面，金额已预先填写。

### HOT PAY 流程
1. 用户选择代币（仅显示已配置的代币）。
2. 其他代币会自动隐藏，避免混淆。
3. 用户输入金额或选择预设金额。
4. 点击“立即支付”。
5. 重定向至对应的 HOT PAY 支付链接。

## 🚀 快速入门

### 1. 安装

```bash
cd ~/.openclaw/skills
# Clone or extract the skill
npm install
```

### 2. 选择支付提供商

您需要选择 **PingPay** 或 **HOT PAY**（或两者均可）：

**选项 A：PingPay**（推荐给新手）：
- 在 https://pingpay.io 注册。
- 在控制台 → 设置中配置您的 NEAR 钱包。
- 从控制台 → 设置 → API 密钥中获取 API 密钥。
- 将 API 密钥添加到 `.env` 文件中：`PINGPAY_API_KEY=your_key_here`。

**选项 B：HOT PAY**（适用于高级用户）：
- 访问 https://pay.hot-labs.org/admin/overview。
- 为每种代币（NEAR、USDC、USDT）创建支付链接。
- 在创建链接时将您的 NEAR 钱包设置为收款人。
- 复制每个链接的 `item_id` 并添加到 `.env` 文件中。

### 3. 配置

将 `.env.example` 文件复制到 `.env` 文件中：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# Display name (actual recipient is set in PingPay/HOT PAY dashboard!)
RECIPIENT_ADDRESS=your-account.near

# Choose provider
PAYMENT_PROVIDER=pingpay  # or 'hotpay'

# PingPay config (if using PingPay)
PINGPAY_API_KEY=your_api_key_here

# HOT PAY config (if using HOT PAY)
HOTPAY_NEAR_ITEM_ID=your_near_item_id
HOTPAY_USDC_ITEM_ID=your_usdc_item_id
HOTPAY_USDT_ITEM_ID=your_usdt_item_id
```

### 4. 启动服务器

```bash
./start.sh
```

或者手动启动服务器：

```bash
npx ts-node start-tunnel.ts
```

这将：
- 在端口 3000 上启动 Express 服务器。
- 生成一个可共享的支付链接。

### 5. 分享链接

分享生成的 `https://xxxxx.lhr.life` 链接以接受支付！

## ⚠️ 重要说明

### 收款人地址配置

收款人地址（支付款项的接收地址）是在支付提供商处配置的，**不在 `.env` 文件中设置**：
- **PingPay**：在 PingPay 控制台 → 设置 → 钱包地址中设置。
- **HOT PAY**：在创建每个支付链接时设置。

`.env` 文件中的 `RECIPIENT_ADDRESS` 仅用于在支付页面上显示。要更改付款的实际接收地址，请更新支付提供商的控制台设置。

### 隧道域名

`localhost.run` 生成的 URL 是随机的，并会在重启后更改。如需使用固定域名：
1. 在 https://admin.localhost.run/ 注册。
2. 配置您的自定义域名。
3. 更新 `start-tunnel.ts` 文件中的隧道配置。

或者使用您自己的反向代理（如 Cloudflare Tunnel、ngrok 等）。

## 📖 在 OpenClaw 中使用

当用户请求接受支付时：

```
User: "Create a payment page to accept USDT donations"

Agent:
1. Check if near-getpay skill is installed
2. Ask which provider they want (PingPay or HOT PAY)
3. Guide them through setup if not configured
4. Run: cd ~/.openclaw/skills/near-getpay && ./start.sh
5. Share the generated public URL
```

### 示例对话流程

```
User: I need to accept crypto payments

Agent: I'll set up a payment page for you using the GetPay skill.

First, do you have a PingPay or HOT PAY account?

User: No, what's easier?

Agent: PingPay is simpler. Here's what to do:

1. Sign up at https://pingpay.io
2. Add your NEAR wallet address in settings
3. Get an API key from Dashboard → API Keys
4. Share it with me (or add to .env yourself)

Let me know when you have the API key!

User: Got it: sk_test_abc123...

Agent: Perfect! Starting your payment server...

[runs start.sh]

✅ Your payment page is live:
https://abc123xyz.lhr.life

Share this link to accept NEAR, USDC, or USDT payments!
```

## 🛠️ 文件结构

```
near-getpay/
├── SKILL.md              ← You are here
├── package.json
├── tsconfig.json
├── .env.example          ← Config template
├── .env                  ← Your config (gitignored)
├── start.sh              ← Quick start script
├── start-tunnel.ts       ← Server + tunnel launcher
├── server-simple.ts      ← Main payment server
└── scripts/
    ├── pingpay-client.ts
    └── payment-orchestrator.ts
```

## 🔧 高级配置

### 自定义端口

编辑 `.env` 文件以更改端口：

```env
PORT=8080
```

### 自定义隧道

在 `start-tunnel.ts` 文件中替换 `localhost.run`：

```typescript
// Option 1: ngrok
const tunnel = spawn('ngrok', ['http', PORT.toString()]);

// Option 2: Cloudflare Tunnel
const tunnel = spawn('cloudflared', ['tunnel', '--url', `http://localhost:${PORT}`]);

// Option 3: localtunnel (less reliable)
const tunnel = spawn('npx', ['localtunnel', '--port', PORT.toString()]);
```

### Webhook 集成（仅限 HOT PAY）

HOT PAY 会向 `/webhook/hotpay` 发送 Webhook 请求。要使用此功能：
1. 公开您的服务器地址（不要使用 `localhost.run`，需要一个稳定的 URL）。
2. 在 HOT PAY 控制台中配置 Webhook 地址。
3. 服务器会自动记录支付确认信息。

## 🎨 自定义设置

### 支付金额

在 `server-simple.ts` 文件中修改预设金额：

```typescript
tokens: [
  {
    symbol: 'NEAR',
    chain: 'NEAR',
    decimals: 24,
    presets: [0.5, 1, 5, 10]  // ← Change these
  },
  // ...
]
```

### 品牌定制

在 `server-simple.ts` 的 HTML 模板中修改颜色、字体和文本。

### 添加更多代币

需要支付提供商的支持，可以将新的代币添加到 `tokens` 数组中：

```typescript
{
  symbol: 'ETH',
  chain: 'NEAR',
  decimals: 18,
  presets: [0.01, 0.05, 0.1, 0.5]
}
```

## 🐛 故障排除

### “未配置支付提供商”

访问 `http://localhost:3000/setup` 查看设置指南。

### “权限被拒绝（publickey）”（使用 `localhost.run` 时）

运行命令：`ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa -N ""`

### “隧道关闭”

`localhost.run` 在长时间无操作后会关闭隧道。请重启服务器。

### “代币未配置”（使用 HOT PAY 时）

您需要为每种代币创建相应的支付链接。未配置的代币将不会显示在支付页面上。

### 支付提供商返回错误

- **PingPay**：检查 API 密钥是否有效以及账户是否处于活跃状态。
- **HOT PAY**：确认 `item_ids` 与您创建的链接是否匹配。

## 🔐 安全性

- ✅ API 密钥存储在 `.env` 文件中（该文件会被 Git 忽略）。
- ✅ 不需要私钥（支付直接发送给支付提供商）。
- ✅ 通过隧道使用 HTTPS 协议。
- ✅ 支付请求会经过 Webhook 签名验证（HOT PAY）。

**请勿将 `.env` 文件提交到 Git！**

## 📦 分享此技能

### 作为技能包分享

```bash
# From the skill directory
openclaw skill pack

# Share the .skill file
# Users install with: openclaw skill install near-getpay.skill
```

### 通过 GitHub 分享

```bash
git init
git add .
git commit -m "Initial commit: NEAR GetPay skill"
git remote add origin https://github.com/yourusername/near-getpay.git
git push -u origin main
```

用户可以通过以下方式安装此技能包：

```bash
cd ~/.openclaw/skills
git clone https://github.com/yourusername/near-getpay.git
cd near-getpay
npm install
```

### 通过 Clawhub 分享

1. 访问 https://clawhub.com。
2. 上传 `.skill` 包。
3. 添加描述和标签。
4. 发布技能包！

## 🤝 技术支持

- **问题反馈**：通过 GitHub 的 Issues 功能提交问题。
- **PingPay**：https://pingpay.io/docs
- **HOT PAY**：https://pay.hot-labs.org/admin
- **OpenClaw**：https://docs.openclaw.ai

## 📝 许可证

MIT 许可证

---

**专为 OpenClaw 设计** 🐾