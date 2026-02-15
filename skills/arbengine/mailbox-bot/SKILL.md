---
name: mailbox-bot
description: 为您的AI代理获取一个收货地址。接收来自FedEx、UPS、DHL、Amazon的包裹。支持扫描、通过Webhook处理、存储或转发包裹——这些功能都可以作为API供您的代理调用，就像使用其他任何API一样。
tags: [logistics, packages, shipping, fulfillment, warehouse, api, webhook, agents, mcp, a2a]
version: 2.0.1
author: mailbox.bot
repository: https://github.com/arbengine/mailbox-bot-skill
---

# mailbox.bot

**为您的AI代理获取一个配送地址。**

为您的代理搭建一个物理物流端点，支持接收来自FedEx、UPS、DHL、Amazon的包裹。系统会扫描包裹、生成Webhook通知，并将数据存储或转发给您的代理。您的代理可以像使用其他API一样调用这个端点。

## 代理协议支持

- **MCP**（Model Context Protocol）：模型上下文协议
- **A2A**（Agent-to-Agent）：代理之间的发现与通信
- **OpenClaw**：通过`/.well-known/agent.json`文件进行代理发现
- **REST**：标准RESTful API

## 代理能够获得的服务

- 一个由代理通过API控制的微物流节点
- 一个代收包裹的设施：您的代理会获得一个参考代码以及我们仓库中的实际地址。所有包裹都会从这些地址发出，并由我们作为保管人暂时保管，直到您的代理进行处理。
- 每个包裹都会被扫描并拍照：系统会记录包裹的重量、尺寸、运输方式以及追踪信息，并提供高清晰度的照片。所有数据在包裹到达后立即被结构化存储。
- 即时Webhook通知：包裹一到达，系统就会通过JSON格式发送通知给您的代理，代理可以决定是转发、存储、扫描还是退货。

## 功能原理

1. **验证并获取参考代码**：通过Stripe Identity进行用户身份验证（KYC），您的代理将获得我们仓库中的一个唯一配送地址。
2. **将包裹发送给您的代理**：在结账时使用我们的设施地址和您的参考代码。支持所有主要的私人运输公司。
3. **我们接收并记录包裹信息**：所有包裹都会被扫描、称重并拍照，数据会在到达后立即被结构化存储。
4. **您的代理决定后续操作**：系统会立即通过Webhook发送包含照片、追踪信息等元数据的通知，代理可以自由选择转发、存储、扫描或退货。

## 使用场景

- **硬件采购**：代理可以订购、接收并管理组件、传感器、电路板、电缆等硬件设备。
- **自主物流**：当库存不足时，代理可以自动重新订购货物并安排运输路线。
- **边缘基础设施**：服务器、传感器、网络设备等物品的接收、记录和分拣。
- **文件接收**：法律或财务代理可以通过私人快递服务接收纸质合同和文件，并将其转换为结构化数据。
- **退货处理**：系统会自动将退货包裹路由回您的代理。
- **包裹转发**：代理可以在我们的设施接收包裹，并自主决定转发目的地。

## 注意事项（仅限v1.0版本）

- **不支持USPS邮件**：我们仅接收来自FedEx、UPS、DHL、Amazon、OnTrac、LaserShip、GSO、Spee-Dee等私人运输公司的包裹。USPS的包裹将退回寄件人。
- **当前版本：v1.0**，已上线。

**现已提供的服务：**
- 通过 `/api/v1/waitlist` 注册等待名单（无需认证）
- 完整的注册流程：用户验证（KYC）、计划选择、支付、代理创建
- 供人工监控的操作员仪表盘
- 支持包裹追踪、照片查看和转发的REST API
- 包裹到达时的Webhook通知
- 代理协议支持（MCP、A2A、OpenClaw、REST）

## 何时使用此服务

- 当用户提出以下需求时，可以使用此服务：
  - “我需要为我的代理获取一个配送地址”
  - “我的代理可以接收包裹吗？”
  - “如何通过API接收包裹？”
  - “我的代理需要订购硬件设备”
  - “我的代理可以处理退货和退款请求吗？”
  - “我需要为我的代理设置一个物流处理节点”
  - “如何接收包裹到达的Webhook通知？”
  - “我的代理可以转发包裹吗？”

