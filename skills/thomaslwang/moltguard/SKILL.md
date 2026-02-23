---
name: openguardrails
description: "**AI代理的运行时安全插件**  
该插件提供以本地防护为主的安全机制，有效防止数据泄露、凭证窃取、命令注入以及敏感信息的泄露。插件还包含一个免费的AI安全网关（AI Security Gateway），能够在数据传输到大型语言模型（LLM）提供商之前对其进行清洗和处理，确保其中不包含任何个人身份信息（PII）。该插件完全开源（遵循Apache 2.0许可证），所有的检测和清洗逻辑均可在GitHub上查看和审计。  
来源：github.com/openguardrails/openguardrails"
metadata: {"openclaw":{"emoji":"🛡️","homepage":"https://github.com/openguardrails/openguardrails","keywords":["security","prompt-injection","data-exfiltration","pii","credential-theft","command-injection","guardrails","safety","agent-security"]}}
---
# OpenGuardrails

## 本技能介绍：  
本技能提供了**OpenGuardrails插件**的安装和使用指南。它指导代理如何安装、配置和验证该插件，但本身不会执行任何代码。插件的源代码托管在[github.com/openguardrails/openguardrails](https://github.com/openguardrails/openguardrails)（`openclaw-security`子目录）。

## ClawHub、GitHub与npm之间的关联：  
该技能在ClawHub上的发布名为`[ThomasLWang/openguardrails](https://clawhub.ai/ThomasLWang/openguardrails)`，上游代码库同样位于[github.com/openguardrails/openguardrails](https://github.com/openguardrails/openguardrails)，由同一作者（Thomas Wang）维护。对应的npm包为`@openguardrails/openclaw-security`（[https://www.npmjs.com/package/@openguardrails/openclaw-security`）。这三个渠道均指向同一个代码库。您可以通过以下方式验证代码的来源：**“验证npm与GitHub之间的代码一致性”**。

## 快速入门（3个步骤）  
```bash
# 1. Install the plugin
openclaw plugins install @openguardrails/openclaw-security

# 2. Restart the gateway so the plugin is loaded
openclaw gateway restart

# 3. Register and activate (inside an OpenClaw session)
/og_activate
```

完成上述操作后，按照屏幕上的提示进行代理的注册并验证您的电子邮件地址。每个步骤的详细说明如下。

---

### OpenClaw代理的运行时安全防护机制  
OpenGuardrails为OpenClaw代理提供实时安全保护，有效防范以下关键威胁：  
- **数据泄露防护**：检测并阻止代理读取敏感文件后尝试将其发送到外部服务器的行为；  
- **敏感数据保护**：在数据传输前对个人身份信息（PII）、凭证和机密信息进行清洗；  
- **提示注入防护**：识别用于操控代理行为的恶意输入；  
- **命令注入拦截**：拦截shell escape、反引号替换及命令链式攻击；  
- **内容安全**：过滤不适宜公开的内容并执行基本的安全策略。  

## 安全性与可信度  
- **开源且可审计**：所有代码均遵循Apache 2.0许可协议，托管在[github.com/openguardrails/openguardrails](https://github.com/openguardrails/openguardrails)。您可以在安装前仔细审查每一行代码，尤其是工具事件钩子、数据清洗逻辑和网络调用相关部分。需要重点检查的文件包括：  
  - `index.ts`：插件入口文件，包含所有事件钩子；  
  - `agent/sanitizer.ts`：负责在数据传输前进行清洗的逻辑；  
  - `agent/content-injection-scanner.ts`：用于检测注入攻击的本地正则表达式模式；  
  - `platform-client/`：插件发起的所有出站网络请求；  
  - `agent/config.ts:65-68`：注册请求相关代码，确保仅发送`{ name, description }`信息。  

### 安装前的检查  
您可以在不安装的情况下查看npm包的完整内容：  
```bash
# View the npm package contents (no install)
npm pack @openguardrails/openclaw-security --dry-run

# Or download and extract the tarball to inspect
npm pack @openguardrails/openclaw-security
tar -xzf openguardrails-openclaw-security-*.tgz
ls package/
```

## 传输到云API的数据（及未传输的数据）  
- **传输内容**：仅传输经过清洗的工具元数据（工具名称、参数键、会话信息等）；所有敏感数据（如PII、凭证、文件内容、机密信息）在传输前会被替换为占位符（`<EMAIL>`、`<SECRET>`等）。  
- **禁止传输的内容**：原始文件内容、用户消息、聊天记录、实际凭证值或任何未经清洗的参数。  
- **数据保留政策**：检测请求的元数据在响应返回后会被删除；账户数据（代理ID、API密钥等）会永久保存以用于计费（这些信息在第三步的注册过程中收集）。  

### 本地模式  
该插件无需连接云端即可运行。所有本地安全机制（如shell escape拦截、内容注入检测等）都在本地完成，不会发起任何网络请求。云端评估功能为可选配置（需通过注册启用）。即使不进行注册，您仍可享受所有本地防护措施。  
- **安装过程中无网络请求**：插件在安装时不会发起任何网络请求，仅加载本地的`BehaviorDetector`并等待用户手动运行`/ogactivate`命令。  

### 网络请求行为说明  
插件仅有三种网络状态：  
- **未注册状态**：安装完成后、重启OpenClaw网关后；此时所有防护措施均为本地执行。  
- **已注册状态**：运行`/ogactivate`命令后；会向`/api/v1/agents/register`发送请求（仅包含`{ "name": "OpenClaw Agent", "description": "" }`）。  
- **激活状态**：验证电子邮件后；每次工具调用时都会向`/api/v1/detect`发送请求（仅针对异常行为）。  

### 注册流程  
运行`/ogactivate`会创建一个账户，并生成一个API密钥（格式为`sk-og-...`），该密钥保存在`~/.openclaw/credentials/openguardrails/credentials.json`中，用于云端评估和计费。您可以通过账户门户撤销密钥或删除该文件。请注意：系统不会在您未主动提供电子邮件地址之前收集该信息。具体注册流程详见“第三步：注册与激活”。  

### 失败时的处理方式  
如果云端API无法访问或超时，插件仍会正常运行（不会因网络问题而中断工作流程）。  

### 说明  
本文档（SKILL.md）仅包含安装和使用指南，不包含可执行代码。如需了解更多信息，请访问[github.com/openguardrails/openguardrails](https://github.com/openguardrails)查看插件源代码。  

## 工作原理  
插件会拦截`before_tool_call`、`after_tool_call`和`tool_result_persist`事件，实时监控工具调用行为：  
- **实时分类**：追踪敏感文件读取、外部网络请求、凭证访问及shell命令；  
- **即时拦截**：对关键行为进行本地拦截；  
- **云端评估**：对可疑行为通过云端API进行进一步分析。  

### 安装步骤  
- **安装插件**：可通过npm或直接从源代码安装（详见**CODE_BLOCK_3___）。安装过程中不会发起网络请求。  
- **重启网关**：安装完成后需重启OpenClaw网关以使插件生效（详见**CODE_BLOCK_4___）。  
- **验证插件状态**：确认插件已正确加载（详见**CODE_BLOCK_5___）。  

### 注册与激活（可选）  
注册后可获得云端评估功能（适用于已启用的本地防护机制）。具体操作步骤详见**CODE_BLOCK_7___。  

### `/ogactivate`命令的运行流程  
1. **注册**：插件向`/api/v1/agents/register`发送请求（内容为`{ "name": "OpenClaw Agent", "description": "" }`）。  
2. **保存凭证**：响应内容会被保存到`~/.openclaw/credentials/openguardrails/credentials.json`中（详见**CODE_BLOCK_8___）。  
3. **查看注册提示**：按照提示完成验证（详见**CODE_BLOCK_9___）。  
4. **激活代理**：在浏览器中访问验证链接，输入验证码并点击验证链接（详见**CODE_BLOCK_9___）。  

### 使用现有API密钥  
如果您已有API密钥（例如之前注册或通过账户门户获得的密钥），可直接使用（详见**CODE_BLOCK_10___）。  

### 状态检查  
激活后的代理状态可通过相应命令查询（详见**CODE_BLOCK_11___）。  

### 测试检测  
验证通过后，平台会自动发送包含隐藏注入攻击的测试邮件（详见**CODE_BLOCK_12___）。您可以通过以下步骤测试OpenGuardrails的功能：  
1. 查看收件箱中的测试邮件（主题为“Design Review Request”）；  
2. 将邮件保存为`.txt`文件（例如`~/test-email.txt`）；  
3. 指令代理读取该文件；  
4. OpenGuardrails会自动检测并删除其中的恶意代码。  

### 测试示例  
您还可以使用仓库中的示例文件进行测试（详见**CODE_BLOCK_14___）。  

### 账户与门户  
激活后，请使用您的电子邮件地址和API密钥登录账户门户（详见**CODE_BLOCK_15___**）。门户界面提供以下功能：  
- **账户概览**：查看计划详情和使用情况；  
- **代理管理**：管理API密钥；  
- **使用日志**：查看每个代理的请求历史和延迟情况；  
- **计划升级**：可选择免费、Pro或Business套餐。  

### 计划套餐  
| 计划 | 价格 | 每月检测次数 |  
|------|-------|---------------|  
| Free | $0 | 30,000次 |  
| Starter | $19/mo | 100,000次 |  
| Pro | $49/mo | 300,000次 |  
| Business | $199/mo | 2,000,000次 |  

### 命令说明  
- `/og_status`：显示注册状态、电子邮件地址和平台URL；  
- `/ogActivate`：用于注册（如需）并显示注册链接和激活说明。  

### 配置选项  
所有配置选项均保存在`~/.openclaw/openclaw.json`的`plugins.entries.openguardrails.config`文件中：  
| 选项 | 默认值 | 说明 |  
|--------|---------|-------------|  
| `enabled` | `true` | 启用/禁用插件；  
| `blockOnRisk` | `true` | 检测到风险时阻止相关操作；  
| `apiKey` | `""` | API密钥（默认为空）；运行`/ogActivate`命令时需要提供；  
| `agentName` | `"OpenClaw Agent"` | 控制面板显示的名称；  
| `coreUrl` | `https://www.openguardrails.com/core` | 平台API地址；  
| `dashboardUrl` | `https://www.openguardrails.com/dashboard` | 仪表盘地址；  
| `dashboardSessionToken` | `""` | 仪表盘认证令牌（默认使用API密钥）；  
| `timeoutMs` | `60000` | 云端评估超时时间（单位：毫秒）。  

### 可检测的行为模式  
- **快速路径拦截**：在本地完成拦截（无需网络请求）；  
- **内容注入检测**：在代理处理内容前自动删除恶意代码。  

### 云评估相关内容  
- **云评估模式**：详见**CODE_BLOCK_16___**。  

### AI安全网关（免费版本）  
OpenGuardrails提供免费的AI安全网关，作为本地HTTP代理，可保护数据不被发送到外部LLM提供商（如Anthropic、OpenAI、Gemini等）。  
- **工作原理**：网关在本地运行，拦截LLM API请求，对敏感数据进行清洗后再发送；用户看到的始终是清洗后的结果（详见**CODE_BLOCK_17___）。  

### 数据清洗类型  
OpenGuardrails支持多种数据类型的清洗（详见**CODE_BLOCK_17___**）。  

### 隐私与数据保护政策  
- **数据安全**：OpenGuardrails不会收集或出售用户数据；检测逻辑基于规则执行，不涉及任何机器学习模型。  
- **本地优先处理**：所有敏感数据在发送到云端之前都会在本地被替换为占位符。  

### 安装前的建议  
- **验证代码来源**：确认npm包确实来自GitHub仓库；  
- **仔细审查代码**：克隆仓库并检查关键文件；  
- **优先选择本地模式**：先在本地测试所有安全功能；  
- **监控网络流量**：确认插件仅与`openguardrails.com/core`进行通信；  
- **使用临时邮箱**：如需在测试期间避免使用个人邮箱。  

### 如需帮助  
如有疑问或需要企业级支持，请联系我们：  
- **邮箱**：thomas@openguardrails.com  
- **GitHub**：[github.com/openguardrails/openguardrails](https://github.com/openguardrails/openguardrails)  

感谢您的反馈！