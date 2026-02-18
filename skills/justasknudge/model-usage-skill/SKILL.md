---
name: model-usage
description: 使用 CodexBar CLI 的本地成本统计功能，可以汇总 Codex 或 Claude 模型的使用情况，包括当前（最新的）模型数据或完整的模型成本明细。该功能会在您从 CodexBar 请求模型级别的使用/成本数据时被触发，或者在您需要从 CodexBar 的 JSON 数据中获取可脚本化的模型级汇总信息时被调用。
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "os": ["darwin"],
        "requires": { "bins": ["codexbar"] },
        "install":
          [
            {
              "id": "brew-cask",
              "kind": "brew",
              "cask": "steipete/tap/codexbar",
              "bins": ["codexbar"],
              "label": "Install CodexBar (brew cask)",
            },
          ],
      },
  }
---
# 模型使用说明

## 概述

可以从 CodexBar 的本地成本日志中获取每个模型的使用成本。支持查看“当前模型”（最新的每日记录）或所有模型的使用情况（适用于 Codex 或 Claude）。

**待办事项：** 在 CodexBar 的 Linux CLI 安装路径被记录后，添加相应的使用指南。

## 快速入门

1. 通过 CodexBar CLI 获取成本数据，或直接传递一个 JSON 文件。
2. 使用附带提供的脚本按模型对成本数据进行汇总。

```bash
python {baseDir}/scripts/model_usage.py --provider codex --mode current
python {baseDir}/scripts/model_usage.py --provider codex --mode all
python {baseDir}/scripts/model_usage.py --provider claude --mode all --format json --pretty
```

## 当前模型的逻辑

- 使用 `modelBreakdowns` 中最新的每日记录。
- 选择该记录中成本最高的模型。
- 如果缺少详细成本信息，则回退到 `modelsUsed` 列表中的最后一条记录。
- 如果需要指定特定模型，可以使用 `--model <模型名称>` 参数进行筛选。

## 输入参数

- 默认参数：`codexbar cost --format json --provider <codex|claude>`。
- 数据来源：文件或标准输入（stdin）。

```bash
codexbar cost --provider codex --format json > /tmp/cost.json
python {baseDir}/scripts/model_usage.py --input /tmp/cost.json --mode all
cat /tmp/cost.json | python {baseDir}/scripts/model_usage.py --input - --mode current
```

## 输出格式

- 输出格式可以是文本（默认）或 JSON（使用 `--format json --pretty` 参数）。
- 输出结果仅包含每个模型的成本信息；在 CodexBar 的输出中，令牌（tokens）不会按模型进行区分。

## 参考资料

- 详细了解 CLI 参数和成本数据字段的格式，请参阅 `references/codexbar-cli.md` 文件。