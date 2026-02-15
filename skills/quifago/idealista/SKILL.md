---
name: idealista
description: 通过 `idealista-cli`（OAuth2 客户端凭据）查询 Idealista API。
license: MIT
homepage: https://github.com/quifago/idealista-cli
metadata: {"clawdbot": {"emoji": "🏠", "requires": {"bins": ["python3"], "env": ["IDEALISTA_API_KEY", "IDEALISTA_API_SECRET"], "primaryEnv": "IDEALISTA_API_KEY"}, "install": [{"id": "git", "kind": "git", "label": "Install idealista-cli (git clone)", "url": "https://github.com/quifago/idealista-cli", "bins": ["python3"]}]}}
---

# idealista

本文档介绍了如何使用本地的 `idealista-cli` 工具来查询 Idealista 的 API。

## 本地项目位置

- `idealista-cli` 的源代码位于：`~/idealista-cli`

## 凭据（client_id / client_secret）

Idealista 使用 OAuth2 客户端凭证进行身份验证。

建议使用环境变量来存储这些凭证：

- `IDEALISTA_API_KEY` = `client_id`
- `IDEALISTA_API_SECRET` = `client_secret`

示例：

```bash
export IDEALISTA_API_KEY="<CLIENT_ID>"
export IDEALISTA_API_SECRET="<CLIENT_SECRET>"
```

或者通过 `idealista-cli` 自动设置这些凭证：

```bash
python3 -m idealista_cli config set \
  --api-key "<CLIENT_ID>" \
  --api-secret "<CLIENT_SECRET>"
```

配置文件路径：
- `~/.config/idealista-cli/config.json`

令牌缓存路径：
- `~/.cache/idealista-cli/token.json`

## 常用命令

- 获取令牌：
  ```bash
python3 -m idealista_cli token
python3 -m idealista_cli token --refresh
```

- 搜索房源：
  ```bash
python3 -m idealista_cli search \
  --center "39.594,-0.458" \
  --distance 5000 \
  --operation sale \
  --property-type homes \
  --all-pages \
  --format summary
```

- 计算房源统计数据：
  ```bash
python3 -m idealista_cli avg \
  --center "39.594,-0.458" \
  --distance 5000 \
  --operation sale \
  --property-type homes \
  --group-by propertyType
```

## 示例查询（自然语言）

以下是一些可以作为调用 `idealista-cli` 的代理程序的查询示例：

- “在拉科鲁尼亚（A Coruña）寻找价格低于 20 万欧元的公寓”
- “告诉我位于北纬 39°34'33.5”，西经 0°30'10.0”附近的房屋的平均价格”
- “帮我找一套位于塔皮亚-德卡萨里埃戈（Tapia de Casariego）的三居室公寓以便购买”