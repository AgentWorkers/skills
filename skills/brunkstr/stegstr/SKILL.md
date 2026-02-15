---
name: stegstr
summary: Embed and decode hidden messages in PNG images. Steganographic Nostr client for hiding data in images—works offline, no registration.
description: 将 Stegstr 载荷解码并嵌入到 PNG 图像中。当用户需要从 Stegstr 图像中提取隐藏的 Nostr 数据、将载荷编码到封面 PNG 图像中，或处理基于隐写技术的社交网络（Nostr-in-images）时，可以使用该功能。支持通过 CLI（stegstr-cli decode、detect、embed、post）命令进行脚本操作和 AI 代理的集成。
license: MIT
tags: steganography, nostr, images, crypto, integration, file-management, automation, cli
install:
  requirements: |
    - Rust (latest stable) - https://rustup.rs
    - Git
  steps: |
    1. git clone https://github.com/brunkstr/Stegstr.git
    2. cd Stegstr/src-tauri && cargo build --release --bin stegstr-cli
    3. Binary: target/release/stegstr-cli (Windows: stegstr-cli.exe)
permissions:
  - filesystem
metadata:
  homepage: https://stegstr.com
  for-agents: https://www.stegstr.com/wiki/for-agents.html
  repo: https://github.com/brunkstr/Stegstr
---

# Stegstr

Stegstr 使用隐写技术将 Nostr 消息和任意有效载荷隐藏在 PNG 图像中。用户可以将他们的内容（帖子、私信、JSON 数据）嵌入到图像中并分享；接收者可以使用 Detect 工具来加载这些隐藏的内容。该工具无需注册，支持离线使用。

## 适用场景

- 用户希望从包含 Stegstr 数据的 PNG 图像中解码（提取）隐藏的数据。
- 用户希望将有效载荷嵌入到封面 PNG 图像中（例如：Nostr 数据包、JSON 数据、文本等）。
- 用户提到隐写技术、图像中的隐藏信息或照片中的秘密消息。
- 用户需要通过编程方式访问该工具，以实现自动化、脚本运行或与 AI 代理的集成。

## 命令行界面（CLI）

可以从 Stegstr 仓库构建命令行界面：

```bash
git clone https://github.com/brunkstr/Stegstr.git
cd Stegstr/src-tauri
cargo build --release --bin stegstr-cli
```

二进制文件：`target/release/stegstr-cli`（Windows 系统下为 `stegstr-cli.exe`）。

### 解码（提取有效载荷）

```bash
stegstr-cli decode image.png
```

将解码后的有效载荷输出到标准输出（stdout）。有效的 UTF-8 JSON 数据将以文本形式显示；否则将以 `base64:<data>` 的格式显示。成功时返回 0。

### 检测（解码并解密数据包）

```bash
stegstr-cli detect image.png
```

解码并解密数据包，然后输出 Nostr 数据包的 JSON 内容：`{"version": 1, "events": [...]}`。

### 嵌入（将有效载荷隐藏在图像中）

```bash
stegstr-cli embed cover.png -o out.png --payload "text or JSON"
stegstr-cli embed cover.png -o out.png --payload @bundle.json
stegstr-cli embed cover.png -o out.png --payload @bundle.json --encrypt
```

使用 `--payload @file` 从文件中加载有效载荷。使用 `--encrypt` 选项可确保任何使用 Stegstr 的用户都能检测到该有效载荷；对于二进制有效载荷，可使用 `--payload-base64 <base64>`。

### 发布（创建 Nostr 数据包）

```bash
stegstr-cli post "Your message here" --output bundle.json
stegstr-cli post "Message" --privkey-hex <64-char-hex> --output bundle.json
```

创建一个 Nostr 数据包，并使用 `stegstr-cli embed` 命令将其隐藏在图像中。

## 示例工作流程

```bash
# Create a post bundle
stegstr-cli post "Hello from OpenClaw" --output bundle.json

# Embed into a cover image (encrypted for any Stegstr user)
stegstr-cli embed cover.png -o stego.png --payload @bundle.json --encrypt

# Recipient detects and extracts
stegstr-cli detect stego.png
```

## 图像格式

仅支持无损的 PNG 格式。JPEG 或其他有损格式会导致隐藏数据损坏。

## 有效载荷格式

- **标识符：** `STEGSTR`（7 字节的 ASCII 字符）
- **长度：** 4 字节（大端字节序）
- **有效载荷：** UTF-8 格式的 JSON 数据或原始字节（桌面应用程序会对其进行加密；命令行界面支持原始数据或使用 `--encrypt` 选项进行加密）

解密后的数据包结构：`{"version": 1, "events": [ ... Nostr 事件 ... ]}`。详细规范请参考：[bundle.schema.json](https://raw.githubusercontent.com/brunkstr/Stegstr/main/schema/bundle.schema.json)。

## 链接

- **代理程序文档：** https://www.stegstr.com/agents.txt
- **代理程序使用指南：** https://www.stegstr.com/wiki/for-agents.html
- **命令行界面文档：** https://www.stegstr.com/wiki/cli.html
- **下载地址：** https://github.com/brunkstr/Stegstr/releases/latest