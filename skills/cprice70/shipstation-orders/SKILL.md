---
name: shipstation-orders
description: 监控 ShipStation 的订单状态，发现潜在问题，并发送警报。适用于那些通过 ShipStation 在多个平台（如 Amazon、Etsy、Shopify、TikTok 等）处理订单的电子商务企业。
metadata:
  {
    "openclaw": {
      "requires": { 
        "bins": ["node"],
        "env": ["SHIPSTATION_API_KEY", "SHIPSTATION_API_SECRET"]
      }
    }
  }
---
# ShipStation 订单监控器

实时监控 ShipStation 的新订单和异常情况，非常适合使用 ShipStation 从多个市场平台聚合订单的电子商务企业。

## 主要功能

- ✅ 新订单通知
- ⚠️ 处理时间超过 48 小时的订单警报
- 🛑 标记待处理的订单
- 📊 每日汇总报告
- 🔄 自动状态跟踪（避免重复警报）

## 系统要求

- 拥有可访问 API 的 ShipStation 账户
- Node.js（OpenClaw 已包含）

## 设置步骤

### 1. 获取 ShipStation API 凭据

1. 登录 ShipStation
2. 进入 **设置** → **账户** → **API 设置**
3. 选择 **Legacy API (V1)**，生成 API 密钥和 API 密码

### 2. 配置凭据

在工作区创建一个 `.env` 文件：

```bash
SHIPSTATION_API_KEY=your_api_key_here
SHIPSTATION_API_SECRET=your_api_secret_here
```

### 3. 测试监控器

```bash
node check-orders.js
```

测试结果会显示：
- 过去 24 小时的总订单数
- 新检测到的订单
- 任何警报信息

退出代码：
- `0` - 成功，无警报
- `1` - 成功，发现警报
- `2` - 错误（API 请求失败，凭据错误）

### 4. 设置心跳监控（可选）

将以下代码添加到您的代理的 `HEARTBEAT.md` 文件中：

```markdown
## Check Orders

Every 15 minutes:

1. Run: `node check-orders.js`
2. Parse results
3. If new orders or alerts → notify via sessions_send
4. If nothing → HEARTBEAT_OK
```

或者使用 cron 作业进行定时检查。

## 使用方法

### 手动检查

```bash
node check-orders.js
```

### 在代理的心跳检查中

```javascript
const { exec } = require('child_process');

exec('node check-orders.js', (error, stdout, stderr) => {
  const results = JSON.parse(stdout);
  
  if (results.newOrdersList.length > 0) {
    // Notify about new orders
  }
  
  if (results.alerts.length > 0) {
    // Notify about issues
  }
});
```

## 警报条件

**新订单：**
- 任何处于 `awaiting_shipment` 或 `awaiting_payment` 状态的订单

**标记为问题的订单：**
- 等待发货超过 48 小时的订单
- 待处理的订单（例如：支付验证问题、地址问题等）

**API 错误：**
- 认证失败
- 超过请求频率限制
- 网络问题

## 状态管理

该脚本使用 `state.json` 文件来记录以下信息：
- 最后一次检查的时间戳
- 已处理的订单 ID（防止重复警报）
- 待处理的警报
- 库存警告（未来功能）

`state.json` 文件会自动保留最近 1000 条订单的数据。

## 自定义设置

编辑 `check-orders.js` 文件以调整以下参数：

**警报阈值：**
```javascript
// Line ~70: Change from 48 hours to 24 hours
if (order.orderStatus === 'awaiting_shipment' && ageHours > 24) {
```

**时间窗口：**
```javascript
// Line ~60: Change from 24 hours to 12 hours
const yesterday = new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString();
```

**额外检查：**
根据您的业务需求添加自定义逻辑（例如：高价值订单、特定产品等）

## API 参考

使用 [ShipStation API V1](https://www.shipstation.com/docs/api/)

**请求频率限制：**
- 每分钟 40 次请求
- 该脚本每次检查仅发送 1 次请求

**使用的 API 端点：**
- `GET /orders?modifyDateStart={date}&pageSize=100`

## 故障排除

**错误：“API 凭据未配置”**
- 确保 `.env` 文件存在于同一目录下
- 验证凭据中不含占位符文本

**错误：“ShipStation API 错误：401”**
- 凭据不正确
- 在 ShipStation 重新生成 API 密钥

**错误：“ShipStation API 错误：429”**
- 超过请求频率限制
- 减少检查频率

**未检测到新订单但实际上存在：**
- 检查 `modifyDateStart` 的时间窗口（默认为 24 小时）
- 验证这些订单是否在 ShipStation 中最近被修改过
- 查看 `state.json` 文件（可能已处理）

## 文件结构

- `check-orders.js` - 主监控脚本
- `state.json` - 自动生成的状态跟踪文件
- `.env` - 你的 API 凭据（请将其添加到 `.gitignore` 文件中！）

## 许可证

MIT

## 作者

专为 [OpenClaw](https://openclaw.ai) 多代理系统开发。