---
name: ecovacs-mcp
description: 通过官方的 Ecovacs MCP 服务器来控制 Ecovacs 系列的机器人吸尘器（DEEBOT 系列）：可以启动/停止/暂停清洁功能，将机器人送回充电站，查看电池电量和清洁状态，以及列出所有连接的设备。无论用户提到的是他们的机器人吸尘器、DEEBOT、Ecovacs、扫地机器人，还是想要进行吸尘、拖地、打扫房间、检查吸尘器是否正在充电，或者将其送回充电站——即使他们没有明确使用“Ecovacs”这个词，都可以使用此功能。
user-invocable: false
metadata: {"clawdbot":{"emoji":"🤖","requires":{"anyBins":["uvx","python3"],"env":["ECO_API_KEY"]},"primaryEnv":"ECO_API_KEY"}}
---
# Ecovacs机器人吸尘器控制

您可以通过[官方的Ecovacs MCP服务器](https://github.com/ecovacs-ai/ecovacs-mcp)来控制Ecovacs机器人吸尘器。这是首个针对机器人清洁设备的官方MCP集成方案。

## 前提条件

- 从[open.ecovacs.com](https://open.ecovacs.com)获取的**API密钥**（`ECO_API_KEY`）
- 推荐使用`uvx`库，或安装了`ecovacs-robot-mcp`的`python3`环境
- 机器人已在Ecovacs移动应用中注册，并绑定到同一账户

## MCP服务器配置

在您的设置中，MCP服务器的配置应如下所示：

```json
{
  "ecovacs_mcp": {
    "command": "uvx",
    "args": ["--from", "ecovacs-robot-mcp", "python", "-m", "ecovacs_robot_mcp"],
    "env": {
      "ECO_API_KEY": "YOUR_API_KEY",
      "ECO_API_URL": "https://open.ecovacs.com"
    }
  }
}
```

**区域端点：**
- 国际地区：`https://open.ecovacs.com`
- 中国大陆：`https://open.ecovacs.cn`

## MCP工具参考

该服务器提供了四种工具。所有设备操作都使用`nickname`参数，该参数支持**模糊匹配**——您不需要输入设备的精确名称。

### get_device_list
列出绑定到该账户的所有机器人。无需参数。**请始终首先调用此函数**，以获取可用的机器人及其昵称。

### start_cleaning
控制清洁操作。

| 参数 | 值 | 描述 |
|-----------|--------|-------------|
| `nickname` | 字符串 | 机器人名称（支持模糊匹配） |
| `act` | `s` | 开始清洁 |
| `act` | `p` | 暂停清洁 |
| `act` | `r` | 恢复清洁 |
| `act` | `h` | 停止清洁 |

### control_recharging
控制机器人的充电操作。

| 参数 | 值 | 描述 |
|-----------|--------|-------------|
| `nickname` | 字符串 | 机器人名称（支持模糊匹配） |
| `act` | `go-start` | 返回充电站 |
| `act` | `stopGo` | 取消返回充电站的动作 |

### query_working_status
返回机器人的实时状态。除了`nickname`参数外，无需其他输入。返回三个状态字段：

- **`cleanSt`** — 清洁状态（扫地、拖地、暂停、空闲、地图绘制）
- **`chargeSt`** — 充电状态（返回充电站、对接、充电、空闲）
- **`stationSt`** — 充电站状态（清洗拖把、干燥、收集灰尘、空闲）

## 操作指南

1. **始终先列出设备** — 在执行任何操作之前，先调用`get_device_list`以获取正确的机器人昵称。将昵称缓存到当前会话中。
2. **确认操作结果** — 在开始或停止清洁后，调用`query_working_status`以验证命令是否生效。
3. **标准工作流程：**
   - *开始清洁：* 列出设备 → `start_cleaning`（act: `s`） → 检查状态
   - *返回充电站：* `control_recharging`（act: `go-start`） → 检查状态
   - *暂停和恢复：* `start_cleaning`（act: `p`） → 后续调用`start_cleaning`（act: `r`）
4. **自然语言映射：**
   - “打扫房子” / “清洁地板” / “开始清洁” → `start_cleaning`（act: `s`）
   - “让它回去” / “对接” / “充电” → `control_recharging`（act: `go-start`）
   - “停止” / “暂停” → `start_cleaning`（act: `p` 或 `h`）
   - “它在做什么？” / “它在充电吗？” → `query_working_status`

## 故障排除

- **未找到设备** — 请确保机器人已在Ecovacs应用中设置，并绑定到用于API密钥的同一账户。
- **认证错误** — 请验证`ECO_API_KEY`是否正确，以及`ECO_API_URL`是否与您的地区匹配。
- **服务器无法启动** — 请确保`uvx`库可用（使用`pip install uv`安装），或直接安装`ecovacs-robot-mcp`库。