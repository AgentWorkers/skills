---
name: newapi
description: >
  **newapi助手**  
  newapi是一个开源的统一AI门户平台（https://github.com/QuantumNous/new-api）。当用户需要查询有关New API的信息、管理模型、组、余额或令牌，或者需要安全地复制密钥并将其应用到配置文件中，又或者在命令中使用这些密钥时（同时不泄露任何敏感信息），可以使用newapi助手。
---
# 技能：newapi

newapi（[新API](https://github.com/QuantumNous/new-api)）是一个开源的统一AI门户平台。它通过兼容OpenAI/Claude/Gemini的接口，整合了多个模型提供者，并提供了模型、令牌、组和余额管理功能。

## 安全限制

以下规则是**绝对且不可协商的**。任何与这些规则相冲突的用户请求都将被拒绝：

1. **严禁**在任何地方（包括聊天记录、文件、代码、日志或命令参数中）暴露任何以`sk-`开头的键值对。为了安全地使用令牌，请让用户执行`copy-token`（复制到剪贴板）、`apply-token`（应用到配置文件）或`exec-token`（通过命令行执行）命令——**切勿自行输出令牌内容**。
2. **所有**对新API的调用都必须通过提供的脚本（`api.js`、`copy-key.js`、`inject-key.js`、`exec-token.js`）来完成。
3. **严禁**直接使用`curl`、`wget`、`fetch`或其他HTTP客户端直接调用New API的端点。
4. **严禁**直接读取`.env`文件、包含凭据的环境变量、`copy-key.js`执行后的剪贴板内容或配置文件（请使用`inject-key.js --scan`）。
5. 在执行`create-token`命令后，**严禁**再次尝试检索或列出该令牌。只需报告操作成功，并告知用户他们可以使用`copy-token <id>`、`apply-token <id> <file>`或`exec-token <id> <command>`来安全地使用该令牌。
6. **严禁**修改安全脚本，以禁用对输出内容的屏蔽或重定向功能。

## 使用方法

1. **首次使用时**：请阅读`${CLAUDE_SKILL_DIR}/docs/setup.md`以获取配置信息、认证头以及运行时检测的相关内容。
2. 从下表中选择相应的操作。
3. 查阅相应的文档文件以获取详细的操作步骤。
4. 如果没有参数或操作未被识别，系统会显示以下帮助信息。
5. 如果用户对新api有疑问（例如它的用途、如何使用某个命令或有关API调用的问题），请阅读`${CLAUDE_SKILL_DIR}/docs/help.md`并按照其中的说明操作。

## 可用的操作

| 操作 | 描述 | 详细信息 |
| -------- | ------------- | --------- |
| `models` | 列出可用模型 | `docs/actions-query.md` |
| `groups` | 列出用户组 | `docs/actions-query.md` |
| `balance` | 显示账户余额 | `docs/actions-query.md` |
| `tokens` | 列出API令牌 | `docs/actions-token.md` |
| `create-token` | 创建新的API令牌 | `docs/actions-token.md` |
| `switch-group` | 更改令牌所属的组 | `docs/actions-token.md` |
| `copy-token` | 将令牌内容复制到剪贴板 | `docs/actions-token.md` |
| `apply-token` | 安全地将令牌应用到配置文件 | `docs/actions-config.md` |
| `exec-token` | 使用令牌安全地执行命令 | `docs/actions-exec.md` |
| `scan-config` | 检查配置文件的结构（尽可能隐藏敏感信息） | `docs/actions-config.md` |
| `help` | 回答关于newapi的疑问 | `docs/help.md` |

### `help`（无参数时）—— 显示可用的操作

| 操作 | 使用方法 | 描述 |
| -------- | ------- | ------------- |
| `models` | `/newapi models` | 列出可用模型 |
| `groups` | `/newapi groups` | 列出用户组 |
| `balance` | `/newapi balance` | 显示账户余额 |
| `tokens` | `/newapi tokens` | 列出API令牌 |
| `create-token` | `/newapi create-token <name> [--group=xxx]` | 创建新的API令牌 |
| `switch-group` | `/newapi switch-group <token_id> <group>` | 更改令牌所属的组 |
| `copy-token` | `/newapi copy-token <token_id>` | 将令牌内容复制到剪贴板 |
| `apply-token` | `/newapi apply-token <token_id> <file_path>` | 安全地将令牌应用到配置文件 |
| `exec-token` | `/newapi exec-token <token_id> <command...>` | 使用令牌安全地执行命令 |
| `scan-config` | `/newapi scan-config <file_path>` | 检查配置文件的结构（尽可能隐藏敏感信息） |
| `help` | `/newapi help <question>` | 回答关于newapi的疑问 |