---
name: clawd-cursor
version: 0.4.1
description: 这款AI桌面代理通过@nut-tree-fork/nut-js库直接控制Windows/Mac操作系统。它为你的自动化脚本提供了“眼睛”（即视觉感知能力）以及完整的鼠标控制功能，包括直接截图、鼠标点击、键盘输入、拖拽操作以及图形用户界面（GUI）自动化。适用于需要桌面自动化、原生AI控制或GUI测试的场景。无需外部服务器支持。使用该工具时，需要具备AI API密钥（Anthropic或OpenAI），以启用视觉处理功能。安装过程通过npm完成（依赖项会自动安装）。隐私声明：截图数据会发送至AI服务提供商（Anthropic或OpenAI）进行处理。
metadata:
  openclaw:
    requires:
      env:
        - AI_API_KEY
      bins:
        - node
        - npm
    primaryEnv: AI_API_KEY
    install:
      - git clone https://github.com/AmrDab/clawd-cursor.git
      - cd clawd-cursor && npm install && npm run build
    privacy:
      - Screenshots sent to external AI provider (Anthropic/OpenAI)
---
# Clawd Cursor

**一个技能，多个终端。** 无需集成数十个API，只需为你的代理程序提供一个屏幕即可。无论是Gmail、Slack、Jira还是Figma，只要你能点击这些界面，你的代理程序也能执行相应的操作。这是一款基于OpenClaw的桌面自动化工具，支持通过操作系统级别的原生控制来实现这些功能。

## 所需凭证

| 变量 | 敏感性 | 用途 |
|----------|------------|---------|
| `AI_API_KEY` | **高** — 用于调用外部API | 用于视觉处理和任务规划的Anthropic或OpenAI API密钥 |

**隐私说明：** 你的桌面截图会被发送到配置好的AI提供商（Anthropic或OpenAI）进行处理。请确保仅在屏幕上没有敏感数据的机器上使用该功能，或者在沙箱环境或虚拟机中运行。

**可选变量：** `AI_PROVIDER`（anthropic\|openai）

## 安装

需要**Node.js 20.0或更高版本**。

```bash
git clone https://github.com/AmrDab/clawd-cursor.git
cd clawd-cursor
npm install && npm run build
```

无需额外的外部服务器或配置脚本，该工具支持原生桌面控制，即可立即使用。

## 配置

在项目根目录下创建`.env`文件：

```env
AI_API_KEY=sk-ant-api03-...
AI_PROVIDER=anthropic
```

## 运行

```bash
# Computer Use (Anthropic — recommended for complex tasks)
npm start -- --provider anthropic

# Action Router (OpenAI/offline — fast for simple tasks)
npm start -- --provider openai
```

## 执行路径

### 路径A：通过Anthropic API执行任务
整个任务流程由Claude通过`computer_20250124`原生工具完成，包括截图、任务规划及自动执行。  
适用于复杂的多应用程序工作流程。执行时间约为100–156秒，非常可靠。

### 路径B：分解任务并路由执行（OpenAI/离线模式）
任务被分解为多个子任务，然后通过UI自动化流程直接与界面元素进行交互。对于常见的操作，完全不依赖大型语言模型（LLM）。  
适用于简单任务，执行时间约为2秒，支持离线运行。

## 安全等级

| 安全等级 | 功能 | 行为 |
|------|---------|----------|
| 🟢 自动模式 | 导航、阅读、打开应用程序 | 立即执行相应操作 |
| 🟡 预览模式 | 输入文本、填写表单 | 在执行前会进行日志记录 |
| 🔴 确认模式 | 发送消息、删除文件、执行购买操作 | 在执行前需要用户确认 |

## API端点

`http://localhost:3847`

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/task` | POST | `{"task": "Open Chrome"}` | 打开Chrome浏览器 |
| `/status` | GET | 获取代理程序的状态 |
| `/confirm` | POST | 发送确认请求（例如“批准”操作） |
| `/abort` | POST | 中止当前任务 |

## 安全注意事项

- **默认情况下，截图不会保存到磁盘**。它们仅保存在内存中，随后会被发送到AI提供商进行处理。如需进行故障排查，可以使用`--debug`参数启用截图保存功能。  
- AI API密钥允许将截图发送到外部API，请使用临时或受限范围的密钥，并在测试后及时更换。  
- Express API仅绑定到`127.0.0.1`地址，无法被网络上的其他机器访问。  
- 对于可能具有破坏性操作（如发送消息、删除文件、执行购买等），`/confirm`端点会强制执行确认流程。  
- 在处理屏幕上显示敏感数据的测试环境中，请确保在沙箱或虚拟机中运行该工具。  
- 安装过程中不会自动运行任何脚本，`npm install`仅用于获取依赖项，不会自动执行任何代码。

## 更新日志

### v0.4.1  
- **安全性改进：** 截图不再保存到磁盘，仅保存在内存中，处理完成后立即删除。  
- 通过`--debug`参数可启用截图保存功能（仅用于调试）。  
- 明确了API仅绑定到`localhost`地址。  
- 删除了2,857行不再使用的VNC相关代码。

### v0.4.0  
- **支持原生桌面控制**：通过`@nut-tree-fork/nut-js`实现，无需VNC服务器。  
- 截图生成速度提升了17倍（从约850毫秒缩短至约50毫秒）。  
- 连接速度提升了5倍（从约200毫秒缩短至约38毫秒）。  
- 简化了安装流程：只需执行`npm install && npm start`即可使用。

### v0.3.3  
- 完善了无头（headless）环境的配置流程，`setup.ps1`脚本可在非交互式shell环境中完整执行配置。

### v0.3.0  
- 对性能进行了多项优化：任务执行速度提升了约70%，减少了90%的冗余大型语言模型调用。

### v0.2.0  
- 将Anthropic的“计算机使用”API作为主要执行路径。  
- 对于简单任务，采用无需大型语言模型的自动化流程（零LLM模式）。