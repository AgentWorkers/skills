---
name: stealth-browser
description: 一种反检测的网络浏览工具，能够绕过机器人检测、验证码（CAPTCHAs）以及基于IP地址的访问限制。该工具使用了 `puppeteer-extra` 库，并配备了 `stealth` 插件，同时支持可选的住宅代理（residential proxy）功能。适用场景包括：  
(1) 当网站禁止使用无头浏览器（headless browsers）或特定数据中心IP地址进行访问时；  
(2) 需要绕过 Cloudflare 或 Vercel 的安全防护机制时；  
(3) 访问会检测自动化行为的网站（如 Reddit、Twitter/X 等）时；  
(4) 抓取受保护的网站内容时；  
(5) 自动执行需要模拟人类行为的网页操作时。
---

# 隐形浏览器（Stealth Browser）

通过 `puppeteer-extra` 的 `stealth` 插件以及可选的 Smartproxy 居民代理服务，可以绕过机器人检测和 IP 块限制。

## 使用场景

- 遭到无头浏览器或数据中心 IP 块限制的网站
- 需要绕过 Cloudflare/Vercel 保护的网站
- 需要规避自动化检测的网站（如 Reddit、Twitter/X、注册流程、奖励网站）
- 需要抓取受保护内容的网站
- 需要模拟人类行为的网页自动化任务

## 已测试通过的网站：

✅ Relay.link（之前被 Vercel 块禁，现已可正常使用）
✅ X/Twitter 账号操作
✅ 机器人检测测试（sannysoft.com）
✅ 受保护的奖励网站
✅ Reddit（数据中心 IP 块限制）

## 快速入门

```bash
# Basic usage (stealth only)
node scripts/browser.js "https://example.com"

# With residential proxy (bypasses IP blocks)
node scripts/browser.js "https://example.com" --proxy

# Screenshot
node scripts/browser.js "https://example.com" --proxy --screenshot output.png

# Get HTML content
node scripts/browser.js "https://example.com" --proxy --html

# Get text content
node scripts/browser.js "https://example.com" --proxy --text
```

## 设置

### 1. 安装依赖项

```bash
cd /path/to/skill
npm install
```

所需包（通过 `npm install` 自动安装，这些包已包含在 `package.json` 中）：
- `puppeteer-extra`
- `puppeteer-extra-plugin-stealth`
- `puppeteer`

### 2. 配置代理（可选，但推荐）

**如需绕过基于 IP 的限制，请设置 Smartproxy 居民代理：**

创建 `~/.config/smartproxy/proxy.json` 文件：

```json
{
  "host": "proxy.smartproxy.net",
  "port": "3120",
  "username": "smart-ppz3iii4l2qr_area-US_life-30_session-xxxxx",
  "password": "your-password"
}
```

从 Smartproxy 控制台获取凭据：https://dashboard.smartproxy.com

**Smartproxy 会话参数：**
- `_area-US` → 使用美国居民 IP
- `_life-30` → 会话持续 30 分钟
- `_session-xxxxx` → 保持同一 IP（持久会话）

如果不使用代理，浏览器仍会使用 `stealth` 插件来避免检测，但仍可能被基于 IP 的保护机制阻止。

## 工作原理

### 隐形功能

该浏览器采用了多种反检测措施：

1. **puppeteer-extra-plugin-stealth**：自动应用所有隐形规避策略：
   - 移除 `navigator.webdriver` 标志
   - 伪造 Chrome 用户代理和头部信息
   - 模拟插件、语言和权限设置
   - 遮盖自动化操作的痕迹

2. **模拟人类行为**：
   - 逼真的视口尺寸（1920x1080）
   - 更新后的用户代理（Chrome 121）
   - 自然的浏览器行为
   - 不显示任何自动化控制的标志

3. **居民代理**（使用 `--proxy` 参数时）：
   - 通过居民 IP 进行请求
   - 绕过数据中心 IP 块限制
   - 保持同一 IP（持久会话）
   - 默认使用美国地区

### 检测规避效果对比

| 防护方式 | 无头 Puppeteer | Stealth 插件 | 使用居民代理 |
|------------|-------------------|----------------|-------------------|
| `navigator.webdriver` | ❌ 被检测到 | ✅ 被隐藏 | ✅ 被隐藏 |
| 用户代理 | ❌ 通用代理 | ✅ 逼真的用户代理 | ✅ 逼真的用户代理 |
| WebGL/Canvas | ❌ 被识别为无头浏览器 | ✅ 被伪造 | ✅ 被伪造 |
| IP 块限制 | ❌ 被数据中心 IP 块限制 | ❌ 被数据中心 IP 块限制 | ✅ 被居民 IP 块限制 |
| Cloudflare | ❌ 被阻止 | ⚠️ 有时会被阻止 | ✅ 通常可以通行 |
| Turnstile CAPTCHA | ❌ 被阻止 | ❌ 被阻止 | ⚠️ 通过几率降低 |

