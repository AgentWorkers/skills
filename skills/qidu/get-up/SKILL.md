---
name: ip-lookup
description: 获取当前的公共IP地址和地理位置信息。当用户询问IP地址、网络位置或想要查看自己的公共IP时，可以使用该功能。该功能既支持获取IP信息，也支持以清晰的方式显示这些信息。
---

# IP查询技能

## 概述

该技能提供了一种简单的方法来查询您的公共IP地址及其地理位置信息。

## 使用方法

当用户提出以下问题时：
- “我的IP地址是什么？”
- “我当前的IP地址是多少？”
- “我位于哪里？”
- “查询我的IP地址”
- “我的公共IP地址是什么？”
- “你的IP地址是多少？”

请按照以下工作流程进行操作。

## 工作流程

### 基本IP查询

运行以下命令以获取您的公共IP地址和位置：

```bash
curl -s myip.ipip.net
```

示例输出：
```
Current IP：8.8.8.8  From: SF CA USA Google
Current IP：1.1.1.1  From: SF CA USA Cloudflare
```

### 替代方法

如果上述方法失败，请尝试以下替代方案：

**方法1：icanhazip.com（备用方案）**
```bash
curl -s icanhazip.com
```

**方法2：ipify API**
```bash
curl -s https://api.ipify.org
```

**方法3：ifconfig.me**
```bash
curl -s ifconfig.me
```

### 详细地理位置查询

如需更详细的地理位置信息：

```bash
curl -s https://ipinfo.io/$(curl -s https://api.ipify.org)/json
```

## 显示格式

以清晰的方式展示信息：

**IP地址：** [address]
**位置：** [city], [region], [country]
**ISP：** [ISP名称]
**组织：** [organization]

## 错误处理

如果主要服务（`myip.ipip.net`）失败：
1. 逐一尝试其他服务
2. 报告哪些服务成功了
3. 如果所有服务都失败，请告知用户网络问题