---
name: kubera
description: **阅读和管理 Kubera.com 的投资组合数据（净资产、资产、负债、资产配置、持有资产）**  
当用户询问自己的财务状况、净资产、投资组合、投资情况、资产配置，或希望更新 Kubera 中的资产价值时，可以使用此功能。该功能适用于任何能够运行 Python 脚本的 AI 代理或命令行界面（CLI）。
---

# Kubera

您可以通过 [Kubera API](https://www.kubera.com) 查询和更新投资组合数据。

## 设置

设置环境变量：
```bash
export KUBERA_API_KEY="your-api-key"
export KUBERA_SECRET="your-api-secret"
```

在 **Kubera 设置 > API** 中生成密钥。除非需要更新数据，否则建议使用只读权限。

## 使用方法

运行 `scripts/kubera.py` 并指定相应的子命令：

```bash
# List portfolios
python3 scripts/kubera.py portfolios

# Net worth summary with allocation + top holdings
python3 scripts/kubera.py summary

# Full portfolio JSON (for detailed analysis)
python3 scripts/kubera.py json

# List assets, optionally filter by sheet or sort
python3 scripts/kubera.py assets --sheet Crypto --sort value

# Search assets by name/ticker/account
python3 scripts/kubera.py search "shopify"

# Update an asset (requires write permission + --confirm flag)
python3 scripts/kubera.py update <ITEM_ID> --value 5000 --confirm
```

对于 `summary`、`assets`、`search` 或 `portfolios` 操作，使用 `--json` 选项可获取机器可读的输出格式；若需要获取完整的原始 API 响应，请使用 `json` 选项。

对于多投资组合账户，请使用 `--portfolio <ID>` 参数进行指定；单投资组合账户将自动被识别。

## 速率限制

- 每分钟 30 次请求，每天 100 次请求（基础账户）；每天 1,000 次请求（高级账户）
- 在同一会话中多次执行查询时，会缓存 `json` 格式的输出结果。

## API 详情

有关认证、端点和对象模式的详细信息，请参阅 [references/api.md](references/api.md)。