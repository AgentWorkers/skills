---
name: farmos-land-portfolio
description: 查询土地所有权、租赁信息、房东详情以及土地相关费用。编写用于支付管理和租赁续期的操作流程。
tags: [farming, land, leases, landlords]
---
# FarmOS 土地管理功能

用于跟踪拥有的和租赁的土地、租赁条款、房东信息、付款情况以及每年的土地成本。

## 重要规则：数据完整性

**严禁使用不完整或被截断的数据。以下规则不可商量：**

1. **严禁使用 `/api/integration/dashboard`** — 该接口仅返回前5条记录，数据会被截断。部分付款信息比没有数据更糟糕，因为它会给人一种数据完整的错觉。
2. **必须使用下面列出的 `/all` 端点来获取完整的数据。**
3. **如果某个接口返回错误或空结果，必须立即向用户报告问题。** 不要默默地切换到其他接口或展示不完整的数据。
4. **必须明确说明返回的记录总数**，让用户知道数据是完整的。例如：“找到了3月份到期的11笔付款，总金额为175,058美元。”
5. **如果无法获取完整数据，必须明确说明。** “我无法获取完整的付款数据”比仅显示11笔付款中的5笔要好得多。

## 该功能适用的场景

- “我们的租赁合同什么时候到期？”
- “Smith地块的租金是多少？”
- “今年的总土地成本是多少？”
- “显示逾期未付的付款记录”
- “房东联系方式”
- “按地块计算每英亩的成本”
- “列出所有租赁的地块”
- “3月份到期的付款有哪些？”
- “下个月的资金需求”
- “将付款 [X] 标记为已支付”
- “将所有3月份的付款标记为已支付”
- “续签Smith地块的租赁合同”
- “预览租赁合同的续签信息”

## 访问控制

租赁条款、租金金额和房东信息属于敏感的商业数据，仅限管理员或经理角色访问。

**角色权限分配：** 查看 `~/.openclaw/farmos-users.json` 中用户的角色。如果用户不是管理员或经理，应告知他们无法访问土地管理数据。

## API 基础地址

http://100.102.77.110:8009

## 集成接口（无需认证）——仅用于读取操作

**重要提示：** 对于写入操作（如标记付款为已支付、续签合同），请使用认证接口；对于读取操作（如列出付款记录、租赁信息、房东信息），请使用 `/all` 端点。**

### 付款信息（完整数据）

**GET /api/integration/payments/all**  
- 返回所有付款的详细信息，包括地块名称、房东名称、逾期状态  
- 查询参数：  
  - `status`：待支付、已支付、逾期、计划支付  
  - `payment_type`：租金、抵押贷款、房产税、保险费、其他费用  
  - `parcel_id`：按特定地块筛选  
  - `due_date_from`：付款开始的日期范围  
  - `due_date_to`：付款结束的日期范围  
  - `crop_year`：按作物年份筛选  
- 示例：  
  - 所有逾期付款：`/api/integration/payments/all?status=overdue`  
  - 2026年3月份的付款记录：`/api/integration/payments/all?due_date_from=2026-03-01&due_date_to=2026-03-31`  
  - 所有租金付款：`/api/integration/payments/all?payment_type=rent`  

### 即将到期的付款（未来N天内）

**GET /api/integration/payments/upcoming?days=30**  
- 返回未来N天内所有即将到期的付款记录（数据不会被截断）  
- 可使用 `days=60` 或 `days=90` 来查看更长时间范围内的付款记录  

### 租赁合同信息

**GET /api/integration/leases/all**  
- 返回所有租赁合同的详细信息，包括房东联系方式和租赁条款  
- 查询参数：  
  - `status`：有效、已到期  
  - `landlord_id`：按房东筛选  

### 即将到期的租赁合同

**GET /api/integration/leases/expiring?days=90**  
- 返回未来N天内到期的所有租赁合同  

### 房东信息

**GET /api/integration/landlords/all**  
- 返回所有房东的详细信息，包括活跃租赁合同的数量、总英亩数和总租金  

### 地块信息

**GET /api/integration/parcels**  
- 返回所有地块的详细信息，包括所有权类型和英亩数  
- 查询参数：`ownership_type`（自有或租赁）  

### 综合统计信息

**GET /api/integration/summary**  
- 总英亩数、自有/租赁地块的分布情况、地块/租赁合同/房东的数量以及年度成本  

### 年度土地成本（按月份和实体划分）

