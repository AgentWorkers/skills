---
name: uxc
description: 使用 UXC 发现并调用远程暴露的接口。当代理或技能需要列出操作、检查操作模式，以及通过一个 CLI 合同执行 OpenAPI、GraphQL、gRPC、MCP 或 JSON-RPC 调用时，可以使用此功能。
metadata:
  short-description: Discover and call remote schema APIs via UXC
---
# UXC 技能

当任务需要调用远程接口，并且该接口能够提供机器可读的元数据时，请使用此技能。

## 使用场景

- 当您需要从其他技能中调用 API 或工具，并希望保持一致的命令行界面（CLI）工作流程时。
- 该接口可以是 OpenAPI、GraphQL、gRPC、MCP 或 JSON-RPC/OpenRPC。
- 您需要获得确定性的、机器可读的输出结果（如 `ok`、`kind`、`data`、`error`）。

请勿将此技能用于纯粹的本地文件操作，因为这些操作不涉及远程接口。

## 先决条件

- `uxc` 已安装，并且位于 `PATH` 环境变量中。
- 对于 gRPC 运行时调用，`grpcurl` 也已安装，并且位于 `PATH` 环境变量中。

### 安装 uxc

请选择以下方法之一进行安装：

**Homebrew（macOS/Linux）：**
```bash
brew tap holon-run/homebrew-tap
brew install uxc
```

**安装脚本（macOS/Linux，运行前请阅读说明）：**
```bash
curl -fsSL https://raw.githubusercontent.com/holon-run/uxc/main/scripts/install.sh -o install-uxc.sh
# Review the script before running it
less install-uxc.sh
bash install-uxc.sh
```

**Cargo：**
```bash
cargo install uxc
```

有关更多安装选项，请参阅 UXC 的 [安装文档](https://github.com/holon-run/uxc#installation)。

## 核心工作流程

1. 查找可用的操作：
   - `uxc <host> -h`
2. 查看特定操作的详细信息：
   - `uxc <host> <operation> -h`
3. 使用结构化输入执行操作：
   - `uxc <host> <operation> key=value`
   - `uxc <host> <operation> '<payload-json>`
4. 将结果解析为 JSON 格式：
   - 成功时：`.ok` 为 `true`，此时可以获取 `.data` 数据。
   - 失败时：`.ok` 为 `false`，此时需要检查 `.error.code` 和 `.error.message`。
5. 为避免混淆，请先使用操作级别的帮助信息：
   - `uxc <host> <operation> -h`
6. 对于需要身份验证的接口，请遵循 OAuth 和绑定流程：
   - 请参阅 [references/oauth-and-binding.md]。

## 包装器技能的链接优先工作流程

包装器技能应默认使用固定的本地链接命令，而不是在每个步骤中都直接调用 `uxc <host> ...`。

1. 在开发技能时指定一个固定的命令名称：
   - 命名规则：`<provider>-mcp-cli`
   - 例如：`notion-mcp-cli`、`context7-mcp-cli`、`deepwiki-mcp-cli`
2. 检查该命令是否存在：
   - `command -v <link_name>`
3. 如果命令不存在，请创建它：
   - `uxc link <link_name> <host>`
   - 对于 schema 位于单独 URL 的 OpenAPI 服务，使用 `uxc link <link_name> <host> --schema-url <schema_url>` 创建链接。
   - 对于需要凭据驱动的 stdio 服务，使用 `uxc link <link_name> <host> --credential <credential_id> --inject-env NAME={{secret}}` 创建链接。
4. 验证链接命令是否有效：
   - `<link_name> -h`
5. 在技能的其余部分中，始终使用该链接命令。

### 命名规则

- 链接的命名由技能开发者决定，而非运行时代理决定。
- 在技能开发或审查过程中解决生态系统中的命名冲突。
- 不要在运行时技能流程中实现动态重命名逻辑。
- 如果运行时检测到无法安全重用的命令冲突，请停止并请求技能维护者的帮助。

### 等价性规则

- `<link_name> <operation> ...` 等价于 `uxc <host> <operation> ...`。
- 如果链接是通过 `--schema-url <schema_url>` 创建的，它等价于 `uxc <host> --schema-url <schema_url> <operation> ...`。
- 如果链接是通过 `--credential <credential_id> --inject-env NAME={{secret}}` 创建的，它等价于 `uxc --auth <credential_id> --inject-env NAME={{secret}} <host> <operation> ...`。
- 调用者可以在运行时通过传递 `--schema-url <other_url>` 显式覆盖已设置的 schema。
- 仅在链接设置不可用时，作为临时替代方案使用 `uxc <host> ...`。

## 输入格式

- 推荐的输入格式（简单的数据结构）：键/值对
  - `uxc <host> <operation> field=value`
- 纯 JSON 格式的参数传递：
  - `uxc <host> <operation> '{"field":"value"}'`
- 请不要通过 `--args` 传递原始 JSON 数据，而是使用参数形式的 JSON。

## 输出格式

其他技能应将该技能视为接口执行层，并仅使用稳定的输出数据结构：
- 成功时的输出字段：`ok`、`kind`、`protocol`、`endpoint`、`operation`、`data`、`meta`
- 失败时的输出字段：`ok`、`error.code`、`error.message`、`meta`

默认输出格式为 JSON。在自动化脚本中请勿使用 `--text` 参数。

## 其他技能的复用规则

- 如果其他技能需要执行远程 API 或工具，请重用此技能，而不是嵌入特定的调用逻辑。
- 包装器技能应采用固定的链接命令（如 `<provider>-mcp-cli`）作为默认的调用方式。
- 上游技能的输入应包括：
  - 目标主机
  - 操作的 ID 或名称
  - 从 `.data` 中提取的必要字段

## 参考文件（按需加载）

- 工作流程详情和调用模式：
  - `references/usage-patterns.md`
- 协议操作命名快速参考：
  - `references/protocol-cheatsheet.md`
- 公共接口的示例和可用性说明：
  - `references/public-endpoints.md`
- 身份验证配置（API 密钥、请求参数、密钥来源）：
  - `references/auth-configuration.md`
- OAuth 和凭据绑定流程：
  - `references/oauth-and-binding.md`
- 错误处理和重试策略：
  - `references/error-handling.md`