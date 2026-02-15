---
name: chia-walletconnect
description: **Chia钱包的Telegram Web应用程序**  
该应用程序支持通过`WalletConnect`和`Sage`进行钱包验证。用户可以利用`MintGarden` API通过签名验证来证明自己对钱包的所有权。
metadata: {"clawdbot":{"requires":{"bins":["node"]},"install":[]}}
---

# Chia WalletConnect 技能

通过使用 Sage Wallet 与 WalletConnect 的集成，在 Telegram 中验证 Chia 钱包的所有权。

## 功能概述

此技能提供了一个 **Telegram 迷你应用**（Web 应用），允许用户：
1. 通过 WalletConnect v2 连接他们的 Sage Wallet
2. 对挑战消息进行加密签名
3. 通过 MintGarden 的签名验证 API 验证钱包所有权
4. 将验证状态返回给您的 Telegram 机器人

**使用场景：**
- 需要 NFT 访问权限的 Telegram 群组
- 空投资格验证
- Web3 风格的身份验证
- DAO 投票身份验证
- 代币持有证明

## 架构

```
/verify command → Web App button → WalletConnect → Sage signs → Verification
```

用户无需离开 Telegram，整个流程都在 Telegram Web 应用程序内部通过 API 完成。

## 安装

```bash
# Install via ClawdHub
clawdhub install chia-walletconnect

# Install dependencies
cd skills/chia-walletconnect
npm install

# Make CLI executable
chmod +x cli.js
```

## 部署

### 第一步：部署 Web 应用

将 `webapp/` 文件夹部署到公共 HTTPS 地址：

**推荐使用 Vercel：**
```bash
cd skills/chia-walletconnect/webapp
vercel
# Copy the URL (e.g., https://chia-verify.vercel.app)
```

**Netlify：**
```bash
cd skills/chia-walletconnect/webapp
netlify deploy --prod
```

**使用自己的服务器：**
```bash
# Start Express server
npm start
# Expose via ngrok or reverse proxy
```

### 第二步：在 BotFather 中注册

