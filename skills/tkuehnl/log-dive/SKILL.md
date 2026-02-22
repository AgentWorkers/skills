---
name: log-dive
description: **统一日志搜索功能：** 支持在 Loki、Elasticsearch 和 CloudWatch 之间进行日志搜索。用户可以使用自然语言查询，这些查询会被转换为 LogQL、Elasticsearch 的 DSL（Domain-Specific Language）或 CloudWatch 的过滤模式。该功能仅提供读取日志数据的功能，不会对日志进行任何修改或删除操作。
version: 0.1.1
author: Anvil AI
tags: [logs, observability, loki, elasticsearch, cloudwatch, incident-response, sre, discord, discord-v2]
---
# Log Dive — 统一日志搜索 🤿

您可以通过一个界面在 **Loki**、**Elasticsearch/OpenSearch** 和 **AWS CloudWatch** 之间搜索日志。只需用简单的英语提出请求，该技能会自动将其转换为相应的查询语言。

> **⚠️ 敏感数据警告：** 日志中经常包含个人身份信息（PII）、密钥、令牌、密码等敏感数据。请勿缓存、存储或重复显示原始日志内容。所有日志输出均应视为机密信息。

## 激活方式

当用户提到以下内容时，该技能会被激活：
- “搜索日志”（search logs）、“在日志中查找”（find in logs）、“日志搜索”（log search）、“查看日志”（check the logs）
- “Loki”、“LogQL”、“logcli”
- “Elasticsearch日志”（Elasticsearch logs）、“Kibana”、“OpenSearch”
- “CloudWatch日志”（CloudWatch logs）、“AWS日志”（AWS logs）、“日志组”（log groups）
- “错误日志”（error logs）、“查找错误”（find errors）、“[服务] 中发生了什么”（what happened in [service]）
- “查看日志尾部”（tail logs）、“实时跟踪日志”（follow logs）、“日志后端”（log backends）、“哪些日志源”（which log sources）、“日志索引”（log indices）、“日志标签”（log labels）
- 涉及日志分析的事件分类（incident triage）
- 明确提到 “log-dive”（log-dive）

## 权限设置

```yaml
permissions:
  exec: true          # Required to run backend scripts
  read: true          # Read script files
  write: false        # Never writes files — logs may contain secrets
  network: true       # Queries remote log backends
```

## 示例请求：
1. “查找过去30分钟内来自结账服务的错误日志”
2. “在所有服务中搜索超时异常”
3. “我配置了哪些日志后端？”
4. “列出Elasticsearch中可用的日志索引”
5. “显示Loki中可用的标签”
6. “查看支付服务的日志尾部”
7. “在CloudWatch中查找api-gateway的所有5xx错误”
8. “关联用户服务和支付服务之间的错误”
9. “今天下午2点到3点之间发生了什么？”

## 后端配置

每个后端都使用环境变量。用户可能配置了一个、两个或全部三个环境变量。

### Loki
| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `LOKI_ADDR` | 是 | Loki服务器地址（例如：`http://loki.internal:3100`） |
| `LOKI_TOKEN` | 否 | 用于身份验证的令牌 |
| `LOKI_TENANT_ID` | 否 | 多租户头信息（`X-Scope-OrgID`） |

### Elasticsearch / OpenSearch
| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `ELASTICSEARCH_URL` | 是 | 基础URL（例如：`https://es.internal:9200`） |
| `ELASTICSEARCH_TOKEN` | 否 | 使用 `Basic <base64>` 或 `Bearer <token>` 进行身份验证 |

### AWS CloudWatch Logs
| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `AWS_PROFILE` 或 `AWS_ACCESS_KEY_ID` | 是 | AWS凭据 |
| `AWS_REGION` | 是 | CloudWatch所在的AWS区域 |

## 代理工作流程

请按照以下步骤操作：

### 第1步：检查后端配置

运行后端检查，了解当前配置的情况：

```bash
bash <skill_dir>/scripts/log-dive.sh backends
```

解析JSON输出。如果没有配置任何后端，请告知用户需要设置哪些环境变量。

### 第2步：转换用户查询

这是关键步骤。将用户的自然语言请求转换为相应的后端特定查询语言。请参考以下查询语言参考。

**对于所有后端，将查询通过调度器传递：**

