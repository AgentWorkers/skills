---
name: symbiont
title: Symbiont
description: >
  这款AI原生代理运行时具备以下特性：  
  - 基于TypeState的强制型ORGAL推理循环（typestate-enforced ORGA reasoning loop）  
  - Cedar策略授权机制（Cedar policy authorization）  
  - 知识桥接功能（knowledge bridge）  
  - 零信任安全模型（zero-trust security）  
  - 多层沙箱环境（multi-tier sandboxing）  
  - Webhook验证机制（webhook verification）  
  - 支持Markdown格式的数据存储（markdown memory）  
  - 技能扫描功能（skill scanning）  
  - 提供详细的性能指标（metrics）  
  - 具备强大的调度能力（scheduling capabilities）  
  - 支持声明式DSL（declarative DSL）  
  此外，该运行时还支持以下高级特性：  
  - AI原生代理架构（AI-native agent architecture）  
  - 强化型安全防护机制（enhanced security features）  
  - 高效的任务管理功能（efficient task management）  
  - 与现有系统的集成能力（integration with existing systems）  
  - 可扩展性设计（scalable architecture）
version: 1.5.0
---
# Symbiont代理开发技能指南

**目的**：本指南帮助AI助手快速构建安全、合规的Symbiont代理，并遵循最佳实践。

