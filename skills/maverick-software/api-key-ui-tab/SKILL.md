---
name: apikeys-ui
description: "OpenClaw 的基于 Vault 的 API 密钥管理功能：  
- 提供安全的文件级密钥存储机制；  
- 支持从明文配置一键迁移密钥；  
- 具有动态密钥发现功能；  
- 提供用于技能管理的密钥选择器；  
- 支持手动创建密钥；  
- 还包含用于插件配置的设置选项卡。"
version: 3.0.0
author: OpenClaw Community
metadata: {"openclaw":{"emoji":"🔐","requires":{"openclaw":">=2026.1.0"},"category":"settings"}}
---
# 开放Claw控制面板中的Vault功能增强（UI v3.0.0）

OpenClaw控制面板支持基于Vault的API密钥管理。密钥存储在安全的文件（`~/.openclaw/secrets.json`，权限设置为0600）中，并通过OpenClaw内置的Secrets系统进行访问。AI代理永远不会看到这些密钥。

## 状态：✅ 已启用

| 组件 | 状态 |
|-----------|--------|
| Vault文件存储 | ✅ 已启用 |
| 密钥引用（SecretRef） | ✅ 已启用 |
| 动态密钥发现 | ✅ 已启用 |
| 一键迁移 | ✅ 已启用 |
| 插件注册选项卡 | ✅ 已启用 |
| Vault状态横幅 | ✅ 已启用 |
| 密钥状态徽章 | ✅ 已启用 |
| 仅限Vault的密钥部分 | ✅ 已启用 |
| 手动“+ 添加密钥”表单 | ✅ 已启用 |
| 重启通知横幅 | ✅ 已启用 |
| 技能 Vault 密钥选择器 | ✅ 已启用 |
| 技能内联密钥创建 | ✅ 已启用 |
| 认证配置文件显示 | ✅ 已启用 |

## 新功能

### 1. 基于Vault的存储

密钥存储在`~/.openclaw/secrets.json`文件中（文件权限设置为0600）。当您保存密钥时，UI会执行以下操作：
- 将密钥值写入vault文件
- 在`openclaw.json`中配置文件密钥提供者（如果尚未配置）
- 用`SecretRef`对象替换原始的配置值
- 显示重启通知——用户需要重启网关才能使更改生效

**迁移前的配置：**
```json
{
  "env": {
    "OPENAI_API_KEY": "sk-proj-abc123..."
  }
}
```

**迁移后的配置：**
```json
{
  "env": {
    "OPENAI_API_KEY": { "source": "file", "provider": "default", "id": "/OPENAI_API_KEY" }
  },
  "secrets": {
    "providers": {
      "default": { "source": "file", "path": "~/.openclaw/secrets.json", "mode": "json" }
    },
    "defaults": { "file": "default" }
  }
}
```

**Vault文件（`~/.openclaw/secrets.json`）：**
```json
{
  "OPENAI_API_KEY": "sk-proj-abc123..."
}
```

### 2. 一键迁移

当检测到明文密钥时，会显示“🔒 迁移到Vault”按钮。该按钮会：
- 扫描`openclaw.json`中的所有明文API密钥值
- 将它们全部迁移到vault文件中
- 用`SecretRef`对象替换配置文件中的密钥值
- 如有必要，自动配置文件提供者
- 显示已迁移的密钥列表

### 3. 动态密钥发现

UI会自动扫描整个配置文件以查找API密钥——无需依赖硬编码的密钥列表。

**检测模式：** `apiKey`、`api_key`、`token`、`secret`、`*_KEY`、`*_TOKEN`、`*_SECRET`

**搜索位置：**
- `env.*` — 环境变量
- `skills.entries.*.apiKey` — 与技能相关的密钥
- `messages.tts.*.apiKey` — TTS提供者的密钥
- 任何嵌套的配置路径

**已识别的提供者**会显示友好的名称、描述以及“获取密钥”链接：

