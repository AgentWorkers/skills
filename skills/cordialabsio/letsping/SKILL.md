---
name: letsping
description: 对于高风险操作（如执行具有破坏性、财务影响或社会影响的操作，或对基础设施进行修改），需要经过人工审核（即“人在回路”（Human-in-the-loop）的批准流程。在执行这些操作之前，代理程序必须先调用 `letssping_ask` 函数。
disable-model-invocation: false
metadata:
  openclaw:
    emoji: ":shield:"
    requires:
      env: ["LETSPING_API_KEY"]
---
### 安装（运行时组件）

此注册表条目仅用于提供安装说明。`letsping_ask` 运行时组件由 `@letsping/openclaw-skill` npm 包提供。您可以通过以下方式之一进行安装：

- **使用 npm：** `npm install @letsping/openclaw-skill`（安装完成后，请在您的 OpenClaw 工作区中注册该组件，以便它能够被正确加载）。
- **克隆代码：** `git clone https://github.com/CordiaLabs/openclaw-skill ~/.openclaw/workspace/skills/letsping && cd ~/.openclaw/workspace/skills/letsping && npm install`。

请将 `LETSPING_API_KEY`（您的 LetsPing 代理密钥，例如 `lp_live_...`）设置在该组件的环境变量中。您可以通过 [https://letsping.co/openclaw/pair](https://letsping.co/openclaw/pair) 或 LetsPing 的代理凭据 API 获取该密钥。请注意：此密钥属于高度敏感的信息，务必使用专用的代理密钥，并在密钥泄露时立即撤销其权限。

### 使用方法

该组件提供了 `letsping_ask` 工具，用于处理高风险操作。代理会触发该工具，在获得您的批准、应用补丁或收到拒绝响应之前暂停操作，仅在执行获授权的操作后才会继续执行。

**重要提示：** 请使用性能较高的模型（如 Claude Opus、GPT-4o 或更高级别的模型）以降低被绕过安全机制的风险。较低性能的模型更容易受到攻击。

**操作说明：** 将以下内容复制到您的工作区文件 `TOOLS.md` 或 `AGENTS.md` 中（或添加到系统的提示系统中）：

> 您仅对 **安全** 操作拥有完全的自主执行权限，例如：读取文件/日志、进行网络搜索、查看/分析数据（且不会产生任何副作用）。

在执行任何 **高风险** 操作之前，**必须** 先调用 `letsping_ask`；**绝对禁止** 直接执行高风险操作。高风险操作包括：
- **财务相关操作：** 任何支出、交易或金额超过 10 美元的预订。
- **破坏性操作：** 删除/覆盖文件、数据库记录或配置文件。
- **社交相关操作：** 在公开平台上发布内容、向新联系人发送私信或群组消息。
- **基础设施相关操作：** 修改 DNS 设置、环境变量、部署配置、基础设施 API 或权限设置。

在请求升级时，请提供以下信息：
- `tool_name`：具体使用的工具名称（例如：“system_run”）。
- `args_json`：原始参数的 JSON 格式化字符串。
- `risk_reason`：清晰、简洁的操作风险说明（例如：“可能删除重要文件”）。

**操作结果处理：**
- **如果请求获得批准：** 仅使用 `executed_payload`（即经过处理的、获授权的操作内容）。
- **如果请求被拒绝或超时：** 中止操作，尝试更安全的方案，或请求用户的指导。

**示例：**
1. **安全操作（无需调用 `letsping_ask`）：`browser_search(query: "当前纽约市的天气")`。
2. **高风险操作（需要调用 `letsping_ask`）：`letsping_ask/tool_name: "vercel_deploy", args_json: "{\"project\":\"my-app\",\"env\":\"production\",\"force\":true}", risk_reason: "强制进行生产环境部署")`。
3. **高风险操作（需要调用 `letsping_ask`）：`letsping_ask/tool_name: "system_run", args_json: "{\"cmd\":\"rm -rf /important/folder\"}", risk_reason: "删除重要文件夹")`。
4. **高风险操作（需要调用 `letsping_ask`）：`letsping_ask/tool_name: "discord_send", args_json: "{\"channel\":\"general\",\"message\":\"意外泄露了文件列表：ls ~\"}", risk_reason: "可能在公开频道中泄露数据")`。

**注意事项：**
- **请先在沙箱环境中彻底测试** 高风险操作流程，验证升级机制的可靠性（在性能良好的模型/提示系统下，该机制的可靠性应达到 90-95%）。如果代理未触发升级请求，请补充更多示例或优化提示语句。
- **故障排除：**
  - **代理未执行规则？** 可通过增加更多测试用例或设置“一旦检测到任何风险类别即触发升级”来加强规则的执行。
  - **操作超时或被拒绝？** 代理应给出友好的提示（例如：“请求被拒绝，请提供其他解决方案”）。