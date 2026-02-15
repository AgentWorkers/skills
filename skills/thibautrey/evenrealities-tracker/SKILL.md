---
name: evenrealities-tracker
description: 自动化 Evenrealities 的订单监控（包括每日检查、状态历史记录以及仅当状态发生变化时发送警报）。通过使用快速浏览器插件（fast-browser-use）填写跟踪表单，比较订单状态，并仅在状态发生变化时通过 Telegram 发送通知；同时将所有监控数据记录到 `memory/evenrealities-status-history.json` 文件中。
---

# Evenrealities订单跟踪器

## 概述

- **自动监控**：每天上午9点使用`memory/evenrealities-orders.json`文件检查每个已保存的订单。
- **仅发送状态变更通知**：仅当订单状态自上次检查后发生变化时，才会通过Telegram发送通知。
- **持续的历史记录**：每个订单都会保留最新的状态和时间戳，以便您能够发现任何问题。
- **可脚本化的命令行界面（CLI）**：`python3 scripts/tracker.py [--check|--config|--history]`命令可用于按需运行跟踪器或查看配置/历史记录。
- **支持多批次发货**：一个订单可能包含多个批次货物（例如，智能戒指可能附带可选的尺寸适配套装）。

该脚本会定期查询`https://track.evenrealities.com`网站，重新计算每个订单的状态，并且只有在状态发生变化时才会发出通知。

## 先决条件与安装

**系统要求：**
- Python 3.7及以上版本
- 约300-500MB的磁盘空间（用于存储Playwright浏览器二进制文件）
- 可访问互联网（以便连接到`track.evenrealities.com`）

**安装依赖项：**

```bash
# Install Python packages
pip install -r skills/evenrealities-tracker/requirements.txt

# Install Playwright browsers (one-time, required for browser automation)
playwright install
```

**安全注意事项：**
- Playwright会下载Chromium浏览器二进制文件（约300-500MB）
- 请查阅Playwright的安装文档：https://playwright.dev/python/docs/intro
- 脚本中不包含任何敏感信息——它仅访问公开的跟踪页面
- Telegram通知通过OpenClaw的定时任务机制发送（不在脚本中实现）
- 所有敏感文件（历史记录、配置信息）都存储在`memory/`目录下

## 了解Evenrealities智能戒指订单

Evenrealities生产不同尺寸的智能戒指。客户在下单时可以选择申请**尺寸适配套装**——这是一套包含所有尺寸的样品，用于试戴以找到合适的尺寸。

### 订单流程

1. **订单1：尺寸适配套装（可选）**
   - 客户收到所有可用尺寸的戒指
   - 该订单的状态与主订单分开跟踪
   - 通常会先发货

2. **订单2：最终戒指（尺寸确认后）**
   - 客户确定合适的尺寸后，返回Evenrealities网站
   - 在订单跟踪页面上指定正确的尺寸
   - 最终戒指会根据客户选择的尺寸单独发货
   - 通常在尺寸适配套装返回/处理完成后发货

### 这对订单跟踪的影响

- **单批次发货订单**：只需跟踪一个状态（未申请尺寸适配套装）
  - 例如：直接购买已知尺寸的戒指 → 状态显示为“已发货”

- **多批次发货订单**：有两个独立的发货状态
  - 尺寸适配套装的发货状态：`处理中` → `已发货`
  - 最终戒指的发货状态：`待确认尺寸` → `处理中` → `已发货`

### 重要提示

如果订单被分批发货，跟踪器会显示**合并后的订单状态**：
- 第一批次发货的状态（尺寸适配套装或直接购买的戒指）
  - 例如：状态可能显示为“已发货（尺寸适配套装已收到，等待最终戒指）”

为了全面了解订单的完成情况，请同时关注这两个状态。

## 快速入门

### 1. 设置订单配置

复制示例文件并添加您的订单信息：

```bash
cp skills/evenrealities-tracker/references/evenrealities-orders-example.json \
   memory/evenrealities-orders.json
```

编辑`memory/evenrealities-orders.json`文件：

```json
{
  "orders": [
    {
      "email": "your-email@example.com",
      "order_id": "ORD-123456"
    },
    {
      "email": "another-email@example.com",
      "order_id": "ORD-789012"
    }
  ]
}
```

### 2. 创建每日定时任务

```bash
clawdbot cron add \
  --name "Evenrealities order check" \
  --schedule "0 9 * * *" \
  --task "python3 /Users/thibautrey/clawd/skills/evenrealities-tracker/scripts/tracker.py --check"
```

