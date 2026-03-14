---
name: jwt-toolkit
description: 从命令行解码、检查并验证 JWT（JSON Web Token）令牌。可以显示令牌的头部信息（header）、有效载荷（payload）、使用的加密算法、过期状态以及已知的声明标签（claim labels）。适用于调试身份验证令牌、检查 JWT 是否已过期、分析 JWT 的声明内容、解码Bearer 令牌或解析令牌结构等场景。该工具会响应以下命令：`decode JWT`、`inspect token`、`JWT expired`、`parse JWT`、`check Bearer token`、`token claims`。
---
# JWT 工具包

这是一个完全不依赖外部库的 JWT 解码器与检查工具。它可以解码任何 JWT 令牌，并显示令牌的头部信息、负载中的声明（claims）、算法详情、过期状态以及签名信息。

## 快速入门

```bash
# Decode a JWT token
python3 scripts/jwt_decode.py eyJhbGciOiJIUzI1NiIs...

# Read token from file
python3 scripts/jwt_decode.py --file token.txt

# Read from stdin (pipe from curl, etc.)
echo "eyJ..." | python3 scripts/jwt_decode.py --stdin

# JSON output for scripting
python3 scripts/jwt_decode.py eyJ... --format json

# Also handles "Bearer " prefix automatically
python3 scripts/jwt_decode.py "Bearer eyJhbGciOiJIUzI1NiIs..."
```

## 主要功能

- 以人类可读的标签形式解码令牌的头部和负载中的声明
- 显示算法详情及安全警告（例如，使用“none”算法时的警告）
- 检查令牌的过期时间（剩余时间或自过期以来的时间）
- 支持 20 多种标准及常见的声明类型（如 iss、sub、aud、roles、scope 等）
- 自动去除令牌开头的 “Bearer ” 字符串
- 提供 JSON 和文本两种输出格式
- 无需任何外部依赖库——仅使用 Python 标准库实现