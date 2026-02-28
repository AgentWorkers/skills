---
name: sectors-api
description: 从 Sectors API (api.sectors.app) 中查询 IDX（印度尼西亚证券交易所）和 SGX（新加坡证券交易所）市场的金融市场数据。当用户询问股票价格、公司报告、财务信息、市场指数、表现最佳的股票、股息、收益、市值或任何印度尼西亚或新加坡股市数据时，可以使用此功能。仅通过 Python 和 requests 库进行调用。
license: MIT
compatibility: >
  Requires Python 3.8+ with the requests library. Requires the SECTORS_API_KEY
  environment variable to be set. Requires network access to https://api.sectors.app.
metadata:
  author: supertype
  version: "1.1"
allowed-tools: Bash(python:*) Bash(pip:*) Read
---
# Sectors API

通过 Sectors REST API 查询 IDX 和 SGX 金融市场数据。

**完整 API 文档**：https://sectors.app/api

## 约束条件

- 仅向 `https://api.sectors.app/v1` 发送 HTTP 请求。切勿调用其他域名、数据库或外部服务。
- 所有端点均为返回 JSON 数据的 `GET` 请求。
- 严禁硬编码或猜测 API 密钥。始终从 `SECTORS_API_KEY` 环境变量中获取 API 密钥。
- 如果未设置 `SECTORS_API_KEY`，请提示用户设置它：`export SECTORS_API_KEY="your-api-key-here"`，或运行 `scripts/check_setup.py` 脚本进行检查。

## 设置

### 1. 设置 API 密钥

API 密钥必须作为 `SECTORS_API_KEY` 环境变量存在。

```bash
# Option A: Set in your current shell
export SECTORS_API_KEY="your-api-key-here"

# Option B: Add to your shell profile (~/.bashrc, ~/.zshrc) for persistence
echo 'export SECTORS_API_KEY="your-api-key-here"' >> ~/.bashrc

# Option C: Use a .env file in the project root (see .env.example)
```

针对特定代理的配置：
- **Claude Code**：`claude config set env SECTORS_API_KEY your-api-key-here`
- **OpenCode**：在 `~/.config/opencode/config.json` 的 `env` 部分进行设置
- **Cursor**：设置 > 功能 > 环境变量

### 2. 安装依赖项

```bash
pip install requests
```

### 3. 验证设置（可选）

```bash
python scripts/check_setup.py
```

### 发送请求

```python
import os
import requests

API_KEY = os.environ["SECTORS_API_KEY"]
BASE_URL = "https://api.sectors.app/v1"

headers = {"Authorization": API_KEY}
response = requests.get(f"{BASE_URL}/subsectors/", headers=headers)
data = response.json()
```

`Authorization` 头部需要包含原始的 API 密钥。切勿在其前加上 `Bearer`。

## 端点选择表

根据用户需求选择合适的端点：

### 市场结构

| 用户需求 | 端点 | 必需参数 |
|---|---|---|
| 列出所有子行业 | `GET /subsectors/` | 无 |
| 列出所有行业 | `GET /industries/` | 无 |
| 列出所有子行业 | `GET /subindustries/` | 无 |
| SGX 行业列表 | `GET /sgx/sectors/` | 无 |

### 公司查询

| 用户需求 | 端点 | 必需参数 |
|---|---|---|
| 获取某个子行业中的公司 | `GET /companies/?sub_sector={sub_sector}` | `sub_sector` |
| 获取某个子行业中的公司 | `GET /companies/?sub_industry={sub_industry}` | `sub_industry` |
| 获取指数中的公司 | `GET /index/{index}/` | `index` |
| 获取包含细分数据的公司 | `GET /companies/list_companies_with_segments/` | 无 |
| 按行业获取 SGX 公司 | `GET /sgx/companies/?sector={sector}` | `sector` |

### 公司详情

