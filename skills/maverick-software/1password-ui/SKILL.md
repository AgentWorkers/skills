---
name: 1password-ui
description: OpenClaw仪表板的1Password UI标签页：通过控制界面（Control UI）管理密钥、凭据映射以及认证状态。
version: 1.1.0
author: OpenClaw Community
metadata: {"clawdbot":{"emoji":"🔐","requires":{"clawdbot":">=2026.1.0"},"category":"tools"}}
---

# 1Password UI 扩展

该扩展为 OpenClaw 控制面板中的 **工具** 组添加了一个 **1Password** 选项卡。用户可以通过网页界面浏览密码库、管理技能的凭证映射以及处理身份验证相关操作。

## 主要功能

| 功能        | 说明                                      |
|------------|-----------------------------------------|
| **控制面板选项卡** | 侧边栏中的 “1Password” 选项卡                         |
| **连接状态**   | 显示当前登录账户及使用的连接模式（CLI/Connect）                |
| **登录流程**   | 直接通过 UI 进行身份验证                         |
| **Docker 支持**   | 支持与 1Password Connect 集成，适用于容器环境           |
| **凭证映射**   | 将 1Password 中的凭证信息映射到技能配置中                   |

## 代理安装提示

要安装此扩展，请向您的代理发送以下提示：

```
Install the 1password-ui skill from ClawHub.

The skill is at: ~/clawd/skills/1password-ui/
Follow INSTALL_INSTRUCTIONS.md step by step.

Summary of changes needed:
1. Copy 1password-backend.ts to src/gateway/server-methods/1password.ts
2. Register handlers in server-methods.ts
3. Add "1password" tab to navigation.ts (TAB_GROUPS, Tab type, TAB_PATHS, icon, title, subtitle)
4. Add state variables to app.ts
5. Copy 1password-views.ts to ui/src/ui/views/1password.ts
6. Add view rendering to app-render.ts
7. Add tab loading to app-settings.ts
8. Build and restart: pnpm build && pnpm ui:build && clawdbot gateway restart
```

## 先决条件

### 本地安装（Ubuntu/Windows/macOS）

1. **1Password CLI**（`op`）：
   ```bash
   # macOS/Linux
   brew install 1password-cli
   
   # Or from https://1password.com/downloads/command-line/
   ```

2. 确保 1Password 应用程序已启用 **CLI 集成**：
   - 设置 → 开发者 → “与 1Password CLI 集成”（已勾选）

### Docker 安装

