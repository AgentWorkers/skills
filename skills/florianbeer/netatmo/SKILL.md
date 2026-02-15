---
name: netatmo
description: 控制 Netatmo 温度计并读取气象站数据。可用于供暖控制（设置温度、切换模式）、查看室内/室外温度、二氧化碳浓度、湿度、噪音以及气压读数。
---

# Netatmo

通过 `netatmo` CLI 控制 Netatmo 智能家居设备。

## 设置

认证信息存储在 `~/.config/netatmo/` 目录下：
- `credentials.json`：`{"client_id": "...", "client_secret": "..."}`
- `tokens.json`：OAuth 令牌（会自动刷新）

## 命令

```bash
netatmo status              # Full overview (thermostat + all sensors)
netatmo thermostat          # Thermostat details only
netatmo weather             # All sensors including Office
netatmo history             # 7-day temperature history with sparklines
netatmo history --days 14   # Custom period
netatmo set 21              # Set target temp (7-30°C, 3h manual mode)
netatmo mode schedule       # Resume schedule
netatmo mode away           # Away mode (12°C)
netatmo mode hg             # Frost guard (7°C)
netatmo <cmd> --json        # JSON output for any command
```

## 可用数据

| 位置 | 温度 | 湿度 | 二氧化碳浓度 | 噪音 | 气压 | 电池电量 |
|----------|------|----------|-----|-------|----------|---------|
| 主卧室 | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| 户外 | ✓ | ✓ | — | — | ✓* | ✓ |
| 客厅 | ✓ | ✓ | ✓ | — | — | ✓ |
| 办公室 | ✓ | — | — | — | — | — |

*气压数据与室外位置相同（使用主站中的传感器）

## 注意事项

- 二氧化碳浓度（CO₂）>1000 ppm 表示通风不良
- `set` 命令会将设备设置为手动模式运行 3 小时，之后自动恢复到预定模式
- 令牌会在过期后自动刷新
- 历史数据以 ASCII 图表的形式显示温度变化趋势