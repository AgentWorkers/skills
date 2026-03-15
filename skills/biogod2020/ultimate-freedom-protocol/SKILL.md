---
name: ultimate-freedom-protocol
description: "终极网络自由协议（Ultimate Web Freedom Protocol，版本9.0.0）。该协议利用“Protocol Phantom”技术（基于curl_cffi的内核级TLS伪装机制），能够绕过DataDome、Cloudflare和Bilibili等网络审查工具，实现服务器端数据的隐蔽提取。非常适合用于进行难以被检测到的数据采集操作。"
metadata:
  openclaw:
    emoji: 🎭
    disable-model-invocation: true
    requires:
      python: ["curl_cffi", "lxml", "DrissionPage"]
      bins: ["google-chrome-stable", "xvfb-run"]
---
# 终极自由协议（SOTA v9.0.0）

该协议使用**“Protocol Phantom”**技术替代了传统的无头浏览方式，重点在于内核级别的网络指纹识别。

## 🚀 核心技术：Protocol Phantom（CFFI模式）
传统的爬虫工具是通过TLS握手来识别的。本工具包使用`curl_cffi`在二进制层面模拟真实浏览器的行为。

### 主要功能：
- **JA4指纹识别**：与Chrome 124及更高版本、Safari iOS 17完美兼容。
- **WAF穿透**：已成功突破DataDome、Akamai以及Bilibili的412/403访问限制。
- **零资源消耗**：除非需要复杂的JavaScript交互，否则无需使用Xvfb或D-Bus等资源。

## 🛠️ 统一入口
`freedom_engine.py`为所有渗透任务提供了标准化的接口。

---
**版本**：9.0.0（Phantom Core） | **作者**：Biogod2020 | **状态**：生产可用（PROD）