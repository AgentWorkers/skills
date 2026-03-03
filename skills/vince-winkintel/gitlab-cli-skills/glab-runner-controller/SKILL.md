---
name: glab-runner-controller
description: 管理 GitLab 的运行器控制器（runner controllers）和认证令牌（authentication tokens）。可以创建、更新或删除控制器；生成、轮换或撤销令牌。这是一个仅限管理员使用的实验性功能，用于管理运行器控制器的生命周期。该功能会针对运行器控制器、控制器令牌、实验性运行器（experimental runners）以及管理员运行器（admin runners）进行相应的操作。
---
# glab-runner-controller

用于管理 GitLab 运行器控制器及其认证令牌。

## ⚠️ 实验性功能

**状态：** 实验性（仅限管理员使用）
- 该功能可能会在未经通知的情况下失效或被删除
- 使用该功能需自行承担风险
- 需要 GitLab 管理员权限
- 详情请参阅：https://docs.gitlab.com/policy/development_stages_support/

## 功能概述

运行器控制器负责管理您基础设施中的 GitLab 运行器。该工具提供了以下命令：
- 创建和配置运行器控制器
- 管理控制器的生命周期（列出、更新、删除）
- 生成和轮换认证令牌
- 撤销已被泄露的令牌

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
- `disabled` - 控制器存在但处于非活动状态
- `enabled` - 控制器处于活动状态（默认值）
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

**令牌的典型生命周期为：** **创建 → 轮换 → 撤销**，这是最佳安全实践。

#### 1. 创建令牌

```bash
# Create token for controller 42
glab runner-controller token create 42

# Create with description
glab runner-controller token create 42 --description "production"

# Output as JSON (for automation)
glab runner-controller token create 42 --output json
```

**重要提示：** 请立即保存令牌值——该值仅在创建时显示一次。

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
- 令牌被泄露时采取的应对措施
- 员工离职前进行令牌更换

#### 4. 撤销令牌

```bash
# Revoke token 1 (with confirmation)
glab runner-controller token revoke 42 1

# Revoke without confirmation
glab runner-controller token revoke 42 1 --force
```

**何时需要撤销令牌：**
- 令牌被泄露或丢失
- 控制器不再使用
- 不再需要访问相关资源

### 令牌安全最佳实践：
1. **定期轮换令牌**——设置定期轮换机制（例如每 90 天一次）
2. **为令牌添加描述**——记录令牌的用途和所有者
3. **令牌泄露后立即撤销**
4. **切勿将令牌提交到版本控制系统中**
5. **使用 `--output json` 选项进行自动化操作（安全地解析令牌值）**

## 决策树：选择控制器状态

```
Do you need the controller active?
├─ Yes → --state enabled
├─ Testing configuration? → --state dry_run
└─ No (maintenance/setup) → --state disabled
```

## 故障排除

**出现 “Permission denied” 或 “403 Forbidden” 错误：**
- 运行器控制器命令需要 GitLab 管理员权限
- 确保您已以管理员身份登录
- 使用 `glab auth status` 命令确认当前用户身份

**出现 “Runner controller not found” 错误：**
- 使用 `glab runner-controller list` 命令验证控制器是否存在
- 可能是控制器已被删除
- 确认您是否有权访问正确的 GitLab 实例

**令牌创建失败：**
- 确保控制器存在且处于启用状态
- 检查管理员权限
- 检查 GitLab 实例版本（实验性功能可能需要最新版本）

**令牌轮换后旧令牌仍可使用时：**
- 令牌失效可能需要几秒钟才能生效
- 等待 10-30 秒后再次尝试
- 检查控制器状态（禁用的控制器不会强制验证令牌）

**无法删除控制器时：**
- 检查控制器是否仍有正在运行的运行器
- 可能需要先停止相关运行器
- 可以使用 `--force` 选项强制删除（⚠️ 此操作具有破坏性）

**实验性功能不可用时：**
- 查看 GitLab 版本：`glab version`（需要 v1.83.0 或更高版本）
- 检查 GitLab 实例上是否启用了该功能
- 确认 GitLab 实例版本支持运行器控制器

**分页功能无法使用：**
- 默认页面显示 30 个条目
- 使用 `--per-page` 选项调整显示数量（具体数量因实例而异）
- 使用 `--page` 选项浏览结果

## v1.87.0 的新功能：运行器范围子命令

从 v1.87.0 开始，运行器控制器支持 `runner` 范围，用于管理与特定控制器关联的运行器。

### 列出范围内的运行器

```bash
# List all runners managed by controller 42
glab runner-controller runner list 42

# Output as JSON
glab runner-controller runner list 42 --output json

# Paginate
glab runner-controller runner list 42 --page 2 --per-page 50
```

### 将运行器添加到范围内

```bash
# Add runner to controller 42's scope
glab runner-controller runner create 42 --runner-id <runner-id>
```

### 从范围内删除运行器

```bash
# Remove runner from controller 42's scope (with confirmation)
glab runner-controller runner delete 42 <runner-id>

# Remove without confirmation
glab runner-controller runner delete 42 <runner-id> --force
```

**使用场景：** 运行器范围管理允许您明确指定哪些运行器由某个控制器管理，从而在多控制器环境中实现更精细的控制。

## 相关工具

**持续集成/持续部署（CI/CD）与运行器：**
- `glab-ci` —— 查看和管理 CI/CD 流程及作业
- `glab-job` —— 重试、取消作业、查看作业日志
- `glab-runner` —— 管理单个运行器（列出、暂停、删除）—— 该功能自 v1.87.0 开始提供

**仓库管理：**
- `glab-repo` —— 管理仓库（运行器控制器属于实例级别）

**认证：**
- `glab-auth` —— 登录和认证管理

## 命令参考

有关完整的命令语法和所有可用选项，请参阅：
- [references/commands.md](references/commands.md)