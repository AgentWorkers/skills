---
name: leak
description: 使用 leak CLI 工具来购买或出售基于 x402 协议的数字内容。在卖家端，当用户希望发布、上传文件或“泄露”文件并希望收取费用时，可以使用此功能；在买家端，当用户希望下载需要付费的文件时，也可以使用此功能。
compatibility: Requires access to the internet
version: 2026.2.14
metadata:
  openclaw:
    emoji: 💦
    os: ["darwin", "linux"]
    requires:
      env:
      bins: ["leak"]
    install:
      - kind: node
        package: leak-cli
        bins: ["leak"]
        label: "Install leak-cli via npm"
    primaryEnv:
  author: eucalyptus-viminalis
---

# leak

## 概述

该功能通过 `leak` CLI 工具来实现以下操作：
- **发布** 文件：将文件发布到一个需要支付 402 状态码（表示“需要付款”）的服务器，并在付款成功后生成一个限时令牌。
- **分享** 文件：使用 `/` 作为促销链接（适合分享到社交媒体），并使用 `/download` 作为购买链接。
- **购买**：用户可以通过促销链接（`/`）或购买链接（`/download`）购买文件，并将文件保存到本地。

## 术语说明

- `content`、`file`、`artifact`、`media`、`digital good` 这些术语可以互换使用，指代任何格式的数字文件（如 `.mp3`、`.zip`、`.png`、`.md` 等）。
- `publish`、`release`、`sell`、`leak`、`drop`、`serve` 这些术语可以互换使用，表示从主机服务器启动服务，通过带有 402 状态码的下载链接将数字文件发布到互联网上。

## 安装 CLI（第一步）

建议将 `leak` CLI 添加到系统的 PATH 环境变量中。如果未安装，可以先通过 npm 全局安装：

```bash
npm i -g leak-cli
```

如果安装失败，或者需要使用开发环境的配置，请使用 `scripts/ensure_leak.sh` 脚本：

运行以下命令：

```bash
bash scripts/ensure_leak.sh
```

**注意：**
- 首先尝试运行 `npm i -g leak-cli`。
- 如果安装失败，脚本会通过 HTTPS 从 GitHub 克隆 `leak` 仓库，然后执行 `npm install` 和 `npm link`。
- 可以通过 `LEAK_REPO_URL=...` 参数自定义仓库地址。
- 如果有辅助脚本可用，它们会自动执行 `leak` 命令；否则会使用 `npx -y leak-cli`。

## 发布内容（服务器端）

当用户执行以下操作时，该功能会被激活：
- “发布这个文件”
- “分享这个文件”
- “让这个文件可下载”

**推荐做法：** 使用辅助脚本，该脚本会自动完成安装并生成一个清晰的分享链接。

### 交互式流程（推荐）

当用户想要发布文件时，引导他们完成以下步骤：
1. **选择文件**：需要发布哪个文件或文件夹？
2. **设置价格**：需要支付多少 USDC？（例如：0.01 或 1.00）
3. **设置时长**：文件的有效时长是多少？（15 分钟、1 小时、6 小时、24 小时）
4. **是否公开分享**：是否需要公开分享？（需要使用 Cloudflare 服务）
5. **指定支付地址**：付款应发送到哪个以太坊地址？

然后运行发布命令，并提供促销链接和购买链接，其中促销链接将作为默认的分享链接。

### 仅限本地使用（适用于测试）

此方法仅用于测试；当用户希望在公开发布之前测试服务器功能时可以使用。

```bash
bash scripts/publish.sh \
  --file /absolute/or/relative/path/to/file \
  --price 0.01 \
  --window 15m \
  --pay-to 0xSELLER_ADDRESS \
  --network eip155:84532
```

**直接使用 CLI 的命令：**

```bash
leak \
  --file /absolute/or/relative/path/to/file \
  --price 0.01 \
  --window 15m \
  --pay-to 0xSELLER_ADDRESS \
  --network eip155:84532
```

**需要提供给买家的信息：**
- `http://127.0.0.1:4021/`（用于分享的促销链接）
- `http://127.0.0.1:4021/download`（直接购买链接）
- 或者你的局域网 IP 地址（如果需要在同一网络内的其他设备上进行测试）

### 使用 Cloudflare 生成公开链接

**前提条件：** 已安装 Cloudflare 服务。

**安装示例：**

```bash
# macOS (Homebrew)
brew install cloudflared

# Windows (winget)
winget install --id Cloudflare.cloudflared
```

**Linux 系统的安装文档：**
`https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/`

**直接使用 CLI 的命令：**