1. 向 [@BotFather](https://t.me/BotFather) 发送消息
2. 发送 `/newapp` 或 `/editapp`
3. 选择您的机器人
4. **Web 应用 URL：** 输入已部署的 URL
5. **简称：** `verify`

### 第三步：将应用添加到机器人中

#### 使用 Clawdbot 消息工具

```javascript
// Send /verify command handler
message({
  action: 'send',
  target: chatId,
  message: 'Click below to verify your Chia wallet:',
  buttons: [[{
    text: '🌱 Verify Wallet',
    web_app: { url: 'https://your-app.vercel.app' }
  }]]
});
```

#### 处理验证响应

```javascript
// In your bot's web_app_data handler
bot.on('web_app_data', async (msg) => {
  const data = JSON.parse(msg.web_app_data.data);
  const { address, message, signature, publicKey, userId } = data;
  
  // Verify signature
  const { verifySignature } = require('./skills/chia-walletconnect/lib/verify');
  const result = await verifySignature(address, message, signature, publicKey);
  
  if (result.verified) {
    // Wallet verified! Grant access, record verification, etc.
    message({
      action: 'send',
      target: msg.chat.id,
      message: `✅ Wallet verified!\n\nAddress: ${address}`
    });
    
    // Store verification
    // await db.saveVerification(userId, address);
  } else {
    message({
      action: 'send',
      target: msg.chat.id,
      message: `❌ Verification failed: ${result.error}`
    });
  }
});
```

## 命令行接口（CLI）使用

该技能包含一个用于测试的 CLI：

```bash
# Generate challenge message
node cli.js challenge xch1abc... telegram_user_123

# Verify signature manually
node cli.js verify xch1abc... "message" "signature" "pubkey"

# Validate address format
node cli.js validate xch1abc...

# Start development server
node cli.js server
```

## API 参考

### MintGarden 签名验证

**端点：** `POST https://api.mintgarden.io/address/verify_signature`

```json
{
  "address": "xch1abc...",
  "message": "Verify ownership of Chia wallet:...",
  "signature": "hex_signature",
  "pubkey": "hex_public_key"
}
```

**响应：**
```json
{
  "verified": true
}
```

### CHIP-0002 方法（WalletConnect）

| 方法 | 功能 |
|--------|---------|
| `chip0002_getPublicKeys` | 从钱包获取公钥 |
| `chip0002_signMessage` | 请求消息签名 |
| `chia_getCurrentAddress` | 获取当前接收地址 |

## 验证流程

```
1. User sends /verify to bot
2. Bot responds with Web App button
3. User taps button → Mini App opens in Telegram
4. Mini App initializes WalletConnect
5. User connects Sage Wallet
6. Challenge message generated (includes nonce + timestamp)
7. User signs message in Sage Wallet
8. Signature sent back to bot via Telegram.WebApp.sendData()
9. Bot verifies signature with MintGarden API
10. Bot confirms verification success/failure
```

**时间：** 完整流程大约需要 5-10 秒（具体取决于用户操作）

## 配置

### 环境变量

在技能文件夹中创建 `.env` 文件：

```env
PORT=3000
WALLETCONNECT_PROJECT_ID=your-project-id
MINTGARDEN_API_URL=https://api.mintgarden.io
```

### 获取 WalletConnect 项目 ID

1. 访问 [WalletConnect Cloud](https://cloud.walletconnect.com)
2. 创建一个新的项目
3. 复制您的项目 ID
4. 在 `webapp/app.js` 中更新该 ID

**默认项目 ID：**  
此技能使用 `6d377259062295c0f6312b4f3e7a5d9b`（参考示例：Dracattus）。在生产环境中，请使用您自己的项目 ID。

## 安全性

### 保护措施

- ✅ 挑战令牌（challenge nonce）可防止重放攻击
- ✅ 时间戳在 5 分钟后失效
- ✅ 使用 MintGarden 的加密验证机制
- ✅ 从不请求用户的私钥
- ✅ Telegram 强制使用 HTTPS 协议

### 最佳实践

1. **安全存储验证结果** — 使用加密数据库
2. **设置请求速率限制** — 防止频繁的验证请求
3. **关联 Telegram 用户 ID** — 防止地址欺骗
4. **实施冷却机制** — 每用户每天仅允许进行一次验证
5. **记录请求日志** — 用于安全审计

### 生产环境检查清单

- [ ] 部署到 HTTPS 地址（Telegram 的要求）
- [ ] 使用您自己的 WalletConnect 项目 ID
- [ ] 仅对您的域名启用 CORS
- [ ] 为 Webhook 端点设置请求速率限制
- [ ] 将验证结果存储在持久化数据库中
- [ ] 实现网络错误的重试逻辑
- [ ] 设置监控和警报机制

## 文件列表

```
chia-walletconnect/
├── webapp/
│   ├── index.html        # Telegram Web App UI
│   ├── app.js            # WalletConnect logic
│   └── styles.css        # Styling
├── lib/
│   ├── challenge.js      # Challenge generation
│   └── verify.js         # MintGarden API client
├── server/
│   └── index.js          # Express webhook server
├── cli.js                # CLI interface
├── package.json          # Dependencies
├── SKILL.md              # This file
└── README.md             # Full documentation
```

## 故障排除

### Web 应用无法加载

- 确认 HTTPS 部署是否正确（Telegram 要求使用 SSL）
- 检查 URL 是否可公开访问
- 直接在浏览器中测试 URL
- 查看浏览器控制台中的错误信息

### WalletConnect 连接失败

- 确保 Sage Wallet 是最新版本
- 尝试手动输入 URI 而不是扫描 QR 码
- 检查 WalletConnect 项目 ID 是否有效
- 确认 Sage Wallet 支持 WalletConnect v2

### 签名验证失败

- 确保消息格式完全正确
- 验证公钥是否与钱包地址匹配
- 检查 MintGarden API 是否正常运行
- 确认签名编码是否正确（应为十六进制）

### 出现“无公钥”错误

- 某些钱包不通过 WalletConnect 提供公钥
- 验证时公钥是可选的
- 即使没有公钥，签名验证也可以正常进行

## 示例

### 简单的验证机器人示例

```javascript
// Clawdbot skill handler

const { verifySignature } = require('./lib/verify');

// /verify command
if (message.text === '/verify') {
  await message({
    action: 'send',
    target: message.chat.id,
    message: 'Verify your Chia wallet:',
    buttons: [[{
      text: '🌱 Connect Wallet',
      web_app: { url: process.env.WEB_APP_URL }
    }]]
  });
}

// Handle web app data
bot.on('web_app_data', async (msg) => {
  const { address, message: challengeMsg, signature, publicKey } = 
    JSON.parse(msg.web_app_data.data);
  
  const result = await verifySignature(address, challengeMsg, signature, publicKey);
  
  if (result.verified) {
    // Grant access
    await grantAccess(msg.from.id, address);
    await message({
      action: 'send',
      target: msg.chat.id,
      message: `✅ Verified! Welcome, ${address.substring(0, 12)}...`
    });
  } else {
    await message({
      action: 'send',
      target: msg.chat.id,
      message: `❌ Verification failed`
    });
  }
});
```

### NFT 访问控制示例

```javascript
// Check if user owns specific NFT collection

const { verifySignature } = require('./skills/chia-walletconnect/lib/verify');
const mintGarden = require('./skills/mintgarden'); // Assume mintgarden skill exists

bot.on('web_app_data', async (msg) => {
  const { address, message, signature, publicKey } = 
    JSON.parse(msg.web_app_data.data);
  
  // Verify signature first
  const verifyResult = await verifySignature(address, message, signature, publicKey);
  
  if (!verifyResult.verified) {
    return bot.sendMessage(msg.chat.id, '❌ Invalid signature');
  }
  
  // Check NFT ownership
  const nfts = await mintGarden.getNFTsByAddress(address);
  const hasRequiredNFT = nfts.some(nft => 
    nft.collection_id === 'col1required...'
  );
  
  if (hasRequiredNFT) {
    // Grant access to private group
    await inviteToGroup(msg.from.id);
    bot.sendMessage(msg.chat.id, '✅ Access granted! Check your invites.');
  } else {
    bot.sendMessage(msg.chat.id, '❌ You need a Wojak NFT to join!');
  }
});
```

## 性能

| 阶段 | 所需时间 |
|-------|------|
| 初始化 WalletConnect | 约 1-2 秒 |
| 连接批准 | 用户操作时间 |
| 签名请求 | 约 2-5 秒 |
| MintGarden 验证 | 约 0.5-1 秒 |
| **总计** | 约 5-10 秒 |

## 依赖项

- `@walletconnect/sign-client` — WalletConnect v2 的客户端库
- `@walletconnect/utils` — WalletConnect 的辅助工具
- `@walletconnect/types` — TypeScript 类型定义
- `express` — Web 服务器框架
- `node-fetch` — HTTP 请求库
- `cors` — CORS 中间件
- `dotenv` — 环境配置文件

## 版本

1.0.0

## 许可证

MIT — Koba42 Corp

## 链接

- **MintGarden API：** https://api.mintgarden.io/docs
- **WalletConnect：** https://docs.walletconnect.com/
- **Telegram Web 应用：** https://core.telegram.org/bots/webapps
- **Sage Wallet：** https://www.sagewallet.io/
- **CHIP-0002：** https://github.com/Chia-Network/chips/blob/main/CHIPs/chip-0002.md

---

**由 Koba42 Corp 使用 🌱 构建**