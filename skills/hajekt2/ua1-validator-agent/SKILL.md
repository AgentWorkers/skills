---
name: ua1-validator-agent
description: 使用 ua1.dev 或 api.ua1.dev（来自 AI 编码代理，如 OpenClaw、Claude Code、Codex、OpenCode）来验证 PDF 文件是否符合 PDF/UA-1 标准。当需要对这些 PDF 文件进行确定性的可访问性检查、生成简洁的机器可读性评估结果、用于持续集成（CI）流程中的决策判断，或实现结构化的修复流程时，可选用此方法。
---
# UA1 验证器代理技能

使用此技能可以从代理工作流中执行确定性的 PDF/UA-1 验证。

## 端点

- 状态检查：`GET https://api.ua1.dev/api/health`
- 验证：`POST https://api.ua1.dev/api/validate`
- 紧凑模式：`POST https://api.ua1.dev/api/validate?format=compact`
- 统计数据：`GET https://api.ua1.dev/api/metrics`

## 必需的请求格式

发送包含 `file` 字段的 multipart form-data 数据。

- 支持的文件格式：`.pdf`

- 常见的响应状态码：
  - `200`：验证成功
  - `415`：不支持的文件类型
  - `413`：文件过大
  - `429`：超出请求速率限制

## 代理的最小工作流程

1. 在批量验证之前先执行一次状态检查。
2. 使用紧凑模式验证每个 PDF 文件，以进行确定性解析。
3. 如果验证结果为“失败”，记录问题并按 `rule_id` 分组。
4. 生成按问题出现频率排序的修复计划。
5. 修复问题后重新执行验证，并比较问题数量。

## 脚本使用方法

运行以下脚本：

```bash
bash scripts/validate_pdf.sh /absolute/or/relative/path/to/file.pdf
```

可选环境变量：

- `UA1_API_BASE`（默认值：`https://api.ua1.dev`）
- `UA1_FORMAT`（默认值为 `compact`；设置为 `full` 以获取完整的数据内容）

## 持续集成（CI）门控规则

将验证结果为“失败”的情况视为质量检查失败。

- 如果验证结果为“通过”，则退出代码 `0`；
- 如果验证结果为“失败”，则退出代码 `2`；
- 如果出现传输或 API 错误，则退出代码 `1`。

请在持续集成流程中直接使用该脚本的退出代码。