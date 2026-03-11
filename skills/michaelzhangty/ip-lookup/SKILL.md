---

# IP 查询工具

该工具可用于查询任意 IP 地址或主机名的相关信息，包括地理位置、ASN（自治系统编号）/ISP（互联网服务提供商）、反向 DNS（PTR）记录、RDAP/WHOIS 网络信息，以及可选的 AbuseIPDB 声誉检查。核心功能无需使用 API 密钥。适用于用户查询 IP 地址、进行地理位置定位、查找网络所有者、查询 IP 对应的 ISP 或 ASN、检查 IP 的恶意行为，或进行反向 DNS 查找等场景。常用查询语句包括：“这个 IP 属于谁？”、“这个 IP 位于哪里？”、“查询 IP 地址”、“检查 IP 是否恶意”等。

## 元数据
```json
{
  "openclaw": {
    "emoji": "mag:",
    "requires": ["python3"]
  }
}
```

---

## IP 查询功能

该工具可独立运行，无需依赖任何外部服务，能够整合四种数据源（地理位置、反向 DNS、RDAP/WHOIS 网络信息以及 AbuseIPDB 声誉检查），并将结果以清晰的终端报告形式输出。无需安装任何第三方库（仅依赖 Python 3 的标准库：`urllib`、`socket`、`json`、`argparse`），适用于所有安装了 Python 的系统，无需虚拟环境或依赖管理。

---

## 快速启动

```bash
python3 {baseDir}/scripts/ip_lookup.py 8.8.8.8
python3 {baseDir}/scripts/ip_lookup.py github.com
```

对于主机名，工具会先尝试将其解析为 IP 地址，然后再执行后续查询。

---

## 各个功能面板说明

### [地理位置]（始终启用）

该功能通过 `ip-api.com`（每分钟 45 次请求，免费使用，无需密钥）获取 IP 地理位置信息。如果 `ip-api.com` 停用，会自动切换到 `ipwho.is`。

返回信息包括：
- 国家、国家代码、地区、城市、邮政编码/ZIP 编码
- 纬度和经度坐标
- 时区（例如：America/New_York）
- ISP 名称及组织信息
- ASN（以 “AS12345 Name” 格式显示）
- 标志（如 PROXY、HOSTING/VPN、MOBILE，由 `ip-api.com` 通过启发式规则检测）

**示例输出（针对 8.8.8.8）：**
```
IP 地址        8.8.8.8
国家           美国 [US]
地区            弗吉尼亚州
城市              阿什本
时区          America/New_York
ISP               Google LLC
组织               Google Public DNS
ASN               AS15169 Google LLC
标志             HOSTING/VPN
```

### [反向 DNS]（默认启用，可通过 `--no-ptr` 选项禁用）

该功能会向 `dns.google` 查询 IP 的 PTR 记录，并将结果转换为 `in-addr.arpa` 格式。如果存在 PTR 记录，则返回对应的主机名；否则返回 “(no PTR record)”。

**用途：** 用于识别服务器主机名、确认 CDN 边缘节点（例如：`server-13-35-12-1.fra50.r.cloudfront.net`）以及验证 FCrDNS（正向确认的反向 DNS）信息。

### [RDAP/WHOIS]（默认启用，可通过 `--no-rdap` 选项禁用）

该功能首先向 `rdap.arin.net` 发起查询；对于欧洲地区的 IP 地址，会切换到 `rdap.db.ripe.net`。

返回信息包括：
- 网络名称（IP 块的注册名称，例如：APNIC-LABS、MSFT）
- CIDR 块（以 CIDR 格式表示，例如：1.1.1.0/24）
- 恶意行为联系人信息（从包含 “abuse” 字样的 RDAP 实体中提取）
- 注册日期和最后修改日期

**示例输出（针对 1.1.1.1）：**
```
网络名称      APNIC-LABS
CIDR 块         1.1.1.0/24
恶意行为联系人    helpdesk@apnic.net
注册日期      2011-08-10
最后修改日期    2023-04-26
```

### [AbuseIPDB 声誉检查]（可选，需使用免费 API 密钥）

该功能会通过 `api.abusei.pdb.com` 查询 IP 的恶意行为记录（查询历史为 90 天）。返回信息包括：
- 恶意行为置信度评分（0-100 分：0 表示无害，100 表示确认为恶意）
- 过去 90 天内的报告总数
- 最后一次报告的时间戳
- IP 的使用类型（例如：数据中心、网站托管、传输等）

**评分标准：**
- 0      ：无报告，很可能无害
- 1-25   ：低风险，可能是配置错误的服务器
- 26-75  ：可疑，需要进一步调查
- 76-100 ：高度可疑（可能是恶意工具、垃圾邮件来源、Tor 出口节点等）

---

## 各个选项说明

| 选项          | 功能                |
|-----------------|----------------------|
| --json       | 以 JSON 格式输出全部结果（不含 ANSI 颜色代码，便于管道传输）|
| --abuse      | 启用 AbuseIPDB 功能（需设置环境变量 ABUSEIPDB_KEY）|
| --no-rdap     | 跳过 RDAP/WHOIS 查询（更快，避免速率限制）|
| --no-ptr       | 跳过反向 DNS/PTR 查询            |

---

## 常用使用场景

- 仅查询地理位置：`python3 {baseDir}/scripts/ip_lookup.py 104.21.0.1 --no-rdap --no-ptr`
- 查找网络对应的恶意行为联系人：`python3 {baseDir}/scripts/ip_lookup.py 185.220.101.1`
- 检查 IP 是否被标记为恶意：`export ABUSEIPDB_KEY=your_key; python3 {baseDir}/scripts/ip_lookup.py 185.220.101.1 --abuse`
- 使用 JSON 格式输出结果：`python3 {baseDir}/scripts/ip_lookup.py 8.8.8.8 --json | python3 -c "import json, sys; d=json.load(sys.stdin); print(d['geo']['country'], d['geo']['as'])`
- 查询主机名（自动解析为 IP）：`python3 {baseDir}/scripts/ip_lookup.py suspicious-domain.example.com`

---

## AbuseIPDB 设置（只需一次操作）

1. 在 [https://www.abuseipdb.com/register](https://www.abuseipdb.com/register) 注册免费账户。
2. 进入控制台的 API 页面，创建 API 密钥（免费 tier 每天允许 1000 次查询）。
3. 设置环境变量：`export ABUSEIPDB_KEY=your_key_here`。

---

## 技术说明：
- 当输出不是通过 TTY（如管道、持续集成工具、日志文件）时，ANSI 颜色代码会自动关闭。
- 该工具支持 IPv6 地址的地理位置和 RDAP 查询；反向 DNS 查询仅支持 IPv4 地址。
- RDAP 查询首先尝试使用 ARIN 数据源，若无结果则切换到 RIPE 数据源。
- `ip-api.com` 的免费 tier 每分钟允许 45 次请求；超出限制会自动切换到 `ipwho.is`。
- 该工具不使用缓存，所有请求均为实时处理；批量查询时建议使用 `--no-rdap --no-ptr` 选项。
- 该工具仅依赖 Python 3 的标准库，无需安装额外的第三方库。