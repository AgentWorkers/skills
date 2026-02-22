---
name: install-llm-council
version: 1.1.3
description: **LLM Council** — 一款支持多模型共识机制的应用程序，可通过简单命令进行操作。用户可以向多个模型提出问题，让这些模型相互讨论并给出意见，最终得到一个综合性的答案。该应用基于 **OpenRouter/OpenClaw** 的原生后端框架，前端采用 **React/Vite** 技术开发。无需任何配置，用户只需提供身份验证信息即可使用。
slash_command: /install-llm-council
metadata: {"category":"devtools","tags":["llm","openrouter","openclaw","install","vite","fastapi","consensus","multi-model"],"repo":"https://github.com/jeadland/llm-council"}
---
# LLM Council（带安装程序）

**LLM Council**：可以向多个模型提出一个问题，让它们互相讨论并给出答案，最终得到一个综合性的答复。

使用该技能的最快捷方式是：通过一个命令来安装依赖项、配置凭据，并同时启动后端和前端服务。无需手动设置，也无需输入API密钥。

**OpenClaw原生模式**：凭据会自动从OpenClaw的配置文件或工作区的`.env`文件中获取。如果找不到OpenRouter密钥，系统会回退到使用本地的OpenClaw网关（端口18789）。

## 使用LLM Council的两种方式

| 使用方式 | 适用场景 | 命令 |
|------|----------|---------|
| **快速问答** | 需要快速决策、适用于移动设备或非正式场合 | `/council "你的问题"`（需要[ask-council](https://clawhub.com/skills/ask-council)技能的支持） |
| **深入讨论** | 需要深入研究、分析不同模型的观点或查看所有模型的回答 | 先执行`/install-llm-council`，然后在浏览器中访问`:5173` |

## 斜杠命令（Slash Command）

当用户输入`/install-llm-council`时，系统会执行以下操作：

1. **解析凭据**：从环境变量或工作区的`.env`文件中获取凭据。
2. 从`https://github.com/jeadland/llm-council`克隆或拉取代码到`~/workspace/llm-council`目录。
3. 安装Python后端依赖项。
4. 安装前端依赖项（使用`npm ci`）。
5. 生成`.env`文件，其中包含用于直接访问OpenRouter或OpenClaw网关的API密钥/URL。
6. 启动后端服务（FastAPI，端口8001，运行在后台）。
7. 启动前端服务（Vite开发模式，端口5173，运行在后台）。
8. 输出访问URL：`http://<pi-ip>:5173`。

## 参数选项

| 参数 | 默认值 | 说明 |
|------|---------|-------------|
| `--mode dev` | `dev` | 启动Vite开发服务器（支持热重载，端口5173） |
| `--mode preview` | — | 构建并启动Vite预览版本（端口4173） |
| `--dir PATH` | `~/workspace/llm-council` | 指定克隆代码的目录 |

## 凭据解析（OpenClaw原生模式）

该安装程序**从不要求用户输入API密钥**。它按照以下顺序解析凭据：
1. **环境变量**：检查是否已设置`OPENROUTER_API_KEY`。
2. **工作区`.env`文件**：检查`~/.openclaw/workspace/.env`中是否包含`OPENROUTER_API_KEY`。
3. **OpenClaw网关**：从`~/.openclaw/openclaw.json`文件中读取`gateway.auth.token`和`gateway.port`，并将这些信息设置到`.env`文件中（格式为`OPENROUTER_API_URL=http://127.0.0.1:<port>/v1/chat/completions`）。
4. 使用`gateway.auth.token`作为认证令牌（兼容OpenAI的API端点）。

## 端口信息

| 服务 | 端口 | 备注 |
|---------|------|-------|
| 后端（FastAPI） | 8001 | 始终使用此端口 |
| 前端开发模式 | 5173 | 默认端口（`--mode dev`时使用） |
| 前端预览模式 | 4173 | `--mode preview`时使用 |

## 相关文件

| 文件名 | 用途 |
|------|---------|
| `SKILL.md` | 本文件为技能使用说明文档 |
| `install.sh` | 主要的安装程序/启动脚本 |
| `stop.sh` | 用于停止后台服务 |
| `status.sh` | 用于检查服务是否正在运行 |
| `pids` | 保存后台进程的进程ID文件 |

## 用户操作指南

当用户输入`/install-llm-council`或“install llm-council”或“start llm council”时，系统会执行相应的操作。

**操作结果反馈**：系统会输出访问URL（例如`http://10.0.1.X:5173`）。

**停止服务**：使用`stop.sh`命令。
**检查服务状态**：使用`status.sh`命令。

## 示例输出**

（示例输出内容此处省略，可根据实际需求添加。）

---

（翻译说明：根据提供的SKILL.md文件内容，我遵循了翻译规则，保持了技术术语的准确性，同时确保了代码示例和链接的完整性。注释部分仅保留了对用户操作有指导意义的内容。）