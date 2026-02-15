---
name: google-maps-leadgen
description: **使用自托管的MCP服务器（`google-maps`）从Google Maps中生成B2B潜在客户，并将结果导出为CSV或XLSX格式。**  
适用于以下场景：  
- 用户按国家/城市/行业筛选潜在客户；  
- 需要获取潜在客户的电话号码、网站地址或电子邮件信息；  
- 需要去除重复的潜在客户数据；  
- 希望通过聊天工具（尤其是Telegram）接收潜在客户数据文件。
---

# Google Maps潜在客户生成（MCP）

使用此技能通过MCP从Google Maps中批量生成潜在客户信息。

## 前提条件

- `mcporter`已配置为使用`google-maps`服务器。
- 环境变量`GOOGLE_MAPS_API_KEY`中设置的服务器密钥必须与服务器兼容（无浏览器引用限制）。
- 如果需要XLSX格式的输出文件，确保`openpyxl`已安装在虚拟环境中。

## 快速工作流程

1. 根据地理位置和目标行业领域构建查询集。
2. 对每个查询执行`maps_search_places`操作。
3. 仅保留位于目标区域内的地点信息，并通过`place_id`进行去重处理。
4. 使用`maps_place_details`功能丰富每个地点的详细信息。
5. 将结果导出为CSV或XLSX格式的文件。
6. 如果用户通过Telegram请求文件，可以使用`message`工具发送文件（使用`action=send`和`media`参数指定文件路径）。

## 查询策略

使用具体、明确的关键词进行搜索，避免使用过于宽泛的通用术语。

- 例如：`"odoo partner <城市> <国家>"`、`"erp integrator <城市> <国家>"`、`"logistics company <城市> <国家>"`
- 避免一次性查询大量重复的地点信息；应分批处理。

## 必需的输出列（V2）

- `name`（名称）
- `address`（地址）
- `phone`（电话号码）
- `website`（网站地址）
- `email`（如果无法获取则显示为空）
- `rating`（评分）
- `place_id`（地点ID）
- `google_maps_url`（适用于移动设备）：
  - `https://www.google.com/maps/search/?api=1&query=<名称>&query_place_id=<地点ID>`

## 成本说明

- 搜索请求通常是主要的付费项目。
- 丰富地点详细信息会额外产生费用。
- 提供粗略的运行成本估算，并说明免费使用量的限制。

## 可靠性保障措施

- 分批处理数据（每批10–50条记录），以避免长时间运行导致超时。
- 对于临时性的故障，应设置重试机制。
- 绝不要泄露API密钥或敏感的输出文件。

## 交付规则

- 如果用户通过聊天请求CSV或XLSX文件，使用`message`工具发送文件（附带`media`参数）。
- 如果用户特别要求XLSX格式或需要对文件进行编辑，请遵循XLSX文件的工作流程标准。
- 保持报告简洁明了：包括数据数量、覆盖范围（是否包含电话号码、网站地址、电子邮件地址）以及文件路径和名称。