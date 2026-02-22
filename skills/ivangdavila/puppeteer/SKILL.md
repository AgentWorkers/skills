---
name: Puppeteer
slug: puppeteer
version: 1.0.0
homepage: https://clawic.com/skills/puppeteer
description: 使用 Puppeteer 自动化 Chrome 和 Chromium 浏览器，以实现数据抓取、测试、截图以及各种浏览器相关操作。
metadata: {"clawdbot":{"emoji":"🎭","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以获取集成指南。

## 使用场景

当用户需要浏览器自动化功能时（如网络爬取、端到端测试、PDF生成、截图或任何无头浏览器操作），该工具非常实用。该工具可处理页面导航、元素交互、等待策略以及数据提取等任务。

## 架构

脚本及输出文件位于 `~/puppeteer/` 目录下。具体结构请参考 `memory-template.md`。

```
~/puppeteer/
├── memory.md       # Status + preferences
├── scripts/        # Reusable automation scripts
└── output/         # Screenshots, PDFs, scraped data
```

## 快速参考

| 主题 | 文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 内存模板 | `memory-template.md` |
| 选择器使用指南 | `selectors.md` |
| 等待策略 | `waiting.md` |

## 核心规则

### 1. 动作前务必等待
在页面导航后，切勿立即点击或输入内容。务必等待相关元素加载完成：
```javascript
await page.waitForSelector('#button');
await page.click('#button');
```
不等待直接点击元素时，90% 的情况下会导致“元素未找到”的错误。

### 2. 使用具体的选择器
优先使用以下稳定性的选择器：
1. `[dataTestId="submit"]` — 基于属性的选择器（最稳定）
2. `#unique-id` — 基于 ID 的选择器
3. `form button[type="submit"]` — 结合语义和标签的选择器
4. `.class-name` — 基于类的选择器（稳定性较低，容易发生变化）

**避免使用：** `div > div > div > button` — 这种选择方式在 DOM 变更时容易出错。

### 3. 明确处理页面导航
执行点击操作后，需等待新页面完全加载：
```javascript
await Promise.all([
  page.waitForNavigation(),
  page.click('a.next-page')
]);
```
如果不等待，脚本会在新页面加载之前继续执行后续操作。

### 4. 设置合理的视口
始终设置合理的视口以保持页面渲染的一致性：
```javascript
await page.setViewport({ width: 1280, height: 800 });
```
默认视口为 800x600，但许多网站的渲染效果可能不同，因此需要根据实际情况进行调整。

### 5. 处理弹窗和对话框
在弹窗或对话框阻塞用户操作之前，先将其关闭：
```javascript
page.on('dialog', async dialog => {
  await dialog.dismiss(); // or dialog.accept()
});
```
未处理的弹窗会导致脚本暂停执行。

### 6. 在出现错误时关闭浏览器
所有代码操作都应使用 `try/finally` 语句进行异常处理：
```javascript
const browser = await puppeteer.launch();
try {
  // ... automation code
} finally {
  await browser.close();
}
```
未关闭的浏览器进程会占用系统资源。

### 7. 遵守请求速率限制
合理控制请求频率以避免被网站封禁：
```javascript
await page.waitForTimeout(1000 + Math.random() * 2000);
```
频繁请求可能导致网站触发验证码或 IP 封禁。

## 常见问题

- 对不可见元素调用 `page.click()` 时，操作会失败（无提示）；此时应使用 `waitForSelector` 并设置 `visible: true`。
- 如果要截图的元素位于屏幕之外，截图结果可能为空；请先将元素滚动到可见位置。
- `page.evaluate()` 方法返回 `undefined` 时，表示无法获取 DOM 节点，只能获取可序列化的数据。
- 无头浏览器可能被某些网站阻止；此时可以使用 `headless: 'new'` 或设置合适的用户代理。
- 表单提交后页面会重新加载，此时需使用 `page.waitForNavigation()` 确保数据不会丢失。
- 阴影 DOM（shadow DOM）中的元素可能无法被选择器访问；此时可以使用 `page.evaluateHandle()` 来获取这些元素。
- 如果 cookie 无法持久保存，可以使用 `userDataDir` 参数来保存会话数据。

## 安全性与隐私

**数据存储位置：**
- 所有爬取的数据存储在 `~/puppeteer/output/` 目录下。
- 浏览器配置信息保存在指定的 `userDataDir` 目录中。

**本工具不会：**
- 将爬取的数据发送到任何外部服务器。
- 存储用户凭证（用户需要为每个脚本单独提供凭证）。
- 访问 `~/puppeteer/` 目录之外的文件。

## 相关技能
如果用户需要，可以使用以下命令安装相关工具：
- `clawhub install <slug>`：安装其他自动化工具（如 `playwright`）
- `chrome`：用于 Chrome 开发工具和调试。
- `web`：用于通用网页开发。

## 反馈建议：
- 如果觉得本工具有用，请给它打星（使用 `clawhub star puppeteer`）。
- 保持更新：通过 `clawhub sync` 功能获取最新信息。