---
name: bits-mcp
description: 通过 Bits MCP 服务器控制浏览器自动化代理。适用于执行网页抓取、表单填写、数据提取或任何基于浏览器的自动化任务。Bits 代理能够浏览网站、点击页面元素、填写表单、处理 OAuth 流程以及提取结构化数据。
---

# Bits MCP – 浏览器自动化平台

Bits 是一个基于人工智能的浏览器自动化平台。通过 MCP 服务器，您可以从自己的 AI 助手中执行浏览器自动化任务。

## 设置

### 1. 获取 API 密钥

1. 访问 [app.usebits.com](https://app.usebits.com)
2. 使用 Google 登录
3. 转到 **设置 → API 密钥**
4. 点击 **创建 API 密钥**，为其命名
5. 复制密钥（密钥以 `bb_` 开头）——您之后将无法再次看到该密钥

### 2. 配置 MCP

将以下配置添加到您的 MCP 配置文件中（例如：`~/.openclaw/openclaw.json`）：

```json
{
  "mcpServers": {
    "bits": {
      "command": "npx",
      "args": ["-y", "usebits-mcp"],
      "env": {
        "BITS_API_KEY": "bb_your_key_here"
      }
    }
  }
}
```

对于 Claude 代码（位于 `~/.claude.json` 中）：

```json
{
  "mcpServers": {
    "bits": {
      "command": "npx",
      "args": ["-y", "usebits-mcp"],
      "env": {
        "BITS_API_KEY": "bb_your_key_here"
      }
    }
  }
}
```

### 3. 重启

重启您的网关/客户端以应用新的 MCP 服务器配置。

## 使用方法

Bits MCP 支持“代码模式”：您需要编写 TypeScript SDK 代码，这些代码将在沙箱环境中执行。平台提供了两种工具：

1. **文档搜索** – 查询 SDK 文档
2. **代码执行** – 使用 TypeScript 编写并运行代码以与 Bits SDK 交互

### 示例：抓取网站数据

```
Use the Bits MCP to go to news.ycombinator.com and get the top 5 story titles
```

代理程序将：
1. 在文档中查找用于导航和数据抓取的方法
2. 编写 TypeScript 代码来导航网站并提取数据
3. 执行代码并返回结果

### 示例：填写表单

```
Use Bits to go to example.com/contact, fill out the contact form with name "Test" and email "test@example.com", then submit
```

### 示例：提取结构化数据

```
Use Bits to scrape the product listings from example-store.com/products and return them as JSON with name, price, and URL fields
```

## 功能

- **导航** – 访问指定 URL，处理重定向
- **读取页面内容** – 提取文本、获取页面布局，截取屏幕截图
- **交互** – 点击页面元素、填写输入框、按键操作
- **处理身份验证** – 处理 OAuth 弹出窗口、登录表单、双因素认证（使用已保存的凭据）
- **多窗口操作** – 在标签页或弹出窗口之间切换
- **结构化输出** – 以特定的 JSON 格式返回数据

## 创建工作流（可选）

对于重复性任务，可以在 Bits 的 Web 应用中创建工作流：

1. 访问 [app.usebits.com](https://app.usebits.com) → **工作流**
2. 创建一个工作流，并为其指定操作步骤
3. （可选）为结构化响应定义输出格式
4. 通过 API 运行工作流：`POST /workflows/{id}/runs`

## 故障排除

- **“API 密钥无效”**：请确认密钥以 `bb_` 开头，并且已正确复制。
- **启动缓慢**：首次运行时，系统会通过 `npx` 下载 MCP 相关包，后续运行会更快。
- **任务卡住**：浏览器自动化过程中可能会遇到验证码或意外弹出的窗口。请检查响应中的实时视图 URL。

## 链接

- Web 应用：[app.usebits.com](https://app.usebits.com)
- API 文档：[api.usebits.com/openapi.json](https://api.usebits.com/openapi.json)