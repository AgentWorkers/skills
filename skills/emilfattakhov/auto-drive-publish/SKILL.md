---
name: auto-drive
description: 通过 Auto Drive 为 AI 代理提供持久化存储功能：可以存储和检索代理的运行记录，将文件上传到去中心化的永久存储系统中，并构建相互关联的记忆链。这一切都只需使用一个免费的 API 密钥即可（支持最大 20 MB 的存储空间）。每个记忆条目都会与前一个条目相互关联，形成一个不可篡改的链条，代理可以通过这个链条来重建自身的完整历史记录。该功能适用于保存代理的记忆数据、上传文件、从 CID（Content Identifier）中检索记忆链内容，或下载之前存储的数据。
  Persistent memory for AI agents via Auto Drive. Store and recall agent experiences,
  upload files to permanent decentralized storage, and build linked memory chains —
  all with a free API key (up to 20 MB). Each memory entry links to the previous one,
  forming an immutable chain your agent can walk to reconstruct its full history.
  Use when saving agent memories, uploading files, recalling memory chains from a CID,
  or downloading previously stored content.
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["curl", "jq", "bash"]
      env: ["AUTO_DRIVE_API_KEY"]
---
# Auto Drive — 持久化代理内存

Auto Drive 为你的代理提供持久化的内存存储，这种存储方式能够在重启、迁移甚至平台更换后仍然保持数据的完整性。它将数据存储在 [Autonomys Network](https://autonomys.xyz) 的分布式存储层中，通过一个简单的内容寻址系统实现数据的永久访问。

每次上传操作都会返回一个 **CID**（内容标识符），这是一个唯一且永久性的数据地址。相同的数据总是会生成相同的 CID。一旦数据被存储，就可以通过公共网关随时访问。

## 为什么使用 Auto Drive

- **免费入门**：你可以在 [ai3.storage](https://ai3.storage) 获取 API 密钥（使用 Google、GitHub 或 Discord 登录）。免费 tier 允许上传最多 20 MB 的数据。
- **永久存储**：数据会被永久保存，没有过期时间，也没有重复收费。
- **内存链**：每个内存条目都会与前一个条目链接起来，形成一个有序的链。你可以从最新的 CID 开始回溯，以获取代理的全部历史记录。
- **公共访问**：任何人都可以通过公共网关下载数据（无需 API 密钥），只有上传操作需要身份验证。
- **结构化数据支持**：你可以存储纯文本、JSON 或任意类型的文件。包含数组、数字、布尔值和空值的嵌套 JSON 数据也能被完美地存储和读取。

## 设置

1. 访问 [ai3.storage](https://ai3.storage)，并使用 Google、GitHub 或 Discord 登录。
2. 转到 **Developers → Create API Key**（开发者 → 创建 API 密钥）。
3. 将 `AUTO_DRIVE_API_KEY` 设置到你的环境变量中。

## 操作

### 上传文件
```bash
scripts/autodrive-upload.sh <file_path> [--json] [--compress]
# Prints CID to stdout, status to stderr
# Gateway URL: https://gateway.autonomys.xyz/file/<CID>
```

### 通过 CID 下载文件
```bash
scripts/autodrive-download.sh <cid> [output_path]
# Streams to stdout, or saves to file
# Falls back to public gateway if API returns an error
```

### 保存内存条目（链式存储）
```bash
scripts/autodrive-save-memory.sh "<text or /path/to/file.json>" [--agent-name NAME] [--state-file PATH]
# Output: {"cid":"...","previousCid":"...","chainLength":N}
```

### 检索完整的内存链
```bash
scripts/autodrive-recall-chain.sh [cid] [--limit N] [--output-dir DIR]
# Walks chain backward from latest CID, prints each entry as JSON
# Falls back to ~/.openclaw/workspace/memory/autodrive-state.json if no CID given
```

## 内存链结构

每个内存条目都会包含代理数据，并附有一个指向前一个 CID 的头部信息：
```json
{
  "header": {
    "agentName": "my-agent",
    "agentVersion": "1.0.0",
    "timestamp": "2026-02-18T...",
    "previousCid": "bafy..."
  },
  "data": { ... }
}
```

`data` 字段可以存储任何有效的 JSON 数据——包括纯字符串、结构化对象、数组以及深度嵌套的数据结构。

链的状态记录在 `~/.openclaw/workspace/memory/autodrive-state.json` 文件中。最新的 CID 也会被保存在 `MEMORY.md` 文件中（如果该文件存在的话）。

## 下载与公共访问

任何 CID 都可以无需身份验证地被公开访问：
```
https://gateway.autonomys.xyz/file/<CID>
```

对于使用 `--compress` 选项上传的文件，网关会自动处理解压缩操作。

## 限制

- **免费 tier**：允许上传最多 20 MB 的数据（具体限制因套餐而异，请通过 API 查询）。
- **下载**：通过公共网关可以无限次下载数据。
- **所有数据都是永久且公开可访问的**：请勿存储密码、敏感信息或其他机密数据。

## 查看剩余信用额度

```bash
curl -H "Authorization: Bearer $AUTO_DRIVE_API_KEY" \
     -H "X-Auth-Provider: apikey" \
     "https://mainnet.auto-drive.autonomys.xyz/api/accounts/@me"
```

该命令会返回 `pendingUploadCredits` 和 `pendingDownloadCredits`（单位：字节）。

## 平台要求

- 脚本需要以下工具：**bash**、**curl** 和 **jq**（适用于 Linux/macOS 或安装了 WSL/Git Bash 的 Windows）。
- 在没有 bash 的 Windows 环境中，代理也可以直接调用 Auto Drive API，遵循相同的上传流程（创建 → 分块上传 → 完成上传）。详细 API 文档请参见 `references/autodrive-api.md`。

## 链接

- **控制面板与 API 密钥**：[ai3.storage](https://ai3.storage)
- **公共网关**：[gateway.autonomys.xyz](https://gateway.autonomys.xyz)
- **开发者文档**：[develop.autonomys.xyz](https://develop.autonomys.xyz)
- **API 参考**：[references/autodrive-api.md]