| 提供者 | 环境变量键 |
|----------|---------|
| Anthropic | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Google / Gemini | `GOOGLE_API_KEY` / `GEMINI_API_KEY` |
| Brave Search | `BRAVE_API_KEY` |
| ElevenLabs | `ELEVENLABS_API_KEY` |
| Deepgram | `DEEPGRAM_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| Groq | `GROQ_API_KEY` |
| Fireworks | `FIREWORKS_API_KEY` |
| Mistral | `MISTRAL_API_KEY` |
| xAI (Grok) | `XAI_API_KEY` |
| Perplexity | `PERPLEXITY_API_KEY` |
| GitHub | `GITHUB_TOKEN` |
| Hume AI | `HUME_API_KEY` / `HUME_SECRET_KEY` |

### 4. Vault状态横幅

页面顶部会显示以下信息：
- **🔒 Vault已启用**（绿色）——所有密钥都存储在vault中，提供者配置完成
- **⚠️ 检测到明文密钥**（黄色）——建议迁移

### 5. 密钥状态徽章

每行密钥都会显示以下状态：
- **VAULT**（绿色）——密钥存储在安全的vault文件中
- **PLAINTEXT**（黄色）——密钥仍以原始字符串形式存在于配置文件中
- **NOT SET**（灰色）——密钥未配置

### 6. 仅限Vault的密钥部分

存储在vault中但未被任何配置路径引用的密钥会显示在专门的“仅限Vault的密钥”卡片中。这些密钥可能是手动创建的，或者是那些没有对应环境/配置条目的技能所使用的。每条密钥会显示：
- 带有密钥名称的🔒图标
- 遮盖后的密钥值预览
- 删除按钮

### 7. 手动“+ 添加密钥”表单

Vault选项卡的标题栏包含一个“+ 添加密钥”按钮，点击后会弹出一个内联表单：
- **KEY_NAME**输入框（建议使用大写蛇形字符）
- **密钥值**输入框（密码字段）
- **保存**/**取消**按钮
- 密钥会写入vault，但不会在配置文件中创建条目，也不会触发重启
- 密钥会立即显示在“仅限Vault的密钥”部分

### 8. 重启通知横幅

当写入vault导致配置文件更改时，会显示一个黄色警告横幅：
> ⚠ 新密钥需要重启网关才能生效。
> [立即重启]

该横幅会一直显示，直到用户点击“立即重启”或刷新页面。这取代了之前可能导致意外重启的自动刷新行为。

### 9. 技能 Vault 密钥选择器

在“技能”选项卡上，声明了`primaryEnv`的技能会显示一个Vault密钥选择器，而不是原始的密码输入框：

**未链接时：**
- 下拉列表会显示所有带有🔒图标的vault密钥
- 提供“选择ENV_NAME...的vault密钥”作为占位符
- 选择密钥后，会将`SecretRef`写入`skills.entries.<key>.apiKey`中
- “＋ 添加新的vault密钥...”选项会打开内联创建表单

**已链接时：**
- 会显示带有“解除链接”按钮的`🔒 KEY_NAME`
- 解除链接会从配置文件中移除`SecretRef`

### 10. 技能内联密钥创建

- 提供`KEY_NAME`和密钥值输入字段
- 点击“保存并链接”后，会一次性创建vault密钥并将其链接到技能
- 密钥也会显示在“仅限Vault的密钥”部分

### 11. 技能默认显示为展开状态

所有技能组（工作区、内置、管理的技能）现在都会默认显示为展开状态（`<details open>`），以便更好地查找技能。之前工作区和内置技能是默认隐藏的。

### 12. 认证配置文件显示

存储在vault中的认证配置文件密钥会连同其状态一起列出。后端RPC支持列出、重置错误和删除这些密钥。

## 架构

### 安全模型

```
┌──────────────────────────────────────────────────────────┐
│  Browser                                                  │
│  ┌──────────────────────────────────────────────────┐    │
│  │  Vault Tab                                        │    │
│  │  ┌──────────────────────────────────────────┐    │    │
│  │  │ OpenAI: [••••••••••] [Save] [✕]  🟢VAULT │    │    │
│  │  │ Anthropic: [        ] [Save]     ⚪NOT SET│    │    │
│  │  │ + Add Secret  [KEY_NAME] [value] [Save]   │    │    │
│  │  └──────────────────────────────────────────┘    │    │
│  │                                                   │    │
│  │  Skills Tab                                       │    │
│  │  ┌──────────────────────────────────────────┐    │    │
│  │  │ whisper-api: 🔒 OPENAI_API_KEY  [Unlink] │    │    │
│  │  │ sag:         [Select vault key ▾]         │    │    │
│  │  └──────────────────────────────────────────┘    │    │
│  └──────────────────────────────────────────────────┘    │
│                           │                               │
│                           ▼ (direct RPC, not via agent)   │
└───────────────────────────┼───────────────────────────────┘
                            │
                    ┌───────▼───────┐
                    │   Gateway     │
                    │ secrets.write │
                    │ skills.update │
                    └──┬─────────┬──┘
                       │         │
              ┌────────▼──┐  ┌──▼────────────┐
              │ secrets.   │  │ openclaw.json  │
              │ json       │  │ (SecretRef     │
              │ (0600)     │  │  objects only) │
              └────────────┘  └────────────────┘
