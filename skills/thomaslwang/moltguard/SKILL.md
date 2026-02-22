---
name: openguardrails
description: "**AI代理的运行时安全插件**  
该插件优先采用本地防护机制，有效防止数据泄露、凭证窃取、命令注入以及敏感信息的泄露。插件还包含一个免费的AI安全网关（AI Security Gateway），可在数据传输至大型语言模型（LLM）提供商之前对其进行清洗和处理（即去除其中的个人身份信息（PII））。  
**完全开源**（遵循Apache 2.0许可证）：所有的检测与清洗逻辑均可在GitHub上公开审核。  
**来源链接**：[github.com/openguardrails/openguardrails]"
metadata: {"openclaw":{"emoji":"🛡️","homepage":"https://github.com/openguardrails/openguardrails","keywords":["security","prompt-injection","data-exfiltration","pii","credential-theft","command-injection","guardrails","safety","agent-security"]}}
---
# OpenGuardrails

## 本技能介绍：  
本文档是关于OpenGuardrails安全插件的安装与使用指南。该插件的源代码托管在开源仓库 [github.com/openguardrails/openguardrails](https://github.com/openguardrails/openguardrails)（子目录 `openclaw-security/`）中。该技能本身不执行任何代码，仅介绍如何安装、配置和验证该插件。

## ClawHub与GitHub的关联：  
该技能在ClawHub上的发布名为 [`ThomasLWang/openguardrails`](https://clawhub.ai/ThomasLWang/openguardrails)，其上游代码同样由Thomas Wang维护，仓库地址为 [github.com/openguardrails/openguardrails](https://github.com/openguardrails/openguardrails)。该技能对应的npm包名为 [`@openguardrails/openclaw-security`](https://www.npmjs.com/package/@openguardrails/openclaw-security)，三者均指向同一代码库。

### OpenClaw代理的运行时安全防护  
OpenGuardrails提供以下安全防护功能：  

- **数据泄露防御**：检测并阻止代理读取敏感文件后尝试将其发送到外部服务器的行为。  
- **敏感数据保护**：在数据传输给大型语言模型（LLM）之前，对个人身份信息（PII）、凭证和机密数据进行清洗。  
- **提示注入防护**：识别用于操控代理行为的恶意输入。  
- **命令注入阻止**：拦截shell escape、反引号替换以及工具参数中的命令链操作。  
- **内容安全**：过滤不适宜公开的内容，并执行基本的安全策略。  

## 安全性与透明度  
- **开源且可审计**：所有代码均遵循Apache 2.0许可证，可在 [github.com/openguardrails/openguardrails](https://github.com/openguardrails/openguardrails) 查看。安装前可审计所有代码，尤其是工具事件钩子、数据清洗逻辑和网络调用相关部分。  
  - **关键文件**：`agent/sanitizer.ts`（负责数据清洗）；`agent/content-injection-scanner.ts`（用于检测注入行为）；`gateway/src/sanitizer.ts`（AI安全网关的清洗逻辑）；`index.ts`（插件入口点，展示所有事件钩子）。  

### 数据传输规则  
- **传输内容**：仅传输经过清洗的工具元数据（如工具名称、参数键、会话信息等）；所有敏感信息（如PII、凭证、文件内容、机密数据）在传输前会被替换为占位符（`<EMAIL>`、`<SECRET>` 等）。  
- **禁止传输的内容**：原始文件内容、用户消息、对话记录、实际凭证值或未经清洗的参数值。  
- **数据保留**：检测请求的元数据在响应返回后会被删除；账户信息（代理ID、邮箱、套餐等级、代理使用量）会永久保存用于计费和账户管理。  

### 本地模式  
该插件无需连接云端即可运行，所有本地安全检测（如shell escape阻止、内容注入检测等）均在本地完成，不涉及网络请求。云端评估为可选功能，需通过注册激活。即使不注册，也能享受所有本地防护措施。  

### 安装过程  
安装过程中插件不会发起任何网络请求，仅加载本地`BehaviorDetector`并等待用户手动运行 `/ogactivate` 命令。  

### 注册流程  
注册时仅发送最小量的数据（`{ name, description }`），服务器返回的API密钥和代理ID会保存在本地。具体请求/响应格式详见“步骤2：注册”部分。  

### 失败情况下的应对机制  
如果云端API不可达或超时，插件仍允许工具正常运行，不会因网络问题影响工作流程。  

### 注意事项  
本文档（SKILL.md）仅包含安装和使用说明，不包含可执行代码。建议在安装前仔细审核源代码。  

## 工作原理  
插件会监听 `before_tool_call`、`after_tool_call` 和 `tool_result_persist` 事件，实时监控所有工具调用行为：  
- 检测敏感文件读取、外部网络请求、凭证访问及shell命令；  
- 危险行为会立即在本地被阻止，复杂行为会通过云端API进行评估。  

### 安装步骤  
1. 通过npm或直接从源代码安装插件（安装过程不涉及网络请求）。  
2. 运行 `/ogactivate` 命令进行注册（可选，注册后可启用云端评估）。  

### 注册请求内容  
注册时插件会发送 `POST /api/v1/agents/register` 请求，包含代理显示名称和可选描述。  

### 本地数据存储  
注册后的响应数据会保存在 `~/.openclaw/credentials/openguardrails/credentials.json` 文件中。  

### 激活步骤  
激活后，请按照以下步骤操作：  
1. 访问 `/ogactivate` 显示的链接；  
2. 输入验证码；  
3. 输入邮箱（作为账户身份验证；  
4. 点击发送到邮箱的验证链接。  

### 测试方法  
系统会发送测试邮件（包含隐藏的注入代码），验证OpenGuardrails是否正常工作。  

### 其他功能  
- 可使用仓库中的示例文件进行测试。  
- 支持通过现有API密钥直接使用插件（无需重新注册）。  

## 配置选项  
所有配置选项均保存在 `~/.openclaw/openclaw.json` 的 `plugins.entries.openguardrails.config` 文件中：  
- `enabled`：启用/禁用插件；  
- `blockOnRisk`：检测到风险时阻止工具调用；  
- `apiKey`：API密钥；  
- 其他配置选项用于自定义插件行为。  

## 隐私与数据保护  
OpenGuardrails遵循严格的数据保护政策，不收集或出售用户数据。所有检测结果仅用于内部用途，不会用于训练模型。  

## 其他特性  
- 提供免费的AI安全网关，保护数据不被发送给外部LLM服务。  
- 支持本地部署，无需额外费用。  

## 如需更多信息或支持，请联系我们。