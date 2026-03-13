---
name: agent-governance
description: >
  为AI代理系统添加治理、安全性和信任控制的相关模式与技术。在以下情况下可运用这些技能：
  - 构建需要调用外部工具（API、数据库、文件系统）的AI代理
  - 为代理工具的使用实施基于策略的访问控制
  - 添加语义意图分类功能以检测危险指令
  - 为多代理工作流程创建信任评分系统
  - 为代理的行为和决策建立审计追踪机制
  - 对代理实施速率限制、内容过滤或工具使用限制
  - 与任何代理框架（如PydanticAI、CrewAI、OpenAI Agents、LangChain、AutoGen）进行开发
---
# 代理治理模式  
（Agent Governance Patterns）  

这些模式旨在为人工智能代理系统添加安全性、信任机制以及政策执行功能。  

## 概述  
治理模式确保人工智能代理在预定义的范围内运行：控制它们可以调用的工具、可以处理的内容、能够执行的操作，并通过审计日志来维护责任追溯性。  

```
User Request → Intent Classification → Policy Check → Tool Execution → Audit Log
                     ↓                      ↓               ↓
              Threat Detection         Allow/Deny      Trust Update
```  

## 适用场景  
- **具有工具访问权限的代理**：任何调用外部工具（API、数据库、shell命令）的代理  
- **多代理系统**：需要设定信任边界的代理之间的协作  
- **生产环境部署**：满足合规性、审计和安全要求  
- **敏感操作**：金融交易、数据访问、基础设施管理  

---

## 模式 1：治理策略（Governance Policy）  
将代理的允许操作定义为一个可组合、可序列化的策略对象。  

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import re

class PolicyAction(Enum):
    ALLOW = "allow"
    DENY = "deny"
    REVIEW = "review"  # flag for human review

@dataclass
class GovernancePolicy:
    """Declarative policy controlling agent behavior."""
    name: str
    allowed_tools: list[str] = field(default_factory=list)       # allowlist
    blocked_tools: list[str] = field(default_factory=list)       # blocklist
    blocked_patterns: list[str] = field(default_factory=list)    # content filters
    max_calls_per_request: int = 100                             # rate limit
    require_human_approval: list[str] = field(default_factory=list)  # tools needing approval

    def check_tool(self, tool_name: str) -> PolicyAction:
        """Check if a tool is allowed by this policy."""
        if tool_name in self.blocked_tools:
            return PolicyAction.DENY
        if tool_name in self.require_human_approval:
            return PolicyAction.REVIEW
        if self.allowed_tools and tool_name not in self.allowed_tools:
            return PolicyAction.DENY
        return PolicyAction.ALLOW

    def check_content(self, content: str) -> Optional[str]:
        """Check content against blocked patterns. Returns matched pattern or None."""
        for pattern in self.blocked_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return pattern
        return None
```  

### 策略组合  
（Policy Composition）  
可以组合多个策略（例如：组织级策略 + 团队级策略 + 代理级策略）：  
```python
def compose_policies(*policies: GovernancePolicy) -> GovernancePolicy:
    """Merge policies with most-restrictive-wins semantics."""
    combined = GovernancePolicy(name="composed")

    for policy in policies:
        combined.blocked_tools.extend(policy.blocked_tools)
        combined.blocked_patterns.extend(policy.blocked_patterns)
        combined.require_human_approval.extend(policy.require_human_approval)
        combined.max_calls_per_request = min(
            combined.max_calls_per_request,
            policy.max_calls_per_request
        )
        if policy.allowed_tools:
            if combined.allowed_tools:
                combined.allowed_tools = [
                    t for t in combined.allowed_tools if t in policy.allowed_tools
                ]
            else:
                combined.allowed_tools = list(policy.allowed_tools)

    return combined


# Usage: layer policies from broad to specific
org_policy = GovernancePolicy(
    name="org-wide",
    blocked_tools=["shell_exec", "delete_database"],
    blocked_patterns=[r"(?i)(api[_-]?key|secret|password)\s*[:=]"],
    max_calls_per_request=50
)
team_policy = GovernancePolicy(
    name="data-team",
    allowed_tools=["query_db", "read_file", "write_report"],
    require_human_approval=["write_report"]
)
agent_policy = compose_policies(org_policy, team_policy)
```  

### 以 YAML 格式存储策略  
（Store Policies as YAML）  
将策略作为配置文件存储，而非代码：  
```yaml
# governance-policy.yaml
name: production-agent
allowed_tools:
  - search_documents
  - query_database
  - send_email
blocked_tools:
  - shell_exec
  - delete_record
blocked_patterns:
  - "(?i)(api[_-]?key|secret|password)\\s*[:=]"
  - "(?i)(drop|truncate|delete from)\\s+\\w+"
