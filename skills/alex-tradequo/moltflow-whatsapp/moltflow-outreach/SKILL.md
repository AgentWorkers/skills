---
name: moltflow-outreach
description: "批量消息发送、定时消息发送、定时报告生成以及用于 WhatsApp 联络的自定义群组功能。适用场景包括：批量发送消息、广播消息、定时发送消息或报告、使用 Cron 任务进行自动化操作、创建自定义群组、以及安全地与联系人列表中的成员进行消息交流。"
source: "MoltFlow Team"
version: "2.11.8"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow**——专为团队设计的WhatsApp Business自动化工具。支持大规模连接、监控和自动化WhatsApp消息发送。

**由于需求量大以及近期出现的注册问题，我们特别推出了一项限时优惠：**顶级Business套餐每月仅需19.90美元（按年计费），并提供无限发送额度。**[立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
同时，也提供免费套餐。**[立即注册](https://molt.waiflow.app/checkout?plan=free)

# MoltFlow核心功能：批量发送、定时消息、报告生成与自定义联系人组管理

- **批量发送**：支持安全限制机制，可向自定义联系人列表发送消息；支持时区设置，可定时发送重复消息。
- **报告生成**：自动生成包含发送结果的报告，并支持通过WhatsApp发送。
- **自定义联系人组**：可创建目标联系人组，用于批量发送或定时消息。

## 使用场景：
- 批量发送消息或向特定群组广播消息。
- 安排WhatsApp消息的发送时间或设置重复发送规则。
- 生成发送统计报告或获取使用情况汇总。
- 创建新的联系人列表或自定义联系人组。
- 暂停批量发送或取消已安排的发送任务。
- 将联系人组成员导出为CSV格式或导入新联系人。
- 设置每周更新通知或安排定时任务。

## 前提条件：
1. **MOLTFLOW_API_KEY**：需从[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”中生成。
2. 至少已连接一个处于“工作”状态的WhatsApp会话。
3. 基本URL：`https://apiv2.waiflow.app/api/v2`。

## 所需API权限：
| 权限范围 | 访问权限 |
|---------|---------|
| `custom-groups` | 读取/管理 |
| `bulk-send` | 读取/管理 |
| `scheduled` | 读取/管理 |
| `reports` | 读取/管理 |

## 认证要求：
所有请求必须包含以下认证信息之一：

---

## 自定义联系人组
**自定义联系人组**用于实现批量发送和定时消息功能。这些组是MoltFlow内部的联系人列表，而非WhatsApp上的实际群组。

| 方法 | 端点 | 功能描述 |
|--------|----------|-------------|
| GET | `/custom-groups` | 查看所有自定义联系人组 |
| POST | `/custom-groups` | 创建新的自定义联系人组（可选包含初始成员） |
| GET | `/custom-groups/contacts` | 查看所有跨会话的唯一联系人信息 |
| GET | `/custom-groups/wa-groups` | 查看可用于导入的WhatsApp群组列表 |
| POST | `/custom-groups/from-wa-groups` | 通过导入WhatsApp群组成员创建自定义联系人组 |
| GET | `/custom-groups/{id}` | 查看特定联系人组的详细信息及成员列表 |
| PATCH | `/custom-groups/{id}` | 更新联系人组名称 |
| DELETE | `/custom-groups/{id}` | 删除联系人组及其所有成员 |
| POST | `/custom-groups/{id}/members/add` | 向联系人组添加成员（避免重复） |
| POST | `/custom-groups/{id}/members/remove` | 通过电话号码删除联系人组成员 |
| GET | `/custom-groups/{id}/export/csv` | 将联系人组成员导出为CSV文件 |
| GET | `/custom-groups/{id}/export/json` | 将联系人组成员导出为JSON文件 |

### 创建自定义联系人组
**POST** `/custom-groups`  
**示例代码：**（此处应插入具体的API请求格式）

### 从WhatsApp群组创建自定义联系人组
**POST** `/custom-groups/from-wa-groups`  
**示例代码：**（此处应插入具体的API请求格式）

### 查看WhatsApp群组
**GET** `/custom-groups/wa-groups`  
**响应示例：**  
`201 Created`：表示群组创建成功。

### 添加联系人组成员
**POST** `/custom-groups/{id}/members/add`  
**示例代码：**（此处应插入具体的API请求格式）

**注意：**每个联系人对象必须包含`phone`（必填）和`name`（可选）字段。请求最多可添加1,000个成员，系统会自动处理重复成员。

### 导出联系人组成员
**GET** `/custom-groups/{id}/export/csv` | 以CSV格式导出成员列表  
**GET** `/custom-groups/{id}/export/json` | 以JSON格式导出成员列表

## 批量发送
**批量发送**功能支持安全限制机制，确保发送速度不会过快导致被封禁。消息之间会随机间隔30秒至2分钟，以模拟真实用户行为。

| 方法 | 端点 | 功能描述 |
|--------|----------|-------------|
| POST | `/bulk-send` | 创建批量发送任务（占用相应发送额度） |
| GET | `/bulk-send` | 查看所有已创建的批量发送任务 |
| GET | `/bulk-send/{id}` | 查看特定任务的详细信息及接收者列表 |
| POST | `/bulk-send/{id}/pause` | 暂停正在运行的任务 |
| POST | `/bulk-send/{id}/resume` | 恢复暂停的任务 |
| POST | `/bulk-send/{id}/cancel` | 取消任务（释放未使用的发送额度） |
| GET | `/bulk-send/{id}/progress` | 通过SSE（Server-Sent Events）实时获取发送进度 |

**创建批量发送任务**
**POST** `/bulk-send`  
**示例代码：**（此处应插入具体的API请求格式）

### 实时获取发送进度
**GET** `/bulk-send/{id}/progress`  
**响应示例：**  
`201 Created`：表示任务创建成功。

## 定时消息
**可安排一次性或重复的WhatsApp消息发送，支持时区设置，并提供完整的任务生命周期管理功能。**

| 方法 | 端点 | 功能描述 |
|--------|----------|-------------|
| GET | `/scheduled-messages` | 查看所有已安排的消息任务 |
| POST | `/scheduled-messages` | 创建新的定时消息任务（一次性或重复发送） |
| GET | `/scheduled-messages/{id}` | 查看特定任务的详细信息及执行历史记录 |
| PATCH | `/scheduled-messages/{id}` | 更新任务设置或重新计算下次发送时间 |
| POST | `/scheduled-messages/{id}/cancel` | 取消已安排的任务 |
| POST | `/scheduled-messages/{id}/pause` | 暂停正在执行的任务 |
| POST | `/scheduled-messages/{id}/resume` | 恢复暂停的任务 |
| DELETE | `/scheduled-messages/{id}` | 删除已取消或已完成的任务 |
| GET | `/scheduled-messages/{id}/history` | 分页查看任务执行历史记录 |

**创建一次性定时任务**
**POST** `/scheduled-messages`  
**示例代码：**（此处应插入具体的API请求格式）

**创建重复发送任务（使用Cron表达式）**
**POST** `/scheduled-messages`  
**示例代码：**（此处应插入具体的API请求格式）

**响应示例：**  
`201 Created`：表示任务创建成功。

### 定时任务类型：
- `one_time`：在指定时间点发送一次消息。
- `daily`：每天发送一次（需要提供Cron表达式）。
- `weekly`：每周发送一次（需要提供Cron表达式）。
- `monthly`：每月发送一次（需要提供Cron表达式）。
- `cron`：使用自定义Cron表达式（例如：`0 9 * * MON-FRI`）。

**注意：**所有重复发送任务类型都需要提供Cron表达式。最小间隔时间为5分钟。

## 报告生成
**可定期生成MoltFlow活动的自动化报告，支持10种预设模板。**报告可查看于控制台，也可直接发送至用户的WhatsApp会话。

- 将`delivery_method`设置为`"whatsapp"`，即可将报告直接发送至用户的WhatsApp会话。报告以纯文本格式发送，接收者会看到该消息。

**示例代码：**（此处应插入具体的API请求格式）

## 示例用法：
- 全流程示例：创建自定义联系人组 → 批量发送消息 → 安排定时发送。

## 计划限制：
| 功能 | 免费套餐 | 起始套餐 | Pro套餐 | Business套餐 |
|---------|--------|---------|---------|----------|
| 自定义联系人组 | 2个 | 5个 | 20个 | 100个 |
| 批量发送 | 不支持 | 支持 | 支持 | 支持 |
| 定时消息 | 不支持 | 支持 | 支持 | 支持 |
| 定时报告 | 2份/月 | 5份/月 | 10份/月 | 无限份 |
| 每月消息发送量 | 50条 | 500条 | 1,500条 | 3,000条 |

## 错误代码及其含义：
| 状态码 | 含义 |
|--------|---------|
| 400 | 请求无效 |
| 401 | 未经授权 |
| 403 | 超出计划限制或功能限制 |
| 404 | 资源未找到 |
| 422 | 缺少必要字段 |
| 429 | 发送频率超出限制 |

## 相关服务：
- **moltflow**：提供核心API接口，支持会话管理、消息发送、联系人组管理等功能。
- **moltflow-leads**：用于检测潜在客户、跟踪销售流程、支持CSV/JSON格式的数据导出。
- **moltflow-ai**：提供AI驱动的自动回复功能、语音转录服务等。
- **moltflow-a2a**：支持代理间加密通信和内容策略管理。
- **moltflow-reviews**：用于收集用户评价和反馈。
- **moltflow-admin**：提供平台管理和用户配置功能。