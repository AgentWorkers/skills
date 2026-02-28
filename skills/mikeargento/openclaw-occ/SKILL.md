---
name: openclaw-occ
title: OCC for OpenClaw
description: "OCC（Origin Controlled Computing）——为每个 OpenClaw 代理的操作提供加密证明。支持安装、配置和审计功能。"
version: 1.1.0
homepage: https://occprotocol.com/openclaw
source: https://github.com/mikeargento/occ-core
requires:
  - npm
  - npx
  - curl
  - wrangler
metadata:
  openclaw:
    homepage: https://occprotocol.com/openclaw
    emoji: "🔐"
---
## 该技能的功能

`openclaw-occ` 是一个 OpenClaw 插件，它在代理程序运行的每个工具之后（如 bash 命令、文件读取、浏览器导航、API 调用等）都会提交一个加密的 OCC（Origin Controlled Computing，即源控计算）证明。这些证明以只读方式存储在 `~/.openclaw/workspace/occ-proofs/` 目录下的 JSONL 文件中。

如果恶意行为或提示注入导致了未经授权的操作，这些操作要么会出现在没有有效签名的证明日志中，要么完全不会被记录——从而在审计追踪中显现出来。

**为什么 OCC 证明与普通日志不同？**：普通日志是由被监控的系统生成的，可以被删除而不会留下任何痕迹。而 OCC 证明是由 OpenClaw 运行时自动提交给外部公证机构的；模型的指令无法掩盖这些证明。证明之间通过一个单调计数器进行链接，因此计数器的跳变（例如从 41 跳到 43）本身就是被掩盖操作的证据。证明的签名使用 Ed25519 算法生成，并且可以在离线环境下进行验证——因此无需信任公证机构即可审计操作记录。

使用此技能可以帮助用户安装该插件、配置它，并理解审计结果。

---

## 隐私与数据安全

**公证机构接收的信息：** 每条证明包含工具名称（例如 `bash`、`read`）、时间戳、与前一条证明链接的 SHA-256 哈希值以及一个单调计数器。但这些证明**不**包含工具的输入内容或输出结果——既没有文件内容，也没有 bash 命令或 API 响应。

**零网络模式（Zero-network mode）：** 在 `~/.openclaw/workspace/occ.json` 中设置 `"mode": "stub"`。所有证明仅以 SHA-256 哈希值的形式存储在本地，不会发送任何外部请求。

**自托管（Self-hosting）：** 可以运行自己的 Cloudflare Worker 公证机构（详见自托管部分），这样证明数据就不会离开用户的基础设施。

---

## 安装插件

请用户执行以下命令：

```bash
npm install -g openclaw-occ
openclaw-occ install
```

然后重启 OpenClaw。下次启动时，插件会自动被识别（它会扫描 `package.json` 文件中的 `openclawextensions` 配置项）。

---

## 配置插件

创建 `~/.openclaw/workspace/occ.json` 文件。该文件包含三种配置模式：

| 模式 | 功能 |
|------|-------------|
| `stub` | 仅存储本地的 SHA-256 哈希值，不进行网络请求。适合离线使用或注重隐私的场景。 |
| `remote` | 将证明数据发送到外部公证机构，并返回带有 Ed25519 签名的证明文件及单调计数器。**默认模式。** |
| `tee` | 同时将证明数据发送到多个公证机构。适用于合规性要求或数据冗余的场景。 |

**默认配置**（使用托管的 OCC 公证机构，无需额外设置）：
```json
{
  "mode": "remote",
  "notaries": ["https://occ-notary.gjp9tm85hq.workers.dev/commit"]
}
```

**多公证机构模式（Tee mode）**（使用用户自托管的公证机构作为备用方案）：
```json
{
  "mode": "tee",
  "notaries": [
    "https://my-own-notary.example.com/commit",
    "https://occ-notary.gjp9tm85hq.workers.dev/commit"
  ]
}
```

---

## 查看审计记录

**在聊天工具中：**（在任何已连接的聊天工具中输入以下命令）：
- `occ audit` — 查看今日的审计摘要：操作次数、证明状态、最后一次运行的工具信息
- `occ verify bash` — 重新验证最近 5 次 bash 命令的证明记录

**在终端中：**
```bash
npx occ-verify                       # recent proofs (last 7 days)
npx occ-verify --verbose             # full detail per proof
npx occ-verify --check               # re-verify all proofs against notary
npx occ-verify --tool bash           # filter by tool name
npx occ-verify --date 2026-02-27     # filter to a specific date
npx occ-verify --session <id>        # filter by session
npx occ-verify --json                # raw JSON output (for piping / scripting)
```

**在控制界面中：** OCC 面板会显示每个操作的相关信息，包括时间戳、工具名称、证明哈希值、模式标识以及一键验证功能。

---

## 解释证明状态

- 🔏 **已签名（Signed）**：证明已成功提交给公证机构；包含 Ed25519 签名和单调计数器
- ⚪ **仅本地存储（Stub）**：配置模式为 `stub`，或无法联系到公证机构
- ⚠ **失败（Failed）**：无法联系到公证机构；系统会存储备用证明，因此操作记录仍然可见

**计数器的跳变非常重要。** 如果计数器从 41 跳到 43，说明证明 42 可能被遗漏了——这可能是操作被掩盖或被注入的证据。

---

## 自托管公证机构

如果用户希望完全控制审计流程并实现离线验证，可以自行部署 Cloudflare Worker 公证机构。

**前提条件：** 需要拥有启用了 Workers 和 KV 功能的 Cloudflare 账户，并且已通过 `npx wrangler login` 命令完成 Wrangler 的身份验证。

```bash
cd ~/.openclaw/extensions/openclaw-occ/notary-worker
npx wrangler kv:namespace create OCC_PROOFS
# Copy the output ID into wrangler.toml under [[kv_namespaces]]
npx wrangler deploy
```

部署完成后，保存公钥以用于离线验证：
```bash
curl https://your-worker.workers.dev/key
# → { "publicKeyB64": "...", "version": "occ/1" }
```

随后更新 `~/.openclaw/workspace/occ.json` 文件：
```json
{
  "mode": "remote",
  "notaries": ["https://your-worker.workers.dev/commit"]
}
```

---

## 证明文件的存储位置

每天生成一个 JSONL 文件。文件采用只读模式存储，具有高可靠性（即使系统崩溃也不会丢失数据），便于使用 `grep` 命令查询、归档或导入其他工具进行处理。

---

## 更多信息：

- 插件安装：`npm install openclaw-occ`
- 文档：https://occprotocol.com/openclaw
- 源代码：https://github.com/mikeargento/occ-core