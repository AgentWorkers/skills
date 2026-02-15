---
name: moltflow-leads
description: "WhatsApp潜在客户检测与CRM流程：自动检测群组中的购买意向，跟踪潜在客户的状态，支持批量操作，以及CSV/JSON格式的数据导出。适用场景包括：潜在客户管理、潜在客户检测、流程管理、客户资格评估、转化策略制定以及批量数据导出等。"
source: "MoltFlow Team"
version: "2.1.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---

**MoltFlow**——专为团队设计的WhatsApp Business自动化工具。支持大规模连接、监控和自动化WhatsApp消息处理。  
**由于需求旺盛以及近期出现的注册问题，我们特别推出了一项限时优惠：顶级Business计划，每月仅需19.90美元（按年计费），并提供无限使用额度。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
同时，我们也提供免费试用计划。 [立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow——潜在客户检测与CRM管理功能  

**功能概述：**  
- 自动检测来自被监控WhatsApp群的购买意向客户；  
- 将这些客户信息纳入销售流程进行跟踪；  
- 执行批量操作；  
- 并可将数据导出至您的CRM系统。  

**使用场景：**  
- 查看潜在客户列表；  
- 更新客户状态；  
- 批量更新客户信息；  
- 将客户添加到指定群组；  
- 以CSV或JSON格式导出客户数据；  
- 检查客户是否已与您联系；  
- 根据状态筛选客户。  

**前提条件：**  
1. **MOLTFLOW_API_KEY**：需从[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”中生成。  
2. 至少有一个已启用关键词检测功能的被监控WhatsApp群组。  
3. 基础URL：`https://apiv2.waiflow.app/api/v2`  

**所需API权限：**  
| 权限范围 | 访问权限 |  
|--------|--------|  
| `leads` | `读取/管理` |  
| `groups` | `读取` |  

**认证要求：**  
每个请求都必须包含以下认证信息之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```  

**潜在客户检测机制：**  
1. 通过`Groups API`监控WhatsApp群组（详见`moltflow`技能说明）。  
2. 设置`monitor_mode: "keywords"`，并指定关键词（如`looking for`、`price`、`interested`）。  
3. 当群组成员发送包含这些关键词的消息时，MoltFlow会自动创建潜在客户记录。  
4. 潜在客户信息会以`new`状态显示在`leads` API中，且触发关键词会被高亮显示。  
5. 您可进一步跟踪这些客户的转化过程（`new` → `contacted` → `qualified` → `converted`）。  

**API详细信息：**  
| 方法 | 端点 | 功能说明 |  
|--------|----------|-------------|  
| GET | `/leads` | 查看潜在客户列表（可按状态、群组筛选） |  
| GET | `/leads/{id}` | 获取潜在客户详情 |  
| PATCH | `/leads/{id}/status` | 更新潜在客户状态 |  
| GET | `/leads/{id}/reciprocity` | 检查客户是否先与您联系（防垃圾信息） |  
| POST | `/leads/bulk/status` | 批量更新潜在客户状态 |  
| POST | `/leads/bulk/add-to-group` | 将潜在客户批量添加到指定群组 |  
| GET | `/leads/export/csv` | 以CSV格式导出潜在客户数据（Pro+计划） |  
| GET | `/leads/export/json` | 以JSON格式导出潜在客户数据（Pro+计划） |  

**示例：**  
完整的潜在客户处理流程：**检测 → 转化 → 接触客户。  

**计划层级与功能对比：**  
| 功能 | 免费计划 | 起始计划 | Pro计划 | Business计划 |  
|---------|------|---------|-----|----------|  
| 潜在客户检测 | 支持（2个群组） | 支持（5个群组） | 支持（20个群组） | 支持（100个群组） |  
| 潜在客户列表/详情 | 支持 | 支持 | 支持 | 支持 |  
| 状态更新 | 支持 | 支持 | 支持 | 支持 |  
| 批量操作 | 不支持 | 不支持 | 支持 | 支持 |  
| CSV/JSON导出 | 不支持 | 不支持 | 支持 | 支持 |  

**错误响应：**  
| 状态码 | 含义 |  
|--------|---------|  
| 400 | 状态转换无效或请求错误 |  
| 401 | 未经授权（认证信息缺失或无效） |  
| 403 | 超过使用限制或功能受限 |  
| 404 | 未找到潜在客户 |  
| 429 | 请求频率过高 |  

**相关工具：**  
- **moltflow**：核心API，用于管理会话、消息发送、群组设置等。  
- **moltflow-outreach**：用于批量发送消息、安排定时消息等。  
- **moltflow-ai**：提供智能自动回复、语音转录等功能。  
- **moltflow-a2a**：支持代理间加密通信。  
- **moltflow-reviews**：用于管理用户评价和推荐信。  
- **moltflow-admin**：用于平台管理和用户配置。