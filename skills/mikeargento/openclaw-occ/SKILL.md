---
name: openclaw-occ
title: OCC for OpenClaw
description: "OCC（Origin Controlled Computing）——为每个 OpenClaw 代理的操作提供加密证明。支持安装、配置和审计功能。"
version: 1.1.1
homepage: https://occprotocol.com/openclaw
source: https://github.com/mikeargento/occ-core/tree/main/packages/occ-core/examples/openclaw-occ
requires:
  - npm
  - npx
  - curl
  - wrangler
metadata:
  openclaw:
    homepage: https://occprotocol.com/openclaw
    emoji: "🔐"
    npm: https://www.npmjs.com/package/openclaw-occ
---
## 该技能的功能

`openclaw-occ` 是一个 OpenClaw 插件，它在代理程序运行的每个工具之后（如 bash 命令、文件读取、浏览器导航、API 调用等）都会提交一个加密的 OCC（Origin Controlled Computing，即 origin-controlled computing）证明。这些证明以只读模式存储在 `~/.openclaw/workspace/occ-proofs/` 目录下的 JSONL 文件中。

如果恶意脚本或提示注入导致了未经授权的操作，这些操作要么会出现在证明日志中但缺少有效的签名，要么完全不会被记录在日志中——从而使得攻击行为在审计追踪中一目了然。

**为什么 OCC 证明与普通日志不同？**：普通日志是由被监控的系统生成的，可以被删除而不会留下任何痕迹。而 OCC 证明是由 OpenClaw 运行时自动提交给外部公证机构的；模型的指令无法隐藏这些证明。证明文件通过一个单调计数器进行链接，因此计数器的跳变（例如从 41 跳到 43）本身就可能是被隐藏操作的证据。证明文件的签名使用 Ed25519 算法生成，并且可以在离线环境下进行验证——因此无需信任公证机构即可审计操作记录。

使用此技能可以帮助用户安装该插件、配置它，并理解相应的审计结果。

---

## 隐私与数据安全

**公证机构接收的信息：** 每个证明文件包含工具名称（例如 `bash`、`read`）、时间戳、与前一个证明文件链接的 SHA-256 哈希值以及一个单调计数器。该文件**不**包含工具的输入内容或输出结果（即不包含文件内容、bash 命令或 API 响应）。来源：[`lib/notary.js`](https://github.com/mikeargento/occ-core/blob/main/packages/occ-core/examples/openclaw-occ/lib/notary.js)

**零网络模式（Zero-network option）：** 在 `~/.openclaw/workspace/occ.json` 中设置 `"mode": "stub"`。所有证明文件仅以 SHA-256 哈希值的形式存储，不会发送任何外部请求。

**自托管（Self-hosting）：** 用户可以运行自己的 Cloudflare Worker 公证机构（详见“自托管”部分），这样证明数据就不会离开用户的基础设施。

---

## 安装插件

请用户执行以下命令：
```bash
npm install -g openclaw-occ
openclaw-occ install
```

然后重启 OpenClaw。下次启动时，插件会自动被识别（OpenClaw 会在 `package.json` 中查找 `openclawextensions` 文件夹）。

---

## 配置插件

创建 `~/.openclaw/workspace/occ.json` 文件。该文件包含三种配置模式：

| 模式 | 功能 |
|------|-------------|
| `stub` | 仅生成本地 SHA-256 哈希值，不进行网络请求。适用于离线环境或重视隐私的场景。 |
| `remote` | 将证明文件发送到指定的公证机构，并返回带有 Ed25519 签名的证明文件以及单调计数器。**默认模式。** |
| `tee` | 同时将证明文件发送到多个公证机构。适用于合规性要求或数据冗余的场景。 |

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
- `occ audit` — 显示当天的操作统计信息、证明状态以及最后一次执行的工具名称。
- `occ verify bash` — 重新验证最近 5 次 bash 命令的执行情况。

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

**在控制界面中：** OCC 面板会显示每个操作的相关信息，包括时间戳、工具名称、证明文件的哈希值、模式标识以及一键验证功能。

---

## 解释证明状态

- 🔏 **已签名（Signed）**：证明文件已成功提交给公证机构，并附带 Ed25519 签名和单调计数器。
- ⚪ **仅生成本地 SHA-256 哈希值（Stub）**：当前配置为 `stub` 模式，或者公证机构无法访问。
- ⚠ **失败（Failed）**：公证机构无法访问；系统会生成备用证明文件，因此操作记录中的间隙仍然可见。

**计数器的跳变非常重要。** 如果计数器从 41 跳到 43，说明证明文件 42 可能被隐藏或被篡改。

---

## 自托管公证机构

如果用户希望完全控制审计流程并实现离线验证，可以自行部署 Cloudflare Worker 公证机构。

**前提条件：** 需要拥有启用了 Workers 和 KV 功能的 Cloudflare 账户，并且已经通过 `npx wrangler login` 命令完成了 Wrangler 的身份验证。

```bash
cd ~/.openclaw/extensions/openclaw-occ/notary-worker
npx wrangler kv:namespace create OCC_PROOFS
# Copy the output ID into wrangler.toml under [[kv_namespaces]]
npx wrangler deploy
```

部署完成后，保存公钥以供离线验证使用：
```bash
curl https://your-worker.workers.dev/key
# → { "publicKeyB64": "...", "version": "occ/1" }
```

然后更新 `~/.openclaw/workspace/occ.json` 文件：
```json
{
  "mode": "remote",
  "notaries": ["https://your-worker.workers.dev/commit"]
}
```

---

## 证明文件的存储位置

证明文件以 JSONL 格式存储，每天生成一个文件。文件采用只读模式，具有高容错性（即使系统崩溃也不会丢失数据），便于使用 `grep` 命令查询、归档或导入其他工具进行处理。

---

## 更多信息：

- 插件安装：`npm install openclaw-occ`
- 文档链接：https://occprotocol.com/openclaw
- 源代码链接：https://github.com/mikeargento/occ-core