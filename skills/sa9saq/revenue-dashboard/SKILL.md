---
description: 实时收入与投资组合仪表板——在一个平台上追踪加密货币收益、自由职业收入和服务收入。
---

# 收入仪表盘

通过一个统一的仪表盘，您可以跟踪您的加密货币持有情况、自由职业收入以及服务收入。

## 系统要求

- Node.js 18 及以上版本
- 无需使用外部 API 密钥（使用 CoinGecko 的免费 tier 来获取加密货币价格）

## 快速入门

```bash
cd {skill_dir}
npm install
npm run build
npm start -- --port 3020    # Production
# or
npm run dev                 # Development with hot reload
```

在浏览器中打开 `http://localhost:3020`。

## API 端点

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| `GET` | `/api/portfolio` | 当前投资组合概览 |
| `GET` | `/api/revenue?from=YYYY-MM-DD&to=YYYY-MM-DD` | 按日期范围显示收入 |
| `POST` | `/api/transactions` | 添加加密货币交易记录 |
| `GET` | `/api/holdings` | 当前持有的加密货币 |
| `POST` | `/api/income` | 记录自由职业或服务收入 |

## 仪表盘界面

1. **投资组合概览** — 总价值、24 小时变化情况、资产分配饼图 |
2. **收入时间线** — 随时间变化的收入情况（折线图/条形图） |
3. **持有资产表** — 各项资产的详细表现 |
4. **收入来源** — 收入来源的详细分类（加密货币、自由职业、服务收入）

## 配置参数

| 参数 | 默认值 | 说明 |
|----------|---------|-------------|
| `PORT` | `3020` | 服务器端口 |
| `DB_PATH` | `./data/revenue.db` | SQLite 数据库路径 |
| `COINGECKO_API` | CoinGecko API 基础 URL |

## 特殊情况与故障排除

- **端口已被占用**：通过 `PORT=3021 npm start` 更改端口，或终止现有进程。
- **数据库锁定**：SQLite 不支持并发写入操作，请确保只有一个进程在运行。
- **CoinGecko 的请求限制**：免费 tier 每分钟约 30 次请求。仪表盘会缓存价格数据 60 秒。
- **数据缺失**：对于没有交易记录的日期范围，API 会返回空数组（而非错误信息）。
- **首次运行**：首次启动时，系统会自动创建数据库和表格。

## 安全性

- 仪表盘默认绑定到 `localhost`。如需公开访问，请使用反向代理（如 nginx）。
- 该系统未内置身份验证机制——在生产环境中请添加基本认证或使用 VPN。
- 请勿公开 SQLite 数据库文件。

## 技术栈

Next.js 14, shadcn/ui, Recharts, SQLite (better-sqlite3)