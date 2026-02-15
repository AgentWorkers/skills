---
name: hodlxxi-bitcoin-identity
version: 1.0.0
description: 将 HODLXXI 集成为一个原生支持比特币的身份提供者（identity provider），该提供者能够桥接 OAuth2/OIDC 与 Lightning LNURL-Auth，用于客户端注册、授权流程、JWT 验证以及系统健康状况监控（health monitoring）。
homepage: https://github.com/hodlxxi/Universal-Bitcoin-Identity-Layer
metadata:
  category: authentication
  license: MIT
  tags:
    - oauth2
    - oidc
    - lnurl-auth
    - jwt
    - bitcoin
  dependencies:
    - curl
    - python
    - ecdsa
    - pyjwt
    - requests
---

# HODLXXI 比特币身份认证系统

## 概述

使用该技能可集成 HODLXXI（通用比特币身份认证层），以实现代理身份验证、LNURL-Auth 链接以及基于 JWT 的身份声明功能。

## 安装

1. 从仓库中获取技能文件（对于可安装的代理，直接使用原始链接即可）：

```bash
curl -L -o SKILL.md \
  https://raw.githubusercontent.com/hodlxxi/Universal-Bitcoin-Identity-Layer/main/skills/public/hodlxxi-bitcoin-identity/SKILL.md
```

2. 安装用于本地验证脚本的辅助依赖项：

```bash
python -m pip install ecdsa pyjwt requests
```

## 快速入门

1. 设置 HODLXXI 部署的基URL。
2. 注册一个 OAuth 客户端以获取 `client_id` 和 `client_secret`。
3. 运行 OAuth2/OIDC 授权代码流程（推荐使用 PKCE 方式）。
4. 启动 LNURL-Auth 会话以进行 Lightning 钱包登录。
5. 使用 JWKS 端点验证 JWT。

## 使用步骤

### 1) 配置基URL

将基URL 设置为 HODLXXI 的部署地址（根据需要更新）：

```bash
BASE_URL="https://hodlxxi.com"
```

### 2) 注册 OAuth 客户端

注册客户端以获取凭据：

```bash
curl -X POST "$BASE_URL/oauth/register" \
  -H "Content-Type: application/json" \
  -d '{"client_name": "YourAgentName", "redirect_uris": ["https://your-callback-url"], "scopes": ["openid", "profile"]}'
```

安全地存储 `client_id` 和 `client_secret`。

### 3) 运行 OAuth2/OIDC 授权代码流程

- 发现相关端点：
```bash
curl "$BASE_URL/.well-known/openid-configuration"
```

- 创建授权请求（推荐使用 PKCE 方式）：
```bash
curl "$BASE_URL/oauth/authorize?client_id=your_client_id&redirect_uri=your_callback&response_type=code&scope=openid%20profile&code_challenge=your_challenge&code_challenge_method=S256"
```

- 将授权代码兑换为令牌：
```bash
curl -X POST "$BASE_URL/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=received_code&redirect_uri=your_callback&client_id=your_client_id&code_verifier=your_verifier"
```

- 获取访问令牌、ID 令牌（JWT）以及可选的刷新令牌。

### 4) 启动 LNURL-Auth 会话

- 创建会话并向用户显示 LNURL：
```bash
curl -X POST "$BASE_URL/api/lnurl-auth/create" \
  -H "Accept: application/json"
```

- 在用户使用 Lightning 钱包扫描 LNURL 后，等待会话完成：
```bash
curl "$BASE_URL/api/lnurl-auth/check/your_session_id"
```

### 5) 验证 JWT

- 获取 JWKS 证书：
```bash
curl "$BASE_URL/oauth/jwks.json"
```

- 使用 Python 进行验证（示例代码使用 PyJWT）：
```python
import jwt
import requests

jwks = requests.get("https://your-hodlxxi-deployment.com/oauth/jwks.json", timeout=10).json()
public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwks["keys"][0])
claims = jwt.decode(your_jwt, public_key, algorithms=["RS256"], audience="your_audience")
print(claims)
```

### 6) 监控系统健康状况和指标

- 检查系统的活跃状态和 OAuth 系统状态：
```bash
curl "$BASE_URL/health"
curl "$BASE_URL/oauthx/status"
```

## 代码示例

### 从 JSON 模板注册客户端

```bash
curl -X POST "$BASE_URL/oauth/register" \
  -H "Content-Type: application/json" \
  -d @templates/oauth-client.json
```

### 创建 LNURL 会话并等待响应

```bash
session_json=$(curl -s -X POST "$BASE_URL/api/lnurl-auth/create")
session_id=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["session_id"])' "$session_json")
curl "$BASE_URL/api/lnurl-auth/check/$session_id"
```

## 最佳实践

- 在生产环境中始终使用 HTTPS 并验证 TLS 证书。
- 将客户端密钥存储在密钥管理器或环境变量中。
- 对于公共客户端使用 PKCE 方式，对敏感客户端定期更换密钥。
- 将 LNURL 会话视为一次性使用，并设置较短的过期时间。
- 验证 JWT 中的 `aud`、`iss` 和 `exp` 属性。

## 高级功能

- 使用 `/oauthx/docs` 查看 OAuth/OIDC API 的详细文档。
- 使用 `/oauthx/status` 监控数据库和 LNURL 会话的状态。
- 通过服务器配置定期更换 JWKS 证书（JWKS 目录 + 更换周期）。

## OAuth 客户端的付费机制

API 调用按 **OAuth `client_id`**（代理/应用）计费，而非按会话公钥计费。当余额或免费配额用尽时，付费接口会返回 **HTTP 402** 错误，并提供 Lightning 购买令牌的路径。

### 计费接口（需要 OAuth 令牌）

- `POST /api/billing/agent/create-invoice`：创建账单
- `POST /api/billing/agent/check-invoice`：查看账单

- 创建账单的示例代码：
```bash
curl -X POST "$BASE_URL/api/billing/agent/create-invoice" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount_sats": 1000}'
```

- 查看账单的示例代码：
```bash
curl -X POST "$BASE_URL/api/billing/agent/check-invoice" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"invoice_id": "your_invoice_id"}'
```

### 402 错误响应

当调用付费接口时，如果余额不足，系统会返回以下错误响应：
```json
{
  "ok": false,
  "error": "payment_required",
  "code": "PAYMENT_REQUIRED",
  "client_id": "your_client_id",
  "cost_sats": 1,
  "balance_sats": 0,
  "create_invoice_endpoint": "/api/billing/agent/create-invoice",
  "hint": "Top up via Lightning PAYG"
}
```

## 支持文件

- `scripts/verify_signature.py`：用于在本地验证 LNURL-Auth 签名。
- `HEARTBEAT.md`：描述了系统的定期健康检查机制。
- `templates/oauth-client.json`：提供了标准的客户端注册数据格式。

## 可选辅助脚本

- 使用 `scripts/verify_signature.py` 在本地验证 LNURL 签名。请先安装相关依赖项：
```bash
python -m pip install ecdsa
python scripts/verify_signature.py --k1 <hex> --signature <hex> --pubkey <hex>
```