---
name: moltguard
version: 6.6.17
description: "**MoltGuard** — 由 OpenGuardrails 开发的 OpenClaw 代理运行时安全插件。该插件帮助用户安装、注册、激活以及检查 MoltGuard 的状态。适用于以下场景：安装 MoltGuard、查看其运行状态、进行注册或激活操作、配置 AI 安全网关，以及了解 MoltGuard 的检测机制。MoltGuard 提供以本地防护为主的安全机制，有效防范数据泄露、凭证窃取、命令注入等安全威胁。  
来源：https://github.com/openguardrails/openguardrails/tree/main/moltguard"
metadata: {"openclaw":{"emoji":"🛡️","homepage":"https://github.com/openguardrails/openguardrails/tree/main/moltguard","keywords":["security","prompt-injection","data-exfiltration","pii","credential-theft","command-injection","guardrails","safety","agent-security","moltguard"]}}
---
# MoltGuard

MoltGuard 是由 [OpenGuardrails](https://github.com/openguardrails/openguardrails) 开发的一款针对 OpenClaw 代理的运行时安全防护工具。该工具采用开源代码（Apache 2.0 协议），具备高度的可审计性。

**ClawHub**: [`ThomasLWang/moltguard`](https://clawhub.ai/ThomasLWang/moltguard) · **npm**: [`@openguardrails/moltguard`](https://www.npmjs.com/package/@openguardrails/moltguard) · **GitHub**: [`openguardrails/openguardrails/tree/main/moltguard`](https://github.com/openguardrails/openguardrails/tree/main/moltguard)

---

## 安全性与来源验证

**安装前请验证来源。** 确保所使用的 npm 包与 GitHub 上的源代码一致。验证方法如下：  
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
如果对发布者信任度较低，建议选择从源代码直接安装：`openclaw plugins install -l ./openguardrails/moltguard`

**`activate.mjs` 的功能：** 该脚本会向 `https://www.openguardrails.com/core` 发送请求以注册代理。用户访问指定 URL 并验证邮箱后，系统会生成一个 API 密钥，并将其保存到 `~/.openclaw/credentials/moltguard/credentials.json` 文件中。如果不信任该接口，请勿激活 MoltGuard；未激活状态下，所有本地防护功能依然可用。

**网络行为：**  
- **未激活状态**：不会发送任何出站请求，仅进行本地检测。  
- **激活状态**：每个代理工具调用时，都会向 `https://www.openguardrails.com/core` 发送行为评估请求，但不会传输消息内容，仅包含工具名称、调用顺序及元数据。

**密钥管理：**  
通过账户门户（`https://www.openguardrails.com/core/login`）定期轮换或撤销 API 密钥。如果选择不使用云服务，本地防护功能可永久保持有效。

---

## 安装前的注意事项

在安装或运行 `activate.mjs` 之前，请务必：  
1. **验证来源**：使用 `npm pack` 和 `diff` 命令比较 npm 包与 GitHub 源代码，确保内容一致。  
2. **自行检查脚本**：`scripts/activate.mjs` 和 `scripts/status.mjs` 文件内容简单易懂，安装前请仔细阅读。  
3. **了解激活过程**：激活操作会将 API 密钥写入 `~/.openclaw/credentials/moltguard/credentials.json`；如后续对接口产生疑虑，请删除该文件并通过平台门户撤销密钥。  
4. **在受监控环境中激活**：如需更高安全保障，可使用 `tcpdump`、`mitmproxy` 或 `Little Snitch` 确认出站请求的目的地，并确认请求数据仅包含经过清洗的元数据（不含实际消息内容）。

---

## 代理工作流程

### 检查状态  
当用户询问 MoltGuard 的状态（是否已注册或当前使用的邮箱/计划信息）时，运行相应命令：  
```bash
node {baseDir}/scripts/status.mjs
```

### 注册与激活  
当用户希望注册 MoltGuard 或启用云服务行为检测功能时，运行相应命令：  
```bash
node {baseDir}/scripts/activate.mjs
```  
激活完成后，向用户提供验证 URL，要求他们访问该 URL 并输入邮箱以完成激活。成功激活后，API 密钥会被保存到 `~/.openclaw/credentials/moltguard/credentials.json` 中。

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
安装完成后，向用户展示验证 URL，并告知他们访问该 URL 并输入邮箱以完成激活。重启后，本地防护功能立即生效（无需额外注册）；云服务行为检测功能需先激活。

## 更新  
更新 MoltGuard 后，请重新运行步骤 3 以确认插件已正确加载并显示当前激活状态。

---

## MoltGuard 的防护功能  

**本地防护（无需云服务或注册）：**  
- 读取敏感文件 → 阻止相关操作  
- 参数中的 shell 逃逸代码（如 `$()`, `;`, `&&`, `|` 等） → 阻止执行  
- 文件/网页内容中的脚本注入攻击 → 实时替换敏感信息  

**云服务防护（需激活）：**  
- 多重凭证访问尝试  
- 网页请求后的 shell 调用 → 阻止执行  
- 不正常的工具使用顺序 → 发出警报  

完整的检测规则和模式详情请参阅 `references/details.md`。

---

## AI 安全网关（免费，无需注册）  
这是一个免费的本地 HTTP 代理，可在数据传输前对个人身份信息（PII）和敏感数据进行清洗：  
```bash
npx @openguardrails/gateway   # runs on port 8900
```  
将代理的 API 基础地址设置为 `http://127.0.0.1:8900`，该网关会清洗电子邮件、信用卡信息、API 密钥、电话号码、SSN、IBAN、IP 地址和 URL 内容，并在响应中恢复原始数据。该服务为无状态设计，不会保留任何用户数据。

---

## 配置选项  
所有配置选项均位于 `~/.openclaw/openclaw.json` 文件的 `plugins.entries.openguardrails.config` 部分：  
| 选项          | 默认值     | 说明                          |
|----------------|-----------|------------------------------------|
| `enabled`       | `true`      | 是否启用该插件                      |
| `blockOnRisk`     | `true`      | 检测到风险时阻止相关操作                |
| `apiKey`        | `""`      | 显式的 API 密钥                      |
| `agentName`     | `"OpenClaw Agent"` | 仪表板中显示的代理名称                |
| `coreUrl`       | `https://www.openguardrails.com/core` | 平台 API 接口地址                    |
| `dashboardUrl`    | `https://www.openguardrails.com/dashboard` | 仪表板链接                        |
| `timeoutMs`     | `60000`     | 云服务评估超时时间（毫秒）                    |

**直接使用现有 API 密钥（无需注册）：**  
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
| 价格方案 | 月费用     | 每月检测次数                    |
|---------|-----------|-----------------------------|
| 免费     | $0         | 30,000次                         |
| 起始套餐 | $19/month   | 100,000次                         |
| 专业套餐 | $49/month   | 300,000次                         |
| 商业套餐 | $199/month   | 2,000,000次                         |
**账户登录地址：** `https://www.openguardrails.com/core/login` （需输入邮箱和 API 密钥）

---

## 卸载  
```bash
rm -rf ~/.openclaw/extensions/moltguard
# Remove moltguard configs from ~/.openclaw/openclaw.json
rm -rf ~/.openclaw/credentials/moltguard   # optional
```  

---

## 更多信息  
有关安全机制、检测规则、隐私政策及数据处理的详细信息，请参阅 `references/details.md`。