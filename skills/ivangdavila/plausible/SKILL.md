---
name: Plausible
slug: plausible
version: 1.0.0
homepage: https://clawic.com/skills/plausible
description: 查询 Plausible Analytics API 以获取流量统计、来源链接、转化情况以及自定义事件的数据。
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":[],"env":["PLAUSIBLE_API_KEY"]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以获取集成指南。

## 使用场景

当用户需要从 Plausible 获取网站流量数据时，可以使用该技能。代理通过 Plausible API 查询访问者信息、页面浏览量、引用来源、目标事件以及自定义事件。

## 架构

数据存储在 `~/plausible/` 目录下。具体存储结构请参考 `memory-template.md`。

```
~/plausible/
├── memory.md     # Sites + preferences (no secrets stored)
└── queries/      # Saved query templates (optional)
```

## 快速参考

| 项目 | 对应文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 数据存储模板 | `memory-template.md` |

## 核心规则

### 1. API 密钥的获取方式
API 密钥来自 `PLAUSIBLE_API_KEY` 环境变量。切勿将密钥硬编码在代码中，也不要让用户通过聊天输入密钥。

### 2. 必需提供站点 ID
每次查询都需要提供站点 ID（域名）。请先查看 `memory.md` 以确认已配置的站点信息。

### 3. 时间范围
默认时间范围为 30 天；用户可自定义为 `day`、`7d`、`30d`、`month`、`6mo`、`12mo` 或 `custom`（需要指定日期范围）。

### 4. 可用的指标
| 指标 | 描述 |
|--------|-------------|
| `visitors` | 独立访问者数量 |
| `visits` | 总会话数 |
| `pageviews` | 总页面浏览量 |
| `views_per_visit` | 每次会话的页面浏览数 |
| `bounce_rate` | 单页访问率（百分比） |
| `visit_duration` | 平均会话时长（秒） |
| `events` | 自定义事件数量 |
| `conversion_rate` | 目标转化率（需要设置目标过滤条件） |

### 5. 数据维度
| 维度 | 描述 |
|-----------|-------------|
| `event:page` | 访问的页面 |
| `event:name` | 自定义事件 |
| `visit:source` | 流量来源 |
| `visit:referrer` | 完整的引用链接 |
| `visit:utm_source` | UTM 源 |
| `visit:utm_medium` | UTM 渠道 |
| `visit:utm_campaign` | UTM 活动 |
| `visit:device` | 设备类型（桌面/移动/平板电脑） |
| `visit:browser` | 浏览器名称 |
| `visit:os` | 操作系统 |
| `visit:country` | 国家代码 |
| `visit:city` | 城市名称 |

### 6. 过滤器语法
过滤器使用以下格式：`dimension==value` 或 `dimension!=value`；多个过滤器之间使用 `;`（表示 AND 关系）。

```
visit:source==Google
event:page==/pricing;visit:country==US
```

### 7. 请求限制
每个 API 密钥每小时最多允许 600 次请求。进行多次查询时，结果会缓存到内存中。

## 常见问题

- 忘记提供站点 ID → API 会返回 400 错误。
- 自定义时间范围的格式不正确 → 请使用 `YYYY-MM-DD` 格式。
- 未设置目标过滤条件就请求 `conversion_rate` → 结果为空。
- 未指定指标就查询数据统计 → 默认仅返回访问者数量。

## 外部接口

| 接口 | 发送的数据 | 用途 |
|----------|-----------|---------|
| https://plausible.io/api/v1/stats/realtime/visitors` | site_id | 实时访问者数量 |
| https://plausible.io/api/v1/stats/aggregate` | site_id, metrics, period, filters | 统计数据汇总 |
| https://plausible.io/api/v1/stats/timeseries` | site_id, metrics, period, interval | 时间序列数据 |
| https://plausible.io/api/v1/stats/breakdown` | site_id, property, metrics, filters | 按维度分类的数据统计 |

自托管实例使用 `memory.md` 中指定的自定义基础 URL。

其他数据不会被外部发送。

## 安全性与隐私

**会发送到外部的数据：**
- 站点 ID（域名）和查询参数（发送给 Plausible API）
- API 密钥（以Bearer 令牌的形式发送）

**保留在本地的数据：**
- 查询结果（缓存到内存中）
- 站点配置信息（存储在 `~/plausible/` 目录下）

**注意事项：**
- 该技能不会以明文形式存储 API 密钥（使用环境变量）。
- 仅发送查询所需的数据，不会泄露用户隐私。
- 不会访问 `~/plausible/` 目录之外的文件。

## 信任须知

使用该技能后，您的网站分析数据会发送到 Plausible（plausible.io 或自托管实例）。请确保您信任 Plausible 并同意其处理您的域名数据。

## 相关技能
如果用户同意，可以使用以下命令安装相关工具：
- `clawhub install <slug>`：安装通用分析工具
- `umami`：替代性的隐私分析工具
- `mixpanel`：产品分析工具

## 反馈建议：
- 如该技能有用，请给 `clawhub` 评分（例如：给它打星）。
- 为了获取最新信息，请使用 `clawhub sync` 命令。