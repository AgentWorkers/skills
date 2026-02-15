---
name: unifi
version: 1.1.1
homepage: https://github.com/odrobnik/unifi-skill
description: 通过 UniFi Site Manager API 监控 UniFi 网络基础设施。该 API 可用于列出所有主机/站点/设备/接入点（AP），并获取客户端/设备的基本统计信息（如数量等）。
metadata:
  openclaw:
    requires:
      env: ["UNIFI_API_KEY"]
      optionalEnv: ["UNIFI_BASE_URL"]
---

# UniFi 网站管理器 API

通过网站管理器 API 监控 UniFi 网络基础设施。

**入口点：** `{baseDir}/scripts/unifi.py`

## 设置

有关先决条件和设置说明，请参阅 [SETUP.md](SETUP.md)。

## 命令

```bash
python3 {baseDir}/scripts/unifi.py list-hosts
python3 {baseDir}/scripts/unifi.py list-sites
python3 {baseDir}/scripts/unifi.py list-devices
python3 {baseDir}/scripts/unifi.py list-aps
```

添加 `--json` 选项以获取原始输出。

## 注意事项
- 该工具使用的是 **网站管理器 API**（用于管理整个网络基础设施），而非针对单个客户端的跟踪功能。