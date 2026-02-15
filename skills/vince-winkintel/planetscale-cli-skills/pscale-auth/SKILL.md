---
name: pscale-auth
description: 管理 PlanetScale CLI 的认证功能，包括登录/登出、检查认证状态以及切换账户。适用于首次设置 pscale、排查认证问题、切换 PlanetScale 账户或管理认证会话的场景。该功能会在发生认证相关操作（如登录、登出、认证失败、凭证问题或涉及 PlanetScale 账户时）被触发。
---

# pscale auth

用于管理 PlanetScale 命令行界面（CLI）的认证功能。

## 常用命令

```bash
# Login to PlanetScale (opens browser)
pscale auth login

# Logout
pscale auth logout

# Check current authentication status
pscale org show
```

## 认证方式

### 1. 交互式登录（默认）

会打开浏览器以完成 OAuth 流程：

```bash
pscale auth login
```

**适用场景：** 本地开发、首次设置

### 2. 服务令牌（CI/CD）

适用于自动化环境：

```bash
export PLANETSCALE_SERVICE_TOKEN_ID=<token-id>
export PLANETSCALE_SERVICE_TOKEN=<token>
pscale database list --org <org>
```

**适用场景：** CI/CD 流程、自动化操作、生产环境部署

有关服务令牌的创建方法，请参阅 `pscale-service-token` 技能文档。

## 工作流程

### 首次设置

```bash
# 1. Login
pscale auth login

# 2. Verify authentication
pscale org show

# 3. List databases to confirm access
pscale database list --org <org>
```

### 在不同账户之间切换

```bash
# Logout current account
pscale auth logout

# Login with different account
pscale auth login
```

### CI/CD 认证

```bash
# Create service token (see pscale-service-token)
pscale service-token create --org <org>

# Use in CI/CD environment
export PLANETSCALE_SERVICE_TOKEN_ID=<token-id>
export PLANETSCALE_SERVICE_TOKEN=<token>

# Test authentication
pscale database list --org <org>
```

## 故障排除

### 登录失败 / 浏览器无法打开

**症状：** `pscale auth login` 命令执行失败或无响应

**解决方法：**
- 检查网络连接是否正常
- 确保防火墙允许访问 `https://auth.planetscale.com`
- 尝试使用无头浏览器进行认证（不支持该方式，建议使用服务令牌）
- 在非交互式环境中使用服务令牌进行认证

### 出现 “未经授权” 错误

**症状：** 收到 `401 Unauthorized` 或 `403 Forbidden` 响应

**解决方法：**
- 运行 `pscale auth logout && pscale auth login` 以刷新会话
- 查证用户所属的组织权限：`pscale org show`
- 确认服务令牌未过期（如果使用令牌的话）
- 确保令牌具有所需的操作权限（如数据库读写、分支创建等）

### 拥有多个账户 / 登录错误组织

**症状：** 无法访问目标数据库

**解决方法：**
- 查看当前所属的组织：`pscale org show`
- 切换组织：`pscale org switch <org-name>`
- 列出所有可用组织：`pscale org list`
- 使用正确的账户重新登录

### 服务令牌认证失败

**症状：** 在 CI/CD 环境中服务令牌认证失败

**解决方法：**
- 确认 `PLANETSCALE_SERVICE_TOKEN_ID` 和 `PLANETSCALE_SERVICE_TOKEN` 值已正确设置
- 检查令牌是否已被吊销：`pscale service-token list --org <org>`
- 确保令牌具有所需的操作权限
- 使用 `--debug` 标志查看详细的认证信息

## 相关技能

- **pscale-service-token**：用于创建和管理 CI/CD 服务令牌
- **pscale-org**：用于在不同组织之间切换
- **pscale-database**：用于需要认证的数据库操作

## 参考资料

有关 `pscale auth` 命令的完整参考信息，请参阅 `references/commands.md` 文档。