| 用户需求 | 端点 | 必需参数 |
|---|---|---|
| 获取完整公司报告（IDX） | `GET /company/report/{ticker}/` | `ticker` |
| 获取 SGX 公司报告 | `GET /sgx/company/report/{ticker}` | `ticker` |
| 获取上市表现 | `GET /listing-performance/{ticker}/` | `ticker` |
| 获取季度财务数据 | `GET /company/get_quarterly_financial_dates/{ticker}/` | `ticker` |
| 获取季度财务报表 | `GET /financials/quarterly/{ticker}/` | `ticker` |
| 获取公司细分信息 | `GET /company/get-segments/{ticker}/` | `ticker` |

### 市场数据

| 用户需求 | 端点 | 必需参数 |
|---|---|---|
| 获取每日股票价格 | `GET /daily/{ticker}` | `ticker` |
| 获取指数每日数据 | `GET /index-daily/{index_code}/` | `index_code` |
| 获取指数概要 | `GET /index/{index}/` | `index` |
| 获取 IDX 总市值 | `GET /idx-total/` | 无 |

### 排名与筛选

| 用户需求 | 端点 | 必需参数 |
|---|---|---|
| 获取涨幅/跌幅最大的公司 | `GET /companies/top-changes/` | 无（全部为可选参数） |
| 按指标排序的顶级公司 | `GET /companies/top/` | 无（全部为可选参数） |
| 增长最快的公司 | `GET /companies/top-growth/` | 无（全部为可选参数） |
| 流量最大的股票 | `GET /most-traded/` | 无（全部为可选参数） |
| SGX 行业龙头公司 | `GET /sgx/companies/top/` | 无（全部为可选参数） |

有关完整的参数列表和响应格式，请参阅：
- [references/idx-endpoints.md](references/idx-endpoints.md) —— 所有 18 个 IDX 端点
- [references/sgx-endpoints.md](references/sgx-endpoints.md) —— 所有 6 个 SGX 端点
- [assets/endpoint-map.md](assets/endpoint-map.md) —— 快速查找表

## 常用模式

### 获取公司报告

```python
import os
import requests

API_KEY = os.environ["SECTORS_API_KEY"]
BASE_URL = "https://api.sectors.app/v1"
headers = {"Authorization": API_KEY}

ticker = "BBCA"
params = {"sections": "overview,valuation,financials"}
resp = requests.get(f"{BASE_URL}/company/report/{ticker}/", headers=headers, params=params)
report = resp.json()

print(report["company_name"])
print(report["overview"]["market_cap"])
```

可用部分：`overview`、`valuation`、`future`、`peers`、`financials`、`dividend`、`management`、`ownership`。可以使用 `all` 来获取所有部分，或者省略某些部分。

### 获取指定日期范围内的每日股票价格

```python
import os
import requests

API_KEY = os.environ["SECTORS_API_KEY"]
BASE_URL = "https://api.sectors.app/v1"
headers = {"Authorization": API_KEY}

ticker = "BBRI.JK"
# Normalize: uppercase, strip .JK
clean = ticker.upper().replace(".JK", "")

params = {"start": "2025-01-01", "end": "2025-01-31"}
resp = requests.get(f"{BASE_URL}/daily/{clean}", headers=headers, params=params)
prices = resp.json()

for day in prices:
    print(day["date"], day["close"], day["volume"])
```

### 查找涨幅/跌幅最大的公司

```python
import os
import requests

API_KEY = os.environ["SECTORS_API_KEY"]
BASE_URL = "https://api.sectors.app/v1"
headers = {"Authorization": API_KEY}

params = {
    "classifications": "top_gainers,top_losers",
    "periods": "7d,30d",
    "n_stock": 5,
    "min_mcap_billion": 5000,
}
resp = requests.get(f"{BASE_URL}/companies/top-changes/", headers=headers, params=params)
movers = resp.json()

for stock in movers["top_gainers"]["7d"]:
    print(stock["symbol"], stock["price_change"])
```

### 列出指数中的公司

```python
import os
import requests

API_KEY = os.environ["SECTORS_API_KEY"]
BASE_URL = "https://api.sectors.app/v1"
headers = {"Authorization": API_KEY}

# Available: lq45, idx30, kompas100, jii70, idxhidiv20, srikehati, etc.
resp = requests.get(f"{BASE_URL}/index/lq45/", headers=headers)
companies = resp.json()

for c in companies:
    print(c["symbol"], c["company_name"])
```

