---
name: aluvia-web-unblock
description: 使用 Aluvia 移动代理来解除网站封锁、绕过验证码（CAPTCHAs）以及 403 错误。无需浏览器自动化即可进行网页搜索和内容提取。
---

# Aluvia Web Unblock

该功能为使用 Aluvia 移动代理的代理程序提供无法被阻止的网页访问权限。您可以使用此功能搜索网页或从那些阻止机器人、数据抓取工具或数据中心 IP 地址的网站中获取页面内容。

## 功能特点

- 支持无障碍的网页搜索
- 可以以 Markdown 格式获取并提取页面内容
- 能够绕过验证码和反机器人机制
- 避免 403 错误及基于 IP 的访问限制
- 通过 Aluvia 移动 IP 地址路由请求
- 支持代理连接的复用

## 所需条件

- Aluvia API 密钥
- Brave Search API 密钥
- （可选）Aluvia 连接 ID（用于代理连接的复用）

## 设置流程

```bash
cd ~/Projects/agent-scripts/skills/aluvia-web-unblock
npm ci
```

```bash
export ALUVIA_API_KEY=your_aluvia_key
export BRAVE_API_KEY=your_brave_key
```

（可选：）

```bash
export ALUVIA_CONNECTION_ID=your_connection_id
```

## 使用方法

### 网页搜索

```bash
./search.js "query"
./search.js "query" -n 10
./search.js "query" --content
```

### 获取页面内容

```bash
./content.js https://example.com/article
```

## 输出结果

返回结构化的搜索结果以及以 Markdown 格式提取的页面内容。

## 使用场景

- 遇到验证码或 403 错误而被阻止的代理程序
- 无需使用无头浏览器即可进行网页检索
- 用于抓取那些阻止云 IP 地址的网站的数据
- 需要稳定 IP 地址的搜索和数据获取工作流程

## 关键词

- 解封网页（unblock）
- 绕过验证码（bypass captcha）
- 403 错误（403 errors）
- 网站访问限制（website block）
- 移动代理（mobile proxy）
- 网页抓取（web scraping）
- 代理程序数据检索（agent retrieval）
- 反机器人机制（anti-bot）