---
name: trendyol-admin
description: 通过API v2.0全面管理Trendyol市场平台。功能涵盖产品生命周期管理（创建、更新、删除、归档）、库存/价格管理、订单处理（状态更新、配送）、退货处理以及客户咨询。请将此技能作为知识库，用于构建正确的API请求。
---
# Trendyol Admin（AI知识库）

本文档提供了关于Trendyol Marketplace API v2.0的全面参考信息，涵盖了管理Trendyol店铺所需的所有端点、授权要求以及数据格式规范。

## 🛠 AI代理的使用方法

1. **身份验证**：始终使用基本身份验证（Basic Auth）：
   - 用户名：`API_KEY`
   - 密码：`API_SECRET`
   - 生成授权头（一行代码）：`echo -n "YOUR_API_KEY:YOUR_API_SECRET" | base64`

2. **必填请求头**：每个请求都必须包含以下头信息：
   - `Authorization: Basic <base64>`
   - `User-Agent: <SupplierId> - SelfIntegration`
   - `storeFrontCode`：**此参数用于切换不同国家/地区的市场设置**：
     - `AE`：阿拉伯联合酋长国（AED）
     - `SA`：沙特阿拉伯（SAR）
     - `QA`：卡塔尔（QAR）
     - `KW`：科威特（KWD）
     - `BH`：巴林（BHD）
     - `OM`：阿曼（OMR）
     - `DE`：德国（EUR）
     - `AZ`：阿塞拜疆（AZN）
     - `RO`：罗马尼亚（RON）
     - `CZ`：捷克共和国（CZK）
     - `HU`：匈牙利（HUF）
     - `SK`：斯洛伐克（EUR）
     - `BG`：保加利亚（BGN）
     - `GR`：希腊（EUR）

3. **端点**：请参考[references/api_reference.md](references/api_reference.md)以获取相应操作的正确URL（如产品查询、库存管理、订单处理等）。

4. **执行方式**：由于没有预构建的脚本，需使用`curl`或Node.js/Python等工具，根据参考文档中的说明来发送请求。

## 📖 参考文档中的关键章节

- **身份验证**：授权头的生成方式及错误代码说明。
- **产品集成**：产品的完整生命周期管理。
- **订单集成**：从创建订单到更新订单状态的全过程。
- **Webhooks**：实时通知机制。
- **API参考文档**：[references/api_reference.md](references/api_reference.md)

## ⚠️ 重要规则

- **基础URL（生产环境）**：`https://apigw.trendyol.com/integration/`
- **请求频率限制**：每10秒内最多发送50个请求。
- **图片要求**：图片尺寸为1200x1800像素，且必须使用HTTPS链接。
- **数据格式**：所有请求数据必须为有效的JSON格式。