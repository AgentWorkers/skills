---
name: go2gg
description: 使用 Go2.gg API 进行 URL 缩短、链接分析、二维码生成、Webhook 设置以及链接显示在个人简介页面的功能。当用户需要创建短链接、跟踪点击次数、生成二维码、设置个人简介页面或管理品牌化链接时，可以使用该服务。免费 tier 包含短链接、二维码和基本分析功能。使用该服务需要设置 `GO2GG_API_KEY` 环境变量；二维码生成功能无需身份验证即可免费使用。
---

# Go2.gg — 一款基于边缘计算的URL缩短服务

Go2.gg 提供 URL 缩短、数据分析、二维码生成、Webhook 配置以及个人简介中的链接插入等功能。该服务依托 Cloudflare 的边缘网络运行，实现全球范围内低于 10 毫秒的快速重定向。

## 设置

请从以下链接获取 API 密钥：  
https://go2.gg/dashboard/api-keys （免费，无需信用卡）

```bash
export GO2GG_API_KEY="go2_your_key_here"
```

**API 基础地址：** `https://api.go2.gg/api/v1`  
**认证方式：** `Authorization: Bearer $GO2GG_API_KEY`  
**文档：** https://go2.gg/docs/api/links

---

## 短链接管理

支持创建、管理和追踪短链接，可自定义链接别名（slug）、标签、过期时间、密码设置，并支持按地理位置或设备类型进行定向。

### 创建链接  
（具体代码块请参考 **CODE_BLOCK_1___**）

**注意：** 必须填写的字段是 `destinationUrl`（而非 `url`），链接别名（slug）是可选的（如未提供则自动生成）。

### 响应数据  
（具体代码块请参考 **CODE_BLOCK_2___**）

### 查看链接列表  
（具体代码块请参考 **CODE_BLOCK_3___**）

**查询参数：** `page`、`perPage`（最多 100 条）、`search`、`domain`、`tag`、`archived`、`sort`（按创建时间/点击次数/更新时间排序）

### 更新链接  
（具体代码块请参考 **CODE_BLOCK_4___**）

### 删除链接  
（具体代码块请参考 **CODE_BLOCK_5___**）

### 链接数据分析  
（具体代码块请参考 **CODE_BLOCK_6___**）

返回数据包括：`totalClicks`（总点击次数）、`byCountry`（按国家统计的点击数）、`byDevice`（按设备类型统计的点击数）、`byBrowser`（按浏览器统计的点击数）、`byReferrer`（来源链接统计的点击数）、`overTime`（按时间区间统计的点击数）。

### 高级链接设置  
（具体代码块请参考 **CODE_BLOCK_7___**）

### 创建链接时可设置的参数  
| 参数 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| destinationUrl | string | 是 | 需要重定向的目标 URL |
| slug | string | 否 | 自定义链接别名（未提供时自动生成） |
| domain | string | 否 | 自定义域名（默认：go2.gg） |
| title | string | 否 | 链接标题 |
| description | string | 否 | 链接描述 |
| tags | string[] | 否 | 用于过滤的标签 |
| password | string | 否 | 链接的密码保护设置 |
| expiresAt | string | 否 | ISO 8601 格式的过期时间 |
| clickLimit | number | 否 | 允许的最大点击次数 |
| geoTargets | object | 否 | 国家与 URL 的映射关系 |
| deviceTargets | object | 否 | 设备与 URL 的映射关系 |
| iosUrl | string | 否 | iOS 应用程序的深度链接 |
| androidUrl | string | 否 | Android 应用程序的深度链接 |
| utmSource/Medium/Campaign/Term/Content | string | 否 | UTM 参数 |

---

## 二维码生成  

支持生成可自定义的二维码。二维码生成功能免费且无需认证。

### 生成二维码（无需认证）  
（具体代码块请参考 **CODE_BLOCK_8___**）

### 二维码参数  
| 参数 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| url | string | 是 | 需要编码的 URL |
| size | number | 256 | 图像尺寸（64-2048 像素） |
| foregroundColor | string | #000000 | 图像前景颜色（十六进制代码） |
| backgroundColor | string | #FFFFFF | 图像背景颜色（十六进制代码） |
| cornerRadius | number | 0 | 图像边框半径（0-50） |
| errorCorrection | string | M | L（7%）、M（15%）、Q（25%）、H（30%） | 编码错误校正级别 |
| format | string | svg | 图像格式（svg 或 png） |

### 保存和追踪二维码（需要认证）  
（具体代码块请参考 **CODE_BLOCK_9___**）

---

## Webhook 功能  

支持实时接收链接点击、创建和更新的事件通知。

**可触发事件：** `click`（链接被点击）、`link.created`（链接创建）、`link.updated`（链接更新）、`linkdeleted`（链接删除）、`domain.verified`（自定义域名验证通过）、`qr.scanned`（二维码被扫描）、`*`（所有事件）。

Webhook 的响应数据中包含 `X-Webhook-Signature`（HMAC SHA256 签名）用于验证。重试间隔：5 秒 → 30 秒 → 2 分钟 → 10 分钟。

---

## 个人简介中的链接插入  

支持通过编程方式在个人简介中插入链接。

**可用主题：** 默认、极简、渐变、暗黑、霓虹、自定义（支持自定义 CSS）  
**链接类型：** 链接、标题栏链接、分隔符、嵌入式链接（如 YouTube 链接）、图片链接

---

## Python 示例  
（具体代码块请参考 **CODE_BLOCK_12___**）

---

## API 端点概览  

| 服务 | 端点 | 方法 | 认证方式 |
|---------|----------|--------|------|
| **链接管理** | `/api/v1/links` | POST | 是 |
| 查看链接列表 | `/api/v1/links` | GET | 是 |
| 获取链接详情 | `/api/v1/links/:id` | GET | 是 |
| 更新链接 | `/api/v1/links/:id` | PATCH | 是 |
| 删除链接 | `/api/v1/links/:id` | DELETE | 是 |
| 查看链接统计 | `/api/v1/links/:id/stats` | GET | 是 |
| **二维码生成** | `/api/v1/qr/generate` | POST | 不需要认证 |
| 保存二维码 | `/api/v1/qr` | POST | 是 |
| 查看二维码列表 | `/api/v1/qr` | GET | 是 |
| 下载二维码 | `/api/v1/qr/:id/download` | GET | 是 |
| **Webhook** | `/api/v1/webhooks` | 创建/读取/更新/删除 Webhook | 是 |
| **图片库** | `/api/v1/galleries` | 创建/读取/更新图片库内容 | 是 |
| 添加图片库项目 | `/api/v1/galleries/:id/items` | 创建/读取/更新图片库项目 | 是 |
| 发布图片库内容 | `/api/v1/galleries/:id/publish` | POST | 是 |

## 使用限制  

| 订阅计划 | 每分钟请求次数 |
|------|-------------|
| 免费 | 60 次 |
| 专业版 | 300 次 |
| 商业版 | 1000 次 |

## 错误代码  

| 代码 | 说明 |
|------|-------------|
| SLUG RESERVED | 链接别名已被占用 |
| SLUG_EXISTS | 该域名已使用相同的链接别名 |
| INVALID_URL | 目标 URL 不合法 |
| LIMIT_REACHED | 当前订阅计划的请求次数已达到上限 |
| DOMAIN_NOT_VERIFIED | 自定义域名未通过验证 |