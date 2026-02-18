# OpenClaw 状态 API

您可以将 OpenClaw 代理的状态和运行状况作为通过 x402 协议收费的 API 端点进行商业化。

## 功能

- 返回代理的状态（活动/空闲）
- 报告定时任务的运行状况
- 显示平台的运行时间
- 通过 Nominatim 对位置进行地理编码
- 通过 Open-Meteo 获取天气数据

## API 端点

| 端点 | 描述 |
|------|------|
| `/api/status` | 获取所有代理的状态和定时任务的运行状况 |
| `/api/geocode?q=City` | 根据城市名称进行地理编码（返回经纬度） |
| `/api/weather?lat=X&lon=Y` | 根据坐标获取天气信息 |

## 价格

每次请求的费用为 0.001 美元 USD，通过 x402 协议结算。

## 设置

```bash
# Deploy to Vercel
vercel deploy --prod

# Or run locally
npm install
node index.js
```

## 支付方式

支付地址：`0x483AE22AaEc52c0a1871C07E631d325bF5C8A08`

## 示例响应

```json
{
  "success": true,
  "platform": "OpenClaw Status API",
  "agents": [
    { "name": "main", "status": "active" },
    { "name": "ceo", "status": "active" }
  ],
  "cronJobs": [
    { "name": "Simmer Trading", "schedule": "15min", "status": "active" }
  ]
}
```