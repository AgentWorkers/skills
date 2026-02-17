---
name: leak-buy
description: 您可以通过促销活动或下载链接购买并下载泄露的内容，也可以使用预先安装好的泄露内容处理工具（leak CLI）来下载这些内容。
compatibility: Requires access to the internet
version: 2026.2.17
metadata:
  openclaw:
    emoji: 🛒
    os: ["darwin", "linux"]
    requires:
      env:
      bins: ["leak"]
    install:
      - kind: node
        package: leak-cli
        bins: ["leak"]
        label: "Install leak-cli via npm"
  author: eucalyptus-viminalis
---
# leak-buy

## 概述

该技能仅用于执行“leak-buy”工作流程：
- 接受促销链接（`/`）或下载链接（`/download`）。
- 当卖家要求时，包含下载代码。
- 仅当卖家要求时，通过 x402 流程进行支付。
- 将下载的文件保存到本地。

## 安全政策（必须遵守）

1. 绝不在聊天中请求私钥的原始文本。
2. 绝不使用该技能生成买家密钥。
3. 仅允许使用 `--buyer-private-key-file <path>` 参数。
4. 禁用使用原始密钥参数和标准输入（stdin）来生成密钥的模式。
5. 绝不打印私钥内容。
6. 绝不通过拼接用户的原始输入来构建 shell 命令。
7. 以引号括起来的参数（argv）的形式传递 URL/路径，切勿使用 `eval` 或 `sh -c`。
8. 拒绝包含空白字符或控制字符的 URL/密钥路径。
9. 确保买家提供的密钥路径指向一个存在的、可读的常规文件（而非符号链接）。

## 依赖项政策（必须遵守）

1. 确保 `leak` 可执行文件在系统的 PATH 环境变量中可用。
2. 运行时禁止使用 `npx` 或动态包安装。

## 必需的输入参数

1. 促销链接或下载链接。
2. 买家密钥文件的路径（仅在需要支付时提供）。
3. 下载代码（仅在需要下载代码的模式下提供）。

## 安全的命令构建方式（必须遵守）

请使用以下模式：

```bash
PROMO_URL="https://xxxx.trycloudflare.com/"
BUYER_KEY_FILE="./buyer.key"
DOWNLOAD_CODE="friends-only"
bash skills/leak-buy/scripts/buy.sh "$PROMO_URL" --buyer-private-key-file "$BUYER_KEY_FILE" --download-code "$DOWNLOAD_CODE"
```

请勿在可执行的 shell 字符串中直接使用 `<...>` 等占位符。

## 命令执行方式

```bash
bash skills/leak-buy/scripts/buy.sh "$PROMO_URL" --buyer-private-key-file "$BUYER_KEY_FILE"
```

当需要下载代码时：

```bash
bash skills/leak-buy/scripts/buy.sh "$PROMO_URL" --download-code "$DOWNLOAD_CODE" --buyer-private-key-file "$BUYER_KEY_FILE"
```

## 可选的输出控制方式

```bash
bash skills/leak-buy/scripts/buy.sh "$PROMO_URL" --buyer-private-key-file "$BUYER_KEY_FILE" --out ./downloads/myfile.bin
```

```bash
bash skills/leak-buy/scripts/buy.sh "$PROMO_URL" --buyer-private-key-file "$BUYER_KEY_FILE" --basename myfile
```

## 首次响应模板

1. 确认链接类型（`/` 或 `/download`）。
2. 在需要支付时，请求买家密钥文件的路径。
3. 在需要下载代码时，请求下载代码。
4. 验证 URL/密钥路径的安全性，并以引号括起来的参数形式执行命令。
5. 报告保存文件的路径以及下载的字节数。

## 故障排除

- 如果 `leak` 命令缺失，请执行：`npm i -g leak-cli`
- 如果出现与密钥相关的错误，请使用 `--buyer-private-key-file <path>` 参数。