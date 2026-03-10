---
name: openfin-enable-banking
description: "通过 Enable Banking API 实现 PSD2 开放银行接口集成。可以连接德意志联邦共和国（DACH）地区的银行账户（如 Sparkasse、Volksbank、Deutsche Bank、Commerzbank、DKB、ING、Postbank）以获取账户余额和交易记录。该系统采用多租户架构，提供三种操作模式：账户注册、数据获取和账户续期。专为税务咨询自动化流程设计。"
license: MIT
---
# 启用银行服务功能

**通过 Enable Banking API 实现 PSD2 开放银行集成。**  
该功能支持多租户架构，用于连接银行、获取账户余额/交易记录以及续期会话。

## 快速入门

```
# 1. Onboard a new mandant
python scripts/onboard.py --bank "Sparkasse Karlsruhe" --country DE --mandant-id mueller

# 2. Fetch balances + transactions
python scripts/fetch.py --mandant-id mueller

# 3. Renew an expired session
python scripts/renew.py --mandant-id mueller
```

## 架构

```
┌─────────────┐     POST /auth      ┌──────────────────────┐
│  onboard.py │ ──────────────────→  │  Enable Banking API  │
│  renew.py   │ ←── redirect_url ──  │  api.enablebanking.com│
└──────┬──────┘                      └──────────┬───────────┘
       │                                        │
       │ poll pending_callbacks/                 │ User authorizes
       │                                        │ at bank portal
       ▼                                        ▼
┌──────────────────┐    GET /callback    ┌─────────────┐
│ callback_server  │ ←───────────────── │  Bank OAuth  │
│ (port 8443 HTTPS)│                    │  Redirect    │
└──────────────────┘                    └─────────────┘
       │
       │ saves code → pending_callbacks/{state}.json
       │
       ▼
┌─────────────┐     POST /sessions    ┌──────────────────────┐
│  onboard.py │ ──────────────────→   │  Enable Banking API  │
│  renew.py   │ ←── session + accs ── │                      │
└──────┬──────┘                       └──────────────────────┘
       │
       │ saves mandanten/{id}.json
       ▼
┌─────────────┐  GET /accounts/{uid}/ ┌──────────────────────┐
│  fetch.py   │ ──────────────────→   │  Enable Banking API  │
│             │ ←── balances + txns ──│                      │
└──────┬──────┘                       └──────────────────────┘
       │
       │ saves data/{id}/{date}.json
       ▼
   stdout: JSON
```

## 目录结构

```
enable-banking/
├── SKILL.md              # This file
├── config.json           # App credentials (DO NOT COMMIT)
├── .keys/                # Private key + callback certs (DO NOT COMMIT)
├── .gitignore
├── scripts/
│   ├── lib/
│   │   ├── __init__.py
│   │   └── auth.py       # Shared JWT + API helpers + mandant I/O
│   ├── callback_server.py   # HTTPS callback daemon
│   ├── onboard.py           # New mandant connection
│   ├── fetch.py             # Autonomous data fetch
│   └── renew.py             # Session renewal
├── references/
│   └── api-reference.md
├── mandanten/            # Per-mandant JSON files (DO NOT COMMIT)
├── data/                 # Fetched data (DO NOT COMMIT)
└── pending_callbacks/    # Temporary callback codes (DO NOT COMMIT)
```

## 脚本参考

### `scripts/lib/auth.py` — 公共模块

| 函数 | 描述 |
|---|---|
| `load_config()` | 加载 `config.json` 配置文件 |
| `generate_jwt(config)` | 生成用于 API 认证的 RS256 JWT 令牌 |
| `api_request(method, endpoint, token, **kwargs)` | 进行带重试机制（处理 429 错误和超时）的 API 调用 |
| `load_mandant(mandant_id)` | 加载指定租户的配置文件（`mandanten/{id}.json`） |
| `save_mandant(mandant_id, data)` | 保存租户配置文件（权限设置为 600） |
| `list_mandanten()` | 列出所有租户的 ID |

### `scripts/callback_server.py` — HTTPS 回调服务器

```bash
python scripts/callback_server.py              # Port 8443 (HTTPS)
python scripts/callback_server.py --port 9443  # Custom port
python scripts/callback_server.py --no-ssl     # HTTP only (dev)
```

- 首次运行时会自动生成自签名证书（保存在 `.keys/` 目录下） |
- 接收请求 `GET /callback?code=...&state=...`，并将其保存到 `pendingCallbacks/{state}.json` 文件中 |
- 响应请求 `GET /health`，返回 200 OK 状态码 |
- 作为后台进程运行：`exec background:true command:"python scripts/callback_server.py"` |

### `scripts/onboard.py` — 租户接入脚本

