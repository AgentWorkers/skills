---
name: agentscale
description: 使用单个命令将Web应用程序和API部署到公共URL。
required_tools: ["tar"]
---
## 免费 tier

- 开始使用无需注册或支付费用。
- 运行 `npx agentscale register` 命令以获取 API 密钥。
- 免费部署的服务会在 1 小时后失效。
- 仅支持部署 1 个服务。

## 付费 tier

- 购买信用额度可消除服务的 1 小时时效限制，并实现永久部署。
- 使用 `npx agentscale account` 命令查看您的等级和信用余额。
- 需要添加信用额度时，可以使用 `agentspend pay` 命令或 AgentSpend 工具。

## 命令

### 注册

```bash
npx agentscale register
```

生成 API 密钥，并将其保存到 `~/.agentscale/config.json` 文件中。

### 部署

```bash
npx agentscale deploy
```

在项目目录中运行此命令。该命令会打包当前目录中的所有文件并完成部署。

**选项：**
- `--name <name>` — 服务名称（省略时将自动生成）

### 列出

```bash
npx agentscale list
```

列出您的服务及其状态。

### 账户信息

```bash
npx agentscale account
```

显示您的账户等级（免费/付费）和信用余额。

**添加信用额度的方法：**

使用 `agentspend pay` 命令；

或者直接使用 x402 钱包进行支付，通过发送 `POST /add-credits` 请求，请求头中需包含 `x-api-key`，请求体中需包含 `amount_cents` 参数。

## 项目要求

- 支持部署 API 和 Web 服务。支持的语言包括 Node.js、Python、Go 等。
- 您的项目需要具备以下标准结构才能被自动识别：
  - **Node.js：** 需有包含启动脚本的 `package.json` 文件。
  - **Python：** 需有 `requirements.txt` 文件。
  - **Go：** 需有 `go.mod` 文件。
- 目前不支持自定义域名、构建命令和启动命令。

## 环境变量

- `AGENTSCALE_API_URL` — 可覆盖默认的 API 基本地址。**注意：** 此设置会将所有 API 请求（包括携带 API 密钥的请求）重定向到指定的地址。

## 系统要求

- 系统路径（PATH）中必须包含 `tar` 命令，用于打包项目以进行部署。

## 限制

- 上传文件大小限制：压缩后不超过 100 MB，解压后不超过 500 MB。