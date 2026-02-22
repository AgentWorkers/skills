---
name: playwright-scraper-skill
description: 基于 Playwright 的 Web 抓取工具 OpenClaw 技能，具备反机器人保护功能。已在 Discuss.com.hk 等复杂网站上成功测试。
version: 1.2.0
author: Simon Chan
---

# Playwright 抓取技能

这是一个基于 Playwright 的 Web 抓取工具，具备反爬虫保护功能。根据目标网站的反爬虫强度，可以选择最适合的方法。

---

## 🎯 使用场景矩阵

| 目标网站 | 反爬虫强度 | 推荐方法 | 脚本 |
|---------------|----------------|-------------------|--------|
| **普通网站** | 低 | OpenClaw 的 `web_fetch` 工具 | 不需要（内置） |
| **动态网站** | 中等 | **Playwright Simple** | `scripts/playwright-simple.js` |
| **受 Cloudflare 保护的网站** | 高 | **Playwright Stealth** ⭐ | `scripts/playwright-stealth.js` |
| **YouTube** | 特殊情况 | **deep-scraper** | 需单独安装 |
| **Reddit** | 特殊情况 | **reddit-scraper** | 需单独安装 |

---

## 📦 安装

```bash
cd playwright-scraper-skill
npm install
npx playwright install chromium
```

---

## 🚀 快速入门

### 1️⃣ 普通网站（无反爬虫保护）

使用 OpenClaw 内置的 `web_fetch` 工具：

```bash
# Invoke directly in OpenClaw
Hey, fetch me the content from https://example.com
```

---

### 2️⃣ 动态网站（需要 JavaScript）

使用 **Playwright Simple**：

```bash
node scripts/playwright-simple.js "https://example.com"
```

**示例输出：**
```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "content": "...",
  "elapsedSeconds": "3.45"
}
```

---

### 3️⃣ 受反爬虫保护的网站（如 Cloudflare 保护的网站）

使用 **Playwright Stealth**：

```bash
node scripts/playwright-stealth.js "https://m.discuss.com.hk/#hot"
```

**功能特点：**
- 隐藏自动化标记（`navigator.webdriver = false`）
- 使用真实的用户代理（iPhone、Android）
- 通过随机延迟模拟人类行为
- 支持截图和保存 HTML 内容

---

### 4️⃣ YouTube 视频字幕提取

使用 **deep-scraper**（需单独安装）：

```bash
# Install deep-scraper skill
npx clawhub install deep-scraper

# Use it
cd skills/deep-scraper
node assets/youtube_handler.js "https://www.youtube.com/watch?v=VIDEO_ID"
```

---

## 📖 脚本说明

### `scripts/playwright-simple.js`
- **适用场景：** 普通动态网站
- **速度：** 快速（3-5 秒）
- **反爬虫措施：** 无
- **输出格式：** JSON（标题、内容、URL）

### `scripts/playwright-stealth.js` ⭐
- **适用场景：** 受 Cloudflare 或其他反爬虫保护的网站
- **速度：** 中等（5-20 秒）
- **反爬虫措施：** 中等强度（隐藏自动化行为，使用真实用户代理）
- **输出格式：** JSON + 截图 + HTML 文件
- **测试结果：** 在 Discuss.com.hk 上的成功率为 100%）

---

## 🎓 最佳实践

### 1. 先尝试使用 `web_fetch`
如果网站没有动态加载内容，直接使用 OpenClaw 的 `web_fetch` 工具，速度最快。

### 2. 需要处理 JavaScript？使用 Playwright Simple
如果需要等待 JavaScript 完成渲染，使用 `playwright-simple.js`。

### 3. 被阻止怎么办？使用 Playwright Stealth
如果遇到 403 错误或 Cloudflare 的反爬虫机制，使用 `playwright-stealth.js`。

### 4. 特殊网站需要专门的处理方法
- YouTube：使用 `deep-scraper`
- Reddit：使用 `reddit-scraper`
- Twitter：使用其他专门的抓取工具

