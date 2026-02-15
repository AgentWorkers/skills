---
name: create-cli
description: >
  Design command-line interface parameters and UX: arguments, flags, subcommands,
  help text, output formats, error messages, exit codes, prompts, config/env
  precedence, and safe/dry-run behavior. Use when you’re designing a CLI spec
  (before implementation) or refactoring an existing CLI’s surface area for
  consistency, composability, and discoverability.
---

# 创建命令行接口（CLI）

设计命令行接口的界面（语法和行为），以用户为中心，同时便于脚本使用。

## 首先要做的

- 阅读 `agent-scripts/skills/create-cli/references/cli-guidelines.md` 并将其作为默认的指导原则。
- 更详细的指南请参考：https://clig.dev/（如需提出修改建议，请访问：https://github.com/cli-guidelines/cli-guidelines）
- 只提出必要的澄清问题，以便确定接口的具体设计。

## 快速澄清

如果用户不确定，可以先提出问题，然后根据最佳猜测进行默认设置：

- 命令名称及其功能（用一句话描述）。
- 主要使用对象：人类用户还是脚本？
- 输入来源：命令行参数（args）还是标准输入（stdin）；文件还是 URL；敏感信息（secret）是否通过命令行参数传递？
- 输出格式：人类可读的文本、JSON 格式、纯文本（--json）或标准输出（--plain）；以及退出代码。
- 交互性：是否允许提示信息？是否需要使用 `--no-input` 选项来禁用提示？对于具有破坏性操作（如删除文件等），是否需要确认？
- 配置方式：通过命令行参数（flags）、环境变量（env）还是配置文件（config-file）；各种配置方式的优先级是什么？
- 平台/运行时限制：macOS、Linux、Windows；是单个可执行文件还是运行时环境？

## 需要交付的成果

在设计命令行接口时，需要提供一份简洁的规范，以便用户能够根据这些规范进行实现：

- 命令结构图（command tree）和用法概述（USAGE synopsis）。
- 命令行参数/标志（args/flags）的表格（类型、默认值、是否必需、示例）。
- 各个子命令的功能（subcommands）；这些命令是否具有幂等性（idempotence）；执行它们后状态会如何变化。
- 输出规则：输出到标准输出（stdout）还是标准错误输出（stderr）；如何检测终端类型（TTY）；是否支持 `--json`/`--plain` 格式；是否需要 `--quiet`/`--verbose` 选项。
- 错误处理和退出代码的对应关系（常见的错误类型）。
- 安全性规则：如何处理 `--dry-run`、`--force`、`--no-input` 等选项。
- 配置文件的优先级规则（命令行参数 > 环境变量 > 项目配置 > 用户自定义配置 > 系统配置）。
- 如果适用，还需说明如何实现 Shell 完成功能（shell completion）：例如如何安装命令行工具或生成相关脚本。

## 默认约定（除非用户另有要求）

- `-h` 或 `--help` 总是会显示帮助信息，并忽略其他参数。
- `--version` 会将版本信息输出到标准输出（stdout）。
- 主要数据输出到标准输出（stdout），诊断信息或错误信息输出到标准错误输出（stderr）。
- 如果需要机器可读的输出格式，使用 `--json`；如果需要稳定的文本格式，可以使用 `--plain`。
- 仅当标准输入（stdin）是终端（TTY）时才显示提示信息；`--no-input` 选项会禁用提示。
- 对于具有破坏性的操作，需要用户进行交互式确认；非交互式操作则需要使用 `--force` 或 `--confirm=...` 选项。
- 尊重用户设置的 `NO_COLOR` 或 `TERM=dumb` 环境变量；如果用户需要，提供 `--no-color` 选项来禁用颜色显示。
- 当用户按下 Ctrl-C 时，程序应快速退出；进行有限的清理操作；尽可能避免程序崩溃。

## 模板（请复制到你的答案中）

### 命令行接口规范模板

填写以下部分，删除不相关的内容：

1. **名称**：`mycmd`
2. **简要描述**：`...`
3. **用法**：
   - `mycmd [全局参数] [子命令] [参数]`
4. **子命令**：
   - `mycmd init ...`
   - `mycmd run ...`
5. **全局参数**：
   - `-h, --help`
   - `--version`
   - `-q, --quiet` / `-v, --verbose` （请明确指定这些选项的含义）
   - `--json` / `--plain` （如果适用）
6. **输入/输出规则**：
   - 标准输出（stdout）：
   - 标准错误输出（stderr）：
7. **退出代码**：
   - `0` 表示成功
   - `1` 表示一般错误
   - `2` 表示用法错误（解析或验证失败）
   - （仅在特定命令有需要时添加其他退出代码）
8. **环境变量/配置文件**：
   - 环境变量的使用方式；配置文件的路径及优先级：
9. **示例**：
   - …

## 注意事项

- 除非用户特别要求，否则建议推荐使用特定语言的解析库；否则应保持接口的跨语言兼容性。
- 如果请求的是“设计参数”，不要涉及具体的实现细节。