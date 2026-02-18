---
name: moltflow-leads
description: "WhatsApp潜在客户检测与CRM流程：在群组中识别购买意向信号，跟踪潜在客户的状态，支持批量操作，并提供CSV/JSON格式的数据导出功能。适用场景包括：潜在客户管理、潜在客户检测、流程优化、客户资格评估、转化策略制定以及批量数据导出等。"
source: "MoltFlow Team"
version: "2.11.8"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
> **MoltFlow**——专为团队设计的WhatsApp Business自动化工具。支持大规模连接、监控和自动化WhatsApp消息处理。  
> **由于需求旺盛以及近期注册问题，我们特推出高级商务套餐：每月仅需19.90美元（按年计费），且配无限使用额度——限时优惠！** [**立即抢购**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
> 免费试用套餐也可使用。[**立即注册**](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow——潜在客户检测与客户关系管理（CRM）功能  

该工具可检测来自被监控WhatsApp群组的购买意向信号，追踪潜在客户线索，并将其导入您的CRM系统。  

## 使用场景  
- 查看潜在客户列表  
- 更新潜在客户状态  
- 批量更新潜在客户信息  
- 将潜在客户添加到特定群组  
- 以CSV或JSON格式导出潜在客户数据  
- 检查潜在客户是否已与您联系  
- 按状态筛选潜在客户  

## 前提条件  
1. **MOLTFLOW_API_KEY**：需从[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”中生成。  
2. 至少拥有一个已启用关键词检测功能的被监控WhatsApp群组。  
3. 基础URL：`https://apiv2.waiflow.app/api/v2`  

## 所需API密钥权限  
| 权限范围 | 访问权限 |  
|---------|---------|  
| `leads` | `读取/管理` |  
| `groups` | `读取` |  

## 认证要求  
每个请求必须包含以下认证信息之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```  

---

## 潜在客户检测机制  
1. 通过“Groups API”配置群组监控（详见`moltflow`技能文档）。  
2. 设置`monitor_mode: "keywords"`，并指定关键词（如`"looking for"`、`"price"`、`"interested"`）。  
3. 当检测到关键词匹配时，MoltFlow会自动创建潜在客户记录。  
4. 潜在客户记录会以`new`状态显示，并标出触发该状态的关键词。  
5. 您可跟踪这些潜在客户的转化过程：`new` -> `contacted` -> `qualified` -> `converted`。  

---

## 相关API接口  
| 方法 | 接口地址 | 功能说明 |  
|--------|----------|-------------|  
| GET | `/leads` | 查看潜在客户列表（可按状态、群组筛选） |  
| GET | `/leads/{id}` | 获取潜在客户详细信息 |  
| PATCH | `/leads/{id}/status` | 更新潜在客户状态 |  
| GET | `/leads/{id}/reciprocity` | 检查潜在客户是否先与您联系（防垃圾信息） |  
| POST | `/leads/bulk/status` | 批量更新潜在客户状态 |  
| POST | `/leads/bulk/add-to-group` | 将潜在客户批量添加到指定群组 |  
| GET | `/leads/export/csv` | 以CSV格式导出潜在客户数据（Pro+套餐） |  
| GET | `/leads/export/json` | 以JSON格式导出潜在客户数据（Pro+套餐） |  

### 查看潜在客户列表  
**GET** `/leads`  
查询参数：  
| `status` | 字符串 | 按状态筛选（`new`、`contacted`、`qualified`、`converted`、`lost`）  
| `source_group_id` | UUID | 按来源群组筛选  
| `search` | 字符串 | 按联系人姓名、电话号码或关键词搜索  
| `limit` | 整数 | 每页显示数量（默认50条）  
| `offset` | 整数 | 分页偏移量  

**响应格式**：`200 OK`  

---

### 获取潜在客户详细信息  
**GET** `/leads/{id}`  
返回潜在客户的完整信息，包括所属群组、检测详情、消息记录及状态。  

### 更新潜在客户状态  
**PATCH** `/leads/{id}/status`  

**状态转换规则**：  
- `new` -> `contacted`、`qualified`、`converted`、`lost`  
- `contacted` -> `qualified`、`converted`、`lost`  
- `qualified` -> `converted`、`lost`  
- `converted` -> （最终状态，无法再转换）  
- `lost` -> `new`（仅可重新开始检测）  
无效的状态转换会导致`400 Bad Request`错误。  

### 检查潜在客户是否先与您联系  
**GET** `/leads/{id}/reciprocity?session_id-session-uuid`  
`session_id`参数是必需的，用于指定检查哪些WhatsApp会话中的消息。  

---

**使用提示**：  
若潜在客户未主动联系您，直接发送消息可能会触发WhatsApp的垃圾信息检测机制。  

### 批量更新潜在客户状态  
**POST** `/leads/bulk/status`  

**响应格式**：`200 OK`  

---

**注意事项**：  
每个潜在客户的状态转换都会经过系统验证。状态转换无效的记录会被标记在错误日志中，但不会影响其他记录的处理。  

### 将潜在客户批量添加到群组  
**POST** `/leads/bulk/add-to-group`  
**用途**：将潜在客户的电话号码添加到指定群组，以便后续发送批量消息或定时消息。  

### 导出潜在客户数据  
**GET** `/leads/export/csv`（CSV格式）  
**GET** `/leads/export/json`（JSON格式）  
支持按`status`、`source_group_id`、`search`参数进行筛选。每次导出最多10,000条记录。  
（仅限Pro+套餐使用。）  

---

## 功能对比（免费/高级/商务套餐）  
| 功能 | 免费套餐 | 起始套餐 | Pro套餐 | 商务套餐 |  
|---------|---------|---------|---------|---------|  
| 潜在客户检测 | 支持（2个群组） | 支持（5个群组） | 支持（20个群组） | 支持（100个群组） |  
| 潜在客户列表及详情 | 支持 | 支持 | 支持 | 支持 | 支持 |  
| 状态更新 | 支持 | 支持 | 支持 | 支持 |  
| 批量操作 | 不支持 | 不支持 | 支持 | 支持 |  
| CSV/JSON导出 | 不支持 | 不支持 | 支持 | 支持 |  

---

## 错误代码说明  
| 状态码 | 含义 |  
|--------|---------|  
| 400 | 状态转换无效或请求错误 |  
| 401 | 未经授权（认证信息缺失或无效） |  
| 403 | 超出套餐使用限制或功能限制 |  
| 404 | 未找到潜在客户 |  
| 429 | 请求频率受限 |  

---

**相关工具**  
- **moltflow**：核心API，用于管理会话、消息发送、群组及标签设置。  
- **moltflow-outreach**：用于批量发送消息、定时发送消息及管理自定义群组。  
- **moltflow-ai**：提供人工智能驱动的自动回复、语音转录等功能。  
- **moltflow-a2a**：支持代理间安全通信及内容策略管理。  
- **moltflow-reviews**：用于收集用户评价和管理推荐信。  
- **moltflow-admin**：平台管理工具，包括用户管理和套餐配置。