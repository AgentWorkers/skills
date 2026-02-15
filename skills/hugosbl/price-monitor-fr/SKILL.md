# 价格监控器

该工具用于监控电子商务网站上的商品价格，并在价格下降时发出警报。

## 使用方法

```bash
python skills/price-monitor/scripts/monitor.py <command> [options]
```

## 命令

| 命令 | 描述 |
|---|---|
| `add <url> [--name "商品名称"] [--target-price 50]` | 添加商品到监控列表 |
| `list` | 显示所有被监控的商品 |
| `check [--all] [id]` | 检查单个或所有商品的价格 |
| `remove <id>` | 从监控列表中删除商品 |
| `history <id>` | 查看商品的价格历史记录 |
| `alerts` | 查看价格下降的警报信息 |

## 全局选项

- `--json` — 以 JSON 格式输出结果（而非文本格式）

## 支持的网站

- **Amazon.fr** — 使用 `a-offscreen` 和 `data-a-color="price"` 标签 |
- **Fnac.com** — 使用 `meta tags` 和 `f-priceBox-price` 标签 |
- **Cdiscount** — 使用 `c-product__price` 和 `itemprop` 标签 |
- **Boulanger** — 使用 `class="price"` 和 `itemprop` 标签 |
- **其他网站** — 使用 `og:price` 标签（通过 JSON-LD 和 `itemprop` 提取价格信息）

## 价格提取规则（优先级顺序）

1. `<meta property="og:price:amount">`
2. JSON-LD 标签（例如：`"price":"XX.XX"`）
3. `itemprop="price"`
4. 如果以上方法不可用，使用正则表达式 `XX,XX €` 来提取价格信息

## 价格警报规则

- **价格达到目标价格**：当前价格 ≤ 目标价格 → 显示警告图标（🎯）
- **价格下降超过 5%**：显示警告信息（🔥）
- 警报格式示例：`Amazon PS5：原价 449€ → 现价 399€（降价 11%）🔥`

## 数据存储

- `~/.price-monitor/products.json`：存储所有被监控的商品列表 |
- `~/.price-monitor/history/<id>.json`：存储每个商品的价格历史记录 |
- `~/.price-monitor/alerts.json`：存储所有已记录的价格下降警报 |

## 使用示例

```bash
# Ajouter un produit
python monitor.py add "https://www.amazon.fr/dp/B0BN..." --name "PS5" --target-price 400

# Vérifier tous les prix
python monitor.py check --all

# Historique
python monitor.py history abc12345

# Alertes en JSON
python monitor.py --json alerts
```

## 技术实现

- 仅使用 Python 标准库（`urllib`, `json`, `re`）
- 使用真实的 Chrome 用户代理 |
- 每个请求的超时时间为 10 秒 |
- 如需添加更多网站的支持，请参考 `references/extractors.md` 文档。