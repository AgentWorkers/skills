---
name: api-dev
description: 用于搭建、测试、文档编写和调试 REST 以及 GraphQL API 的工具。当用户需要创建 API 端点、编写集成测试、生成 OpenAPI 规范、使用 curl 进行测试、模拟 API 行为或排查 HTTP 相关问题时，可以使用该工具。
metadata: {"clawdbot":{"emoji":"🔌","requires":{"anyBins":["curl","node","python3"]},"os":["linux","darwin","win32"]}}
---

# API开发

通过命令行构建、测试、文档编写和调试HTTP API。涵盖了API的整个生命周期：搭建端点、使用curl进行测试、生成OpenAPI文档、模拟服务以及调试问题。

## 使用场景

- 搭建新的REST或GraphQL端点
- 使用curl或脚本测试API
- 生成或验证OpenAPI/Swagger规范
- 为开发目的模拟外部API
- 调试HTTP请求/响应问题
- 对端点进行负载测试

## 使用curl测试API

### GET请求

```bash
# Basic GET
curl -s https://api.example.com/users | jq .

# With headers
curl -s -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  https://api.example.com/users | jq .

# With query params
curl -s "https://api.example.com/users?page=2&limit=10" | jq .

# Show response headers too
curl -si https://api.example.com/users
```

### POST/PUT/PATCH/DELETE

```bash
# POST JSON
curl -s -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "Alice", "email": "alice@example.com"}' | jq .

# PUT (full replace)
curl -s -X PUT https://api.example.com/users/123 \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Updated", "email": "alice@example.com"}' | jq .

# PATCH (partial update)
curl -s -X PATCH https://api.example.com/users/123 \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice V2"}' | jq .

# DELETE
curl -s -X DELETE https://api.example.com/users/123

# POST form data
curl -s -X POST https://api.example.com/upload \
  -F "file=@document.pdf" \
  -F "description=My document"
```

### 调试请求

```bash
# Verbose output (see full request/response)
curl -v https://api.example.com/health 2>&1

# Show only response headers
curl -sI https://api.example.com/health

# Show timing breakdown
curl -s -o /dev/null -w "DNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTLS: %{time_appconnect}s\nFirst byte: %{time_starttransfer}s\nTotal: %{time_total}s\n" https://api.example.com/health

# Follow redirects
curl -sL https://api.example.com/old-endpoint

# Save response to file
curl -s -o response.json https://api.example.com/data
```

## API测试脚本

### Bash测试运行器

```bash
#!/bin/bash
# api-test.sh - Simple API test runner
BASE_URL="${1:-http://localhost:3000}"
PASS=0
FAIL=0

assert_status() {
  local method="$1" url="$2" expected="$3" body="$4"
  local args=(-s -o /dev/null -w "%{http_code}" -X "$method")
  if [ -n "$body" ]; then
    args+=(-H "Content-Type: application/json" -d "$body")
  fi
  local status
  status=$(curl "${args[@]}" "$BASE_URL$url")
  if [ "$status" = "$expected" ]; then
    echo "PASS: $method $url -> $status"
    ((PASS++))
  else
    echo "FAIL: $method $url -> $status (expected $expected)"
    ((FAIL++))
  fi
}

assert_json() {
  local url="$1" jq_expr="$2" expected="$3"
  local actual
  actual=$(curl -s "$BASE_URL$url" | jq -r "$jq_expr")
  if [ "$actual" = "$expected" ]; then
    echo "PASS: GET $url | jq '$jq_expr' = $expected"
    ((PASS++))
  else
    echo "FAIL: GET $url | jq '$jq_expr' = $actual (expected $expected)"
    ((FAIL++))
  fi
}

# Health check
assert_status GET /health 200

# CRUD tests
assert_status POST /api/users 201 '{"name":"Test","email":"test@test.com"}'
assert_status GET /api/users 200
assert_json /api/users '.[-1].name' 'Test'
assert_status DELETE /api/users/1 204

# Auth tests
assert_status GET /api/admin 401
assert_status GET /api/admin 403  # with wrong role

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
```

