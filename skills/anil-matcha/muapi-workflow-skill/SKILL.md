---
slug: muapi-workflow-skill
name: muapi-workflow
version: "0.1.0"
description: 构建、运行并可视化多步骤的AI生成工作流程。AI架构师将自然语言描述转换为相互连接的节点图，从而将图像生成、视频创建、视频处理以及视频编辑等步骤整合成自动化的工作流程。
acceptLicenseTerms: true
---
# 人工智能工作流构建器

您可以将 muapi.ai 提供的任意生成步骤组合起来，形成自动化的工作流。人工智能架构师会将您的自然语言描述转换为一个可执行的节点图。

## 先决条件

在运行任何命令之前，请确保 `muapi` 命令行工具（CLI）是最新的。每次会话开始时，请从源代码重新安装它：

```bash
pip install --upgrade /path/to/muapi-cli
```

请将 `/path/to/muapi-cli` 替换为您工作空间中 `muapi-cli` 目录的实际路径（该目录包含 `pyproject.toml` 文件）。

## 核心操作

1. **生成** (`generate-workflow.sh`) — 人工智能架构师根据描述创建工作流
2. **查找** (`discover-workflow.sh`) — 通过自然语言查找现有的相关工作流
3. **编辑** (`generate-workflow.sh --workflow-id`) — 提示用户后修改现有工作流
4. **交互式运行** (`interactive-run.sh`) — 提示用户输入信息并执行工作流
5. **运行** (`run-workflow.sh`) — 逐个节点执行工作流并收集输出结果
6. **CLI** (`muapi workflow`) — 直接通过终端进行完整的创建、读取、更新和删除（CRUD）操作以及可视化展示

---

## 代理引导的发现与选择

作为人工智能代理，您能够阅读并理解可用工作流的用途，从而为用户选择最适合的任务工作流（例如：“创建一个用户生成内容（UGC）视频”）。

1. **发现**：以 JSON 格式获取可用工作流及其描述。
   ```bash
   muapi workflow discover --output-json
   ```
2. **匹配（内部推理）**：利用您的大型语言模型（LLM）功能分析返回的工作流的 `name`（名称）、`category`（类别）和 `description`（描述）字段，找到最符合用户需求的工作流。
3. **分析**：如果找到合适的工作流，检查其结构以确保它包含必要的节点和参数。
   ```bash
   muapi workflow get <workflow_id>
   ```
   **重要规则**：`muapi workflow get` 的输出中会包含一个“API 输入”表格。您必须阅读此表格以了解所需的输入信息。
4. **选择并确认用户输入**：
   - 如果找到了完全匹配的工作流，必须先询问用户提供所需的 API 输入值，然后再执行该工作流。**切勿自行发明或猜测输入值（如提示信息、URL 等）**。
   - 如果有多个工作流与用户需求高度相关，请向用户展示这些工作流及其描述，并询问他们选择哪一个，同时获取所需的输入信息。
   - 如果没有工作流能满足用户的复杂需求，可以建议用户使用 `muapi workflow create` 命令来创建一个新的工作流。

### 代理推理示例
> “用户需要一个产品宣传视频。我使用 `discover` 命令获取了工作流目录。找到了两个潜在的工作流：
> 1. `wf_123`：‘带背景音乐的产品宣传视频’
> 2. `wf_456`：‘简单视频生成’
> 我会使用 `get` 命令分析 `wf_123`，确认它包含所需的节点。如果匹配准确，我会建议使用 `wf_123`，或者直接执行它。”

---

## 协议：构建工作流

### 第一步 — 描述您的工作流

```bash
muapi workflow create "take a text prompt, generate an image with flux-dev, then upscale it to 4K"
```

架构师会返回一个具有唯一 ID 的工作流及其节点图。请保存该 ID。

### 第二步 — 检查和可视化

```bash
# Rich ASCII node graph in the terminal
muapi workflow get <workflow_id>

# Or raw JSON
muapi workflow get <workflow_id> --output-json
```

### 第三步 — 运行工作流

```bash
# Run with specific inputs
muapi workflow execute <workflow_id> \
  --input "node1.prompt=a glowing crystal cave at midnight"

# Use --download to pull results locally
muapi workflow execute <workflow_id> \
  --input "node1.prompt=a sunset" \
  --download ./outputs
```

### 第四步 — 查找（可选）
如果您想重用现有的工作流而不是创建新的工作流：

```bash
# Search by keywords
muapi workflow discover "ugc video"
```

### 第五步 — 交互式执行
运行工作流时，命令行工具会提示您输入每个所需的参数：

```bash
muapi workflow run-interactive <workflow_id>
```

---

## 工作流示例

### 图像处理工作流

```bash
# Text → Image → Upscale
muapi workflow create "take a text prompt, generate with flux-dev, upscale the result"

# Text → Image → Background removal → Product shot
muapi workflow create "generate a product image with hidream, remove background, create professional product shot"
```

### 视频处理工作流

```bash
# Text → Video
muapi workflow create "generate a 10-second cinematic video from a text prompt using kling-master"

# Image → Video → Lipsync
muapi workflow create "animate an input image with seedance, then apply lipsync from an audio file"
```

---

## 修改现有工作流

```bash
# Add a step
muapi workflow edit <id> --prompt "add a face-swap step after the image generation"

# Swap a model
muapi workflow edit <id> --prompt "change the video model from kling to veo3"
```

---

## 命令行工具参考

```bash
# List all your workflows
muapi workflow list

# Browse templates
muapi workflow templates

# Generate new workflow
muapi workflow create "text → flux image → upscale → face swap"

# Visualize a workflow
muapi workflow get <id>

# Execute with inputs
muapi workflow execute <id> --input "node1.prompt=a sunset"

# Monitor a run
muapi workflow status <run_id>

# Get outputs
muapi workflow outputs <run_id> --download ./results

# Edit with AI
muapi workflow edit <id> --prompt "add lipsync at the end"

# Rename / delete
muapi workflow rename <id> --name "Product Pipeline v2"
muapi workflow delete <id>
```

---

## 人工智能代理使用的 MCP 工具

| 工具 | 描述 |
|------|-------------|
| `muapi_workflow_list` | 列出用户的工作流 |
| `muapi_workflow_create` | 人工智能架构师：根据提示创建工作流 |
| `muapi_workflow_get` | 获取工作流定义及节点图 |
| `muapi_workflow_execute` | 使用特定参数执行工作流 |
| `muapi_workflow_status` | 逐节点显示执行状态 |
| `muapi_workflow_outputs` | 最终输出结果的 URL |

---

## 限制条件

- 工作流可以包含 muapi.ai 提供的任意类型的节点（图像、视频、音频、增强、编辑等）
- 节点的输出会自动作为输入传递给下游节点
- `--sync` 模式会等待最多 120 秒以完成生成；对于复杂的工作流，请使用 `--async` 模式并分别进行poll操作
- 每个工作流的执行超时时间为 10 分钟