### 获取 SGX 公司报告

```python
import os
import requests

API_KEY = os.environ["SECTORS_API_KEY"]
BASE_URL = "https://api.sectors.app/v1"
headers = {"Authorization": API_KEY}

ticker = "D05"  # DBS Group
resp = requests.get(f"{BASE_URL}/sgx/company/report/{ticker}", headers=headers)
report = resp.json()

print(report["name"])
print(report["valuation"]["pe"])
print(report["financials"]["gross_margin"])
```

## 股票代码规范化

| 市场 | 规则 | 示例 |
|---|---|---|
| IDX | 将代码转换为大写，并去掉 `.JK` 后缀 | `bbca.jk` -> `BBCA` |
| SGX | 将代码转换为大写，并去掉 `.SI` 后缀 | `d05.si` -> `D05` |

在传递给端点之前，请务必进行规范化处理。

## 注意事项

1. **授权头部格式**：使用 `Authorization: <raw_key>`。不要使用 `Bearer <key>` 或 `Authorization: Bearer <key>`。
2. **日期格式**：始终使用 `YYYY-MM-DD` 格式。例如：`2025-06-15`。
3. **日期范围限制**：`/most-traded/` 端点要求的开始日期和结束日期必须在 90 天之内。
4. 子行业和行业的命名规则：使用 `banks`、`financing-service`、`consumer-defensive` 等格式，不要使用驼峰式或蛇形命名法。
5. **嵌套响应结构**：排名相关的端点（`top-changes`、`top`、`top-growth`）返回的数据结构是先按分类排序，再按时间段排序。请确保正确导航这两层结构。

   ```python
   # top-changes returns: { "top_gainers": { "7d": [...], "30d": [...] } }
   # top returns: { "dividend_yield": [...], "revenue": [...] }
   ```

6. **市值单位**：IDX 的市值单位为十亿印尼盾（`min_mcap_billion`），SGX 的市值单位为百万新加坡元（`min_mcap_million`）。
7. **默认值**：许多可选参数的默认值为 `"all"` 或特定值（例如 `n_stock` 的默认值为 5，`min_mcap_billion` 的默认值为 5000）。需要不同行为时请明确指定。
8. **指数代码**：IDX 指数的每日数据使用小写代码（如 `ihsg`、`lq45`、`idx30`）。按行业查询公司时也使用相同的代码。
9. **季度财务报表的 `approx` 标志**：当 `approx=true` 时，如果找不到精确匹配的 `report_date`，API 会返回最接近的季度数据。
10. **公司报告部分参数**：只有当请求所有部分时才需要在 URL 中添加 `sections` 参数；如果只需要部分内容，则可以省略该参数。

## 可用的 IDX 指数

`ftse`、`idx30`、`idxbumn20`、`idxesgl`、`idxg30`、`idxhidiv20`、`idxv30`、`jii70`、`kompas100`、`lq45`、`sminfra18`、`srikehati`、`economic30`、`idxvesta28`

## 顶级公司分类

**IDX** (`/companies/top/`）：`dividend_yield`、`total_dividend`、`revenue`、`earnings`、`market_cap`、`pb`、`pe`、`ps`

**IDX 增长类** (`/companies/top-growth/`）：`top_earnings_growth_gainers`、`top_earnings_growth_losers`、`top_revenue_growth_gainers`、`top_revenue_growth_losers`

**IDX 行业变动类** (`/companies/top-changes/`）：`top_gainers`、`top_losers`

**SGX** (`/sgx/companies/top/`）：`dividend_yield`、`revenue`、`earnings`、`market_cap`、`pe`

## 错误处理

始终检查响应状态：

```python
resp = requests.get(url, headers=headers)
if resp.status_code == 403:
    raise ValueError("Invalid or missing API key. Ensure SECTORS_API_KEY is set correctly.")
if resp.status_code == 404:
    raise ValueError(f"Resource not found: {url}")
if not resp.ok:
    raise RuntimeError(f"API error {resp.status_code}: {resp.text}")
data = resp.json()
```