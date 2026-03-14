---
name: polymarket-market-importer
displayName: "Polymarket Market Importer"
description: 自动发现并导入符合您的关键词、标签和交易量要求的 Polymarket 市场。该功能会按照预设的时间表运行，确保您不会错过任何值得交易的新市场。只需设置一次筛选条件，其余工作都将由该工具自动完成。
version: "1.0.3"
authors:
  - name: "DjDyll"
difficulty: "beginner"
---
# 🎯 Polymarket 市场导入器

> **这是一个模板。** 关键词、类别和成交量过滤器需要您自行设置。该工具会按照您的要求定期在 Polymarket 上进行搜索，根据您的条件过滤数据，并将符合条件的市场导入到 Simmer 系统中。您负责配置搜索条件，工具会自动完成后续的工作。

## 设置

1. **安装 SDK：**
   ```bash
   pip install simmer-sdk
   ```

2. **设置 API 密钥：**
   ```bash
   export SIMMER_API_KEY="sk_live_..."
   ```

3. **设置过滤器：**
   ```bash
   python market_importer.py --set keywords=bitcoin,ethereum,solana
   python market_importer.py --set min_volume=25000
   ```

4. **进行试运行以验证配置：**
   ```bash
   python market_importer.py
   ```

5. **正式启用：**
   ```bash
   python market_importer.py --live
   ```

## 配置参数

| 参数          | 环境变量          | 默认值       | 说明                                      |
|--------------|-----------------|------------|-----------------------------------------|
| `keywords`      | `IMPORTER_KEYWORDS`     | `bitcoin,ethereum` | 用逗号分隔的搜索关键词                   |
| `min_volume`     | `IMPORTER_MIN_VOLUME`    | `10000`      | 每 24 小时的最低成交量要求（用于过滤成交量过低的市场）          |
| `max_per_run`    | `IMPORTER_MAX_PER_RUN`    | `5`        | 每次运行的最大导入数量上限                          |
| `categories`     | `IMPORTER_CATEGORIES`    | `crypto`      | 用逗号分隔的类别过滤器（如：crypto、politics、sports 等）     |

## 快速操作命令

```bash
# Dry run — preview what would be imported
python market_importer.py

# Import for real
python market_importer.py --live

# Check what you've already imported
python market_importer.py --positions

# Show current config
python market_importer.py --config

# Update a setting
python market_importer.py --set keywords=bitcoin,ethereum,xrp

# Quiet mode — only output on imports or errors
python market_importer.py --live --quiet
```

## 示例输出

```
🎯 Polymarket Market Importer
==================================================

  [LIVE MODE] Importing markets for real.

  Config: keywords=bitcoin,ethereum | min_volume=10000 | max_per_run=5 | categories=crypto

  Searching for: bitcoin
    Found 12 importable markets
    3 already imported, 9 new
    Category match: 7

  Searching for: ethereum
    Found 8 importable markets
    2 already imported, 6 new
    Category match: 5

  Importing: "Will BTC exceed $150k by July 2026?" (vol: $125,000)
    ✅ Imported successfully
  Importing: "Will ETH reach $5k by June 2026?" (vol: $89,000)
    ✅ Imported successfully

  Summary: 20 found | 5 already seen | 2 imported (max 5)
```

## 故障排除

| 故障现象        | 解决方案                                      |
|------------------|--------------------------------------------|
| “未找到可导入的市场”    | 扩大搜索关键词范围或降低 `min_volume` 的值                |
| “导入失败”       | 可能已达到每日导入限额（免费用户每天 10 次，高级用户每天 50 次）。请尝试再次运行。 |
| “SIMMER_API_KEY 未设置” | 请从 simmer.markets/dashboard 的 SDK 标签页获取 API 密钥        |
| 市场与类别不匹配    | 确保使用的关键词和标签与实际市场类别一致。可以尝试更换关键词或标签    |

## 定时任务

该工具通过 cron 任务每 6 小时运行一次（`0 */6 * * *`）。如有需要，可在 `clawhub.json` 文件中调整运行频率。