# n8n_dispatch 代理技能

该技能通过 `mcporter` 将 OpenClaw 与您的现有 n8n-dispatch 服务连接起来。它提供了一个名为 `dispatch` 的命令，用于将用户的请求类型和提示信息转发给已注册的 MCP 服务。

## 工作原理

1. `dispatch` 命令需要两个参数：
   * `requestType`：可以是 `state`、`action` 或 `historical`。
   * `text`：用户的原始提示信息。
2. 该技能会生成一个包含这两个值的 JSON 数据包，并调用 MCP 服务 `n8n_dispatch`。
3. n8n 工作流程接收该数据包，处理请求后返回响应，OpenClaw 会显示该响应。

## 使用方法

```bash
# In your OpenClaw session or a shell
n8n_dispatch dispatch state "What is the living room light status?"
```

该命令的输出示例如下：`请求类型：state；提示信息：客厅的灯光状态是什么？`

## 示例

| 请求类型 | 提示信息 | 命令示例 | 服务返回的结果 |
|--------------|--------|------------------|--------------------------|
| `state` | *“车库门是否打开？”* | `n8n_dispatch dispatch state "Is the garage door open?"` | *“车库门是关闭的”* |
| `action` | *“打开走廊的灯。”* | `n8n_dispatch dispatch action "Turn on the hallway light."` | *“走廊的灯已打开”* |
| `historical` | *“显示昨天的温度。”* | `n8n_dispatch dispatch historical "Show me the temperature for yesterday."` | *昨天的温度：72°F* |

## 配置

将此技能放置在您的工作空间中的 `skills/n8n_dispatch` 目录下，并确保您的 MCP 服务已注册：

```bash
openclaw mcporter add \
  --name "n8n_dispatch" \
  --url "http://your-n8n-host:8080/api"
```

一旦该技能被加载（使用 `openclaw skills load n8n_dispatch` 命令），您就可以从任何 OpenClaw 会话中调用 `dispatch` 命令了。