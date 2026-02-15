---
name: cloudphone
description: 使用 `mcporter` 调用 `cpc-mcp-server` 的 AutoJS Agent 工具来执行云端的 Android 任务并获取结果。
metadata:
  {
    "openclaw":
      {
        "emoji": "📱",
        "requires":
          { "bins": ["mcporter"], "env": ["CLOUDPHONE_API_KEY"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "mcporter",
              "bins": ["mcporter"],
              "label": "Install mcporter (node)",
            },
          ],
        "primaryEnv": "CLOUDPHONE_API_KEY",
      },
  }
---

## 该技能的功能

`cloudphone` 能够指导代理在云电话环境中运行 Android 自动化任务，它通过 `mcporter` 调用 `cpc-mcp-server` 工具来实现这一功能。

该技能适用于以下场景：
- 基于 AutoJS 的云电话自动化操作
- 应用程序回归测试/冒烟测试的执行
- 远程批量操作工作流程
- 在云端的 Android 设备上进行脚本化交互

---

## 何时使用该技能

当用户需要执行以下操作时，请使用该技能：
- “在云电话上运行一个脚本”
- “使用 AutoJS 自动化这个应用程序流程”
- “远程执行 Android 用户界面操作并返回截图/日志”
- “使用 cpc-mcp-server 进行云设备的自动化操作”

---

## 何时不使用该技能

以下情况不建议使用该技能：
- 本地 ADB/模拟器自动化（非云设备）
- iOS 自动化（例如 XCUITest）
- 仅进行静态脚本/代码审查，无需实际设备执行
- 仅提供咨询请求，而没有具体的可执行任务目标

---

## 执行前必须满足的先决条件

在执行任何操作之前，请确保身份验证配置正确。

`cpc-mcp-server` 需要以下授权信息：
- `Authorization: Bearer <API_KEY>`

该技能通过以下方式统一管理 API 密钥：
- 使用 `CLOUDPHONE_API_KEY`（必填）

### 其他要求

1. 设置环境变量 `CLOUDPHONE_API_KEY`。
2. 在执行前确保 MCP 服务器的头部信息（header）已正确设置：
   - `Authorization: Bearer $CLOUDPHONE_API_KEY`
3. 绝不要将真实的 API 密钥硬编码到仓库文件、`SKILL.md` 或配置文件中。

> 该技能仅定义了名称和先决条件；具体的密钥注入逻辑由运行时/环境配置负责处理。

---

## 调用模型（通过 mcporter）

该技能不直接调用 MCP 工具，而是通过 `mcporter` 命令行工具来调用 `cpc-mcp-server` 上的相应工具。

常见的命令模式包括：
- 列出已配置的 MCP 服务器：
  - `mcporter list`
- 检查服务器的配置信息：
  - `mcporter list cpc-mcp-server --schema`
- 带参数调用工具（推荐使用 JSON 格式）：
  - `mcporter call cpc-mcp-server.<tool> --args '<json>'`

> 对于较长的指令、包含多语言文本或特殊字符的情况，建议使用 `--args` 参数传递 JSON 数据。

---

## 创建任务前的基本信息收集

在创建任务之前，请收集以下信息（如果缺少某些信息，可以后续补充）：
1. 目标应用程序（名称/包名）
2. 需要执行的操作
3. 成功的标准（什么情况算作任务完成）
4. 预期的输出类型（截图/日志/文本结果）

---

## 工具 1：创建任务（`createAutoJsAgentTask`）

### 功能

创建并调度一个 AutoJS 代理任务，然后获取任务的唯一标识符（`taskId`，可能还包括 `sessionId`）。

### 推荐的调用方式

```bash
mcporter call cpc-mcp-server.createAutoJsAgentTask --args '{
  "instruction": "在云电话上打开 <APP_NAME> 应用程序，使用测试账户登录，导航到订单页面，捕获截图，并返回订单数量。",
  "lang": "en"
}'
```