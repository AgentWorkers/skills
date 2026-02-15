---
name: moltflow-outreach
description: "批量消息发送、定时消息发送、定时报告生成以及用于 WhatsApp 宣传活动的自定义群组功能。适用场景包括：批量发送消息、广播消息、定时发送消息、定时生成报告、使用 cron 任务、创建自定义群组、以及进行安全（不会被屏蔽）的消息交流。"
source: "MoltFlow Team"
version: "2.8.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---

**MoltFlow**——专为团队设计的WhatsApp Business自动化工具。支持大规模连接、监控和自动化WhatsApp消息发送。

**由于需求旺盛以及近期出现的注册问题，我们特别推出了一项限时优惠：**顶级商务计划（Business Plan）每月仅需19.90美元（按年计费），且配无限发送额度。**[立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
同时，我们还提供免费试用计划。**[立即注册](https://molt.waiflow.app/checkout?plan=free)

# MoltFlow的主要功能：
- **批量发送消息**：支持安全发送机制，可自定义发送间隔（模拟人类发送消息的频率）。
- **定时消息**：支持定时发送一次性或重复性消息，并支持时区设置。
- **报告生成**：自动生成活动报告，可查看发送详情和效果。
- **自定义联系人组**：方便管理目标联系人群组，便于批量发送或定时发送消息。

## 使用场景：
- 需要向大量联系人发送消息。
- 需要定时向特定联系人群组发送消息。
- 需要生成活动报告以分析发送效果。
- 需要创建或管理联系人列表。
- 需要暂停或取消批量发送操作。
- 需要将联系人信息导出为CSV或JSON格式。

## 前提条件：
1. **MOLTFLOW_API_KEY**：请从[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”中生成。
2. 至少已连接一个可使用的WhatsApp会话（状态为“working”）。
3. 基础URL：`https://apiv2.waiflow.app/api/v2`。

## 所需API权限：
| 权限范围 | 访问权限 |
|---------|---------|
| `custom-groups` | `读取/管理` |
| `bulk-send` | `读取/管理` |
| `scheduled` | `读取/管理` |
| `reports` | `读取/管理` |

## 认证要求：
所有请求必须包含以下认证信息之一：

---

## 自定义联系人组（Custom Groups）：
- **创建自定义联系人组**：用于批量发送或定时发送消息。这些组是MoltFlow内部管理的联系人列表，而非WhatsApp官方群组。
  - **API方法**：`POST /custom-groups`  
  - **参数说明**：
    - `/custom-groups`：列出所有自定义组。
    - `/custom-groups`：创建新的自定义组（可选指定初始成员）。
    - `/custom-groups/contacts`：列出所有跨会话的唯一联系人。
    - `/custom-groups/wa-groups`：列出可用于导入的WhatsApp群组。
    - `/custom-groups/from-wa-groups`：通过导入WhatsApp群组成员创建自定义组。
    - `/custom-groups/{id}`：查看或修改特定组的详细信息及成员。
    - `/custom-groups/{id}`：删除组及其成员。
    - `/custom-groups/{id}/members/add`：添加成员（避免重复）。
    - `/custom-groups/{id}/members/remove`：按电话号码删除成员。
    - `/custom-groups/{id}/export/csv`：将成员信息导出为CSV。
    - `/custom-groups/{id}/export/json`：将成员信息导出为JSON。

### 创建自定义组（Create Custom Group）：
**POST** `/custom-groups`
**参数说明**：
- `members`：一个包含`phone`（必填）和`name`（可选）的数组。省略`members`参数可创建空组。

### 从WhatsApp群组创建自定义组（Create Group from WhatsApp Groups）：
**POST** `/custom-groups/from-wa-groups`
**参数说明**：
- 从指定的WhatsApp群组中提取成员信息，去除重复项后创建自定义组。

### 查看WhatsApp群组（View WhatsApp Groups）：
**GET** `/custom-groups/wa-groups`
**返回内容**：列出所有可导入的WhatsApp群组及其成员数量。

### 添加成员（Add Members）：
**POST** `/custom-groups/{id}/members/add`
**参数说明**：
- 每个联系人对象包含`phone`（必填）和`name`（可选）字段。每次请求最多添加1,000个成员，重复成员会被自动忽略。

### 导出成员信息（Export Members）：
**GET** `/custom-groups/{id}/export/csv`：将成员信息导出为CSV文件。
**GET** `/custom-groups/{id}/export/json`：将成员信息导出为JSON数组。

## 批量发送消息（Bulk Send）：
- **创建批量发送任务**：设置发送间隔，模拟人类发送消息的频率。
  - **API方法**：`POST /bulk-send`
  - **参数说明**：
    - `session_id`：发送消息的WhatsApp会话ID。
    - `custom_group_id`：目标自定义组ID。
    - `message_type`：消息类型（`text`或`media`）。
    - `message_content`：消息内容（最多4096个字符）。
    - `media_url`：媒体文件的HTTP(S)链接（如提供媒体文件）。
  **返回内容**：任务创建成功后的响应。

### 实时跟踪发送进度（Stream Progress）：
**GET** `/bulk-send/{id}/progress`
**返回内容**：通过Server-Sent Events（SSE）实时更新发送进度。

## 定时消息（Scheduled Messages）：
- **创建定时消息**：支持一次性或重复性消息发送，并支持时区设置。
  - **API方法**：`POST /scheduled-messages`
  - **参数说明**：
    - `name`：定时消息的名称。
    - `session_id`：发送消息的WhatsApp会话ID。
    - `custom_group_id`：目标自定义组ID。
    - `schedule_type`：发送类型（`one_time`、`daily`、`weekly`、`monthly`或`cron`。
    - `cron_expression`：定时表达式（用于重复性消息）。
  **返回内容**：任务创建成功后的响应。

## 定时报告（Scheduled Reports）：
- **生成报告**：定期生成活动报告。
  - **API方法**：`POST /reports`
  - **参数说明**：
    - `name`：报告名称。
    - `schedule_type`：报告类型。
    - `delivery_method`：报告发送方式（`dashboard`或`whatsapp`）。
  **返回内容**：报告生成后的响应，可根据设置发送方式查看或接收。

## 示例用法：
- **完整工作流程**：创建自定义组 → 批量发送消息 → 定时发送消息。

## 计划限制（Plan Limits）：
| 功能 | 免费版 | 起始版 | 专业版 | 商务版 |
|---------|---------|---------|---------|----------|
| 自定义联系人组 | 2个 | 5个 | 20个 | 100个 |
| 批量发送 | 不支持 | 支持 | 支持 | 支持 |
| 定时消息 | 不支持 | 支持 | 支持 | 支持 |
| 定时报告 | 2个 | 5个 | 10个 | 无限制 |
| 每月发送消息数量 | 50条 | 500条 | 1,500条 | 3,000条 |

## 错误响应（Error Responses）：
- **常见错误代码及含义**：
  - `400`：请求无效。
  - `401`：未经授权。
  - `403`：超出计划限制或功能限制。
  - `404`：资源未找到。
  - `422`：缺少必要参数。
  - `429`：达到发送频率上限。

## 相关服务：
- **moltflow**：提供核心API接口，用于管理会话、消息发送、联系人组等。
- **moltflow-leads**：用于检测潜在客户、跟踪销售流程、批量操作等。
- **moltflow-ai**：提供智能自动回复、语音转录等功能。
- **moltflow-a2a**：支持代理间加密通信和内容策略。
- **moltflow-reviews**：用于收集用户评价和反馈。
- **moltflow-admin**：用于平台管理和用户配置。