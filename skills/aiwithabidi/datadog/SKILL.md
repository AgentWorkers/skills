---
name: datadog
description: "Datadog监控功能：通过REST API管理监控项、仪表板、指标、日志、事件和故障。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🐕", "requires": {"env": ["DD_API_KEY", "DD_APP_KEY"]}, "primaryEnv": "DD_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🐕 Datadog

Datadog 是一款用于监控的工具，支持通过 REST API 管理监控项、仪表板、指标、日志、事件和故障报告等功能。

## 所需配置

| 变量          | 必需      | 说明                          |
|-----------------|----------|---------------------------------------------|
| `DD_API_KEY`     | ✅       | 来自 app.datadoghq.com 的 API 密钥                |
| `DD_APP_KEY`     | ✅       | 应用程序密钥                        |

## 快速入门

```bash
# List monitors
python3 {{baseDir}}/scripts/datadog.py monitors --query <value> --tags <value>

# Get monitor
python3 {{baseDir}}/scripts/datadog.py monitor-get id <value>

# Create monitor
python3 {{baseDir}}/scripts/datadog.py monitor-create --name <value> --type <value> --query <value> --message <value>

# Update monitor
python3 {{baseDir}}/scripts/datadog.py monitor-update id <value> --name <value> --query <value>

# Delete monitor
python3 {{baseDir}}/scripts/datadog.py monitor-delete id <value>

# Mute monitor
python3 {{baseDir}}/scripts/datadog.py monitor-mute id <value>

# List dashboards
python3 {{baseDir}}/scripts/datadog.py dashboards

# Get dashboard
python3 {{baseDir}}/scripts/datadog.py dashboard-get id <value>
```

## 所有命令

| 命令           | 说明                          |
|-----------------|---------------------------------------------|
| `monitors`      | 列出所有监控项                        |
| `monitor-get`     | 获取特定监控项的信息                   |
| `monitor-create`   | 创建新的监控项                     |
| `monitor-update`   | 更新监控项的信息                   |
| `monitor-delete`   | 删除监控项                        |
| `monitor-mute`    | 静音某个监控项                     |
| `dashboards`     | 列出所有仪表板                     |
| `dashboard-get`    | 获取特定仪表板的信息                   |
| `dashboard-create`   | 创建新的仪表板                     |
| `dashboard-delete`   | 删除仪表板                        |
| `metrics-search`   | 搜索指标                        |
| `metrics-query`    | 查询指标数据                     |
| `events-list`    | 列出所有事件                        |
| `event-create`    | 创建新的事件                        |
| `logs-search`    | 搜索日志                         |
| `incidents`     | 列出所有故障报告                     |
| `incident-get`    | 获取特定故障报告的信息                 |
| `hosts`       | 列出所有主机                         |
| `downtimes`     | 列出所有主机停机时间                   |
| `downtime-create`   | 创建新的主机停机记录                 |
| `slos`        | 列出服务水平协议（SLOs）                   |
| `synthetics`     | 列出所有合成测试结果                   |
| `users`       | 列出所有用户                         |

## 输出格式

所有命令默认以 JSON 格式输出。若需以易读的格式输出，请添加 `--human` 参数。

```bash
python3 {{baseDir}}/scripts/datadog.py <command> --human
```

## 脚本参考

| 脚本          | 说明                          |
|-----------------|---------------------------------------------|
| `{{baseDir}}/scripts/datadog.py` | 主要的 CLI 脚本文件，包含所有命令                    |

## 致谢

该工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
更多内容请访问 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi)。  
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)