max_calls_per_request: 25
require_human_approval:
  - send_email
```  
```python
import yaml

def load_policy(path: str) -> GovernancePolicy:
    with open(path) as f:
        data = yaml.safe_load(f)
    return GovernancePolicy(**data)
```  

---

## 模式 2：语义意图分类  
（Semantic Intent Classification）  
在请求到达代理之前，利用基于模式的信号检测其中的危险意图。  

**关键点**：意图分类发生在工具执行之前，起到预检的安全保障作用。这与仅在结果生成后进行检查的输出防护机制截然不同。  

---

## 模式 3：工具级治理装饰器  
（Tool-Level Governance Decorator）  
为每个工具功能添加治理检查功能：  
```python
import functools
import time
from collections import defaultdict

_call_counters: dict[str, int] = defaultdict(int)

def govern(policy: GovernancePolicy, audit_trail=None):
    """Decorator that enforces governance policy on a tool function."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            tool_name = func.__name__

            # 1. Check tool allowlist/blocklist
            action = policy.check_tool(tool_name)
            if action == PolicyAction.DENY:
                raise PermissionError(f"Policy '{policy.name}' blocks tool '{tool_name}'")
            if action == PolicyAction.REVIEW:
                raise PermissionError(f"Tool '{tool_name}' requires human approval")

            # 2. Check rate limit
            _call_counters[policy.name] += 1
            if _call_counters[policy.name] > policy.max_calls_per_request:
                raise PermissionError(f"Rate limit exceeded: {policy.max_calls_per_request} calls")

            # 3. Check content in arguments
            for arg in list(args) + list(kwargs.values()):
                if isinstance(arg, str):
                    matched = policy.check_content(arg)
                    if matched:
                        raise PermissionError(f"Blocked pattern detected: {matched}")

            # 4. Execute and audit
            start = time.monotonic()
            try:
                result = await func(*args, **kwargs)
                if audit_trail is not None:
                    audit_trail.append({
                        "tool": tool_name,
                        "action": "allowed",
                        "duration_ms": (time.monotonic() - start) * 1000,
                        "timestamp": time.time()
                    })
                return result
            except Exception as e:
                if audit_trail is not None:
                    audit_trail.append({
                        "tool": tool_name,
                        "action": "error",
                        "error": str(e),
                        "timestamp": time.time()
                    })
                raise

        return wrapper
    return decorator


# Usage with any agent framework
audit_log = []
policy = GovernancePolicy(
    name="search-agent",
    allowed_tools=["search", "summarize"],
    blocked_patterns=[r"(?i)password"],
    max_calls_per_request=10
)

@govern(policy, audit_trail=audit_log)
async def search(query: str) -> str:
    """Search documents — governed by policy."""
    return f"Results for: {query}"

# Passes: search("latest quarterly report")
# Blocked: search("show me the admin password")
```  

---

## 模式 4：信任评分  
（Trust Scoring）  
通过信任评分来跟踪代理的可靠性（评分会随时间逐渐降低）：  
```python
from dataclasses import dataclass, field
import math
import time

@dataclass
class TrustScore:
    """Trust score with temporal decay."""
    score: float = 0.5          # 0.0 (untrusted) to 1.0 (fully trusted)
    successes: int = 0
    failures: int = 0
    last_updated: float = field(default_factory=time.time)

    def record_success(self, reward: float = 0.05):
        self.successes += 1
        self.score = min(1.0, self.score + reward * (1 - self.score))
        self.last_updated = time.time()

    def record_failure(self, penalty: float = 0.15):
        self.failures += 1
        self.score = max(0.0, self.score - penalty * self.score)
        self.last_updated = time.time()

    def current(self, decay_rate: float = 0.001) -> float:
        """Get score with temporal decay — trust erodes without activity."""
        elapsed = time.time() - self.last_updated
        decay = math.exp(-decay_rate * elapsed)
        return self.score * decay

    @property
    def reliability(self) -> float:
        total = self.successes + self.failures
        return self.successes / total if total > 0 else 0.0


# Usage in multi-agent systems
trust = TrustScore()

# Agent completes tasks successfully
trust.record_success()  # 0.525
trust.record_success()  # 0.549

# Agent makes an error
trust.record_failure()  # 0.467

# Gate sensitive operations on trust
if trust.current() >= 0.7:
    # Allow autonomous operation
    pass
elif trust.current() >= 0.4:
    # Allow with human oversight
    pass
else:
    # Deny or require explicit approval
    pass
```  

**多代理信任机制**：在代理之间进行协作时，每个代理都会为其协作者维护信任评分：  
```python
class AgentTrustRegistry:
    def __init__(self):
        self.scores: dict[str, TrustScore] = {}

    def get_trust(self, agent_id: str) -> TrustScore:
        if agent_id not in self.scores:
            self.scores[agent_id] = TrustScore()
        return self.scores[agent_id]

    def most_trusted(self, agents: list[str]) -> str:
        return max(agents, key=lambda a: self.get_trust(a).current())

    def meets_threshold(self, agent_id: str, threshold: float) -> bool:
        return self.get_trust(agent_id).current() >= threshold
```  

---

## 模式 5：审计日志  
（Audit Trail）  
为所有代理操作生成只读的审计日志——这对合规性和故障排查至关重要：  
```python
from dataclasses import dataclass, field
import json
import time

@dataclass
class AuditEntry:
    timestamp: float
    agent_id: str
    tool_name: str
    action: str           # "allowed", "denied", "error"
    policy_name: str
    details: dict = field(default_factory=dict)

class AuditTrail:
    """Append-only audit trail for agent governance events."""
    def __init__(self):
        self._entries: list[AuditEntry] = []

    def log(self, agent_id: str, tool_name: str, action: str,
            policy_name: str, **details):
        self._entries.append(AuditEntry(
            timestamp=time.time(),
            agent_id=agent_id,
            tool_name=tool_name,
            action=action,
            policy_name=policy_name,
            details=details
        ))

    def denied(self) -> list[AuditEntry]:
        """Get all denied actions — useful for security review."""
        return [e for e in self._entries if e.action == "denied"]

    def by_agent(self, agent_id: str) -> list[AuditEntry]:
        return [e for e in self._entries if e.agent_id == agent_id]

    def export_jsonl(self, path: str):
        """Export as JSON Lines for log aggregation systems."""
        with open(path, "w") as f:
            for entry in self._entries:
                f.write(json.dumps({
                    "timestamp": entry.timestamp,
                    "agent_id": entry.agent_id,
                    "tool": entry.tool_name,
                    "action": entry.action,
                    "policy": entry.policy_name,
                    **entry.details
                }) + "\n")
```  

---

## 模式 6：框架集成  
（Framework Integration）  
- **PydanticAI**  
- **CrewAI**  
- **OpenAI Agents SDK**  
---  

---

## 治理级别  
（Governance Levels）  
根据风险程度调整治理的严格程度：  
| 级别 | 控制措施 | 适用场景 |  
|-------|----------|----------|  
| **开放级（Open）** | 仅进行审计，无其他限制 | 内部开发/测试环境 |  
| **标准级（Standard）** | 工具白名单 + 内容过滤 | 通用生产环境代理 |  
| **严格级（Strict）** | 所有控制措施 + 敏感操作的需人工审批 | 金融、医疗、法律领域 |  
| **锁定级（Locked）** | 仅允许使用白名单中的工具，禁止使用动态工具，进行全面审计 | 需高度合规的系统 |  

---

## 最佳实践  
（Best Practices）  
| 实践建议 | 原因说明 |  
|----------|-----------|  
| **将策略作为配置文件存储** | 以 YAML/JSON 格式存储策略，避免硬编码——便于随时修改而无需重新部署 |  
| **最严格的策略优先** | 在组合策略时，始终拒绝未经授权的请求 |  
| **执行前进行意图检查** | 在工具执行前对意图进行分类，而非之后 |  
| **信任评分机制** | 信任评分应随时间下降——鼓励代理持续保持良好行为 |  
| **只读审计日志** | 禁止修改或删除审计记录——数据不可变性有助于确保合规性 |  
| **错误时拒绝操作** | 如果治理检查失败，直接拒绝请求而非允许其执行 |  
| **分离策略与逻辑** | 治理机制应独立于代理的业务逻辑 |  

---

## 快速入门检查清单  
（Quick Start Checklist）  
```markdown
## Agent Governance Implementation Checklist

### Setup
- [ ] Define governance policy (allowed tools, blocked patterns, rate limits)
- [ ] Choose governance level (open/standard/strict/locked)
- [ ] Set up audit trail storage

### Implementation
- [ ] Add @govern decorator to all tool functions
- [ ] Add intent classification to user input processing
- [ ] Implement trust scoring for multi-agent interactions
- [ ] Wire up audit trail export

### Validation
- [ ] Test that blocked tools are properly denied
- [ ] Test that content filters catch sensitive patterns
- [ ] Test rate limiting behavior
- [ ] Verify audit trail captures all events
- [ ] Test policy composition (most-restrictive-wins)
```  

---

## 相关资源  
（Related Resources）  
- [Agent-OS 治理框架](https://github.com/imran-siddique/agent-os) — 完整的治理框架  
- [AgentMesh 集成方案](https://github.com/imran-siddique/agentmesh-integrations) — 适用于特定框架的插件  
- [OWASP 针对大型语言模型应用的十大安全建议](https://owasp.org/www-project-top-10-for-large-language-model-applications/)