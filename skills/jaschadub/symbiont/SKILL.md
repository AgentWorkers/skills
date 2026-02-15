# Symbiont 代理开发技能指南

**目的**：本指南帮助 AI 助手快速构建安全、合规的 Symbiont 代理，并遵循最佳实践。

**完整文档请参阅**：[DSL 指南](https://github.com/thirdkeyai/symbiont/blob/main/docs/dsl-guide.md)、[DSL 规范](https://github.com/thirdkeyai/symbiont/blob/main/docs/dsl-specification.md) 和 [示例代理](https://github.com/thirdkeyai/symbiont/blob/main/agents/README.md)。

## Symbiont 的独特之处

- **零信任安全**：所有输入默认被视为不可信，需要明确的政策配置。
- **政策即代码**：声明性安全规则在运行时执行。
- **多层沙箱隔离**：使用 Docker → gVisor → Firecracker 进行隔离。
- **企业合规性**：内置 HIPAA、SOC2、GDPR 等合规性机制。
- **加密验证**：使用 MCP 工具的 SchemaPin 和 Ed25519 签名算法。
- **Webhook 集成**：支持 GitHub/Stripe/Slack 等平台的签名验证。
- **持久化内存**：基于 Markdown 的代理内存系统，支持数据保留和压缩。

---

## 快速入门模板

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

## 以安全为先的政策模式

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

### 2. API 集成代理（外部调用）

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

### 3. 安全扫描代理（审计/合规性检查）

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

### 4. 工作流编排代理（多步骤操作）

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

| 层级 | 技术 | 用例 | 性能 | 安全性 | 开销 |
|------|------------|----------|-------------|----------|----------|
| **Tier1** | Docker | 通用工作负载 | 快速 | 良好 | 低（约 100 毫秒） |
| **Tier2** | gVisor | 处理不可信代码 | 中等 | 高 | 中等（约 500 毫秒） |
| **Tier3** | Firecracker | 多租户隔离 | 较慢 | 最高 | 高（约 2 秒） |
| **Native** | 仅用于开发 | 最快 | 无 | 极低 |

**选择指南**：
- **Tier1 (Docker)**：大多数代理的默认选择。
- **Tier2 (gVisor)**：用于处理外部数据和用户提供的代码。
- **Tier3 (Firecracker)**：适用于高度敏感的场景和合规性要求。
- **Native**：严禁在生产环境中使用（仅限开发/测试）。

---

## DSL 语法速查表

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

### 政策语言

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

### With 块（执行上下文）

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

### 2. MCP 工具集成（加密验证）

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

### 3. HTTP Webhook 处理

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

### 5. 持久化内存（DSL 配置）

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

内存文件采用人类可读的 Markdown 格式存储在 `data/agents/{agent_id}/memory.md` 中，包含事实、流程和学到的模式。每日交互日志会被追加到 `logs/{date}.md` 文件中，并根据保留策略进行压缩。

**REPL 命令**：
- `:memory inspect <agent-id>` — 显示代理的内存内容。
- `:memory compact <agent-id>` — 清除每日日志，删除过期条目。
- `:memory purge <agent-id>` — 删除代理的所有内存数据。

### 6. Webhook 端点（DSL 配置）

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

提供商预设了签名验证规则：
- **github**：`X-Hub-Signature-256` 标头，`sha256=` 前缀，HMAC-SHA256 签名。
- **stripe**：`Stripe-Signature` 标头，HMAC-SHA256 签名。
- **slack**：`X-Slack-Signature` 标头，`v0=` 前缀，HMAC-SHA256 签名。
- **custom**：`X-Signature` 标头，HMAC-SHA256 签名。

所有签名在请求到达代理处理程序之前都会进行常数时间内的验证。无效签名会返回 HTTP 401 错误。

**REPL 命令**：
- `:webhook list` — 显示配置的 Webhook 定义。

### 7. 持久化内存与 RAG 引擎

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

### 模式 1：数据验证管道

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

### 模式 2：格式转换器

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

### 模式 3：API 集成器

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

### 模式 4：安全扫描器

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

### 模式 5：通知路由器

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

### 模式 6：工作流编排器

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

### ❌ 反模式 1：缺少政策定义

```dsl
// BAD: No policies defined
agent insecure_agent(input: String) -> String {
    with memory = "ephemeral" {
        return process(input);
    }
}
```

✅ **修复方法**：始终定义明确的政策。

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

### ❌ 反模式 2：过于宽松的政策

```dsl
// BAD: Allows everything
policy bad_policy {
    allow: "*" if true
}
```

✅ **修复方法**：遵循最小权限原则。

```dsl
policy good_policy {
    // Only allow what's needed
    allow: ["read_data", "write_output"] if authorized
    // Explicitly deny risky operations
    deny: ["execute_code", "network_access", "file_system"]
    require: {authentication: true}
}
```

### ❌ 反模式 3：没有资源限制

```dsl
// BAD: No timeout, unlimited memory
with memory = "persistent" {
    // Could run forever or consume unlimited memory
    while true {
        expensive_operation();
    }
}
```

✅ **修复方法**：始终设置资源限制。

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

### ❌ 反模式 4：记录敏感数据

```dsl
// BAD: Logs passwords and secrets
audit: {
    log_level: "info",
    include_input: true,   // Will log passwords!
    include_output: true
}
```

✅ **修复方法**：切勿记录敏感数据。

```dsl
audit: {
    log_level: "info",
    include_input: false,      // Protect PII/secrets
    include_output: false,     // Protect PII/secrets
    include_metadata: true,    // OK to log metadata
    include_timing: true       // OK to log performance
}
```

### ❌ 反模式 5：硬编码的秘密

```dsl
// BAD: API key hardcoded
let api_key = "sk_live_abc123xyz789";
```

✅ **修复方法**：使用 Vault 来管理秘密。

```dsl
// GOOD: Secret from Vault
let api_key = vault://application/api/key;
```

### ❌ 反模式 6：没有输入验证

```dsl
// BAD: No validation
agent bad_agent(input: String) -> String {
    return execute_command(input);  // Command injection risk!
}
```

✅ **修复方法**：始终验证输入。

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

### ❌ 反模式 7：错误的沙箱层级

```dsl
// BAD: Processing untrusted code in Tier1
agent code_runner(untrusted_code: String) -> String {
    with sandbox = "Tier1" {  // Not enough isolation!
        return eval(untrusted_code);
    }
}
```

✅ **修复方法**：选择合适的沙箱层级。

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

### ❌ 反模式 8：没有错误处理

```dsl
// BAD: Unhandled errors will crash agent
agent fragile_agent(url: String) -> String {
    let response = http.get(url);  // What if this fails?
    return response.body;
}
```

✅ **修复方法**：始终处理错误。

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

## 部署前的验证

### 安全性检查
- [ ] 所有操作都有明确的政策定义。
- [ ] 遵循最小权限原则（默认拒绝未经授权的请求）。
- [ ] 选择适合工作负载的沙箱层级。
- [ ] 秘密信息通过 Vault 管理（切勿硬编码）。
- [ ] 所有用户输入都经过验证。
- [ ] 输出经过清洗，防止注入攻击。
- [ ] 审计日志中不含敏感数据。

### 资源管理
- [ ] 配置适当的超时时间。
- [ ] 根据工作负载设置内存限制。
- [ ] 定义 CPU 限制。
- [ ] 限制代理的并发调用次数。
- [ ] 配置外部调用的速率限制。

### 错误处理
- [ ] 对风险操作使用 try/catch 块进行错误处理。
- [ ] 错误信息具有误导性，但不会泄露敏感信息。
- [ ] 为临时故障提供重试逻辑。
- [ ] 对于连锁故障，使用断路器机制。
- [ ] 在依赖项失败时实现优雅降级。

### 合规性与审计
- [ ] 配置审计日志。
- [ ] 根据需要添加合规性标签（如 HIPAA、SOC2、GDPR）。
- [ ] 设置适当的保留策略。
- [ ] 按照规定处理个人身份信息（PII）。
- [ ] 数据在存储和传输过程中都经过加密。

### 测试
- [ ] 对核心功能进行单元测试。
- [ ] 与依赖项进行集成测试。
- [ ] 进行安全测试（如注入攻击、溢出等）。
- [ ] 在资源限制范围内进行性能测试。
- [ ] 进行混沌测试（测试故障场景）。

---

## 快速参考

### 内置函数

| 类别 | 函数 | 用途 |
|----------|----------|---------|
| **字符串** | `len(s)` | 获取字符串长度 |
| | `to_upper(s)` | 将字符串转换为大写 |
| | `to_lower(s)` | 将字符串转换为小写 |
| | `trim(s)` | 删除字符串中的空白字符 |
| | `split(s, delim)` | 根据分隔符分割字符串 |
| | `contains(s, substr)` | 检查字符串是否包含子字符串 |
| **JSON** | `json.parse(s)` | 解析 JSON 字符串 |
| | `json.stringify(obj)` | 将对象转换为 JSON 字符串 |
| | `json.validate(s, schema)` | 根据模式验证 JSON 字符串 |
| **HTTP** | `http.get(url, opts)` | 发送 HTTP GET 请求 |
| | `http.post(url, body, opts)` | 发送 HTTP POST 请求 |
| | `verify_hmac_sha256(data, secret, sig)` | 验证 HMAC 签名 |
| **加密** | `encrypt(data)` | 使用 AES-256-GCM 加密数据 |
| | `decrypt(data)` | 使用 AES-256-GCM 解密数据 |
| | `hash_sha256(data)` | 计算数据的 SHA-256 哈希值 |
| | `sign(data)` | 生成 Ed25519 签名 |
| **时间** | `now()` | 获取当前时间戳 |
| | `sleep(ms)` | 休眠指定毫秒数 |
| | `format_time(ts, fmt)` | 格式化时间戳 |
| **日志** | `log(level, msg)` | 记录日志 |
| | `debug(msg)` | 调试日志 |
| | `info(msg)` | 信息日志 |
| | `warn(msg)` | 警告日志 |
| | `error(msg)` | 错误日志 |
| **验证** | `is_valid_email(s)` | 验证电子邮件地址 |
| | `is_valid_url(s)` | 验证 URL 是否有效 |
| | `is_valid_json(s)` | 验证 JSON 字符串的有效性 |
| **数组** | `push(arr, item)` | 向数组中添加元素 |
| | `pop(arr)` | 从数组中删除元素 |
| | `map(arr, fn)` | 对数组应用函数 |
| | `filter(arr, fn)` | 过滤数组 |
| | `reduce(arr, fn, init)` | 对数组进行归约操作 |

### 资源限制建议

| 工作负载类型 | 内存 | CPU | 超时 | 沙箱层级 |
|---------------|--------|-----|---------|---------|
| **数据验证** | 256MB | 0.5 | 5秒 | Tier1 |
| **格式转换** | 512MB | 1.0 | 10秒 | Tier1 |
| **API 集成** | 512MB | 1.0 | 15秒 | Tier1 |
| **代码分析** | 1GB | 2.0 | 30秒 | Tier2 |
| **安全扫描** | 2GB | 2.0 | 60秒 | Tier2 |
| **机器学习推理** | 4GB | 4.0 | 120秒 | Tier2 |
| **工作流编排** | 1GB | 1.0 | 600秒 | Tier1 |
| **不可信代码** | 512MB | 1.0 | 10秒 | Tier3 |

### 常见错误代码

| 代码 | 含义 | 解决方案 |
|------|---------|------------|
| `POLICY_VIOLATION` | 操作被政策拒绝 | 检查政策中的允许/拒绝规则 |
| `RESOURCE_EXCEEDED` | 资源超出限制 | 增加资源限制或优化代码 |
| `TIMEOUT` | 执行超时 | 增加超时时间或优化代码 |
| `AUTH_FAILED` | 认证失败 | 检查 Vault 凭据 |
| `SIGNATURE_INVALID` | 签名无效 | 验证签名 |
| `SANDBOX_ERROR` | 沙箱隔离失败 | 检查沙箱层级的兼容性 |
| `VALIDATION_ERROR` | 输入验证失败 | 修复输入数据格式 |
| `NETWORK_ERROR` | 网络请求失败 | 检查端点和连接性 |

### 文档链接

- **完整 DSL 指南**：[docs/dsl-guide.md](https://github.com/thirdkeyai/symbiont/blob/main/docs/dsl-guide.md)
- **DSL 规范**：[docs/dsl-specification.md](https://github.com/thirdkeyai/symbiont/blob/main/docs/dsl-specification.md)
- **示例代理**：[agents/README.md](https://github.com/thirdkeyai/symbiont/blob/main/agents/README.md)（8 个生产环境示例）
- **运行时架构**：[docs/runtime-architecture.md](https://github.com/thirdkeyai/symbiont/blob/main/docs/runtime-architecture.md)
- **API 参考**：[docs/api-reference.md](https://github.com/thirdkeyai/symbiont/blob/main/docs/api-reference.md)
- **工具评审流程**：[docs/tool_review_workflow.md](https://github.com/thirdkeyai/symbiont/blob/main/docs/tool_review_workflow.md)
- **入门指南**：[docs/getting-started.md](https://github.com/thirdkeyai/symbiont/blob/main/docs/getting-started.md)

---

## AI 助手的实用建议

1. **始终从安全性开始**：在实现之前先设计好安全策略。
2. **使用示例代理**：参考 `/agents/` 目录中的 8 个生产环境代理示例。
3. **尽早进行验证**：在代码开始时添加输入验证。
4. **优雅地处理错误**：用 try/catch 块处理风险操作。
5. **谨慎记录日志**：仅记录重要信息，切勿记录敏感数据。
6. **选择合适的沙箱层级**：根据威胁模型选择合适的沙箱层级。
7 **逐步进行测试**：从简单功能开始，逐步添加新功能并测试。
8 **记录假设**：对复杂的政策逻辑进行注释说明。
9 **监控资源使用**：根据工作负载设置合理的资源限制。
10. **部署前进行验证**：使用提供的验证检查列表。

---

**SKILL.md 结束**

*本指南优先考虑安全性、合规性和最佳实践，以构建生产级的 Symbiont 代理。*