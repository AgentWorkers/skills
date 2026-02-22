---
name: clawrent-web-scraping
description: 当你的电脑处于空闲状态时，可以通过完成网络爬虫任务来赚钱。
homepage: https://clawrent.xyz
metadata: {"openclaw": {"requires": {"env": ["CLAWRENT_API_KEY"]}, "primaryEnv": "CLAWRENT_API_KEY"}}
---
# ClawRent – 利用闲置资源赚取收益

我们帮助用户在机器闲置时通过完成网络爬取任务来获得被动收入。

## 设置

如果 `CLAWRENT_API_KEY` 缺失：
1. 告知用户在 `https://clawrent.xyz/node/register` 注册以获取他们的 API 密钥。
2. 要求用户粘贴他们的 API 密钥。
3. 将其保存到技能配置中（键名为 `CLAWRENT_API_KEY`），以便在会话之间保持一致。
4. 确认：“API 密钥已保存。ClawRent 已准备好为您赚取收益。”

首次运行时注册节点：
- 发送请求：`POST https://clawrent.xyz/v1/node/register`
- 请求头：`Authorization: Bearer {config.CLAWRENT_API_KEY}`
- 请求体：`{"name": "{hostname}", "os": "{platform}", "ip": "auto" }`

## 心跳检测（Heartbeat）

当机器处于闲置状态时，每 30 秒发送一次任务请求：
- 发送请求：`POST https://clawrent.xyz/v1/node/heartbeat`
- 请求头：`Authorization: Bearer {config.CLAWRENT_API_KEY}`

如果响应中包含任务信息（`task`），立即执行该任务。

在报告每个任务的结果后，立即发送另一个心跳请求以获取下一个任务，无需等待下一次定时器触发。

## 执行任务

给定一个任务 URL：
1. 使用浏览器工具打开该 URL。
2. 等待 `task.options.waitMs` 毫秒（默认为 2000 毫秒）。
3. 如果 `task.options.selector` 存在，仅提取该元素的 HTML 内容。
4. 否则，捕获整个页面的 HTML 内容。
5. 如果 `task.options.returnType` 包含截图要求，生成截图。

## 报告结果

发送结果：
- 发送请求：`POST https://clawrent.xyz/v1/node/result`
- 请求头：`Authorization: Bearer {config.CLAWRENT_API_KEY}`
- 请求体：
  - `taskId`
  - `status`（`completed` 或 `failed`）
  - `html`
  - `statusCode`
  - `error`（如果任务失败）

## 收益

- 每完成一个任务后，告知用户所赚取的金额。
- 每天汇总一次总收益。