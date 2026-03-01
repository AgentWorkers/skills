---
name: translate-cli
description: >
  **用户指南：如何运行和配置 `translate` 命令行工具**
  本指南介绍了如何使用 `translate` 命令行工具（CLI）处理文本、标准输入（stdin）、文件或全局文件路径作为输入源，以及如何选择翻译服务提供商、设置预设参数、自定义提示模板和配置 TOML 文件。适用于用户需要了解命令构建方法、更新配置（`translate config`/`translate presets`）、设置翻译服务提供商、进行模拟验证或排查翻译相关问题的场景。
  **主要内容包括：**
  - 如何使用 `translate` 命令行工具处理不同类型的输入源。
  - 如何选择合适的翻译服务提供商。
  - 如何自定义命令行提示模板。
  - 如何配置 TOML 文件以自定义工具的行为。
  **适用场景：**
  - 当用户需要了解如何构建和使用 `translate` 命令时。
  - 当用户希望更新工具的配置设置时。
  - 当用户需要设置翻译服务提供商时。
  - 当用户希望进行模拟测试以验证翻译功能是否正常工作时。
  - 当用户遇到翻译相关问题时需要寻求帮助时。
  **建议阅读人群：**
  - 所有希望使用 `translate` 命令行工具进行文本翻译的用户。
  - 开发人员或系统管理员，需要了解工具的配置和用法。
  - 技术支持人员，需要解决与工具使用相关的问题。
---
# translate-cli

使用此技能可帮助最终用户运行和配置 `translate` 命令行工具。

`translate` 是一个用于文本、标准输入（stdin）、文件以及 `.xcstrings` 目录的命令行翻译工具。它支持多种翻译服务提供商（OpenAI、Anthropic、Ollama、与 OpenAI 兼容的端点、Apple 提供的服务、DeepL），支持提示语预设和模板覆盖功能，并支持持久化的 TOML 配置。

## 功能

- 为内联文本、标准输入、单文件和多文件工作流程生成正确的 `translate` 命令。
- 在构建命令时，确保选项位于位置参数之前（例如：`translate --to de README.md`）。
- 解释提供商选择、认证信息、模型/基础 URL 的要求以及各提供商的特定限制。
- 使用 `translate config` 和 `config.toml` 配置默认值、提供商端点、网络设置和预设选项。
- 通过预设、内联模板、`@file` 模板和占位符来自定义提示语。
- 说明输出行为（`stdout`、`--output`、`--in-place`、后缀命名规则）、并行处理、试运行功能以及验证错误处理。
- 流式输出：`--stream` 选项用于强制开启流式输出，`--no-stream` 用于强制关闭流式输出；否则将使用默认的 `stream` 设置。

## 基本命令

```bash
translate --text --to fr "Hello world"
translate --to de README.md
translate --provider ollama --text --to en --dry-run "Merhaba dunya"
translate config set defaults.provider anthropic
```

注意：在所有示例和生成的命令中，请始终遵循“选项位于输入参数之前的顺序”。

## 参考资料

- 快速使用示例：`references/quickstart.md`
- 完整的标志和子命令参考：`references/flags-and-subcommands.md`
- TOML 规范和优先级：`references/config-toml.md`
- 提供商规则和环境变量：`referencesproviders-and-env.md`
- 预设选项、提示语模板和占位符：`references/presets-and-prompts.md`
- 运行时行为、警告信息及退出代码：`references/behavior-and-errors.md`