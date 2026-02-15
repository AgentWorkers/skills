---
name: linz-public-transport
description: 查询林茨公共交通（Linz Linien）的原始EFA（Electronic Fare Allocation）端点，以获取车站信息及实时出发信息。适用于需要搜索林茨公共交通车站、根据车站名称解析车站ID，或获取车站的即将出发的班次信息的任务。
metadata: {"homepage":"https://docs.openclaw.ai/tools/skills","env":["LINZ_TRANSPORT_API_BASE_URL"],"network":"required","version":"1.0.1","notes":"Uses Linz EFA endpoints /efa/XML_STOPFINDER_REQUEST and /efa/XML_DM_REQUEST at default base http://www.linzag.at/linz2"}
---

# 林茨公共交通

使用此技能与林茨公共交通（Linz Linien EFA）的终端进行交互：
- `GET /efa/XML_STOPFINDER_REQUEST`
- `GET /efa/XML_DM_REQUEST`

在实施之前，请阅读 `{baseDir}/references/endpoints.md` 中的终端详细信息。
默认执行路径为 `{baseDir}/scripts/linz_transport.py`。

## 工作流程
1. 确定 API 的基础 URL。
2. 运行与任务匹配的脚本子命令。
3. 返回一个简洁、用户友好的摘要。

## 主要工具
- 脚本路径：`{baseDir}/scripts/linz_transport.py`
- 运行时：仅使用 Python 3 的标准库。
- 基础 URL 输入方式：
  - 使用 `--base-url <url>` 参数
  - 或使用 `LINZ_TRANSPORT_API_BASE_URL` 环境变量
  - 默认值为 `http://www.linzag.at/linz2`

推荐的命令：
- 搜索车站：
  - `python {baseDir}/scripts/linz_transport.py stops "taubenmarkt"`
- 根据车站 ID 获取出发信息：
  - `python {baseDir}/scripts/linz_transport.py departures --stop-id 60501160 --limit 10`
- 一次性查询车站信息及出发时间：
  - `python {baseDir}/scripts/linz_transport.py next "taubenmarkt" --limit 10 --pick-first`

## 第一步：确定基础 URL
- 首先使用用户提供的基础 URL。
- 如果没有提供，则使用 `LINZ_TRANSPORT_API_BASE_URL`（如果存在）。
- 如果两者都不存在，则使用 `http://www.linzag.at/linz2`。

## 第二步：展示结果
- 如有需要，按 `countdownInMinutes` 降序排序结果。
- 除非用户要求显示更多信息，否则仅显示接下来的 5-10 个出发班次。
- 同时显示相对时间（`countdownInMinutes`）和绝对时间（`time`）。
- 在返回 JSON 数据时保持字段名称的一致性。

## 错误处理
- 如果搜索车站的结果为空，建议尝试使用相近的拼写并重新查询。
- 如果返回多个匹配结果，请使用明确的 `--stop-id` 参数；只有在可以接受结果不明确性的情况下，才使用 `next ... --pick-first`。
- 如果获取出发班次的信息为空，说明当前没有即将出发的班次。
- 如果 HTTP 请求失败，报告状态码、端点信息以及重试建议。
- 如果 EFA 的响应中包含 `message` 代码，请将该代码包含在错误诊断信息中。

## 最小示例

```bash
python {baseDir}/scripts/linz_transport.py stops "taubenmarkt"
python {baseDir}/scripts/linz_transport.py departures --stop-id 60501160 --limit 10
python {baseDir}/scripts/linz_transport.py next "taubenmarkt" --limit 10 --pick-first
```

```powershell
python "{baseDir}/scripts/linz_transport.py" stops "taubenmarkt"
python "{baseDir}/scripts/linz_transport.py" departures --stop-id 60501160 --limit 10
python "{baseDir}/scripts/linz_transport.py" next "taubenmarkt" --limit 10 --pick-first
```