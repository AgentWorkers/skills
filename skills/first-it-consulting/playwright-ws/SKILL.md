---
name: playwright-ws
description: 通过远程 Playwright WebSocket 服务器实现浏览器自动化，用于截图、生成 PDF 文件以及进行测试。
metadata: {"clawdbot":{"emoji":"🎭","requires":{"bins":["node"],"env":["PLAYWRIGHT_WS"]},"primaryEnv":"PLAYWRIGHT_WS"}}
---
# Playwright 技能

通过 Playwright 的 WebSocket 服务器实现远程浏览器自动化。无需在本地安装浏览器。

## 使用场景

| 任务 | 脚本 | 描述 |
|------|--------|-------------|
| 截图 | `scripts/screenshot.js` | 捕获网页截图 |
| 生成 PDF | `scripts/pdf-export.js` | 从 URL 生成 PDF 文件 |
| 远程测试 | `scripts/test-runner.js` | 远程运行 Playwright 测试 |

## 安装

```bash
cd playwright-skill
npm install
export PLAYWRIGHT_WS=ws://your-server:3000
```

## 快速入门

```bash
# Screenshot
node scripts/screenshot.js https://example.com screenshot.png --full-page

# PDF
node scripts/pdf-export.js https://example.com page.pdf
```

## 配置

将 `PLAYWRIGHT_WS` 环境变量设置为你的 Playwright WebSocket 服务器地址：

```bash
export PLAYWRIGHT_WS=ws://your-playwright-server:3000
```

## 脚本

- `screenshot.js` - 带参数截图 |
- `pdf-export.js` - 生成 PDF 文件 |
- `test-runner.js` - 远程运行测试 |

## 参考资料

- `references/selectors.md` - 选择器策略 |
- `references/api-reference.md` - API 文档