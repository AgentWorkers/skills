---
name: glab-runner-controller
description: 管理 GitLab 的运行器控制器（runner controllers）和认证令牌（authentication tokens）。可以创建、更新或删除控制器；生成、轮换或撤销令牌。该功能为管理员专用，用于管理运行器控制器的生命周期。适用于运行器控制器、控制器令牌、实验性运行器（experimental runner）以及管理员运行器（admin runner）的相关操作。
---

# glab-runner-controller

用于管理 GitLab 运行器控制器及其认证令牌。

## ⚠️ 实验性功能

**状态：** 实验性（仅限管理员使用）
- 该功能可能存在故障或被删除，恕不另行通知
- 使用该功能需自行承担风险
- 需要 GitLab 管理员权限
- 详情请参阅：https://docs.gitlab.com/policy/development_stages_support/

## 功能概述

运行器控制器负责管理您基础设施中的 GitLab 运行器。此工具提供了以下命令：
- 创建和配置运行器控制器
- 管理控制器的生命周期（列出、更新、删除）
- 生成和轮换认证令牌
- 撤销被泄露的令牌

## 常见工作流程

### 创建运行器控制器

```bash
# Create with default settings
glab runner-controller create

# Create with description
glab runner-controller create --description "Production runners"

# Create enabled controller
glab runner-controller create --description "Prod" --state enabled
```

**状态：**
- `disabled` - 控制器存在但处于禁用状态
- `enabled` - 控制器处于启用状态（默认值）
- `dry_run` - 测试模式（不执行实际运行）

### 列出和查看控制器

```bash
# List all controllers
glab runner-controller list

# List with pagination
glab runner-controller list --page 2 --per-page 50

# Output as JSON
glab runner-controller list --output json
```

### 更新控制器

```bash
# Update description
glab runner-controller update 42 --description "Updated name"

# Change state
glab runner-controller update 42 --state disabled

# Update both
glab runner-controller update 42 --description "Prod" --state enabled
```

### 删除控制器

```bash
# Delete with confirmation prompt
glab runner-controller delete 42

# Delete without confirmation
glab runner-controller delete 42 --force
```

## 令牌管理流程

**令牌的典型生命周期为：** **创建 → 轮换 → 撤销**，以遵循安全最佳实践。

#### 1. 创建令牌

```bash
# Create token for controller 42
glab runner-controller token create 42

# Create with description
glab runner-controller token create 42 --description "production"

# Output as JSON (for automation)
glab runner-controller token create 42 --output json
```

**注意：** 请立即保存令牌值——该值仅在创建时显示一次。

#### 2. 列出令牌

```bash
# List all tokens for controller 42
glab runner-controller token list 42

# List as JSON
glab runner-controller token list 42 --output json

# Paginate
glab runner-controller token list 42 --page 1 --per-page 20
```

#### 3. 轮换令牌

轮换操作会生成新的令牌并使旧令牌失效。

```bash
# Rotate token 1 (with confirmation)
glab runner-controller token rotate 42 1

# Rotate without confirmation
glab runner-controller token rotate 42 1 --force

# Rotate and output as JSON
glab runner-controller token rotate 42 1 --force --output json
```

**使用场景：**
- 定期轮换令牌（符合安全政策）
- 令牌被泄露时的处理
- 员工离职前的令牌更新

#### 4. 撤销令牌

```bash
# Revoke token 1 (with confirmation)
glab runner-controller token revoke 42 1

# Revoke without confirmation
glab runner-controller token revoke 42 1 --force
```

**何时撤销令牌：**
- 令牌被泄露或损坏
- 控制器不再使用
- 无需再使用该令牌的访问权限

### 令牌安全最佳实践：
1. **定期轮换令牌**——设置定期轮换计划（例如，每 90 天一次）
2. **为令牌添加描述**——记录令牌的用途和所有者
3. **令牌被泄露后立即撤销**
4. **切勿将令牌提交到版本控制系统中**
5. **使用 `--output json` 选项进行自动化操作（安全地解析令牌值）**

## 控制器状态选择决策树

```
Do you need the controller active?
├─ Yes → --state enabled
├─ Testing configuration? → --state dry_run
└─ No (maintenance/setup) → --state disabled
```

## 故障排除

- **出现 “Permission denied” 或 “403 Forbidden” 错误：**
  - 运行器控制器命令需要 GitLab 管理员权限
  - 确认您已以管理员身份登录
  - 使用 `glab auth status` 命令检查当前用户身份

- **出现 “Runner controller not found” 错误：**
  - 使用 `glab runner-controller list` 命令验证控制器是否存在
  - 可能是控制器已被删除
  - 确认您是否有权访问正确的 GitLab 实例

- **令牌创建失败：**
  - 确保控制器存在且处于启用状态
  - 检查是否具有管理员权限
  - 检查 GitLab 实例版本（实验性功能可能需要最新版本）

- **令牌轮换后旧令牌仍可使用时：**
  - 令牌失效可能需要几秒钟才能生效
  - 等待 10-30 秒后重新尝试
  - 检查控制器状态（禁用的控制器不会强制验证令牌）

- **无法删除控制器时：**
  - 检查控制器是否仍有正在运行的运行器
  - 可能需要先停止相关运行器
  - 可以使用 `--force` 选项强制删除（⚠️ 此操作具有破坏性）

- **实验性功能不可用时：**
  - 查看 GitLab 版本：`glab version`（需要 v1.83.0 或更高版本）
  - 检查 GitLab 实例上是否启用了该功能
  - 确认 GitLab 实例版本支持运行器控制器

- **分页功能无法使用：**
  - 默认页面显示 30 个条目
  - 使用 `--per-page` 选项调整每页显示数量（具体数量因实例而异）
  - 使用 `--page` 选项浏览结果

## 相关技能

- **持续集成/持续部署 (CI/CD) 与运行器：**
  - `glab-ci`：查看和管理 CI/CD 流程及作业
  - `glab-job`：重试、取消作业以及查看作业日志

- **仓库管理：**
  - `glab-repo`：管理仓库（运行器控制器属于实例级别配置）

- **身份验证：**
  - `glab-auth`：登录和管理用户身份验证

## 命令参考

有关完整的命令语法和所有可用选项，请参阅：
- [references/commands.md](references/commands.md)