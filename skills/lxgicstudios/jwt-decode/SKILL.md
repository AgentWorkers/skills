---
name: JWT Decode - Token Inspector CLI
description: 从命令行解码并检查 JWT 令牌。可以验证令牌的有效期、提取其中的声明信息，并用于调试身份验证过程。无需再使用 jwt.io 等第三方工具。这是一个免费的命令行工具。
---

# JWT 解码

从终端解码 JWT（JSON Web Tokens），查看其内部内容，并检查其是否已过期。

## 安装

```bash
npm install -g @lxgicstudios/jwt-decode
```

## 命令

### 解码令牌

```bash
npx @lxgicstudios/jwt-decode eyJhbGciOiJIUzI1NiIs...

# Works with Bearer prefix
npx @lxgicstudios/jwt-decode "Bearer eyJhbGci..."
```

### 从环境变量中获取

```bash
echo $AUTH_TOKEN | npx @lxgicstudios/jwt-decode
```

### 从文件中获取

```bash
npx @lxgicstudios/jwt-decode -f token.txt
```

### 检查是否过期

```bash
npx @lxgicstudios/jwt-decode --check $TOKEN && echo "Valid" || echo "Expired"
```

### 提取特定字段

```bash
npx @lxgicstudios/jwt-decode -c sub $TOKEN
npx @lxgicstudios/jwt-decode -c email $TOKEN
```

## 示例输出

```
Header
──────
  alg: "HS256"
  typ: "JWT"

Payload
───────
  sub: "1234567890"
  name: "John Doe"
  email: "john@example.com"
  iat: 1706547200 (2024-01-29T16:00:00.000Z)
  exp: 1706633600 (2024-01-30T16:00:00.000Z)

Status
──────
  Valid - expires in 23 hours
```

## 选项

| 选项 | 描述 |
|--------|-------------|
| `-f, --file` | 从文件中读取数据 |
| `-c, --claim` | 提取特定字段 |
| `--header` | 仅显示头部信息 |
| `--payload` | 仅显示有效载荷 |
| `--json` | 以 JSON 格式输出 |
| `--check` | 如果令牌过期，则退出（返回代码 1） |

## 常见用法

**调试认证令牌：**
```bash
npx @lxgicstudios/jwt-decode $AUTH_TOKEN
```

**从令牌中获取用户 ID：**
```bash
npx @lxgicstudios/jwt-decode -c sub $TOKEN
```

**在脚本中使用：**
```bash
if npx @lxgicstudios/jwt-decode --check $TOKEN 2>/dev/null; then
  echo "Token valid"
else
  echo "Token expired, refreshing..."
fi
```

## 特点

- 输出结果支持颜色显示，便于阅读 |
- 自动处理令牌持有者前缀 |
- 显示易于理解的过期时间 |
- 支持时间戳转换 |
- 提供适合脚本使用的退出代码 |
- 支持 JSON 格式输出 |

---

**由 [LXGIC Studios](https://lxgicstudios.com) 开发**

🔗 [GitHub](https://github.com/lxgicstudios/jwt-decode) · [Twitter](https://x.com/lxgicstudios)