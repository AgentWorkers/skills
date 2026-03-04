---
name: fadnote
version: 1.0.2
description: 创建安全、可共享且会自动销毁的笔记
license: MIT
metadata:
  openclaw:
    emoji: 🔥
    requires:
      bins: ["node"]
      env: ["FADNOTE_URL"]
    primaryEnv: "FADNOTE_URL"
    homepage: https://github.com/easyFloyd/fadnote
---
# FadNote 技能

**适用于 OpenClaw 的安全、可自毁的共享笔记功能**

您可以直接从 OpenClaw 创建加密的、仅可一次性阅读的笔记。服务器永远不会看到您的明文内容。

---

## 概述

| 属性 | 值 |
|----------|-------|
| **名称** | fadnote |
| **版本** | 1.0.2 |
| **作者** | easyFloyd |
| **许可证** | MIT |
| **开源** | 是 — https://github.com/easyFloyd/fadnote |
| **运行环境** | Node.js 18+ |

---

## 安装

```bash
# Via ClawHub
claw install fadnote

# Manual
git clone https://github.com/easyFloyd/fadnote.git
ln -s $(pwd)/fadnote/openclaw-skill/scripts/fadnote.js ~/.claw/bin/fadnote
```

---

## 配置

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `FADNOTE_URL` | `https://fadnote.com` | FadNote 服务器的端点地址 |

---

## 使用方法

### 通过 OpenClaw 使用

```
user: Secure this API key: sk-abc123xyz

claw: I'll create a secure, self-destructing note for that.
      [runs: echo "sk-abc123xyz" | fadnote]

      🔗 https://fadnote.com/n/abc123# decryption-key-here

      Share it with the recipient via any channel and this link will self-destruct after first view.
```

### 通过命令行 (CLI) 使用

```bash
  Usage: fadnote [options] [text]
         echo "text" | fadnote [options]

  Create secure self-destructing notes that can only be viewed once.

  Options:
    -h, --help          Show this help message and exit
        --ttl <secs>    Time until note expires (default: 86400 = 24h)
        --json          Output JSON with noteId, expiresIn, and decryptionUrl

  Environment:
    FADNOTE_URL         API endpoint (default: https://fadnote.com)

  Examples:
    # Standard
    fadnote "My secret message" # direct input
    echo "My secret" | fadnote # from stdin

    # With options
    fadnote --ttl 3600 "Expires in 1 hour" # Custom TTL
    fadnote --json --ttl 7200 "JSON output" # JSON output:
      # {noteId: string, expiresIn: number, decryptionUrl: string}

    # File and clipboard input
    cat file.txt | fadnote --ttl 86400 # from stdin with options
    pbpaste | fadnote  # macOS clipboard
    xclip -o -selection clipboard | fadnote # from clipboard (Linux with xclip)
    xsel -b | fadnote # from clipboard (Linux with xsel)

```

**单行输出：** 生成包含共享链接的字符串。
**JSON 输出：** 
```json
{
  noteId: string,
  expiresIn: number,
  decryptionUrl: string
}
```

---

## 触发条件

当您说出以下任何指令时，I (OpenClaw) 会自动使用 FadNote 技能：
- “保护此内容”
- “使用 FadNote 处理此内容”
- “为此内容创建安全链接”
- “安全分享此内容”
- “创建一次性使用的笔记”
- “加密并分享此内容”

**如果启用了电子邮件发送功能：**
- “保护此内容并通过电子邮件发送给 [收件人]：[内容]”
- “使用 FadNote 将此内容发送到 [电子邮件地址]”
- “将安全笔记发送到 [电子邮件地址]”

**示例：**
```
- Secure this API key: sk-live-12345

- FadNote this password for the server

- Create a secure link for these credentials

- Share this securely: my private SSH key

- One-time note: the meeting location
```

---

## 安全性

- **客户端加密**：使用 AES-256-GCM 加密算法和 PBKDF2（600,000 次迭代）
- **零知识原则**：服务器仅接收加密后的数据块
- **一次性阅读**：笔记在首次被读取后立即删除
- **自动过期**：默认过期时间为 24 小时
- **开源**：服务器代码可在 https://github.com/easyFloyd/fadnote 上公开审核

解密密钥嵌入在 URL 中（`#key` 部分），且永远不会发送到服务器。

---

## 相关文件

```
openclaw-skill/
├── SKILL.md           # This file
└── scripts/
    └── fadnote.js     # Main CLI script (~160 lines)
```

---

## 系统要求

- Node.js 18+（无需外部依赖）

---

## 常见问题及解决方法

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `FADNOTE_URL 未设置` | 环境变量缺失 | 设置 `export FADNOTE_URL=https://fadnote.com` |
| 笔记为空** | 未提供输入内容 | 使用 `echo "secret" \| fadnote` 命令输入内容 |
| **404 Not Found** | 服务器端点地址错误 | 确保 `FADNOTE_URL` 指向正在运行的 FadNote 服务 |
| **连接失败** | 服务器无法访问 | 确认服务器是否正常运行或使用实时服务 |
| **加密功能不可用** | Node.js 版本低于 18 | 升级至 Node.js 18+ |

---

## 链接

- **实时服务地址：** https://fadnote.com
- **源代码：** https://github.com/easyFloyd/fadnote
- **问题反馈：** https://github.com/easyFloyd/fadnote/issues