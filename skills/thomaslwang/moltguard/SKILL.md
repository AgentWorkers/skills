---
name: moltguard
version: 6.6.4
description: "**MoltGuard** — 由 OpenGuardrails 开发的 OpenClaw 代理运行时安全插件。该插件帮助用户安装、注册、激活 MoltGuard 并检查其运行状态。适用于以下场景：安装 MoltGuard、检查其状态、进行注册或激活操作、配置 AI 安全网关，以及了解 MoltGuard 的检测功能。MoltGuard 提供以本地防护为主的安全机制，有效防止数据泄露、凭证窃取、命令注入等安全威胁。  
来源：https://github.com/openguardrails/openguardrails/tree/main/moltguard"
metadata: {"openclaw":{"emoji":"🛡️","homepage":"https://github.com/openguardrails/openguardrails/tree/main/moltguard","keywords":["security","prompt-injection","data-exfiltration","pii","credential-theft","command-injection","guardrails","safety","agent-security","moltguard"]}}
---
# MoltGuard

MoltGuard 是由 [OpenGuardrails](https://github.com/openguardrails/openguardrails) 开发的一款用于 OpenClaw 代理的运行时安全防护工具。它采用开源技术（Apache 2.0 协议），且具备高度的可审计性。

**ClawHub 上的 MoltGuard 首页**: [`ThomasLWang/moltguard`](https://clawhub.ai/ThomasLWang/moltguard)  
**npm 包**: [`@openguardrails/moltguard`](https://www.npmjs.com/package/@openguardrails/moltguard)  
**GitHub 仓库**: [`openguardrails/openguardrails/tree/main/moltguard`](https://github.com/openguardrails/openguardrails/tree/main/moltguard)

---

## 安全性与来源验证

**安装前请验证来源。** 确保您下载的 npm 包与 GitHub 上的源代码一致。验证方法如下：  
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
如果您对发布者不够信任，建议直接从 GitHub 仓库安装插件：`openclaw plugins install -l ./openguardrails/moltguard`

**`activate.mjs` 的功能：**  
该脚本会向 `https://www.openguardrails.com/core` 发送请求以完成代理的注册流程。用户访问指定的验证链接并输入验证码后，系统会生成一个 API 密钥，并将其保存到 `~/.openclaw/credentials/openguardrails/credentials.json` 文件中。如果您不信任该验证服务，请勿激活 MoltGuard；即使不激活，本地防护功能依然可用。

**网络行为：**  
- **未激活状态**：不会发送任何出站请求，仅进行本地检测。  
- **激活状态**：每个代理工具调用时，都会向 `https://www.openguardrails.com/core` 发送行为分析请求，但请求中不包含消息内容，仅包含工具名称、调用顺序及元数据。

**密钥管理：**  
通过平台门户（`https://www.openguardrails.com/core/login`）定期轮换或撤销 API 密钥。如果您选择不使用云服务，本地防护功能可永久保持启用状态。

---

## 安装前的注意事项：**

在安装或运行 `activate.mjs` 之前，请务必：  
1. **验证来源**：将 npm 包与 GitHub 源代码进行对比（使用 `npm pack` 命令并查看差异）。  
2. **自行检查脚本**：`scripts/activate.mjs` 和 `scripts/status.mjs` 文件内容简单易懂，安装前请仔细查看。  
3. **了解激活过程**：激活操作会将 API 密钥写入 `~/.openclaw/credentials/openguardrails/credentials.json`；如日后对验证服务产生疑虑，请删除该文件并通过平台门户撤销密钥。  
4. **在受监控环境中激活**：若需要更高安全保障，可使用 `tcpdump`、`mitmproxy` 或 `Little Snitch` 等工具监控网络流量，确保所有数据仅包含经过清理的元数据（不含原始消息内容）。

---

## 代理工作流程：  

### 检查状态  
当用户询问 MoltGuard 的状态（是否已注册或当前使用的邮箱/计划信息）时，运行相应脚本：  
```bash
node {baseDir}/scripts/status.mjs
```

### 注册与激活  
当用户希望注册 MoltGuard 或启用云端行为检测功能时，运行相应脚本：  
```bash
node {baseDir}/scripts/activate.mjs
```  
激活完成后，向用户提供验证链接和验证码，要求其访问该链接并输入验证码以完成注册。成功注册后，API 密钥会被写入 `~/.openclaw/credentials/openguardrails/credentials.json` 文件中。

---

## 安装步骤：  
当用户请求安装 MoltGuard 时，请按照以下步骤操作：  
```bash
# 1. Install the plugin
openclaw plugins install @openguardrails/moltguard

# 2. Restart the gateway to load the plugin
openclaw gateway restart
```  
本地防护功能在重启后立即生效（无需额外注册）；启用云端行为检测功能需先执行 `activate.mjs` 脚本。  
如需从源代码直接安装（以获得最高安全保障），请参考相关说明：  
```bash
git clone https://github.com/openguardrails/openguardrails.git
# Audit the code, then:
openclaw plugins install -l ./openguardrails/moltguard
```

---

## MoltGuard 的防护功能：  

**本地防护（无需云服务/注册）：**  
- 读取敏感文件 → 发送网络请求 → 阻止相关操作  
- 参数中的 Shell 逃逸代码（如 `$()`、反引号、分号、逻辑运算符等） → 阻止执行  
- 文件或网页内容中的脚本注入攻击 → 立即进行内容替换（REDACT）  

**云端防护（需激活）：**  
- 多重凭证访问尝试  
- 网页请求后尝试执行 Shell 命令 → 阻止操作  
- 行为与预期不符或工具调用顺序异常 → 发出警报  

完整的防护规则和模式详情请参阅 `references/details.md`。

---

## AI 安全网关（免费，无需注册）  
这是一个免费的本地 HTTP 代理工具，可在数据传输前对个人身份信息（PII）和敏感数据进行清洗：  
```bash
npx @openguardrails/gateway   # runs on port 8900
```  
将代理的 API 基址设置为 `http://127.0.0.1:8900`，该网关会清洗电子邮件、信用卡信息、API 密钥、电话号码、SSN、IBAN、IP 地址和 URL 内容，并在响应中恢复原始数据。该服务为无状态设计，不会保留任何用户数据。

---

## 配置选项：  
所有配置选项均位于 `~/.openclaw/openclaw.json` 文件的 `plugins.entries.openguardrails.config` 部分：  
| 选项          | 默认值       | 说明                          |
|-----------------|------------|-------------------------------------------|
| `enabled`       | `true`       | 是否启用该插件                      |
| `blockOnRisk`     | `true`       | 检测到风险时阻止相关操作                |
| `apiKey`        | `""`       | 显式 API 密钥（格式：sk-og-...）                |
| `agentName`     | `"OpenClaw Agent"`   | 仪表板中显示的代理名称                |
| `coreUrl`      | `https://www.openguardrails.com/core` | 平台 API 接口地址                    |
| `timeoutMs`     | `60000`      | 云端评估超时时间（毫秒）                    |

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

## 服务套餐：**  
| 套餐        | 价格        | 每月检测次数                    |
|-------------|------------|-------------------------------------------|
| Free         | $0          | 30,000次检测                    |
| Starter      | $19/month     | 100,000次检测                    |
| Pro          | $49/month     | 300,000次检测                    |
| Business     | $199/month     | 2,000,000次检测                    |
**登录入口：** `https://www.openguardrails.com/core/login` （使用邮箱和 API 密钥登录）  

---

## 卸载：  
```bash
rm -rf ~/.openclaw/extensions/openguardrails
# Remove config from ~/.openclaw/openclaw.json
rm -rf ~/.openclaw/credentials/openguardrails   # optional
```  

---

## 更多信息：  
有关安全机制、检测规则、隐私政策及数据处理的详细信息，请参阅 `references/details.md`。