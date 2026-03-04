---
name: reg-limited
description: 针对中国城市的车辆限行查询与提醒工具：可查询每日限行信息，并设置定时提醒。
---
# RegLimited - 车辆限行查询与提醒工具

这是一个帮助您查询中国城市车辆限行信息并设置提醒的工具。

## 主要功能

1. **限行查询** - 根据城市和车牌号码，检查您的车辆是否在当天被限制通行。
2. **定时提醒** - 在指定时间接收限行信息的通知。
3. **支持多城市** - 支持北京、上海、广州、深圳、杭州、成都等主要中国城市。

## 使用方法

### 1. 查询当天的限行信息

```bash
# Query today's restricted digits for a city
reg-limited query --city beijing

# Check if a plate is restricted
reg-limited check --city beijing --plate 京A12345
```

### 2. 设置限行提醒

```bash
# Basic usage
reg-limited add --city beijing --plate 京A12345 --time "07:00"

# Full parameters
reg-limited add --city beijing --plate 京A12345 --time "07:00" --notify-channel feishu
```

### 3. 查看所有提醒

```bash
reg-limited list
```

### 4. 删除提醒

```bash
reg-limited remove --id <reminder_id>
```

## 支持的城市

- 北京 (北京)
- 上海 (上海)
- 广州 (广州)
- 深圳 (深圳)
- 杭州 (杭州)
- 成都 (成都)
- 天津 (天津)
- 武汉 (武汉)
- 西安 (西安)
- 南京 (南京)

## 限行规则

### 北京
- 从北京市交通管理局获取实时限行数据：
  - 官方来源：https://jtgl.beijing.gov.cn/jgj/lszt/659722/660341/index.html
  - 有效期：2025-12-29 至 2026-03-29
  - 限行时间为周一至周五，7:00-20:00

| 星期 | 被限制的数字 |
|-----|------------|
| 星期一 | 3, 8 |
| 星期二 | 4, 9 |
| 星期三 | 5, 0 |
| 星期四 | 1, 6 |
| 星期五 | 2, 7 |

### 其他城市
- **上海**：高架道路限行
- **广州**：实施“开四停四”政策
- **深圳**：早晚高峰时段限行
- **杭州/成都/天津/武汉/西安/南京**：按具体日期设置限行车牌号码

## 输出格式

以 JSON 格式提供给程序处理：

```json
{
  "success": true,
  "data": {
    "city": "北京",
    "date": "2026-03-03",
    "restricted": ["4", "9"],
    "isRestricted": true,
    "plate": "京A12345",
    "lastDigit": "4"
  }
}
```

## 示例对话

> 用户：北京今天的车辆限行情况是什么？
> 机器人：今天的限行数字是 4 和 9（您的车牌号码以 4 结尾，因此今天被限制通行！）
> 用户：我的车牌号是 京A12345，今天被限制了吗？
> 机器人：是的！今天（星期二），北京限制车牌号码 4 和 9。您的车牌号码以 4 结尾，所以被限制通行。
> 用户：设置一个明天早上 7 点的限行提醒吧。
> 机器人：已设置！明天早上 7 点您会收到限行提醒。

## 技术实现

1. 从官方政府渠道获取每日限行信息。
2. 对于北京，查询地址为：https://jtgl.beijing.gov.cn/jgj/lszt/659722/660341/index.html
3. 从官方表格中解析限行车牌号码。
4. 比较车牌号码的最后一位是否在限行范围内。
5. 通过定时任务发送提醒通知。

## 所需依赖库/工具

- Node.js
- 网络访问权限（用于查询限行信息）
- 消息发送渠道（如 Feishu、Telegram 等）

---

*更多城市即将支持……*