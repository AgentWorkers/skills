---
name: leak
description: 使用 `leak` CLI 工具来购买或出售基于 x402 协议的数字内容。在卖家端，当用户希望发布、分发或“泄露”某份文件并希望收取费用时，可以使用此功能；在买家端，当用户希望下载需要付费的文件时，也可以使用此功能。
compatibility: Requires access to the internet
version: 2026.2.15
metadata:
  openclaw:
    emoji: 💦
    os: ["darwin", "linux"]
    requires:
      env:
      bins: ["node", "leak"]
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

该技能用于操作 `leak` 命令行工具（CLI）：
- **发布** 本地文件，并设置 x402 状态码为 `402 Payment Required`（表示需要支付）。
- **分享** 促销链接（`/`），以便在社交媒体上分享或让代理发现该文件。
- **购买** 文件（通过促销链接 `/` 或下载链接 `/download`），并将文件保存到本地。

## 安全政策（强制要求）

每次使用该技能时，请遵守以下规则：
1. **严禁** 在命令参数中请求、存储或传递原始私钥。
2. **默认情况下** 不会创建钱包。只有在用户明确同意的情况下，才允许创建钱包。
3. **在发布文件之前**，必须获得用户的明确确认。
4. **在公开文件之前**，必须获得用户的明确同意（使用 `--public` 选项）。
5. **禁止** 在常规输出中显示私钥内容。

## 命令使用说明

如果 `leak` 已经安装在系统的 PATH 环境变量中，可以直接使用该命令：

```bash
leak --help
```

如果 `leak` 未安装，可以使用以下命令进行一次性安装：

```bash
npx -y leak-cli@2026.2.14 --help
```

**请勿** 从该技能中运行自动安装或通过 Git 克隆相关的脚本。

## 发布内容（卖家）

当用户请求发布、出售或泄露文件时，激活该功能。

### 必需输入参数：
1. 文件路径（必须是普通文件）。
2. 价格（以 USDC 为单位）。
3. 销售窗口的持续时间。
4. 卖家的收款地址（`--pay-to`）。
5. 是否公开文件（`--public`）。

### CLI 实施的安全限制：
1. **拒绝** 目录和符号链接的上传。
2. **默认情况下**，禁止上传敏感文件路径（如 `~/.ssh`、`~/.aws`、`~/.gnupg`、`~/.config/gcloud`、`/etc`、`/proc`、`/sys`、`/var/run/secrets`）。
3. 如果使用了 `--public` 选项，必须获得用户的明确确认。

### 本地发布

```bash
bash skills/leak/scripts/publish.sh \
  --file ./protected/asset.bin \
  --price 0.01 \
  --window 15m \
  --pay-to 0xSELLER_ADDRESS \
  --network eip155:84532
```

### 公开发布

```bash
bash skills/leak/scripts/publish.sh \
  --file ./protected/asset.bin \
  --price 0.01 \
  --window 15m \
  --pay-to 0xSELLER_ADDRESS \
  --public
```

该工具会输出以下信息：
- **促销链接：** `https://.../`
- **购买链接：** `https://.../download`

请将促销链接（`/`）分享到社交媒体上。

## 购买内容（买家）

当用户请求购买或下载文件时，激活该功能。

### 买家快速操作流程（强制要求）

对于未知的购买链接，请按照以下流程操作：
1. 如果系统中没有 `leak` 工具，请先安装它。
2. 询问用户是否拥有现有的购买密钥文件路径。
3. 如果用户没有密钥文件，可以提供以下替代方案：
   “我可以在 `./.leak/buyer.key` 文件中生成一个新的购买密钥。这是一个临时钱包，请确保资金量较少，并安全地备份密钥。”
4. **仅当用户明确同意** 时，才执行以下密钥生成流程。
5. 运行以下命令：

```bash
bash skills/leak/scripts/buy.sh "<promo_or_download_url>" --buyer-private-key-file <buyer_key_file_path>
```

6. 报告下载的文件路径和下载的字节数。