```bash
# Search across all configured backends
bash <skill_dir>/scripts/log-dive.sh search --query '<QUERY>' [OPTIONS]

# Search a specific backend
bash <skill_dir>/scripts/log-dive.sh search --backend loki --query '{app="checkout"} |= "error"' --since 30m --limit 200

bash <skill_dir>/scripts/log-dive.sh search --backend elasticsearch --query '{"query":{"bool":{"must":[{"match":{"message":"error"}},{"match":{"service":"checkout"}}]}}}' --index 'app-logs-*' --since 30m --limit 200

bash <skill_dir>/scripts/log-dive.sh search --backend cloudwatch --query '"ERROR" "checkout"' --log-group '/ecs/checkout-service' --since 30m --limit 200
```

### 第3步：列出可用目标

在搜索之前，您可能需要先了解有哪些可用的后端。

```bash
# Loki: list labels and label values
bash <skill_dir>/scripts/log-dive.sh labels --backend loki
bash <skill_dir>/scripts/log-dive.sh labels --backend loki --label app

# Elasticsearch: list indices
bash <skill_dir>/scripts/log-dive.sh indices --backend elasticsearch

# CloudWatch: list log groups
bash <skill_dir>/scripts/log-dive.sh indices --backend cloudwatch
```

### 第4步：实时跟踪日志

实时跟踪日志（默认持续30秒），并流式显示结果。

### 第5步：分析结果

收到日志输出后，必须执行以下操作：
1. **识别错误类型** — 将相似的错误分组并统计出现次数
2. **找出根本原因** — 查找最早的错误并追踪依赖关系链
3. **跨服务关联错误** — 如果服务A中的错误提到了服务B，请记录这种依赖关系
4. **构建时间线** — 按时间顺序排列事件
5. **提供可操作的总结** — “例如：结账服务在14:23开始返回500状态码的错误，原因是数据库连接池已耗尽（最大连接数为10个，当前使用了10个）。连接池耗尽是由库存服务中的慢查询引起的。”

**切勿直接向用户展示原始日志内容。** 必须对日志内容进行总结、提取模式，并以结构化的方式呈现结果。

### Discord v2 提供方式（OpenClaw v2026.2.14+）

当对话在Discord频道中进行时：
- 首先发送一个简洁的事件摘要（后端、查询意图、主要错误类型、根本原因假设），然后询问用户是否需要详细信息。
- 保持第一条回复的长度在1200个字符以内，并避免在第一条消息中展示原始日志内容。
- 如果Discord支持相关功能，可以包括以下操作：
  - **显示错误时间线**（Show Error Timeline）
  - **显示主要错误模式**（Show Top Error Patterns）
  - **运行相关服务查询**（Run Related Service Query）
- 如果相关功能不可用，可以提供编号列表形式的后续信息。
- 在分享时间线或分组结果时，每条消息的长度应尽量控制在15行以内。

## 查询语言参考

### LogQL（Loki）

LogQL包含两部分：流选择器和过滤管道。

**流选择器：**
```
{app="myapp"}                          # exact match
{namespace="prod", app=~"api-.*"}      # regex match
{app!="debug"}                         # negative match
```

**过滤管道（位于选择器之后）：**
```
{app="myapp"} |= "error"              # line contains "error"
{app="myapp"} != "healthcheck"         # line does NOT contain
{app="myapp"} |~ "error|warn"          # regex match on line
{app="myapp"} !~ "DEBUG|TRACE"         # negative regex
```

**结构化元数据（已解析的日志）：**
```
{app="myapp"} | json                   # parse JSON logs
{app="myapp"} | json | status >= 500   # filter by parsed field
{app="myapp"} | logfmt                 # parse logfmt
{app="myapp"} | regexp `(?P<ip>\d+\.\d+\.\d+\.\d+)` # regex extract
```

**常见模式：**
- 服务中的错误：`{app="checkout"} |= "error" | json | level="error"`
- HTTP 5xx错误：`{app="api"} | json | status >= 500`
- 慢速请求：`{app="api"} | json | duration > 5s`
- 堆栈跟踪：`{app="myapp"} |= "Exception" |= "at "`

### Elasticsearch 查询DSL

**简单匹配：**
```json
{"query": {"match": {"message": "error"}}}
```

**布尔查询（AND/OR）：**
```json
{
  "query": {
    "bool": {
      "must": [
        {"match": {"message": "error"}},
        {"match": {"service.name": "checkout"}}
      ],
      "must_not": [
        {"match": {"message": "healthcheck"}}
      ]
    }
  },
  "sort": [{"@timestamp": "desc"}],
  "size": 200
}
```

