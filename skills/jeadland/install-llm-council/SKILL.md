---
name: install-llm-council
version: 1.1.6
description: LLM Council：一款多模型共识应用程序，支持一键式设置。您可以向多个模型提出问题，让这些模型相互讨论并给出综合性的答案。该应用基于 OpenRouter/OpenClaw 构建后端，前端采用 React/Vite 技术开发，无需任何配置；用户认证信息会自动处理。
slash_command: /install-llm-council
metadata: {"category":"devtools","tags":["llm","openrouter","openclaw","install","vite","fastapi","consensus","multi-model"],"repo":"https://github.com/jeadland/llm-council"}
---
# LLM Council（含安装器）

**LLM Council**：可以向多个模型提出一个问题，让它们互相评审，然后获得一个综合的答案。

使用该技能的最快捷方式是：通过一个命令即可完成依赖项的安装、凭据的配置以及后端和前端的启动。无需手动设置，也无需输入API密钥。

**OpenClaw-native**：凭据会自动从OpenClaw的配置文件或工作区的`.env`文件中获取。如果找不到OpenRouter密钥，系统会回退到使用本地的OpenClaw网关（端口18789）。

## 使用LLM Council的两种方式

| 方式 | 适用场景 | 命令 |
|------|----------|---------|
| **快速回答** | 快速决策、移动设备使用、非正式问题 | `/council "你的问题"`（需要[ask-council](https://clawhub.com/skills/ask-council)技能） |
| **全面讨论** | 深入研究、探讨不同意见、查看所有模型的回答 | `/install-llm-council`，然后在浏览器中访问`:5173` |

## 斜杠命令（Slash Command）

当用户输入`/install-llm-council`时，脚本会执行以下操作：

1. **解析凭据**：从环境变量中获取凭据，或从工作区的`.env`文件中读取；系统不会提示用户输入任何信息。
2. 从`https://github.com/jeadland/llm-council`克隆或拉取代码到`~/workspace/llm-council`目录。
3. 安装Python后端依赖项。
4. 安装前端依赖项（使用`npm ci`）。
5. 生成`.env`文件，其中包含用于直接访问OpenRouter或OpenClaw网关的API密钥/URL。
6. 启动应用程序（使用`start.sh`脚本，该脚本具备模式识别功能，并能进行健康检查）。
7. 自动处理端口冲突（当默认端口被占用时，会选择安全的备用端口）。
8. 输出可访问的URL（包括通过Caddy代理的路径和常见的直接访问方式）。

## 标志参数（Flags）

| 标志 | 默认值 | 说明 |
|------|---------|-------------|
| `--mode auto` | `auto` | 如果检测到Caddy服务器运行在端口5173上，则使用预览模式；否则使用开发模式。 |
| `--mode dev` | — | 启动Vite开发服务器（支持热重载，默认端口为5173）。 |
| `--mode preview` | — | 构建并运行Vite预览版本（默认端口为4173）。 |
| `--dir PATH` | `~/workspace/llm-council` | 指定克隆代码的目录。 |

## 凭据解析（OpenClaw-native）

安装器**从不要求用户输入API密钥**。它按照以下顺序解析凭据：

1. 环境变量`OPENROUTER_API_KEY`。
2. 工作区的`.env`文件（例如`~/.openclaw/workspace/.env`，其中可能包含`OPENROUTER_API_KEY=...`）。
3. OpenClaw网关配置（`~/.openclaw/openclaw.json`文件中的`gateway.auth.token`和`gateway.port`）：
   - 将`OPENROUTER_API_URL`设置为`http://127.0.0.1:<port>/v1/chat/completions`。
   - 使用网关生成的令牌作为认证凭据（兼容OpenAI的API端点）。

## 端口信息

| 服务 | 端口 | 备注 |
|---------|------|-------|
| 后端（FastAPI） | 8001 | 始终使用此端口。 |
| 前端开发模式 | 5173 | 默认端口（使用`--mode dev`时）。 |
| 前端预览模式 | 4173 | 使用`--mode preview`时。 |

## 文件说明

| 文件名 | 用途 |
|------|---------|
| `SKILL.md` | 本文件为技能使用说明文档。 |
| `install.sh` | 主要的安装和启动脚本。 |
| `stop.sh` | 用于停止后台服务。 |
| `status.sh` | 用于检查服务是否正在运行。 |
| `pids` | 保存后台进程的进程ID。 |

## 用户操作指南

当用户输入`/install-llm-council`或“install llm-council”或“start llm council”时，脚本会输出应用程序的访问URL（例如`http://10.0.1.X:5173`）。

**停止应用程序：** 使用`stop.sh`命令。
**检查应用程序状态：** 使用`status.sh`命令。

## 示例输出**

（示例输出内容略……）