# 技能：agent-cli-orchestrator（多AI命令行工具编排器）

**版本：** 2.0.0（2026-03-16）  
**状态：** 稳定  
**专长：** 命令行自动化、错误恢复、工具链管理  

---

## 1. 描述

`ai-cli-orchestrator` 是一个元技能，它整合了多个 AI 命令行工具（如 Gemini CLI、Cursor Agent、Claude Code），构建了一个高可用性的自动化工作流程。该技能能够智能识别当前环境中的 AI 工具链，根据任务类型分配最合适的工具，并在主要工具遇到速率限制、API 故障或逻辑瓶颈时实现无缝的任务上下文传递及自动回退。  

---

## 2. 触发场景

- **复杂的编码任务**：当需要在多个文件和模块之间进行大规模重构，且某个 AI 工具遇到性能瓶颈时。  
- **高稳定性要求**：在持续集成/持续部署（CI/CD）或自动化脚本中，任务不能因单个 AI 服务的 API 波动而中断。  
- **领域特定优化**：利用不同 AI 的优势（例如 Gemini 的长上下文处理能力、Claude 的严谨代码逻辑）。  
- **资源限制**：当主要工具触发令牌或速率限制时，需要切换到备用工具。  

---

## 3. 核心工作流程  

### 3.1 发现阶段  

1. **自动扫描**：扫描系统路径（PATH），检测已安装的 AI 命令行工具（如 `gemini`、`cursor-agent`、`claude` 等）。  
2. **可用性检查**：运行 `tool --version` 或简单的 `echo` 测试，验证 API 密钥的有效性。  
3. **环境同步**：从项目根目录读取 `.ai-config.yaml` 或 `.env` 文件，获取权限配置信息。  

### 3.2 用户配置  

#### 1. 自动扫描可用的 AI 命令行工具  
```
🤖 AI Assistant Initialization

Detected AI CLI tools:
✅ gemini - Installed
❌ cursor-agent - Not detected
✅ claude - Installed

Select tools to enable (multi-select):
[1] gemini
[2] cursor-agent  
[3] claude
[4] Add custom...
```  

#### 2. 添加自定义 AI 命令行工具  
```
Enter command name: kimi
Enter test command: kimi --version
Enter description: Moonshot AI
```  

#### 3. 设置优先级  
```
Priority (lower number = higher priority):
1. gemini
2. claude
```  

#### 4. 选择策略  
```
Choose AI response strategy:

[1] AI CLI First
    - When receiving questions, automatically use AI CLI to search for answers first

[2] Direct Response
    - Use model capabilities directly

[3] Hybrid Mode
    - Simple questions answered directly, complex questions use AI CLI
```  

### 3.3 任务调度阶段  

1. **意图识别**：分析用户输入（是研究、编码还是调试？）。  
2. **优先级匹配**：根据优先级矩阵选择合适的工具。  
3. **会话管理**：  
   - 检查是否存在关联的会话 ID。  
   - 对于连续性任务，尝试将中间输出（如差异文件或思考过程）作为上下文传递给新工具。  

### 3.4 监控与回退阶段  

1. **实时监控**：监控命令行工具的错误输出（stderr）和退出代码。  
2. **故障检测**：  
   - 出现 “速率限制”（`429 Too Many Requests`）、“过载”（`overloaded`）或 “认证错误”（`auth error`）等错误代码。  
   - 如果输出连续三次验证失败，则视为故障。  
3. **状态切换**：启动备用工具，并自动重试失败的指令。  

---

## 4. 配置示例  

在项目根目录创建 `.ai-cli-orchestrator.yaml` 文件：  
```yaml
version: "2.0"
settings:
  default_strategy: "balanced" # options: speed, quality, economy
  auto_fallback: true
  max_retries: 2

tools:
  gemini:
    priority: 1
    alias: "gemini"
    capabilities: ["long-context", "multimodal", "fast-search"]
  cursor-agent:
    priority: 2
    alias: "cursor"
    capabilities: ["codebase-indexing", "surgical-edit"]
  claude-code:
    priority: 3
    alias: "claude"
    capabilities: ["logic-reasoning", "unit-testing"]

strategies:
  balanced:
    primary: "gemini"
    secondary: "cursor-agent"
    emergency: "claude-code"
```  

---

## 5. 错误处理  

