---
name: proxymock
description: 使用 `proxymock CLI` 来记录、检查、模拟、重放以及生成 API 流量。当用户需要捕获 HTTP/gRPC/数据库流量、根据实际流量或 OpenAPI 规范创建模拟数据、重放流量以进行测试、比较流量快照、运行模拟服务器或管理 `proxymock RRPair` 文件时，都可以使用该工具。此外，它还适用于负载测试、回归测试、持续集成（CI）流程集成，以及任何涉及 `proxymock` 或 `Speedscale` 流量重放的任务。
metadata: {"openclaw":{"requires":{"binaries":["proxymock"]}}}
---
# proxymock

proxymock 通过一个透明的代理来捕获真实的 API 和数据库流量，然后利用这些流量生成模拟数据（mocks）并进行测试——无需修改任何代码。

## 核心工作流程

```
record → inspect → mock / replay
```

1. 使用 `proxymock record -- <app-command>` 记录流量。
2. 使用 `proxymock inspect` 检查捕获到的请求/响应对（RRPairs）。
3. 使用 `proxymock mock -- <app-command>` 对依赖项进行模拟。
4. 使用 `proxymock replay --test-against <url>` 重放记录的测试。

## 关键命令

### 记录流量

```bash
# Record while running app as child process (recommended)
proxymock record -- go run .
proxymock record -- npm start

# Custom output dir
proxymock record --out my-recording -- python app.py

# Record database traffic via reverse proxy
proxymock record --map 65432=postgres://localhost:5432 -- ./my-app

# Record with custom app port
proxymock record --app-port 3000 -- ./my-app
```

**架构说明：**  
- 入站代理监听端口 `:4143`，连接到应用程序（默认端口为 `8080`）；
- 出站代理监听端口 `:4140`，用于捕获数据流量。

### 模拟服务器

```bash
# Start mock server, launch app as child
proxymock mock -- go run .

# Source mocks from specific dir
proxymock mock --in ./my-recordings -- npm start

# Fast mode (no simulated latency)
proxymock mock --fast -- ./my-app

# Don't write observed traffic to disk
proxymock mock --no-out -- ./my-app

# Database mock via reverse proxy
proxymock mock --map 65432=localhost:5432 -- ./my-app
```

在模拟请求时，应用程序通过代理 `:4140` 连接到外部服务。匹配到的请求会返回预先记录的响应；未匹配到的请求会直接传递给真实的后端服务。

### 重放/负载测试

```bash
# Replay recorded tests against app
proxymock replay --test-against http://localhost:8080

# Load test: 10 virtual users for 5 minutes
proxymock replay --test-against http://localhost:8080 --vus 10 --for 5m

# Run tests 3 times
proxymock replay --test-against http://localhost:8080 --times 3

# Fail on conditions (CI-friendly)
proxymock replay --test-against http://localhost:8080 \
  --fail-if "requests.failed!=0" \
  --fail-if "latency.p99>100"

# Multi-service routing
proxymock replay \
  --test-against auth=auth.example.com \
  --test-against frontend=http://localhost:8080 \
  --test-against http://localhost:9000
```

**验证指标：**  
- 响应延迟：`latency.{avg,p50,p90,p95,p99,max,min}`  
- 请求统计：`requests.{total,succeeded,failed,per-second,per-minute,response-pct,result-match-pct}`

### 检查（TUI）

```bash
proxymock inspect                    # Current directory
proxymock inspect --in ./my-recording
proxymock inspect --demo             # Demo data
```

**注意：**  
`inspect` 命令会启动一个终端界面；执行时需使用 `pty=true` 选项。

### 从 OpenAPI 生成模拟数据

```bash
proxymock generate api-spec.yaml
proxymock generate --out ./mocks --host api.staging.com api-spec.yaml
proxymock generate --tag-filter "users,orders" api-spec.yaml
proxymock generate --include-optional --examples-only api-spec.yaml
```

### 文件工具

```bash
# Compare RRPair files for differences
proxymock files compare --in recorded/ --in replayed/

# Convert between formats
proxymock files convert --in proxymock --out-format json

# Update mock signatures after editing RRPairs
proxymock files update-mocks --in ./my-mocks
```

### 企业级云服务

```bash
proxymock cloud push snapshot    # Push to Speedscale cloud
proxymock cloud pull snapshot    # Pull from cloud
```

### 导入流量数据

```bash
# Import traffic from a snapshot file
proxymock import snapshot.json
proxymock import --in ./snapshots snapshot.tar.gz
```

### MCP 服务器

```bash
# Start Model Context Protocol (MCP) server for AI tool integration
proxymock mcp
```

### 其他功能

```bash
proxymock send-one path/to/test.md http://localhost:8080   # Send single request
proxymock init --api-key <key>                              # Initialize config
proxymock certs                                             # Manage TLS certs
proxymock version                                           # Version info
proxymock completion bash                                   # Generate shell completions (bash/zsh/fish/powershell)
```

## RRPair 文件

流量数据以 RRPair（请求/响应对）的形式存储在 `proxymock/` 目录下的 markdown 文件中。每个文件包含：
- `### REQUEST (TEST) ###` 或 `### REQUEST (MOCK) ###`：捕获到的请求内容。
- `### RESPONSE ###`：捕获到的响应内容。
- `### SIGNATURE ###`：模拟请求的匹配规则（仅用于模拟请求）。

这些文件可供人类阅读和大型语言模型（LLM）理解。可以直接编辑文件来修改测试数据或模拟响应；如果修改了影响匹配规则的请求细节，请运行 `proxymock files update-mocks` 命令。

## 代理环境配置

当不使用 `-- <command>` 子进程模式时，需要手动设置代理环境变量：

```bash
# HTTP/HTTPS/gRPC
export http_proxy=http://localhost:4140
export https_proxy=http://localhost:4140
export grpc_proxy=http://$(hostname):4140

# Database (SOCKS)
export all_proxy=socks5h://localhost:4140
```

有关特定语言的配置信息，请参阅 [语言参考文档](https://docs.speedscale.com/proxymock/getting-started/language-reference/)。

## 参考资料

有关签名匹配、架构细节和高级用法，请参阅 `references/cli-reference.md`。