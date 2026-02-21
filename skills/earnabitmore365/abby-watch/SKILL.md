---
name: abby-watch
description: >
  **Abby的简单时间显示功能**  
  当您需要了解当前时间或倒计时到某个特定时间时，可以使用此功能。
---
# Abby Watch

一个用于快速查看时间的简单工具。

## 使用方法

```bash
# Simple time
abby time

# Verbose (full details)
abby time --verbose

# Countdown to a time
abby time --countdown "11:00"
```

## 示例

| 查询 | 命令 | 输出 |
|-------|---------|--------|
| 现在几点了？ | `abby time` | 🕐 08:00 |
| 显示完整信息 | `abby time --verbose` | 2026年2月15日，星期日，上午8:00（澳大利亚/悉尼时区） |
| 距离11点还有多久？ | `abby time --countdown 11:00` | ⏰ 还有3小时 |

## 注意事项

- 默认显示格式为 HH:MM
- 详细信息会包含完整的日期和时区
- 计时功能支持24小时制（HH:MM）