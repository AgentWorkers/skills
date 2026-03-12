# Network-AI 技能简介  
**描述：** 一种基于 Python 的编排技能，支持通过黑板文件（blackboard file）、权限控制（permission gating）和令牌预算（token budget）脚本来管理本地多代理工作流程。所有执行操作均为本地化处理，无需网络调用，也不依赖 Node.js。TypeScript/Node.js 相关功能（如 HMAC 令牌、AES-256 加密、MCP 服务器、15 个适配器以及 CLI）包含在独立的 npm 包中（`npm install -g network-ai`），不属于此技能包的组成部分。  

## 元数据（Metadata）  
```json
openclaw:  
  emoji: "\U0001F41D"  
  homepage: https://github.com/Jovancoding/Network-AI  
  bundle_scope: "仅包含 Python 脚本（scripts/*.py）"  
  sessions_ops: "由 OpenClaw 平台提供——`sessions_send`、`sessions_list` 和 `sessions_history` 是 OpenClaw 的内置功能，不由本技能的 Python 脚本实现或调用"  
  requires:  
    bins: [python3]  
  optionalBins: []  
  env:  
    SWARM_TOKEN_SECRET:  
      required: false  
      description: "仅用于 Node.js MCP 服务器——本 Python 脚本不使用"  
    SWARM_ENCRYPTION_KEY:  
      required: false  
    OPENAI_API_KEY:  
      required: false  
    MINIMAX_API_KEY:  
      required: false  
  privacy:  
    audit_log:  
      path: "data/audit_log.jsonl"  
      scope: "仅限本地"  
      description: "记录操作元数据的本地 JSONL 文件（包含 agentId、action、timestamp、outcome）"  
```

## Swarm 编排器技能（Swarm Orchestrator Skill）  
**技能范围：** 所有指令均通过本地 Python 脚本（`scripts/*.py`）执行，不进行网络调用。令牌基于 UUID（格式为 `grant_{uuid4().hex}`）存储在 `data/active_grants.json` 文件中。审计日志采用简单的 JSONL 格式（`data/audit_log.jsonl`）记录；Python 层不进行 HMAC 签名。HMAC 签名的令牌、AES-256 加密以及独立的 MCP 服务器等功能均属于配套的 Node.js 包（`npm install -g network-ai`），并未在这些 Python 脚本中实现。  

### 设置（Setup）  
**无需安装 pip。** 所有脚本仅使用 Python 标准库，不依赖第三方包。**  
> **关于 `requirements.txt`：** 该文件仅用于文档说明，列出了使用的标准库模块，**无强制依赖项**。无需运行 `pip install -r requirements.txt`。  

**示例用法：**  
```bash
# 先确保已安装 python3（版本 ≥ 3.8）  
python3 --version  

# 直接运行脚本：  
python3 scripts/blackboard.py list  
python3 scripts/swarm_guard.py budget-init --task-id "task_001" --budget 10000  

# （可选）：在 Windows 环境中用于文件锁定：  
pip install filelock  
```  

**注意：** `data/` 目录会在首次运行时自动创建。无需配置文件、环境变量或凭据。  

### 多代理协调系统（Multi-Agent Coordination System）  
适用于需要任务分解、并行执行以及对敏感 API 进行权限控制访问的复杂工作流程。  

### 编排器系统指令（Orchestrator System Instructions）  
**作为编排器代理（Orchestrator Agent），** 负责将复杂任务分解为多个子任务，分配给相应代理，并整合最终结果：  
1. **将复杂请求分解为 3 个子任务**  
2. **使用基于预算的传递协议进行任务分配**  
3. **在提交结果前在黑板上验证**  
4. **只有在所有验证通过后才能合成最终输出**  

### 预先要求（Prerequisites）  
- **Python 3.8 或更高版本**  
- **无需额外安装第三方包**  

### 使用说明（Usage Instructions）  
- **首先初始化预算**  
  ```bash  
  python3 scripts/swarm_guard.py budget-init --task-id "task_001" --budget 10000 --description "Q4 财务分析"  
  ```  
- **根据需要使用 OpenClaw 平台工具进行任务分配**  
  ```bash  
  # 先检查预算  
  python3 scripts/swarm_guard.py intercept-handoff ...  
  # 然后使用 OpenClaw 平台工具分配任务  
  ```  
- **在访问 API 之前检查权限**  
  ```bash  
  python {baseDir}/scripts/check_permission.py ...  
  ```  

### 黑板（Blackboard）  
用于实时代理间协调的共享 markdown 文件，包含任务结果、令牌、状态标志和基于 TTL 的缓存条目。  

### 三层内存模型（Three-Layer Memory Model）  
每个代理都有三层内存：  
- **代理上下文（Agent Context）**：仅包含当前任务的临时信息，由 OpenClaw/LLM 平台自动管理。  
- **黑板（Blackboard）**：跨代理共享的状态信息，条目会自动过期。  
- **项目上下文（Project Context）**：包含所有代理需要了解的长期信息。  

### 快速启动（Quick Start）  
1. 初始化预算。  
2. 根据预算分配任务。  
3. 检查权限后执行任务。  
4. 使用黑板协调代理间的状态。  

### 安全性考虑（Security Considerations）  
- **始终检查权限**，确保遵循权限规则。  
- **自动记录审计日志**，以便追踪操作。  

### 附录：可选的 Node.js 伴侣包（Appendix: Optional Node.js Companion）  
> 该 npm 包提供了额外的功能（如 HMAC 签名、AES-256 加密等），但不是此技能包的必备部分。