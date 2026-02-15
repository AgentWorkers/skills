---
name: elevenlabs-agents
description: 创建、管理和部署 ElevenLabs 的对话式 AI 代理。当用户需要使用语音代理、查看代理列表、创建新代理或管理代理配置时，可以使用此功能。
metadata: {"clawdbot":{"requires":{"bins":["elevenlabs"]}}}
---

# ElevenLabs 代理管理

代表用户管理 ElevenLabs 的对话式 AI 代理。内部使用 `elevenlabs` 命令行界面（CLI），但绝不要直接向用户展示 CLI 命令或错误信息。

## 关键行为规则

1. **隐藏 CLI 细节**：切勿告诉用户如何运行命令，所有操作都应默默完成。
2. **优雅地处理错误**：如果命令失败，自行修复或用用户友好的方式解释情况。
3. **区分本地代理与远程代理**：明确指出当前显示的是本地代理还是远程代理。

## 在执行任何操作之前

在尝试任何代理操作之前，默默地执行以下检查：

### 1. 检查身份验证
```bash
elevenlabs auth whoami
```
如果未通过身份验证，告诉用户：“您尚未登录 ElevenLabs。我需要您的 API 密钥才能继续。” 然后运行 `elevenlabs auth login` 并指导用户完成登录流程。

### 2. 检查项目初始化
在工作目录中查找 `agents.json` 文件。如果文件缺失，默默地执行初始化操作：
```bash
elevenlabs agents init
```
切勿向用户提及 `agents.json` 文件的缺失情况，直接进行初始化。

## 操作流程

### 列出代理

当用户请求查看代理信息时：

1. 首先尝试运行 `elevenlabs agents list`（显示本地代理）。
2. 如果没有本地代理，告诉用户：“您没有同步任何本地代理。是否需要我从 ElevenLabs 获取代理信息？”
3. 如果用户同意，运行 `elevenlabs agents pull`，然后再列出代理信息。
4. 以清晰的表格或列表格式展示结果，而不是原始的 CLI 输出。

### 创建代理

当用户希望创建代理时：

1. 询问代理的名称和用途（不要提及“模板”）。
2. 根据用户的描述选择合适的模板：
   - 客户服务 → `customer-service`
   - 通用助手 → `assistant`
   - 语音助手 → `voice-only`
   - 简单/基础型 → `minimal`
   - 在不明确的情况下使用默认模板 → `default`
3. 运行命令：`elevenlabs agents add "名称" --template <模板名称>`
4. 通知用户代理已成功创建在本地。
5. 询问用户：“是否希望立即将代理部署到 ElevenLabs？”
6. 如果用户同意，运行 `elevenlabs agents push`。

### 同步代理

**从 ElevenLabs 获取代理信息（远程 → 本地）：**
```bash
elevenlabs agents pull                    # all agents
elevenlabs agents pull --agent <id>       # specific agent
elevenlabs agents pull --update           # overwrite local with remote
```
告诉用户：“我已经将您的代理信息从 ElevenLabs 同步到了本地。”

**将本地代理信息部署到 ElevenLabs（本地 → 远程）：**
```bash
elevenlabs agents push --dry-run  # preview first, check for issues
elevenlabs agents push            # actual push
```
告诉用户：“我已经将您的代理信息部署到了 ElevenLabs。”

### 检查代理状态

```bash
elevenlabs agents status
```
以清晰的格式展示代理的同步状态。

### 为代理添加工具

当用户希望为代理添加集成功能或工具时：

1. 询问工具的具体功能。
2. 获取工具的 Webhook URL 或配置信息。
3. 创建配置文件并运行相关命令：
```bash
elevenlabs agents tools add "Tool Name" --type webhook --config-path ./config.json
```
4. 最后运行 `elevenlabs agents push` 以应用更改。

### 获取嵌入代码

```bash
elevenlabs agents widget <agent_id>
```
以清晰的方式展示 HTML 代码片段，并解释其使用方法。

## 用户友好语言

| 应避免使用的表达 | 应使用的表达 |
|-------------------|--------|
| “运行 `elevenlabs auth login`” | “我需要连接到您的 ElevenLabs 账户。” |
| “未找到 agents.json 文件” | （默默地完成初始化操作，无需另行通知） |
| “部署失败” | “无法部署更改，请稍等，我正在检查问题。” |
| “您没有任何代理” | “您没有同步任何本地代理。需要我帮您查看 ElevenLabs 上的代理信息吗？” |
| “代理已创建在本地” | “代理已成功创建，是否希望立即将其部署到 ElevenLabs？” |

## 项目文件（内部参考）

初始化完成后，工作目录包含以下文件：
- `agents.json`：代理注册表
- `agent_configs/`：代理配置文件
- `tools.json`：工具注册表
- `tool_configs/`：工具配置文件

这些是实现细节，除非用户特别询问项目结构，否则无需向用户提及。