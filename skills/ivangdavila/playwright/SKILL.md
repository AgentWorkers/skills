---
name: Playwright
description: 编写、调试和维护 Playwright 测试脚本以及数据抓取工具；使用具有高稳定性的选择器（resilient selectors）来处理那些容易出错的测试用例（flaky tests）；并实现与持续集成/持续部署（CI/CD）系统的集成。
---

## 触发器（Trigger）

在编写 Playwright 测试、调试错误、使用 Playwright 进行数据抓取，或设置 CI/CD 流程时可以使用触发器。

## 选择器优先级（Selector Priority, 始终适用）

1. `getByRole()` — 可访问性高，稳定性好
2. `getByTestId()` — 明确且稳定
3. `getByLabel()`、`getByPlaceholder()` — 用于选择表单元素
4. `getByText()` — 用于选择可见内容（优先匹配精确内容）
5. CSS/XPath — 最后选择，避免使用 `nth-child` 或动态生成的类名

## 核心功能（Core Capabilities）

| 功能 | 参考文档 |
|------|-----------|
| 测试框架与 POM 配置 | `testing.md` |
| 选择器策略 | `selectors.md` |
| 数据抓取模式 | `scraping.md` |
| CI/CD 集成 | `ci-cd.md` |
| 错误调试 | `debugging.md` |

## 重要规则（Important Rules）

- **切勿使用 `page.waitForTimeout()`** — 应使用 `waitFor*` 方法或带有轮询机制的 `expect` 方法
- **务必关闭浏览器上下文** — 使用 `browser.close()` 或 `context.close()` 以防止内存泄漏
- **谨慎使用 `networkidle`** — 由于单页应用（SPA）可能永远不会进入“空闲”状态，建议使用基于 DOM 的等待机制
- **为独立测试启用并行执行** — 使用 `test.describe.configure({ mode: 'parallel' })`
- **仅在失败时进行日志记录** — 在配置文件中设置 `trace: 'on-first-retry'`，而非始终记录日志

## 快速解决方法（Quick Fixes）

| 问题 | 解决方案 |
|---------|-----|
| 元素未找到 | 在进行交互前使用 `waitFor()`，检查页面上下文 |
- 点击操作不稳定 | 先使用 `click({ force: true })` 或 `waitFor({ state: 'visible' })`
- CI 测试超时 | 增加超时时间，添加 `expect.poll()`，检查视口大小 |
- 元素状态失效 | 重新查询元素定位器，避免存储元素引用 |
- 测试之间丢失认证信息 | 使用 `storageState` 保存 cookie 或 localStorage 数据