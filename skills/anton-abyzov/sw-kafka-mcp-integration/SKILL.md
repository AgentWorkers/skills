---
name: kafka-mcp-integration
description: **MCP服务器集成：用于Kafka操作与Claude Desktop及SpecWeave的配合**  
本文档介绍了如何在配置Kafka MCP服务器、将Claude连接到Kafka主题，或在不同的MCP实现方案中进行选择时使用相关功能。
---

# Kafka MCP服务器集成

本文介绍了如何将SpecWeave与Kafka MCP（Model Context Protocol）服务器集成。支持4种不同的MCP服务器实现方式，并提供自动检测和配置指导。

---

> **优先推荐使用代码**：对于大多数Kafka自动化任务，直接编写代码比使用MCP更高效（可减少98%的通信开销）。建议使用`kafkajs`或`kafka-node`：
>
> ```typescript
> import { Kafka } from 'kafkajs';
> const kafka = new Kafka({ brokers: ['localhost:9092'] });
> const producer = kafka.producer();
> await producer.send({ topic: 'events', messages: [{ value: 'Hello' }] });
> ```
>
> **MCP的适用场景**：快速交互式调试、主题探索、与Claude桌面应用程序集成。
>
> **何时使用代码**：在CI/CD管道、测试自动化、生产脚本等需要可重复使用的场景中。

---

## 支持的MCP服务器

### 1. kanapuli/mcp-kafka（Node.js）

**安装**：
```bash
npm install -g mcp-kafka
```

**功能**：
- 认证方式：SASL_PLAINTEXT、PLAINTEXT
- 支持的操作：生产消息、消费消息、列出主题、描述主题、获取消息偏移量
- 适用场景：基本Kafka操作、快速原型开发

**配置示例**：
```json
{
  "mcpServers": {
    "kafka": {
      "command": "npx",
      "args": ["mcp-kafka"],
      "env": {
        "KAFKA_BROKERS": "localhost:9092",
        "KAFKA_SASL_MECHANISM": "plain",
        "KAFKA_SASL_USERNAME": "user",
        "KAFKA_SASL_PASSWORD": "password"
      }
    }
  }
}
```

### 2. tuannvm/kafka-mcp-server（Go语言）

**安装**：
```bash
go install github.com/tuannvm/kafka-mcp-server@latest
```

**功能**：
- 认证方式：SASL_SCRAM_SHA_256、SASL_SCRAM_SHA_512、SASL_SSL、PLAINTEXT
- 支持的所有操作：CRUD操作、消费者组管理、偏移量管理
- 适用场景：生产环境、需要高级SASL认证的场景

**配置示例**：
```json
{
  "mcpServers": {
    "kafka": {
      "command": "kafka-mcp-server",
      "args": [
        "--brokers", "localhost:9092",
        "--sasl-mechanism", "SCRAM-SHA-256",
        "--sasl-username", "admin",
        "--sasl-password", "admin-secret"
      ]
    }
  }
}
```

### 3. Joel-hanson/kafka-mcp-server（Python语言）

**安装**：
```bash
pip install kafka-mcp-server
```

**功能**：
- 认证方式：SASL_PLAINTEXT、PLAINTEXT、SSL
- 支持的操作：生产消息、消费消息、列出主题、描述主题
- 适用场景：与Claude桌面应用程序集成、Python开发环境

**配置示例**：
```json
{
  "mcpServers": {
    "kafka": {
      "command": "python",
      "args": ["-m", "kafka_mcp_server"],
      "env": {
        "KAFKA_BOOTSTRAP_SERVERS": "localhost:9092"
      }
    }
  }
}
```

### 4. Confluent官方MCP（企业级版本）

**安装**：
```bash
confluent plugin install mcp-server
```

**功能**：
- 认证方式：OAuth、SASL_SCRAM、API密钥
- 支持的所有Kafka操作、模式注册表（Schema Registry）、Flink SQL
- 高级功能：自然语言接口、基于AI的查询生成
- 适用场景：Confluent Cloud平台、企业级部署

**配置示例**：
```json
{
  "mcpServers": {
    "kafka": {
      "command": "confluent",
      "args": ["mcp", "start"],
      "env": {
        "CONFLUENT_CLOUD_API_KEY": "your-api-key",
        "CONFLUENT_CLOUD_API_SECRET": "your-api-secret"
      }
    }
  }
}
```

## 自动检测

SpecWeave能够自动检测已安装的MCP服务器：

```bash
/sw-kafka:mcp-configure
```

该命令会：
1. 扫描系统中安装的MCP服务器（通过npm、go、pip或confluent CLI安装）
2. 检查哪些服务器正在运行
3. 根据功能对服务器进行排序（Confluent > tuannvm > kanapuli > Joel-hanson）
4. 生成推荐的配置文件
5. 测试与服务器的连接

