---
name: knods
description: 使用 OpenClaw Gateway 的轮询协议来构建和修改 Knods 的视觉 AI 工作流程。当 Knods 发送包含 `messageId`、`message`、`history` 等字段的轮询数据包时，需要将这些响应以增量数据块（delta chunks）的形式流式传输回来，并在辅助文本中包含可选的 `[KNODS_ACTION]` JSON 块。该方案还包括一个用于持续轮询的封装好的运行时环境（runtime）和安装程序。
metadata:
  openclaw:
    emoji: "🔌"
    homepage: "https://github.com/alesys/openclaw-skill-knods"
    os: ["linux"]
    requires:
      bins: ["python3", "bash", "openclaw", "systemctl"]
      env: ["KNODS_BASE_URL"]
---
# Knods

## 概述

Knods 负责处理聊天中的请求，这些请求会在可视化画布上创建新的节点或对现有节点进行编辑。它解析来自 Knods 的轮询数据包，生成助手文本，并在需要更新画布内容时插入 `[KNODS_ACTION]...[/KNODS_ACTION]` 格式的代码块。

## 工作流程

1. 解析传入的数据包内容：
   - 将 `message` 视为主请求内容。
   - 使用 `history` 来保持对话的连贯性。
   - 在对话的第一个环节中，`message` 中通常会包含描述节点类型和操作规则的上下文信息。
   - 使用 `messageId` 将所有响应内容与对应的请求关联起来。

2. 决定是否需要生成画布操作代码块：
   - 使用 `addNode` 来添加单个节点。
   - 使用 `addFlow` 来创建多节点工作流或处理需要连接边的请求。
   - 如果用户只是提问，只需返回普通文本，无需生成操作代码块。

3. 构建操作相关的 JSON 数据：
   - 每个操作都应按照以下格式编写：
     - `[KNODS_ACTION]{"action":"addNode",...}[/KNODS_ACTION]`
     - `[KNODS_ACTION]{"action":"addFlow",...}[/KNODS_ACTION]`
   - 对于 `addFlow` 操作，确保每个边的 `source` 和 `target` 都引用现有的节点 ID。
   - 每个工作流都必须以一个 `Output` 节点结束。
   - 切勿直接连接两个生成节点；必须通过 `Output` 节点或适当的输入/输出结构进行连接。
   - 使用稳定的节点 ID（例如 `input_1`、`image_1`、`output_1`），以便后续编辑更加方便。
   - 避免在操作 JSON 中使用未知的键。

4. 将响应内容发送回 Knods：
   - 将助手文本分块发送到 `/respond` 端点，每个块都应使用相同的 `messageId`。
   - 完成操作后，发送 `{"messageId":"...","done":true}`。
   - 确保第一个响应块尽快发送，以避免超时。

## 输出规则

- 返回普通的助手文本；不要将整个回复内容封装在自定义的格式中。
- 仅在需要更新画布内容时，才在文本中直接插入 `[KNODS ACTION]...[/KNODS_ACTION]` 格式的代码块。
- 不要在面向用户的文本中提及内部的轮询 URL 或令牌信息。
- 保持操作 JSON 的格式正确且简洁。

## 工作流设计原则

- 构建满足请求的最小化工作流。
- 如果对话中提供了节点类型的上下文信息，优先使用这些信息。
- 当上下文缺失时，使用默认的节点类型列表：`ChatGPT`、`Claude`、`Gemini`、`GPTImage`、`FluxImage`、`FalAIImage`、`Veo31Video`、`WanAnimate`、`TextInput`、`ImagePanel`、`Dictation`、`Output`。
- 仅当用户意图明确需要参数时，才添加 `initialData`。
- 如果一个生成节点需要向另一个生成节点传递数据，必须通过 `Output` 节点进行传递。
- 当节点类型未知时，应做出最佳猜测并明确说明所依据的假设。

## 网关行为限制

- 轮询间隔：大约 1-2 秒。
- 消息超时时间：大约 2 分钟。
- 在同一轮对话中，所有响应内容都必须使用相同的 `messageId`。
- 网关认证使用 `gw_...` 令牌（通过查询参数 `token` 进行）；在此过程中不需要使用 Supabase JWT。

## 运行时操作

在运行持续轮询服务/进程时：

- 支持两种配置方式：
  - `KNODS_BASE_URL` 已经包含了 `/updates?token=...`；
  - 或者 `KNODS_BASE_URL` 指向连接端点，令牌需要单独提供（通过 `KNODS_GATEWAY_TOKEN`）。
- 从与 `/updates` 相同的连接路径中获取 `/respond` 端点。
- 记录处理的 `messageId` 值和传输错误信息，以便调试。

### 所需的运行时组件

此技能提供了运行时所需的组件和安装程序：

- `scripts/knods_iris_bridge.py`
- `scripts/install_local.sh`

从技能文件夹中安装/部署：

```bash
bash /home/rolf/.openclaw/skills/knods/scripts/install_local.sh
```

安装程序会部署以下文件：
- `~/.openclaw/scripts/knods_iris_bridge.py`
- `~/.config/systemd/user/knods-iris-bridge.service`

然后执行以下命令：
- `systemctl --user daemon-reload`
- `systemctl --user enable --now knods-iris-bridge.service`

### 环境变量

在 `~/.openclaw/.env` 中设置以下环境变量：

- 必需的变量：
  - `KNODS_BASE_URL`
  - 如果 `KNODS_BASE_URL` 中没有包含 `?token=...`，则需要设置：
    - `KNODS_GATEWAY_TOKEN`
- 可选的变量：
  - `OPENCLAW_AGENT_ID`（默认值：`iris`
  - `OPENCLAW_BIN`（默认值：`PATH` 中的 `openclaw`）

### 服务操作

- 查看服务状态：
  - `systemctl --user status knods-iris-bridge.service`
- 重启服务：
  - `systemctl --user restart knods-iris-bridge.service`
- 查看日志：
  - `journalctl --user -u knods-iris-bridge.service -f`

### 配置变更处理

在更改网关 URL 或令牌环境变量后，需要重启正在运行的服务进程以加载新的配置：

- 通用服务重启命令：
  - `systemctl --user restart <knods-bridge-service>`
- 通用进程重启步骤：
  - 停止旧进程
  - 使用更新后的环境变量重新启动轮询程序

请注意：环境变量的更改不会自动生效，需要手动重启服务才能应用新的配置。

## 参考资料

请参阅 `references/protocol.md`，以获取标准的轮询端点、数据包格式和操作示例。