# Vapi (vapi.ai) — OpenClaw 技能

当您需要管理 OpenClaw 代理中的 **Vapi 语音助手**、通话、电话号码、工具和 Webhook 时，请使用此技能。

此技能基于 **API**（Vapi REST）设计，并可选地与 **Vapi CLI** 集成，以支持 MCP 文档和本地工作流程。

## 您可以执行的操作

- 创建/更新/列出 **语音助手**
- 开始/检查/结束 **通话**
- 管理 **电话号码**
- 创建/管理 **工具**（函数调用）
- 配置 **Webhook** 并检查事件

## 所需的密钥

请设置以下密钥之一：

- `VAPI_API_KEY`（推荐）— Vapi 仪表板 API 密钥。

### 如何提供密钥（推荐）

- 将密钥存储为网关密钥或环境变量（更佳）；
- 在运行辅助脚本之前将其导出到您的 shell 中。

切勿将密钥粘贴到公共日志中。

## 端点

基础 URL：

- `https://api.vapi.ai`

认证：

- `Authorization: Bearer $VAPI_API_KEY`

API 参考：

- https://api.vapi.ai/api (Swagger)

## 工具选项

此技能支持 **两种** 方法；您可以根据部署需求进行选择：

- 设置 `VAPI_MODE=api` 以优先使用 REST（默认值）；
- 设置 `VAPI_MODE=cli` 以优先使用 Vapi CLI（交互式操作）。

### 选项 A — 通过辅助脚本使用 REST（适用于所有环境）

此仓库包含一个简单的 Node.js 辅助脚本：

- `skills/vapi/bin/vapi-api.mjs`

示例：

```bash
# list assistants
VAPI_API_KEY=... node skills/vapi/bin/vapi-api.mjs assistants:list

# create assistant
VAPI_API_KEY=... node skills/vapi/bin/vapi-api.mjs assistants:create \
  --name "Claw Con Concierge" \
  --modelProvider openai --model gpt-4o-mini \
  --voiceProvider 11labs --voiceId rachel

# start an outbound call (example shape; see swagger for required fields)
VAPI_API_KEY=... node skills/vapi/bin/vapi-api.mjs calls:create \
  --assistantId asst_xxx \
  --to "+14155551234" \
  --from "+14155559876"
```

### 选项 B — 使用 Vapi CLI（适用于交互式操作）

如果 `VAPI_MODE=cli`，建议使用 CLI 进行管理任务；如果未安装 CLI，则可回退到 REST。

文档：
- https://docs.vapi.ai/cli
- https://github.com/VapiAI/cli

安装：

```bash
curl -sSL https://vapi.ai/install.sh | bash
vapi login
```

### 选项 C — 用于 IDE 的 MCP 文档服务器

这可以提升 IDE 的辅助功能（如 Cursor、Windsurf、VSCode）：

- https://docs.vapi.ai/cli/mcp

```bash
vapi mcp setup
```

## 代理使用指南

当用户请求对 Vapi 进行更改时，请遵循以下步骤：

1. 明确更改的范围：是修改语音助手、电话号码、Webhook 还是工具调用；
2. 在进行任何破坏性更改之前，先执行 **只读** 操作（如列出或获取信息）；
3. 在创建语音助手时，请提供以下信息：
   - 助手名称
   - 模型提供者/模型
   - 语音提供者/语音 ID
   - 对工具/函数调用的需求
   - Webhook URL（如果使用服务器事件）
4. 在发起通话时，请确认以下信息：
   - 调用方/被调用方的电话号码
   - 助手 ID
   - 合规性要求（如录音、同意政策）

## 本技能包含的文件

- `skills/vapi/SKILL.md` — 本文件
- `skills/vapi/bin/vapi-api.mjs` — 基本的 REST 辅助脚本

## 参考资源

- Vapi 文档简介：https://docs.vapi.ai/quickstart/introduction
- Vapi CLI：https://github.com/VapiAI/cli
- Vapi MCP：https://docs.vapi.ai/cli/mcp
- Vapi API（Swagger）：https://api.vapi.ai/api
- 示例服务器（Node.js）：https://github.com/VapiAI/example-server-javascript-node
- OpenClaw：https://github.com/openclaw/openclaw