**GET /api/integration/finance/costs?year=2026**  
- 按类别（租金、抵押贷款、税费、保险费）划分的月度成本  
- 实体分类  
- 查询参数：`year`、`entity_id`  

### 每块土地的成本（用于损益计算）

**GET /api/integration/finance/cost-per-field?year=2026**  
- 分配给生产地块的土地成本  
- 查询参数：`year`、`entity_id`  

### 逾期未付的款项

**GET /api/integration/tasks/overdue**  
- 所有逾期未付的付款记录及提醒  

### 需要处理的款项

**GET /api/integration/tasks/actionable?days_ahead=30**  
- 即将到期的付款记录、即将到期的租赁合同以及待处理的提醒  

## 需要认证的接口（用于写入操作）

这些接口需要使用JWT令牌进行认证。请参阅下面的认证部分。

### 认证流程

该功能需要使用JWT令牌来访问受保护的FarmOS接口。  

**获取令牌：** 使用相应的角色运行认证辅助工具：  
```bash
TOKEN=$(~/clawd/scripts/farmos-auth.sh admin)
```  

**使用令牌：** 将令牌作为Bearer令牌包含在请求头中：  
```bash
curl -H "Authorization: Bearer $TOKEN" http://100.102.77.110:8009/api/endpoint
```  

**令牌有效期：** 令牌有效期为15分钟。如果收到401错误响应，请请求新的令牌。  

### 标记单笔付款为已支付

**POST /api/payments/{id}/mark-paid**  
- 授权方式：Bearer {token}  
- 请求体格式：application/json  

### 批量标记付款为已支付

**POST /api/payments/bulk/mark-paid**  
- 授权方式：Bearer {token}  
- 请求体格式：application/json  

### 按日期范围标记付款为已支付

**POST /api/payments/bulk/mark-paid-by-date**  
- 授权方式：Bearer {token}  
- 请求体格式：application/json  

**示例：** 当用户要求“将3月份的所有付款标记为已支付”时，可以使用此接口进行批量操作。  

### 预览租赁合同续签信息

**POST /api/leases/renewal-preview**  
- 授权方式：Bearer {token}  
- 请求体格式：application/json  

**返回内容：** 显示续签后的租赁合同详情，包括新的付款计划。在执行批量续签操作前，请先预览。  

### 执行批量租赁合同续签

**POST /api/leases/bulk-renew**  
- 授权方式：Bearer {token}  
- 请求体格式：application/json  

**重要提示：** 必须先预览，确认用户需求后再执行操作。  

### 年度结算预览

**POST /api/payments/year-end-rollover/preview**  
- 授权方式：Bearer {token}  
- 请求体格式：application/json  

**返回内容：** 显示新作物年度的付款计划。  

### 年度结算执行

**POST /api/payments/year-end-rollover/execute**  
- 授权方式：Bearer {token}  
- 请求体格式：application/json  

**重要提示：** 该操作会根据当前年度的租赁合同生成下一年的付款计划。务必先预览。  

## 禁用接口

| 接口 | 禁用原因 |
|----------|-----|
| `GET /api/integration/dashboard` | 该接口仅返回前5条记录，数据会被截断。严禁使用。**  

## 关键概念

- **地块（Parcels）**：土地的基本单位，可以是自有或租赁的。  
- **租赁类型（Lease types）**：现金租金、作物分成租金、灵活租金等。  
- **租赁到期日（Lease expiration）**：需要密切关注的关键信息，临近到期的租赁合同需要及时处理。  
- **土地付款（Land payments）**：包括租金、抵押贷款、房产税、保险费等，每种费用都有相应的付款日期。  

## 使用注意事项

- 租赁合同到期日的跟踪是最重要的查询内容——务必标记出6个月内到期的租赁合同。  
- 付款状态（是否到期）非常重要——需立即标记逾期未付的款项。  
- 按英亩计算的成本分析有助于比较自有土地和租赁土地的经济效益。  
- 房东联系方式属于敏感信息——严禁在非管理员或经理渠道中泄露。  
- 当用户询问“资金需求”或“我们欠多少钱”时，务必使用 `/api/integration/payments/all` 并结合日期筛选来获取完整信息。  
- 对于财务规划问题，建议将 `/api/integration/payments/all` 与 `/api/integration/finance/costs` 结合使用以获取完整的数据。  
- **写入操作：** 对于标记付款为已支付或续签合同等操作，必须使用认证接口。执行批量操作前请先预览。  
- **批量标记付款**：当用户要求“将3月份的所有付款标记为已支付”时，请使用按日期分批处理的接口，而非单独调用每个接口。