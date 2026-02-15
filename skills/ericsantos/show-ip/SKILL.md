---
name: show-ip
description: 显示服务器当前的公共 IP 地址。当被询问 IP 地址、公共 IP 或网络身份时，可以使用此信息。
---

# 公共 IP 地址

显示服务器当前的公共 IP 地址。

## 使用方法

运行脚本：
```bash
bash scripts/get-ip.sh
```

脚本将返回服务器的公共 IPv4 地址。如果服务器同时支持 IPv6，也会显示 IPv6 地址。