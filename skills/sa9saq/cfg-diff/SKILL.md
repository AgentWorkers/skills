---
description: 比较配置文件，突出显示差异，并为 YAML、JSON、TOML 和 INI 格式提供合并策略。
---

# 配置文件差异比较与合并工具

本工具用于比较和合并配置文件。

## 功能

- **差异比较**：支持并排显示或统一格式的配置文件差异
- **语义差异分析**：能够理解 YAML/JSON/TOML 文件的结构（而不仅仅是文本内容）
- **合并建议**：针对冲突的配置文件提供合并方案
- **文件格式支持**：YAML、JSON、TOML、INI、环境变量文件（.env）

## 使用方法

您可以向工具发出如下指令：
- “比较 config.yml 和 config.production.yml 文件”
- “这两个 JSON 配置文件之间有哪些变化？”
- “帮我合并这两个 TOML 文件”
- “显示 .env.local 和 .env.production 文件之间的差异”

## 工作原理

该工具基于 `diff`、`jq`、`yq` 等工具以及文本分析技术来实现功能。

## 所需环境

- 已安装 `diff` 工具
- 可选：为处理 JSON 文件需安装 `jq`，为处理 YAML 文件需安装 `yq`
- 无需使用 API 密钥

```bash
diff --unified config-a.yml config-b.yml
jq -S . a.json > /tmp/a.json && jq -S . b.json > /tmp/b.json && diff /tmp/a.json /tmp/b.json
```