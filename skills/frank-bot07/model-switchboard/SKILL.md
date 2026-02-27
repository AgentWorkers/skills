# Model Switchboard v3.0 — 为 OpenClaw 提供的安全 AI 模型配置工具

> ⛔ **重要规则：** **严禁直接编辑 `openclaw.json` 文件中的模型字段！**  
> 请始终使用本工具提供的命令进行模型配置，没有任何例外。

## 该工具存在的必要性  

直接编辑 `openclaw.json` 文件来修改模型配置是导致 OpenClaw 网关崩溃的首要原因。错误的模型类型被分配到错误的插槽中会导致系统立即崩溃；如果没有备份数据，则需要花费数小时时间重新构建系统。本工具能够完全避免此类问题。

## 工作原理  

1. 在进行任何修改之前，会先验证模型的格式和角色兼容性。  
2. 每次修改前都会自动备份配置（保留 30 份备份数据）。  
3. 该工具使用 OpenClaw 的 CLI 命令行接口（`openclaw models set`）进行操作，绝不会直接使用原始的 JSON 数据。  
4. 该工具会阻止不安全的模型配置（例如：将仅用于图像生成的模型设置为主要的 Large Language Model）。  
5. 如果出现任何问题，系统会立即回滚到之前的配置状态。  
6. 提供图形化的 Canvas 用户界面（`ui/index.html`）用于直观地管理模型配置。

## 快速参考  

```bash
SWITCHBOARD="$SKILL_DIR/scripts/switchboard.sh"

# View current setup
$SWITCHBOARD status

# Change models
$SWITCHBOARD set-primary "anthropic/claude-opus-4-6"
$SWITCHBOARD set-image "google/gemini-3-pro-preview"
$SWITCHBOARD add-fallback "openai/gpt-5.2"
$SWITCHBOARD remove-fallback "openai/gpt-5.2"
$SWITCHBOARD add-image-fallback "openai/gpt-5.1"

# Preview before applying
$SWITCHBOARD dry-run set-primary "openai/gpt-5.2"

# Discovery & recommendations
$SWITCHBOARD discover          # List all available models
$SWITCHBOARD recommend         # Get optimal suggestions

# Redundancy (3-deep failover)
$SWITCHBOARD redundancy        # Assess current redundancy
$SWITCHBOARD redundancy-deploy # Preview optimal config
$SWITCHBOARD redundancy-apply  # Apply optimal config
$SWITCHBOARD redundancy-apply 4  # Custom depth

# Backup & restore
$SWITCHBOARD backup            # Manual backup
$SWITCHBOARD list-backups      # Show all backups
$SWITCHBOARD restore latest    # Undo last change

# Import/Export (portable model configs)
$SWITCHBOARD export config.json
$SWITCHBOARD import config.json

# Cron model validation
$SWITCHBOARD validate-cron-models  # Check cron jobs use valid models

# Diagnostics
$SWITCHBOARD health            # Gateway + provider status
$SWITCHBOARD validate <model> <role>  # Test compatibility
```

## 模型角色及其用途  

| 角色 | 用途 | 配置键值对 |
|------|---------|-----------|
| **Primary** | 用于所有对话的主要 Large Language Model | `agents.defaults.model.primary` |
| **Fallback** | 备用的 Large Language Models | `agentsdefaults.model.fallbacks` |
| **Image** | 用于图像处理 | `agentsdefaults.imageModel.primary` |
| **Image Fallback** | 备用的图像处理模型 | `agentsdefaults.imageModel.fallbacks` |
| **Heartbeat** | 用于低成本的轮询任务 | `agentsdefaults.heartbeat.model` |
| **Coding** | 用于生成子代理代码的模型 | `agentsdefaults.coding.model` |

## 验证规则  

验证引擎（`scripts/validate.py`）会执行以下检查：  
- **格式要求**：模型名称必须遵循 `provider/model-name` 的格式（例如：`anthropic/claude-opus-4-6`）。  
- **能力匹配**：模型角色必须具备 `llm` 或 `tools` 能力。  
- **图像处理模型**：必须具备 `vision` 能力。  
- **禁止的模型**：仅用于图像生成的模型（如 DALL-E、Stability）无法被分配给任何大型语言模型角色。  
- **未知模型**：虽然会被警告，但仍然允许使用（特别是对于新的 OpenRouter 模型）。  

## 支持的模型提供者  

- `anthropic`：Claude 系列模型（Opus、Sonnet、Haiku）  
- `openai`：GPT 系列模型  
- `openai-codex`：Codex OAuth 模型  
- `google`：Gemini 系列模型  
- `opencode`：Zen 代理（可访问多种模型）  
- `zai`：GLM 系列模型  
- `xai`：Grok 系列模型  
- `openrouter`：多提供者模型管理工具  
- `groq`、`cerebras`：快速推理模型  

## Canvas 用户界面  

在 `ui/index.html` 中，可以通过 Canvas 用户界面查看以下信息：  
- 主要使用的 Large Language Model 及图像处理模型（通过颜色编码显示）  
- 备用模型列表（按使用顺序排列）  
- 提供者的认证状态（绿色/红色指示灯）  
- 模型的允许使用情况  
- 配置错误及其严重程度  
- 备份次数  

## 对代理程序的操作说明  

当用户请求更改模型配置时，请按照以下步骤操作：  
1. 首先阅读本文档（`SKILL.md`）。  
2. 查看当前模型配置状态：`$SWITCHBOARD status`。  
3. 预览即将进行的配置更改：`$SWITCHBOARD dry-run <action> <model>`。  
4. 得到用户确认后再执行更改。  
5. 实际应用更改：`$SWITCHBOARD <action> <model>`。  
6. 更改后检查网关的运行状态。  

**严禁以下操作：**  
- 直接编辑 `openclaw.json` 文件中的模型字段。  
- 在更改主要模型配置时跳过预测试步骤。  
- 未经用户确认就直接应用更改。  
- 忽视验证错误。  

## 常见问题及解决方法  

**网关无法启动？**  
请检查配置文件和系统日志。  

**出现 “模型不被允许使用” 的错误？**  
请确认该模型是否在允许使用的模型列表中；如果不在列表中，请将其添加到列表中或从列表中删除。  

**出现 “未知模型” 的警告？**  
该模型可能尚未在系统注册表中注册。请将其添加到注册表中以便后续使用。  

## 文件结构  

```
model-switchboard/
├── SKILL.md              # This file — agent instructions
├── README.md             # ClawHub publishing readme
├── model-registry.json   # Known model capabilities database
├── scripts/
│   ├── switchboard.sh    # Main CLI tool (bash)
│   └── validate.py       # Validation engine (python3, no deps)
└── ui/
    └── index.html        # Canvas dashboard (single-file, no deps)
```