---

## 🔧 自定义设置

所有脚本都支持环境变量：

```bash
# Set screenshot path
SCREENSHOT_PATH=/path/to/screenshot.png node scripts/playwright-stealth.js URL

# Set wait time (milliseconds)
WAIT_TIME=10000 node scripts/playwright-simple.js URL

# Enable headful mode (show browser)
HEADLESS=false node scripts/playwright-stealth.js URL

# Save HTML
SAVE_HTML=true node scripts/playwright-stealth.js URL

# Custom User-Agent
USER_AGENT="Mozilla/5.0 ..." node scripts/playwright-stealth.js URL
```

---

## 📊 性能比较

| 方法 | 速度 | 反爬虫效果 | 在 Discuss.com.hk 上的成功率 |
|--------|-------|----------|-------------------------------|
| web_fetch | ⚡ 最快 | ❌ 无反爬虫保护 | 0% |
| Playwright Simple | 🚀 快速 | ⚠️ 反爬虫效果较弱 | 20% |
| **Playwright Stealth** | ⏱️ 中等 | ✅ 中等强度 | **100%** |
| Puppeteer Stealth | ⏱️ 中等 | ✅ 中等强度 | 约 80% |
| Crawlee（deep-scraper） | 🐢 较慢 | ❌ 被轻易检测到 | 0% |
| Chaser（Rust） | ⏱️ 中等 | ❌ 被轻易检测到 | 0% |

---

## 🔧 反爬虫技术总结

从我们的测试中得出的经验：

### ✅ 有效的反爬虫措施：
1. **隐藏 `navigator.webdriver`** — 必须执行
2. **使用真实的用户代理** — 使用真实的设备（如 iPhone、Android）
3. **模拟人类行为** — 通过随机延迟和滚动操作
4. **避免使用特定框架的标识** — 如 Crawlee、Selenium 等容易被识别
5. **使用 `addInitScript`（Playwright）** — 在页面加载前注入脚本

### ❌ 无效的反爬虫措施：
1. **仅更改用户代理** — 不够有效
2. **使用高级抓取框架（如 Crawlee）** — 更容易被检测到
3. **使用 Docker 进行隔离** — 对抗 Cloudflare 保护无效

---

## 🔍 故障排除

### 问题：遇到 403 禁止访问错误
**解决方案：** 使用 `playwright-stealth.js`

### 问题：遇到 Cloudflare 的挑战
**解决方案：**
1. 增加等待时间（10-15 秒）
2. 尝试将 `headless` 参数设置为 `false`（有时全屏模式成功率更高）
3. 考虑使用代理 IP

### 问题：页面为空
**解决方案：**
1. 增加 `waitForTimeout` 的时间
2. 使用 `waitUntil: 'networkidle'` 或 `'domcontentloaded'` 等方法
3. 检查是否需要登录

---

## 📝 性能与测试结果

### 2026-02-07 在 Discuss.com.hk 的测试结果
- ✅ 仅使用 Playwright 和 Playwright Stealth 的组合成功（5 秒内完成，200 个请求全部成功）
- ❌ Crawlee（deep-scraper）失败（收到 403 错误）
- ❌ Chaser（Rust）失败（遇到 Cloudflare 防护）
- ❌ Puppeteer 失败（收到 403 错误）

**最佳解决方案：** 仅使用 Playwright 并结合反爬虫技术（不依赖特定抓取框架）

---

## 🚧 未来改进计划
- [ ] 添加代理 IP 旋转功能
- [ ] 实现 cookie 管理（保持登录状态）
- [ ] 处理验证码（支持多种验证码类型）
- [ ] 批量抓取（同时处理多个 URL）
- [ ] 与 OpenClaw 的 `browser` 工具集成

---

## 📚 参考资料
- [Playwright 官方文档](https://playwright.dev/)
- [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth)
- [deep-scraper 技术文档](https://clawhub.com/opsun/deep-scraper)