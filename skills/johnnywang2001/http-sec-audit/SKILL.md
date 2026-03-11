---
name: http-sec-audit
description: 审计任何网站的HTTP安全头信息。当用户要求检查安全头信息、加固Web服务器、审核HSTS/CSP/X-Frame-Options的合规性、查找信息泄露（如Server、X-Powered-By字段）或评估网站的安全状况时，可使用该工具。该工具会检查10个安全头信息，并给出A–F等级的评估结果。支持多个URL输入，并支持JSON格式的输出。
---
# HTTP安全头审计

扫描任何URL，检测是否存在缺失或配置错误的安全头，并生成一份包含评分、修复建议及信息泄露检测结果的报告。

## 快速入门

```bash
python3 scripts/sec_headers.py https://example.com
```

## 命令

```bash
# Single URL audit
python3 scripts/sec_headers.py https://example.com

# Multiple URLs
python3 scripts/sec_headers.py https://example.com https://google.com https://github.com

# JSON output (for programmatic use)
python3 scripts/sec_headers.py https://example.com --json

# Custom timeout
python3 scripts/sec_headers.py https://example.com --timeout 5
```

## 检查内容

**安全头**（按严重程度分级）：
- `Strict-Transport-Security` (HSTS) — 高风险
- `Content-Security-Policy` (CSP) — 高风险
- `X-Content-Type-Options` — 中等风险
- `X-Frame-Options` — 中等风险
- `Referrer-Policy` — 中等风险
- `Permissions-Policy` — 中等风险
- `X-XSS-Protection` — 低风险
- `Cross-Origin-Opener-Policy` (COOP) — 低风险
- `Cross-Origin-Resource-Policy` (CORP) — 低风险
- `Cross-Origin-Embedder-Policy` (COEP) — 低风险

**信息泄露检测：**
- `Server` 头（软件版本泄露）
- `X-Powered-By`（技术栈泄露）
- `X-AspNet-Version`（框架版本泄露）

## 评分标准

| 评分 | 分数 | 含义 |
|-------|-------|---------|
| A | 90–100 | 优秀 — 所有关键安全头均存在 |
| B | 75–89 | 良好 — 存在少量缺失的安全头 |
| C | 50–74 | 一般 — 重要安全头缺失 |
| D | 25–49 | 较差 — 存在严重的安全风险 |
| F | 0–24 | 失败 — 大多数安全头均缺失 |

## 所需依赖项

```bash
pip install requests
```