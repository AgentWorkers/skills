---
name: myclub
description: 从 myclub.fi 网站获取账户的体育赛事安排、训练信息、比赛详情以及相关活动。系统会自动识别您在 myclub.fi 账户中关联的账户和俱乐部信息。该功能可用于查看训练时间与地点、查找即将进行的比赛、浏览俱乐部活动或获取赛事日程概要。使用该功能需要您的 myclub.fi 账户凭证（这些凭证会存储在本地设备上）。
metadata:
  clawdbot:
    version: "1.0.0"
    author: "hanninen"
    homepage: "https://github.com/hanninen/myclub-skill"
requires:
  runtime: "python3"
  python: ">=3.10"
files: ["scripts/*"]
---
# myclub 技能

从 myclub.fi 获取体育赛事安排信息，包括训练时间、比赛日期、地点以及注册状态。

## 外部接口

该技能连接到以下外部服务：

- `id.myclub.fi` — 认证（通过 POST 请求并携带 CSRF 令牌进行登录）
- `*.myclub.fi` — 获取俱乐部页面和赛事安排信息（每个俱乐部都有自己的子域名）

不与其他外部服务进行交互。

## 安全性与隐私

- **凭证**：您的 myclub.fi 电子邮件地址和密码会以仅限所有者访问的权限（`0600`）存储在 `~/.myclub-config.json` 文件中。这些凭证仅用于在 `id.myclub.fi` 上进行认证，不会被发送到其他地方。
- **数据传输**：登录凭证通过 HTTPS 传输到 `id.myclub.fi`；赛事安排数据也通过 HTTPS 从 `*.myclub.fi` 获取。所有数据都不会被发送给第三方。
- **无数据收集**：该技能不收集任何分析数据或使用情况信息。
- **数据仅限本地使用**：所有解析后的赛事安排数据都会返回给调用该技能的程序，不会被存储或传输到其他地方。

## 信任声明

当数据离开您的设备时：您的 myclub.fi 电子邮件地址和密码会被发送到 `id.myclub.fi` 用于认证；赛事安排数据仅从 `*.myclub.fi` 获取。除非您信任 myclub.fi 并愿意提供自己的凭证，否则请勿安装此技能。

## 设置（一次性操作）

```bash
python3 scripts/fetch_myclub.py setup --username your_email@example.com --password your_password
```

凭证存储在 `~/.myclub-config.json` 文件中，权限设置为仅限所有者访问（`600`）。

## 命令

### discover

列出所有可用账户及其所属的俱乐部。

```bash
python3 scripts/fetch_myclub.py discover [--json]
```

**`--json`**：以 JSON 格式输出结果，而非格式化的文本。

### fetch

```bash
python3 scripts/fetch_myclub.py fetch --account "Account Name" [--period PERIOD | --start DATE [--end DATE]] [--json]
```

**`--period`**：可选值：`this week`（默认）、`next week`、`this month`、`next month`  
**`--start` / `--end`**：自定义日期范围（格式为 `YYYY-MM-DD`，可覆盖 `--period` 的设置）  
**`--json`**：以 JSON 格式输出结果，而非格式化的文本。

## 赛事字段

| 字段 | 描述 |
|-------|-------------|
| `id` | 唯一的赛事标识符 |
| `name` | 赛事名称 |
| `group` | 队伍或组别（例如：“P2015 Black”） |
| `venue` | 比赛地点 |
| `month` | 赛事开始的月份（格式为 YYYY-MM-DD） |
| `day` | 比赛日期（芬兰时间格式，例如：“15.3.”）；如不可用则显示 `null` |
| `time` | 比赛时间范围（例如：“17:00 - 18:00”）；如不可用则显示 `null` |
| `event_category` | 赛事类型（例如：“Harjoitus”（训练）、“Ottelu”（比赛）、“Turnaus”（锦标赛）、“Muu”（其他） |
| `type` | 根据内容自动推断的赛事类型（例如：训练、比赛、锦标赛、会议等） |
| `registration_status` | 来自 myclub.fi 的注册状态信息；可能为 “unknown” |

## 故障排除

- **“未找到 .myclub-config.json 文件”**：请先运行 `setup` 命令进行配置。
- **“账户 ‘Name’ 未知”**：运行 `discover` 命令检查账户名称的拼写（区分大小写）。
- **超时/认证错误**：使用 `discover` 命令验证凭证；检查网络连接是否正常。
- **JSON 解析失败**：可能是 myclub.fi 的页面结构发生了变化，请检查日历页面上是否包含 `data-events` 属性。

## 系统要求

需要 Python 3.10 及以上版本（无外部依赖，仅使用标准库）。