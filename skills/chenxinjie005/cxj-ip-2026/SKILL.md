---
name: my-ip-checker
description: 使用简单的 shell 命令获取公共（外部）和本地（内部）IP 地址。当用户询问他们的 IP 地址、公共 IP 地址或本地网络地址时，可以使用这些命令。
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["curl.exe"]}}}
---
# 我的IP检查工具

该工具可以检测当前机器的**公共（外部）IP地址**和**本地（内部）IP地址**。

## 第一步：获取公共IP地址

使用一个简单的HTTPS接口来获取你的公共IP地址（以纯文本形式返回）：

```bash
curl.exe -s https://ifconfig.me
````

如果该服务被阻止或响应缓慢，可以尝试使用以下地址：

```bash
curl.exe -s https://api.ipify.org
````

## 第二步：获取本地IPv4地址

在**Windows**（PowerShell或cmd）系统中：

```bash
ipconfig
````

然后从输出结果中筛选出包含“IPv4 地址”或“IPv4 Address”的行。

在**Linux**系统中：

```bash
hostname -I
````

通常会返回一个或多个由空格分隔的本地IP地址。

## 使用说明：

- 在配置防火墙、VPN或任何外部允许列表时，请使用第一步。
- 在调试局域网连接、端口转发或内部路由时，请使用第二步。
- 建议优先使用HTTPS接口，并避免使用API密钥；这些服务都是免费且匿名的。