## 使用示例

### 示例 1：检查网站是否检测自动化行为

```bash
# Test on bot detection site
node scripts/browser.js "https://bot.sannysoft.com" --screenshot detection.png
```

绿色勾选表示未被检测到，红色表示被检测到。

### 示例 2：抓取受保护的页面

```bash
# Get page text content
node scripts/browser.js "https://protected-site.com" --proxy --text > output.txt
```

### 示例 3：监控网站变化

```bash
# Take daily screenshot for comparison
node scripts/browser.js "https://target-site.com" --proxy --screenshot "$(date +%Y-%m-%d).png"
```

### 示例 4：提取结构化数据

```javascript
import { browse } from './scripts/browser.js';

const result = await browse('https://example.com', {
  proxy: true,
  html: true
});

// Parse result.html with cheerio or similar
console.log(result.html);
```

## 代理费用说明

**Smartproxy 居民代理定价：**
- 每 GB 流量约 7.50 美元
- 平均页面加载量：1-3 MB
- 大致费用：每页 0.01-0.03 美元

**何时使用代理：**
- 网站明确禁止使用数据中心 IP（如 Reddit、某些奖励网站）
- 遭到 Cloudflare/Vercel 保护的网站
- 来自同一 IP 的多次请求被限制
- 需要根据地理位置进行请求（例如美国与国际地区）

**仅使用隐形模式时：**
- 网站仅检测自动化操作的痕迹，而不关注 IP
- 对于 IP 块限制影响较小的低价值抓取任务
- 测试/开发阶段（代理费用较高）

## 故障排除

### 浏览器启动失败

```
Error: Failed to launch the browser process
```

**解决方案**：安装所需的系统依赖项：

```bash
# Debian/Ubuntu
sudo apt-get install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 \
  libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 \
  libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 \
  libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 \
  libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 \
  libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation \
  libappindicator1 libnss3 lsb-release xdg-utils wget
```

### 代理认证失败

```
Error: net::ERR_PROXY_AUTH_REQUESTED
```

**解决方案**：检查 `~/.config/smartproxy/proxy.json` 中的代理凭据。确保用户名和密码在 Smartproxy 控制台中的信息正确。

### 仍然被检测到

**尝试以下方法：**

1. **更新代理会话 ID**（强制使用新的 IP）：
   ```json
   "username": "smart-ppz3iii4l2qr_area-US_life-30_session-NEW_RANDOM_STRING"
   ```

2. **增加与页面交互前的等待时间**：
   ```javascript
   await page.goto(url, { waitUntil: 'networkidle2' });
   await page.waitForTimeout(5000); // Wait 5s
   ```

3. **重新进行检测测试**：
   ```bash
   node scripts/browser.js "https://bot.sannysoft.com" --proxy --screenshot test.png
   ```

4. **尝试不同的地理位置**（如果特定地区被限制）：
   ```json
   "username": "smart-ppz3iii4l2qr_area-GB_life-30_session-xxxxx"
   ```

## 限制因素

- **CAPTCHA**：隐形模式可以降低被检测到的几率，但不能完全消除 CAPTCHA 挑战。建议结合使用其他 CAPTCHA 解决方案。
- **JavaScript 指纹识别**：高级的指纹识别技术（如 Canvas、WebGL 哈希分析）可能在高度保护的网站上仍能检测到自动化行为。
- **费用**：使用居民代理会产生每次请求的费用。请合理使用。
- **速度**：代理路由和隐形规避机制会增加请求延迟。

## 安全注意事项

- 代理凭据包含敏感的认证信息。请确保 `~/.config/smartproxy/proxy.json` 文件的权限设置为 600（仅允许管理员访问）。
- 绝不要将代理凭据提交到 Git 仓库。
- 居民代理的请求会通过真实的居民 IP 发送。请遵守相关速率限制和服务条款。

## 相关资源

- **2captcha 技巧**：当隐形模式不足以解决问题时，可以使用该技巧来破解 CAPTCHA。
- **Smartproxy 控制台**：https://dashboard.smartproxy.com 可用于监控使用情况。
- **机器人检测测试**：https://bot.sannysoft.com 可用于验证隐形模式的有效性。