---
name: unifi
description: 通过 UniFi Site Manager API 监控 UniFi 网络基础设施。该 API 可用于列出所有主机/站点/设备/接入点（AP），并获取客户端/设备的基本统计信息（如总数等）。
metadata:
  openclaw:
    requires:
      env: ["UNIFI_API_KEY"]
      optionalEnv: ["UNIFI_BASE_URL"]
---

# UniFi Site Manager API

## 设置
- **必需项：** `UNIFI_API_KEY`（需设置为环境变量）*或* 在该文件旁边创建 `config.json` 文件（该文件会被 Git 忽略）。建议从 `config.json.example` 文件开始修改。
- 可选项：`UNIFI_BASE_URL`（默认值为 `https://api.ui.com`）。
- 该技能当前使用的是 **Site Manager API**（用于管理基础设施和设备信息）。除非通过扩展功能使用本地 Network API，否则不提供针对单个客户的跟踪功能。

## 命令
- `python3 scripts/unifi.py list-hosts`：列出所有主机信息。
- `python3 scripts/unifi.py list-sites`：列出所有站点信息。
- `python3 scripts/unifi.py list-devices`：列出所有设备信息。
- `python3 scripts/unifi.py list-aps`：列出所有应用（Application Profiles）信息。
- 使用 `--json` 选项可获取原始数据输出（JSON 格式）。