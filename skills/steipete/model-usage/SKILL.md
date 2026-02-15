---
name: model-usage
description: 使用 CodexBar CLI 的本地成本统计功能，可以汇总 Codex 或 Claude 模型的使用情况，包括当前（最新的）模型数据或完整的模型成本明细。该功能会在需要从 CodexBar 获取模型级别的使用/成本数据时被触发，或者在需要从 CodexBar 的 JSON 数据中提取可脚本化的模型级汇总信息时被调用。
metadata: {"clawdbot":{"emoji":"📊","os":["darwin"],"requires":{"bins":["codexbar"]},"install":[{"id":"brew-cask","kind":"brew","cask":"steipete/tap/codexbar","bins":["codexbar"],"label":"Install CodexBar (brew cask)"}]}}
---

# 模型使用说明

## 概述
可以从 CodexBar 的本地成本日志中获取每个模型的使用成本。支持查看“当前模型”（最新的每日记录）或所有模型的使用情况（适用于 Codex 或 Claude）。

**待办事项：** 在 CodexBar 的 Linux CLI 安装路径文档准备好后，添加相应的 Linux CLI 使用指南。

## 快速入门
1) 通过 CodexBar CLI 获取成本数据（以 JSON 格式）；或者直接提供一个 JSON 文件。
2) 使用附带提供的脚本按模型对成本数据进行汇总。

```bash
python {baseDir}/scripts/model_usage.py --provider codex --mode current
python {baseDir}/scripts/model_usage.py --provider codex --mode all
python {baseDir}/scripts/model_usage.py --provider claude --mode all --format json --pretty
```

## 当前模型的处理逻辑
- 使用 `modelBreakdowns` 中最新的每日记录。
- 选择该记录中成本最高的模型。
- 如果缺少详细成本数据，将回退到 `modelsUsed` 列表中的最后一条记录。
- 如果需要指定特定模型，可以使用 `--model <模型名称>` 参数进行覆盖。

## 输入参数
- 默认参数：`codexbar cost --format json --provider <codex|claude>`。

## 输出格式
- 可以选择文本格式（默认）或 JSON 格式（使用 `--format json --pretty`）。
- 输出结果仅包含每个模型的成本信息；在 CodexBar 的输出中，令牌（tokens）不会按模型进行区分。

## 参考资料
- 请参阅 `references/codexbar-cli.md` 以了解 CLI 参数和成本数据 JSON 字段的详细信息。