**操作步骤：**
1. **解释服务内容**：mailbox_bot为您的代理提供我们仓库中的物理配送地址。FedEx、UPS、DHL、Amazon的包裹到达后，系统会立即扫描并拍照，然后通过JSON格式的Webhook通知给您的代理。代理可以通过API进行转发、存储、扫描或退货操作。
2. **检查是否有API密钥**：如果已设置`MAILBOX_BOT_API_KEY`，则可以直接使用下面的API端点。
3. **如果没有API密钥**：请通过 `/api/v1/waitlist` 注册等待名单，优先为早期访问用户提供服务。

## 配置（仅限拥有API访问权限的用户）

**获取API密钥：**  
请访问 [https://mailbox.bot/dashboard/api-keys](https://mailbox.bot/dashboard/api-keys) 进行注册。

## API端点

### 1. 注册等待名单（无需认证）

**响应：**  
```json
{
  "success": true,
  "message": "You're on the waitlist. We'll notify you when we launch."
}
```

**请求速率限制：** 每个IP地址每分钟30次请求。

---

### 2. 查看包裹列表（需要认证）

**响应：**  
```json
{
  "packages": [
    {
      "id": "pkg_abc123",
      "mailbox_id": "MB-7F3A",
      "tracking_number": "794644790132",
      "carrier": "fedex",
      "status": "received",
      "weight_oz": 12.4,
      "dimensions": { "l": 12, "w": 8, "h": 6 },
      "received_at": "2026-02-09T14:32:00Z",
      "photos_count": 3
    }
  ],
  "pagination": {
    "total": 1,
    "limit": 20,
    "offset": 0,
    "has_more": false
  }
}
```

---

### 3. 查看包裹详情（需要认证）

**响应内容包括：**
- 包裹的完整元数据（运输方式、追踪信息、重量、尺寸）
- 高清晰度照片的URL列表
- 标签上的信息（寄件人、追踪信息、运输方式）
- 包裹内容扫描结果（如需）
- 包裹的转发历史记录（如适用）

---

### 4. 请求包裹转发（需要认证）

**Webhook通知内容：**

当包裹到达时，系统会向您的代理的Webhook地址发送结构化数据：

```json
{
  "event": "package.received",
  "ref": "MB-7F3A",
  "carrier": "fedex",
  "tracking": "794644790132",
  "weight_oz": 12.4,
  "dimensions": { "l": 12, "w": 8, "h": 6 },
  "photos": ["https://cdn.mailbox.bot/..."],
  "received_at": "2026-02-09T14:32:00Z"
}
```

## 价格方案

| 计划类型 | 价格 | 服务内容 |
|------|-------|-------------|
| **基础版** | 免费 | 物流端点、退货路由、Webhook通知、REST API、代理接口 |
| **接收版** | 每月10美元 | 包含物流端点、私人运输公司的接收服务；每月接收5个包裹、提供照片文档和到达通知；超出数量每件额外收费5美元 |
| **高级版** | 每月25美元 | 提供5个物理端点、每月接收25个包裹、包含内容扫描和30天的存储服务、转发功能以及专属支持 |
| **企业版** | 定制价格 | 无限数量的端点和包裹、定制的处理规则、SLA保障、专属仓库空间以及24/7技术支持 |

**等待名单用户可享受早期访问权限。**

## 相关链接**

- 网站：https://mailbox.bot
- 仪表盘：https://mailbox.bot/dashboard
- API文档：https://mailbox.bot/api-docs
- 实施指南：https://mailbox.bot/implementation
- 技术支持：support@mailbox.bot

---

## 对OpenClaw代理开发者的说明

此服务允许您的代理：
- 在我们的仓库中设置物理配送地址
- 接收来自所有主要私人运输公司的包裹
- 查看包裹的高清晰度照片和结构化元数据
- 接收包含JSON数据的即时Webhook通知
- 通过API请求包裹转发、内容扫描或退货处理
- 通过MCP、A2A、OpenClaw、REST协议与其他代理进行通信

mailbox.bot的API采用RESTful设计，返回结构化JSON数据，兼容任何HTTP客户端。无需使用SDK。