---
name: openclaw-occ
title: OCC for OpenClaw
description: "OCC（Origin Controlled Computing）——为每个 OpenClaw 代理的操作提供加密证明。支持安装、配置和审计功能。"
version: 1.0.7
homepage: https://occ.fyi/openclaw
source: https://github.com/mikeargento/occ-core
requires:
  - npm
  - npx
  - curl
metadata:
  openclaw:
    homepage: https://occ.fyi/openclaw
    emoji: "🔐"
---
## 该技能的功能

`openclaw-occ` 是一个 OpenClaw 插件，它在代理程序运行的每个工具之后（如 bash 命令、文件读取、浏览器导航、API 调用等）都会提交相应的加密 OCC（Origin Controlled Computing，原产地控制计算）证明。这些证明以只读模式（append-only）存储在 `~/.openclaw/workspace/occ-proofs/` 目录下的 JSONL 文件中。

如果恶意脚本或提示注入导致了未经授权的操作，这些操作要么会出现在证明日志中但缺少有效的签名，要么根本不会被记录——从而在审计追踪中暴露出来。

使用此技能可以帮助用户安装该插件、配置相关设置，并了解他们的审计结果。

---

## 隐私与数据安全

**公证方接收的信息：** 每条证明包含工具名称（例如 `bash`、`read`）、时间戳、与前一条证明链接的 SHA-256 哈希值以及一个单调计数器。该证明不包含工具的输入或输出内容——既没有文件内容，也没有 bash 命令或 API 响应。

**零网络模式（Zero-network option）：** 在 `~/.openclaw/workspace/occ.json` 中设置 `"mode": "stub"`。所有证明仅以 SHA-256 哈希值的形式存储在本地，不会发送任何网络请求。

**自托管（Self-hosting）：** 用户可以运行自己的 Cloudflare Worker 公证服务（详见“自托管”部分），从而确保证明数据不会离开用户的基础设施。

---

## 安装插件

请用户执行以下命令：

```bash
npm install -g openclaw-occ
openclaw-occ install
```

之后重启 OpenClaw。下次启动时，插件将会自动被识别（OpenClaw 会扫描 `package.json` 文件中的 `openclawextensions` 项）。

---

## 配置插件

创建 `~/.openclaw/workspace/occ.json` 文件。该文件支持三种模式：

| 模式 | 功能说明 |
|------|-------------|
| `stub` | 仅生成本地 SHA-256 哈希值，不进行网络请求。适用于离线环境或注重隐私的场景。 |
| `remote` | 将证明数据发送到一个公证方，并返回带有 Ed25519 签名的证明文件及单调计数器。**默认模式。** |
| `tee` | 同时将证明数据发送到多个公证方。适用于合规性要求或数据冗余的场景。 |

**默认配置**（使用托管的 OCC 公证服务，无需额外设置）：
```json
{
  "mode": "remote",
  "notaries": ["https://occ-notary.gjp9tm85hq.workers.dev/commit"]
}
```

**Tee 模式**（使用用户自己的公证服务作为备用方案）：
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

**在聊天工具中：**（可以在任何已连接的聊天应用中输入命令）
- `occ audit` — 显示当天的审计总结：操作次数、证明状态、最后一次执行的工具名称
- `occ verify bash` — 重新验证最近 5 次 bash 操作的证明文件

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

**在控制界面中：** OCC 面板会显示每项操作的详细信息，包括时间戳、工具名称、证明哈希值、模式标识以及一键验证功能。

---

## 解释证明状态

- 🔏 **已签名（Signed）** — 证明数据已成功提交给公证方，并附带 Ed25519 签名及单调计数器
- ⚪ **仅生成本地 SHA-256 哈希值（Stub mode）** — 当前模式设置为 `stub`，或者公证方无法访问
- ⚠ **失败（Failed）** — 公证方无法访问；系统会生成备用证明，因此操作记录仍然可见

**计数器变化的重要性：** 如果计数器从 41 突然跳到 43，说明可能存在被隐藏或被注入的操作。

---

## 自托管公证服务

如果用户希望完全控制审计流程并进行离线验证，可以自行部署 Cloudflare Worker 公证服务。

**前提条件：** 需要拥有启用了 Workers 和 KV 功能的 Cloudflare 账户，并且已经通过 `npx wrangler login` 命令完成认证。

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

每天生成一个 JSONL 文件，采用只读存储方式。该文件具有高容错性，便于使用 `grep` 命令查询、归档或导入其他工具进行处理。

---

## 更多信息：

- 插件安装：`npm install openclaw-occ`
- 文档链接：https://occ.fyi/openclaw
- 源代码链接：https://github.com/mikeargento/occ-core