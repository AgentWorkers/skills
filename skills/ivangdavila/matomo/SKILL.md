---
name: Matomo Analytics
slug: matomo
version: 1.0.1
homepage: https://clawic.com/skills/matomo
description: 通过 API 集成、自定义报告和目标跟踪功能，查询、分析和管理 Matomo 分析数据。
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以获取集成指南。该工具将配置信息存储在 `~/matomo/` 目录下。

## 使用场景

用户需要查询 Matomo 分析数据、生成报告、跟踪目标或管理自己托管的分析系统。该工具通过代理处理 API 请求、数据分析、访客洞察以及转化跟踪等功能。

## 架构

内存数据存储在 `~/matomo/` 目录下。具体结构请参阅 `memory-template.md` 文件。

```
~/matomo/
├── memory.md         # Sites, credentials ref, preferences
├── reports/          # Saved report templates
└── queries/          # Reusable API query templates
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 内存模板 | `memory-template.md` |
| API 参考 | `api.md` |
| 报告模板 | `reports.md` |

## 核心规则

### 1. 绝不泄露凭证信息
- 令牌（token）应存储在系统的密钥链或环境变量中，切勿保存在内存文件中。
- 仅通过引用名称来引用凭证信息。
- 如果用户在聊天中输入令牌，请警告其并建议使用安全的方式存储令牌。

### 2. 使用报告 API 进行数据查询
```bash
# Base pattern
curl -s "https://{matomo_url}/index.php?module=API&method={method}&idSite={site_id}&period={period}&date={date}&format=json&token_auth={token}"
```
常用方法：
- `VisitsSummary.get` — 访问者数量、访问次数、页面浏览量
- `ActionsgetPageUrls` — 热门页面
- `Referrers.getWebsites` — 流量来源
- `Goals.get` — 转化数据

### 3. 理解日期范围
| 时间范围 | 日期格式 | 例子 |
|--------|-------------|---------|
| `day` | `YYYY-MM-DD` | `2025-01-15` |
| `week` | `YYYY-MM-DD` | 包含该日期的整周 |
| `month` | `YYYY-MM` | `2025-01` |
| `year` | `YYYY` | `2025` |
| `range` | `YYYY-MM-DD,YYYY-MM-DD` | `2025-01-01,2025-01-31` |

特殊日期：`today`（今天）、`yesterday`（昨天）、`last7`（过去7天）、`last30`（过去30天）、`lastMonth`（上个月）、`lastYear`（去年）

### 4. 处理多站点配置
- 在进行查询前务必确认目标站点。
- 将站点列表及其对应的 ID 存储在 `memory.md` 文件中。
- 如果未配置，默认使用使用频率最高的站点。

### 5. 以易于理解的方式格式化数据
- 将百分比四舍五入到小数点后一位。
- 对于较大的数字，使用 K/M（千/百万）等后缀进行表示。
- 在比较数据时需考虑时间背景（例如与上周/上月相比）。
- 强调显著的变化（变化幅度超过 10%）。

### 6. 遵守速率限制
- 尽可能将相关查询集中在同一时间范围内进行。
- 将最近的结果缓存到内存中，以便后续查询。
- 避免在对话中重复查询相同的数据。

### 7. 使用分段（Segmentation）获取更深入的洞察
分段功能可根据访客属性过滤数据。在查询中添加 `&segment=` 参数即可：

```bash
# Mobile visitors only
&segment=deviceType==smartphone

# From specific country
&segment=countryCode==US

# Returning visitors who converted
&segment=visitorType==returning;goalConversionsSome>0

# Combine with AND (;) or OR (,)
&segment=browserCode==CH;operatingSystemCode==WIN
```

常用分段维度：
- `deviceType` — 智能手机、平板电脑、桌面电脑
- `browserCode` — CH（Chrome）、FF（Firefox）、SF（Safari）
- `countryCode` — ISO 2 位国家代码
- `visitorType` — 新访客、重复访问者
- `referrerType` — 直接访问、搜索、网站、活动推广

## 使用 Matomo 时需要注意的问题
- **使用错误的站点 ID** → 会导致查询错误，从而得到误导性的数据。务必先确认目标站点。
- **忘记提供令牌（token_auth）** → 会导致 403 错误或空响应。所有非公开接口都需要令牌。
- **日期格式错误** → 可能导致结果混乱。使用 `period=range` 时，日期格式应为 `date=start,end`。
- **混淆术语** — Matomo 使用的是“visits”而非“sessions”，“actions”而非“events”。请注意术语差异。
- **忽略分段设置** → 会错过重要的数据洞察。分段功能可根据访客属性过滤数据。

## 外部接口

| 接口 | 发送的数据 | 用途 |
|----------|-----------|---------|
| `{user_matomo_url}/index.php` | API 方法、站点 ID、时间范围、认证令牌 | 查询分析数据 |

该工具不会向外部发送任何数据。所有请求都发送到用户自己的 Matomo 实例。

## 安全性与隐私

**离开用户设备的数据：**
- API 请求仅发送到用户的 Matomo 实例。
- 请求中包含认证令牌（由用户控制）。

**保留在本地的数据：**
- 站点配置信息存储在 `~/matomo/` 目录下。
- 报告模板文件。
- 不会向第三方发送任何数据。

**该工具不会：**
- 以明文形式存储认证令牌。
- 向除用户 Matomo 之外的任何服务发送数据。
- 访问 `~/matomo/` 之外的文件。

## 相关工具
如果用户需要，可以使用以下命令安装相关工具：
- `clawhub install <slug>`：安装通用分析工具（`analytics`）
- `umami`：专注于隐私保护的分析工具
- `api`：REST API 集成工具

## 反馈建议
- 如果觉得本工具有用，请给它打星（`clawhub star matomo`）。
- 保持更新：`clawhub sync`