**完整文档请参阅**：[DSL指南](https://github.com/thirdkeyai/symbiont/blob/main/docs/dsl-guide.md)、[DSL规范](https://github.com/thirdkeyai/symbiont/blob/main/docs/dsl-specification.md)以及[示例代理](https://github.com/thirdkeyai/symbiont/blob/main/agents/README.md)。

## Symbiont的独特之处

- **ORGA推理循环**：由typestate强制执行的观察-推理-决策-执行周期，具有编译时安全性
- **Cedar策略授权**：通过`cedar-policy` crate的`Authorizer::is_authorized()`进行正式的策略评估
- **知识桥**：基于向量的检索和自动学习持久化的上下文感知推理
- **持久化日志**：记录所有7种循环事件类型，以便在发生故障时无需重新调用LLM即可恢复和回放
- **零信任安全**：默认情况下所有输入均不受信任，需要明确的策略
- **策略即代码**：在运行时执行声明性安全规则
- **多层沙箱**：Docker → gVisor → Firecracker隔离
- **企业合规性**：内置HIPAA、SOC2、GDPR模式
- **加密验证**：MCP工具使用SchemaPin，代理身份使用AgentPin，Ed25519签名
- **Webhook DX**：带有GitHub/Stripe/Slack预设的签名验证中间件
- **持久化内存**：基于Markdown的代理内存，支持保留和压缩

---

## 快速启动模板

### 最小可行代理

```dsl
metadata {
    version = "1.0.0"
    author = "Your Name"
    description = "Brief description of what this agent does"
    tags = ["category", "use-case"]
}

agent my_agent(input: String) -> String {
    capabilities = ["process_data", "validate_input"]

    policy security_policy {
        // Allow specific operations
        allow: ["read_input", "write_output"] if input.length() < 10000

        // Deny dangerous operations
        deny: ["network_access", "file_system"] if true

        // Require conditions
        require: {
            input_validation: true,
            output_sanitization: true
        }

        // Audit important actions
        audit: {
            log_level: "info",
            include_input: false,  // Don't log sensitive data
            include_output: true
        }
    }

    with memory = "ephemeral", security = "high", timeout = 30000 {
        try {
            // Validate input
            if input.is_empty() {
                return error("Input cannot be empty");
            }

            // Process data
            let result = process(input);

            // Return result
            return result;

        } catch (error) {
            log("ERROR", "Processing failed: " + error.message);
            return error("Processing failed");
        }
    }
}

fn process(data: String) -> String {
    // Your processing logic here
    return data.to_uppercase();
}
```

---

## 代理推理循环（ORGA循环）

推理循环通过typestate强制执行的周期来驱动代理的自主行为：

1. **观察** — 从之前的工具执行中收集结果
2. **推理** — LLM生成建议的操作（工具调用或文本响应）
3. **决策** — 策略引擎评估每个建议的操作
4. **执行** — 被批准的操作被发送到工具执行器

### 最小化推理循环

```rust
use std::sync::Arc;
use symbi_runtime::reasoning::{
    ReasoningLoopRunner, LoopConfig, Conversation, ConversationMessage,
    circuit_breaker::CircuitBreakerRegistry,
    context_manager::DefaultContextManager,
    executor::DefaultActionExecutor,
    loop_types::BufferedJournal,
    policy_bridge::DefaultPolicyGate,
};
use symbi_runtime::types::AgentId;

let runner = ReasoningLoopRunner {
    provider: Arc::new(my_inference_provider),
    policy_gate: Arc::new(DefaultPolicyGate::permissive()),
    executor: Arc::new(DefaultActionExecutor::default()),
    context_manager: Arc::new(DefaultContextManager::default()),
    circuit_breakers: Arc::new(CircuitBreakerRegistry::default()),
    journal: Arc::new(BufferedJournal::new(1000)),
    knowledge_bridge: None, // Optional: add KnowledgeBridge for RAG
};

let mut conv = Conversation::with_system("You are a helpful agent.");
conv.push(ConversationMessage::user("What is 6 * 7?"));

let result = runner
    .run(AgentId::new(), conv, LoopConfig::default())
    .await;
```

### 编译时安全性的阶段转换

无效的转换在编译时被捕获：

```
Reasoning → PolicyCheck → ToolDispatching → Observing → Reasoning (loop)
                                                      → Complete (exit)
```

### 日志事件

日志记录所有7种事件类型，以确保持久性：

| 事件 | 时间 | 目的 |
|-------|------|---------|
| `Started` | 循环开始 | 配置快照 |
| `ReasoningComplete` | LLM响应后，策略检查之前 | 发生故障时无需重新调用LLM即可恢复 |
| `PolicyEvaluated` | 策略检查后 | 操作计数，拒绝计数 |
| `ToolsDispatched` | 工具执行后 | 工具计数，墙钟持续时间 |
| `ObservationsCollected` | 收集结果后 | 观察结果计数 |
| `Terminated` | 循环结束 | 原因，迭代次数，使用情况，持续时间 |
| `RecoveryTriggered` | 工具失败后恢复 | 恢复策略，错误上下文 |

### Cedar策略决策（功能：`cedar`）

使用`cedar-policy` crate进行正式授权：

```rust
use symbi_runtime::reasoning::cedar_gate::{CedarPolicyGate, CedarPolicy};

let gate = CedarPolicyGate::deny_by_default();

// Cedar policies use entity types: Agent (principal), Action (action), Resource (resource)
gate.add_policy(CedarPolicy {
    name: "allow_respond".into(),
    source: r#"permit(principal, action == Action::"respond", resource);"#.into(),
    active: true,
}).await;

gate.add_policy(CedarPolicy {
    name: "deny_search".into(),
    source: r#"forbid(principal, action == Action::"tool_call::search", resource);"#.into(),
    active: true,
}).await;
```

操作映射：`tool_call::<name>`、`respond`、`delegate::<target>`、`terminate`。

Cedar语义强制执行：禁止覆盖，允许，错误时跳过。

### 知识桥（可选）

添加基于向量的检索的上下文感知推理：

```rust
use symbi_runtime::reasoning::KnowledgeBridge;

let bridge = Arc::new(KnowledgeBridge::new(knowledge_config));

let runner = ReasoningLoopRunner {
    // ... other fields ...
    knowledge_bridge: Some(bridge),
};
```

该桥在每个推理步骤之前注入相关上下文，并在循环完成后持久化学习结果。

---

## 以安全为先的策略模式

### 1. 数据处理代理（读取/转换/写入）

```dsl
policy data_processing_policy {
    // Allow data operations with size limits
    allow: [
        "read_data",
        "transform_data",
        "write_output"
    ] if request.data_size < 10_000_000  // 10MB limit

    // Deny dangerous operations
    deny: [
        "execute_code",
        "spawn_process",
        "network_access"
    ] if true

    // Require validation
    require: {
        input_validation: true,
        output_sanitization: true,
        rate_limiting: "100/minute"
    }

    // Audit with PII protection
    audit: {
        log_level: "info",
        include_input: false,      // Protect PII
        include_output: false,     // Protect PII
        include_metadata: true,
        retention_days: 90
    }
}
```

### 2. API集成代理（外部调用）

```dsl
policy api_integration_policy {
    // Allow specific endpoints only
    allow: [
        "https_request"
    ] if request.url.starts_with("https://api.trusted-service.com/")

    // Deny everything else
    deny: [
        "http_request",           // Only HTTPS
        "file_access",
        "database_access"
    ] if true

    // Require security measures
    require: {
        tls_verification: true,
        api_key_rotation: "30_days",
        rate_limiting: "1000/hour",
        timeout: "5000ms"
    }

    // Audit all API calls
    audit: {
        log_level: "info",
        include_request_headers: true,
        include_response_status: true,
        include_latency: true,
        alert_on_errors: true
    }
}
```

### 3. 安全扫描代理（审计/合规）

```dsl
policy security_scanner_policy {
    // Allow read-only scanning
    allow: [
        "read_files",
        "analyze_code",
        "check_dependencies",
        "validate_configs"
    ] if scan.depth <= 5  // Limit recursion

    // Deny modifications
    deny: [
        "write_files",
        "modify_permissions",
        "execute_code"
    ] if true

    // Require strict controls
    require: {
        signature_verification: true,
        checksum_validation: true,
        sandbox_tier: "Tier2",  // gVisor isolation
        max_scan_time: "300000ms"  // 5 minutes
    }

    // Audit findings
    audit: {
        log_level: "warning",
        include_findings: true,
        include_risk_scores: true,
        alert_on_critical: true,
        compliance_tags: ["HIPAA", "SOC2"]
    }
}
```

### 4. 工作流编排代理（多步骤）

```dsl
policy orchestration_policy {
    // Allow agent coordination
    allow: [
        "invoke_agent",
        "message_passing",
        "state_management"
    ] if orchestration.depth < 10  // Prevent infinite loops

    // Deny resource-intensive ops
    deny: [
        "spawn_unlimited_agents",
        "recursive_orchestration"
    ] if true

    // Require controls
    require: {
        max_concurrent_agents: 50,
        total_timeout: "600000ms",  // 10 minutes
        failure_recovery: "retry_with_backoff",
        circuit_breaker: true
    }

    // Audit workflow
    audit: {
        log_level: "info",
        include_workflow_graph: true,
        include_timing: true,
        include_dependencies: true,
        trace_id: true
    }
}
```

---

## 沙箱层级选择指南

| 层级 | 技术 | 使用场景 | 性能 | 安全性 | 开销 |
|------|------------|----------|-------------|----------|----------|
| **Tier1** | Docker | 通用工作负载 | 快速 | 良好 | 低（约100毫秒） |
| **Tier2** | gVisor | 不受信任的代码 | 中等 | 高 | 中等（约500毫秒） |
| **Tier3** | Firecracker | 多租户隔离 | 较慢 | 最高 | 高（约2秒） |
| **Native** | 仅限进程 | 仅限开发 | 最快 | 无 | 最小 |

**选择指南**：
- **Tier1（Docker）**：大多数代理的默认选择
- **Tier2（gVisor）**：处理外部数据，用户提供的代码
- **Tier3（Firecracker）**：高度敏感，需要合规性
- **Native**：切勿在生产环境中使用（仅限开发/测试）

---

## DSL语法速查表

### 类型系统

```dsl
// Primitives
let name: String = "value";
let count: Integer = 42;
let price: Float = 19.99;
let active: Boolean = true;
let data: Bytes = [0x01, 0x02, 0x03];

// Collections
let tags: Array<String> = ["tag1", "tag2"];
let config: Map<String, String> = {"key": "value"};
let unique: Set<Integer> = {1, 2, 3};

// Security-Aware Types
let sensitive: EncryptedData<String> = encrypt("secret");
let private_data: PrivateData<Integer> = private(123);
let verified: VerifiableResult<String> = sign("data");

// Optional Types
let optional: Optional<String> = Some("value");
let none_value: Optional<String> = None;
```

### 控制流

```dsl
// If/Else
if condition {
    // true branch
} else if other_condition {
    // else if branch
} else {
    // false branch
}

// Match (Pattern Matching)
match value {
    Some(x) => process(x),
    None => default_value,
    Error(e) => handle_error(e)
}

// Loops
for item in collection {
    process(item);
}

while condition {
    do_work();
}

// Error Handling
try {
    risky_operation();
} catch (error) {
    log("ERROR", error.message);
    return error("Operation failed");
}
```

### 策略语言

```dsl
policy policy_name {
    // Allow operations with conditions
    allow: ["operation1", "operation2"] if condition
    allow: "operation3" if complex.condition && other.check

    // Deny operations
    deny: ["dangerous_op"] if true
    deny: "risky_op" if environment == "production"

    // Required conditions
    require: {
        authentication: true,
        authorization: "role:admin",
        encryption: "AES-256-GCM",
        rate_limit: "100/second"
    }

    // Audit specification
    audit: {
        log_level: "info" | "warning" | "error",
        include_input: boolean,
        include_output: boolean,
        retention_days: integer,
        compliance_tags: array<string>
    }
}
```

### With块（执行上下文）

```dsl
with
    memory = "ephemeral" | "persistent",
    privacy = "strict" | "medium" | "low",
    security = "high" | "medium" | "low",
    sandbox = "Tier1" | "Tier2" | "Tier3",
    timeout = milliseconds,
    requires = ["clearance:level5", "approval:manager"]
{
    // Agent implementation
}
```

---

## 集成模式

### 1. 秘密管理（Vault/OpenBao）

```dsl
agent secure_api_caller(endpoint: String) -> String {
    policy secret_access {
        allow: ["read_secret"] if secret.path.starts_with("application/")
        deny: ["write_secret", "delete_secret"] if true

        require: {
            vault_auth: true,
            token_rotation: "1_hour"
        }

        audit: {
            log_level: "warning",
            include_secret_path: true,
            include_secret_value: false  // NEVER log secrets
        }
    }

    with memory = "ephemeral", security = "high" {
        // Reference secrets using vault:// protocol
        let api_key = vault://application/api/key;
        let api_secret = vault://application/api/secret;

        // Use secrets in API call
        let response = http.post(endpoint, {
            headers: {
                "Authorization": "Bearer " + api_key,
                "X-API-Secret": api_secret
            }
        });

        return response.body;
    }
}
```

### 2. MCP工具集成（加密验证）

```dsl
agent mcp_tool_user(tool_name: String, input: String) -> String {
    capabilities = ["invoke_mcp_tool"]

    policy mcp_security {
        // Only allow verified tools
        allow: ["mcp_invoke"] if tool.verified == true
        deny: ["mcp_invoke"] if tool.signature_invalid

        require: {
            schema_pin_verification: true,  // ECDSA P-256
            tofu_trust_model: true,         // Trust-On-First-Use
            tool_review_required: false     // Auto for signed tools
        }

        audit: {
            log_level: "info",
            include_tool_signature: true,
            include_tool_schema: true
        }
    }

    with security = "high" {
        // Discover and invoke MCP tool
        let tool = mcp.discover(tool_name);

        // Verify cryptographic signature
        if !tool.verify_signature() {
            return error("Tool signature verification failed");
        }

        // Invoke tool
        let result = mcp.invoke(tool, input);
        return result;
    }
}
```

### 3. HTTP Webhook处理

```dsl
agent webhook_processor(request: HttpRequest) -> HttpResponse {
    capabilities = ["process_webhook", "validate_signature"]

    policy webhook_policy {
        allow: ["parse_json", "validate_data"] if request.size < 1_000_000
        deny: ["execute_code", "file_access"] if true

        require: {
            signature_verification: true,
            rate_limiting: "1000/minute",
            timeout: "5000ms"
        }

        audit: {
            log_level: "info",
            include_request_id: true,
            include_source_ip: true,
            alert_on_invalid_signature: true
        }
    }

    with memory = "ephemeral", timeout = 5000 {
        // Verify webhook signature (e.g., GitHub, Stripe)
        let signature = request.headers["X-Webhook-Signature"];
        let secret = vault://webhooks/secret;

        if !verify_hmac_sha256(request.body, secret, signature) {
            return HttpResponse(401, "Invalid signature");
        }

        // Parse and process webhook
        let data = json.parse(request.body);
        let result = process_event(data);

        return HttpResponse(200, json.stringify(result));
    }
}
```

### 4. 定时执行

```dsl
metadata {
    schedule = "0 */6 * * *"  // Every 6 hours (cron format)
}

agent scheduled_cleanup() -> String {
    capabilities = ["cleanup_data", "archival"]

    policy cleanup_policy {
        allow: ["read_old_data", "archive", "delete"] if data.age > 90_days
        deny: ["delete"] if data.age <= 90_days

        require: {
            backup_verification: true,
            retention_check: true
        }

        audit: {
            log_level: "warning",
            include_deleted_count: true,
            include_archived_count: true
        }
    }

    with memory = "persistent", timeout = 300000 {
        let old_data = query_old_data(90);
        let archived_count = archive_data(old_data);
        let deleted_count = delete_archived_data(old_data);

        return "Archived: " + archived_count + ", Deleted: " + deleted_count;
    }
}
```

### 5. 持久化内存（DSL配置）

```dsl
// Top-level memory block — configures Markdown-backed agent memory
memory agent_memory {
    store    markdown           // Storage backend (markdown only for now)
    path     "data/agents"     // Root directory for memory files
    retention 90d              // How long daily logs are kept
    search {
        vector_weight  0.7     // Semantic similarity weight
        keyword_weight 0.3     // BM25 keyword match weight
    }
}
```

内存文件是以Markdown格式存储在`data/agents/{agent_id}/memory.md`中，包含事实、程序和学到的模式。每日交互日志被追加到`logs/{date}.md`中，并根据保留策略进行压缩。

**REPL命令**：
- `:memory inspect <agent-id>` — 显示代理的内存.md
- `:memory compact <agent-id>` — 清空每日日志，删除过期的条目
- `:memory purge <agent-id>` — 删除代理的所有内存

### 6. Webhook端点（DSL配置）

```dsl
// Top-level webhook block — defines verified webhook endpoints
webhook github_events {
    path     "/hooks/github"
    provider github                              // Preset: github, stripe, slack, custom
    secret   "secret://vault/github-webhook-secret"  // HMAC secret (supports vault refs)
    agent    code_review_agent                   // Route to this agent
    filter {
        json_path "$.action"
        equals    "opened"                       // Only process "opened" events
    }
}
```

提供者预设自动配置签名验证：
- **github**：`X-Hub-Signature-256`头部，`sha256=`前缀，HMAC-SHA256
- **stripe**：`Stripe-Signature`头部，`v0=`前缀，HMAC-SHA256
- **slack**：`X-Slack-Signature`头部，`v0=`前缀，HMAC-SHA256
- **custom**：`X-Signature`头部，HMAC-SHA256

所有签名在请求到达代理处理程序之前都会进行常数时间比较验证。无效的签名会返回HTTP 401错误。

**REPL命令**：
- `:webhook list` — 显示配置的Webhook定义

### 7. 持久化内存与RAG引擎

```dsl
agent knowledge_assistant(query: String) -> String {
    capabilities = ["semantic_search", "rag_retrieval", "synthesis"]

    policy knowledge_policy {
        allow: [
            "vector_search",
            "knowledge_retrieval",
            "context_synthesis"
        ] if query.length() < 1000

        deny: ["knowledge_modification"] if true

        require: {
            embedding_model: "all-MiniLM-L6-v2",
            similarity_threshold: 0.7,
            max_results: 10
        }

        audit: {
            log_level: "info",
            include_query: true,
            include_relevance_scores: true
        }
    }

    with memory = "persistent", security = "medium" {
        // Semantic search in vector database
        let context = rag.search(query, {
            top_k: 5,
            similarity_threshold: 0.7
        });

        // Synthesize response
        let response = synthesize(query, context);

        // Store interaction for future learning
        memory.store({
            query: query,
            response: response,
            timestamp: now()
        });

        return response;
    }
}
```

### 8. 代理间通信

```dsl
agent coordinator(task: String) -> String {
    capabilities = ["message_passing", "agent_coordination"]

    policy coordination_policy {
        allow: [
            "send_message",
            "receive_message",
            "invoke_agent"
        ] if coordination.depth < 5

        deny: ["broadcast"] if true  // Prevent message storms

        require: {
            message_encryption: true,  // AES-256-GCM
            message_signing: true,     // Ed25519
            max_concurrent_agents: 10
        }

        audit: {
            log_level: "info",
            include_message_flow: true,
            include_agent_graph: true
        }
    }

    with memory = "persistent" {
        // Invoke specialized agent
        let validator_response = agent.invoke("data_validator", {
            data: task
        });

        // Send encrypted message to another agent
        agent.send_message("processor_agent", {
            type: "process_request",
            payload: validator_response,
            priority: "high"
        });

        // Wait for response
        let result = agent.receive_message(timeout = 10000);

        return result.payload;
    }
}
```

---

## 常见代理模式

### 模式1：数据验证管道

```dsl
agent data_validator(data: String, schema: String) -> ValidationResult {
    capabilities = ["schema_validation", "data_quality_check"]

    policy validation_policy {
        allow: ["parse_schema", "validate_data", "quality_scoring"]
        deny: ["modify_data", "execute_code"]
        require: {
            max_data_size: "10MB",
            timeout: "5000ms"
        }
        audit: {
            log_level: "warning",
            include_validation_errors: true
        }
    }

    with memory = "ephemeral", security = "high" {
        try {
            // Parse schema
            let parsed_schema = json.parse(schema);

            // Validate against schema
            let validation = validate(data, parsed_schema);

            // Calculate quality score
            let quality_score = calculate_quality(data);

            return ValidationResult {
                valid: validation.success,
                errors: validation.errors,
                quality_score: quality_score,
                recommendations: generate_recommendations(validation)
            };

        } catch (error) {
            return ValidationResult {
                valid: false,
                errors: [error.message],
                quality_score: 0.0,
                recommendations: []
            };
        }
    }
}
```

### 模式2：格式转换器

```dsl
agent format_converter(data: String, from_format: String, to_format: String) -> String {
    capabilities = ["parse_format", "transform_data", "serialize_format"]

    policy conversion_policy {
        allow: ["parse", "transform", "serialize"] if data.size < 50_000_000
        deny: ["execute_code", "file_access"]
        require: {
            supported_formats: ["json", "xml", "yaml", "csv"],
            charset_validation: true
        }
        audit: {
            log_level: "info",
            include_conversion_stats: true
        }
    }

    with memory = "ephemeral", timeout = 10000 {
        // Validate formats
        if !is_supported(from_format) || !is_supported(to_format) {
            return error("Unsupported format");
        }

        // Parse source format
        let parsed = parse(data, from_format);

        // Transform to intermediate representation
        let transformed = normalize(parsed);

        // Serialize to target format
        let result = serialize(transformed, to_format);

        return result;
    }
}
```

### 模式3：API聚合器

```dsl
agent api_aggregator(sources: Array<String>) -> AggregatedData {
    capabilities = ["parallel_requests", "data_normalization", "deduplication"]

    policy aggregation_policy {
        allow: ["https_request"] if url in sources
        deny: ["http_request", "file_access"]
        require: {
            tls_verification: true,
            concurrent_limit: 10,
            timeout_per_request: "3000ms",
            total_timeout: "15000ms"
        }
        audit: {
            log_level: "info",
            include_source_latencies: true,
            alert_on_source_failure: true
        }
    }

    with memory = "ephemeral", timeout = 15000 {
        let results = [];

        // Parallel fetch from all sources
        for source in sources {
            async {
                try {
                    let response = http.get(source, {
                        timeout: 3000,
                        verify_tls: true
                    });
                    results.push(response.json());
                } catch (error) {
                    log("WARNING", "Source failed: " + source);
                }
            }
        }

        // Wait for all requests
        await_all(results);

        // Normalize and deduplicate
        let normalized = normalize_data(results);
        let deduplicated = deduplicate(normalized);

        return AggregatedData {
            sources: sources.length,
            records: deduplicated.length,
            data: deduplicated
        };
    }
}
```

### 模式4：安全扫描器

```dsl
agent security_scanner(target: String, scan_type: String) -> ScanReport {
    capabilities = [
        "vulnerability_detection",
        "dependency_analysis",
        "compliance_check"
    ]

    policy scanner_policy {
        allow: [
            "read_files",
            "analyze_dependencies",
            "check_vulnerabilities"
        ] if scan.depth <= 10

        deny: [
            "write_files",
            "execute_code",
            "network_access"
        ]

        require: {
            sandbox_tier: "Tier2",  // gVisor isolation
            cvss_scoring: true,
            cwe_classification: true
        }

        audit: {
            log_level: "warning",
            include_findings: true,
            include_cvss_scores: true,
            compliance_tags: ["OWASP", "CWE"]
        }
    }

    with memory = "ephemeral", security = "high", sandbox = "Tier2" {
        let findings = [];

        // Scan based on type
        match scan_type {
            "dependencies" => {
                findings = scan_dependencies(target);
            },
            "vulnerabilities" => {
                findings = scan_vulnerabilities(target);
            },
            "compliance" => {
                findings = check_compliance(target, ["HIPAA", "SOC2"]);
            },
            _ => {
                return error("Unknown scan type");
            }
        }

        // Calculate risk score
        let risk_score = calculate_risk(findings);

        return ScanReport {
            target: target,
            scan_type: scan_type,
            findings_count: findings.length,
            critical_count: count_by_severity(findings, "CRITICAL"),
            high_count: count_by_severity(findings, "HIGH"),
            risk_score: risk_score,
            findings: findings,
            recommendations: generate_remediation(findings)
        };
    }
}
```

### 模式5：通知路由器

```dsl
agent notification_router(event: Event, routing_rules: RoutingRules) -> String {
    capabilities = ["event_filtering", "multi_channel_delivery", "retry_logic"]

    policy notification_policy {
        allow: [
            "send_email",
            "send_slack",
            "send_webhook"
        ] if event.priority != "spam"

        deny: ["send_sms"] if event.priority == "low"  // Cost control

        require: {
            rate_limiting: "100/minute",
            retry_attempts: 3,
            backoff_strategy: "exponential"
        }

        audit: {
            log_level: "info",
            include_delivery_status: true,
            include_retry_count: true
        }
    }

    with memory = "ephemeral" {
        // Filter event
        if !should_notify(event, routing_rules) {
            return "Event filtered";
        }

        // Determine channels
        let channels = select_channels(event, routing_rules);

        // Send notifications with retry
        let results = [];
        for channel in channels {
            let success = send_with_retry(channel, event, max_attempts = 3);
            results.push({channel: channel, success: success});
        }

        return format_results(results);
    }
}
```

### 模式6：工作流编排器

```dsl
agent workflow_orchestrator(workflow_spec: WorkflowSpec) -> WorkflowResult {
    capabilities = [
        "step_execution",
        "dependency_resolution",
        "failure_recovery"
    ]

    policy orchestration_policy {
        allow: [
            "invoke_agent",
            "manage_state",
            "handle_errors"
        ] if workflow.depth < 10

        deny: [
            "recursive_workflows",
            "unlimited_agents"
        ]

        require: {
            max_concurrent_steps: 20,
            total_timeout: "600000ms",  // 10 minutes
            checkpoint_enabled: true,
            circuit_breaker: true
        }

        audit: {
            log_level: "info",
            include_workflow_graph: true,
            include_step_timing: true,
            include_failure_trace: true
        }
    }

    with memory = "persistent", timeout = 600000 {
        let state = WorkflowState.new(workflow_spec);

        try {
            // Execute workflow steps
            for step in workflow_spec.steps {
                // Check dependencies
                if !dependencies_met(step, state) {
                    await_dependencies(step, state);
                }

                // Execute step
                let result = execute_step(step, state);

                // Update state with checkpoint
                state.complete_step(step.id, result);
                checkpoint(state);
            }

            return WorkflowResult {
                status: "completed",
                outputs: state.collect_outputs(),
                execution_time: state.elapsed_time()
            };

        } catch (error) {
            // Attempt recovery
            if can_recover(error, state) {
                let recovered_state = recover_workflow(state);
                return resume_workflow(recovered_state);
            }

            return WorkflowResult {
                status: "failed",
                error: error.message,
                completed_steps: state.completed_steps(),
                checkpoint: state.last_checkpoint()
            };
        }
    }
}
```

---

## 应避免的安全反模式

### ❌ 反模式1：缺少策略定义

```dsl
// BAD: No policies defined
agent insecure_agent(input: String) -> String {
    with memory = "ephemeral" {
        return process(input);
    }
}
```

✅ **修复方法**：始终定义明确的策略

```dsl
agent secure_agent(input: String) -> String {
    policy security_policy {
        allow: ["process_data"] if input.length() < 10000
        deny: ["network_access", "file_access"]
        require: {input_validation: true}
        audit: {log_level: "info"}
    }

    with memory = "ephemeral" {
        return process(input);
    }
}
```

### ❌ 反模式2：过于宽松的策略

```dsl
// BAD: Allows everything
policy bad_policy {
    allow: "*" if true
}
```

✅ **修复方法**：使用最小权限原则

```dsl
policy good_policy {
    // Only allow what's needed
    allow: ["read_data", "write_output"] if authorized
    // Explicitly deny risky operations
    deny: ["execute_code", "network_access", "file_system"]
    require: {authentication: true}
}
```

### ❌ 反模式3：没有资源限制

```dsl
// BAD: No timeout, unlimited memory
with memory = "persistent" {
    // Could run forever or consume unlimited memory
    while true {
        expensive_operation();
    }
}
```

✅ **修复方法**：始终设置资源限制

```dsl
with
    memory = "ephemeral",       // Use ephemeral when possible
    timeout = 30000,            // 30 second timeout
    max_memory_mb = 512,        // Memory limit
    max_cpu_cores = 1.0         // CPU limit
{
    for item in limited_dataset {
        process(item);
    }
}
```

### ❌ 反模式4：记录敏感数据

```dsl
// BAD: Logs passwords and secrets
audit: {
    log_level: "info",
    include_input: true,   // Will log passwords!
    include_output: true
}
```

✅ **修复方法**：永远不要记录敏感数据

```dsl
audit: {
    log_level: "info",
    include_input: false,      // Protect PII/secrets
    include_output: false,     // Protect PII/secrets
    include_metadata: true,    // OK to log metadata
    include_timing: true       // OK to log performance
}
```

### ❌ 反模式5：硬编码的秘密

```dsl
// BAD: API key hardcoded
let api_key = "sk_live_abc123xyz789";
```

✅ **修复方法**：使用Vault引用

```dsl
// GOOD: Secret from Vault
let api_key = vault://application/api/key;
```

### ❌ 反模式6：没有输入验证

```dsl
// BAD: No validation
agent bad_agent(input: String) -> String {
    return execute_command(input);  // Command injection risk!
}
```

✅ **修复方法**：始终验证输入

```dsl
agent good_agent(input: String) -> String {
    // Validate input
    if !is_valid_input(input) {
        return error("Invalid input");
    }

    // Sanitize before use
    let sanitized = sanitize(input);
    return safe_process(sanitized);
}
```

### ❌ 反模式7：错误的沙箱层级

```dsl
// BAD: Processing untrusted code in Tier1
agent code_runner(untrusted_code: String) -> String {
    with sandbox = "Tier1" {  // Not enough isolation!
        return eval(untrusted_code);
    }
}
```

✅ **修复方法**：使用适当的沙箱层级

```dsl
agent code_runner(untrusted_code: String) -> String {
    policy strict_isolation {
        deny: ["file_access", "network_access"]
        require: {sandbox_tier: "Tier3"}
    }

    with sandbox = "Tier3" {  // Firecracker microVM
        return safe_eval(untrusted_code);
    }
}
```

### ❌ 反模式8：没有错误处理

```dsl
// BAD: Unhandled errors will crash agent
agent fragile_agent(url: String) -> String {
    let response = http.get(url);  // What if this fails?
    return response.body;
}
```

✅ **修复方法**：始终处理错误

```dsl
agent robust_agent(url: String) -> String {
    try {
        let response = http.get(url, timeout = 5000);

        if response.status != 200 {
            return error("HTTP error: " + response.status);
        }

        return response.body;

    } catch (error) {
        log("ERROR", "Request failed: " + error.message);
        return error("Request failed");
    }
}
```

---

## 验证检查表

在部署代理之前，请验证：

### 安全检查表
- [ ] 所有操作都有定义的策略
- [ ] 应用了最小权限原则（默认拒绝）
- [ ] 沙箱层级适合工作负载
- [ ] 秘密通过Vault引用（从不硬编码）
- [ ] 所有用户输入都有输入验证
- [ ] 输出清理防止注入攻击
- [ ] 审计日志中没有敏感数据

### 资源管理
- [ ] 配置了适当的超时
- [ ] 根据工作负载设置了内存限制
- [ ] 定义了CPU限制
- [ ] 为代理调用设置了并发限制
- [ ] 为外部调用配置了速率限制

### 错误处理
- [ ] 在风险操作周围使用try/catch块
- [ ] 错误信息具有信息性，但不泄露秘密
- [ ] 对于临时失败有重试逻辑
- [ ] 对于级联失败有断路器
- [ ] 在依赖项失败时进行优雅降级

### 合规性与审计
- [ ] 配置了审计日志
- [ ] 添加了合规性标签（根据需要包括HIPAA、SOC2、GDPR）
- [ ] 设置了适当的保留策略
- [ ] PII处理符合法规
- [ ] 数据在存储和传输过程中进行了加密

### 测试
- [ ] 对核心功能进行单元测试
- [ ] 与依赖项进行集成测试
- [ ] 进行安全测试（注入、溢出等）
- [ ] 进行性能测试（在资源限制范围内）
- [ ] 进行混沌测试（故障场景）

---

## 快速参考

### 内置函数

| 类别 | 函数 | 目的 |
|----------|----------|---------|
| **字符串** | `len(s)` | 字符串长度 |
| | `to_upper(s)` | 转换为大写 |
| | `to_lower(s)` | 转换为小写 |
| | `trim(s)` | 删除空白字符 |
| | `split(s, delim)` | 分割字符串 |
| | `contains(s, substr)` | 检查子字符串 |
| **JSON** | `json.parse(s)` | 解析JSON字符串 |
| | `json.stringify(obj)` | 转换为JSON |
| | `json.validate(s, schema)` | 根据模式验证 |
| **HTTP** | `http.get(url, opts)` | 发送HTTP GET请求 |
| | `http.post(url, body, opts)` | 发送HTTP POST请求 |
| | `verify_hmac_sha256(data, secret, sig)` | 验证HMAC签名 |
| **加密** | `encrypt(data)` | AES-256-GCM加密 |
| | `decrypt(data)` | AES-256-GCM解密 |
| | `hash_sha256(data)` | SHA-256哈希 |
| | `sign(data)` | Ed25519签名 |
| **时间** | `now()` | 当前时间戳 |
| | `sleep(ms)` | 睡眠指定毫秒 |
| | `format_time(ts, fmt)` | 格式化时间戳 |
| **日志** | `log(level, msg)` | 记录消息 |
| | `debug(msg)` | 调试日志 |
| | `info(msg)` | 信息日志 |
| | `warn(msg)` | 警告日志 |
| | `error(msg)` | 错误日志 |
| **验证** | `is_valid_email(s)` | 验证电子邮件 |
| | `is_valid_url(s)` | 验证URL |
| | `is_valid_json(s)` | 验证JSON |
| **数组** | `push(arr, item)` | 向数组中添加元素 |
| | `pop(arr)` | 从数组中删除元素 |
| | `map(arr, fn)` | 对数组应用函数 |
| | `filter(arr, fn)` | 过滤数组 |
| | `reduce(arr, fn, init)` | 对数组进行归约 |

### 资源限制建议

| 工作负载类型 | 内存 | CPU | 超时 | 沙箱 |
|---------------|--------|-----|---------|---------|
| **数据验证** | 256MB | 0.5 | 5秒 | Tier1 |
| **格式转换** | 512MB | 1.0 | 10秒 | Tier1 |
| **API集成** | 512MB | 1.0 | 15秒 | Tier1 |
| **代码分析** | 1GB | 2.0 | 30秒 | Tier2 |
| **安全扫描** | 2GB | 2.0 | 60秒 | Tier2 |
| **机器学习推理** | 4GB | 4.0 | 120秒 | Tier2 |
| **工作流编排** | 1GB | 1.0 | 600秒 | Tier1 |
| **不受信任的代码** | 512MB | 1.0 | 10秒 | Tier3 |

### 常见错误代码

| 代码 | 含义 | 解决方案 |
|------|---------|------------|
| `POLICY_VIOLATION` | 操作被策略拒绝 | 检查策略的允许/拒绝规则 |
| `RESOURCE_EXCEEDED` | 资源限制达到 | 增加限制或优化代码 |
| `TIMEOUT` | 执行超时 | 增加超时时间或优化 |
| `AUTH_FAILED` | 认证失败 | 检查Vault凭据 |
| `SIGNATURE_INVALID` | 加密签名无效 | 验证工具签名 |
| `SANDBOX_ERROR` | 沙箱隔离失败 | 检查沙箱层级的兼容性 |
| `VALIDATION_ERROR` | 输入验证失败 | 修复输入数据格式 |
| `NETWORK_ERROR` | 网络请求失败 | 检查端点和连接性 |

### 文档链接

- **完整DSL指南**：[docs/dsl-guide.md](https://github.com/thirdkeyai/symbiont/blob/main/docs/dsl-guide.md)
- **DSL规范**：[docs/dsl-specification.md](https://github.com/thirdkeyai/symbiont/blob/main/docs/dsl-specification.md)
- **推理循环指南**：[docs/reasoning-loop.md](https://github.com/thirdkeyai/symbiont/blob/main/docs/reasoning-loop.md)
- **示例代理**：[agents/README.md](https://github.com/thirdkeyai/symbiont/blob/main/agents/README.md)（8个生产示例）
- **运行时架构**：[docs/runtime-architecture.md](https://github.com/thirdkeyai/symbiont/blob/main/docs/runtime-architecture.md)
- **API参考**：[docs/api-reference.md](https://github.com/thirdkeyai/symbiont/blob/main/docs/api-reference.md)
- **安全模型**：[docs/security-model.md](https://github.com/thirdkeyai/symbiont/blob/main/docs/security-model.md)
- **入门**：[docs/getting-started.md](https://github.com/thirdkeyai/symbiont/blob/main/docs/getting-started.md)

---

## AI助手的专业提示

1. **始终从安全开始**：在实现之前设计策略
2. **使用示例代理**：从`/agents/`中的8个生产代理中进行调整
3. **尽早验证**：在开始时添加输入验证
4. **优雅地处理错误**：将风险操作包装在try/catch中
5. **谨慎记录**：仅记录重要的信息，永远不要记录敏感数据
6. **选择正确的沙箱**：根据威胁模型选择合适的层级
7. **逐步测试**：从简单开始，逐步添加功能并进行测试
8. **记录假设**：对复杂的策略逻辑进行注释
9. **监控资源**：根据工作负载设置合理的限制
10. **部署前审查**：使用验证检查表

---

**SKILLS.md结束**

*本指南优先考虑安全性、合规性和构建生产级Symbiont代理的最佳实践。*