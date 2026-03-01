---
name: vt-hash-intel
description: >
  **使用 VirusTotal 即时检测文件、URL、域名或 IP 是否具有恶意**  
  只需将任何 MD5/SHA1/SHA256 哈希值、URL、域名或 IP 地址粘贴到聊天框中，即可获得完整的威胁报告。该报告涵盖以下信息：  
  - 来自 70 多个安全引擎的检测结果  
  - 恶意软件家族信息  
  - YARA 匹配结果  
  - 沙箱测试结果  
  - DNS 记录  
  - WHOIS 信息  
  - 直接链接到 VirusTotal 的报告页面  
  支持单次查询或批量查询多种类型的 IOC（Indicator of Compromise，即恶意软件相关数据）。同时支持处理经过处理的 IOC 数据（格式如 `hxxp`、`[.]`）。  
  **适用场景**：  
  - 事件响应  
  - 威胁狩猎  
  - IOC 数据补充  
  - 安全运营（SOC）  
  - 日常安全监控  
  **使用建议**：  
  每当用户怀疑某个哈希值、URL、域名或 IP 地址可能存在恶意时，均可使用此功能进行检测。  
  **相关关键词**：  
  VirusTotal  
  MD5/SHA1/SHA256 哈希  
  URL  
  域名  
  IP 地址  
  恶意软件  
  威胁情报  
  IOC（Indicator of Compromise）
version: 2.0.0
metadata:
  openclaw:
    requires:
      env:
        - VT_API_KEY
---
# VT Hash 集成 — VirusTotal 威胁情报

您可以将任何 IOC（入侵指标，Indicator of Compromise）与 VirusTotal 的 70 多个安全引擎进行比对。该工具支持四种类型的 IOC：

| 类型 | 示例 | VT 终端地址 |
|---|---|---|
| **哈希值**（MD5/SHA1/SHA256） | `44d88612fea8a8f36de82e1278abb02f` | `/files/{hash}` |
| **URL** | `https://malicious-site.com/payload` | `/urls/{id}` |
| **域名** | `evil-domain.com` | `/domains/{domain}` |
| **IP 地址** | `1.2.3.4` | `/ip_addresses/{ip}` |

## 先决条件

必须设置 `VT_API_KEY` 环境变量。免费密钥：https://www.virustotal.com/gui/my-apikey

## 操作步骤

### 第 1 步：从用户输入中识别 IOC

脚本会自动检测 IOC 的类型：
- **哈希值**：32 个十六进制字符（MD5）、40 个十六进制字符（SHA1）、64 个十六进制字符（SHA256）
- **URL**：以 `http://` 或 `https://` 开头
- **IP 地址**：IPv4 格式（例如 `1.2.3.4`
- **域名**：其他所有包含点且具有有效顶级域名（TLD）的字符串（例如 `evil.com`）

脚本还会自动处理一些常见的转换：
- `hxxp://` → `http://`
- `hXXp://` → `http://`
- `evil[.]com` → `evil.com`
- `1[.]2[.]3[.]4` → `1.2.3.4`

### 第 2 步：执行查询

```bash
SKILL_DIR="$(dirname "$(find /root/.openclaw -name 'SKILL.md' -path '*/vt-hash-intel/*' 2>/dev/null | head -1)")"

# Single IOC (auto-detect type)
python3 "$SKILL_DIR/scripts/vt_lookup.py" <ioc>

# Mixed batch (hashes + URLs + domains + IPs together)
python3 "$SKILL_DIR/scripts/vt_lookup.py" <hash> <url> <domain> <ip>

# Force type if auto-detection is wrong
python3 "$SKILL_DIR/scripts/vt_lookup.py" --type domain example.com
```

### 第 3 步：解析并展示结果

JSON 输出始终包含以下字段：
- `ioc`：被查询的值
- `ioc_type`：`hash` | `url` | `domain` | `ip`
- `detection_ratio`：例如 “45/72”
- `threat_level`：`clean` | `low` | `medium` | `high`
- `threat_emoji`：✅ | ⚠️ | 🟠 | 🔴
- `detections`：标记该 IOC 的引擎列表
- `reputation`：VirusTotal 社区的信誉评分
- `vt_link`：直接链接到 VirusTotal 的报告
- `error`：如果出现错误，则显示错误信息

**针对哈希值的特定字段**：`sha256`、`md5`、`sha1`、`file_name`、`file_type`、`file_size_human`、`threat_label`、`popular_threat_name`、`crowdsourced_yara`、`sandbox_verdicts`、`sigma_rules`

**针对 URL 的特定字段**：`url`、`final_url`、`title`、`categories`

**针对域名的特定字段**：`registrar`、`creation_date`、`dns_records`、`categories`、`popularity_ranks`

**针对 IP 地址的特定字段**：`asn`、`as_owner`、`country`、`network`

### 第 4 步：格式化响应

**重要提示**：无论威胁级别如何，都必须提供完整的上下文分析。即使 IOC 被标记为 “clean”（未检测到任何威胁），上下文信息对于安全分析仍然非常有价值。VT 的 “clean” 结果并不意味着该 IOC 安全——它可能太新、具有针对性，或者尚未被提交到 VirusTotal 的数据库中。

