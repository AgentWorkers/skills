---
name: moltflow-outreach
description: "批量消息发送、定时消息发送、定时报告生成以及用于 WhatsApp 客户关系管理的自定义群组功能。适用场景包括：批量发送消息、广播消息、定时发送消息、定时生成报告、使用 Cron 任务进行自动化操作、创建自定义群组、以及实现安全且不会被屏蔽的通信方式。"
source: "MoltFlow Team"
version: "2.16.1"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow**——专为团队设计的WhatsApp Business自动化工具。支持大规模连接、监控和自动化WhatsApp消息发送。

**由于需求量大以及近期出现的注册问题，我们特别推出了一项限时优惠：顶级Business计划，每月仅需19.90美元（按年计费），且配无限发送额度。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
同时，也提供免费试用计划。** [立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow的核心功能：  
- **批量发送消息**：支持安全发送机制，可自定义发送间隔（模拟人类发送消息的节奏）。  
- **定时消息**：支持设置一次性或定期发送消息的时间表。  
- **报告生成**：自动生成活动报告，便于数据分析。  
- **自定义联系人组**：可创建和管理目标联系人列表。  

## 实际应用场景：  
- **健身房老板**：定期向会员发送新年祝福信息，并附赠折扣码，同时避免被WhatsApp封禁。  
- **自由职业顾问**：每周五下午向活跃客户发送周末服务信息。  
- **营销机构**：整合多个WhatsApp群组的数据，生成统一的目标联系人列表，用于发布产品公告。  

## 使用场景：  
- 批量发送消息  
- 安排定时消息  
- 生成报告  
- 创建联系人组  
- 暂停或恢复批量发送  
- 将联系人信息导出为CSV或JSON  
- 设置每周更新通知  

## 前提条件：  
1. **MOLTFLOW_API_KEY**：需从[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”中生成。  
2. 至少已连接一个可使用的WhatsApp会话（状态为“working”）。  
3. 基础URL：`https://apiv2.waiflow.app/api/v2`  

## 所需API权限：  
| 权限范围 | 访问权限 |  
|--------|--------|  
| `custom-groups` | `读取/管理` |  
| `bulk-send` | `读取/管理` |  
| `scheduled` | `读取/管理` |  
| `reports` | `读取/管理` |  

## 认证方式：  
每个请求都必须包含以下认证信息之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```  

---

## **自定义联系人组**  
自定义联系人组可用于批量发送和定时消息。这些组是MoltFlow内部的联系人列表，而非WhatsApp群组。  

- **操作方法** | **端点** | **说明**  
|--------|----------|-------------|  
| GET` | `/custom-groups` | 列出所有自定义组。  
| POST` | `/custom-groups` | 创建新的自定义组（可选包含初始成员）。  
| GET` | `/custom-groups/contacts` | 列出所有跨会话的唯一联系人。  
| GET` | `/custom-groups/wa-groups` | 列出可用于导入的WhatsApp群组。  
| POST` | `/custom-groups/from-wa-groups` | 通过导入WhatsApp群组成员创建新组。  
| GET` | `/custom-groups/{id}` | 查看组详情及成员信息。  
| PATCH` | `/custom-groups/{id}` | 更新组名。  
| DELETE` | `/custom-groups/{id}` | 删除组及所有成员。  
| POST` | `/custom-groups/{id}/members/add` | 添加成员（避免重复）。  
| POST` | `/custom-groups/{id}/members/remove` | 按电话号码删除成员。  
| GET` | `/custom-groups/{id}/export/csv` | 将成员信息导出为CSV。  
| GET` | `/custom-groups/{id}/export/json` | 将成员信息导出为JSON。  

### 创建自定义组  
**POST** `/custom-groups`  
（具体请求参数见**CODE_BLOCK_2___**）  

### 从WhatsApp群组创建自定义组  
**POST** `/custom-groups/from-wa-groups`  
（具体请求参数见**CODE_BLOCK_3___**）  

### 列出所有WhatsApp群组  
**GET** `/custom-groups/wa-groups`  
（返回所有可导入的WhatsApp群组及其成员数量。）  

### 添加成员  
**POST** `/custom-groups/{id}/members/add`  
（每个联系人对象包含`phone`（必填）和`name`（可选）信息。每次请求最多添加1,000个成员，重复成员会被自动忽略。）  

### 导出成员信息  
**GET** `/custom-groups/{id}/export/csv` | 以CSV格式导出成员信息。  
**GET** `/custom-groups/{id}/export/json` | 以JSON格式导出成员信息。  

---

## **批量发送消息**  
- 可向自定义组发送消息，系统会自动控制发送间隔（避免被封禁）。  
- 支持定时发送，每次发送之间有30秒至2分钟的随机延迟。  

- **操作方法** | **端点** | **说明**  
|--------|----------|-------------|  
| POST` | `/bulk-send` | 创建批量发送任务。  
| GET` | `/bulk-send` | 查看所有批量发送任务列表。  
| GET` | `/bulk-send/{id}` | 查看任务详情及接收者信息。  
| POST` | `/bulk-send/{id}/pause` | 暂停正在执行的任务。  
| POST` | `/bulk-send/{id}/resume` | 恢复暂停的任务。  
| POST` | `/bulk-send/{id}/cancel` | 取消任务（释放未使用的发送额度）。  
| GET` | `/bulk-send/{id}/progress` | 通过SSE实时获取发送进度。  

### 创建批量发送任务  
**POST** `/bulk-send`  
（具体请求参数见**CODE_BLOCK_6___**）  

### 实时进度监控  
**GET** `/bulk-send/{id}/progress`  
（通过SSE实时获取发送进度信息。）  

## **定时消息**  
- 可安排一次性或定期向自定义组发送消息，支持时区设置。  

- **操作方法** | **端点** | **说明**  
|--------|----------|-------------|  
| GET` | `/scheduled-messages` | 列出所有定时任务。  
| POST` | `/scheduled-messages` | 创建新的定时任务（一次性或定期）。  
| GET` | `/scheduled-messages/{id}` | 查看任务详情及执行历史。  
| PATCH` | `/scheduled-messages/{id}` | 更新任务设置或重新计算发送时间。  
| POST` | `/scheduled-messages/{id}/cancel` | 取消定时任务。  
| POST` | `/scheduled-messages/{id}/pause` | 暂停正在执行的定时任务。  
| DELETE` | `/scheduled-messages/{id}` | 删除已取消或完成的任务。  
| GET` | `/scheduled-messages/{id}/history` | 查看任务执行历史（分页显示）。  

### 创建一次性定时任务  
**POST** `/scheduled-messages`  
（具体请求参数见**CODE_BLOCK_9___**）  

### 创建定期任务（使用cron表达式）  
**POST** `/scheduled-messages`  
（具体请求参数见**CODE_BLOCK_10___**）  

**注意：** 所有定期任务类型（`daily`、`weekly`、`monthly`、`cron`）都需要提供`cron_expression`。最小间隔为5分钟。  

## 报告功能  
- 可生成自动化报告，涵盖消息发送、会话活动等数据。  
- 报告模板支持多种格式（如纯文本或直接发送到WhatsApp）。  

- **发送方式**：  
  - **`dashboard`：报告以表格形式显示在MoltFlow控制台。  
  - **`whatsapp`：报告以纯文本形式发送到指定的WhatsApp会话。  

## 示例：  
- 完整工作流程：创建自定义组 → 批量发送 → 安排定时任务。  
- 暂停或恢复批量发送。  
- 导出联系人信息。  

## 计划方案限制：  
| 功能 | 免费版 | 起始版 | 专业版 | 商业版 |  
|---------|------|---------|-----|----------|  
| 自定义组 | 2个 | 5个 | 20个 | 100个 |  
| 批量发送 | 无限制 | 是 | 是 | 是 |  
| 定时消息 | 无限制 | 是 | 是 | 是 |  
| 定时报告 | 2个 | 5个 | 10个 | 无限 |  
| 每月消息发送量 | 50条 | 500条 | 1,500条 | 3,000条 |  

## 错误代码说明：  
- **400**：请求无效。  
- **401**：未经授权。  
- **403**：超出计划限制或功能限制。  
- **404**：资源未找到。  
- **422**：缺少必要字段。  
- **429**：达到发送频率上限。  

## 相关服务：  
- **moltflow**：提供核心API接口（会话管理、消息发送、联系人组管理等）。  
- **moltflow-leads**：用于检测潜在客户、跟踪销售流程等。  
- **moltflow-ai**：支持智能回复、语音转录等功能。  
- **moltflow-a2a**：实现代理间安全通信。  
- **moltflow-reviews**：用于收集用户评价和管理反馈。  
- **moltflow-admin**：用于平台管理和用户配置。  

## **WhatsApp频道（v7.0）**  
支持向WhatsApp频道发送消息，无需公开你的电话号码，且无需担心垃圾信息问题。  

**实际应用场景：**  
- **出版商**：每周一上午9点向频道发送新闻通讯。  
- **品牌**：向3,000名频道订阅者立即发布产品公告。  

**关键API端点：**  
- **列出/创建/管理频道**：`/api/v2/channels`  
- **安排频道发布**：`/api/v2/channels/scheduled-messages`（目标类型：channel）。  

## 计划方案限制：  
- **免费版**：最多1个频道，每月1条发布。  
- **专业版**：最多5个频道，每月50条发布。  
- **商业版**：最多20个频道，每月2,000条发布。  

---

更多详细信息和示例代码请参阅官方文档。