```bash
leak --file ./protected/asset.bin --price 0.01 --window 15m --pay-to 0x... --public
```

**CLI 会输出以下信息：**
- `[leak] 公开链接：https://xxxx.trycloudflare.com`
- `[leak] 促销链接：https://xxxx.trycloudflare.com/`
- `[leak] 购买链接：https://xxxx.trycloudflare.com/download`

**在社交媒体帖子中分享文件时，请使用 `/` 作为链接；使用 `/download` 进行代理辅助购买。**

**可选的 OpenGraph 图片元数据设置：**

```bash
leak --file ./protected/asset.bin --price 0.01 --window 15m --pay-to 0x... --public \
  --og-title "Nightwire" \
  --og-description "Limited release, agent-assisted purchase" \
  --og-image-url https://cdn.example.com/nightwire-cover.jpg \
  --ended-window-seconds 86400
```

### 确认付款（可选）

使用 `--confirmed` 参数在生成令牌之前确认付款是否完成：

```bash
leak --file ./protected/asset.bin --price 0.01 --window 15m --pay-to 0x... --confirmed
```

当用户希望出售文件时，必须使用此参数，以确保只有在付款确认后才允许买家下载文件。

## 购买文件

当用户执行以下操作时，该功能会被激活：
- “购买这个文件”
- “下载这个文件”
- “获取这个文件”
- 或者直接提供文件链接

**推荐做法：** 使用辅助脚本（确保先完成文件安装）。

**前提条件：** 用户需要拥有兼容以太坊网络的私钥。

### 买家购买流程：

当用户想要购买文件时，请按照以下步骤操作：
1. **获取链接**：获取促销链接或购买链接（如果尚未提供）：
   - 促销链接示例：`https://xxxx.trycloudflare.com/`
   - 购买链接示例：`https://xxxx.trycloudflare.com/download`
2. **检查前提条件**：
   - 用户是否有钱包或私钥？
   - 用户是否有足够的 USDC 来支付文件费用？
3. **如果没有钱包？**
   - 告知用户所需支付的金额，并协助他们创建一个兼容以太坊网络的钱包。
   - 帮助用户安全地保存私钥，并告知他们保存位置。
4. **资金不足？**
   - 告知用户需要支付的 USDC 金额，并等待确认后再尝试。
5. **执行购买操作**：
   - 使用用户的私钥运行购买脚本。
   - 显示交易详情（交易哈希、网络信息）。
   - 确认文件已成功保存。
6. **购买成功**：
   - 确认文件已保存，并告知用户文件的具体保存路径。

**直接使用 CLI 的命令：**

```bash
bash scripts/buy.sh "https://xxxx.trycloudflare.com/" --buyer-private-key 0xBUYER_KEY
```

**可选的文件命名规则：**

```bash
# choose exact output path
leak buy "https://xxxx.trycloudflare.com/" --buyer-private-key 0x... --out ./downloads/myfile.bin

# choose basename, keep server extension
leak buy "https://xxxx.trycloudflare.com/" --buyer-private-key 0x... --basename myfile
```

### 常见买家问题及应对方式：

| 问题 | 响应方式 |
|-------|---------------|
| “我没有钱包” | 建议使用 `eth-account` 工具创建钱包，并安全保存私钥。|
| “我没有 USDC” | 告知所需支付的金额以及获取 USDC 的方法。|
| “交易失败” | 检查交易费用（gas）是否足够，或者尝试重新支付，或者确认销售是否已经结束。|
| “文件已经存在” | 提供覆盖现有文件的选项或选择新的文件名。|

### 买家示例交互：

用户：**“我想购买这个文件：https://abc123.trycloudflare.com/”**

客服：**“我会帮助您下载这个文件。首先，我会查询文件的价格……”**
- **获取 402 状态码以确认价格。**
- **“这个文件的价格是 0.01 USDC。您有 USDC 吗？或者需要帮助创建钱包吗？”**

## 故障排除**

- **“找不到 `leak` 命令”**：运行 `bash skills/leak/scripts/ensure_leak.sh` 或使用 `npx -y leak-cli --help` 来查看命令用法。
- **“卖家提供的支付地址无效”**：确保使用的支付地址是有效的以太坊地址（格式为 `0x` 后跟 40 个十六进制字符）。
- **“使用 `--public` 选项时出现错误”**：请先安装 Cloudflare 服务（在 macOS 上使用 `brew install cloudflared`），然后再尝试。
- **端口已被占用**：尝试使用其他端口号（例如 `--port 4021`），并在配置隧道时使用新的端口号。