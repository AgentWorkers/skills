---
name: geo-ip
description: "查询任意 IP 地址的地理位置信息"
metadata:
  {
    "openclaw":
      {
        "emoji": "🌍",
        "requires": { "bins": ["curl"] },
        "install": [],
      },
  }
---

# 地理IP

可以使用ipinfo.io API查询任意IP地址的地理位置信息。返回内容包括城市、地区、国家、坐标以及ISP（互联网服务提供商）的相关信息。

## 命令

```bash
# Look up location for a specific IP address
geo-ip <ip-address>

# Look up your own public IP location
geo-ip me
```

## 安装

无需安装任何软件。系统上通常已经预装了`curl`工具，该工具会使用ipinfo.io的公共API来获取所需数据。