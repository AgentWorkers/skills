---
name: leak
description: 使用 `leak` CLI 工具来购买或出售基于 x402 标准的数字内容。对于卖家而言，当用户希望发布、释放或“泄露”某个文件并希望收取费用时，可以使用此功能；对于买家而言，当用户希望下载需要付费的文件时，也可以使用此功能。
compatibility: Requires access to the internet
version: 2026.2.15-beta.1
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

该技能用于操作 `leak` 命令行工具（CLI）：
- **发布** 本地文件，并设置 x402 状态码为 “402 Payment Required”（表示需要支付）。
- **分享** 促销链接（`/`），以便在社交媒体上推广或供代理发现使用。
- **购买** 通过促销链接（`/`）或下载链接（`/download`）获取文件，并将其保存到本地。

## 安全政策（强制要求）

每次使用该技能时，请遵守以下规则：
1. **严禁** 在命令参数中请求、存储或传递原始私钥。
2. **默认情况下** 不会创建钱包。只有在用户明确同意的情况下，才允许创建钱包。
3. **在发布文件之前**，必须获得用户的明确确认。
4. **在将文件公开到互联网之前**，必须获得用户的明确同意（使用 `--public` 选项）。
5. **严禁** 在常规输出中显示私钥内容。

## 命令解析

如果 `leak` 已经安装在系统的 PATH 环境变量中，可以直接使用该命令：

```bash
leak --help
```

如果 `leak` 未安装，可以使用以下命令进行一次性安装：

```bash
npx -y leak-cli@2026.2.14 --help
```

**请勿** 从该技能中运行自动安装或通过 git 克隆相关的脚本。

## 发布内容（卖家）

当用户请求发布、出售或泄露文件时，激活该功能。

### 必需输入参数
1. 文件路径（必须是普通文件）。
2. 价格（以 USDC 为单位）。
3. 销售窗口的持续时间。
4. 卖家的收款地址（使用 `--pay-to` 选项指定）。
5. 是否公开文件（使用 `--public` 选项指定）。

### CLI 实施的安全限制
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
- **促销链接**：`https://.../`
- **购买链接**：`https://.../download`

请将促销链接（`/`）分享到社交媒体上。

## 购买内容（买家）

当用户请求购买或下载文件时，激活该功能。

### 买家快速操作流程（强制要求）

对于未知的购买链接，请按照以下默认流程操作：
1. 如果 `leak` 未安装，请先安装它。
2. 询问用户是否拥有现有的买家密钥文件路径。
3. 如果用户没有密钥文件，可以提供以下备用方案：
   “我可以在 `./.leak/buyer.key` 文件中生成一个新的买家密钥。请注意，这是一个临时钱包，因此请保持资金量最小化，并妥善备份密钥。”
4. **只有在用户明确同意的情况下**，才继续执行下面的密钥生成流程。
5. 运行以下命令：

```bash
bash skills/leak/scripts/buy.sh "<promo_or_download_url>" --buyer-private-key-file <buyer_key_file_path>
```

6. 报告保存的文件路径以及下载的字节数。

默认的密钥生成方式为 `--buyer-private-key-file`。如果用户要求通过标准输入（stdin）生成密钥，请使用 `--buyer-private-key-stdin` 选项。

**注意事项**：
1. **严禁** 在聊天中请求用户的原始私钥文本。
2. **不要** 先进行手动的安全传输或签名操作。
3. **在尝试购买之前**，不要向用户展示多个可能的购买选项。

如果用户明确询问相关协议细节，请向其解释 x402 协议的运作原理。

### 明确同意后的密钥生成流程（确定性操作）

只有在用户明确同意创建密钥后，才执行以下流程：
1. 确认密钥文件的保存路径：`./.leak/buyer.key`。
2. 创建一个仅限所有者具有访问权限的目录和密钥文件：
   - 目录权限设置为 `0700`
   - 密钥文件权限设置为 `0600`
3. 将私钥以十六进制字符串的形式写入密钥文件中（不要添加 `0x` 前缀）。
4. **严禁** 在常规输出中显示私钥内容。只需显示生成的钱包地址即可。
5. 如果当前工作区是 Git 仓库，请告知用户会将密钥路径添加到 `.gitignore` 文件中，以防止文件被跟踪。

6. 继续执行购买流程：

```bash
bash skills/leak/scripts/buy.sh "<promo_or_download_url>" --buyer-private-key-file ./.leak/buyer.key
```

### 买家首次回复模板

收到文件链接后，使用以下模板进行回复：
1. 确认链接类型（促销链接 `/` 或下载链接 `/download`）。
2. 请求用户批准安装 `leak` 工具：`clawhub install leak`。
3. 询问用户是否拥有现有的买家密钥文件路径。
4. 提供备用方案：`如果您需要，我可以在 `./.leak/buyer.key` 中为您生成一个新的密钥。`

### 密钥处理要求

只能使用以下两种方式之一：
1. `--buyer-private-key-file <路径>`
2. `--buyer-private-key-stdin`

**严禁** 使用 `--buyer-private-key` 选项，因为它已被禁止使用。

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

## 故障排除
- 如果出现 “`leak: command not found`” 错误，请尝试以下操作：
  - 全局安装 `leak-cli`：`npm i -g leak-cli`
  - 或者使用固定的版本进行安装：`npx -y leak-cli@2026.2.14 --help`
- 如果出现 “无效的卖家收款地址” 错误，请使用有效的以太坊地址（格式为 `0x` + 40 个十六进制字符）。
- 如果在使用 `--public` 选项时出现确认失败，请重新运行命令，并按照提示提供正确的确认语句。