```

### 后端RPC

| 方法 | 描述 |
|--------|-------------|
| `secrets.status` | 查看vault文件的状态、密钥数量和明文密钥的数量 |
| `secrets.list` | 列出带有遮盖值的密钥ID |
| `secrets.write` | 将密钥存储在vault中，并可选地使用`SecretRef`更新配置文件。`envEntry`参数（默认值为`true`）决定是否创建环境配置条目。返回`restartNeeded`标志，而不是自动刷新配置文件。 |
| `secrets.delete` | 从vault和配置文件中删除密钥 |
| `secrets.migrate` | 将所有明文密钥批量迁移到vault |
| `secrets.authProfiles.list` | 列出带有vault状态的认证配置文件密钥 |
| `secrets.authProfiles.resetErrors` | 重置认证配置文件的错误状态 |
| `secrets.authProfiles.delete` | 删除认证配置文件 |
| `skills.update` | 使用`vaultKeyId`参数更新配置文件——将`SecretRef`写入`skills.entries.<key>.apiKey`或解除链接 |

### 技能状态与Vault的集成

`SkillStatusEntry`包含一个`vaultKeyId`字段，用于读取**原始**的配置文件JSON（而不是运行时解析后的配置文件，因为在运行时`SecretRef`会被替换为解析后的字符串）。这是通过`extractVaultKeyIdFromConfig()`实现的，该方法直接读取`openclaw.json`并检查`skills.entries.<key>.apiKey`中的`SecretRef`对象。

### 重启行为

**保存密钥时不会自动重启。** 之前，`secrets.write`方法会调用`reloadSecrets()`，这可能会导致网关重启。现在：
- 仅存储在vault中的密钥（`envEntry: false`）不会修改配置文件——因此不需要重启
- 修改配置文件后，如果需要重启，则会返回`restartNeeded: true`——UI会显示重启横幅
- 将技能与vault关联后，会通过`writeConfigFile()`方法写入配置文件——这会触发配置文件监视器，从而导致网关重启（这是配置文件监视器的固有行为）

### OpenClaw Secrets系统的集成

此技能使用了OpenClaw内置的Secrets系统（`src/secrets/`）：
- **文件提供者：** `{ source: "file", path: "~/.openclaw/secrets.json", mode: "json" }`
- **SecretRef格式：** `{ source: "file", provider: "default", id: "/<KEY_NAME>" }`
- **运行时解析：** `prepareSecretsRuntimeSnapshot()`在网关启动时解析所有`SecretRef`对象
- **安全性：** 检查文件权限（0600），验证文件所有权，并保护文件路径

Secrets系统还支持`env`和`exec`提供者，以支持更高级的设置（例如环境变量、外部vault命令）。对于此UI来说，文件提供者是默认的。

### 修改的文件（OpenClaw仓库中的源代码位置）

| 文件 | 用途 |
|------|---------|
| `src/gateway/server-methods/secrets.ts` | Vault相关的RPC方法（状态、列表、写入、删除、迁移、认证配置文件） |
| `src/gateway/server-methods/skills.ts` | 使用`vaultKeyId`参数更新技能配置 |
| `src/gateway/server-methods/plugins-ui.ts` | 插件视图注册 |
| `src/gateway/protocol/schema/agents-models-skills.ts` | `SkillsUpdateParamsSchema`中的`vaultKeyId` |
| `src/agents/skills-status.ts` | `SkillStatusEntry`中的`vaultKeyId`字段，用于读取原始配置文件 |
| `ui/src/ui/controllers/apikeys.ts` | 具有vault意识的状态处理、添加Vault密钥、加载仅限vault的密钥 |
| `ui/src/ui/controllers/skills.ts` | `VaultKeyEntry`类型、加载仅限vault的密钥、将技能链接到vault密钥 |
| `ui/src/ui/views/apikeys.ts` | Vault UI（横幅、徽章、迁移功能、添加表单、仅限vault的密钥、重启横幅） |
| `ui/src/ui/views/skills.ts` | Vault密钥选择器下拉列表、内联密钥创建功能 |
| `ui/src/ui/app.ts` | 状态属性（vault、重启、技能密钥管理） |
| `ui/src/ui/app-render.ts` | 用于处理vault和技能的状态属性 |
| `ui/src/ui/app-settings.ts` | 用于加载vault密钥的选项卡触发逻辑 |
| `ui/src/ui/types.ts` | `SkillStatusEntry`中的`vaultKeyId` |
| `ui/src/ui/navigation.ts` | Vault选项卡（锁定图标），移除了1password和Discord独立选项卡 |

### 参考文件

```
apikeys-ui/
├── SKILL.md                              # This file
├── INSTALL_INSTRUCTIONS.md               # Step-by-step installation (legacy)
└── reference/
    ├── apikeys-controller.ts             # UI controller (vault tab)
    ├── apikeys-views.ts                  # UI view (vault tab)
    ├── secrets-rpc.ts                    # Backend vault RPCs
    ├── skills-controller.ts              # UI controller (skills vault integration)
    ├── skills-views.ts                   # UI view (vault key selector)
    ├── skills-status.ts                  # Backend skill status with vaultKeyId
    └── skills-rpc.ts                     # Backend skills update RPC