**时间范围过滤：**
```json
{
  "query": {
    "bool": {
      "must": [{"match": {"message": "timeout"}}],
      "filter": [
        {"range": {"@timestamp": {"gte": "now-30m", "lte": "now"}}}
      ]
    }
  }
}
```

**通配符/正则表达式：**
```json
{"query": {"regexp": {"message": "error.*timeout"}}}
```

**常见模式：**
- 服务中的错误：`{"query":{"bool":{"must":[{"match":{"message":"error"}},{"match":{"service.name":"checkout"}}]}}`
- HTTP 5xx错误：`{"query":{"range":{"http.status_code":{"gte":500}}}}`
- 按字段聚合：使用 `aggs` — 但建议代理使用简单查询

### CloudWatch过滤模式

**简单文本匹配：**
```
"ERROR"                              # contains ERROR
"ERROR" "checkout"                   # contains ERROR AND checkout
```

**JSON过滤模式：**
```
{ $.level = "error" }               # JSON field match
{ $.statusCode >= 500 }             # numeric comparison
{ $.duration > 5000 }               # duration threshold
{ $.level = "error" && $.service = "checkout" }  # compound
```

**否定和通配符：**
```
?"ERROR" ?"timeout"                  # ERROR OR timeout (any term)
-"healthcheck"                       # does NOT contain (use with other terms)
```

**常见模式：**
- 错误：`"ERROR"`
- 服务中的错误：`{"$.level = "error" && $.service = "checkout" }`
- HTTP 5xx错误：`{"$.statusCode >= 500 }`
- 异常：`"Exception" "at "`

## 输出格式

在展示搜索结果时，请使用以下格式：

```markdown
## Log Search Results

**Backend:** Loki | **Query:** `{app="checkout"} |= "error"`
**Time range:** Last 30 minutes | **Results:** 47 entries

### Error Summary

| Error Type | Count | First Seen | Last Seen | Service |
|-----------|-------|------------|-----------|---------|
| NullPointerException | 23 | 14:02:31 | 14:28:45 | checkout |
| ConnectionTimeout | 18 | 14:05:12 | 14:29:01 | checkout → db |
| HTTP 503 | 6 | 14:06:00 | 14:27:33 | checkout → payment |

### Root Cause Analysis

1. **14:02:31** — First `NullPointerException` in checkout service...
2. **14:05:12** — Database connection timeouts begin...

### Recommended Actions

- [ ] Check database connection pool settings
- [ ] Review recent deployments to checkout service

---
*Powered by Anvil AI 🤿*
```

## 常见工作流程

### 事件分类
1. 检查后端 → 在受影响的服务中搜索错误 → 在上游/下游服务中继续搜索 → 关联错误 → 构建时间线 → 提出处理建议。

### 性能调查
1. 搜索响应缓慢的请求（`duration > 5s`） → 识别常见模式 → 检查数据库中的慢查询 → 检查外部服务的超时情况。

### 部署验证
1. 搜索部署后的服务中的错误 → 将错误率与部署前的情况进行比较 → 标记新的错误类型。

## 限制：
- **只读权限：** 该技能仅支持搜索和读取日志，无法删除、修改或创建日志条目。
- **输出大小限制：** 默认输出条数为200条。日志输出会经过预过滤以减少令牌消耗。对于大规模调查，建议使用多个针对性查询，而不是单一的广泛查询。
- **网络访问：** 运行OpenClaw的机器必须能够访问日志后端。
- **不支持流式聚合：** 对于复杂的聚合操作（如百分比、比率），建议使用后端的原生界面（Grafana、Kibana、CloudWatch Insights）。

## 故障排除

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| “未配置后端” | 未设置环境变量 | 设置 `LOKI_ADDR`、`ELASTICSEARCH_URL`，或配置AWS CLI |
| “logcli未找到” | 未安装logcli | 从 [https://grafana.com/docs/loki/latest/tools/logcli/](https://grafana.com/docs/loki/latest/tools/logcli/) 安装 |
| “aws: 命令未找到” | 未安装AWS CLI | 从 [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) 安装 |
| “curl命令未找到” | 未安装curl | 使用 `apt install curl` 或 `brew install curl` 安装 |
| “jq命令未找到” | 未安装jq | 使用 `apt install jq` 或 `brew install jq` 安装 |
| “连接失败” | 无法访问后端 | 检查URL、VPN设置和防火墙规则 |
| “401未经授权” | 凭据错误 | 检查 `LOKI_TOKEN`、`ELASTICSEARCH_TOKEN` 或AWS凭据 |

---
*由Anvil AI提供支持 🤿*