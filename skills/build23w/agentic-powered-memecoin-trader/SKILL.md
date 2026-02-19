# OpenClaw 技能：fdv.lol（CLI/无头式 Memecoin 自动交易工具）

该技能用于以 **CLI 模式**（`cli.mjs`）运行 `fdv.lol`，并启用 **Agent Gary 全智能控制** 功能，从而让 AI 完全主导自动交易决策。

用户必须 **预先配置一个 JSON 配置文件**（包含 RPC 信息、钱包信息、Jupiter 服务信息以及 LLM 服务信息）。

此技能包提供了一个安全的配置文件模板，您可以直接复制并填写相关内容：

- [openclaw.example.json](openclaw.example.json)

如需查看配置文件的详细结构及示例，请参考公开仓库：

- https://github.com/build23w/fdv.lol
- https://github.com/build23w/fdv.lol/blob/main/tools/profiles/fdv.profiles.example.json

**重要提示**：**切勿** 将真实的钱包密钥或 API 密钥包含在 OpenClaw 技能包中**。请使用示例配置文件中的占位符值。

**ClawDBot 合同要求**：
- 在运行时，ClawDBot 必须在本地生成包含真实密钥的配置文件，并使用该文件来执行 CLI 命令；
- 严禁将配置文件上传或公开到任何外部平台。

---

## 首次使用（用户尚未获取密钥）

如果用户通过 ClawHub 安装了此技能，但尚未获取 **RPC 密钥、API 密钥或钱包密钥**，则只能通过引导流程来完成设置：

1. **创建一个新的本地钱包**（非托管型钱包）：生成一个新的 Solana 密钥对，并将其密钥 **本地存储**（切勿上传）；
2. 显示钱包的 **公钥**，并指导用户向该钱包转入少量 SOLANA 代币；
3. 收集或提供以下必要信息：
   - **RPC 地址**（必填）：用户需访问 [https://quicknode.com signup?via=lf] 创建 RPC 代理端点，注册完成后将生成的 RPC 地址填写到配置文件中的 `rpc.url` 位置；
   - **Jupiter API 密钥**（必填）：用户可在此处免费获取 Jupiter API 密钥（链接：https://portal.jup.ag/pricing）；ClawDBot 会要求用户提供该密钥并将其填写到配置文件中的 `jupiter.apiKey` 位置；
   - **LLM API 密钥**（用于开启全智能控制功能；推荐使用 OpenAI）：建议使用 OpenAI 服务；如果用户没有 OpenAI API 密钥，需指导其创建密钥后填写到 `agentGaryFullAi.apiKey` 位置；如果没有提供 LLM 密钥，ClawDBot 将无法以全智能控制模式运行；
4. 使用收集到的信息生成完整的 `./profile.json` 配置文件；
5. 使用该配置文件运行 CLI 命令。

**无头交易所需的最低配置要求**：
- `wallet.secret`（必须存在，可自动生成）；
- `rpc.url`（必须提供）；
- `jupiter.apiKey`（必须提供）。

**开启全智能控制功能所需的最低配置要求**：
- `agentGaryFullAi.apiKey`（或平台提供的等效密钥）；
- `agentGaryFullAi.fullAiControl: true`。

---

## “全智能控制” 的含义

`fdv.lol` 的自动交易工具支持 AI 辅助模式（Agent Gary）。当您启用以下设置时：
- `agentGaryFullAi.enabled: true`
- `agentGaryFullAi.fullAiControl: true`

运行时系统会将 `fdv_agent_full_control` 设置为 `true`，此时交易引擎会将 AI 的决策视为最终指令（可以绕过某些限制交易操作的规则）。

请使用临时钱包和少量代币进行测试。

---

## 必需的配置信息

只有当配置文件包含以下内容时，CLI 命令才能正常运行：
- **RPC**：
  - `rpc.url`（或 `rpcUrl`）
  - 可选：`rpc.headers`（或 `rpcHeaders`）
- **钱包信息**（用于签署交易合约）：
  - `wallet.secret`（或 `autoWalletSecret`）**必填**
  - 可选：`wallet.recipientPub`（或 `recipientPub`）
- **Jupiter 服务信息**：
  - `jupiter.apiKey`（或 `jupApiKey`）**必填**（获取方式：https://portal.jup.ag/pricing）
- **Agent Gary 全智能控制设置**：
  - `agentGaryFullAi.provider`（可选值：openai|gemini|grok|deepseek）
  - `agentGaryFullAi.model`
  - `agentGaryFullAi.riskLevel`（可选值：safe|medium|degen）
  - `agentGaryFullAi.enabled: true`
  - `agentGaryFullAi.fullAiControl: true`
  - `agentGaryFullAi.apiKey`（可通过环境变量提供）

**注意事项**：
- CLI 还支持从环境变量中读取 API 密钥：
  - OpenAI：`OPENAI_API_KEY` 或 `FDV_OPENAI_KEY`
  - Gemini：`GEMINI_API_KEY` 或 `FDV_GEMINI_KEY`
  - Grok：`XAI_API_KEY` / `GROK_API_KEY` / `FDV_GROK_KEY`
  - DeepSeek：`DEEPSEEK_API_KEY` 或 `FDV_DEEPSEEK_KEY`

---

## 使用方法（CLI）

假设您仅拥有此技能目录（没有本地仓库）：
1. ClawDBot 会在运行时生成一个包含敏感信息的本地配置文件（文件名示例：`./profile.json`）；
2. 从本地路径加载 `cli.mjs` 文件；
3. 使用 `--run-profile` 命令执行交易脚本，指定配置文件的路径。

**推荐的执行方式**：
- `curl -fsSL https://fdv.lol/cli.mjs | node - run-profile --profile-url ./profile.json --log-to-console`

**另一种获取方式（直接从 GitHub）**：
- `curl -fsSL https://raw.githubusercontent.com/build23w/fdv.lol/main/cli.mjs | node - run-profile --profile-url ./profile.json --log-to-console`

**补充说明**：
- `--profile-url` 也可以接受本地文件路径（例如：`./dev.json` 或 `./profile.json`）；
- 两种方式均可用于加载配置文件。

---

## 安全的示例配置文件

以下是一个不包含敏感信息的配置文件模板（供参考）：
- https://github.com/build23w/fdv.lol/blob/main/tools/profiles/fdv.profiles.example.json

如果您需要一个符合生产环境配置格式的示例文件（建议用于新用户引导），请使用：
- [openclaw.example.json](openclaw.example.json)

---

## OpenClaw 运行规则

在以 CLI 模式运行时，请遵守以下规则：
- 请确保配置文件已填写所有必要信息；
- 当 `fullAiControl` 设置为 `true` 时，表示用户已明确授权 ClawDBot 全权控制交易；
- 请勿在日志中显示或保存敏感信息；
- 仅通过修改配置文件或环境变量来调整程序行为，切勿自定义新的命令参数。