**x402 购买流程的支付规则**：
- **仅使用** 服务器在 `402 Payment Required` 响应中提供的支付令牌/资产及金额（例如 `0.01 USDC`）。
- **标准 x402 购买流程** 中，**不允许** 使用响应中未指定的资产作为支付手段。
- **只有在 `leak buy` 命令返回与气体费用相关的错误时**，才需要用户提供气体费用的相关信息。

默认的密钥生成方式为 `--buyer-private-key-file`。如果用户要求使用标准输入（stdin），则使用 `--buyer-private-key-stdin`。

**禁止以下操作**：
1. **不要** 在聊天中请求用户的原始私钥文本。
2. **不要** 在开始购买流程之前进行手动 x402 转账或签名操作。
3. **在尝试购买之前**，不要向用户展示多个复杂的选项。
4. **如果 402 响应中未指定气体费用所需的资产**，**不要** 告诉用户需要 ETH 来支付气体费用。

如果用户明确询问相关协议细节，再向其解释 x402 的内部工作原理。

### 明确同意后的密钥生成流程（确定性操作）

**仅在用户明确同意生成密钥后**，使用以下流程：
1. 确认目标文件路径：`./.leak/buyer.key`。
2. 创建一个仅限所有者访问的目录和密钥文件：
   - 目录权限：`0700`
   - 密钥文件权限：`0600`
3. 将私钥以十六进制字符串的形式写入密钥文件中（不要添加 `0x` 前缀）。
4. **禁止** 在常规输出中显示私钥内容。只需显示生成的钱包地址即可。
5. **如果当前工作区是 Git 仓库**，请告知用户会将密钥路径添加到 `.gitignore` 文件中以防止文件被跟踪，然后执行以下操作：

```bash
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  touch .gitignore
  grep -qxF "./.leak/buyer.key" .gitignore || echo "./.leak/buyer.key" >> .gitignore
fi
```

6. 继续执行购买流程：

```bash
bash skills/leak/scripts/buy.sh "<promo_or_download_url>" --buyer-private-key-file ./.leak/buyer.key
```

### 买家首次回复模板

在收到文件链接后，使用以下回复内容：
1. 确认链接类型（促销链接 `/` 或下载链接 `/download`）。
2. 请求用户批准安装 `leak` 工具：`clawhub install leak`。
3. 询问用户是否拥有现有的购买密钥文件路径。
4. 提供替代方案：`如果您需要，我可以在 `./.leak/buyer.key` 中为您生成一个新的密钥。`

### 密钥处理要求

**必须使用以下两种方式之一**：
1. `--buyer-private-key-file <路径>`
2. `--buyer-private-key-stdin`

**禁止使用** `--buyer-private-key` 选项。

### 购买示例

```bash
bash skills/leak/scripts/buy.sh "https://xxxx.trycloudflare.com/" --buyer-private-key-file ./buyer.key
```

```bash
cat ./buyer.key | bash skills/leak/scripts/buy.sh "https://xxxx.trycloudflare.com/" --buyer-private-key-stdin
```

### 可选的输出控制选项

```bash
bash skills/leak/scripts/buy.sh "https://xxxx.trycloudflare.com/" --buyer-private-key-file ./buyer.key --out ./downloads/myfile.bin
```

```bash
bash skills/leak/scripts/buy.sh "https://xxxx.trycloudflare.com/" --buyer-private-key-file ./buyer.key --basename myfile
```

## 故障排除：
- 如果出现 “`leak: command not found`” 错误，**请执行以下操作**：
  - 全局安装 `leak-cli`：`npm i -g leak-cli`
  - 或者使用固定版本的 `leak-cli`：`npx -y leak-cli@2026.2.14 --help`
- 如果出现 “无效的卖家收款地址” 错误，请使用有效的以太坊地址（格式为 `0x` + 40 个十六进制字符）。
- 如果使用 `--public` 选项时出现确认失败，请重新运行命令，并按照提示提供正确的确认语句。