---
name: newman
description: 使用 Newman CLI 通过 Postman 集合进行自动化 API 测试。适用于用户请求 API 测试、集合执行、自动化测试、CI/CD 集成，或提及“Postman”、“Newman”、“API 测试”、“运行集合”或“自动化测试”的场景。
---

# Newman – Postman 命令行运行器

Newman 是一个用于 Postman 的命令行工具，允许您直接从命令行运行和测试 Postman 集合。它具备强大的报告功能、环境管理功能以及与持续集成（CI）/持续交付（CD）系统的集成能力。

## 快速入门

### 安装

```bash
# Global install (recommended)
npm install -g newman

# Project-specific
npm install --save-dev newman

# Verify
newman --version
```

### 基本使用

```bash
# Run collection
newman run collection.json

# With environment
newman run collection.json -e environment.json

# With globals
newman run collection.json -g globals.json

# Combined
newman run collection.json -e env.json -g globals.json -d data.csv
```

## 核心工作流程

### 1. 从 Postman 桌面应用导出数据

**在 Postman 中：**
1. 选择“Collections” → 点击“...” → 选择“Export”
2. 选择“Collection v2.1”（推荐格式）
3. 将文件保存为 `collection.json`

**环境配置：**
1. 选择“Environments” → 点击“...” → 选择“Export”
2. 将文件保存为 `environment.json`

### 2. 运行测试

```bash
# Basic run
newman run collection.json

# With detailed output
newman run collection.json --verbose

# Fail on errors
newman run collection.json --bail

# Custom timeout (30s)
newman run collection.json --timeout-request 30000
```

### 3. 基于数据的测试

**数据格式：CSV**
```csv
username,password
user1,pass1
user2,pass2
```

**运行方式：**
```bash
newman run collection.json -d test_data.csv --iteration-count 2
```

### 4. 报告生成

```bash
# CLI only (default)
newman run collection.json

# HTML report
newman run collection.json --reporters cli,html --reporter-html-export report.html

# JSON export
newman run collection.json --reporters cli,json --reporter-json-export results.json

# JUnit (for CI)
newman run collection.json --reporters cli,junit --reporter-junit-export junit.xml

# Multiple reporters
newman run collection.json --reporters cli,html,json,junit \
  --reporter-html-export ./reports/newman.html \
  --reporter-json-export ./reports/newman.json \
  --reporter-junit-export ./reports/newman.xml
```

### 5. 安全最佳实践

**❌ **切勿在集合中硬编码敏感信息！**  
建议使用环境变量来存储敏感数据：

```bash
# Export sensitive vars
export API_KEY="your-secret-key"
export DB_PASSWORD="your-db-pass"

# Newman auto-loads from env
newman run collection.json -e environment.json

# Or pass directly
newman run collection.json --env-var "API_KEY=secret" --env-var "DB_PASSWORD=pass"
```

**在 Postman 集合测试中：**
```javascript
// Use {{API_KEY}} in requests
pm.request.headers.add({key: 'Authorization', value: `Bearer {{API_KEY}}`});

// Access in scripts
const apiKey = pm.environment.get("API_KEY");
```

**环境配置文件（environment.json）：**
```json
{
  "name": "Production",
  "values": [
    {"key": "BASE_URL", "value": "https://api.example.com", "enabled": true},
    {"key": "API_KEY", "value": "{{$processEnvironment.API_KEY}}", "enabled": true}
  ]
}
```

Newman 会自动将 `{{$processEnvironment.API_KEY}}` 替换为对应的环境变量值。

## 常见使用场景

### 持续集成/持续交付（CI/CD）集成

请参考 `references/ci-cd-examples.md`，了解如何将 Newman 与 GitHub Actions、GitLab CI 和 Jenkins 等工具集成。

### 自动化回归测试

```bash
#!/bin/bash
# scripts/run-api-tests.sh

set -e

echo "Running API tests..."

newman run collections/api-tests.json \
  -e environments/staging.json \
  --reporters cli,html,junit \
  --reporter-html-export ./test-results/newman.html \
  --reporter-junit-export ./test-results/newman.xml \
  --bail \
  --color on

echo "Tests completed. Report: ./test-results/newman.html"
```

### 负载测试

```bash
# Run with high iteration count
newman run collection.json \
  -n 100 \
  --delay-request 100 \
  --timeout-request 5000 \
  --reporters cli,json \
  --reporter-json-export load-test-results.json
```

### 并行执行

```bash
# Install parallel runner
npm install -g newman-parallel

# Run collections in parallel
newman-parallel -c collection1.json,collection2.json,collection3.json \
  -e environment.json \
  --reporters cli,html
```

## 高级功能

### 自定义脚本

**请求前脚本（在 Postman 中配置）：**
```javascript
// Generate dynamic values
pm.environment.set("timestamp", Date.now());
pm.environment.set("nonce", Math.random().toString(36).substring(7));
```

**测试脚本（在 Postman 中配置）：**
```javascript
// Status code check
pm.test("Status is 200", function() {
    pm.response.to.have.status(200);
});

// Response body validation
pm.test("Response has user ID", function() {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('user_id');
});

// Response time check
pm.test("Response time < 500ms", function() {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

// Set variable from response
pm.environment.set("user_token", pm.response.json().token);
```

### SSL/TLS 配置

```bash
# Disable SSL verification (dev only!)
newman run collection.json --insecure

# Custom CA certificate
newman run collection.json --ssl-client-cert-list cert-list.json

# Client certificates
newman run collection.json \
  --ssl-client-cert client.pem \
  --ssl-client-key key.pem \
  --ssl-client-passphrase "secret"
```

### 错误处理

**集合未找到：**
- 使用绝对路径：`newman run /full/path/to/collection.json`
- 检查文件权限：`ls -la collection.json`

**环境变量未加载：**
- 验证语法：`{{$processEnvironment.VAR_NAME}}`
- 查看变量值：`echo $VAR_NAME`
- 可以使用 `--env-var` 参数作为备用方案

**超时错误：**
- 增加超时时间：`--timeout-request 60000`（60 秒）
- 检查网络连接是否正常
- 确认 API 端点是否可访问

**SSL 错误：**
- 开发环境：暂时使用 `--insecure` 参数
- 生产环境：添加 CA 证书：`--ssl-extra-ca-certs`

**内存问题（处理大型集合）：**
- 减少测试迭代次数
- 将集合拆分为更小的部分
- 增加 Node.js 的内存分配：`NODE_OPTIONS=--max-old-space-size=4096 newman run ...`

## 最佳实践

1. **版本控制**：将集合和环境配置文件存储在 Git 中。
2. **环境分离**：为开发、测试和生产环境分别配置不同的文件。
3. **敏感信息管理**：使用环境变量，切勿将敏感信息直接提交到代码库。
4. **文件命名规范**：使用描述性强的文件名。
5. **测试原子性**：每个测试用例应只验证一个具体的功能。
6. **添加断言**：为每个请求添加详细的测试逻辑。
7. **文档编写**：利用 Postman 的描述功能来提供测试背景信息。
8. **集成到 CI 流程**：在每次提交（PR）时自动运行 Newman。
9. **报告生成**：保留 HTML 报告以供后续分析。
10. **设置合理的超时时间**：根据生产环境的实际需求设置合适的超时值。

## 参考资料

- **CI/CD 集成示例**：请参阅 `references/ci-cd-examples.md`。
- **高级使用技巧**：请参阅 `references/advanced-patterns.md`。
- **官方文档**：https://learning.postman.com/docs/running-collections/using-newman-cli/command-line-integration-with-newman/