---
name: provider-sync
description: 将某个提供者的模型及相关字段审查并同步到本地的 OpenClaw 配置文件中。该功能可用于获取上游提供者的元数据、映射和规范模型条目、预览差异，并在明确确认后应用最小范围的配置更新（同时保留备份）。
license: MIT
spdx: MIT
---
# 提供商数据同步

将上游提供商的元数据同步到本地 OpenClaw 配置文件中，并采用“先审查后执行”的工作流程。

## 功能说明

- 从上游获取提供商的元数据或模型列表
- 将模型数据映射并转换为 OpenClaw 可识别的格式
- 在实际写入数据之前预览所有更改内容
- 对目标提供商的配置文件进行最小范围的修改，并创建备份文件

## 输入参数与访问权限

- 该工具会读取本地的 OpenClaw 配置文件，并在用户确认后应用相应的更改。
- 在执行写入操作之前，务必确认目标配置文件的路径。
- 常见的配置文件路径为 `/root/.openclaw/openclaw.json`，但请勿盲目假设该路径始终有效。
- 对于受保护的上游服务端点，可能需要使用特定的请求头（如 `Authorization`）进行身份验证。
- 用于身份验证的凭据应来自用户或已配置的本地环境；切勿在日志或摘要中显示敏感信息。

## 安全工作流程

1. 确认目标配置文件的路径和对应的提供商 ID。
2. 从上游获取数据并读取映射文件。
3. 首先执行 `--check-only` 或 `--dry-run` 命令进行测试。
4. 显示所有被修改的文件路径、模型之间的差异以及 API 兼容性信息。
5. 仅在用户明确确认后，才执行实际的写入操作。
6. 将重启或运行时应用更改视为独立的确认步骤。

## 主脚本

使用方式：`scripts/provider_sync.py`

**示例：**

```bash
python3 scripts/provider_sync.py \
  --config /root/.openclaw/openclaw.json \
  --provider-id cliplus \
  --endpoint https://api.example.com/v1/models \
  --mapping-file references/mapping.openai-models.json \
  --normalize-models \
  --preserve-existing-model-fields \
  --probe-api-modes openai-responses,openai-completions \
  --dry-run
```

## 有用的命令参数

- `--config` — 目标配置文件的路径
- `--check-only` — 仅验证数据，不进行写入操作
- `--dry-run` — 预览计划中的更改内容
- `--normalize-models` — 将上游模型数据转换为 OpenClaw 可识别的格式
- `--normalize-profile gemini` — 适用于 Gemini 平台的特定数据格式化规则
- `--preserve-existing-model-fields` — 在可能的情况下保留本地模型中的字段信息
- `--include-model` / `--exclude-model` — 确定需要处理的模型范围
- `--output json` — 以机器可读的格式输出摘要信息

## 参考文档

- `references/examples.md`
- `references/provider-patterns.md`
- `references/field-normalization.md`
- `references/gemini.md`
- `references/safety-rules.md`
- `references/mapping.example.json`

## 安全注意事项

- 建议遵循“先检查/预览 → 确认 → 执行”的安全流程。
- 除非明确要求，否则不要在 `modelsproviders.<provider-id>` 目录之外写入任何数据。
- 默认情况下，系统不会自动重启或应用运行时的更改。
- 在执行写入操作时请务必创建备份；如果写入失败，请记录详细的错误信息。