这样就完成了！定时任务每天上午9点会自动运行。

## 工作原理

**每日流程（上午9点）：**

1. 脚本从`memory/evenrealities-orders.json`文件中加载订单信息。
2. 对每个订单，使用浏览器自动化工具执行以下操作：
   - 访问`https://track.evenrealities.com`
   - 输入电子邮件地址和订单编号
   - 点击确认按钮
   - 提取订单状态信息
3. 将当前状态与历史记录进行比较
4. **如果状态发生变化**：发送Telegram通知
5. **如果状态未变**：不发送通知
6. 更新`memory/evenrealities-status-history.json`文件

## 命令

### 立即检查所有订单

```bash
python3 scripts/tracker.py --check
```

**输出示例：**
```
🔍 Checking 2 order(s)...
============================================================

📦 Checking: user@example.com / Order #ORD-123456
   Status: SHIPPED
   (No change)

📦 Checking: other@example.com / Order #ORD-789012
   Status: PROCESSING
   ✨ CHANGED: PENDING → PROCESSING

✨ 1 change(s) detected!
   📦 ORD-789012: PENDING → PROCESSING
```

### 查看配置信息

```bash
python3 scripts/tracker.py --config
```

### 查看订单状态历史

```bash
python3 scripts/tracker.py --history
```

## 配置文件

### `memory/evenrealities-orders.json`

文件位置：`memory/evenrealities-orders.json`

**字段说明：**
- `email`：用于跟踪的电子邮件地址
- `order_id`：订单编号（格式：ORD-XXXXXX或类似格式）

根据需要添加更多订单信息。

### `memory/evenrealities-status-history.json`

文件位置：`memory/evenrealities-status-history.json`（自动生成）

**说明：**该文件会在每次脚本运行时自动更新。

## 通知机制

### 何时会收到通知

✨ **订单状态发生变化** → 会通过Telegram发送通知

**通知示例：**
```
📦 Order Update!

Order: ORD-789012
Email: user@example.com
Previous: PENDING
New: PROCESSING
Time: 2026-02-02 09:00 AM
```

### 何时不会收到通知

✓ 状态未变
✓ 这是首次检查（没有之前的状态可供比较）
✓ 未配置任何订单

## 浏览器自动化（使用Playwright）

该工具使用**Playwright**库进行浏览器自动化操作（而非`fast-browser-use`）：

1. 访问`https://track.evenrealities.com`
2. 输入电子邮件地址（使用前会进行验证）
3. 输入订单编号（使用前会进行验证）
4. 点击确认按钮
5. 等待1-2秒以获取页面响应
6. 从页面中提取订单状态信息
7. 优雅地关闭浏览器

**为什么选择Playwright？**
- 专为无头浏览器控制设计的成熟库
- 不需要额外的依赖项
- 可直接访问页面内容并精确控制操作时机

**安全性：**
- 在发送到浏览器之前，电子邮件地址和订单编号会经过验证
- 不会向浏览器传递任何敏感信息
- 浏览器会话是临时创建的（每次检查后都会销毁）

## 工作流程

**设置步骤（一次性）：**
1. 复制示例订单文件
2. 根据实际情况修改订单信息
3. 创建定时任务

**日常操作（自动执行）：**
1. 每天上午9点：定时任务启动
2. 脚本检查所有订单
3. 将当前状态与昨日的状态进行比较
4. 如果状态发生变化：发送通知
5. 更新历史记录

## 故障排除

### “未配置任何订单”

确保`memory/evenrealities-orders.json`文件中至少包含一个订单。

### “无法获取订单状态”

- 确保`https://track.evenrealities.com`网站可访问
- 验证输入的电子邮件地址和订单编号是否正确
- 如果网站布局发生变化，可能需要调整浏览器自动化脚本

### “未收到通知”

- 首次运行时：由于没有历史记录，因此不会发送通知
- 之后的运行中：只有在状态发生变化时才会发送通知
- 可使用`--history`命令查看历史记录

### 更改定时任务时间

修改定时任务的执行时间。例如，将时间改为上午8点：

```bash
clawdbot cron remove <job-id>
clawdbot cron add \
  --name "Evenrealities order check" \
  --schedule "0 8 * * *" \
  --task "python3 /Users/thibautrey/clawd/skills/evenrealities-tracker/scripts/tracker.py --check"
```

## 参考资料

- Evenrealities订单跟踪页面：https://track.evenrealities.com
- 关于`fast-browser-use`的文档：浏览器自动化相关资料
- 关于Cron任务的设置文档：Clawdbot的相关文档