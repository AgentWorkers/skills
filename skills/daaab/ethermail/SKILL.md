---
name: ethermail
description: 通过 WalletConnect 使用 EtherMail 访问 Web3 电子邮件功能。当您需要使用以太坊钱包地址查看或发送电子邮件、接收来自 Web3 服务的通知，或通过去中心化的电子邮件与其他 AI 代理进行通信时，可以使用此功能。
---

# EtherMail（Web3 邮箱服务）

您可以使用以太坊钱包地址来访问邮箱服务。无需输入电子邮件地址或密码——只需使用钱包进行登录即可！

## 🚀 快速入门

**最简单的方法：** 使用 Telegram Mini 应用！
👉 [在 Telegram 上打开 EtherMail 应用](https://t.me/ethermailappbot/app?startapp=afid_6986e9a5c5a97b905a78c390)

## 先决条件

1. **WalletConnect 连接器**：使用 `walletconnect-agent` 技能或您自己设置的 WalletConnect 服务。
2. **浏览器自动化工具**：Clawdbot 浏览器工具或 Puppeteer。
3. **EVM 钱包**：任何兼容以太坊的钱包地址。

## 您的 EtherMail 地址

您的邮箱地址会自动从您的钱包中生成：
```
<your-wallet-address>@ethermail.io
```
示例：`0xYourWalletAddress@ethermail.io`

您还可以在账户设置中设置自定义别名，例如 `myname@ethermail.io`。

---

## 访问方法

### 方法 1：Telegram Mini 应用（推荐）

访问 EtherMail 的最简单方式：
1. 打开：https://t.me/ethermailappbot/app?startapp=afid_6986e9a5c5a97b905a78c390
2. 通过 WalletConnect 连接您的钱包
3. 直接在 Telegram 中阅读和发送邮件！

### 方法 2：Web 浏览器 + WalletConnect

#### 第 1 步：导航到登录页面

```bash
browser action=navigate profile=clawd targetUrl="https://ethermail.io/accounts/login"
```

#### 第 2 步：点击“使用钱包登录”

找到并点击“使用钱包登录”按钮以触发 WalletConnect 弹窗。

#### 第 3 步：从 Shadow DOM 中提取 WalletConnect URI

EtherMail 会将 WalletConnect 功能嵌入到 Shadow DOM 中。使用以下脚本提取 URI：

```javascript
// Run in browser console or via browser action=act evaluate
function findWalletConnectURI() {
  function searchShadow(root, depth = 0) {
    if (depth > 5) return null;
    const elements = root.querySelectorAll('*');
    for (const el of elements) {
      if (el.shadowRoot) {
        const html = el.shadowRoot.innerHTML;
        const match = html.match(/wc:[a-f0-9]+@2\?[^"'<>\s]+/);
        if (match) return match[0];
        const found = searchShadow(el.shadowRoot, depth + 1);
        if (found) return found;
      }
    }
    return null;
  }
  return searchShadow(document);
}
findWalletConnectURI();
```

或者使用随附的脚本：
```bash
# Returns: wc:abc123...@2?relay-protocol=irn&symKey=xyz...
node scripts/extract-wc-uri.js
```

#### 第 4 步：使用 WalletConnect 连接钱包

使用 `walletconnect-agent` 技能（从 ClawdHub 安装）：

```bash
# Install walletconnect-agent skill first
clawdhub install walletconnect-agent

# Then use its wc-connect.js script
cd ~/clawd/skills/walletconnect-agent
export PRIVATE_KEY="0x..."
node scripts/wc-connect.js "<WC_URI>"
```

该连接器会自动处理 `personal_sign` 请求，完成登录过程。

> ⚠️ **安全提示：** 请始终使用 ClawdHub 提供的官方 `walletconnect-agent` 技能。
> 不要使用未经验证的第三方 WalletConnect 脚本。

#### 第 5 步：访问收件箱

登录成功后，浏览器会重定向到您的收件箱。您可以使用浏览器自动化工具来：
- 阅读邮件
- 撰写新邮件
- 查看通知

---

## Shadow DOM 提取脚本

对于浏览器自动化操作，请使用 `scripts/extract-wc-uri.js`：

```bash
# Usage with Puppeteer
node scripts/extract-wc-uri.js --url "https://ethermail.io/accounts/login"
```

---

## 使用场景

1. **代理间通信**——接收来自其他 AI 代理的邮件。
2. **Web3 通知**——NFT 发布、DAO 投票、DeFi 警报。
3. **去中心化身份验证**——将邮箱与您的链上身份关联。
4. **备用通信渠道**——在其他通信渠道失败时使用。
5. **赚取奖励**——通过阅读推广邮件获得 $EMT 代币奖励。

---

## 故障排除

### 找不到 WalletConnect URI
- Shadow DOM 的搜索深度需要足够深（尝试深度大于 5）。
- URI 只有在 WalletConnect 弹窗完全加载后才会显示。
- 有些浏览器会阻止访问 Shadow DOM——请使用无头版 Chromium 浏览器。

### URI 过期
- WalletConnect URI 会在大约 5 分钟后失效。
- 关闭弹窗并重新打开以获取新的 URI。

### 登录失败
- 确保钱包地址与预期的签名者地址匹配。
- 检查 `wc-connect.js` 是否支持 `personal_sign` 功能。
- 确认您使用的是兼容以太坊的网络。

### CAPTCHA 阻止登录
- EtherMail 在网页上使用了 Turnstile CAPTCHA 验证。
- 建议使用 Telegram Mini 应用以获得更便捷的登录体验。

---

## 安全提示

- ⚠️ 严禁泄露私钥。
- 将凭据存储在环境变量或安全文件中。
- EtherMail 仅需要邮件签名功能（登录不需要进行任何交易）。
- 请使用专用的钱包进行代理操作。
- 使用 ClawdHub 提供的官方 `walletconnect-agent` 技能进行 WalletConnect 集成。
- 为确保安全，浏览器自动化操作应在启用 Puppeteer 沙箱的环境中进行。

---

## 更新日志

### v1.1.0 (2026-02-08) - 安全更新
- 🔐 从 Puppeteer 中移除了 `--no-sandbox` 标志，以增强安全隔离性。
- 📝 明确要求使用 ClawdHub 提供的官方 `walletconnect-agent` 技能。
- 📝 添加了关于供应链安全的说明。

### v1.0.0
- 🎉 首次发布

---

## 链接

- **Telegram 应用：** https://t.me/ethermailappbot/app?startapp=afid_6986e9a5c5a97b905a78c390
- **官方网站：** https://ethermail.io
- **移动应用：** 支持 iOS 和 Android 平台。