| 错误类型 | 检测方式 | 处理方式 |  
| :--- | :--- | :--- |  
| **速率限制** | `429 Too Many Requests` | 记录错误信息，切换到下一个工具，延迟 30 秒后重试。 |  
| **逻辑循环** | 同一文件被编辑三次 | 强制中断任务，输出当前上下文，并请求更高级别的工具处理。 |  
| **认证失败** | `401 Unauthorized` | 尝试使用本地备份的 `.env` 文件；如果失败，则跳过当前任务并通知用户。 |  
| **网络超时** | `ETIMEDOUT` | 重试一次；如果仍失败，则切换到离线模式或使用备用命令行工具。 |  
| **命令未找到** | `command not found` | 跳过当前工具，切换到下一个可用的工具。 |  
| **任务停滞超过 30 秒** | 超时 | 强制中断任务，切换工具并重试。 |  

---

## 6. 会话管理  

### 6.1 任务元数据  

每个任务包含以下信息：  
- 任务 ID（唯一标识符）  
- 文件快照（与任务相关的文件）  
- 命令历史记录（执行的命令）  
- 最后一次任务总结  

### 6.2 会话切换规则  

| 情况 | 处理方式 |  
|----------|--------|  
| 同一任务 | 继续在同一会话中处理，避免创建新会话 |  
| 不同任务 | 创建新会话 |  
| 返回上一个任务 | 切换到对应的会话 |  

### 6.3 上下文恢复  

切换回上一个任务时：  
1. 读取任务总结信息。  
2. 加载之前的命令历史记录。  
3. 快速恢复任务状态。  

---

## 7. AI 命令行工具的优先级  

| 优先级 | 工具 | 用途 | 备用工具 |  
|----------|------|---------|----------|  
| 1 | gemini | 主要的问答/搜索工具 | 自动切换到 `cursor-agent` 或 `claude-code` |  
| 2 | cursor-agent | 代码相关任务 | 自动切换到 `claude-code` |  
| 3 | claude-code | 用于处理错误或紧急情况 | 自动切换到 `gemini` |  

---

## 8. 最佳实践  

- **原子操作**：执行单一意图的任务，以确保在回退时能够准确传递 “最后一次成功的状态”。  
- **共享上下文**：切换工具时，始终将 `git diff` 结果或最新的 `summary.md` 文件传递给新的工具。  
- **保护凭证**：切勿将 API 密钥通过日志或 AI 提示泄露。  
- **严格验证**：无论使用哪种 AI 工具，都应使用 `npm test` 或 `ruff` 等本地工具进行验证。  
- **定期维护**：每月更新一次，确保所有命令行工具的版本是最新的。  

---

## 9. 可用的命令  

- `ai-cli-orchestrator init`：交互式配置工具链和优先级。  
- `ai-cli-orchestrator run "<task>"`：根据策略执行任务并管理其生命周期。  
- `ai-cli-orchestrator status`：查看所有 AI 服务的可用性状态。  
- `ai-cli-orchestrator session switch <id>`：在不同 AI 会话之间手动迁移数据。  

---

## 10. 可扩展性  

支持通过编写简单的适配器来集成新的 AI 命令行工具。只需提供以下功能：  
1. `detect()`：用于查找相应的工具。  
2. `execute(prompt, context)`：用于调用工具并获取其输出结果。  
3. `parse_error()`：用于解析工具返回的错误类型。  

---

## 12. 安全性与凭证管理  

### 为什么需要读取配置文件  

该技能需要读取 shell 和项目配置文件，以便：  
- 扫描系统路径中的已安装 AI 命令行工具。  
- 验证 API 密钥的有效性。  
- 读取项目特定的配置文件（如 `.ai-config.yaml`、`.env`）。  

### 凭证保护措施：  

- **仅在本地处理**：所有凭证验证操作都在用户机器上完成。  
- **禁止数据泄露**：凭证永远不会被发送到外部服务器。  
- **最小化访问权限**：仅读取必要的配置文件，绝不写入或修改它们。  
- **沙箱执行**：AI 命令行工具在隔离的进程中运行。  

### 最佳实践：  

- 始终确认哪些 AI 命令行工具有权访问用户的凭证。  
- 使用针对不同环境的 API 密钥（开发环境与生产环境分开）。  
- 定期审计已安装的 AI 命令行工具。  

---

## 11. 版本历史记录  

- v2.0.0（2026-03-16）：主要更新包括初始化配置、执行策略、会话管理以及自动回退功能的改进。