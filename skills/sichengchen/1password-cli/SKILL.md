# 1Password CLI for Agents

此功能允许代理使用 1Password CLI (`op`) 和服务账户安全地访问和管理密码等敏感信息。它提供了用于读取、写入和管理专用密码库中数据的命令。

## 先决条件

1. **安装 1Password CLI：**
    - macOS: `brew install --cask 1password-cli`
    - Linux/Windows: 请参阅[官方文档](https://developer.1password.com/docs/cli/get-started)。
2. **创建服务账户：**
    - 访问[1Password 开发者门户](https://developer.1password.com/)。
    - 创建一个服务账户，并为其授予对特定密码库（例如“Agent Vault”）的访问权限。
    - 复制服务账户令牌。
3. **设置环境变量：**
    - 在环境变量中设置 `OP_SERVICE_ACCOUNT_TOKEN`（例如，在 `.env` 文件中或通过 shell 进行设置）。
    - 对于 OpenClaw，可以在 `.env` 文件中添加 `OP_SERVICE_ACCOUNT_TOKEN=...`。

## 使用方法

所有命令都需要设置 `OP_SERVICE_ACCOUNT_TOKEN`。

### 1. 验证身份

验证服务账户是否正常工作：

```bash
op whoami
```

### 2. 列出密码库

列出服务账户可以访问的密码库：

```bash
op vault list
```

### 3. 读取数据

获取数据的详细信息（JSON 格式更便于解析）：

```bash
op item get "Item Name" --vault "Vault Name" --format json
```

或获取特定字段（例如密码）：

```bash
op read "op://Vault Name/Item Name/password"
```

### 4. 创建数据

创建登录凭据：

```bash
op item create --category login --title "My Service" --url "https://example.com" --vault "Vault Name" username="myuser" password="mypassword"
```

创建安全笔记：

```bash
op item create --category "Secure Note" --title "API Key" --vault "Vault Name" notes="my-secret-key"
```

### 5. 修改数据

更新密码：

```bash
op item edit "Item Name" password="newpassword" --vault "Vault Name"
```

### 6. 删除数据

```bash
op item delete "Item Name" --vault "Vault Name"
```

## 给代理的建议

- **始终使用 JSON 格式输出：** 在 `op` 命令中添加 `--format json` 选项，以便输出结构化的数据，便于后续处理。
- **安全性：** 除非明确要求，否则切勿将 `OP_SERVICE_ACCOUNT_TOKEN` 或获取到的敏感信息打印到控制台。
- **密码库：** 如果有多个密码库，请使用 `--vault` 标志来指定目标密码库，以避免混淆。
- **速率限制：** 服务账户有使用频率限制。如果可能，请缓存结果或使用重试机制。

## 故障排除

- **“您当前未登录”：** 确保 `OP_SERVICE_ACCOUNT_TOKEN` 设置正确。
- **“账户未被授权”：** 检查服务账户是否具有对特定密码库及相应操作（读取/写入）的权限。