### Python测试运行器

```python
#!/usr/bin/env python3
"""api_test.py - API integration test suite."""
import json, sys, urllib.request, urllib.error

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"
PASS = FAIL = 0

def request(method, path, body=None, headers=None):
    """Make an HTTP request, return (status, body_dict, headers)."""
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body else None
    hdrs = {"Content-Type": "application/json", "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        resp = urllib.request.urlopen(req)
        body = json.loads(resp.read().decode()) if resp.read() else None
    except urllib.error.HTTPError as e:
        return e.code, None, dict(e.headers)
    return resp.status, body, dict(resp.headers)

def test(name, fn):
    """Run a test function, track pass/fail."""
    global PASS, FAIL
    try:
        fn()
        print(f"  PASS: {name}")
        PASS += 1
    except AssertionError as e:
        print(f"  FAIL: {name} - {e}")
        FAIL += 1

def assert_eq(actual, expected, msg=""):
    assert actual == expected, f"got {actual}, expected {expected}. {msg}"

# --- Tests ---
print(f"Testing {BASE}\n")

test("GET /health returns 200", lambda: (
    assert_eq(request("GET", "/health")[0], 200)
))

test("POST /api/users creates user", lambda: (
    assert_eq(request("POST", "/api/users", {"name": "Test", "email": "t@t.com"})[0], 201)
))

test("GET /api/users returns array", lambda: (
    assert_eq(type(request("GET", "/api/users")[1]), list)
))

test("GET /api/notfound returns 404", lambda: (
    assert_eq(request("GET", "/api/notfound")[0], 404)
))

print(f"\nResults: {PASS} passed, {FAIL} failed")
sys.exit(0 if FAIL == 0 else 1)
```

## OpenAPI规范生成

### 从现有端点生成规范

```bash
# Scaffold an OpenAPI 3.0 spec from curl responses
# Run this, then fill in the details
cat > openapi.yaml << 'EOF'
openapi: "3.0.3"
info:
  title: My API
  version: "1.0.0"
  description: API description here
servers:
  - url: http://localhost:3000
    description: Local development
paths:
  /health:
    get:
      summary: Health check
      responses:
        "200":
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: ok
  /api/users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        "200":
          description: List of users
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/User"
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateUser"
      responses:
        "201":
          description: User created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "400":
          description: Validation error
  /api/users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          description: User details
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "404":
          description: Not found
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        email:
          type: string
          format: email
        createdAt:
          type: string
          format: date-time
    CreateUser:
      type: object
      required:
        - name
        - email
      properties:
        name:
          type: string
        email:
          type: string
          format: email
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
EOF
```

### 验证OpenAPI规范

```bash
# Using npx (no install needed)
npx @redocly/cli lint openapi.yaml

# Quick check: is the YAML valid?
python3 -c "import yaml; yaml.safe_load(open('openapi.yaml'))" && echo "Valid YAML"
```

## 模拟服务器

### 使用Python快速创建模拟服务器