**对于哈希值**：
- 显示判断结果（表情符号 + 危险级别 + 检测比例）
- 文件信息：名称、类型、大小、首次出现日期
- 威胁分类（如果为恶意）：家族名称、威胁标签
- 主要检测到的引擎（如果有）
- YARA 规则、沙箱检测结果、Sigma 规则（如果有）
- VirusTotal 的链接
- 上下文分析及建议

**对于 URL**：
- 显示判断结果
- URL 及最终重定向 URL（如果不同，则显示重定向路径——可能表明存在重定向链）
- 页面标题
- 安全供应商分配的类别
- 主要检测结果（如果有）
- VirusTotal 的链接
- 上下文分析：分析 URL 的模式是否可疑（例如随机字符串、可疑的顶级域名、常见的恶意文件路径模式，如 `/wp-content/uploads/*.exe`）
- 建议

**对于域名**：
- 无论是否安全，都必须显示以下信息：
- 判断结果
- 注册商及注册日期（如果是在过去 30 天内新注册的，则标记为可疑——这可能是钓鱼或恶意行为的迹象）
- DNS 记录（A、AAAA、MX、NS、TXT 记录——有助于识别托管信息和基础设施）
- 安全供应商提供的分类
- 人气排名（如果某个域名在排名中很低，则可能表示可疑）
- 信誉评分
- VirusTotal 的链接
- 上下文分析：注意域名是否非常新、使用了可疑的顶级域名、人气较低，或者使用了知名的防护型托管服务
- 建议

**对于 IP 地址**：
- 无论是否安全，都必须显示以下信息：
- 判断结果
- ASN 号码及 AS 所有者（有助于识别托管服务提供商——标记知名的防护型托管服务提供商）
- 国家（地理位置信息）
- 网络 CIDR 范围
- 信誉评分
- VirusTotal 的链接
- 上下文分析：注意 IP 是否属于云服务提供商、VPS、住宅代理或知名的托管服务提供商。如果相关，还需标记与恶意基础设施相关的国家。
- 建议

**威胁级别分类（所有类型相同）**：

| 恶意检测数量 | 危险级别 | 表情符号 |
|---|---|---|
| 0 | clean | ✅ |
| 1–5 | low | ⚠️ |
| 6–15 | medium | 🟠 |
| 16+ | high | 🔴 |

### 第 5 步：提供建议

根据威胁级别和上下文提供可操作的建议：
- **🔴 high**：立即在防火墙/EDR/代理中阻止该 IP，扫描环境中相关的 IOC，调查受影响的主机，收集来自 VirusTotal 的相关哈希值/域名/IP。
- **🟠 medium**：可能为恶意——隔离并调查，提交到沙箱进行检测，检查网络中的相关 IOC。
- **⚠️ low**：可能是误报——通过沙箱进行验证，检查文件/URL 的上下文和来源，进行监控。
- **✅ clean**：提供所有可用的上下文信息（ASN、国家、注册商、DNS、类别、信誉评分）。提醒用户：“VT 判断为 ‘clean’ 并不意味着绝对安全——该 IOC 可能太新、具有针对性，或者尚未被提交。建议查看其他威胁情报来源（如 AbuseIPDB、Shodan、URLhaus 等）。”
- **❓ not found**：从未提交到 VirusTotal 的数据库中——这并不意味着该 IOC 安全。建议将文件上传到 VirusTotal，或查看 AlienVault OTX、AbuseIPDB、URLhaus 以获取更多信息。

对于包含多种类型的结果，首先展示一个汇总表（IOC | 类型 | 判断结果 | 检测比例 | 关键发现），然后为每个条目提供详细报告。

## 错误处理

| 错误类型 | 原因 | 处理方式 |
|---|---|---|
| `NotFoundError` | IOC 未在 VirusTotal 数据库中 | “未在 VirusTotal 中找到。但这并不意味着该 IOC 是安全的。” |
| `AuthenticationError` | API 密钥错误或缺失 | “请检查 `.env` 文件中的 `VT_API_KEY`。” |
| `QuotaExceededError` | 达到速率限制 | “达到速率限制。请等待后再试。” |
| `UnrecognizedIOC` | 无法识别 IOC 类型 | “无法识别此 IOC 类型。尝试使用 `--type` 标志。” |
| `ConnectionError` | 网络问题 | “无法连接到 VirusTotal 的 API。请检查网络连接。” |

## 示例

**用户**：帮我查一下这个哈希值 `44d88612fea8a8f36de82e1278abb02f`  
**代理**：检测到 MD5 哈希值 → 执行查询 → 显示文件威胁报告。

**用户**：检查这个 URL：`https://suspicious-site.com/download.exe`  
**代理**：检测到 URL → 执行查询 → 显示包含类别和检测结果的 URL 分析报告。

**用户**：这个域名 `evil-domain.com` 安全吗？  
**代理**：检测到该域名 → 执行查询 → 显示包含 DNS、WHOIS 和检测结果的域名报告。

**用户**：查一下这些 IOC：  
`44d88612fea8a8f36de82e1278abb02f`  
`hxxps://bad-site[.]com/malware`  
`evil.com`  
`1.2.3.4`  
**代理**：检测到多种类型的 IOC → 执行批量查询 → 首先展示汇总表，然后按严重程度排序显示详细报告。