# api-monetizer

该工具将微服务（micro-SaaS）的应用逻辑封装为付费API，并在RapidAPI等市场平台上进行发布。

## 概述

该工具从每个微服务产品中提取核心的转换/生成逻辑，将其封装成一个独立的API接口。同时生成相应的文档、使用示例以及市场平台所需的列表信息，从而实现基于API的收入来源，与通过Web界面获得的收入相辅相成。

## 使用方法

- `api create PRODUCT-SLUG`：为某个产品生成API接口
- `api docs PRODUCT-SLUG`：生成API文档
- `api listing PRODUCT-SLUG`：生成用于RapidAPI平台的列表内容
- `api stats`：显示API的使用情况和收入统计

## 工作流程

### 第1步：提取核心逻辑
针对每个微服务产品，确定其核心功能：
- **二维码生成器**：`generateQR(text, options) -> image`
- **发票生成器**：`createInvoice(data) -> PDF`
- **Markdown转换器**：`convertMarkdown(input, format) -> output`
- **JSON格式化工具**：`formatJSON(input, indent) -> formatted`
- **Base64编码器**：`encode/decode(input) -> output`

### 第2步：创建API路由
将API路由添加到现有的Next.js项目中：
`/src/app/api/v1/[endpoint]/route.ts`

API路由的结构包括：
- 从请求头（`X-API-Key`）中验证API密钥
- 实施速率限制：免费用户每天100次请求；付费用户无限制
- 解析请求体中的输入数据
- 调用核心功能函数
- 返回包含结果的JSON响应

### 第3步：API密钥管理
将API密钥存储在Supabase数据库中（如可用）或简单的JSON文件中：
`/home/milad/PRODUCT-SLUG/api-keys.json`

**定价层级**：
- **免费**：每天100次请求，基础功能
- **专业版（Pro）**：每月9美元，每天10,000次请求，所有功能
- **企业版（Enterprise）**：每月49美元，每天10,000次请求，优先支持及SLA服务

### 第4步：生成文档
为每个API生成OpenAPI/Swagger规范：
- API接口地址
- 认证方式
- 带有示例的请求/响应结构
- 错误代码
- 提供curl、JavaScript、Python等语言的代码示例

### 第5步：在RapidAPI平台上发布API
生成用于RapidAPI平台的列表内容：
- 标题：`[工具名称] API - [简短的功能描述]`
- 描述：200字以内介绍该API的用途
- 提供类别选择功能
- 将定价层级与RapidAPI的套餐对应起来
- 提供示例请求和响应数据

保存文件路径：`/home/milad/.openclaw/workspace/skills/api-monetizer/listings/PRODUCT-SLUG/`

## 收入模型

| 定价层级 | 价格 | 每天请求次数 | 收入目标 |
|------|-------|-------------|----------------|
| 免费 | $0 | 100 | 用于潜在客户获取（Lead Generation） |
| 专业版 | $9/月 | 10,000 | 主要收入来源 |
| 企业版 | $49/月 | 10,000 | 高价值收入来源 |

## 重要说明
- API货币化是一种额外的收入来源，不能替代Web界面的收入
- 实际的RapidAPI列表内容由人工上传（系统仅负责准备工作）
- API的使用情况需与Web界面的使用情况分开记录
- API密钥必须妥善保管，切勿以明文形式存储