```bash
# Connect a new mandant
python scripts/onboard.py --bank "Sparkasse Karlsruhe" --mandant-id mueller

# With manual auth code (no callback server needed)
python scripts/onboard.py --bank "Sparkasse Karlsruhe" --mandant-id mueller --code ABC123

# List available banks
python scripts/onboard.py --list-banks --country DE

# Business account
python scripts/onboard.py --bank "DKB" --mandant-id firma --psu-type business
```

**操作流程（不使用 `--code` 参数时）：**
1. 发送 POST 请求到 `/auth`，系统生成重定向 URL；
2. 将重定向 URL 打印到标准输出（通过 WhatsApp 或电子邮件发送给用户）；
3. 定期检查 `pendingCallbacks/{state}.json` 文件（需要回调服务器处于运行状态）；
4. 使用生成的代码发送 POST 请求到 `/sessions`；
5. 保存租户的配置文件（`mandanten/{id}.json`）。

### `scripts/fetch.py` — 数据获取脚本

```bash
# Single mandant
python scripts/fetch.py --mandant-id mandant-1

# All mandanten
python scripts/fetch.py --all

# Date range
python scripts/fetch.py --mandant-id mandant-1 --date-from 2026-03-01 --date-to 2026-03-10

# Only balances or transactions
python scripts/fetch.py --mandant-id mandant-1 --balances-only
python scripts/fetch.py --mandant-id mandant-1 --transactions-only
```

- 默认数据获取范围为过去 30 天；
- 将获取的数据保存到 `data/{mandant-id}/{YYYY-MM-DD}.json` 文件中；
- 更新租户配置文件中的 `lastFetch` 时间戳；
- 如果会话过期（退出代码为 2），则需要重新获取数据。

### `scripts/renew.py` — 会话续期脚本

```bash
python scripts/renew.py --mandant-id mueller
python scripts/renew.py --mandant-id mueller --code ABC123
```

- 从现有租户配置文件中获取银行信息和国家代码；
- 使用与接入流程相同的认证机制；
- 保留会话的备份信息在租户配置文件中。

## 租户数据格式

`mandanten/{id}.json` 文件格式：

```json
{
  "mandantId": "mueller",
  "bank": "Sparkasse Karlsruhe",
  "country": "DE",
  "psuType": "personal",
  "sessionId": "cbe3cd33-...",
  "accounts": [
    {
      "uid": "2818be38-...",
      "iban": "DE17...",
      "name": "Max Mueller",
      "currency": "EUR",
      "product": "Sichteinlagen"
    }
  ],
  "validUntil": "2026-09-06T07:18:35Z",
  "createdAt": "2026-03-10T08:18:00Z",
  "lastFetch": null
}
```

## 数据输出格式

`data/{id}/{date}.json` 文件以及标准输出的内容：

```json
{
  "mandantId": "mueller",
  "fetchedAt": "2026-03-10T08:00:00Z",
  "accounts": [
    {
      "uid": "...",
      "iban": "DE17...",
      "name": "Max Mueller",
      "balances": [
        {"type": "CLBD", "amount": "-993.13", "currency": "EUR", "date": "2026-03-10"}
      ],
      "transactions": [
        {
          "date": "2026-03-02",
          "amount": "-171.00",
          "currency": "EUR",
          "creditDebit": "DBIT",
          "counterparty": "...",
          "description": "...",
          "bookingDate": "2026-03-02",
          "valueDate": "2026-03-02"
        }
      ]
    }
  ]
}
```

## 所需依赖库

- Python 3.10 及以上版本 |
- PyJWT（通过 `pip install PyJWT` 安装） |
- cryptography（通过 `pip install cryptography` 安装） |
- requests（通过 `pip install requests` 安装） |

## 部署方式

**本地（开发/测试环境）：**
- 回调服务器使用自签名证书；
- 支持使用 `--code` 参数（手动输入代码，无需额外服务器）。

**VPS（生产环境）：**
- 在 Nginx/Caddy 服务器后运行 `callback_server.py`，并使用真实的 SSL 证书；
- 将 `config.json` 文件中的 `redirectUrl` 指向你的域名；
- 使用 cron 定时执行 `scripts/fetch.py --all` 命令来获取数据。

## 故障排除

| 错误 | 解决方案 |
|---|---|
| `401 Unauthorized` | 确保在 Enable Banking 端口中输入的应用程序 ID 和令牌匹配正确 |
| `403 Forbidden` | 会话已过期，请执行 `python renew.py --mandant-id <id>` 来续期会话 |
| 退出代码为 2 | 会话已过期，需要重新获取数据 |
| 端口已被占用 | 使用 `lsof -i :8443 \| grep LISTEN \| awk '{print $2}' \| xargs kill` 来终止占用该端口的进程 |
| 未收到回调响应 | 确保回调服务器正在运行，并检查防火墙是否允许该端口的通信 |
| 请求被限制（429 错误） | 自动重试；如果问题持续存在，请稍后再次尝试。