请参阅下面的 [Docker 设置](#docker-setup-1password-connect) 文章。

## 使用方法

### 登录

1. 打开 OpenClaw 控制面板 → **工具** → **1Password**
2. 点击 “使用 1Password 登录”
3. 在 1Password 应用程序的弹出窗口中完成授权（或在终端中运行 `op signin`）
4. 状态栏会显示 “已连接” 以及您的账户信息

### 凭证映射

登录成功后，您可以执行以下操作：

1. 如 Pipedream 等技能可以从 1Password 中读取凭证信息。
2. 凭证映射信息存储在 `~/clawd/config/1password-mappings.json` 文件中。
3. 文件格式：`{ "skillId": { "item": "凭证名称", "vault": "密码库名称", "fields": {...} } }`

### 示例：Pipedream 与 1Password 的集成

```bash
# Store Pipedream credentials in 1Password
op item create --category="API Credential" --title="Pipedream Connect" \
  --vault="Private" \
  "client_id[text]=your_client_id" \
  "client_secret[password]=your_client_secret" \
  "project_id[text]=proj_xxxxx"

# Use in token refresh
PIPEDREAM_1PASSWORD_ITEM="Pipedream Connect" python3 ~/clawd/scripts/pipedream-token-refresh.py
```

## Gateway RPC 方法

| 方法        | 说明                                      |
|------------|-----------------------------------------|
| `1password.status` | 获取 CLI/Connect 的连接状态及登录账户信息           |
| `1password.signin` | 触发登录流程                               |
| `1password.signout` | 退出当前会话                                 |
| `1password.vaults`   | 列出可用的密码库                         |
| `1password.items` | 列出密码库中的所有凭证                         |
| `1password.getItem` | 获取凭证的字段结构（不包含实际值）                   |
| `1password.readSecret` | 读取凭证内容（仅限后端使用）                     |
| `1password.mappings.list` | 获取技能与 1Password 之间的映射关系                   |
| `1password.mappings.set` | 创建或更新凭证映射                         |
| `1password.mappings.delete` | 删除凭证映射                         |
| `1password.mappings.test` | 测试凭证映射是否正常工作                         |

## Docker 设置（1Password Connect）

对于基于 Docker 的 OpenClaw 安装环境，请使用 1Password Connect 代替 CLI。

### 第一步：部署 1Password Connect

```yaml
# docker-compose.yml
services:
  op-connect-api:
    image: 1password/connect-api:latest
    ports:
      - "8080:8080"
    volumes:
      - ./1password-credentials.json:/home/opuser/.op/1password-credentials.json:ro
      - op-data:/home/opuser/.op/data

  op-connect-sync:
    image: 1password/connect-sync:latest
    volumes:
      - ./1password-credentials.json:/home/opuser/.op/1password-credentials.json:ro
      - op-data:/home/opuser/.op/data

volumes:
  op-data:
```

### 第二步：获取凭证信息

1. 访问 [my.1password.com](https://my.1password.com) → “集成” → “Secrets Automation”
2. 创建一个 Connect 服务器
3. 下载 `1password-credentials.json` 文件
4. 生成访问令牌

### 第三步：配置 OpenClaw

```yaml
services:
  clawdbot:
    environment:
      - OP_CONNECT_HOST=http://op-connect-api:8080
      - OP_CONNECT_TOKEN=your-access-token
```

UI 会自动检测当前使用的连接模式（CLI/Connect）。

## 所包含的文件

```
1password-ui/
├── SKILL.md                      # This file
├── INSTALL_INSTRUCTIONS.md       # Step-by-step installation
├── CHANGELOG.md                  # Version history
├── package.json                  # Skill metadata
├── reference/
│   ├── 1password-backend.ts      # Gateway RPC handlers
│   ├── 1password-views.ts        # UI view (Lit template)
│   ├── 1password-settings.ts     # Tab loading logic
│   └── 1password-plugin.ts       # Plugin registration (optional)
└── scripts/
    └── op-helper.py              # CLI/Connect bridge for skills
```

## 安全性考虑

### ✅ 设计上的安全性保障

| 安全方面        | 实现方式                                      |
|----------------|-----------------------------------------|
| **凭证不显示在 UI 中** | `getItem` 和 `items` 方法仅返回字段名称，不显示实际值           |
| **无网络安装脚本**   | 无 `curl` 或 `sh` 脚本等网络安装工具，所有代码均为本地执行       |
| **手动安装**       | 需要手动修改代码，无自动更新机制                   |
| **映射文件权限设置** | `1password-mappings.json` 文件的权限设置为 0600（仅包含文件引用，不含敏感信息） |
| **CLI 认证**     | 支持使用 1Password 应用程序的生物特征认证功能（如可用）           |

### ⚠️ 已记录的风险及应对措施

| 风险        | 应对措施                                      |
|------------|-----------------------------------------|
| **`readSecret` 方法的暴露** | `1password.readSecret` 方法通过 Gateway RPC 提供，这是有意为之（技能需要访问凭证）。安全性依赖于：(1) 1Password 的用户认证机制；(2) Gateway 的访问控制（默认为仅限本地访问）。 |
| **Gateway 的安全性** | 所有 1password.* 方法均为 RPC 调用。如果将 Gateway 暴露到网络中，需采取相应的安全措施。 |
| **Connect 令牌**     | 在 Docker 模式下，`OP_CONNECT_TOKEN` 用于控制对密码库的访问权限。请像保护 API 密钥一样保护该令牌。 |

### 文件安全

```bash
# Recommended permissions for mapping file
chmod 600 ~/clawd/config/1password-mappings.json
```

## 常见问题及解决方法

### “找不到 1Password CLI”
```bash
brew install 1password-cli
# or download from 1password.com/downloads/command-line/
```

### “未登录”
```bash
op signin
op whoami  # verify
```

### 登录失败 / “授权被拒绝”
- 确保已登录 1Password 应用程序。
- 启用 CLI 集成：设置 → 开发者 → “与 1Password CLI 集成”。

### Docker 使用时出现 “连接拒绝” 错误
```bash
docker ps | grep op-connect  # check containers running
```

### Docker 使用时出现 “401 未经授权” 错误
- 确保 `OP_CONNECT_TOKEN` 设置正确。
- 检查令牌是否过期。

## 技术支持

- **ClawHub**：[clawhub.ai/skills/1password-ui](https://clawhub.ai/skills/1password-ui)
- **1Password CLI**：[developer.1password.com/docs/cli](https://developer.1password.com/docs/cli)
- **1Password Connect**：[developer.1password.com/docs/connect](https://developer.1password.com/docs/connect)
- **OpenClaw 的 Discord 社区**：[discord.com/invite/clawd](https://discord.com/invite/clawd)

## 更新日志

### v1.1.0 (2025-02-11)
- 完整实现了与控制面板 UI 的集成。
- 支持通过网页界面登录。
- 支持 CLI 和 Connect 模式。
- 引入了凭证映射功能。

### v1.0.0 (2025-02-11)
- 首次发布版本，包含基础功能实现。