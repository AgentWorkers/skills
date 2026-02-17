---
name: discord-connect-hub
description: Clawdbot的完整Discord集成功能，支持自动安装用户界面（UI）。该集成提供了与Discord机器人的连接、控制面板中的相关标签页、设置向导、凭证管理、服务器监控以及插件架构接口。适用于配置Discord频道集成或向Control控制面板添加Discord标签页的场景。集成过程中会自动安装UI组件、RPC处理程序，并更新导航界面。
---
# Discord Connect Hub

这是一个专为Clawdbot设计的完整Discord集成插件，支持自动安装用户界面（UI）。该插件提供了连接Discord机器人所需的所有功能，包括：

- **Discord频道插件**：实现与Discord机器人的全面消息交互功能。
- **控制面板（Dashboard）**：提供用于设置和监控的Web界面。
- **设置向导（Setup Wizard）**：引导用户逐步创建和配置机器人。
- **凭证管理（Credential Management）**：支持安全地存储机器人凭证（使用OpenBao技术）。
- **服务器监控（Server Monitoring）**：包括服务器健康检查和公会管理功能。
- **插件架构钩子（Plugin Architecture Hooks）**：实现UI组件的自动安装。

## 安装

该插件会自动安装所有必要的组件：

```bash
# Install via agent
Install the discord-connect-hub skill from ClawHub
```

安装完成后，插件将自动完成以下操作：
1. 如果尚未安装，会自动安装Discord频道插件。
2. 在控制面板（Control Dashboard）中添加Discord相关选项卡。
3. 注册用于管理Discord功能的RPC（Remote Procedure Call）处理程序。
4. 设置导航结构和路由规则。
5. 安装UI组件并显示在控制面板上。

## 主要功能

### Discord机器人集成
- 完整的Discord.js机器人实现。
- 支持发送和接收带格式化的消息。
- 支持反应（Reactions）和表情符号（Emojis）。
- 支持文件附件（File Attachments）。
- 支持Slash命令（Slash Commands）。
- 支持成员和公会（Members and Guilds）管理。

### 控制面板（Dashboard）
- **连接状态（Connection Status）**：显示机器人的实时状态和健康状况。
- **设置向导（Setup Wizard）**：提供交互式的机器人创建指南。
- **服务器管理（Server Management）**：可以查看公会、频道和权限信息。
- **邀请生成器（Invite Generator）**：生成机器人邀请链接。
- **健康诊断（Health Diagnostics）**：提供自动故障排查功能。
- **凭证管理（Token Management）**：安全存储机器人凭证。

### 插件架构集成
- 自动安装Discord相关选项卡。
- 动态更新导航结构。
- 注册RPC方法（RPC Method Registration）。
- 提供配置管理功能。
- 支持重启机器人服务（Restart Orchestration）。

## 快速设置

