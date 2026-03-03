---
name: site-analyze
description: 网站机房溯源全维度分析工具。当用户需要查询某个网站的机房位置、CDN服务提供商、IP地址的归属地、网络路由链路、页面响应延迟、使用的SSL证书以及子域名等相关信息时，该工具可提供有力支持。该工具支持通过DNS over HTTPS（阿里/腾讯/360）进行查询，从而绕过UDP网络封锁；同时能够自动识别Cloudflare、Akamai、阿里云、腾讯云等主流的CDN服务提供商，并生成详细的溯源分析报告。
---
# Site Analyze — 网站基础设施追踪工具

该工具可运行9个分析模块，并为任意域名生成完整的基础设施报告。无需API密钥，支持任何具有出站HTTPS访问权限的网络环境。

## 使用方法

```bash
python3 scripts/site-analyze.py <domain>
```

支持输入简化的域名或完整的URL（系统会自动去除协议和路径部分）：

```bash
python3 scripts/site-analyze.py example.com
python3 scripts/site-analyze.py https://example.com/some/path
```

## 分析模块

| 编号 | 模块        | 方法                          |
|------|------------------|-----------------------------|
| 0    | DoH服务器探测    | 从8个候选服务器中自动检测可用的DNS-over-HTTPS服务器 |
| 1    | DNS解析      | 使用多台服务器进行DoH解析（Google/CF/Quad9/AliDNS/DNSPod/360/AdGuard/OpenDNS）；同时检查A/AAAA/MX/NS/TXT/SOA记录 |
| 2    | IP地理位置与CDN检测 | 通过ipinfo.io及内置的ASN数据库（Cloudflare、Akamai、Fastly、AWS、阿里云等）进行判断 |
| 3    | 子域名枚举      | 扫描常见子域名；标记非CDN服务的IP地址 |
| 4    | TCP延迟检测    | 使用Python socket库检测80和443端口的延迟；若IP使用Anycast技术会发出警告 |
| 5    | HTTP/HTTPS头部信息   | 通过curl提取相关头部信息（如CF-RAY、服务器信息、代理信息等） |
| 6    | HTTPS传输时间分析 | 分析DNS、TCP、TLS和TTFB（Time To First Byte）的传输时间；估算到边缘节点的单向RTT（Round-Trip Time） |
| 7    | SSL证书验证    | 使用openssl验证SSL证书的颁发者、主体、SAN（Subject Alternative Name）及有效期 |
| 8    | TCP追踪      | 使用tcptraceroute进行TCP路径追踪（若无tcptraceroute则使用ICMP追踪） |
| 9    | 总结与分析    | 自动标记出站的真实IP地址；提示可能隐藏在CDN后的真实服务器位置 |

## 结果解读

- **TCP延迟较低但TTFB较高**：目标网站可能使用了Anycast技术，实际服务器位于更远的位置 |
- 如果IP地址显示“anycast: true”，则TCP延迟反映的是最近的PoP（Point of Presence）位置，而非真实服务器位置；此时应参考TTFB数据 |
- 如果HTTP头部包含“CF-RAY”后缀，说明请求由Cloudflare的PoP节点处理（例如AMS代表阿姆斯特丹、SJC代表圣何塞等） |
- 如果502错误响应中包含“proxy-agent: VM-xxx-centos”，说明Cloudflare的错误导致服务器信息泄露 |
- 如果某个子域名解析结果为非CDN IP地址，该子域名可能是真实服务器所在地 |

## 所需依赖库

- Python 3.6及以上版本（仅需要标准库） |
- `curl`（用于发送HTTP请求和获取响应头部信息） |
- `openssl`（用于验证SSL证书） |
- `tcptraceroute`或`traceroute`（用于TCP路径追踪；如未安装则跳过此步骤）