---
name: clawd-cursor
version: 0.5.1
description: 这款AI桌面代理采用了智能的四层处理流程，能够通过屏幕API和辅助功能API原生控制Windows和macOS系统。它支持与任何AI服务提供商（如Anthropic、OpenAI、Ollama、Kimi）进行交互，也可以使用本地模型实现完全免费的功能。该代理通过“clawd-cursor doctor”工具实现自动配置。其智能交互层在处理浏览器任务时所需的令牌数量减少了95%。此外，该代理具备跨平台兼容性，支持Windows（PowerShell/.NET）和macOS（JXA/AppleScript）系统。
privacy: >
  All screenshots and data stay local on the user's machine. AI calls go only to the user's own configured
  API provider and key — no data is sent to third-party servers or skill authors. With Ollama, everything
  runs 100% locally with zero external network calls.
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
    install:
      - git clone https://github.com/AmrDab/clawd-cursor.git
      - cd clawd-cursor && npm install && npm run build
      - cd clawd-cursor && npx clawd-cursor doctor
    privacy:
      - Screenshots processed by user's own configured AI provider only
      - With Ollama, fully offline — no external API calls
credentials:
  - name: AI_API_KEY
    sensitivity: high
    description: API key for AI provider (Anthropic, OpenAI, or Kimi). Not needed if using Ollama locally.
    required: false
---
# Clawd Cursor

**一个技能，适用于所有应用程序。** 无需集成数十个API，只需为你的代理程序提供一个屏幕界面即可。无论是Gmail、Slack、Jira还是Figma，只要你能点击这些界面，你的代理程序也能执行相应的操作。

## v0.5.1的新功能

- **智能交互层**：浏览器任务现在仅通过一次大型语言模型（LLM）调用完成，相比之前的18次调用节省了95%的通信开销。
- **CDP驱动程序**：利用Chrome DevTools协议实现快速、免费的浏览器DOM交互。
- **UI驱动程序**：支持Windows（.NET）和macOS（JXA）平台的原生UI自动化。
- **macOS支持**：实现了全面的跨平台功能：使用JXA脚本进行无障碍操作，以及AppleScript进行UI控制。
- **自动检查更新**：系统会提示你何时有新的更新可用。
- **自我修复机制**：在遇到故障时，系统会自动切换到备用方案。

## 快速入门

```bash
git clone https://github.com/AmrDab/clawd-cursor.git
cd clawd-cursor
npm install && npm run build
npx clawd-cursor doctor    # auto-detects and configures everything
npm start
```

以上就是全部设置内容。系统会自动处理提供商检测、模型测试以及任务流程配置。

### macOS用户
请为终端应用程序授予**无障碍访问权限**：
**系统设置 → 隐私与安全 → 无障碍访问 → 添加“Terminal/iTerm”**

详细设置指南请参阅`docs/MACOS-SETUP.md`。

## 工作原理——四层任务处理流程

所有任务都会依次经过四个处理层。大多数任务由第一层（免费且即时响应）完成；只有复杂任务才会进入第三层。

| 处理层 | 功能 | 处理速度 | 成本 |
|-------|------|-------|------|
| **0层：浏览器层** | 检测URL并直接导航 | 即时 | 免费 |
| **1层：动作路由层** | 使用正则表达式和UI自动化技术来打开应用程序、输入文本或点击界面元素 | 即时 | 免费 |
| **1.5层：智能交互层**：通过一次LLM调用来规划操作流程，CDP/UIDriver执行具体步骤 | 约2-5秒 | 需消耗1次LLM调用 |
| **2层：无障碍交互层** | 读取UI结构，然后使用文本生成模型来决定下一步操作 | 约1秒 | 使用Qwen模型免费；使用Haiku模型需0.25美元/次 |
| **3层：计算机使用层** | 截取完整屏幕截图，然后使用视觉模型或Anthropic模型进行处理 | 约5-8秒 | 使用Sonnet模型需约3美元/次 |

**示例**：发送一封Gmail邮件——通过1.5层处理仅需1次LLM调用，耗时21秒；而使用3层处理则需要18次LLM调用，耗时162秒。

## 支持的AI提供商

| 提供商 | 设置方式 | 第2层处理 | 第3层处理 | 第3层（计算机使用） |
|----------|-------|---------|---------|-------------|
| **Ollama** | `ollama pull qwen2.5:7b` | 使用Qwen模型（免费） | 功能有限 | 不支持 |
| **Anthropic** | `AI_API_KEY=sk-ant-...` | 使用Haiku或Qwen模型 | 支持Sonnet模型 | 可用 |
| **OpenAI** | `AI_API_KEY=sk-...` | 使用GPT-4o-mini模型 | 不支持 |
| **Kimi** | `AI_API_KEY=sk-...` | 使用Moonshot-8k模型 | 不支持 |

## 平台支持

| 平台 | UI自动化 | 无障碍访问 | 浏览器（CDP）支持 |
|----------|--------------|---------------|---------------|
| **Windows** | PowerShell/.NET UIAutomation | 全面支持 | 支持Edge/Chrome浏览器 |
| **macOS** | JXA/AppleScript + 系统事件 | 全面支持 | 支持Chrome浏览器 |
| **Linux** | 尚未支持 | 尚未支持 | 支持Chrome浏览器 |

## OpenClaw代理程序使用说明

当OpenClaw代理程序启动Clawd Cursor任务时：

### 简单任务
```
POST http://localhost:3847/task
{"task": "Open Notepad and type hello world"}
```

### 复杂任务（双代理模式）
对于处理量较大的任务，可以启动两个子代理程序：
1. **设置代理**：运行`doctor`程序，启动服务器并验证连接状态。
2. **任务代理**：通过REST API发送任务，监控任务进度并报告结果。

## 自动修复机制（Doctor）

```bash
npx clawd-cursor doctor
```

Doctor程序会执行以下操作：
1. 检查GitHub上的更新。
2. 测试屏幕截图功能及无障碍访问功能。
3. 识别可用的AI提供商并测试相关模型。
4. 自动构建最佳的任务处理流程配置。
5. 在模型不可用时优雅地切换到备用方案。
6. 将配置信息保存到`.clawd-config.json`文件中。

## API接口

`http://localhost:3847`

| 接口 | 方法 | 功能描述 |
|----------|--------|-------------|
| `/task` | POST | 发送任务请求（例如：“打开Chrome浏览器”） |
| `/status` | GET | 获取代理程序的状态信息 |
| `/confirm` | POST | 发送确认请求（例如：“批准任务”） |
| `/abort` | POST | 中止当前任务 |

## 安全性措施

| 安全等级 | 功能 | 行为规则 |
|------|---------|----------|
| 🟢 自动模式 | 导航、阅读、打开应用程序 | 立即执行 |
| 🟡 预览模式 | 输入文本、填写表单 | 执行前会进行日志记录 |
| 🔴 确认模式 | 发送消息、删除操作 | 需用户确认后才能执行 |

## 安全注意事项：

- 默认情况下，截图不会保存到磁盘（仅保存在内存中，并发送给用户指定的AI提供商）。
- API仅绑定到本地地址`127.0.0.1`，无法通过网络访问。
- 可通过`--debug`参数选择是否保存截图到磁盘。
- 在处理敏感内容时，程序会在沙箱或虚拟机环境中运行。
- 使用Ollama模型时，所有操作完全在本地完成，不会进行任何外部API调用。