### 1. 设置Discord应用
1. 访问 [discord.com/developers/applications](https://discord.com/developers/applications)。
2. 创建新应用（Create New Application），输入应用名称并点击“创建”（Create）。
3. 转到“机器人”（Bot）选项卡，点击“重置令牌”（Reset Token），然后复制令牌（Copy Token）。
4. 确保已启用“消息内容意图”（Message Content Intent）功能。

### 2. 配置机器人权限
1. 转到“OAuth2”（OAuth2）设置，点击“URL生成器”（URL Generator）：
   - 选择权限范围：`bot` 和 `applicationscommands`。
   - 设置权限：发送消息（Send Messages）、读取历史记录（Read History）、使用反应（Reactions）、嵌入内容（Embeds）、使用Slash命令（Slash Commands）。
   - 复制生成的邀请链接（Invite URL），在浏览器中打开并授权（Authorize）。

### 3. 在Clawdbot中进行配置
**推荐方式：使用控制面板（Option A）**
1. 打开控制面板（Control Dashboard），选择“频道”（Channels），然后点击“Discord”。
2. 粘贴机器人令牌（Paste Bot Token），然后点击“保存并连接”（Save & Connect）。

**备用方式：使用配置文件（Option B）**
```yaml
channels:
  discord:
    botToken: "YOUR_BOT_TOKEN"
    # Or with OpenBao:
    # botToken: "bao:channels/discord#bot_token"
```

## 插件架构钩子（Plugin Architecture Hooks）

该插件包含以下钩子，用于与Clawdbot的插件架构集成：

### 安装钩子（Installation Hooks）
- `install/navigation.js`：在控制面板中添加Discord选项卡。
- `install/rpc-handlers.js`：注册用于处理Discord请求的RPC方法。
- `install/ui-components.js`：安装UI组件和模板。
- `install/config-defaults.js`：设置默认配置。

### 运行时钩子（Runtime Hooks）
- `hooks/post-install.js`：安装完成后进行配置验证和初始化。
- `hooks/pre-uninstall.js`：在卸载插件前进行清理操作。
- `hooks/config-updated.js`：响应配置变更。

### 插件功能声明
该插件向插件系统声明了以下功能：
- **UI选项卡（UI Tabs）**：包含Discord相关选项卡及导航功能。
- **RPC方法（RPC Methods）**：提供与Discord API交互的接口。
- **频道类型（Channel Type）**：支持与Discord频道进行交互。
- **配置模式（Config Schema）**：支持配置Discord频道的相关参数。

## RPC方法（RPC Methods）

| 方法 | 描述 |
|--------|-------------|
| `discord.status` | 获取机器人连接状态和用户信息。 |
| `discord.health` | 进行全面的机器人健康检查。 |
| `discordguilds` | 列出已连接的Discord服务器。 |
| `discord.guild` | 获取服务器的详细信息。 |
| `discordchannels` | 列出服务器中的频道。 |
| `discord.invite` | 生成机器人邀请链接。 |
| `discord.testToken` | 验证令牌的有效性（不保存令牌）。 |
| `discord.setToken` | 存储和激活机器人令牌。 |
| `discord.permissions` | 检查机器人的权限。 |

## 配置选项（Configuration Options）

```yaml
channels:
  discord:
    # Required
    botToken: "YOUR_BOT_TOKEN"
    
    # Guild restrictions (optional)
    guilds:
      "SERVER_ID":
        enabled: true
        channels:
          "CHANNEL_ID":
            enabled: true
            requireMention: false
    
    # Global behavior
    requireMention: true        # Require @mention in servers
    dmPolicy: "pairing"         # DM handling: pairing|open|closed
    groupPolicy: "open"         # Server handling: open|mention|closed
    
    # Advanced options
    retryAttempts: 3
    heartbeatInterval: 30000
    reconnectDelay: 5000
```

## 安全特性
- **令牌保护（Token Protection）**：在API响应中不会泄露完整的令牌信息。
- **OpenBao集成（OpenBao Integration）**：使用OpenBao技术安全存储机器人凭证。
- **权限控制（Permission Control）**：仅请求必要的机器人权限。
- **输入验证（Input Validation）**：对所有Discord API请求进行清洗和处理。
- **速率限制（Rate Limiting）**：遵守Discord API的速率限制。
- **HTTPS加密**：确保令牌传输的安全性。

## 健康检查（Health Checks）
自动执行的健康检查包括：
- **令牌有效性（Token Validity）**：验证机器人令牌的有效性。
- **连接状态（Gateway Connection）**：检查与Discord WebSocket的连接状态。
- **消息意图（Message Intent）**：确保已启用所需的消息交互功能。
- **权限验证（Permission Verification）**：检查机器人在频道中的权限。
- **通道访问控制（Channel Access）**：检查读写权限。
- **API速率限制（API Rate Limits）**：监控当前的API使用情况并遵守限制。

## 故障排除（Troubleshooting）

### 常见问题及解决方法

- **“无效令牌”错误（Invalid token）**：确保使用的是机器人令牌（而非用户令牌），确认令牌已完整复制，并尝试在开发者门户中重置令牌。
- **机器人未在频道中响应**：检查是否已启用“消息内容意图”功能，确认机器人具有在频道中发送消息的权限，以及`requireMention`设置是否正确（可以尝试使用@提及）。
- **控制面板无法加载**：确认UI组件已成功安装，检查浏览器控制台是否有错误信息，必要时重启Clawdbot服务。

### 日志分析（Log Analysis）
```bash
# Check Discord connection logs
clawdbot logs | grep discord

# Test token independently
python scripts/test-token.py YOUR_TOKEN
```

## 文件结构（File Structure）
```
discord-connect-hub/
├── SKILL.md                 # This skill guide
├── scripts/
│   ├── test-token.py       # Token validation utility
│   ├── install-plugin.js   # Plugin installation script
│   └── health-check.py     # Diagnostic tool
├── references/
│   ├── discord-api.md      # Discord API documentation
│   ├── bot-setup.md        # Detailed setup guide
│   └── troubleshooting.md  # Extended troubleshooting
└── assets/
    ├── discord-backend.ts   # RPC handler implementation
    ├── discord-views.ts     # UI component templates
    ├── navigation-hooks.js  # Navigation registration
    ├── install-hooks.js     # Installation automation
    └── config-schema.json   # Configuration validation
```

## 插件集成细节（Plugin Integration Details）

### 自动安装流程
1. **环境检测（Detect Environment）**：检查Clawdbot源代码是否可用。
2. **后台安装（Install Backend）**：将RPC处理程序复制到服务器。
3. **注册处理程序（Register Handlers）**：将相关方法注册到服务器。
4. **安装UI组件（Install UI Components）**：复制UI组件和模板。
5. **更新导航结构（Update Navigation）**：在控制面板中添加Discord选项卡。
6. **配置路由（Configure Routes）**：设置Discord选项卡的路由规则。
7. **编译并重启（Build & Restart）**：编译代码更改并重启Clawdbot服务。

### 手动安装方案
如果自动安装失败，该插件提供与原始“discord-connect”插件类似的手动安装指南。

### 兼容性要求
- **Clawdbot**：版本需大于或等于2026.1.0。
- **Node.js**：版本需大于或等于18.0.0。
- **Discord.js**：版本需大于或等于14.0.0。
- **插件架构（Plugin Architecture）**：版本需大于或等于v2.0。

## 相关链接
- [Discord开发者门户（Discord Developer Portal）：[https://discord.com/developers/applications](https://discord.com/developers/applications)
- **机器人权限计算器（Bot Permissions Calculator）：[https://discordapi.com/permissions.html]
- **Clawdbot官方Discord页面（Clawdbot Discord）：[https://discord.com/invite/clawd]
- **ClawHub仓库（ClawHub Repository）：[https://clawdhub.com]