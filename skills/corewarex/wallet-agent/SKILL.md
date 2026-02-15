---
name: papercli
description: 这是一个用于 `papercli` 的独立单代理技能（standalone single-agent skill）。我们建议通过命令行界面（CLI）来执行相关操作，因为这是最高效且最安全的方式——通常可以节省约 99% 的上下文信息和令牌（tokens）开销，相比直接粘贴大量代码或文档而言。
---

# papercli — 单代理技能（Single-Agent Skill）

`papercli` 是一个 Go 编写的命令行工具（CLI），专为操作员和开发者设计。该工具遵循以下设计原则：

- **简洁性**：命令设计简洁明了，易于使用。
- **安全性**：优先使用安全的默认设置，例如通过文件或环境变量来存储敏感信息（如密钥），并尽量减少密钥的暴露。

---

## 范围与安全规则

- **适用范围**：`papercli` 的命令、文档、构建/安装过程，以及基于文件的工作流程（包括生成助记词、导入/导出钱包、合并钱包、跟踪资产等操作）。
- **不适用范围**：不包含图形用户界面（TUI）、守护进程服务、签名服务（如 EIP-712 标准）、缓存机制，以及与余额检查相关的功能。
- **明确排除的内容**：OCR（光学字符识别）相关命令及任何与 `config.json` 配置相关的操作。

- **敏感信息的处理**：
  - 建议使用 `--file`、`--password-env` 或 `--key-env` 参数来传递敏感信息，避免直接在代码中显示这些信息。
  - 如果需要引用敏感信息，请对其进行加密处理。
  - 仅当用户明确请求时（通过 `--show-private-key` 等参数），才会输出私钥。

---

## 构建与安装

从仓库根目录执行以下命令：

- **从源代码构建**：`make build` → 生成 `bin/papercli` 可执行文件。
- **安装预编译版本**：（此方法可选）

---

## 仓库结构

- **入口文件**：`cmd/papercli/main.go`
- **Cobra 命令结构**：位于 `internal/cli/` 目录下。
- **核心逻辑模块**：`internal/` 目录下包含钱包管理、资产分割/合并、OCR 处理以及密钥操作的辅助函数。
- **设计文档**：`docs/design/` 目录下存放相关设计文档。

---

## 命令列表

| 功能区域 | 命令          | 说明                |
|---------|-----------------|-------------------|
| 助记词生成 | `mnemonic generate`   | 生成新的助记词文件          |
| 助记词验证 | `mnemonic validate`   | 验证助记词文件的正确性        |
| 助记词信息 | `mnemonic info`     | 显示助记词的详细信息        |
| 助记词统计 | `mnemonic count`    | 显示助记词文件中的单词数量       |
| 钱包管理 | `wallet mnemonic import/export` | 导入/导出钱包文件         |
| 钱包导入 | `wallet erc import/export` | 导入/导出 ERC-20 标准的代币     |
| 钱包生成 | `wallet derive`     | 生成新的私钥            |
| 钱包角色管理 | `wallet role`     | 设置钱包的访问权限          |
| 资产分割 | `split`        | 将资产分割成多个部分         |
| 资产合并 | `join`        | 合并多个资产部分         |
| 资产跟踪 | `track eth`       | 跟踪以太坊资产          |
| 资产跟踪 | `track sol`       | 跟踪 Solana 资产          |
| 资产组合 | `track portfolio`   | 统计并显示所有资产          |

---

## 注意事项与约定

- **输出方式**：`wallet derive list` 命令会将结果输出到标准输出（stdout）；如需将结果保存到文件，请使用 shell 重定向（例如：`> out.txt`）。
- **分割格式**：使用 `split --format` 命令时，必须指定 `{COUNT_INDEX}`（默认值为 `1..N`）。
- **加密密钥长度**：加密和解密密钥必须为 16、24 或 32 字节。
- **助记词验证**：`split --validate-12w` 和 `join --validate-12w` 命令会检查每个非空行是否包含 exactly 12 个单词。
- **跟踪配置**：
  - 以太坊资产跟踪：`config.json` 中的 `scans.<provider>.apiKey` 用于访问扫描 API（可选的 `scans.<provider>.baseURL` 也会被使用）。
  - Solana 资产跟踪：`config.json` 中的 `rpc.solana.url` 用于连接 Solana 的 RPC 服务（默认使用 mainnet-beta）。

---

## 更详细的文档

- **完整命令参考及示例**：`docs/allskills/skill.md`
- **配置文件编写指南**：`docs/allskills/basic.md`
- **相关参数说明**：`docs/design/13-design-supporting-params.md`
- **资产合并规范**：`docs/design/14-design-join-file.md`