---
name: shipstation-orders
description: 监控 ShipStation 的订单状态，及时发现潜在问题，并发送警报。适用于那些使用 ShipStation 在多个平台（如 Amazon、Etsy、Shopify、TikTok 等）上处理订单的电子商务企业。
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
# ShipStation 订单监控工具

该工具用于实时监控 ShipStation 平台上的新订单和异常情况，非常适合使用 ShipStation 从多个市场聚合订单的电子商务企业。

## 主要功能

- ✅ 新订单通知
- ⚠️ 通知处理时间超过 48 小时的订单
- 🛑 标记待处理的订单
- 🚚 对于加急订单、需在 2 天内发货的订单或优先级订单立即发送警报
- 📊 每日汇总报告
- 🔄 自动跟踪订单状态（避免重复警报）

## 系统要求

- 拥有可访问 ShipStation API 的账户
- Node.js（OpenClaw 已包含）

## 设置步骤

### 1. 获取 ShipStation API 密钥

1. 登录 ShipStation
2. 进入 **设置** → **账户** → **API 设置**
3. 选择 **Legacy API (V1)**，生成 API 密钥和 API 密码

### 2. 配置 API 密钥

在工作区创建一个 `.env` 文件：

```bash
SHIPSTATION_API_KEY=your_api_key_here
SHIPSTATION_API_SECRET=your_api_secret_here
```

### 3. 测试监控工具

```bash
node check-orders.js
```

测试结果将显示：
- 过去 24 小时的总订单数
- 新检测到的订单
- 任何警报信息

退出代码：
- `0`：成功，无警报
- `1`：成功，发现警报
- `2`：错误（API 请求失败，凭证无效）

### 4. 设置心跳检测（可选）

在您的代理程序的 `HEARTBEAT.md` 文件中添加相关配置：

```markdown
## Check Orders

Every 15 minutes:

1. Run: `node check-orders.js`
2. Parse results
3. If new orders or alerts → notify via sessions_send
4. If nothing → HEARTBEAT_OK
```

或者使用 cron 作业进行定期检查。

## 使用方法

### 手动检查

```bash
node check-orders.js
```

### 在代理程序的心跳检测中配置

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
- 状态为 `awaiting_shipment` 或 `awaiting_payment` 的订单

**标记为问题的订单：**
- 等待发货时间超过 48 小时的订单
- 被暂缓处理的订单（如支付验证问题、地址问题等）

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

`state.json` 文件会自动保留最近 1000 条订单记录。

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

该工具基于 [ShipStation API V1](https://www.shipstation.com/docs/api/) 进行开发。

**请求频率限制：**
- 每分钟 40 次请求
- 该脚本每次检查仅发送 1 次请求

**使用的 API 端点：**
- `GET /orders?modifyDateStart={date}&pageSize=100`

## 故障排除

**错误：“API 密钥未配置”**
- 确保 `.env` 文件存在于同一目录下
- 验证凭证内容是否正确

**错误：“ShipStation API 错误：401”**
- 请检查凭证是否正确
- 在 ShipStation 重新生成 API 密钥

**错误：“ShipStation API 错误：429”**
- 请求频率超过限制，请降低检查频率

**未检测到新订单但实际上存在：**
- 检查 `modifyDateStart` 的时间窗口（默认为 24 小时）
- 验证这些订单是否在 ShipStation 中最近被更新过
- 查看 `state.json` 文件，确认订单是否已被处理

## 文件结构

- `check-orders.js`：主要订单监控脚本
- `check-shipping.js`：加急发货警报监控脚本
- `state.json`：自动生成的订单状态跟踪文件
- `shipping-state.json`：自动生成的发货状态跟踪文件
- `.env`：您的 API 密钥（请将其添加到 `.gitignore` 文件中）

## 许可证

MIT 许可证

## 开发者

该工具专为 [OpenClaw](https://openclaw.ai) 的多代理系统开发。