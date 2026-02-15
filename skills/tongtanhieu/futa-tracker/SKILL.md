---
name: futa-tracker
description: 使用 FUTA Express（Phương Trang）的公开 API 来追踪包裹的配送状态。当用户需要查询或追踪来自 FUTA Express 或 Phương Trang Express 的订单时，可以使用此功能。查询时需要提供一个追踪码（mã vận đơn）。
---

# Futa Tracker

## 概述

该技能允许通过 FUTA Express 的公共 API 来跟踪包裹的配送状态。

## API 端点

```
https://api.futaexpress.vn/bo-operation/f1/full-bill-by-code-public/<tracking_code>
```

## 跟踪流程

1. 从用户输入中提取跟踪代码。
2. 使用 `web_fetch` 调用 API。
3. 解析 JSON 响应。
4. 显示详细的跟踪信息。
5. **重要提示**：所有字段均保持原始的越南语格式，切勿翻译。

## 响应结构

响应中的关键字段：
- `data.barcode` - 包裹编码
- `data.from_fullname` / `data.from_phone` - 发件人
- `data.to_fullname` / `data.to_phone` - 收件人
- `data.from_department_name` - 发货地点
- `data.to_department_name` - 收货地点
- `data.service_type_name` - 服务类型
- `data.pay_type` - 支付方式
- `data.package_total` - 包裹数量
- `data.totalcost` - 总费用
- `data.addcost` - 额外费用
- `data.status_bill` - 订单状态
- `data.note` - 备注
- `data.packages[]` - 每个包裹的详细信息
  - `package_description` - 包裹描述
  - `receive_fullname` / `receive_phone` / `receive_identity` - 实际收件人
  - `receive_time` - 收货时间
  - `arrival_time` - 到达时间
  - `go_time` - 出发时间
  - `arrival_note` - 到达地点的备注
- `data.services[]` - 额外服务
  - `add_service_name` - 服务名称
  - `value` - 服务费用
- `data.trackings[]` - 跟踪记录（通常与 `packages` 数组中的信息重复）

## 输出格式

信息应按以下顺序显示：

```
📦 FUTA Express - Tra cứu vận đơn: <barcode>

👤 Người gửi: <from_fullname>
   📞 <from_phone>
   🏢 Điểm gửi: <from_department_name>

👤 Người nhận: <to_fullname>
   📞 <to_phone>
   🏢 Điểm đến: <to_department_name>

📋 Thông tin đơn hàng:
   • Loại dịch vụ: <service_type_name>
   • Hình thức thanh toán: <pay_type>
   • Số kiện: <package_total>
   • Tổng chi phí: <totalcost>đ (cước chính: <cost_main>đ + phụ: <addcost>đ)
   • Trạng thái: <status_bill>

📦 Chi tiết hàng hóa:
   • <packages[*].package_description>
   Ghi chú vận chuyển: <packages[*].arrival_note>

🔐 Người nhận thực tế (nếu đã giao):
   • Tên: <packages[*].receive_fullname>
   • SĐT: <packages[*].receive_phone>
   • CMND/CCCD: <packages[*].receive_identity>
   • Thời gian nhận: <packages[*].receive_time>

📝 Ghi chú đơn hàng: <note>

📍 Lịch sử vận chuyển:
| Thời gian | Trạng thái | Chi tiết |
|-----------|------------|----------|
| <time> | <status> | <details> |

🛎️ Dịch vụ thêm:
   • <add_service_name>: <value>đ
```

## 重要规则

- **切勿翻译越南语字段**：状态名称、部门名称等所有字段均保持越南语原样。
- 货币格式使用句点（例如：350.000đ）。
- 如果存在部分电话号码/ID 信息，应将其隐藏（用 X 表示或按 API 的原始格式显示）。
- 时间戳需以易读的格式显示（YYYY-MM-DD HH:MM）。
- 显示响应中的所有有效数据。

## 错误处理

- 如果 `data.bill_id` 为 0：未找到跟踪代码。
- 如果 `data.packages` 为空：没有包裹详细信息。
- 即使某些字段为空，也必须显示完整的响应数据。