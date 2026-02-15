---
name: ip-lookup
description: 获取当前的公共IP地址和地理位置信息。当用户询问IP地址、网络位置或想要查看自己的公共IP时，可以使用此功能。该功能既支持获取IP信息，也支持以清晰的方式显示这些信息。
---

# IP查询技能

## 概述

该技能提供了一种简单的方法来查看您的公共IP地址及其地理位置信息。

## 使用方法

当用户询问以下问题时：
- “我的IP地址是什么？”
- “我当前的IP地址是什么？”
- “我的公共IP地址是什么？”
- “我在哪里？”
- “我的位置在哪里？”
- “查询我的位置”
- “获取我的IP位置”
- “定位我”
- “IP地址是多少？”
- “你的IP地址是多少？”

请执行以下工作流程。

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

以清晰的方式呈现信息：

**IP地址：** [地址]
**位置：** [城市], [地区], [国家]
**ISP：** [ISP名称]
**组织：** [组织名称]

## 错误处理

如果主要服务（`myip.ipip.net`）失败：
1. 逐一尝试其他服务
2. 报告哪些服务成功了
3. 如果所有服务都失败，请告知用户网络问题