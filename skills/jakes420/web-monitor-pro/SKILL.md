---
name: web-monitor
description: "监控网页上的变化，如价格下降、库存情况以及自定义条件。适用于用户要求监控某个URL、接收价格变动通知、检查商品是否重新上市，或跟踪网站更新的情况。同时支持添加、删除和查看现有的监控任务。"
metadata:
  {
    "openclaw":
      {
        "emoji": "👁️",
        "requires": { "bins": ["python3", "curl"] },
      },
  }
---

# 网页监控器

实时跟踪任何网页上的变化。当价格下降、库存状态变化、内容更新或满足自定义条件时，系统会发送警报。

## 设置

无需API密钥。使用`curl`来获取数据，并将结果存储在`~/.web-monitor/`目录下。

## 核心脚本

所有操作都通过`scripts/monitor.py`脚本完成：

```bash
python3 scripts/monitor.py <command> [args]
```

## 命令

### 添加监控项

```bash
python3 scripts/monitor.py add "https://example.com/product" \
  --label "Product Name" \
  --condition "price below 500" \
  --interval 360
```

选项：
- `--label/-l` — 为用户友好的名称
- `--selector/-s` — 类似CSS的选择器，用于精确匹配目标内容（例如`#price`或`.stock-status`）
- `--condition/-c` — 警报条件（详见下文）
- `--interval/-i` — 检查间隔（单位：分钟，默认值：360）

### 检查监控项

```bash
python3 scripts/monitor.py check              # Check all
python3 scripts/monitor.py check --id <id>     # Check one
python3 scripts/monitor.py check --verbose     # Include content preview
```

返回包含`status`（变化/未变化）、`condition_met`（条件是否满足）和`diff`（变化摘要）的JSON信息。

### 列出所有监控项

```bash
python3 scripts/monitor.py list
```

### 删除监控项

```bash
python3 scripts/monitor.py remove <id>
```

### 查看历史记录

```bash
python3 scripts/monitor.py history <id> --limit 5
```

## 条件语法

- `price below 500` 或 `price < 500` — 价格阈值（支持使用R、$等符号）
- `price above 1000` 或 `price > 1000`
- `contains 'in stock'` — 检查文本中是否包含“有库存”字样
- `not contains 'out of stock'` — 检查文本中是否包含“缺货”字样

## 使用Cron任务自动化监控

可以设置Cron任务来定期检查监控项并向用户发送警报：

```
Task: Check all web monitors. Run: python3 <skill_dir>/scripts/monitor.py check
Report any monitors where status is "changed" or "condition_met" is true.
If nothing changed, say so briefly or stay silent.
```

推荐的时间表：每6小时执行一次（`0 */6 * * *`）。

## 提示

- 对于包含大量JavaScript的网站（如Takealot、Amazon），建议使用`web_fetch`工具获取渲染后的页面内容，然后再进行手动对比。
- 该脚本为每个监控项最多保存20个历史快照。
- 为节省存储空间，每个快照的大小限制为10KB。
- 使用`--selector`来精确匹配目标元素，以减少无关内容（如时间戳、广告等）对监控结果的影响。
- 当用户要求“关注这个页面”或“在……时提醒我”时，可以创建相应的监控项并设置Cron任务。