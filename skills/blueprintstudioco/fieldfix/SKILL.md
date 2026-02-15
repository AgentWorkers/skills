---
name: fieldfix
description: 通过 FieldFix 的 API 查询和管理您的重型设备车队。您可以追踪设备信息、记录维护记录、监控开支，并获取人工智能诊断结果。
version: 1.0.0
author: FieldFix <support@fieldfix.ai>
homepage: https://www.fieldfix.ai/api
---

# FieldFix 技能

通过 FieldFix 的代理 API 查询和管理您的重型设备车队。

## 设置

1. 从 [FieldFix 设置](https://app.fieldfix.ai/settings/api) 获取您的 API 密钥。
2. 设置环境变量：  
   ```bash
   export FIELDFIX_API_KEY=ff_sk_live_your_key_here
   ```

## 价格

所有付费计划均包含 API 访问权限：
- **每台机器每月 $10**（1-25 台机器）
- **每台机器每月 $7**（26-100 台机器）
- **每台机器每月 $5**（100 台以上机器）
- **2 个月免费试用** — 无需信用卡

## 功能

### 读取操作

**列出所有机器：**
```bash
node scripts/fieldfix.js machines
```

**获取机器详情：**
```bash
node scripts/fieldfix.js machine <id>
```

**获取机器费用：**
```bash
node scripts/fieldfix.js expenses <id>
```

**获取服务历史：**
```bash
node scripts/fieldfix.js service <id>
```

**获取车队警报：**
```bash
node scripts/fieldfix.js alerts
```

### 写入操作

**记录服务条目：**
```bash
node scripts/fieldfix.js log-service <id> "Oil Change" 120 "Changed oil and filter"
```

**记录费用：**
```bash
node scripts/fieldfix.js log-expense <id> fuel 250 "Filled tank"
```

**更新小时计：**
```bash
node scripts/fieldfix.js update-hours <id> 1250
```

## 示例提示

配置完成后，您可以尝试向代理询问以下问题：

- “我在 FieldFix 中有多少台机器？”
- “我的 CAT 299 机器什么时候需要维护？”
- “我这个月在燃料上花了多少钱？”
- “为挖掘机记录一次价值 $120 的换油操作。”
- “我的滑移转向车的每小时总成本是多少？”

## API 端点

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/machines` | GET | 列出所有机器 |
| `/machines/{id}` | GET | 获取机器详情 |
| `/machines/{id}/expenses` | GET | 获取费用历史 |
| `/machines/{id}/service` | GET | 获取服务历史 |
| `/alerts` | GET | 获取车队警报 |
| `/machines/{id}/service` | POST | 记录服务条目 |
| `/machines/{id}/expenses` | POST | 记录费用 |
| `/machines/{id}/hours` | POST | 更新机器使用小时数 |

## 链接

- [FieldFix 应用程序](https://app.fieldfix.ai)
- [API 文档](https://www.fieldfix.ai/api)
- [MCP 服务器（Claude Desktop）](https://www.npmjs.com/package/fieldfix-mcp-server)