## 快速入门

### 选项1：自动配置（推荐）

```bash
/sw-kafka:mcp-configure
```

交互式向导会引导您完成以下步骤：
- 选择MCP服务器（或自动检测）
- 配置Kafka broker的URL
- 设置认证信息
- 测试连接

### 选项2：手动配置

1. 安装所需的MCP服务器（参见上述安装命令）
2. 创建`.mcp.json`配置文件：
```json
{
  "serverType": "tuannvm",
  "brokerUrls": ["localhost:9092"],
  "authentication": {
    "mechanism": "SASL/SCRAM-SHA-256",
    "username": "admin",
    "password": "admin-secret"
  }
}
```

3. 测试连接：
```bash
# Via MCP server CLI
kafka-mcp-server test-connection

# Or via SpecWeave
node -e "import('./dist/lib/mcp/detector.js').then(async ({ MCPServerDetector }) => {
  const detector = new MCPServerDetector();
  const result = await detector.detectAll();
  console.log(JSON.stringify(result, null, 2));
});"
```

## MCP服务器对比

| 功能 | kanapuli | tuannvm | Joel-hanson | Confluent |
|---------|----------|---------|-------------|-----------|
| **语言** | Node.js | Go | Python | 官方CLI |
| **SASL_PLAINTEXT** | ✅ | ✅ | ✅ | ✅ |
| **SCRAM-SHA-256** | ❌ | ✅ | ❌ | ✅ |
| **SCRAM-SHA-512** | ❌ | ✅ | ❌ | ✅ |
| **TLS/SSL** | ❌ | ✅ | ✅ | ✅ |
| **OAuth** | ❌ | ❌ | ❌ | ✅ |
| **消费者组** | ❌ | ✅ | ❌ | ✅ |
| **偏移量管理** | ❌ | ✅ | ❌ | ✅ |
| **模式注册表** | ❌ | ❌ | ❌ | ✅ |
| **ksqlDB** | ❌ | ❌ | ❌ | ✅ |
| **Flink SQL** | ❌ | ❌ | ❌ | ✅ |
| **AI/NL接口** | ❌ | ❌ | ❌ | ✅ |
| **适用场景** | 快速原型开发 | 生产环境 | 桌面应用 | 企业级部署 |

## 故障排除

### 未检测到MCP服务器

```bash
# Check if MCP server installed
npm list -g mcp-kafka         # kanapuli
which kafka-mcp-server        # tuannvm
pip show kafka-mcp-server     # Joel-hanson
confluent version             # Confluent
```

### 连接被拒绝

- 确保Kafka broker正在运行：`kcat -L -b localhost:9092`
- 检查防火墙规则
- 验证Kafka broker的URL（主机和端口是否正确）

### 认证失败

- 重新核对用户名、密码和API密钥
- 确认使用的认证方式与Kafka broker的配置一致
- 查看Kafka broker的日志以获取认证错误信息

### 操作失败

- 确认所选MCP服务器支持相应的操作（参见功能对比表）
- 检查Kafka broker的ACL设置（确保用户具有必要的权限）
- 使用`/sw-kafka:mcp-configure list-topics`命令验证主题是否存在

## 通过MCP执行Kafka操作

配置完成后，您可以通过MCP执行各种Kafka操作：

```typescript
import { MCPServerDetector } from './lib/mcp/detector';

const detector = new MCPServerDetector();
const result = await detector.detectAll();

// Use recommended server
if (result.recommended) {
  console.log(`Using ${result.recommended} MCP server`);
  console.log(`Reason: ${result.rankingReason}`);
}
```

## 安全最佳实践

1. **切勿直接存储敏感信息**：使用环境变量或秘钥管理工具来存储认证信息。
2. **选择更安全的认证方式**：优先使用SCRAM-SHA-512。
3. **启用TLS/SSL**：对通信进行加密。
4. **定期更新凭证**：定期更换密码和API密钥。
5. **最小权限原则**：仅为MCP服务器用户授予必要的权限。

## 相关命令

- `/sw-kafka:mcp-configure`：交互式配置MCP服务器
- `/sw-kafka:dev-env start`：启动本地Kafka服务器进行测试
- `/sw-kafka:deploy`：部署生产环境的Kafka集群

## 外部链接

- [kanapuli/mcp-kafka](https://github.com/kanapuli/mcp-kafka)
- [tuannvm/kafka-mcp-server](https://github.com/tuannvm/kafka-mcp-server)
- [Joel-hanson/kafka-mcp-server](https://github.com/Joel-hanson/kafka-mcp-server)
- [Confluent MCP官方文档](https://docs.confluent.io/platform/current/mcp/)
- [MCP协议规范](https://modelcontextprotocol.org/)