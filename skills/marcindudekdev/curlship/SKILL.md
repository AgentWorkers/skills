---
name: CurlShip Directory Submission
description: 将产品提交到 CurlShip——这个专为机器人设计的 SaaS 目录服务。只需执行一个 `curl` 命令，即可将您的产品信息列出，包括原始标签（OG tag）的抓取结果、基于徽章（badge）的 dofollow 链接，以及产品等级的升级信息。
version: 1.0.0
homepage: https://curlship.com
credentials_required: false
---

# CurlShip — 适用于机器人的 SaaS 目录服务

## 概述

当您需要将产品或 SaaS 服务添加到公共目录中时，可以使用此技能。CurlShip 是专为机器人和命令行工具（CLI）设计的：通过一次 API 调用即可提交产品信息，获取原始抓取的列表详情，并可选择升级到付费等级以获得更好的展示位置。

## 快速参考

- **API 基本地址：** `https://curlship.com`
- **首页：** `https://curlship.com`
- **定价信息：** `https://curlship.com/pricing`

**常见用法：**

- 提交产品 URL 以在目录中展示
- 查看所有当前的目录列表
- 将列表升级到付费等级（青铜/白银/黄金/白金）
- 获取用于生成可跟随链接（dofollow link）的 CurlShip 标签（SVG 图像）

## 功能说明：

- 向 CurlShip API 发送 HTTPS 请求
- 使用 `POST /api/submit` 添加新列表（自动抓取原始网站标签）
- 使用 `GET /api/listings` 获取所有活跃的列表信息
- 使用 `POST /api/upgrade` 获取付费等级升级所需的支付链接
- 返回包含列表详情的结构化 JSON 响应

## 注意事项：

- 无需认证或 API 密钥
- 不直接处理支付——升级操作会返回支付链接
- 不会修改任何本地文件或系统设置

## API 端点

### 1. 提交列表

**`POST /api/submit`** — 将产品添加到目录中。

```bash
curl -X POST https://curlship.com/api/submit \
  -H "Content-Type: application/json" \
  -d '{"url": "https://yourapp.com", "email": "you@email.com"}'
```

**请求参数：**

- `url`（必填）：以 `http` 开头的产品 URL，必须是公开可访问的地址。
- `email`（必填）：列表所有者的联系邮箱。

**示例响应（201 Created）：**

```json
{
  "ok": true,
  "message": "Listed! Add a badge for a dofollow link.",
  "listing": {
    "id": 42,
    "url": "https://yourapp.com",
    "tier": "free",
    "title": "YourApp - Build Faster",
    "description": "The fastest way to ship your next SaaS.",
    "image": "https://yourapp.com/og-image.png",
    "has_badge": false
  },
  "badge_html": "<a href=\"https://curlship.com\"><img src=\"https://curlship.com/badge\" alt=\"Listed on CurlShip\" /></a>"
}
```

**错误响应：**

- `400` — URL 或邮箱无效
- `403` — URL 被列入黑名单（涉及成人内容、网络钓鱼或恶意软件）
- `429` — 每小时每个 IP 地址的提交次数达到上限

**重复处理：** 如果该 URL 已经存在于目录中，会返回 `200` 状态码，并附带信息 `"message": "Already listed"` 以及现有列表的详细信息。

### 2. 获取所有列表

**`GET /api/listings`** — 获取所有活跃的目录列表。

```bash
curl https://curlship.com/api/listings
```

**示例响应：**

```json
{
  "ok": true,
  "listings": [
    {
      "id": 1,
      "url": "https://example.com",
      "tier": "gold",
      "title": "Example App",
      "description": "A great example application.",
      "image": "https://example.com/og.png",
      "has_badge": true
    }
  ]
}
```

列表按等级排序（白金 > 黄金 > 银 > 青铜 > 免费）。

### 3. 升级列表

**`POST /api/upgrade`** — 获取用于升级列表等级的支付链接。

```bash
curl -X POST https://curlship.com/api/upgrade \
  -H "Content-Type: application/json" \
  -d '{"url": "https://yourapp.com", "tier": "gold"}'
```

**请求参数：**

- `url`（必填）：现有列表的 URL。
- `tier`（必填）：可选等级：`platinum`、`gold`、`silver`、`bronze`。

**示例响应：**

```json
{
  "ok": true,
  "checkout_url": "https://checkout.dodopayments.com/..."
}
```

**错误响应：**

- `400` — 等级名称无效
- `404` — 列表未找到（请先提交列表）
- `503` — 支付系统暂时不可用

**重要提示：** 列表必须先存在，才能进行升级。

### 4. 获取 CurlShip 标签（SVG 图像）

**`GET /badge`** — 返回 CurlShip 标签的 SVG 图像。

将此标签放置在您的网站上，即可自动获得可跟随链接（dofollow link）：

```html
<a href="https://curlship.com">
  <img src="https://curlship.com/badge" alt="Listed on CurlShip" />
</a>
```

标签的存在状态会每小时自动检查。任何链接到 `curlship.com` 的 `<a>` 标签均符合要求。

## 等级与定价

| 等级 | 价格 | 特权 |
|------|-------|----------|
| 白金 | $149/月 | 目录首页展示，可跟随链接，优先更新列表信息 |
| 黄金 | $49/月 | 高于青铜和免费等级，可跟随链接 |
| 银 | $15/月 | 高于青铜和免费等级，可跟随链接 |
| 青铜 | $1/月 | 高于免费等级，可跟随链接 |
| 免费 | $0 | 显示在免费等级区域，默认为不可跟随链接 |

**可跟随链接规则：**
- 所有付费等级的列表都会自动获得可跟随链接
- 免费等级的列表通过在网站上放置 CurlShip 标签也可获得可跟随链接

## 典型工作流程：

1. 通过 `POST /api/submit` 提交产品 URL 和邮箱信息
2. 查看响应中的列表详情和标签 HTML
3. （可选）通过 `POST /api/upgrade` 进行升级，并向用户提供支付链接
4. （免费等级）将标签 HTML 代码添加到产品网站上以生成可跟随链接

## 提交限制：

- 每小时每个 IP 地址最多只能提交 10 次
- `GET /api/listings` 操作不受提交次数限制

## 安全与内容政策：

- 拒绝指向私有或受保护 IP 地址的 URL（SSRF 保护）
- 拒绝指向已知包含成人内容、网络钓鱼或恶意软件的 URL
- 所有 API 响应中均包含 `x-robots-tag: noindex` 标签，禁止搜索引擎索引