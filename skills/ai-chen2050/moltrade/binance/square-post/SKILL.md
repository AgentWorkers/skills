---
name: square-post
description: >
  将内容发布到 Binance Square（Binance 的社交平台，用于分享交易见解）。  
  当收到如“post to square”或“square post”之类的消息时，系统会自动执行发布操作。  
  支持发布纯文本形式的帖子。
metadata:
  author: binance-square
  version: "1.1"
---
# Square Post Skill

## 概述

用于将文本内容发布到 Binance Square 平台。

---

## API：添加内容

### 方法：POST

**URL**：
```
https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add
```

**请求头**：

| 头部字段 | 是否必填 | 说明 |
|--------|----------|-------------|
| X-Square-OpenAPI-Key | 是 | Square OpenAPI 密钥 |
| Content-Type | 是 | `application/json` |
| clienttype | 是 | `binanceSkill` |

**请求体**：

| 字段 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| bodyTextOnly | string | 是 | 发布的内容文本（支持使用 #标签） |

### 示例请求

```bash
curl -X POST 'https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add' \
  -H 'X-Square-OpenAPI-Key: your_api_key' \
  -H 'Content-Type: application/json' \
  -H 'clienttype: binanceSkill' \
  -d '{
    "bodyTextOnly": "BTC looking bullish today!"
  }'
```

### 响应示例

```json
{
  "code": "000000",
  "message": null,
  "data": {
    "id": "content_id_here"
  }
}
```

### 响应字段

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| code | string | `"000000"` 表示成功 |
| message | string | 错误信息（成功时为空） |
| data.id | string | 创建的内容 ID |

### 发布内容的 URL 格式

成功后，生成的发布内容 URL 为：
```
https://www.binance.com/square/post/{id}
```

示例：如果 `data.id` 的值为 `298177291743282`，则发布内容的 URL 为：
```
https://www.binance.com/square/post/298177291743282
```

---

## 错误处理

| 错误代码 | 说明 |
|------|-------------|
| 000000 | 成功 |
| 10004 | 网络错误，请重试 |
| 10005 | 仅允许已完成身份验证的用户使用该功能 |
| 10007 | 该功能当前不可用 |
| 20002 | 检测到敏感词汇 |
| 20013 | 内容长度超出限制 |
| 20020 | 不支持发布空内容 |
| 20022 | 检测到包含敏感词汇的内容 |
| 20041 | URL 存在潜在的安全风险 |
| 30004 | 未找到用户 |
| 30008 | 因违反平台规定而被封禁 |
| 220003 | 未找到 API 密钥 |
| 220004 | API 密钥已过期 |
| 220009 | 当天发布的帖子数量已达到限制 |
| 220010 | 不支持该类型的内容 |
| 220011 | 内容正文不能为空 |
| 2000001 | 账户被永久禁止发布内容 |
| 2000002 | 设备被永久禁止发布内容 |

---

## 认证

### 必需的请求头

| 头部字段 | 是否必填 | 说明 |
|--------|----------|-------------|
| X-Square-OpenAPI-Key | 是 | 用于发布内容的 Square OpenAPI 密钥 |

---

## 安全性

### 绝不显示完整的密钥

在向用户展示凭证时：
- **X-Square-OpenAPI-Key**：仅显示前 5 位和最后 4 位：`abc12...xyz9`

### 列出账户信息

在列出账户信息时，仅显示账户名称和描述，切勿显示完整的密钥：
```
Accounts:
* default (Default account for Square posting)
```

---

## 代理行为

1. **在调用 API 之前检查密钥**：确认 X-Square-OpenAPI-Key 已正确配置，且不是占位符 `your_api_key`。
2. **如果密钥缺失，提示用户提供**：如果密钥未配置，要求用户先提供他们的 API 密钥。
3. **如果内容缺失，提示用户提供内容**：如果用户尝试发布内容但未提供具体内容，询问他们想要发布什么。
4. **绝不显示完整的密钥**：仅显示前 5 位和最后 4 位（例如：`abc12...xyz9`）。
5. **存储用户提供的密钥**：当用户提供新的密钥时，更新本文件中的账户信息。
6. **发布前优化内容**：
   - 对用户的原始输入进行优化，以提高可读性。
   - 显示优化后的内容，并询问用户是使用优化后的版本还是原始内容进行发布。
7. **成功发布后返回 URL**：成功发布内容后，返回以下 URL：`https://www.binance.com/square/post/{id}`。
8. **处理 `data.id` 为空的情况**：如果响应代码为 `000000`，但 `data.id` 为空或缺失，告知用户发布可能已经成功，但 URL 无法获取，建议用户手动查看 Square 平台的页面。

---

## 注意事项

1. 目前仅支持纯文本形式的帖子。
2. 请检查每天的发布次数限制，以避免遇到错误代码 `220009`。