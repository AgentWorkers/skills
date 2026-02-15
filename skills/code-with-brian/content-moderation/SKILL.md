---
name: content-moderation
description: 使用 Vettly 的内容审核 API（通过 MCP 服务器），对文本、图片和视频进行审核。
metadata.openclaw: {"requires": {"env": ["VETTLY_API_KEY"], "bins": ["npx"]}}
---

# 内容审核

使用 Vettly 的人工智能驱动的内容审核 API 来审核用户生成的内容。该技能通过 `@vettly/mcp` MCP 服务器，根据可配置的审核策略对文本、图片和视频进行检测，并生成可审计的审核结果。

## 设置

将 `@vettly/mcp` MCP 服务器添加到您的配置中：

```json
{
  "mcpServers": {
    "vettly": {
      "command": "npx",
      "args": ["-y", "@vettly/mcp"],
      "env": {
        "VETTLY_API_KEY": "your-api-key"
      }
    }
  }
}
```

在 [vettly.dev](https://vettly.dev) 获取 API 密钥。

## 可用工具

### `moderate_content`

根据 Vettly 的审核策略检查文本、图片或视频内容。返回包含类别评分、采取的措施、使用的服务提供商、处理延迟和费用的审核结果。

**参数：**
- `content`（必填）- 需要审核的内容（文本字符串，或图片/视频的 URL）
- `policyId`（必填）- 用于审核的策略 ID
- `contentType`（可选，默认：`text`）- 内容类型：`text`、`image` 或 `video`

### `validate_policy`

验证 Vettly 的策略 YAML 文件（不保存文件）。返回验证结果，包括任何语法或配置错误。在部署策略之前使用此功能进行测试。

**参数：**
- `yamlContent`（必填）- 需要验证的 YAML 策略内容

### `list_policies`

列出您 Vettly 账户中所有可用的审核策略。无需参数。在审核内容之前，可以使用此功能查找可用的策略 ID。

### `get_usage_stats`

获取您 Vettly 账户的使用统计信息，包括请求次数、费用和审核结果。

**参数：**
- `days`（可选，默认：`30`）- 统计的时间范围（1-365 天）

### `get_recent_decisions`

获取最近的审核决策，支持按结果、内容类型或策略进行筛选。

**参数：**
- `limit`（可选，默认：`10`）- 返回的决策数量（1-50）
- `flagged`（可选）- 筛选条件：仅显示被标记的内容（`true`）或安全的内容（`false`）
- `policyId`（可选）- 按特定策略 ID 进行筛选
- `contentType`（可选）- 按内容类型进行筛选：`text`、`image` 或 `video`

## 使用场景

- 在发布之前审核用户生成的内容（评论、帖子、上传文件）
- 在开发过程中测试和验证审核策略的 YAML 配置
- 审计最近的审核决策，以查看被标记的内容
- 监控账户的审核费用和使用情况
- 比较不同策略的审核结果

## 示例

### 审核用户评论

```
Moderate this user comment for my community forum policy:
"I hate this product, it's the worst thing I've ever used and the developers should be ashamed"
```

调用 `list_policies` 查找可用的策略，然后使用相应的策略 ID 调用 `moderate_content` 并获取审核结果。

### 在部署前验证策略

```
Validate this moderation policy YAML:

categories:
  - name: toxicity
    threshold: 0.8
    action: flag
  - name: spam
    threshold: 0.6
    action: block
```

调用 `validate_policy` 并报告任何语法或配置错误。

### 查看最近被标记的内容

```
Show me all flagged content from the last week
```

调用 `get_recent_decisions` 并设置 `flagged: true` 以获取最近被标记的审核决策。

## 提示

- 如果不知道使用哪个策略 ID，请先调用 `list_policies`
- 在将策略部署到生产环境之前，使用 `validate_policy` 进行测试
- 使用 `get_usage_stats` 监控费用并发现异常增长
- 通过 `contentType` 或 `policyId` 筛选 `get_recent_decisions` 的结果
- 对于图片和视频的审核，请传递内容 URL 而不是原始数据