```python
#!/usr/bin/env python3
"""mock_server.py - Lightweight API mock from OpenAPI-like config."""
import json, http.server, re, sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

# Define mock routes: (method, path_pattern) -> response
ROUTES = {
    ("GET", "/health"): {"status": 200, "body": {"status": "ok"}},
    ("GET", "/api/users"): {"status": 200, "body": [
        {"id": "1", "name": "Alice", "email": "alice@example.com"},
        {"id": "2", "name": "Bob", "email": "bob@example.com"},
    ]},
    ("POST", "/api/users"): {"status": 201, "body": {"id": "3", "name": "Created"}},
    ("GET", r"/api/users/\w+"): {"status": 200, "body": {"id": "1", "name": "Alice"}},
    ("DELETE", r"/api/users/\w+"): {"status": 204, "body": None},
}

class MockHandler(http.server.BaseHTTPRequestHandler):
    def _handle(self):
        for (method, pattern), response in ROUTES.items():
            if self.command == method and re.fullmatch(pattern, self.path.split('?')[0]):
                self.send_response(response["status"])
                if response["body"] is not None:
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(response["body"]).encode())
                else:
                    self.end_headers()
                return
        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Not found"}).encode())

    do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = _handle

    def log_message(self, fmt, *args):
        print(f"{self.command} {self.path} -> {args[1] if len(args) > 1 else '?'}")

print(f"Mock server on http://localhost:{PORT}")
http.server.HTTPServer(("", PORT), MockHandler).serve_forever()
```

运行命令：`python3 mock_server.py 8080`

## Node.js Express框架

### 最简单的REST API搭建

```javascript
// server.js - Minimal Express REST API
const express = require('express');
const app = express();
app.use(express.json());

// In-memory store
const items = new Map();
let nextId = 1;

// CRUD endpoints
app.get('/api/items', (req, res) => {
  const { page = 1, limit = 20 } = req.query;
  const all = [...items.values()];
  const start = (page - 1) * limit;
  res.json({ items: all.slice(start, start + +limit), total: all.length });
});

app.get('/api/items/:id', (req, res) => {
  const item = items.get(req.params.id);
  if (!item) return res.status(404).json({ error: 'Not found' });
  res.json(item);
});

app.post('/api/items', (req, res) => {
  const { name, description } = req.body;
  if (!name) return res.status(400).json({ error: 'name required' });
  const id = String(nextId++);
  const item = { id, name, description: description || '', createdAt: new Date().toISOString() };
  items.set(id, item);
  res.status(201).json(item);
});

app.put('/api/items/:id', (req, res) => {
  if (!items.has(req.params.id)) return res.status(404).json({ error: 'Not found' });
  const item = { ...req.body, id: req.params.id, updatedAt: new Date().toISOString() };
  items.set(req.params.id, item);
  res.json(item);
});

app.delete('/api/items/:id', (req, res) => {
  if (!items.has(req.params.id)) return res.status(404).json({ error: 'Not found' });
  items.delete(req.params.id);
  res.status(204).end();
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal server error' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`API running on http://localhost:${PORT}`));
```

### 设置环境

```bash
mkdir my-api && cd my-api
npm init -y
npm install express
node server.js
```

## 调试技巧

### 检查端口是否被占用

```bash
# Linux/macOS
lsof -i :3000
# or
ss -tlnp | grep 3000

# Kill process on port
kill $(lsof -t -i :3000)
```

### 测试CORS（跨源资源共享）

```bash
# Preflight request
curl -s -X OPTIONS https://api.example.com/users \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -I
```

### 监控响应时间的变化

```bash
# Quick benchmark (10 requests)
for i in $(seq 1 10); do
  curl -s -o /dev/null -w "%{time_total}\n" http://localhost:3000/api/users
done | awk '{sum+=$1; if($1>max)max=$1} END {printf "Avg: %.3fs, Max: %.3fs\n", sum/NR, max}'
```

### 检查JWT令牌

```bash
# Decode JWT payload (no verification)
echo "$TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null | jq .
```

## 提示

- 使用`jq`处理JSON响应：`curl -s url | jq '.items[] | {id, name}'`
- 在每个带有请求体的请求中设置`Content-Type`头——缺少该头会导致隐式的400错误
- 使用`-w '\n'`选项让curl的输出以换行符结尾
- 对于较大的响应体，可以将输出通过`jq -C . | less -R`命令分页显示（并带有颜色提示）
- 测试错误情况：无效的JSON、字段缺失、类型错误、权限问题、请求未找到等
- 对于WebSocket测试：`npx wscat -c ws://localhost:3000/ws`