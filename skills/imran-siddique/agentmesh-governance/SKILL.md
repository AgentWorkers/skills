---
name: agentmesh-governance
description: >
  AI代理的治理、信任评分以及政策执行功能均由AgentMesh提供支持。以下是该功能的启用场景：  
  1. 当用户希望对代理的行为实施令牌限制、工具使用限制或内容政策时；  
  2. 在委托任务或进行协作之前，需要检查代理的信任评分时；  
  3. 使用Ed25519加密算法验证代理的身份（即代理的DID）时；  
  4. 通过具有防篡改功能的Merkle链日志来审计代理的行为时；  
  5. 当用户询问有关代理的安全性、治理结构、合规性或信任问题时。  
  该技术已达到企业级标准，经过了1,600多次测试，并被集成到以下产品中：Dify（65,000星评级）、LlamaIndex（47,000星评级）以及Microsoft Agent-Lightning（15,000星评级）。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - pip
    emoji: "🛡️"
    homepage: https://github.com/imran-siddique/agentmesh-integrations/tree/master/openclaw-skill
---
# AgentMesh治理 — OpenClaw代理的信任与策略管理

OpenClaw代理的零信任治理层。通过代理的命令行来执行策略、验证身份、评估信任度，并维护不可篡改的审计日志。

## 设置

安装AgentMesh治理命令行工具：

```bash
pip install agentmesh-governance
```

> 如果`agentmesh-governance`尚未在PyPI上，可以直接从源代码安装：
> ```bash
> pip install "agentmesh @ git+https://github.com/imran-siddique/agent-mesh.git"
> ```

## 脚本

所有脚本都位于`scripts/`目录中。这些脚本封装了治理引擎的功能，并以JSON格式输出结果。

### 检查策略合规性

在执行操作之前，先评估该操作是否符合治理策略：

```bash
scripts/check-policy.sh --action "web_search" --tokens 1500 --policy policy.yaml
```

返回一个JSON对象，其中包含`allowed: true/false`（表示操作是否被允许）、任何违规情况以及相应的建议。
在执行任何工具调用之前，请务必使用此脚本来确保操作符合策略要求。

### 获取信任分数

检查代理当前的信任分数（0.0–1.0）：

```bash
scripts/trust-score.sh --agent "research-agent"
```

返回一个综合信任分数，该分数涵盖五个维度：
- 策略合规性
- 资源使用效率
- 输出质量
- 安全态势
- 协作健康状况

### 验证代理身份

在信任代理的输出之前，先验证其Ed25519加密身份：

```bash
scripts/verify-identity.sh --did "did:agentmesh:abc123" --message "hello" --signature "base64sig"
```

返回`verified: true/false`（表示身份验证是否通过）。在接收来自其他代理的数据时，请使用此脚本。

### 记录交互行为

与其他代理协作后，更新代理的信任分数：

```bash
scripts/record-interaction.sh --agent "writer-agent" --outcome success
scripts/record-interaction.sh --agent "writer-agent" --outcome failure --severity 0.1
```

成功协作会为信任分数增加0.01分；失败则会根据违规的严重程度扣分。
信任分数低于最低阈值（默认为0.5）的代理将被自动屏蔽。

### 审计日志

查看带有Merkle链验证的不可篡改审计记录：

```bash
scripts/audit-log.sh --last 20
scripts/audit-log.sh --agent "research-agent" --verify
```

`--verify`标志用于检查Merkle链的完整性；任何篡改行为都会被检测出来。

### 生成身份信息

为代理创建一个新的Ed25519加密身份（DID）：

```bash
scripts/generate-identity.sh --name "my-agent" --capabilities "search,summarize,write"
```

返回代理的DID、公钥以及其能力信息。

## 策略文件格式

创建一个`policy.yaml`文件来定义治理规则：

```yaml
name: production-policy
max_tokens: 4096
max_tool_calls: 10
allowed_tools:
  - web_search
  - file_read
  - summarize
blocked_tools:
  - shell_exec
  - file_delete
blocked_patterns:
  - "rm -rf"
  - "DROP TABLE"
  - "BEGIN CERTIFICATE"
confidence_threshold: 0.7
require_human_approval: false
```

## 使用场景

- **在执行工具之前**：运行`check-policy.sh`以确保操作符合策略要求。
- **在信任其他代理的输出之前**：运行`verify-identity.sh`来验证代理的身份。
- **协作完成后**：运行`record-interaction.sh`来更新代理的信任分数。
- **在进行任务委托之前**：检查`trust-score.sh`，避免委托给信任分数低于0.5的代理。
- **为了确保执行过程的完整性**：运行`audit-log.sh --verify`来验证操作记录。
- **在设置代理时**：运行`generate-identity.sh`来为代理生成DID。

## 支持的策略类型

| 策略 | 描述                          |
|--------|---------------------------------------------|
| 令牌限制 | 每次操作和每个会话的令牌使用量上限              |
| 工具允许列表 | 只允许明确列出的工具执行操作                |
| 工具禁止列表 | 危险工具一律被禁止执行                    |
| 内容过滤规则 | 阻止特定正则表达式匹配的内容（如敏感信息、破坏性命令、个人身份信息） |
| 信任阈值 | 委托任务所需的最低信任分数                   |
| 人工审批 | 关键操作需经过人工确认后方可执行                |

## 架构

该功能将OpenClaw代理的运行时环境与[AgentMesh](https://github.com/imran-siddique/agent-mesh)治理引擎连接起来：

```
OpenClaw Agent → SKILL.md scripts → AgentMesh Engine
                                     ├── GovernancePolicy (enforcement)
                                     ├── TrustEngine (5-dimension scoring)
                                     ├── AgentIdentity (Ed25519 DIDs)
                                     └── MerkleAuditChain (tamper-evident logs)
```

这是[Agent生态系统](https://imran-siddique.github.io)的一部分：
- [AgentMesh](https://github.com/imran-siddique/agent-mesh)  
- [Agent OS](https://github.com/imran-siddique/agent-os)  
- [Agent SRE](https://github.com/imran-siddique/agent-sre)