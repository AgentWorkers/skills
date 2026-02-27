---
name: cursor-agent
version: 3.0.2
description: "您可以通过两种方式使用 Cursor Agent 执行编码任务：  
(1) **本地 CLI**：直接从终端运行 Cursor Agent，适用于任何项目的快速、通用编码需求；  
(2) **VS Code Node**：通过 OpenClaw Node 协议远程控制 Cursor/VS Code IDE，适用于需要完整 IDE 功能（如诊断、参考资料、调试）的项目。  
如果追求速度，建议选择 CLI；当需要 IDE 的高级功能时，则可以选择 Node 方式。"
metadata:
  {
    "openclaw": {
      "emoji": "🖥️",
      "requires": { "anyBins": ["agent", "cursor-agent"] }
    },
  }
---
# **Cursor Agent 技能**

**OpenClaw 提供了两种使用 Cursor Agent 的方式，适用于不同的场景。**

## 相关工具

- **[OpenClaw Node for VS Code](https://marketplace.visualstudio.com/items?itemName=xiaoyaner.openclaw-node-vscode)**：**VS Code 扩展程序**，支持通过 Node 路径与 Cursor Agent 交互（使用第二种方式前请先安装此扩展）。
- **[vscode-node](https://clawhub.ai/xiaoyaner0201/vscode-node)**：**独立工具**，仅用于通过 Node 路径与 Cursor Agent 交互（如果您不需要使用 CLI）。
- **源代码仓库**：[github.com/xiaoyaner-home/openclaw-vscode](https://github.com/xiaoyaner-home/openclaw-vscode)

## **路径选择**

| **场景** | **使用路径** | **原因** |
|--------|-----------|-------------------|
| **快速编码、修复 bug、重构** | **CLI** | 快速、无需设置，可在任何地方使用 |
| **生成代码、审阅 Pull Request、编写测试** | **CLI** | 非交互式的 `-p` 模式非常适用 |
| **使用实时诊断工具修复类型错误** | **Node** | `diagnostics.get` 可显示实际的 TypeScript/Lint 错误 |
| **先导航到定义或引用位置** | **Node** | `langdefinition`、`langreferences` 可帮助快速定位 |
| **运行项目测试并迭代** | **Node** | `test.run` 和 `test.results` 可帮助您管理测试流程 |
| **使用断点进行调试** | **Node** | 支持完整的调试协议 |
| **对特定项目进行针对性修改** | **Node** | 可利用 IDE 的工作区上下文 |

**默认设置：使用 CLI。** 仅在需要 IDE 的智能功能时才使用 Node。

---

## **路径 1：CLI（本地 Cursor Agent）**

### **先决条件**

### **模式**

| **模式** | **标志** | **使用场景** |
|--------|---------|-------------------|
| **Agent** | （默认） | 全面编码操作（读取、写入、执行命令） |
| **Plan** | `--plan` 或 `--mode=plan` | 先设计执行方案，再选择在本地还是云端执行 |
| **Ask** | `--mode=ask` | 仅用于读取代码库信息，不支持编辑 |

### **交互模式**

### **非交互模式（自动化）**

### **将工作推送到云端（继续执行）**

### **会话管理**

### **斜杠命令（交互式操作）**

| **命令** | **功能** |
|---------|-------------------|
| `/plan` | 切换到计划模式 / 查看当前计划 |
| `/ask` | 切换到询问模式 |
| `/models` | 切换 AI 模型 |
| `/compress` | 总结对话内容 |
| `/rules` | 创建/编辑规则 |
| `/commands` | 创建/编辑自定义命令 |
| `/mcp enable <name>` | 启用 MCP 服务器 |
| `/mcp disable <name>` | 关闭 MCP 服务器 |
| `/sandbox` | 配置沙箱模式 |
| `/max-mode [on\|off]` | 切换最大模式 |
| `/resume` | 恢复之前的对话 |

### **键盘快捷键**

| **快捷键** | **功能** |
|---------|-------------------|
| `Shift+Tab` | 在 Agent、Plan、Ask 模式之间切换 |
| `Shift+Enter` | 插入换行符（多行提示符） |
| `Ctrl+R` | 查看更改内容（`i` 表示查看详细信息，箭头键用于导航） |
| `Ctrl+D` | 退出（双击可确保安全退出） |
| `ArrowUp` | 查看上一条消息 |

### **上下文与规则**

CLI 会自动加载以下文件：
- `.cursor/rules` 目录 |
- 项目根目录下的 `AGENTS.md` 文件 |
- 项目根目录下的 `CLAUDE.md` 文件 |
- 从 `mcp.json` 文件中加载的 MCP 服务器配置

在交互模式下，可以使用 `@filename` 或 `@directory/` 来引用相关上下文信息。

### **注意：** **必须使用带有 `pty:true` 的终端窗口来使用 CLI**

Cursor CLI 是一个交互式图形用户界面（TUI），因此需要一个真实的终端窗口。请确保在命令行中设置 `pty:true`：

---

**对于长时间运行的任务，建议使用后台进程并设置超时：**

---

### **沙箱控制**

沙箱模式支持精细的网络访问控制，您可以定义代理可以访问的域名。

---

## **路径 2：VS Code / Cursor Node**

通过 OpenClaw Node 协议远程控制 VS Code 和 Cursor Agent。确保 VS Code 安装了 `openclaw-node-vscode` 扩展程序，并且该扩展已在 VS Code 中显示为可用节点。

### **先决条件**

- 确保已安装 [VS Code 扩展程序](https://marketplace.visualstudio.com/items?itemName=xiaoyaner.openclaw-node-vscode)。
- 在 VS Code 的节点列表中能看到相应的 Node 节点。
- 扩展程序的状态栏应显示绿色勾选（🟢）。

### **调用方式**

### **超时设置**

| **操作类型** | **超时时间（毫秒）** | **说明** |
|---------|------------------|-------------------|
| **文件/编辑器/语言操作** | 15000 | 快速的操作 |
| **Git 操作** | 30000 | 可能涉及磁盘 I/O 操作 |
| **测试** | 60000 | 取决于测试套件的执行时间 |
| **代理计划/询问操作** | 180000 | AI 的思考时间 |
| **代理执行操作** | 300000 | 全面的编码任务 |

### **命令参考**

| **类别** | **前缀** | **常用命令** |
|---------|------------------|-------------------|
| **文件** | `vscode.file.*` | 读取、写入、编辑、删除文件 |
| **目录** | `vscode.dir.*` | 列出目录内容 |
| **语言** | `vscode.lang.*` | 查看语言定义、引用信息、悬停提示、符号信息、重命名文件、格式化代码 |
| **编辑器** | `vscode.editor.*` | 查看文件上下文、打开文件、选择文件内容 |
| **诊断工具** | `vscode.diagnostics.*` | 查看错误/警告信息 |
| **Git** | `vscode.git.*` | 查看 Git 状态、执行差分操作、查看日志、标记修改、暂存文件、提交更改 |
| **测试** | `vscode.test.*` | 列出测试用例、运行测试、查看测试结果 |
| **调试** | `vscode.debug.*` | 启动/停止调试、设置断点、查看变量值、查看调用栈 |
| **代理** | `vscode.agent.*` | 查看代理状态、运行代理任务、配置代理 |
| **工作区** | `vscodeWorkspace.*` | 查看工作区相关信息 |

### **快速示例**

### **Node 工作流程：修复问题 → 验证结果 → 提交更改**

Node 路径的强大之处在于它能够与 IDE 智能功能紧密结合，形成一个完整的闭环：

---

### **综合工作流程示例**

- 使用 CLI 完成基础任务；
- 在需要更高精度时切换到 Node 模式进行详细操作。

---

## **错误处理**

| **错误类型** | **原因** | **解决方法** |
|---------|----------------|-------------------|
| **CLI 停滞** | 未使用 `pty` 参数 | 在执行命令时添加 `pty:true` 参数 |
| **找不到 Node** | 扩展程序未正确连接 | 检查 VS Code 的状态栏 |
| **命令不被允许执行** | 可能被禁止的命令 | 将该命令添加到 `gateway.nodes.allowCommands` 文件中 |
| **超时** | 操作耗时过长 | 增加 `invokeTimeoutMs` 的值 |
| **路径遍历失败** | 使用了绝对路径 | 对于 Node 操作，请使用相对路径 |

## **安全性**

- **CLI**：遵循沙箱模式和命令审批规则。
- **Node**：所有路径均以工作区为基准；使用 Ed25519 加密技术进行身份验证；需要通过 Gateway 进行操作审批。
- **两者**：默认情况下都不允许直接访问原始 shell 环境。