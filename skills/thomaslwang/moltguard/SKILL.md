---
name: moltguard
version: 6.6.16
description: "**MoltGuard** — 由 OpenGuardrails 开发的 OpenClaw 代理运行时安全插件。该插件帮助用户安装、注册、激活并检查 MoltGuard 的状态。适用于以下场景：安装 MoltGuard、检查其运行状态、进行注册或激活操作、配置 AI 安全网关，以及了解 MoltGuard 所能检测到的安全威胁。MoltGuard 提供以本地防护为主的安全机制，有效防止数据泄露、凭证窃取、命令注入等安全问题。  
来源：https://github.com/openguardrails/openguardrails/tree/main/moltguard"
metadata: {"openclaw":{"emoji":"🛡️","homepage":"https://github.com/openguardrails/openguardrails/tree/main/moltguard","keywords":["security","prompt-injection","data-exfiltration","pii","credential-theft","command-injection","guardrails","safety","agent-security","moltguard"]}}
---
# MoltGuard

MoltGuard 是由 [OpenGuardrails](https://github.com/openguardrails/openguardrails) 开发的一款用于 OpenClaw 代理的运行时安全防护工具。该工具采用开源许可证（Apache 2.0），且所有代码均可被审计。

**ClawHub**: [`ThomasLWang/moltguard`](https://clawhub.ai/ThomasLWang/moltguard) · **npm**: [`@openguardrails/moltguard`](https://www.npmjs.com/package/@openguardrails/moltguard) · **GitHub**: [`openguardrails/openguardrails/tree/main/moltguard`](https://github.com/openguardrails/openguardrails/tree/main/moltguard)

---

## 安全性与代码来源验证

**在安装前请验证代码来源。** 确保您下载的 npm 包与 GitHub 上的源代码一致。验证方法如下：
```bash
# Download and inspect the package contents
npm pack @openguardrails/moltguard --dry-run

# Or do a full diff against the cloned repo:
mkdir /tmp/moltguard-audit && cd /tmp/moltguard-audit
npm pack @openguardrails/moltguard
tar -xzf openguardrails-moltguard-*.tgz
git clone https://github.com/openguardrails/openguardrails
diff -r package/scripts openguardrails/moltguard/scripts
```
如果您对发布者不太信任，建议直接从 GitHub 仓库安装：`openclaw plugins install -l ./openguardrails/moltguard`

**`activate.mjs` 的功能：** 该脚本会向 `https://www.openguardrails.com/core` 发送一个请求以完成代理的注册。用户访问指定的 URL 并验证邮箱后，系统会生成一个 API 密钥，并将其保存到 `~/.openclaw/credentials/moltguard/credentials.json` 文件中。如果您不信任该 API 端点，请勿激活 MoltGuard；即使不激活，本地防护功能依然可用。

**网络行为：**
- **未激活状态**：不会发送任何 outbound 请求，仅进行本地检测。
- **激活状态**：每个代理工具调用时都会向 `https://www.openguardrails.com/core` 发送行为评估请求，但不会传输消息内容，仅发送工具名称、调用顺序及元数据。

**密钥管理：** 请将激活过程中生成的 API 密钥视为敏感信息。如有需要，可通过账户门户（`https://www.openguardrails.com/core/login`）进行密钥轮换或撤销。如果您选择不使用云服务，本地防护功能可永久保持启用状态。

---

## 安装前的注意事项

在安装或运行 `activate.mjs` 之前，请务必：
1. **验证代码来源**：使用 `npm pack` 命令下载包，并通过 `diff` 命令与 GitHub 源代码进行比对，确保内容一致。
2. **自行检查脚本**：`scripts/activate.mjs` 和 `scripts/status.mjs` 文件内容简单易懂，安装前请仔细阅读。
3. **了解激活过程**：激活操作会将 API 密钥写入 `~/.openclaw/credentials/moltguard/credentials.json` 文件；如果日后对相关端点产生疑虑，请删除该文件并通过平台门户撤销密钥。
4. **在需要高安全性的环境中激活**：可以使用 `tcpdump`、`mitmproxy` 或 `Little Snitch` 等工具监控网络流量，确认所有 outbound 请求的目标地址以及传输的数据中仅包含经过清洗的元数据（不含实际消息内容）。

---

## 代理工作流程

### 检查状态
当用户询问 MoltGuard 的状态（是否已注册或当前使用的邮箱/计划信息）时，运行以下命令：
```bash
node {baseDir}/scripts/status.mjs
```

### 注册与激活
当用户希望注册 MoltGuard 或启用云行为检测功能时，运行以下命令：
```bash
node {baseDir}/scripts/activate.mjs
```
激活完成后，向用户提供注册 URL，要求他们访问该 URL 并输入邮箱以完成激活流程。成功激活后，系统会将 API 密钥写入 `~/.openclaw/credentials/moltguard/credentials.json` 文件。

---

## 安装步骤
当用户请求安装 MoltGuard 时，请按照以下步骤操作：
```bash
# 1. Install the plugin
openclaw plugins install @openguardrails/moltguard

# 2. Restart the gateway to load the plugin
openclaw gateway restart

# 3. Register and show activation link
node {baseDir}/scripts/activate.mjs
```

安装完成后，向用户展示注册 URL，并告知他们需要访问该 URL 并输入邮箱以完成激活。

本地防护功能在重启后立即生效（无需额外注册），而云行为检测功能需要先进行激活。

## 更新
更新 MoltGuard 后，请重新运行步骤 3 以确认插件已正确加载，并查看当前的激活状态。

---

## MoltGuard 的防护机制

**本地防护（无需云服务/无需注册）：**
- 读取敏感文件 → 发生网络请求 → 立即阻止该请求。
- 参数中包含 shell 逃逸代码（如 `$()`, `backtick`, `;`, `&&`, `|`） → 立即阻止该请求。
- 文件或网页内容中存在恶意脚本注入 → 直接删除相关内容。

**云服务防护（需激活）：**
- 多个账户同时访问同一资源 → 立即阻止。
- 工具使用顺序异常或行为不符合预期 → 发出警报。

完整的防护规则和模式详情请参阅 `references/details.md`。

---

## AI 安全网关（免费，无需注册）

MoltGuard 还提供了一个免费的本地 HTTP 代理服务，可在数据传输到大型语言模型（LLM）提供商之前对个人身份信息（PII）和敏感数据进行清洗：
```bash
npx @openguardrails/gateway   # runs on port 8900
```

将代理的 API 基址设置为 `http://127.0.0.1:8900`，该代理会清洗电子邮件、信用卡号码、API 密钥、电话号码、SSN、IBAN、IP 地址和 URL 内容，并在响应中恢复原始数据。该服务为无状态设计，不会保留任何用户数据。

---

## 配置选项
所有配置选项均位于 `~/.openclaw/openclaw.json` 文件的 `plugins.entries.openguardrails.config` 部分：
| 选项 | 默认值 | 说明 |
|--------|---------|-------------|
| `enabled` | `true` | 是否启用该插件 |
| `blockOnRisk` | `true` | 检测到风险时是否阻止相关请求 |
| `apiKey` | `""` | API 密钥（格式为 `sk-og-...`） |
| `agentName` | `"OpenClaw Agent"` | 代理在控制面板中的显示名称 |
| `coreUrl` | `https://www.openguardrails.com/core` | 平台 API 端点 |
| `dashboardUrl` | `https://www.openguardrails.com/dashboard` | 用于查看检测日志的仪表板地址 |
| `timeoutMs` | `60000` | 云服务评估的超时时间（以毫秒为单位） |

**直接使用现有 API 密钥的配置：**  
```json
{
  "plugins": {
    "entries": {
      "openguardrails": {
        "config": { "apiKey": "sk-og-<your-key>" }
      }
    }
  }
}
```

---

## 价格方案
| 价格方案 | 月费用 | 每月检测次数 |
|------|-------|---------------|
| 免费 | $0 | 30,000 次 |
| 起始套餐 | $19/mo | 100,000 次 |
| 专业套餐 | $49/mo | 300,000 次 |
| 商业套餐 | $199/mo | 2,000,000 次 |

账户管理门户：`https://www.openguardrails.com/core/login`（需要输入邮箱和 API 密钥）

---

## 卸载
卸载 MoltGuard 的步骤如下：
```bash
rm -rf ~/.openclaw/extensions/moltguard
# Remove moltguard configs from ~/.openclaw/openclaw.json
rm -rf ~/.openclaw/credentials/moltguard   # optional
```

---

## 更多信息
有关安全机制、检测规则、隐私政策及数据处理的详细信息，请参阅 `references/details.md`。