```

## 关于密钥设计的决策

1. **保存密钥时不会自动重启** — `secrets.write`方法不再调用`reloadSecrets()`。现在会显示一个带有“立即重启”按钮的横幅，让用户决定是否需要重启。
2. **仅限Vault的密钥** — 使用`envEntry: false`创建的密钥不会显示在配置文件中。通过单独的`secrets.list`方法可以找到所有存储在vault中的密钥，并将它们显示在专门的区域。
3. **读取原始配置文件以获取`vaultKeyId` — 运行时会将`SecretRef`解析为字符串，因此`loadConfig()`方法返回解析后的值。`extractVaultKeyIdFromConfig()`方法直接读取原始JSON文件（并使用mtime进行缓存），以检测`SecretRef`对象。
4. **技能默认显示为展开状态** — 所有`<details>`组都会默认显示，以便更好地使用。之前默认隐藏了需要配置的技能。
5. **技能使用vault引用，而不是明文密钥** — 声明`primaryEnv`的技能会显示一个Vault密钥选择器下拉列表，而不是原始的密码输入框。链接密钥时，会将`SecretRef`写入`skills.entries.<key>.apiKey`中。
6. **技能内联密钥创建** — 在技能下拉列表中选择“＋ 添加新的vault密钥...”后，会一次性创建并链接密钥。

## 更新日志

### v3.0.0
- 在Vault选项卡的标题栏中添加了“+ 添加密钥”表单——允许在没有配置条目的情况下创建vault密钥
- 显示了“仅限Vault的密钥”部分——显示配置文件中未引用的vault密钥
- 添加了重启通知横幅——黄色警告和“立即重启”按钮取代了自动刷新功能
- 技能的Vault密钥选择器——使用下拉列表代替了原始的密码输入框
- 技能内联密钥创建功能——点击“＋ 添加新的vault密钥...”后，可以一次性创建并链接密钥
- 所有技能组默认显示为展开状态——不再默认隐藏
- `SkillStatusEntry`中包含`vaultKeyId`字段——用于读取原始配置文件以检测`SecretRef`对象
- `secrets.write`方法中的`envEntry`参数——用于控制是否创建环境配置条目
- `skills.update`方法中的`vaultKeyId`参数——用于将`SecretRef`写入`skills.entries.<key>.apiKey`或解除链接

### v2.0.0
- **基于Vault的存储：** 密钥存储在`~/.openclaw/secrets.json`文件中（权限设置为0600），而不是以明文形式存储在配置文件中
- **SecretRef集成：** 配置文件中的值被替换为指向vault的OpenClaw `SecretRef`对象
- **一键迁移：** “迁移到Vault”功能可以批量迁移所有明文密钥
- **Vault状态横幅：** 绿色（所有密钥都存储在vault中）或黄色警告（检测到明文密钥）
- **密钥徽章：** 根据密钥类型显示VAULT / PLAINTEXT / NOT SET
- **新增的RPC方法：** `secrets.status`、`secrets.list`、`secrets.write`、`secrets.delete`、`secrets.migrate`
- **插件UI注册：** 将插件注册功能从旧导航栏移至插件架构（设置组，位于第1位）
- **自动配置提供者：** 保存密钥时会自动配置文件密钥提供者（如果该提供者不存在）

### v1.1.0
- 动态密钥发现——扫描整个配置文件，而不是依赖硬编码的密钥列表
- 根据类别（环境/技能/其他）自动对密钥进行分组
- 即使未配置，也会显示常见的环境密钥

### v1.0.0
- 初始版本，提供者字段为硬编码
- 通过`config.patch`实现保存/清除功能