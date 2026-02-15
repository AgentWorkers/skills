---
name: tour-booking
description: 子代理用于执行出站列表办公室（listing-office）的呼叫任务，以使用提供的呼叫脚本和结构化数据（payload）来请求并确认房产展示的可用时间（showing slots）。当父工作流程需要为一个或多个房产执行呼叫操作时，可以使用该子代理，包括生成测试数据（dry-run payload）、发起实际的 ElevenLabs 呼叫请求，以及将呼叫结果解析为预订状态（booking statuses）。
---
# 旅游预订服务

## 概述

本模块负责处理与旅游预订相关的电话呼叫执行流程：
1. 根据房源信息和客户数据生成统一的通话提示语。
2. 向 ElevenLabs 发送出站呼叫请求（或进行模拟测试）。
3. 将呼叫结果转换为结构化的状态字段。

## 输入参数

每个呼叫任务应包含以下信息：
- `job_id`（任务ID）
- `client_name`（客户名称）
- `listing.address`（房源地址）
- `listing.office_phone`（房产办公室电话）
- `preferred_windows_text`（客户偏好的联系时间窗口）
- `timezone`（客户所在的时区）

## 执行流程

### 1) 构建请求数据

```bash
python3 scripts/prepare_call_payload.py \
  --job /tmp/job.json \
  --output /tmp/call-payload.json
```

### 2) 发起呼叫

- 模拟测试（默认安全模式）：
```bash
python3 scripts/place_outbound_call.py \
  --payload /tmp/call-payload.json \
  --output /tmp/call-result.json \
  --dry-run
```

- 实时模式：
```bash
python3 scripts/place_outbound_call.py \
  --payload /tmp/call-payload.json \
  --output /tmp/call-result.json \
  --live
```

### 3) 解析呼叫结果

```bash
python3 scripts/parse_call_result.py \
  --input /tmp/call-result.json \
  --output /tmp/booking-outcome.json
```

## 呼叫规则

- 明确说明呼叫方是由房产经纪人代表人工智能助手进行的。
- 首先询问客户请求的时间窗口内是否有可用的预订时段；如果无法满足需求，提供其他替代方案。
- 在结束通话前，确认最终的预订时段（包括具体日期和当地时间）。
- 如果房产办公室无法确认预订，将状态标记为 `pending_callback`（待回电），并记录回电的相关要求。